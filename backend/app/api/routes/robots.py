"""机器人管理路由

提供机器人创建、登录、状态查询和消息发送等功能。
"""

from fastapi import APIRouter, Depends, Path, Query
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from opengewe.client import GeweClient
from opengewe.logger import get_logger

from backend.app.api.deps import (
    service_result_to_response,
    get_current_active_user,
    admin_required,
    standard_response,
)
from backend.app.gewe.dependencies import get_gewe_client
from backend.app.services.robot_service import RobotService
from backend.app.models.user import User

# 创建路由实例
router = APIRouter()

# 获取日志记录器
logger = get_logger("API.Robots")


# 消息发送模型
class MessageSend(BaseModel):
    """消息发送模型"""

    receiver: str
    content: str
    msg_type: str = "text"  # text, image, voice, video, file, link


# 创建机器人模型
class RobotCreate(BaseModel):
    """创建机器人模型"""

    name: str
    avatar: Optional[str] = None
    description: Optional[str] = None


@router.get("", response_model=Dict[str, Any])
async def get_robots(
    current_user: User = Depends(get_current_active_user),
):
    """获取机器人列表

    此路由用于解决前端直接请求/api/robots的404问题

    Returns:
        Dict: 包含机器人列表的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求获取机器人列表")
    # 返回空列表，前端开发阶段使用
    return standard_response(0, "获取机器人列表成功", {"robots": []})


@router.get("/status", response_model=Dict[str, Any])
async def get_robot_status(
    gewe_client: GeweClient = Depends(get_gewe_client),
    current_user: User = Depends(get_current_active_user),
):
    """获取机器人状态

    Returns:
        Dict: 包含机器人状态的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求获取机器人状态")
    result = await RobotService.get_robot_status(gewe_client)
    return service_result_to_response(result)


@router.post("/login", response_model=Dict[str, Any])
async def login_robot(
    gewe_client: GeweClient = Depends(get_gewe_client),
    current_user: User = Depends(admin_required),
):
    """登录机器人

    Args:
        gewe_client: GeWe客户端实例
        current_user: 当前管理员用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求登录机器人")
    result = await RobotService.login_robot(gewe_client)
    return service_result_to_response(result)


@router.post("/logout", response_model=Dict[str, Any])
async def logout_robot(
    gewe_client: GeweClient = Depends(get_gewe_client),
    current_user: User = Depends(admin_required),
):
    """登出机器人

    Args:
        gewe_client: GeWe客户端实例
        current_user: 当前管理员用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求登出机器人")
    result = await RobotService.logout_robot(gewe_client)
    return service_result_to_response(result)


@router.get("/qrcode", response_model=Dict[str, Any])
async def get_login_qrcode(
    gewe_client: GeweClient = Depends(get_gewe_client),
    current_user: User = Depends(admin_required),
):
    """获取登录二维码

    Args:
        gewe_client: GeWe客户端实例
        current_user: 当前管理员用户

    Returns:
        Dict: 包含二维码信息的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求获取登录二维码")
    result = await RobotService.get_login_qrcode(gewe_client)
    return service_result_to_response(result)


@router.post("/send", response_model=Dict[str, Any])
async def send_message(
    message: MessageSend,
    gewe_client: GeweClient = Depends(get_gewe_client),
    current_user: User = Depends(get_current_active_user),
):
    """发送消息

    Args:
        message: 消息内容
        gewe_client: GeWe客户端实例
        current_user: 当前用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(
        f"用户 {current_user.username} 请求发送 {message.msg_type} 类型消息到 {message.receiver}"
    )
    result = await RobotService.send_message(
        receiver=message.receiver,
        content=message.content,
        msg_type=message.msg_type,
        gewe_client=gewe_client,
    )
    return service_result_to_response(result)


