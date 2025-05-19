"""GeweClient依赖项模块

提供FastAPI路由处理程序使用的依赖项函数，用于获取GeweClient实例。
"""

from typing import Optional

from fastapi import Depends

from opengewe.client import GeweClient
from opengewe.logger import get_logger

from backend.app.core.device import get_device_id_dependency
from backend.app.gewe.client_manager import client_manager

# 获取日志记录器
logger = get_logger("GeweClientDependencies")


async def get_gewe_client(
    device_id: str = Depends(get_device_id_dependency),
    load_plugins: bool = True,
) -> GeweClient:
    """获取当前设备的GeweClient实例

    这是一个FastAPI依赖项函数，用于在路由处理程序中获取GeweClient实例。
    它依赖于device_id依赖项函数，自动获取当前请求的设备ID。

    Args:
        device_id: 设备ID，由device_id依赖项函数提供
        load_plugins: 是否加载插件

    Returns:
        GeweClient: 客户端实例
    """
    # FastAPI应用启动时，依赖系统不会正常工作，会传入字符串形式的依赖表达式
    invalid_device_ids = [None, "", "Depends(get_device_id_dependency)"]

    if device_id in invalid_device_ids or not isinstance(device_id, str):
        # 应用启动时或依赖解析失败时，使用默认设备
        from backend.app.core.config import get_settings
        from backend.app.core.device import get_current_device_id

        # 首先检查上下文中是否已有设备ID
        context_device_id = get_current_device_id()
        if context_device_id:
            logger.debug(f"从上下文获取设备ID: {context_device_id}")
            device_id = context_device_id
        else:
            # 使用配置中的默认设备
            try:
                settings = get_settings()
                device_id = settings.devices.get_default_device_id()
                logger.info(
                    f"依赖解析失败或在应用启动时调用，使用默认设备: {device_id}"
                )
            except Exception as e:
                logger.error(f"获取默认设备失败: {e}")
                raise ValueError("无法获取有效的设备ID，且未配置默认设备") from e

    logger.debug(f"获取设备 {device_id} 的GeweClient实例")
    return await client_manager.get_client(device_id, load_plugins)


async def get_optional_gewe_client(
    device_id: Optional[str] = None,
    load_plugins: bool = True,
) -> Optional[GeweClient]:
    """获取可选的GeweClient实例

    与get_gewe_client不同，这个函数不抛出异常，如果无法获取客户端则返回None。
    适用于后台任务或不需要严格错误处理的场景。

    Args:
        device_id: 设备ID，如果为None则使用当前上下文的设备ID
        load_plugins: 是否加载插件

    Returns:
        Optional[GeweClient]: 客户端实例或None
    """
    try:
        return await client_manager.get_client(device_id, load_plugins)
    except Exception as e:
        logger.error(f"获取GeweClient实例时出错: {e}")
        return None
