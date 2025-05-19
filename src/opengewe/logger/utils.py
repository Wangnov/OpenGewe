"""日志工具模块

提供实用工具函数，如禁用/启用日志记录、拦截标准库日志等。
"""

import logging
import sys
import inspect
import os
import time
import uuid
import threading
import contextlib
from functools import wraps
from types import ModuleType
from typing import Optional, Dict, Any, List, Generator

from loguru import logger


# 请求上下文数据的线程本地存储
_request_context = threading.local()


def disable_logger(level: str = "INFO") -> None:
    """禁用特定级别及以下的日志记录

    Args:
        level: 要禁用的日志级别，默认为INFO
    """
    logger.disable(None)
    logger.enable(level)


def enable_logger() -> None:
    """启用所有日志记录"""
    logger.configure(handlers=[])
    logger.enable(None)


def reset_logger() -> None:
    """重置日志记录器配置"""
    logger.remove()


class LoggingInterceptHandler(logging.Handler):
    """拦截标准库日志并重定向到loguru的处理器"""

    def emit(self, record: logging.LogRecord) -> None:
        # 获取对应的loguru级别，默认为同名级别
        level = record.levelname
        frame = inspect.currentframe()
        depth = 2  # 默认深度

        # 传递数据到loguru
        while frame and depth > 0:
            frame = frame.f_back
            depth -= 1

        # 提取frame信息，或使用默认值
        file_path = record.pathname if frame is None else frame.f_code.co_filename
        function = record.funcName if frame is None else frame.f_code.co_name
        line = record.lineno if frame is None else frame.f_lineno

        # 从logging记录中提取模块名作为source
        module = record.module
        source = getattr(record, "source", module)

        # 确保source不为空
        if not source or source == "root":
            source = "Logging"

        # 获取当前请求ID（如果有）
        request_id = getattr(_request_context, "request_id", None)
        extra_kwargs = {
            "source": source,
            "file": file_path,
            "line": line,
            "function": function,
        }
        if request_id:
            extra_kwargs["request_id"] = request_id

        logger.bind(**extra_kwargs).opt(depth=0).log(level, record.getMessage())


def intercept_logging(level: Optional[str] = None) -> None:
    """拦截标准库日志，重定向到loguru

    Args:
        level: 日志级别，默认为None（使用root logger的级别）
    """
    # 获取根日志记录器
    logging_logger = logging.getLogger()

    # 如果指定了级别，则设置
    if level is not None:
        logging_logger.setLevel(getattr(logging, level))

    # 移除所有现有处理器
    if logging_logger.handlers:
        for handler in logging_logger.handlers[:]:
            logging_logger.removeHandler(handler)

    # 添加拦截处理器
    intercept_handler = LoggingInterceptHandler()
    logging_logger.addHandler(intercept_handler)


def log_function_call(logger=None, level="DEBUG"):
    """记录函数调用的装饰器

    Args:
        logger: 日志记录器，默认使用loguru.logger
        level: 日志级别，默认为DEBUG

    Returns:
        装饰函数的装饰器
    """
    if logger is None:
        logger = logger

    def decorator(func):
        name = func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            logger_ = logger.bind(source=f"{func.__module__}.{name}")
            signature = ", ".join(
                [repr(a) for a in args] + [f"{k}={repr(v)}" for k, v in kwargs.items()]
            )

            # 限制签名长度，避免日志过长
            if len(signature) > 300:
                signature = signature[:150] + "..." + signature[-150:]

            logger_.log(level, f"调用: {name}({signature})")

            try:
                result = func(*args, **kwargs)

                # 记录结果，但限制结果长度
                result_repr = repr(result)
                if len(result_repr) > 300:
                    result_repr = result_repr[:150] + "..." + result_repr[-150:]

                logger_.log(level, f"返回: {name} -> {result_repr}")
                return result
            except Exception as e:
                logger_.error(f"异常: {name} -> {type(e).__name__}: {e}")
                raise

        return wrapper

    return decorator


