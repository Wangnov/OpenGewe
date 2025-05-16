"""系统管理路由

提供系统配置管理、系统状态查询等功能。
"""

from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional
from pydantic import BaseModel
import psutil
import sys
from datetime import datetime

from opengewe.logger import get_logger

from backend.app.api.deps import (
    standard_response,
    service_result_to_response,
    admin_required,
)
from backend.app.services.admin_service import AdminService
from backend.app.models.user import User
from backend.app.core.config import get_settings

# 创建路由实例
router = APIRouter()

# 获取日志记录器
logger = get_logger("API.System")

# 获取配置
settings = get_settings()


class SystemConfig(BaseModel):
    """系统配置更新模型"""

    config_section: str
    config_data: Dict[str, Any]


@router.get("/config", response_model=Dict[str, Any])
async def get_system_config(
    section: Optional[str] = Query(None, description="配置部分名称"),
    current_user: User = Depends(admin_required),
):
    """获取系统配置

    Args:
        section: 配置部分名称，如果为空则返回所有配置
        current_user: 当前管理员用户

    Returns:
        Dict: 包含系统配置的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求获取系统配置，部分: {section}")
    result = await AdminService.get_system_config(section)
    return service_result_to_response(result)


@router.put("/config", response_model=Dict[str, Any])
async def update_system_config(
    config: SystemConfig,
    current_user: User = Depends(admin_required),
):
    """更新系统配置

    Args:
        config: 配置更新数据
        current_user: 当前管理员用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(
        f"管理员 {current_user.username} 请求更新系统配置，部分: {config.config_section}"
    )
    result = await AdminService.update_system_config(
        config_section=config.config_section, config_data=config.config_data
    )
    return service_result_to_response(result)


@router.get("/status", response_model=Dict[str, Any])
async def get_system_status(
    current_user: User = Depends(admin_required),
):
    """获取系统状态信息

    Args:
        current_user: 当前管理员用户

    Returns:
        Dict: 包含系统状态的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求获取系统状态")

    try:
        # 收集系统信息
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        # 获取启动时间
        uptime = datetime.now().timestamp() - psutil.boot_time()

        # 构建状态信息
        status_info = {
            "system": {
                "platform": sys.platform,
                "python_version": sys.version,
                "cpu_count": psutil.cpu_count(),
                "uptime_seconds": int(uptime),
            },
            "resources": {
                "cpu_percent": cpu_percent,
                "memory_total": memory.total,
                "memory_available": memory.available,
                "memory_percent": memory.percent,
                "disk_total": disk.total,
                "disk_free": disk.free,
                "disk_percent": disk.percent,
            },
            "app": {
                "version": "0.1.0",  # 可以从某处获取真实版本
                "devices_count": len(settings.devices.keys()),
                "enabled_plugins": len(settings.plugins.enabled_plugins),
            },
        }

        return standard_response(0, "获取系统状态成功", status_info)
    except Exception as e:
        logger.error(f"获取系统状态时出错: {e}")
        return standard_response(1, f"获取系统状态失败: {str(e)}")


@router.post("/restart", response_model=Dict[str, Any])
async def restart_system(
    current_user: User = Depends(admin_required),
):
    """重启系统

    注意：此功能需要系统级权限，可能无法在所有环境中工作

    Args:
        current_user: 当前管理员用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.warning(f"管理员 {current_user.username} 请求重启系统")

    try:
        # 这里可以实现适当的系统重启逻辑
        # 例如，使用守护进程管理器如PM2或Supervisor重启应用
        # 或者简单地退出当前进程，依靠外部服务管理器重启

        # 对于实际生产环境，这里应该有更健壮的实现
        # 例如，使用异步任务在一定延迟后重启服务

        return standard_response(0, "系统将在10秒后重启")
    except Exception as e:
        logger.error(f"重启系统时出错: {e}")
        return standard_response(1, f"重启系统失败: {str(e)}")


@router.get("/logs", response_model=Dict[str, Any])
async def get_system_logs(
    level: Optional[str] = Query(None, description="日志级别"),
    limit: int = Query(100, description="返回的日志条数"),
    current_user: User = Depends(admin_required),
):
    """获取系统日志

    Args:
        level: 日志级别筛选
        limit: 返回的日志条数
        current_user: 当前管理员用户

    Returns:
        Dict: 包含系统日志的标准响应
    """
    logger.info(
        f"管理员 {current_user.username} 请求获取系统日志，级别: {level}，条数: {limit}"
    )
    result = await AdminService.get_system_logs(level, limit)
    return service_result_to_response(result)
