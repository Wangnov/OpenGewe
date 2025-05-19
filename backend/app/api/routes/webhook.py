"""WebHook路由

处理微信回调消息，接收来自GeWe的事件通知。
"""

from fastapi import (
    APIRouter,
    Depends,
    Request,
    BackgroundTasks,
    Path,
    Header,
    HTTPException,
)
from fastapi.responses import PlainTextResponse
import json
from typing import Dict, Any, Optional

from opengewe.client import GeweClient
from opengewe.logger import get_logger

from backend.app.core.config import get_settings
from backend.app.gewe.dependencies import get_gewe_client
from backend.app.gewe.client_manager import client_manager
from backend.app.core.device import set_current_device_id

# 创建路由实例
router = APIRouter()

# 获取日志记录器
logger = get_logger("API.WebHook")


@router.post("", response_class=PlainTextResponse)
async def webhook_callback_root(
    request: Request,
    background_tasks: BackgroundTasks,
    content_type: Optional[str] = Header(None, alias="Content-Type"),
):
    """处理来自GeWe的通用WebHook回调请求

    不需要在URL中指定设备ID，而是从回调消息中的"Appid"字段提取。
    同时支持GeWeAPI的测试消息验证。

    Args:
        request: FastAPI请求对象
        background_tasks: 后台任务管理器
        content_type: 请求内容类型

    Returns:
        PlainTextResponse: 固定的"success"文本响应
    """
    try:
        # 获取请求体
        if content_type and "application/json" in content_type.lower():
            # JSON格式数据
            payload = await request.json()
        else:
            # 其他格式，尝试获取原始数据并解析
            raw_body = await request.body()
            try:
                payload = json.loads(raw_body)
            except json.JSONDecodeError:
                logger.error(f"无法解析WebHook请求体: {raw_body}")
                raise HTTPException(status_code=400, detail="无效的请求格式")

        # 检查是否为GeWeAPI的测试消息
        if "testMsg" in payload and "token" in payload:
            logger.info(f"收到GeWeAPI测试消息: {payload}")
            return "success"

        # 从payload中提取设备ID (Appid)
        device_id = None
        if "Appid" in payload:
            device_id = payload["Appid"]
            logger.info(f"从回调消息中提取Appid: {device_id}")

        # 如果没有Appid，尝试使用默认设备ID
        if not device_id:
            settings = get_settings()
            try:
                device_id = settings.devices.get_default_device_id()
                logger.debug(f"未在回调消息中找到Appid，使用默认设备ID: {device_id}")
            except ValueError:
                logger.error("未在回调消息中找到Appid，且系统未配置任何设备")
                # 仍然返回成功以避免GeWeAPI重试
                return "success"

        # 记录接收到的回调
        logger.debug(f"设备 {device_id} 收到WebHook回调: {payload}")

        # 在后台处理消息，避免阻塞响应
        background_tasks.add_task(
            process_webhook_callback_with_device,
            device_id=device_id,
            payload=payload,
        )

        # 立即返回成功，避免GeWe超时重试
        return "success"
    except Exception as e:
        logger.error(f"处理WebHook回调时出错: {e}")
        # 即使出错也返回成功，避免GeWe重复发送
        return "success"


@router.post("/{device_id}", response_class=PlainTextResponse)
async def webhook_callback(
    request: Request,
    background_tasks: BackgroundTasks,
    device_id: str = Path(..., description="设备ID"),
    gewe_client: GeweClient = Depends(get_gewe_client),
    content_type: Optional[str] = Header(None, alias="Content-Type"),
):
    """处理来自GeWe的WebHook回调请求

    Args:
        request: FastAPI请求对象
        background_tasks: 后台任务管理器
        device_id: 设备ID
        gewe_client: GeWe客户端实例
        content_type: 请求内容类型

    Returns:
        PlainTextResponse: 固定的"success"文本响应
    """
    try:
        # 获取请求体
        if content_type and "application/json" in content_type.lower():
            # JSON格式数据
            payload = await request.json()
        else:
            # 其他格式，尝试获取原始数据并解析
            raw_body = await request.body()
            try:
                payload = json.loads(raw_body)
            except json.JSONDecodeError:
                logger.error(f"无法解析WebHook请求体: {raw_body}")
                raise HTTPException(status_code=400, detail="无效的请求格式")

        # 记录接收到的回调
        logger.debug(f"设备 {device_id} 收到WebHook回调: {payload}")

        # 在后台处理消息，避免阻塞响应
        background_tasks.add_task(
            process_webhook_callback,
            gewe_client=gewe_client,
            device_id=device_id,
            payload=payload,
        )

        # 立即返回成功，避免GeWe超时重试
        return "success"
    except Exception as e:
        logger.error(f"处理WebHook回调时出错: {e}")
        # 即使出错也返回成功，避免GeWe重复发送
        return "success"


