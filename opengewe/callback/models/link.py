from dataclasses import dataclass
from typing import Dict, Any, Optional, TYPE_CHECKING
import xml.etree.ElementTree as ET

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import BaseMessage

# 使用TYPE_CHECKING条件导入
if TYPE_CHECKING:
    from opengewe.client import GeweClient


@dataclass
class LinkMessage(BaseMessage):
    """链接消息"""

    title: str = ""  # 链接标题
    description: str = ""  # 链接描述
    url: str = ""  # 链接URL
    thumb_url: str = ""  # 缩略图URL
    source_username: str = ""  # 来源用户名
    source_displayname: str = ""  # 来源显示名称

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], client: Optional["GeweClient"] = None
    ) -> "LinkMessage":
        """从字典创建链接消息对象

        Args:
            data: 原始数据
            client: GeweClient实例
        """
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
                msg.from_wxid = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取链接信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        # 获取链接类型，确保是链接消息(type=5)
                        link_type = appmsg.find("type")
                        if link_type is not None and link_type.text == "5":
                            title = appmsg.find("title")
                            if title is not None:
                                msg.title = title.text or ""

                            desc = appmsg.find("des")
                            if desc is not None:
                                msg.description = desc.text or ""

                            url = appmsg.find("url")
                            if url is not None:
                                msg.url = url.text or ""

                            thumb_url = appmsg.find("thumburl")
                            if thumb_url is not None:
                                msg.thumb_url = thumb_url.text or ""

                            source_username = appmsg.find("sourceusername")
                            if source_username is not None:
                                msg.source_username = source_username.text or ""

                            source_displayname = appmsg.find("sourcedisplayname")
                            if source_displayname is not None:
                                msg.source_displayname = source_displayname.text or ""
                except Exception:
                    pass

        return msg


@dataclass
class MiniappMessage(BaseMessage):
    """小程序消息"""

    title: str = ""  # 小程序标题
    description: str = ""  # 小程序描述
    url: str = ""  # 小程序URL
    app_id: str = ""  # 小程序AppID
    username: str = ""  # 小程序原始ID
    pagepath: str = ""  # 小程序页面路径
    thumb_url: str = ""  # 缩略图URL
    icon_url: str = ""  # 小程序图标URL
    version: str = ""  # 小程序版本

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], client: Optional["GeweClient"] = None
    ) -> "MiniappMessage":
        """从字典创建小程序消息对象

        Args:
            data: 原始数据
            client: GeweClient实例
        """
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
                msg.from_wxid = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取小程序信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        # 获取小程序类型，确保是小程序消息(type=33)
                        app_type = appmsg.find("type")
                        if app_type is not None and app_type.text == "33":
                            title = appmsg.find("title")
                            if title is not None:
                                msg.title = title.text or ""

                            desc = appmsg.find("des")
                            if desc is not None:
                                msg.description = desc.text or ""

                            url = appmsg.find("url")
                            if url is not None:
                                msg.url = url.text or ""

                            # 获取小程序信息
                            weappinfo = appmsg.find("weappinfo")
                            if weappinfo is not None:
                                app_id_node = weappinfo.find("appid")
                                if app_id_node is not None:
                                    msg.app_id = app_id_node.text or ""

                                username_node = weappinfo.find("username")
                                if username_node is not None:
                                    msg.username = username_node.text or ""

                                pagepath_node = weappinfo.find("pagepath")
                                if pagepath_node is not None:
                                    msg.pagepath = pagepath_node.text or ""

                                version_node = weappinfo.find("version")
                                if version_node is not None:
                                    msg.version = version_node.text or ""

                                icon_url_node = weappinfo.find("weappiconurl")
                                if icon_url_node is not None:
                                    msg.icon_url = icon_url_node.text or ""
                except Exception:
                    pass

        return msg 
    


@dataclass
class FinderMessage(BaseMessage):
    """视频号消息"""

    finder_id: str = ""  # 视频号ID
    finder_username: str = ""  # 视频号用户名
    finder_nickname: str = ""  # 视频号昵称
    object_id: str = ""  # 内容ID
    object_type: str = ""  # 内容类型，例如视频、直播等
    object_title: str = ""  # 内容标题
    object_desc: str = ""  # 内容描述
    cover_url: str = ""  # 封面URL
    url: str = ""  # 分享链接URL

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FinderMessage":
        """从字典创建视频号消息对象"""
        msg = cls(
            type=MessageType.FINDER,
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

                # 解析XML获取视频号信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        # 获取视频号ID
                        finder_info = appmsg.find("finderFeed")
                        if finder_info is not None:
                            msg.finder_id = finder_info.get("id", "")
                            msg.finder_username = finder_info.get("username", "")
                            msg.finder_nickname = finder_info.get("nickname", "")
                            msg.object_id = finder_info.get("objectId", "")
                            msg.object_type = finder_info.get("objectType", "")
                            msg.object_title = finder_info.get("title", "")
                            msg.object_desc = finder_info.get("desc", "")
                            msg.cover_url = finder_info.get("coverUrl", "")

                        # 获取URL
                        url_node = appmsg.find("url")
                        if url_node is not None and url_node.text:
                            msg.url = url_node.text
                except Exception:
                    pass

        return msg
