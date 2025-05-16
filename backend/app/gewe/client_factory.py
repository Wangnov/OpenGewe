"""GeweClient工厂模块

提供创建和配置GeweClient实例的工厂函数。
"""

from typing import Optional, Dict, Any, Tuple

from opengewe.client import GeweClient
from opengewe.logger import get_logger

from backend.app.core.config import get_settings, DeviceSettings

# 获取日志记录器
logger = get_logger("GeweClientFactory")


async def create_client(
    device_id: Optional[str] = None,
    device_config: Optional[DeviceSettings] = None,
    queue_options: Optional[Dict[str, Any]] = None,
    debug: bool = False,
) -> GeweClient:
    """创建GeweClient实例

    根据配置创建并配置GeweClient实例。可以通过device_id从配置中加载设备配置，
    或者直接传入device_config对象。

    Args:
        device_id: 设备ID，用于从配置中加载设备配置
        device_config: 设备配置对象，如果提供则优先使用
        queue_options: 消息队列选项，如果为None则使用配置文件的设置
        debug: 是否开启调试模式

    Returns:
        GeweClient: 配置好的GeweClient实例

    Raises:
        ValueError: 如果既没有提供device_id也没有提供device_config，或者指定的device_id不存在
    """
    settings = get_settings()

    # 如果没有提供设备配置，则尝试通过设备ID加载
    if device_config is None:
        if device_id is None:
            try:
                device_id = settings.devices.get_default_device_id()
                logger.debug(f"使用默认设备ID: {device_id}")
            except ValueError:
                raise ValueError("系统未配置任何设备，且未提供设备配置")

        try:
            device_config = settings.devices[device_id]
            logger.debug(f"已加载设备配置: {device_id}")
        except KeyError:
            raise ValueError(f"设备ID '{device_id}' 不存在")

    # 如果没有提供队列选项，则使用配置文件中的设置
    if queue_options is None:
        queue_config = settings.queue
        queue_options = {
            "broker": queue_config.broker,
            "backend": queue_config.backend,
            "queue_name": queue_config.name,
        }

    # 创建GeweClient实例
    client = GeweClient(
        base_url=device_config.base_url,
        download_url=device_config.download_url,
        callback_url=device_config.callback_url,
        app_id=device_config.app_id,
        token=device_config.token,
        debug=debug,
        is_gewe=device_config.is_gewe,
        queue_type=settings.queue.queue_type,
        **queue_options,
    )

    logger.info(f"已创建GeweClient实例: {device_config.name} ({device_config.app_id})")
    return client


async def verify_client_config(
    device_id: Optional[str] = None, device_config: Optional[DeviceSettings] = None
) -> Tuple[bool, str]:
    """验证GeweClient配置的有效性

    检查设备配置是否完整，尝试获取设备列表以验证token是否有效。

    Args:
        device_id: 设备ID，用于从配置中加载设备配置
        device_config: 设备配置对象，如果提供则优先使用

    Returns:
        Tuple[bool, str]: (是否有效, 错误信息)
    """
    settings = get_settings()

    # 如果没有提供设备配置，则尝试通过设备ID加载
    if device_config is None:
        if device_id is None:
            try:
                device_id = settings.devices.get_default_device_id()
            except ValueError:
                return False, "系统未配置任何设备，且未提供设备配置"

        try:
            device_config = settings.devices[device_id]
        except KeyError:
            return False, f"设备ID '{device_id}' 不存在"

    # 检查必要配置是否完整
    if not device_config.base_url:
        return False, "设备配置缺少base_url"
    if not device_config.callback_url:
        return False, "设备配置缺少callback_url"
    if not device_config.token:
        return False, "设备配置缺少token"

    # 创建一个临时客户端用于验证配置
    try:
        client = await create_client(device_config=device_config)
        # 尝试获取设备列表，验证token是否有效
        result, success = await client.login.get_device_list()
        await client.close()

        if success:
            return True, "配置有效"
        else:
            error_msg = result.get("msg", "未知错误")
            return False, f"Token验证失败: {error_msg}"
    except Exception as e:
        return False, f"验证配置时出错: {str(e)}"