@router.get("", response_class=PlainTextResponse)
async def webhook_verification_root(
    request: Request,
    echostr: Optional[str] = None,
):
    """处理WebHook根路径验证请求

    微信服务器在配置WebHook时会发送验证请求，
    需要原样返回echostr参数值。

    Args:
        request: FastAPI请求对象
        echostr: 验证字符串

    Returns:
        PlainTextResponse: 原样返回的echostr
    """
    logger.info(f"收到WebHook根路径验证请求，echostr: {echostr}")
    return echostr or ""


@router.get("/{device_id}", response_class=PlainTextResponse)
async def webhook_verification(
    request: Request,
    device_id: str = Path(..., description="设备ID"),
    echostr: Optional[str] = None,
):
    """处理WebHook验证请求

    微信服务器在配置WebHook时会发送验证请求，
    需要原样返回echostr参数值。

    Args:
        request: FastAPI请求对象
        device_id: 设备ID
        echostr: 验证字符串

    Returns:
        PlainTextResponse: 原样返回的echostr
    """
    logger.info(f"设备 {device_id} 收到WebHook验证请求，echostr: {echostr}")
    return echostr or ""


async def process_webhook_callback_with_device(device_id: str, payload: Dict[str, Any]):
    """在后台处理WebHook回调消息

    根据device_id获取相应的GeweClient实例

    Args:
        device_id: 设备ID
        payload: 回调消息数据
    """
    try:
        # 设置当前设备ID上下文
        set_current_device_id(device_id)

        # 获取设置
        settings = get_settings()

        # 验证设备ID是否存在于配置中
        if device_id not in settings.devices.keys():
            logger.warning(f"设备ID '{device_id}' 在配置中不存在，尝试使用默认设备ID")
            try:
                # 尝试使用默认设备
                device_id = settings.devices.get_default_device_id()
                set_current_device_id(device_id)
            except ValueError:
                logger.error("无法获取默认设备ID")
                return

        # 获取对应设备的客户端
        gewe_client = await client_manager.get_client(device_id)

        await process_webhook_callback(gewe_client, device_id, payload)
    except Exception as e:
        logger.error(f"处理设备 {device_id} 的WebHook回调时出错: {e}")


async def process_webhook_callback(
    gewe_client: GeweClient, device_id: str, payload: Dict[str, Any]
):
    """在后台处理WebHook回调消息

    Args:
        gewe_client: GeWe客户端实例
        device_id: 设备ID
        payload: 回调消息数据
    """
    try:
        logger.info(f"处理设备 {device_id} 的WebHook回调: {payload}")

        # 处理GeWeAPI特有的消息格式
        if "TypeName" in payload:
            # GeWeAPI的消息格式，包含TypeName字段
            type_name = payload.get("TypeName")

            # 记录回调类型
            logger.info(f"收到GeWeAPI回调: TypeName={type_name}")

            # 直接将消息转发到消息工厂进行处理
            if hasattr(gewe_client, "message_factory"):
                await gewe_client.message_factory.process_payload(payload)
            else:
                logger.warning("GeweClient没有message_factory属性，无法处理回调消息")
            return

        # 兼容旧的消息格式
        msg_type = payload.get("type")
        if msg_type:
            logger.info(f"收到旧格式回调: type={msg_type}")

            # 直接将消息转发到消息工厂进行处理
            if hasattr(gewe_client, "message_factory"):
                await gewe_client.message_factory.process_payload(payload)
            else:
                logger.warning("GeweClient没有message_factory属性，无法处理回调消息")
        else:
            logger.warning(f"未知的回调消息类型: {payload}")
    except Exception as e:
        logger.error(f"后台处理WebHook回调时出错: {e}")
