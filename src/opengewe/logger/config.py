"""日志配置模块

提供基于loguru的日志配置和格式化功能。
"""

import os
import sys
import json
from typing import Dict, Optional, Any, List, Union, Callable

from loguru import logger

from opengewe.logger.formatters import (
    format_console_message,
    should_escape_message,
)

# 默认日志目录
DEFAULT_LOG_DIR = "logs"

# 日志级别对应的emoji
LEVEL_EMOJIS = {
    "TRACE": "🔍",
    "DEBUG": "🐛",
    "INFO": "ℹ️ ",
    "SUCCESS": "✅",
    "WARNING": "⚠️ ",
    "ERROR": "❌",
    "CRITICAL": "🔥",
}

# 存储当前全局日志级别
_GLOBAL_LOG_LEVEL = "INFO"

# 存储全局配置项
_LOGGER_CONFIG = {
    "console": True,
    "file": True,
    "level": "INFO",
    "format": "color",  # 可选值: "color", "simple", "json"
    "stdout": True,  # 是否将日志输出到标准输出
    "show_source": True,  # 是否显示日志源
    "show_time": True,  # 是否显示时间
}


# 获取全局日志级别
def get_global_log_level() -> str:
    """获取当前全局日志级别

    Returns:
        str: 当前设置的全局日志级别
    """
    return _GLOBAL_LOG_LEVEL


# 获取日志格式
def get_log_format() -> str:
    """获取当前日志格式

    Returns:
        str: 当前设置的日志格式
    """
    return _LOGGER_CONFIG.get("format", "color")


# 默认日志格式 - 使用居中对齐
DEFAULT_CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level.name: ^8}</level> {extra[level_emoji]} | "
    "<cyan>[{extra[source]}]</cyan> - "
    "{message}"
)

# 简单的控制台格式
SIMPLE_CONSOLE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "{level.name: ^8} | "
    "[{extra[source]}] - "
    "{message}"
)

DEFAULT_FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "{level.name: ^8} {extra[level_emoji]} | "
    "[{extra[source]}] | "
    "{file}:{line} - "
    "{message}"
)

# 结构化日志默认JSON格式
DEFAULT_JSON_FORMAT = {
    "time": "{time:YYYY-MM-DD HH:mm:ss}",
    "level": "{level.name}",
    "source": "{extra[source]}",
    "message": "{message}",
    "file": "{file}",
    "line": "{line}",
    "function": "{function}",
    "thread": "{thread.id}",
    "process": "{process.id}",
    "exception": "{exception}",
}

# 默认处理器配置
DEFAULT_HANDLERS = [
    # 添加API日志文件，记录所有API请求
    {
        "sink": "logs/api_{time:YYYY-MM-DD}.log",
        "level": "INFO",
        "rotation": "1 day",
        "retention": "30 days",
        "compression": "zip",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level.name: ^8} {extra[level_emoji]} | [{extra[source]}] | {message}",
        "filter": lambda record: "API" in record["extra"].get("source", "") 
                              or "api" in record["message"].lower()
                              or "请求" in record["message"]
                              or "响应" in record["message"],
    },
    # 添加DEBUG级别日志文件，记录详细信息
    {
        "sink": "logs/debug_{time:YYYY-MM-DD}.log",
        "level": "DEBUG",
        "rotation": "1 day",
        "retention": "30 days",
        "compression": "zip",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level.name: ^8} {extra[level_emoji]} | [{extra[source]}] | {file}:{line} - {message}",
    },
    # 添加特殊日志文件，专门记录调度任务相关信息
    {
        "sink": "logs/scheduler_{time:YYYY-MM-DD}.log",
        "level": "DEBUG",
        "rotation": "1 day",
        "retention": "30 days",
        "compression": "zip",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level.name: ^8} {extra[level_emoji]} | [{extra[source]}] | {message}",
        "filter": lambda record: "scheduler" in record["message"].lower()
        or "task" in record["message"].lower()
        or "job" in record["message"].lower()
        or "Scheduler" in record["extra"].get("source", ""),
    },
    # 添加错误日志文件
    {
        "sink": "logs/error_{time:YYYY-MM-DD}.log",
        "level": "ERROR",
        "rotation": "1 day",
        "retention": "30 days",
        "compression": "zip",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level.name: ^8} {extra[level_emoji]} | [{extra[source]}] | {file}:{line} - {message}",
        "backtrace": True,
        "diagnose": True,
    },
    # 添加插件日志文件
    {
        "sink": "logs/plugins_{time:YYYY-MM-DD}.log",
        "level": "DEBUG",
        "rotation": "1 day",
        "retention": "30 days",
        "compression": "zip",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level.name: ^8} {extra[level_emoji]} | [{extra[source]}] | {message}",
        "filter": lambda record: "Plugin" in record["extra"].get("source", "") 
                              or record["extra"].get("source", "").startswith("Plugins."),
    },
]


def create_batching_sink(sink, batch_size, flush_interval):
    """创建批处理接收器

    为了避免循环导入问题，动态导入 BatchingSink

    Args:
        sink: 接收器
        batch_size: 批处理大小
        flush_interval: 刷新间隔

    Returns:
        批处理接收器
    """
    from opengewe.logger.utils import BatchingSink

    return BatchingSink(sink, batch_size, flush_interval)


