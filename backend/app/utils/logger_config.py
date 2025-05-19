"""日志配置模块

配置应用程序的日志系统，集成OpenGewe的日志功能和后端特定需求。
"""

import os
from typing import Dict, Any, Optional

from opengewe.logger import (
    setup_logger as opengewe_setup_logger,
    get_logger as opengewe_get_logger,
    init_default_logger,
    intercept_logging,
    RequestContext,
)

from backend.app.core.config import get_settings


def setup_logger() -> None:
    """设置应用程序日志系统

    基于应用配置初始化日志系统，集成OpenGewe的日志功能。
    """
    try:
        # 首先应用loguru拦截，确保后续的日志记录都能正确识别来源
        from opengewe.logger.utils import intercept_plugin_loguru

        # 拦截loguru导入
        intercept_plugin_loguru()

        # 获取配置
        settings = get_settings()
        log_config = settings.logging

        # 确保日志目录存在
        log_dir = log_config.path
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # 检查是否使用结构化日志
        is_structured = log_config.format.lower() == "json"

        # 初始化日志系统
        opengewe_setup_logger(
            console=log_config.stdout,
            file=True,
            level=log_config.level,
            log_dir=log_dir,
            rotation=log_config.rotation,
            retention=log_config.retention,
            compression=log_config.compression,
            structured=is_structured,
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

        # 拦截标准库日志，重定向到loguru
        intercept_logging()

        # 再次应用loguru拦截，确保它被正确应用
        custom_logger = intercept_plugin_loguru()

        logger = get_logger("Logger")
        logger.info(
            f"日志系统初始化完成 [级别: {log_config.level}, 格式: {log_config.format}, 目录: {log_dir}]"
        )

        # 验证拦截是否有效
        import sys

        if "loguru" in sys.modules:
            from loguru import logger as loguru_logger

            if not hasattr(loguru_logger, "_original_logger"):
                print("警告: loguru拦截可能未完全生效")

    except Exception as e:
        # 使用备用配置初始化
        print(f"使用默认配置初始化日志系统: {str(e)}")
        _setup_default_logger()


def _setup_default_logger() -> None:
    """使用默认配置设置日志系统

    当无法加载应用配置时使用此函数。
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # 使用OpenGewe的默认日志配置
    init_default_logger(
        level="INFO",
        enqueue=True,
        batch_size=0,
        flush_interval=0.0,
        structured=False,
    )

    get_logger("Logger").info("已使用默认配置初始化日志系统")


def get_logger(name: str, **extra_context: Any):
    """获取日志记录器

    Args:
        name: 日志记录器名称
        extra_context: 额外的上下文信息

    Returns:
        Logger: 日志记录器
    """
    return opengewe_get_logger(name, **extra_context)


def get_request_context(request_id: Optional[str] = None) -> RequestContext:
    """获取请求上下文

    Args:
        request_id: 请求ID

    Returns:
        RequestContext: 请求上下文管理器
    """
    return RequestContext(request_id=request_id)


def configure_logger_from_settings(settings: Dict[str, Any]) -> None:
    """从配置字典配置日志系统

    用于动态更新日志配置。

    Args:
        settings: 日志配置字典
    """
    level = settings.get("level", "INFO")
    format_type = settings.get("format", "color")
    stdout = settings.get("stdout", True)
    log_dir = settings.get("path", "./logs")
    rotation = settings.get("rotation", "500 MB")
    retention = settings.get("retention", "10 days")
    compression = settings.get("compression", "zip")

    is_structured = format_type.lower() == "json"

    # 确保日志目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # 重新配置日志系统
    opengewe_setup_logger(
        console=stdout,
        file=True,
        level=level,
        log_dir=log_dir,
        rotation=rotation,
        retention=retention,
        compression=compression,
        structured=is_structured,
        enqueue=True,
    )

    get_logger("Logger").info(
        f"日志系统已重新配置 [级别: {level}, 格式: {format_type}, 目录: {log_dir}]"
    )
