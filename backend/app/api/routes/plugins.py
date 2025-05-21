"""插件管理路由

提供插件的列表查询、启用/禁用、配置管理等功能。
"""

from fastapi import APIRouter, Depends, Path, Query
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from opengewe.client import GeweClient
from opengewe.logger import get_logger

from backend.app.api.deps import (
    standard_response,
    service_result_to_response,
    admin_required,
    get_current_active_user,
)
from backend.app.gewe.dependencies import get_gewe_client
from backend.app.services.plugin_service import PluginService
from backend.app.models.user import User

# 创建路由实例
router = APIRouter()

# 获取日志记录器
logger = get_logger("API.Plugins")


# 插件配置模型
class PluginConfigUpdate(BaseModel):
    """插件配置更新模型"""

    config: Dict[str, Any]


@router.get("", response_model=Dict[str, Any])
async def get_plugins(
    current_user: User = Depends(get_current_active_user),
):
    """获取插件列表

    此路由用于解决前端直接请求/api/plugins的401问题

    Returns:
        Dict: 包含插件列表的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求获取插件列表")
    # 返回空列表，前端开发阶段使用
    return standard_response(0, "获取插件列表成功", {"plugins": []})


@router.get("/", response_model=Dict[str, Any])
async def get_all_plugins(
    current_user: User = Depends(admin_required),
):
    """获取所有插件

    Args:
        current_user: 当前管理员用户

    Returns:
        Dict: 包含插件列表的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求获取所有插件")
    result = await PluginService.get_all_plugins()
    return service_result_to_response(result)


@router.get("/{plugin_id}", response_model=Dict[str, Any])
async def get_plugin(
    plugin_id: str = Path(..., description="插件ID"),
    current_user: User = Depends(admin_required),
):
    """获取指定插件的详细信息

    Args:
        plugin_id: 插件ID

    Returns:
        Dict: 包含插件详情的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求获取插件 {plugin_id} 的详情")
    result = await PluginService.get_plugin_by_id(plugin_id)
    return service_result_to_response(result)


@router.post("/{plugin_id}/enable", response_model=Dict[str, Any])
async def enable_plugin(
    plugin_id: str = Path(..., description="插件ID"),
    current_user: User = Depends(admin_required),
    gewe_client: GeweClient = Depends(get_gewe_client),
):
    """启用指定插件

    Args:
        plugin_id: 插件ID

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求启用插件 {plugin_id}")
    result = await PluginService.enable_plugin(plugin_id)

    # 如果启用成功，重新加载插件
    if result[0]:
        try:
            await gewe_client.reload_plugins()
            logger.info("已为客户端重新加载插件")
        except Exception as e:
            logger.error(f"重新加载插件时出错: {e}")

    return service_result_to_response(result)


@router.post("/{plugin_id}/disable", response_model=Dict[str, Any])
async def disable_plugin(
    plugin_id: str = Path(..., description="插件ID"),
    current_user: User = Depends(admin_required),
    gewe_client: GeweClient = Depends(get_gewe_client),
):
    """禁用指定插件

    Args:
        plugin_id: 插件ID

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求禁用插件 {plugin_id}")
    result = await PluginService.disable_plugin(plugin_id)

    # 如果禁用成功，重新加载插件
    if result[0]:
        try:
            await gewe_client.reload_plugins()
            logger.info("已为客户端重新加载插件")
        except Exception as e:
            logger.error(f"重新加载插件时出错: {e}")

    return service_result_to_response(result)


@router.get("/{plugin_id}/config", response_model=Dict[str, Any])
async def get_plugin_config(
    plugin_id: str = Path(..., description="插件ID"),
    current_user: User = Depends(admin_required),
):
    """获取指定插件的配置

    Args:
        plugin_id: 插件ID

    Returns:
        Dict: 包含插件配置的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求获取插件 {plugin_id} 的配置")
    result = await PluginService.get_plugin_config(plugin_id)
    return service_result_to_response(result)


@router.put("/{plugin_id}/config", response_model=Dict[str, Any])
async def update_plugin_config(
    plugin_config: PluginConfigUpdate,
    plugin_id: str = Path(..., description="插件ID"),
    current_user: User = Depends(admin_required),
    gewe_client: GeweClient = Depends(get_gewe_client),
):
    """更新指定插件的配置

    Args:
        plugin_id: 插件ID
        plugin_config: 更新的配置数据

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求更新插件 {plugin_id} 的配置")
    result = await PluginService.update_plugin_config(plugin_id, plugin_config.config)

    # 如果更新成功，重新加载插件
    if result[0]:
        try:
            await gewe_client.reload_plugins()
            logger.info("已为客户端重新加载插件")
        except Exception as e:
            logger.error(f"重新加载插件时出错: {e}")

    return service_result_to_response(result)


@router.post("/scan", response_model=Dict[str, Any])
async def scan_plugins(
    current_user: User = Depends(admin_required),
):
    """扫描插件目录，发现新插件

    Returns:
        Dict: 包含扫描结果的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求扫描插件")
    result = await PluginService.scan_plugins()
    return service_result_to_response(result)


@router.post("/reload", response_model=Dict[str, Any])
async def reload_plugins(
    current_user: User = Depends(admin_required),
    gewe_client: GeweClient = Depends(get_gewe_client),
):
    """重新加载所有插件

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求重新加载插件")
    try:
        await gewe_client.reload_plugins()
        return standard_response(0, "插件重新加载成功")
    except Exception as e:
        logger.error(f"重新加载插件时出错: {e}")
        return standard_response(1, f"重新加载插件失败: {str(e)}")
