from dataclasses import dataclass
from typing import Dict, Any, Optional, TYPE_CHECKING
import xml.etree.ElementTree as ET

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import BaseMessage

# 使用TYPE_CHECKING条件导入
if TYPE_CHECKING:
    from opengewe.client import GeweClient


@dataclass
class FileNoticeMessage(BaseMessage):
    """文件通知消息"""

    file_name: str = ""      # 文件名
    file_ext: str = ""       # 文件扩展名
    file_size: int = 0       # 文件大小
    file_md5: str = ""       # 文件MD5值
    file_token: str = ""     # 文件上传令牌

    @classmethod
    async def from_dict(
        cls, data: Dict[str, Any], client: Optional["GeweClient"] = None
    ) -> "FileNoticeMessage":
        """从字典创建文件通知消息对象

        Args:
            data: 原始数据
            client: GeweClient实例，用于下载文件
        """
        msg = cls(
            type=MessageType.FILE_NOTICE,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_wxid = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取文件信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        # 获取文件名
                        title = appmsg.find("title")
                        if title is not None and title.text:
                            msg.file_name = title.text

                        # 获取文件属性
                        appattach = appmsg.find("appattach")
                        if appattach is not None:
                            # 文件大小
                            totallen = appattach.find("totallen")
                            if totallen is not None and totallen.text:
                                msg.file_size = int(totallen.text)

                            # 文件扩展名
                            fileext = appattach.find("fileext")
                            if fileext is not None and fileext.text:
                                msg.file_ext = fileext.text

                            # 文件上传令牌
                            fileuploadtoken = appattach.find("fileuploadtoken")
                            if fileuploadtoken is not None and fileuploadtoken.text:
                                msg.file_token = fileuploadtoken.text

                        # 获取MD5
                        md5 = appmsg.find("md5")
                        if md5 is not None and md5.text:
                            msg.file_md5 = md5.text
                except Exception:
                    pass

        return msg


@dataclass
class FileMessage(BaseMessage):
    """文件消息"""

    file_name: str = ""       # 文件名
    file_ext: str = ""        # 文件扩展名
    file_size: int = 0        # 文件大小
    file_md5: str = ""        # 文件MD5值
    file_url: str = ""        # 文件下载URL
    attach_id: str = ""       # 附件ID
    cdn_attach_url: str = ""  # CDN附件URL
    aes_key: str = ""         # AES密钥

    @classmethod
    async def from_dict(
        cls, data: Dict[str, Any], client: Optional["GeweClient"] = None
    ) -> "FileMessage":
        """从字典创建文件消息对象

        Args:
            data: 原始数据
            client: GeweClient实例，用于下载文件
        """
        msg = cls(
            type=MessageType.FILE,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_wxid = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取文件信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        # 获取文件名
                        title = appmsg.find("title")
                        if title is not None and title.text:
                            msg.file_name = title.text

                        # 获取文件属性
                        appattach = appmsg.find("appattach")
                        if appattach is not None:
                            # 文件大小
                            totallen = appattach.find("totallen")
                            if totallen is not None and totallen.text:
                                msg.file_size = int(totallen.text)

                            # 文件扩展名
                            fileext = appattach.find("fileext")
                            if fileext is not None and fileext.text:
                                msg.file_ext = fileext.text

                            # 附件ID
                            attachid = appattach.find("attachid")
                            if attachid is not None and attachid.text:
                                msg.attach_id = attachid.text

                            # CDN附件URL
                            cdnattachurl = appattach.find("cdnattachurl")
                            if cdnattachurl is not None and cdnattachurl.text:
                                msg.cdn_attach_url = cdnattachurl.text

                            # AES密钥
                            aeskey = appattach.find("aeskey")
                            if aeskey is not None and aeskey.text:
                                msg.aes_key = aeskey.text

                        # 获取MD5
                        md5 = appmsg.find("md5")
                        if md5 is not None and md5.text:
                            msg.file_md5 = md5.text

                        # 如果提供了GeweClient实例，使用API获取下载链接
                        if client and msg.content:
                            # 调用下载文件接口获取文件URL
                            try:
                                download_result = await client.message.download_file(
                                    msg.content
                                )
                                if (
                                    download_result
                                    and download_result.get("ret") == 200
                                    and "data" in download_result
                                ):
                                    file_url = download_result["data"].get(
                                        "fileUrl", ""
                                    )
                                    if file_url and client.download_url:
                                        msg.file_url = (
                                            f"{client.download_url}?url={file_url}"
                                        )
                            except Exception:
                                # 下载失败不影响消息处理
                                pass
                except Exception:
                    pass

        return msg 