from dataclasses import dataclass
from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET

from opengewechat.message.types import MessageType
from opengewechat.message.models.base import BaseMessage
from opengewechat.client import GewechatClient


@dataclass
class FileNoticeMessage(BaseMessage):
    """文件通知消息"""

    file_name: str = ""  # 文件名
    file_size: int = 0  # 文件大小(字节)
    file_id: str = ""  # 文件ID
    file_type: str = ""  # 文件类型

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FileNoticeMessage":
        """从字典创建文件通知消息对象"""
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
                msg.from_user = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_user = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取文件信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        title_node = appmsg.find("title")
                        if title_node is not None and title_node.text:
                            msg.file_name = title_node.text

                        file_attrs = appmsg.find("appattach")
                        if file_attrs is not None:
                            size_node = file_attrs.find("totallen")
                            if size_node is not None and size_node.text:
                                try:
                                    msg.file_size = int(size_node.text)
                                except ValueError:
                                    pass

                            file_ext_node = file_attrs.find("fileext")
                            if file_ext_node is not None and file_ext_node.text:
                                msg.file_type = file_ext_node.text

                            file_id_node = file_attrs.find("attachid")
                            if file_id_node is not None and file_id_node.text:
                                msg.file_id = file_id_node.text
                except Exception:
                    pass

        return msg


@dataclass
class FileMessage(BaseMessage):
    """文件消息"""

    file_name: str = ""  # 文件名
    file_size: int = 0  # 文件大小(字节)
    file_id: str = ""  # 文件ID
    file_type: str = ""  # 文件类型
    file_url: str = ""  # 文件下载链接
    aes_key: str = ""  # 文件加密密钥
    md5: str = ""  # 文件MD5

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], client: Optional[GewechatClient] = None
    ) -> "FileMessage":
        """从字典创建文件消息对象

        Args:
            data: 原始数据
            client: GewechatClient实例，用于下载文件
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
                msg.from_user = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_user = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取文件信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        title_node = appmsg.find("title")
                        if title_node is not None and title_node.text:
                            msg.file_name = title_node.text

                        file_attrs = appmsg.find("appattach")
                        if file_attrs is not None:
                            size_node = file_attrs.find("totallen")
                            if size_node is not None and size_node.text:
                                try:
                                    msg.file_size = int(size_node.text)
                                except ValueError:
                                    pass

                            file_ext_node = file_attrs.find("fileext")
                            if file_ext_node is not None and file_ext_node.text:
                                msg.file_type = file_ext_node.text

                            file_id_node = file_attrs.find("attachid")
                            if file_id_node is not None and file_id_node.text:
                                msg.file_id = file_id_node.text

                            aes_key_node = file_attrs.find("encryver")
                            if aes_key_node is not None and aes_key_node.text:
                                msg.aes_key = aes_key_node.text

                            md5_node = file_attrs.find("md5")
                            if md5_node is not None and md5_node.text:
                                msg.md5 = md5_node.text

                            # 如果提供了GewechatClient实例，使用API获取下载链接
                            if client and msg.file_id:
                                try:
                                    download_result = client.message.download_file(
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