def configure_from_dict(config: Dict[str, Any]) -> None:
    """从字典配置日志系统

    Args:
        config: 配置字典，包含日志相关配置项
    """
    # 更新全局配置
    global _LOGGER_CONFIG
    _LOGGER_CONFIG.update({k: v for k, v in config.items() if k in _LOGGER_CONFIG})
    
    # 提取主要配置项
    level = config.get("level", "INFO")
    format_type = config.get("format", "color")
    log_dir = config.get("path", DEFAULT_LOG_DIR)
    console = config.get("stdout", True)
    
    # 解析日志轮转参数
    rotation = config.get("rotation", "1 day")
    retention = config.get("retention", "30 days")
    compression = config.get("compression", "zip")
    
    # 根据format_type选择格式
    if format_type == "json":
        structured = True
        console_format = lambda record: format_structured_record(record, DEFAULT_JSON_FORMAT)
    elif format_type == "simple":
        structured = False
        console_format = SIMPLE_CONSOLE_FORMAT
    else:  # 默认彩色格式
        structured = False
        console_format = DEFAULT_CONSOLE_FORMAT
    
    # 配置日志系统
    setup_logger(
        console=console,
        file=True,
        level=level,
        log_dir=log_dir,
        rotation=rotation,
        retention=retention,
        compression=compression,
        console_format=console_format,
        structured=structured,
    )


def setup_logger(
    console: bool = True,
    file: bool = True,
    level: str = "INFO",
    log_dir: str = DEFAULT_LOG_DIR,
    rotation: str = "1 day",
    retention: str = "30 days",
    compression: str = "zip",
    console_format: Union[str, Callable] = DEFAULT_CONSOLE_FORMAT,
    file_format: Union[str, Callable] = DEFAULT_FILE_FORMAT,
    backtrace: bool = True,
    diagnose: bool = True,
    enqueue: bool = True,
    workers: int = 1,  # 保留参数但不再直接传递给loguru
    queue_size: int = 1000,  # 保留参数但不再直接传递给loguru
    batch_size: int = 0,
    flush_interval: float = 0.0,
    structured: bool = False,
    json_format: Optional[Dict[str, str]] = None,
    custom_handlers: List[Dict[str, Any]] = None,
) -> None:
    """配置日志记录器

    Args:
        console: 是否输出到控制台
        file: 是否记录到文件
        level: 日志级别，默认INFO
        log_dir: 日志文件目录
        rotation: 日志轮换策略
        retention: 日志保留时间
        compression: 日志压缩方式
        console_format: 控制台输出格式
        file_format: 文件记录格式
        backtrace: 是否显示回溯信息
        diagnose: 是否显示诊断信息
        enqueue: 是否启用多进程安全的异步写入
        workers: 异步处理的工作线程数，已弃用，保留参数以兼容旧代码
        queue_size: 异步队列大小，已弃用，保留参数以兼容旧代码
        batch_size: 批处理大小，设为0禁用批处理
        flush_interval: 批处理刷新间隔(秒)，设为0禁用自动刷新
        structured: 是否启用结构化日志(JSON格式)
        json_format: 自定义JSON格式，仅当structured=True时有效
        custom_handlers: 自定义处理器配置列表，如果为None则使用默认处理器
    """
    # 设置全局日志级别
    global _GLOBAL_LOG_LEVEL
    _GLOBAL_LOG_LEVEL = level.upper()

    # 更新formatters模块中的全局日志级别变量
    import opengewe.logger.formatters

    opengewe.logger.formatters.GLOBAL_LOG_LEVEL = level.upper()

    # 重置当前记录器
    logger.remove()

    # 确保日志目录存在
    if file and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # 配置通用选项
    logger.configure(
        handlers=[],
        extra={
            "source": "OpenGewe",
            "level_emoji": "",
            "request_id": None,
        },  # 默认源标识、emoji和request_id
        patcher=lambda record: record.update(
            extra={
                **record["extra"],
                "level_emoji": LEVEL_EMOJIS.get(record["level"].name, ""),
            },
            message=format_console_message(record)
            if should_escape_message(record["message"])
            else record["message"],
        ),
    )

    # 添加控制台处理器
    if console:
        # 使用结构化日志格式（如果启用）
        actual_format = console_format
        if structured and not callable(actual_format):
            def actual_format(record):
                return format_structured_record(
                    record, json_format or DEFAULT_JSON_FORMAT
                )

        # 如果需要批处理，使用BatchingSink包装sink
        if batch_size > 0:
            sink = create_batching_sink(sys.stderr, batch_size, flush_interval)
        else:
            sink = sys.stderr

        logger.add(
            sink,
            level=level,
            format=actual_format,
            colorize=True,
            backtrace=backtrace,
            diagnose=diagnose,
            enqueue=enqueue,
        )

    # 添加文件处理器 - 常规日志
    if file:
        # 使用结构化日志格式（如果启用）
        actual_format = file_format
        if structured and not callable(actual_format):
            def actual_format(record):
                return format_structured_record(
                    record, json_format or DEFAULT_JSON_FORMAT
                )

        # 常规日志文件路径
        log_file = os.path.join(log_dir, "opengewe_{time:YYYY-MM-DD}.log")

        # 如果需要批处理，使用BatchingSink
        if batch_size > 0:
            # 创建一个带有批处理的接收器
            logger.add(
                create_batching_sink(log_file, batch_size, flush_interval),
                level=level,
                format=actual_format,
                rotation=rotation,
                retention=retention,
                compression=compression,
                backtrace=backtrace,
                diagnose=diagnose,
                enqueue=enqueue,
            )
        else:
            # 直接添加标准文件接收器
            logger.add(
                log_file,
                level=level,
                format=actual_format,
                rotation=rotation,
                retention=retention,
                compression=compression,
                backtrace=backtrace,
                diagnose=diagnose,
                enqueue=enqueue,
            )

        # 添加文件处理器 - 调试日志（更详细）
        debug_file = os.path.join(log_dir, "debug_{time:YYYY-MM-DD}.log")
        if batch_size > 0:
            logger.add(
                create_batching_sink(debug_file, batch_size, flush_interval),
                level="DEBUG",
                format=actual_format,
                rotation=rotation,
                retention=retention,
                compression=compression,
                backtrace=backtrace,
                diagnose=diagnose,
                enqueue=enqueue,
            )
        else:
            logger.add(
                debug_file,
                level="DEBUG",
                format=actual_format,
                rotation=rotation,
                retention=retention,
                compression=compression,
                backtrace=backtrace,
                diagnose=diagnose,
                enqueue=enqueue,
            )

        # 添加文件处理器 - 错误日志
        error_file = os.path.join(log_dir, "error_{time:YYYY-MM-DD}.log")
        if batch_size > 0:
            logger.add(
                create_batching_sink(error_file, batch_size, flush_interval),
                level="ERROR",
                format=actual_format,
                rotation=rotation,
                retention=retention,
                compression=compression,
                backtrace=backtrace,
                diagnose=diagnose,
                enqueue=enqueue,
            )
        else:
            logger.add(
                error_file,
                level="ERROR",
                format=actual_format,
                rotation=rotation,
                retention=retention,
                compression=compression,
                backtrace=backtrace,
                diagnose=diagnose,
                enqueue=enqueue,
            )

    # 添加自定义处理器 - 优先使用传入的自定义处理器，否则使用默认处理器
    handlers_to_add = (
        custom_handlers if custom_handlers is not None else DEFAULT_HANDLERS
    )
    if handlers_to_add:
        for handler_config in handlers_to_add:
            # 复制配置以避免修改原始配置
            config = dict(handler_config)

            # 如果启用了结构化日志且配置中未指定format
            if structured and "format" in config and not callable(config["format"]):
                config["format"] = lambda record: format_structured_record(
                    record, json_format or DEFAULT_JSON_FORMAT
                )

            # 确保日志目录存在
            sink = config.get("sink")
            if isinstance(sink, str) and sink.startswith(log_dir):
                # 创建目录
                os.makedirs(os.path.dirname(sink), exist_ok=True)

            # 添加批处理支持（如果需要）
            if batch_size > 0 and isinstance(sink, str):  # 只对文件路径应用批处理
                config["sink"] = create_batching_sink(sink, batch_size, flush_interval)

            # 确保enqueue参数一致
            if "enqueue" not in config:
                config["enqueue"] = enqueue

            logger.add(**config)