@router.get("/contacts", response_model=Dict[str, Any])
async def get_contacts(
    page: int = Query(1, description="页码"),
    limit: int = Query(20, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    gewe_client: GeweClient = Depends(get_gewe_client),
    current_user: User = Depends(get_current_active_user),
):
    """获取联系人列表

    Args:
        page: 页码
        limit: 每页数量
        keyword: 搜索关键词
        gewe_client: GeWe客户端实例
        current_user: 当前用户

    Returns:
        Dict: 包含联系人列表的标准响应
    """
    logger.info(
        f"用户 {current_user.username} 请求获取联系人列表，页码 {page}，每页 {limit}，关键词 {keyword}"
    )
    result = await RobotService.get_contacts(
        page=page, limit=limit, keyword=keyword, gewe_client=gewe_client
    )
    return service_result_to_response(result)


@router.get("/groups", response_model=Dict[str, Any])
async def get_groups(
    page: int = Query(1, description="页码"),
    limit: int = Query(20, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    gewe_client: GeweClient = Depends(get_gewe_client),
    current_user: User = Depends(get_current_active_user),
):
    """获取群组列表

    Args:
        page: 页码
        limit: 每页数量
        keyword: 搜索关键词
        gewe_client: GeWe客户端实例
        current_user: 当前用户

    Returns:
        Dict: 包含群组列表的标准响应
    """
    logger.info(
        f"用户 {current_user.username} 请求获取群组列表，页码 {page}，每页 {limit}，关键词 {keyword}"
    )
    result = await RobotService.get_groups(
        page=page, limit=limit, keyword=keyword, gewe_client=gewe_client
    )
    return service_result_to_response(result)


@router.get("/messages", response_model=Dict[str, Any])
async def get_messages(
    chat_id: str = Query(..., description="聊天ID"),
    page: int = Query(1, description="页码"),
    limit: int = Query(20, description="每页数量"),
    gewe_client: GeweClient = Depends(get_gewe_client),
    current_user: User = Depends(get_current_active_user),
):
    """获取聊天消息记录

    Args:
        chat_id: 聊天ID
        page: 页码
        limit: 每页数量
        gewe_client: GeWe客户端实例
        current_user: 当前用户

    Returns:
        Dict: 包含消息记录的标准响应
    """
    logger.info(
        f"用户 {current_user.username} 请求获取聊天 {chat_id} 的消息记录，页码 {page}，每页 {limit}"
    )
    result = await RobotService.get_messages(
        chat_id=chat_id, page=page, limit=limit, gewe_client=gewe_client
    )
    return service_result_to_response(result)


@router.post("/create", response_model=Dict[str, Any])
async def create_robot(
    robot_data: RobotCreate,
    current_user: User = Depends(admin_required),
):
    """创建机器人

    Args:
        robot_data: 机器人创建数据
        current_user: 当前管理员用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求创建机器人 {robot_data.name}")
    result = await RobotService.create_robot(
        name=robot_data.name,
        avatar=robot_data.avatar,
        description=robot_data.description,
    )
    return service_result_to_response(result)


@router.get("/{robot_id}", response_model=Dict[str, Any])
async def get_robot(
    robot_id: str = Path(..., description="机器人ID"),
    current_user: User = Depends(get_current_active_user),
):
    """获取机器人详情

    Args:
        robot_id: 机器人ID
        current_user: 当前用户

    Returns:
        Dict: 包含机器人详情的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求获取机器人 {robot_id} 的详情")
    result = await RobotService.get_robot_by_id(robot_id)
    return service_result_to_response(result)


@router.delete("/{robot_id}", response_model=Dict[str, Any])
async def delete_robot(
    robot_id: str = Path(..., description="机器人ID"),
    current_user: User = Depends(admin_required),
):
    """删除机器人

    Args:
        robot_id: 机器人ID
        current_user: 当前管理员用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求删除机器人 {robot_id}")
    result = await RobotService.delete_robot(robot_id)
    return service_result_to_response(result)