class RequestContext:
    """请求上下文管理器

    用于创建和管理请求追踪上下文，提供请求ID和分布式追踪支持。
    可以作为上下文管理器使用，或直接调用方法。

    示例:
        # 使用上下文管理器
        with RequestContext() as ctx:
            logger.info("在请求上下文中记录日志")

        # 直接使用
        RequestContext.set_request_id("custom-id")
        logger.info("使用自定义请求ID记录日志")
        RequestContext.clear()
    """

    # 追踪相关的请求头
    TRACE_HEADERS = {
        "x-request-id": "request_id",
        "x-trace-id": "trace_id",
        "x-span-id": "span_id",
        "x-parent-id": "parent_id",
    }

    @classmethod
    def generate_request_id(cls) -> str:
        """生成唯一的请求ID

        Returns:
            唯一请求ID
        """
        return str(uuid.uuid4())

    @classmethod
    def get_request_id(cls) -> Optional[str]:
        """获取当前请求ID

        Returns:
            当前请求ID，如果不存在则返回None
        """
        return getattr(_request_context, "request_id", None)

    @classmethod
    def set_request_id(cls, request_id: Optional[str] = None) -> str:
        """设置请求ID

        Args:
            request_id: 请求ID，如果为None则自动生成

        Returns:
            设置的请求ID
        """
        if request_id is None:
            request_id = cls.generate_request_id()

        _request_context.request_id = request_id
        return request_id

    @classmethod
    def get_trace_data(cls) -> Dict[str, Any]:
        """获取当前追踪数据

        Returns:
            包含所有追踪数据的字典
        """
        data = {}
        for key in cls.TRACE_HEADERS.values():
            value = getattr(_request_context, key, None)
            if value:
                data[key] = value

        # 添加请求计时信息
        if hasattr(_request_context, "request_start_time"):
            start_time = getattr(_request_context, "request_start_time")
            data["request_start_time"] = start_time
            data["request_duration"] = time.time() - start_time

        return data

    @classmethod
    def extract_from_headers(cls, headers: Dict[str, str]) -> Dict[str, str]:
        """从HTTP请求头中提取追踪信息

        Args:
            headers: HTTP请求头

        Returns:
            追踪信息字典
        """
        trace_data = {}

        # 处理标准追踪头
        for header, attr in cls.TRACE_HEADERS.items():
            if header in headers:
                trace_data[attr] = headers[header]

        # 如果没有请求ID但有追踪ID，使用追踪ID作为请求ID
        if "request_id" not in trace_data and "trace_id" in trace_data:
            trace_data["request_id"] = trace_data["trace_id"]

        # 如果仍然没有请求ID，生成一个
        if "request_id" not in trace_data:
            trace_data["request_id"] = cls.generate_request_id()

        return trace_data

    @classmethod
    def set_trace_data(cls, trace_data: Dict[str, Any]) -> None:
        """设置追踪数据

        Args:
            trace_data: 追踪数据字典
        """
        for key, value in trace_data.items():
            setattr(_request_context, key, value)

    @classmethod
    def clear(cls) -> None:
        """清除当前追踪上下文"""
        for key in list(vars(_request_context).keys()):
            delattr(_request_context, key)

    def __init__(
        self, request_id: Optional[str] = None, headers: Dict[str, str] = None
    ):
        """初始化请求上下文

        Args:
            request_id: 请求ID，如果为None则自动生成
            headers: HTTP请求头，用于提取追踪信息
        """
        self.generated_request_id = False

        if headers:
            # 从请求头提取追踪信息
            trace_data = self.extract_from_headers(headers)
            if request_id:
                trace_data["request_id"] = request_id
            self.trace_data = trace_data
        else:
            # 使用指定的请求ID或生成新的
            self.trace_data = {"request_id": request_id or self.generate_request_id()}
            self.generated_request_id = request_id is None

        # 添加请求开始时间
        self.trace_data["request_start_time"] = time.time()

    def __enter__(self) -> "RequestContext":
        """进入上下文时设置追踪数据"""
        self.set_trace_data(self.trace_data)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """退出上下文时清除追踪数据"""
        self.clear()


