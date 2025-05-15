"""OpenGewe 日志模块

提供基于 loguru 的统一日志配置和使用接口。
"""

from opengewe.log.config import setup_logger, get_logger
from opengewe.log.utils import (
    disable_logger,
    enable_logger,
    intercept_logging,
    intercept_plugin_loguru,
    reset_logger,
)


def init_default_logger(level: str = "INFO"):
    """初始化默认日志系统
    
    这个函数封装了日志系统的完整初始化过程，包含:
    1. 设置基本日志配置，使用默认处理器
    2. 拦截标准库logging调用
    3. 拦截插件的loguru调用
    
    Args:
        level: 日志级别，默认为INFO
    """
    # 设置默认日志配置
    setup_logger(level=level)
    
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
] 