def format_structured_record(
    record: Dict[str, Any], format_dict: Dict[str, str]
) -> str:
    """将日志记录格式化为结构化的JSON字符串

    Args:
        record: 日志记录
        format_dict: 格式化字典

    Returns:
        格式化后的JSON字符串
    """
    # 深度复制格式化字典
    output = {}

    # 填充字段
    for key, format_str in format_dict.items():
        try:
            # 处理嵌套结构
            if isinstance(format_str, dict):
                output[key] = {}
                for sub_key, sub_format in format_str.items():
                    output[key][sub_key] = record.get(sub_key, "")
            else:
                # 格式化字符串
                output[key] = format_str.format(**record)
        except (KeyError, ValueError):
            output[key] = f"Error formatting {key}"

    # 添加额外信息
    for key, value in record["extra"].items():
        if key not in ["level_emoji", "source"] and value is not None:
            output[key] = value

    return json.dumps(output, ensure_ascii=False)


def get_logger(source: str = "OpenGewe", **extra_context):
    """获取带有标识的日志记录器

    Args:
        source: 日志源标识，例如模块名或插件名
        **extra_context: 额外的上下文信息

    Returns:
        配置了源标识的日志记录器
    """
    context = {"source": source}
    context.update(extra_context)
    return logger.bind(**context)

# 解析日志配置文件
def load_logging_config(config_dict: Dict[str, Any]) -> None:
    """从配置文件加载日志配置

    Args:
        config_dict: 配置字典
    """
    if "logging" in config_dict:
        logging_config = config_dict["logging"]
        configure_from_dict(logging_config)
    else:
        # 使用默认配置
        setup_logger()