class BatchingSink:
    """批处理日志接收器

    将日志消息存储在内存缓冲区中，当达到指定的批处理大小或
    时间间隔时触发写入操作，减少I/O操作次数。

    Args:
        sink: 目标接收器（文件、函数等）
        batch_size: 批处理大小
        flush_interval: 刷新间隔（秒）
    """

    def __init__(
        self,
        sink: Any,
        batch_size: int = 100,
        flush_interval: float = 1.0,
    ):
        self.sink = sink
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.buffer: List[str] = []
        self.lock = threading.Lock()
        self.last_flush_time = time.time()

        # 启动定时刷新线程
        if flush_interval > 0:
            self.flush_thread = threading.Thread(
                target=self._timed_flush_worker,
                daemon=True,
            )
            self.flush_thread.start()
        else:
            self.flush_thread = None

        # 注册程序退出时的刷新
        import atexit

        atexit.register(self.flush)

    def __call__(self, message: str) -> None:
        """接收日志消息

        Args:
            message: 日志消息
        """
        with self.lock:
            self.buffer.append(message)

            # 如果达到批处理大小，执行刷新
            if len(self.buffer) >= self.batch_size:
                self._flush()

    def _flush(self) -> None:
        """内部刷新方法，必须在获取锁的情况下调用"""
        if not self.buffer:
            return

        # 如果接收器是可调用对象，则逐条传递消息
        if callable(self.sink):
            for message in self.buffer:
                self.sink(message)
        # 如果是文件类对象，则一次性写入所有消息
        elif hasattr(self.sink, "write"):
            for message in self.buffer:
                self.sink.write(message)
            if hasattr(self.sink, "flush"):
                self.sink.flush()

        # 清空缓冲区
        self.buffer.clear()
        self.last_flush_time = time.time()

    def flush(self) -> None:
        """手动刷新缓冲区"""
        with self.lock:
            self._flush()

    def _timed_flush_worker(self) -> None:
        """定时刷新工作线程"""
        while True:
            time.sleep(
                min(0.1, self.flush_interval)
            )  # 每0.1秒检查一次，最多不超过刷新间隔

            current_time = time.time()
            if current_time - self.last_flush_time >= self.flush_interval:
                self.flush()


def traced_function(name: Optional[str] = None, logger=None, level="INFO"):
    """跟踪函数执行并记录日志的装饰器

    用于跟踪函数执行时间并在请求上下文中记录日志。
    如果函数在请求上下文中执行，会继承该上下文。

    Args:
        name: 操作名称，默认为函数名
        logger: 日志记录器，默认使用loguru.logger
        level: 日志级别，默认为INFO

    Returns:
        装饰函数的装饰器
    """
    if logger is None:
        logger = logger

    def decorator(func):
        func_name = name or func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取或生成请求ID
            request_id = RequestContext.get_request_id()
            if not request_id:
                # 不在请求上下文中，创建临时上下文
                with RequestContext():
                    return _traced_execution(
                        func, func_name, logger, level, args, kwargs
                    )
            else:
                # 已在请求上下文中，直接执行
                return _traced_execution(func, func_name, logger, level, args, kwargs)

        return wrapper

    return decorator


def _traced_execution(func, func_name, logger, level, args, kwargs):
    """执行被跟踪的函数并记录日志"""
    start_time = time.time()
    log_context = {
        "operation": func_name,
        "request_id": RequestContext.get_request_id(),
    }

    logger.bind(**log_context).log(level, f"开始执行 {func_name}")

    try:
        result = func(*args, **kwargs)

        # 计算执行时间
        execution_time = time.time() - start_time
        log_context["execution_time"] = f"{execution_time:.6f}s"

        logger.bind(**log_context).log(
            level, f"完成执行 {func_name} (耗时: {execution_time:.6f}s)"
        )
        return result
    except Exception as e:
        # 计算执行时间
        execution_time = time.time() - start_time
        log_context["execution_time"] = f"{execution_time:.6f}s"
        log_context["error"] = str(e)
        log_context["error_type"] = type(e).__name__

        logger.bind(**log_context).exception(
            f"执行 {func_name} 失败 (耗时: {execution_time:.6f}s): {str(e)}"
        )
        raise


@contextlib.contextmanager
def log_group(
    name: str, logger=None, level="INFO", **context
) -> Generator[None, None, None]:
    """创建一个日志分组，用于对相关日志进行分组

    Args:
        name: 分组名称
        logger: 日志记录器，默认使用loguru.logger
        level: 日志级别，默认为INFO
        **context: 附加的上下文信息

    Yields:
        无
    """
    if logger is None:
        logger = logger

    # 获取或使用现有请求ID
    request_id = RequestContext.get_request_id()
    with_context = request_id is None

    try:
        # 如果没有请求上下文，创建一个临时的
        if with_context:
            ctx = RequestContext()
            ctx.__enter__()

        # 记录分组开始日志
        log_ctx = {"group": name, **context}
        if request_id:
            log_ctx["request_id"] = request_id

        logger.bind(**log_ctx).log(level, f"开始: {name}")
        start_time = time.time()

        yield

        # 记录分组结束日志
        duration = time.time() - start_time
        log_ctx["duration"] = f"{duration:.6f}s"
        logger.bind(**log_ctx).log(level, f"结束: {name} (耗时: {duration:.6f}s)")

    finally:
        # 清理临时请求上下文
        if with_context:
            ctx.__exit__(None, None, None)


