"""日志工具模块

提供实用工具函数，如禁用/启用日志记录、拦截标准库日志等。
"""

import logging
import sys
import inspect
import os
from functools import wraps
from types import ModuleType
from typing import Optional, Dict, Any, Callable, Union

from loguru import logger


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

        logger.bind(
            source=source,
            file=file_path,
            line=line,
            function=function
        ).opt(depth=0).log(level, record.getMessage())


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
                [repr(a) for a in args] +
                [f"{k}={repr(v)}" for k, v in kwargs.items()]
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
                if 'plugins/' in filename or 'plugins\\' in filename:
                    plugin_parts = filename.split(os.path.sep)
                    plugin_idx = -1
                    
                    # 查找plugins目录的索引
                    for i, part in enumerate(plugin_parts):
                        if part == "plugins" and i+1 < len(plugin_parts):
                            plugin_idx = i+1
                            break
                            
                    if plugin_idx != -1 and plugin_idx < len(plugin_parts):
                        plugin_name = plugin_parts[plugin_idx]
                        return f"Plugin.{plugin_name}"
                        
                # 或者从模块名称中提取
                if module_name.startswith('plugins.'):
                    parts = module_name.split('.')
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
        if name in ["trace", "debug", "info", "success", "warning", "error", "critical"]:
            @wraps(attr)
            def wrapped_log_method(*args, **kwargs):
                plugin_name = self._detect_plugin_name()
                return self._original_logger.bind(source=plugin_name).log(name.upper(), *args, **kwargs)
            return wrapped_log_method
            
        # 对bind方法特殊处理，确保source被正确设置
        if name == "bind":
            @wraps(attr)
            def wrapped_bind(*args, **kwargs):
                if "source" not in kwargs:
                    plugin_name = self._detect_plugin_name()
                    kwargs["source"] = plugin_name
                return attr(*args, **kwargs)
            return wrapped_bind
            
        # 对log方法特殊处理
        if name == "log":
            @wraps(attr)
            def wrapped_log(level, *args, **kwargs):
                plugin_name = self._detect_plugin_name()
                return self._original_logger.bind(source=plugin_name).log(level, *args, **kwargs)
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