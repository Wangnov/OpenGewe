"""日志配置模块

提供基于loguru的日志配置和格式化功能。
"""

import os
import sys
import re
from typing import Dict, Optional, Any, Callable, List, Union
from pathlib import Path
from datetime import datetime

from loguru import logger

from opengewe.log.formatters import (
    format_console_message,
    format_file_message,
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

# 默认日志格式 - 使用居中对齐
DEFAULT_CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level.name: ^8}</level> {extra[level_emoji]} | "
    "<cyan>[{extra[source]}]</cyan> - "
    "{message}"
)

DEFAULT_FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "{level.name: ^8} {extra[level_emoji]} | "
    "[{extra[source]}] | "
    "{file}:{line} - "
    "{message}"
)

# 默认处理器配置
DEFAULT_HANDLERS = [
    # 添加API日志文件，记录所有API请求
    {
        "sink": "logs/api_{time:YYYY-MM-DD}.log",
        "level": "INFO",
        "rotation": "1 day",
        "retention": "30 days",
        "compression": "zip",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level.name: ^8} {extra[level_emoji]} | [{extra[source]}] | {message}"
    },
    # 添加DEBUG级别日志文件，记录详细信息
    {
        "sink": "logs/debug_{time:YYYY-MM-DD}.log",
        "level": "DEBUG",
        "rotation": "1 day",
        "retention": "30 days",
        "compression": "zip",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level.name: ^8} {extra[level_emoji]} | [{extra[source]}] | {file}:{line} - {message}"
    },
    # 添加特殊日志文件，专门记录调度任务相关信息
    {
        "sink": "logs/scheduler_{time:YYYY-MM-DD}.log",
        "level": "DEBUG",
        "rotation": "1 day",
        "retention": "30 days",
        "compression": "zip",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level.name: ^8} {extra[level_emoji]} | [{extra[source]}] | {message}",
        "filter": lambda record: "scheduler" in record["message"].lower() or 
                     "task" in record["message"].lower() or
                     "job" in record["message"].lower()
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
        "diagnose": True
    }
]


def setup_logger(
    console: bool = True,
    file: bool = True,
    level: str = "INFO",
    log_dir: str = DEFAULT_LOG_DIR,
    rotation: str = "1 day",
    retention: str = "30 days",
    compression: str = "zip",
    console_format: str = DEFAULT_CONSOLE_FORMAT,
    file_format: str = DEFAULT_FILE_FORMAT,
    backtrace: bool = True,
    diagnose: bool = True,
    enqueue: bool = True,
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
        custom_handlers: 自定义处理器配置列表，如果为None则使用默认处理器
    """
    # 重置当前记录器
    logger.remove()
    
    # 确保日志目录存在
    if file and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # 配置通用选项
    logger.configure(
        handlers=[],
        extra={"source": "OpenGewe", "level_emoji": ""},  # 默认源标识和空emoji
        patcher=lambda record: record.update(
            extra={
                **record["extra"],
                "level_emoji": LEVEL_EMOJIS.get(record["level"].name, "")
            },
            message=format_console_message(record)
            if should_escape_message(record["message"])
            else record["message"]
        ),
    )
    
    # 添加控制台处理器
    if console:
        logger.add(
            sys.stderr,
            level=level,
            format=console_format,
            colorize=True,
            backtrace=backtrace,
            diagnose=diagnose,
            enqueue=enqueue,
        )
    
    # 添加文件处理器 - 常规日志
    if file:
        logger.add(
            os.path.join(log_dir, "opengewe_{time:YYYY-MM-DD}.log"),
            level=level,
            format=file_format,
            rotation=rotation,
            retention=retention,
            compression=compression,
            backtrace=backtrace,
            diagnose=diagnose,
            enqueue=enqueue,
        )
        
        # 添加文件处理器 - 调试日志（更详细）
        logger.add(
            os.path.join(log_dir, "debug_{time:YYYY-MM-DD}.log"),
            level="DEBUG",
            format=file_format,
            rotation=rotation,
            retention=retention,
            compression=compression,
            backtrace=backtrace,
            diagnose=diagnose,
            enqueue=enqueue,
        )
        
        # 添加文件处理器 - 错误日志
        logger.add(
            os.path.join(log_dir, "error_{time:YYYY-MM-DD}.log"),
            level="ERROR",
            format=file_format,
            rotation=rotation,
            retention=retention,
            compression=compression,
            backtrace=backtrace,
            diagnose=diagnose,
            enqueue=enqueue,
        )
    
    # 添加自定义处理器 - 优先使用传入的自定义处理器，否则使用默认处理器
    handlers_to_add = custom_handlers if custom_handlers is not None else DEFAULT_HANDLERS
    if handlers_to_add:
        for handler_config in handlers_to_add:
            logger.add(**handler_config)


def get_logger(source: str = "OpenGewe"):
    """获取带有标识的日志记录器
    
    Args:
        source: 日志源标识，例如模块名或插件名
    
    Returns:
        配置了源标识的日志记录器
    """
    return logger.bind(source=source) 