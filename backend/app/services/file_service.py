"""文件服务模块

提供文件管理的业务逻辑，包括文件上传、下载、存储和微信媒体文件处理等功能。
"""

import os
import uuid
import shutil
import aiofiles
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, BinaryIO, Union
from fastapi import UploadFile

from opengewe.client import GeweClient
from opengewe.logger import get_logger

from backend.app.core.config import get_settings
from backend.app.gewe import get_gewe_client

# 获取日志记录器
logger = get_logger("FileService")


class FileService:
    """文件服务类

    提供文件管理的业务逻辑。
    """

    @staticmethod
    async def upload_file(
        file: UploadFile,
        folder: str = "uploads",
        prefix: Optional[str] = None,
        max_size: int = 50 * 1024 * 1024,  # 默认最大50MB
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """上传文件

        Args:
            file: 上传的文件对象
            folder: 存储的文件夹
            prefix: 文件名前缀
            max_size: 最大文件大小（字节）

        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: (是否成功, 消息, 文件信息)
        """
        # 检查文件大小
        if file.size and file.size > max_size:
            return False, f"文件大小超过限制 ({max_size / 1024 / 1024:.1f}MB)", None

        # 创建存储路径
        settings = get_settings()
        upload_dir = os.path.join(settings.files.storage_path, folder)
        os.makedirs(upload_dir, exist_ok=True)

        # 生成文件名
        original_filename = file.filename or "未命名文件"
        file_extension = os.path.splitext(original_filename)[1]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        prefix = f"{prefix}_" if prefix else ""
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{prefix}{timestamp}_{unique_id}{file_extension}"
        file_path = os.path.join(upload_dir, filename)

        # 保存文件
        try:
            # 读取文件内容
            contents = await file.read()

            # 写入文件
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(contents)

            # 生成访问URL
            url = f"{settings.backend.base_url}{settings.files.url_prefix}/{folder}/{filename}"

            # 返回文件信息
            file_info = {
                "original_filename": original_filename,
                "filename": filename,
                "path": file_path,
                "url": url,
                "size": len(contents),
                "mime_type": file.content_type,
                "uploaded_at": datetime.now().isoformat(),
            }

            logger.info(f"文件 '{original_filename}' 上传成功: {file_path}")
            return True, "文件上传成功", file_info
        except Exception as e:
            logger.error(f"上传文件 '{original_filename}' 时出错: {e}")
            # 清理可能部分写入的文件
            if os.path.exists(file_path):
                os.remove(file_path)
            return False, f"文件上传失败: {str(e)}", None

    @staticmethod
    async def download_wx_media(
        media_id: str,
        save_path: Optional[str] = None,
        client: Optional[GeweClient] = None,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """下载微信媒体文件

        Args:
            media_id: 微信媒体ID
            save_path: 保存路径，如果为None则使用默认路径
            client: 可选的GeweClient实例，如果不提供则使用默认实例

        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: (是否成功, 消息, 文件信息)
        """
        # 获取GeweClient实例
        if client is None:
            try:
                client = await get_gewe_client()
            except Exception as e:
                logger.error(f"获取GeweClient实例失败: {e}")
                return False, f"获取客户端实例失败: {str(e)}", None

        # 创建保存路径
        settings = get_settings()
        save_dir = save_path or os.path.join(settings.files.storage_path, "wx_media")
        os.makedirs(save_dir, exist_ok=True)

        # 下载文件
        try:
            # 调用GeweClient下载媒体文件
            result, success = await client.message.download_media(media_id)

            if not success:
                error_msg = result.get("msg", "未知错误")
                return False, f"下载微信媒体文件失败: {error_msg}", None

            # 提取文件信息
            file_url = result.get("url")
            content_type = result.get("contentType", "application/octet-stream")

            if not file_url:
                return False, "下载URL为空", None

            # 从URL获取文件名
            filename = os.path.basename(file_url.split("?")[0])
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                extension = FileService._get_extension_from_content_type(content_type)
                filename = f"media_{timestamp}_{media_id}{extension}"

            # 保存文件路径
            file_path = os.path.join(save_dir, filename)

            # 下载文件内容
            session = await client.session
            async with session.get(file_url) as response:
                if response.status != 200:
                    return False, f"下载文件失败: HTTP {response.status}", None

                content = await response.read()

                # 写入文件
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(content)

            # 生成访问URL
            url = f"{settings.backend.base_url}{settings.files.url_prefix}/wx_media/{filename}"

            # 返回文件信息
            file_info = {
                "filename": filename,
                "path": file_path,
                "url": url,
                "size": len(content),
                "mime_type": content_type,
                "media_id": media_id,
                "downloaded_at": datetime.now().isoformat(),
            }

            logger.info(f"微信媒体文件 '{media_id}' 下载成功: {file_path}")
            return True, "微信媒体文件下载成功", file_info

        except Exception as e:
            logger.error(f"下载微信媒体文件 '{media_id}' 时出错: {e}")
            return False, f"下载微信媒体文件失败: {str(e)}", None

    @staticmethod
    async def list_files(
        folder: str = "uploads",
        recursive: bool = False,
        filter_ext: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """列出文件夹中的文件

        Args:
            folder: 文件夹名称
            recursive: 是否递归列出子文件夹中的文件
            filter_ext: 过滤文件扩展名列表

        Returns:
            List[Dict[str, Any]]: 文件信息列表
        """
        settings = get_settings()
        folder_path = os.path.join(settings.files.storage_path, folder)

        if not os.path.exists(folder_path):
            logger.warning(f"文件夹 '{folder_path}' 不存在")
            return []

        result = []

        try:
            # 遍历文件夹
            for root, dirs, files in os.walk(folder_path):
                # 计算相对路径
                rel_path = os.path.relpath(root, settings.files.storage_path)

                # 处理文件
                for file in files:
                    # 如果有扩展名过滤，检查是否符合
                    if filter_ext:
                        ext = os.path.splitext(file)[1].lower()
                        if ext not in filter_ext:
                            continue

                    file_path = os.path.join(root, file)
                    stat = os.stat(file_path)

                    # 生成访问URL
                    url = f"{settings.backend.base_url}{settings.files.url_prefix}/{rel_path}/{file}"

                    file_info = {
                        "filename": file,
                        "path": file_path,
                        "relative_path": os.path.join(rel_path, file),
                        "url": url.replace("\\", "/"),  # 确保URL使用正斜杠
                        "size": stat.st_size,
                        "modified_at": datetime.fromtimestamp(
                            stat.st_mtime
                        ).isoformat(),
                    }

                    result.append(file_info)

                # 如果不递归，则不遍历子文件夹
                if not recursive:
                    break

            return result
        except Exception as e:
            logger.error(f"列出文件夹 '{folder}' 的文件时出错: {e}")
            return []

    @staticmethod
    async def delete_file(file_path: str) -> Tuple[bool, str]:
        """删除文件

        Args:
            file_path: 文件路径，可以是相对路径或绝对路径

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        settings = get_settings()

        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(file_path):
            file_path = os.path.join(settings.files.storage_path, file_path)

        # 检查文件是否存在
        if not os.path.exists(file_path):
            return False, f"文件 '{file_path}' 不存在"

        # 检查是否在允许的目录内
        storage_path = os.path.abspath(settings.files.storage_path)
        file_abs_path = os.path.abspath(file_path)

        if not file_abs_path.startswith(storage_path):
            return False, f"无法删除 '{file_path}'：不在允许的目录内"

        try:
            os.remove(file_path)
            logger.info(f"文件 '{file_path}' 已删除")
            return True, f"文件已删除"
        except Exception as e:
            logger.error(f"删除文件 '{file_path}' 时出错: {e}")
            return False, f"删除文件失败: {str(e)}"

    @staticmethod
    async def create_folder(folder_path: str) -> Tuple[bool, str]:
        """创建文件夹

        Args:
            folder_path: 文件夹路径，可以是相对路径或绝对路径

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        settings = get_settings()

        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(folder_path):
            folder_path = os.path.join(settings.files.storage_path, folder_path)

        # 检查是否在允许的目录内
        storage_path = os.path.abspath(settings.files.storage_path)
        folder_abs_path = os.path.abspath(folder_path)

        if not folder_abs_path.startswith(storage_path):
            return False, f"无法创建 '{folder_path}'：不在允许的目录内"

        try:
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"文件夹 '{folder_path}' 已创建")
            return True, f"文件夹已创建"
        except Exception as e:
            logger.error(f"创建文件夹 '{folder_path}' 时出错: {e}")
            return False, f"创建文件夹失败: {str(e)}"

    @staticmethod
    async def delete_folder(
        folder_path: str, recursive: bool = False
    ) -> Tuple[bool, str]:
        """删除文件夹

        Args:
            folder_path: 文件夹路径，可以是相对路径或绝对路径
            recursive: 是否递归删除文件夹及其内容

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        settings = get_settings()

        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(folder_path):
            folder_path = os.path.join(settings.files.storage_path, folder_path)

        # 检查文件夹是否存在
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return False, f"文件夹 '{folder_path}' 不存在"

        # 检查是否在允许的目录内
        storage_path = os.path.abspath(settings.files.storage_path)
        folder_abs_path = os.path.abspath(folder_path)

        if not folder_abs_path.startswith(storage_path):
            return False, f"无法删除 '{folder_path}'：不在允许的目录内"

        # 防止删除根存储目录
        if folder_abs_path == storage_path:
            return False, "不能删除根存储目录"

        try:
            if recursive:
                shutil.rmtree(folder_path)
            else:
                os.rmdir(folder_path)

            logger.info(f"文件夹 '{folder_path}' 已删除")
            return True, f"文件夹已删除"
        except OSError as e:
            if e.errno == 39:  # 目录不为空
                return False, f"文件夹不为空，请使用recursive=True递归删除"
            logger.error(f"删除文件夹 '{folder_path}' 时出错: {e}")
            return False, f"删除文件夹失败: {str(e)}"
        except Exception as e:
            logger.error(f"删除文件夹 '{folder_path}' 时出错: {e}")
            return False, f"删除文件夹失败: {str(e)}"

    @staticmethod
    async def generate_temp_url(
        file_path: str, expires_in: int = 3600, download_filename: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """生成临时文件访问URL

        Args:
            file_path: 文件路径，可以是相对路径或绝对路径
            expires_in: 有效期（秒）
            download_filename: 下载文件名，如果为None则使用原文件名

        Returns:
            Tuple[bool, str, Optional[str]]: (是否成功, 消息, 临时URL)
        """
        settings = get_settings()

        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(file_path):
            file_path = os.path.join(settings.files.storage_path, file_path)

        # 检查文件是否存在
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return False, f"文件 '{file_path}' 不存在", None

        # 检查是否在允许的目录内
        storage_path = os.path.abspath(settings.files.storage_path)
        file_abs_path = os.path.abspath(file_path)

        if not file_abs_path.startswith(storage_path):
            return False, f"无法访问 '{file_path}'：不在允许的目录内", None

        try:
            # 生成相对路径
            rel_path = os.path.relpath(file_abs_path, storage_path)

            # 设置过期时间
            expires_at = datetime.now() + timedelta(seconds=expires_in)
            expires_timestamp = int(expires_at.timestamp())

            # 生成令牌
            import hashlib
            import hmac

            # 获取或生成密钥
            secret_key = settings.files.secret_key
            if not secret_key:
                logger.warning("文件服务密钥未设置，使用默认密钥")
                secret_key = "default_secret_key"

            # 准备签名数据
            filename = os.path.basename(file_path)
            download_name = download_filename or filename
            signature_data = f"{rel_path}|{expires_timestamp}|{download_name}"

            # 生成签名
            signature = hmac.new(
                secret_key.encode(), signature_data.encode(), hashlib.sha256
            ).hexdigest()

            # 生成URL
            temp_url = (
                f"{settings.backend.base_url}{settings.files.url_prefix}/temp/"
                f"{signature}/{expires_timestamp}/{rel_path}"
            )

            # 添加下载文件名查询参数
            if download_filename:
                from urllib.parse import quote

                temp_url += f"?download={quote(download_filename)}"

            return True, "临时URL生成成功", temp_url
        except Exception as e:
            logger.error(f"为文件 '{file_path}' 生成临时URL时出错: {e}")
            return False, f"生成临时URL失败: {str(e)}", None

    @staticmethod
    def _get_extension_from_content_type(content_type: str) -> str:
        """根据内容类型获取文件扩展名

        Args:
            content_type: 内容类型

        Returns:
            str: 文件扩展名（包含点）
        """
        content_type = content_type.lower()

        # 常见MIME类型到扩展名的映射
        mime_to_ext = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/bmp": ".bmp",
            "image/webp": ".webp",
            "image/svg+xml": ".svg",
            "audio/mpeg": ".mp3",
            "audio/wav": ".wav",
            "audio/ogg": ".ogg",
            "audio/midi": ".midi",
            "audio/x-ms-wma": ".wma",
            "audio/webm": ".webm",
            "audio/amr": ".amr",
            "video/mp4": ".mp4",
            "video/mpeg": ".mpeg",
            "video/quicktime": ".mov",
            "video/x-ms-wmv": ".wmv",
            "video/webm": ".webm",
            "video/x-msvideo": ".avi",
            "application/pdf": ".pdf",
            "application/msword": ".doc",
            "application/vnd.ms-excel": ".xls",
            "application/vnd.ms-powerpoint": ".ppt",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
            "application/zip": ".zip",
            "application/x-rar-compressed": ".rar",
            "application/x-7z-compressed": ".7z",
            "application/x-tar": ".tar",
            "application/x-gzip": ".gz",
            "text/plain": ".txt",
            "text/html": ".html",
            "text/css": ".css",
            "text/javascript": ".js",
            "application/json": ".json",
            "application/xml": ".xml",
        }

        return mime_to_ext.get(content_type, ".bin")
