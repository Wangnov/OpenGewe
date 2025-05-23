from dataclasses import dataclass
from typing import Dict, Any, Optional, TYPE_CHECKING
import xml.etree.ElementTree as ET

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import FileBaseMessage

# 使用TYPE_CHECKING条件导入
if TYPE_CHECKING:
    from opengewe.client import GeweClient


@dataclass
class FileNoticeMessage(FileBaseMessage):
    """文件通知消息"""
    file_md5: str = ""       # 文件MD5值
    file_token: str = ""     # 文件上传令牌
    
    # 设置消息类型类变量
    message_type = MessageType.FILE_NOTICE
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理文件通知特有数据"""
        # 解析XML获取文件信息
        try:
            root = ET.fromstring(self.content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                # 获取文件名
                title = appmsg.find("title")
                if title is not None and title.text:
                    self.file_name = title.text

                # 获取文件属性
                appattach = appmsg.find("appattach")
                if appattach is not None:
                    # 文件大小
                    totallen = appattach.find("totallen")
                    if totallen is not None and totallen.text:
                        self.file_size = int(totallen.text)

                    # 文件扩展名
                    fileext = appattach.find("fileext")
                    if fileext is not None and fileext.text:
                        self.file_ext = fileext.text

                    # 文件上传令牌
                    fileuploadtoken = appattach.find("fileuploadtoken")
                    if fileuploadtoken is not None and fileuploadtoken.text:
                        self.file_token = fileuploadtoken.text

                # 获取MD5
                md5 = appmsg.find("md5")
                if md5 is not None and md5.text:
                    self.file_md5 = md5.text
        except Exception:
            pass


@dataclass
class FileMessage(FileBaseMessage):
    """文件消息"""
    file_md5: str = ""        # 文件MD5值
    file_url: str = ""        # 文件下载URL
    attach_id: str = ""       # 附件ID
    cdn_attach_url: str = ""  # CDN附件URL
    aes_key: str = ""         # AES密钥
    
    # 设置消息类型类变量
    message_type = MessageType.FILE
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理文件消息特有数据"""
        # 解析XML获取文件信息
        try:
            root = ET.fromstring(self.content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                # 获取文件名
                title = appmsg.find("title")
                if title is not None and title.text:
                    self.file_name = title.text

                # 获取文件属性
                appattach = appmsg.find("appattach")
                if appattach is not None:
                    # 文件大小
                    totallen = appattach.find("totallen")
                    if totallen is not None and totallen.text:
                        self.file_size = int(totallen.text)

                    # 文件扩展名
                    fileext = appattach.find("fileext")
                    if fileext is not None and fileext.text:
                        self.file_ext = fileext.text

                    # 附件ID
                    attachid = appattach.find("attachid")
                    if attachid is not None and attachid.text:
                        self.attach_id = attachid.text

                    # CDN附件URL
                    cdnattachurl = appattach.find("cdnattachurl")
                    if cdnattachurl is not None and cdnattachurl.text:
                        self.cdn_attach_url = cdnattachurl.text

                    # AES密钥
                    aeskey = appattach.find("aeskey")
                    if aeskey is not None and aeskey.text:
                        self.aes_key = aeskey.text

                # 获取MD5
                md5 = appmsg.find("md5")
                if md5 is not None and md5.text:
                    self.file_md5 = md5.text

                # 如果提供了GeweClient实例，使用API获取下载链接
                if client and self.content:
                    # 调用下载文件接口获取文件URL
                    try:
                        download_result = await client.message.download_file(
                            self.content
                        )
                        if (
                            download_result
                            and download_result.get("ret") == 200
                            and "data" in download_result
                        ):
                            file_url = download_result["data"].get("fileUrl", "")
                            if file_url and client.download_url:
                                self.file_url = f"{client.download_url}?url={file_url}"
                    except Exception:
                        # 下载失败不影响消息处理
                        pass
        except Exception:
            pass 