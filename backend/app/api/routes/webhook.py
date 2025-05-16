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

from backend.app.gewe.dependencies import get_gewe_client

# 创建路由实例
router = APIRouter()

# 获取日志记录器
logger = get_logger("API.WebHook")


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
        # 根据消息类型处理不同的回调
        msg_type = payload.get("type")

        if msg_type == "message":
            # 处理消息类型回调
            await gewe_client.process_message(payload)
        elif msg_type == "event":
            # 处理事件类型回调
            await gewe_client.process_event(payload)
        else:
            logger.warning(f"未知的回调消息类型: {msg_type}")
    except Exception as e:
        logger.error(f"后台处理WebHook回调时出错: {e}")
