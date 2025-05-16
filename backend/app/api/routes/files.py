"""文件管理路由

提供文件上传、下载和微信媒体文件处理等功能。
"""

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Form,
    Path,
    Query,
    HTTPException,
)
from fastapi.responses import FileResponse, StreamingResponse
from typing import Dict, Any, Optional
import os
import io

from opengewe.client import GeweClient
from opengewe.logger import get_logger

from backend.app.api.deps import (
    service_result_to_response,
    get_current_active_user,
)
from backend.app.gewe.dependencies import get_gewe_client
from backend.app.services.file_service import FileService
from backend.app.models.user import User

# 创建路由实例
router = APIRouter()

# 获取日志记录器
logger = get_logger("API.Files")


@router.post("/upload", response_model=Dict[str, Any])
async def upload_file(
    file: UploadFile = File(...),
    file_type: str = Form("common"),
    current_user: User = Depends(get_current_active_user),
):
    """上传文件

    Args:
        file: 上传的文件
        file_type: 文件类型，可选值有common(普通文件)、image(图片)、
                  voice(语音)、video(视频)、file(文件附件)
        current_user: 当前用户

    Returns:
        Dict: 包含上传结果的标准响应
    """
    logger.info(
        f"用户 {current_user.username} 上传文件 {file.filename}，类型 {file_type}"
    )

    # 读取文件内容
    content = await file.read()

    # 调用服务保存文件
    result = await FileService.save_file(
        file_name=file.filename,
        file_content=content,
        file_type=file_type,
        user_id=current_user.id,
    )

    return service_result_to_response(result)


@router.get("/download/{file_id}", response_class=FileResponse)
async def download_file(
    file_id: str = Path(..., description="文件ID"),
    current_user: User = Depends(get_current_active_user),
):
    """下载文件

    Args:
        file_id: 文件ID
        current_user: 当前用户

    Returns:
        FileResponse: 文件响应
    """
    logger.info(f"用户 {current_user.username} 下载文件 {file_id}")

    # 获取文件信息
    result = await FileService.get_file(file_id)
    success, message, file_data = result

    if not success:
        raise HTTPException(status_code=404, detail=message)

    # 返回文件
    file_path = file_data.get("path")
    filename = file_data.get("name", "download")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=file_data.get("mime_type", "application/octet-stream"),
    )


@router.get("/list", response_model=Dict[str, Any])
async def list_files(
    file_type: Optional[str] = Query(None, description="文件类型"),
    page: int = Query(1, description="页码"),
    limit: int = Query(10, description="每页数量"),
    current_user: User = Depends(get_current_active_user),
):
    """获取文件列表

    Args:
        file_type: 文件类型过滤
        page: 页码
        limit: 每页数量
        current_user: 当前用户

    Returns:
        Dict: 包含文件列表的标准响应
    """
    logger.info(
        f"用户 {current_user.username} 请求文件列表，类型 {file_type}，页码 {page}，每页 {limit}"
    )

    result = await FileService.list_files(
        file_type=file_type, page=page, limit=limit, user_id=current_user.id
    )

    return service_result_to_response(result)


@router.delete("/{file_id}", response_model=Dict[str, Any])
async def delete_file(
    file_id: str = Path(..., description="文件ID"),
    current_user: User = Depends(get_current_active_user),
):
    """删除文件

    Args:
        file_id: 文件ID
        current_user: 当前用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"用户 {current_user.username} 删除文件 {file_id}")

    result = await FileService.delete_file(file_id, current_user.id)
    return service_result_to_response(result)


@router.post("/upload-to-wechat", response_model=Dict[str, Any])
async def upload_to_wechat(
    file: UploadFile = File(...),
    media_type: str = Form(
        ..., description="媒体类型，可选值有image、voice、video、file"
    ),
    current_user: User = Depends(get_current_active_user),
    gewe_client: GeweClient = Depends(get_gewe_client),
):
    """将文件上传到微信服务器

    Args:
        file: 上传的文件
        media_type: 媒体类型
        current_user: 当前用户
        gewe_client: GeWe客户端实例

    Returns:
        Dict: 包含上传结果的标准响应
    """
    logger.info(
        f"用户 {current_user.username} 上传文件 {file.filename} 到微信，类型 {media_type}"
    )

    # 读取文件内容
    content = await file.read()

    # 上传到微信
    result = await FileService.upload_to_wechat(
        file_name=file.filename,
        file_content=content,
        media_type=media_type,
        gewe_client=gewe_client,
    )

    return service_result_to_response(result)


@router.get("/wechat/{media_id}", response_class=StreamingResponse)
async def download_from_wechat(
    media_id: str = Path(..., description="微信媒体ID"),
    current_user: User = Depends(get_current_active_user),
    gewe_client: GeweClient = Depends(get_gewe_client),
):
    """从微信服务器下载媒体文件

    Args:
        media_id: 微信媒体ID
        current_user: 当前用户
        gewe_client: GeWe客户端实例

    Returns:
        StreamingResponse: 文件流响应
    """
    logger.info(f"用户 {current_user.username} 从微信下载媒体 {media_id}")

    # 从微信获取媒体
    result = await FileService.download_from_wechat(media_id, gewe_client)
    success, message, media_data = result

    if not success:
        raise HTTPException(status_code=404, detail=message)

    # 返回文件流
    file_content = media_data.get("content")
    filename = media_data.get("filename", "media")
    content_type = media_data.get("content_type", "application/octet-stream")

    if not file_content:
        raise HTTPException(status_code=404, detail="无法获取媒体内容")

    # 创建文件流
    file_stream = io.BytesIO(file_content)

    return StreamingResponse(
        file_stream,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