# 用于记录日志调用源的插件路径识别
class PluginLoggerProxy:
    """代理loguru.logger对象，自动标记插件来源"""

    def __init__(self, original_logger):
        self._original_logger = original_logger
        self._plugin_name = None

    def _detect_plugin_name(self):
        """从调用栈中检测插件名称"""
        frame = inspect.currentframe()

        try:
            # 向上遍历调用栈，查找插件来源
            for _ in range(20):  # 限制查找深度
                if frame is None:
                    break

                module_name = frame.f_globals.get("__name__", "")
                filename = frame.f_code.co_filename

                # 检查是否是插件目录中的文件
                if "plugins/" in filename or "plugins\\" in filename:
                    plugin_parts = filename.split(os.path.sep)
                    plugin_idx = -1

                    # 查找plugins目录的索引
                    for i, part in enumerate(plugin_parts):
                        if part == "plugins" and i + 1 < len(plugin_parts):
                            plugin_idx = i + 1
                            break

                    if plugin_idx != -1 and plugin_idx < len(plugin_parts):
                        plugin_name = plugin_parts[plugin_idx]
                        return f"Plugin.{plugin_name}"

                # 或者从模块名称中提取
                if module_name.startswith("plugins."):
                    parts = module_name.split(".")
                    if len(parts) > 1:
                        return f"Plugin.{parts[1]}"

                frame = frame.f_back

            return "Plugin.Unknown"
        finally:
            del frame  # 避免循环引用

    def __getattr__(self, name):
        # 获取原始logger的属性
        attr = getattr(self._original_logger, name)

        # 如果是日志级别方法，包装它以添加source绑定
        if name in [
            "trace",
            "debug",
            "info",
            "success",
            "warning",
            "error",
            "critical",
        ]:

            @wraps(attr)
            def wrapped_log_method(*args, **kwargs):
                plugin_name = self._detect_plugin_name()
                context = {"source": plugin_name}

                # 添加请求ID（如果存在）
                request_id = RequestContext.get_request_id()
                if request_id:
                    context["request_id"] = request_id

                return self._original_logger.bind(**context).log(
                    name.upper(), *args, **kwargs
                )

            return wrapped_log_method

        # 对bind方法特殊处理，确保source被正确设置
        if name == "bind":

            @wraps(attr)
            def wrapped_bind(*args, **kwargs):
                if "source" not in kwargs:
                    plugin_name = self._detect_plugin_name()
                    kwargs["source"] = plugin_name

                # 添加请求ID（如果存在且未指定）
                if "request_id" not in kwargs:
                    request_id = RequestContext.get_request_id()
                    if request_id:
                        kwargs["request_id"] = request_id

                return attr(*args, **kwargs)

            return wrapped_bind

        # 对log方法特殊处理
        if name == "log":

            @wraps(attr)
            def wrapped_log(level, *args, **kwargs):
                plugin_name = self._detect_plugin_name()
                context = {"source": plugin_name}

                # 添加请求ID（如果存在）
                request_id = RequestContext.get_request_id()
                if request_id:
                    context["request_id"] = request_id

                return self._original_logger.bind(**context).log(level, *args, **kwargs)

            return wrapped_log

        # 返回原始属性
        return attr


# 保存原始loguru模块
_original_loguru = sys.modules.get("loguru")
_original_logger = logger


def intercept_plugin_loguru():
    """拦截插件对loguru的使用，自动添加插件来源标识

    这个函数通过替换sys.modules中的loguru模块，确保插件导入loguru时
    获取的是我们的自定义版本，从而在日志记录时自动添加插件来源。
    """

    # 创建一个新的loguru模块，包装原始logger
    class CustomLoguru(ModuleType):
        """自定义loguru模块，代替原始模块"""

        def __init__(self):
            super().__init__("loguru")
            # 复制原始loguru模块的所有属性
            self.__dict__.update(_original_loguru.__dict__)
            # 使用代理替换logger
            self.logger = PluginLoggerProxy(_original_logger)

    # 使用自定义模块替换sys.modules中的loguru
    custom_loguru = CustomLoguru()
    sys.modules["loguru"] = custom_loguru

    # 同时替换logger全局变量，因为有些代码可能直接导入了logger
    if "logger" in sys.modules.get("loguru", {}).__dict__:
        sys.modules["loguru"].__dict__["logger"] = custom_loguru.logger
