"""OpenGewe 日志模块

提供基于 loguru 的统一日志配置和使用接口。
"""

from opengewe.logger.config import setup_logger, get_logger, format_structured_record
from opengewe.logger.utils import (
    disable_logger,
    enable_logger,
    intercept_logging,
    intercept_plugin_loguru,
    reset_logger,
    RequestContext,
    BatchingSink,
    traced_function,
    log_group,
)


def init_default_logger(
    level: str = "INFO",
    enqueue: bool = True,
    workers: int = 1,
    batch_size: int = 0,
    flush_interval: float = 0.0,
    structured: bool = False,
):
    """初始化默认日志系统

    这个函数封装了日志系统的完整初始化过程，包含:
    1. 设置基本日志配置，使用默认处理器
    2. 拦截标准库logging调用
    3. 拦截插件的loguru调用

    Args:
        level: 日志级别，默认为INFO
        enqueue: 是否启用异步日志，默认为True
        workers: 异步处理的工作线程数，已弃用，保留参数以兼容旧代码
        batch_size: 批处理大小，设为0禁用批处理，默认为0
        flush_interval: 批处理刷新间隔(秒)，设为0禁用自动刷新，默认为0
        structured: 是否启用结构化日志(JSON格式)，默认为False
    """
    # 设置默认日志配置
    setup_logger(
        level=level,
        enqueue=enqueue,
        workers=workers,
        batch_size=batch_size,
        flush_interval=flush_interval,
        structured=structured,
    )

    # 拦截标准库日志，重定向到loguru
    intercept_logging()

    # 拦截插件的loguru使用，添加Plugin源标识
    intercept_plugin_loguru()


__all__ = [
    "setup_logger",
    "get_logger",
    "disable_logger",
    "enable_logger",
    "intercept_logging",
    "intercept_plugin_loguru",
    "reset_logger",
    "init_default_logger",
    "RequestContext",
    "BatchingSink",
    "traced_function",
    "log_group",
    "format_structured_record",
]
