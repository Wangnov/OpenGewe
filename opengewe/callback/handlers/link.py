"""链接相关消息处理器"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional

from opengewe.callback.models import (
    BaseMessage,
    LinkMessage,
    FinderMessage,
    MiniappMessage,
)
from opengewe.callback.handlers.base import BaseHandler


class LinkMessageHandler(BaseHandler):
    """链接消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为链接消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 链接消息类型为49，且需要解析Content中的XML
        if data["Data"].get("MsgType") != 49:
            return False

        # 获取处理过的XML内容
        xml_content = self.extract_xml_content(data)
        if not xml_content:
            return False

        # 解析XML
        try:
            root = ET.fromstring(xml_content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                appmsg_type = appmsg.find("type")
                # 链接消息的appmsg.type为5，但需要排除群聊邀请消息
                if appmsg_type is not None and appmsg_type.text == "5":
                    title = appmsg.find("title")
                    if title is not None and "邀请你加入群聊" not in title.text:
                        return True
            return False
        except Exception:
            return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理链接消息"""
        return LinkMessage.from_dict(data)


class FinderHandler(BaseHandler):
    """视频号消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为视频号消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 视频号消息类型为49
        if data["Data"].get("MsgType") != 49:
            return False

        # 获取处理过的XML内容
        xml_content = self.extract_xml_content(data)
        if not xml_content:
            return False

        try:
            root = ET.fromstring(xml_content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                # 视频号消息的类型标识为19(视频号视频分享)或22(视频号直播分享)
                type_node = appmsg.find("type")
                if type_node is not None and type_node.text in ["19", "22"]:
                    return True

                # 查找finderFeed节点，存在则为视频号消息
                finder_feed = appmsg.find("finderFeed")
                return finder_feed is not None
        except Exception:
            pass

        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理视频号消息"""
        # 直接使用FinderMessage类处理消息
        return FinderMessage.from_dict(data)


class MiniappHandler(BaseHandler):
    """小程序消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为小程序消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 小程序消息类型
        if data["Data"].get("MsgType") != 49:  # 小程序消息使用与链接相同的消息类型49
            return False

        # 获取处理过的XML内容
        xml_content = self.extract_xml_content(data)
        if not xml_content:
            return False

        try:
            root = ET.fromstring(xml_content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                # 小程序消息的类型标识为33
                type_node = appmsg.find("type")
                return type_node is not None and type_node.text == "33"
        except Exception:
            pass

        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理小程序消息"""
        # 直接使用MiniappMessage类处理消息
        return MiniappMessage.from_dict(data)
