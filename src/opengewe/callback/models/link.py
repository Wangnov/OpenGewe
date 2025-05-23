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
    
    # 设置消息类型类变量
    message_type = MessageType.LINK
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理链接消息特有数据"""
        # 解析XML获取链接信息
        try:
            root = ET.fromstring(self.content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                # 获取链接类型，确保是链接消息(type=5)
                link_type = appmsg.find("type")
                if link_type is not None and link_type.text == "5":
                    title = appmsg.find("title")
                    if title is not None:
                        self.title = title.text or ""

                    desc = appmsg.find("des")
                    if desc is not None:
                        self.description = desc.text or ""

                    url = appmsg.find("url")
                    if url is not None:
                        self.url = url.text or ""

                    thumb_url = appmsg.find("thumburl")
                    if thumb_url is not None:
                        self.thumb_url = thumb_url.text or ""

                    source_username = appmsg.find("sourceusername")
                    if source_username is not None:
                        self.source_username = source_username.text or ""

                    source_displayname = appmsg.find("sourcedisplayname")
                    if source_displayname is not None:
                        self.source_displayname = source_displayname.text or ""
        except Exception:
            pass


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
    
    # 设置消息类型类变量
    message_type = MessageType.MINIAPP
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理小程序消息特有数据"""
        # 解析XML获取小程序信息
        try:
            root = ET.fromstring(self.content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                # 获取小程序类型，确保是小程序消息(type=33)
                app_type = appmsg.find("type")
                if app_type is not None and app_type.text == "33":
                    title = appmsg.find("title")
                    if title is not None:
                        self.title = title.text or ""

                    desc = appmsg.find("des")
                    if desc is not None:
                        self.description = desc.text or ""

                    url = appmsg.find("url")
                    if url is not None:
                        self.url = url.text or ""

                    # 获取小程序信息
                    weappinfo = appmsg.find("weappinfo")
                    if weappinfo is not None:
                        app_id_node = weappinfo.find("appid")
                        if app_id_node is not None:
                            self.app_id = app_id_node.text or ""

                        username_node = weappinfo.find("username")
                        if username_node is not None:
                            self.username = username_node.text or ""

                        pagepath_node = weappinfo.find("pagepath")
                        if pagepath_node is not None:
                            self.pagepath = pagepath_node.text or ""

                        version_node = weappinfo.find("version")
                        if version_node is not None:
                            self.version = version_node.text or ""

                        icon_url_node = weappinfo.find("weappiconurl")
                        if icon_url_node is not None:
                            self.icon_url = icon_url_node.text or ""
        except Exception:
            pass


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
    
    # 设置消息类型类变量
    message_type = MessageType.FINDER
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理视频号消息特有数据"""
        # 解析XML获取视频号信息
        try:
            root = ET.fromstring(self.content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                # 获取视频号ID
                finder_info = appmsg.find("finderFeed")
                if finder_info is not None:
                    self.finder_id = finder_info.get("id", "")
                    self.finder_username = finder_info.get("username", "")
                    self.finder_nickname = finder_info.get("nickname", "")
                    self.object_id = finder_info.get("objectId", "")
                    self.object_type = finder_info.get("objectType", "")
                    self.object_title = finder_info.get("title", "")
                    self.object_desc = finder_info.get("desc", "")
                    self.cover_url = finder_info.get("coverUrl", "")

                # 获取URL
                url_node = appmsg.find("url")
                if url_node is not None and url_node.text:
                    self.url = url_node.text
        except Exception:
            pass
