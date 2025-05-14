"""文件相关消息处理器"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional

from opengewe.callback.models import BaseMessage, FileNoticeMessage, FileMessage
from opengewe.callback.handlers.base import BaseHandler


class FileNoticeMessageHandler(BaseHandler):
    """文件发送通知处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为文件发送通知"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 文件消息类型为49，且需要解析Content中的XML
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
                # 文件发送通知的appmsg.type为74
                return appmsg_type is not None and appmsg_type.text == "74"
            return False
        except Exception:
            return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理文件发送通知"""
        # 直接使用FileNoticeMessage类处理消息
        return FileNoticeMessage.from_dict(data)


class FileMessageHandler(BaseHandler):
    """文件消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为文件消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 文件消息类型为49，且需要解析Content中的XML
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
                # 文件消息的appmsg.type为6
                return appmsg_type is not None and appmsg_type.text == "6"
            return False
        except Exception:
            return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理文件消息"""
        # 直接使用FileMessage类处理消息
        return FileMessage.from_dict(data, self.client)
