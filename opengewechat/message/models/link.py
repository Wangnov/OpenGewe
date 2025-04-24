from dataclasses import dataclass, field
from typing import Dict, Any
import xml.etree.ElementTree as ET

from opengewechat.message.types import MessageType
from opengewechat.message.models.base import BaseMessage


@dataclass
class LinkMessage(BaseMessage):
    """链接消息"""

    title: str = ""  # 标题
    description: str = ""  # 描述
    url: str = ""  # 链接URL
    thumb_url: str = ""  # 缩略图URL

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LinkMessage":
        """从字典创建链接消息对象"""
        msg = cls(
            type=MessageType.LINK,
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

                # 解析XML获取链接信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        title_node = appmsg.find("title")
                        msg.title = (
                            title_node.text
                            if title_node is not None and title_node.text
                            else ""
                        )

                        des_node = appmsg.find("des")
                        msg.description = (
                            des_node.text
                            if des_node is not None and des_node.text
                            else ""
                        )

                        url_node = appmsg.find("url")
                        msg.url = (
                            url_node.text
                            if url_node is not None and url_node.text
                            else ""
                        )

                        thumburl_node = appmsg.find("thumburl")
                        msg.thumb_url = (
                            thumburl_node.text
                            if thumburl_node is not None and thumburl_node.text
                            else ""
                        )
                except Exception:
                    pass

        return msg


@dataclass
class MiniappMessage(BaseMessage):
    """小程序消息"""

    title: str = ""  # 小程序标题
    description: str = ""  # 小程序描述
    username: str = ""  # 小程序username
    app_id: str = ""  # 小程序appid
    thumb_url: str = ""  # 小程序缩略图
    source_username: str = ""  # 来源小程序username
    source_display_name: str = ""  # 来源小程序显示名称
    weapp_info: Dict[str, Any] = field(default_factory=dict)  # 小程序信息
    raw_data: Dict[str, Any] = field(default_factory=dict)  # 原始数据

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MiniappMessage":
        """从字典创建小程序消息对象"""
        msg = cls(
            type=MessageType.MINIAPP,
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

                # 解析XML获取小程序信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        # 获取标题和描述
                        title_node = appmsg.find("title")
                        msg.title = (
                            title_node.text
                            if title_node is not None and title_node.text
                            else ""
                        )

                        des_node = appmsg.find("des")
                        msg.description = (
                            des_node.text
                            if des_node is not None and des_node.text
                            else ""
                        )

                        # 获取小程序信息
                        weapp_info = appmsg.find("weappinfo")
                        if weapp_info is not None:
                            # 获取小程序username和appid
                            username_node = weapp_info.find("username")
                            msg.username = (
                                username_node.text
                                if username_node is not None and username_node.text
                                else ""
                            )

                            appid_node = weapp_info.find("appid")
                            msg.app_id = (
                                appid_node.text
                                if appid_node is not None and appid_node.text
                                else ""
                            )

                            # 获取来源小程序信息
                            source_username_node = weapp_info.find("sourcedisplayname")
                            msg.source_display_name = (
                                source_username_node.text
                                if source_username_node is not None
                                and source_username_node.text
                                else ""
                            )

                            source_username_node = weapp_info.find("sourceusername")
                            msg.source_username = (
                                source_username_node.text
                                if source_username_node is not None
                                and source_username_node.text
                                else ""
                            )

                            # 构建小程序信息字典
                            msg.weapp_info = {
                                "username": msg.username,
                                "appid": msg.app_id,
                                "source_username": msg.source_username,
                                "source_display_name": msg.source_display_name,
                            }

                        # 获取缩略图
                        thumburl_node = appmsg.find("thumburl")
                        msg.thumb_url = (
                            thumburl_node.text
                            if thumburl_node is not None and thumburl_node.text
                            else ""
                        )
                except Exception:
                    pass

        return msg
