"""文件相关消息处理器"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional

from opengewechat.message.models import BaseMessage, FileNoticeMessage, FileMessage
from opengewechat.message.handlers.base_handler import BaseHandler


class FileNoticeMessageHandler(BaseHandler):
    """文件发送通知处理器"""

    def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为文件发送通知"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 文件消息类型为49，且需要解析Content中的XML
        if data["Data"].get("MsgType") != 49:
            return False

        # 获取Content内容
        content = data["Data"].get("Content", {}).get("string", "")
        if not content:
            return False

        # 解析XML
        try:
            root = ET.fromstring(content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                appmsg_type = appmsg.find("type")
                # 文件发送通知的appmsg.type为74
                return appmsg_type is not None and appmsg_type.text == "74"
            return False
        except Exception:
            return False

    def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理文件发送通知"""
        # 直接使用FileNoticeMessage类处理消息
        return FileNoticeMessage.from_dict(data)


class FileMessageHandler(BaseHandler):
    """文件消息处理器"""

    def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为文件消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 文件消息类型为49，且需要解析Content中的XML
        if data["Data"].get("MsgType") != 49:
            return False

        # 获取Content内容
        content = data["Data"].get("Content", {}).get("string", "")
        if not content:
            return False

        # 解析XML
        try:
            root = ET.fromstring(content)
            appmsg = root.find("appmsg")
            if appmsg is not None:
                appmsg_type = appmsg.find("type")
                # 文件消息的appmsg.type为6
                return appmsg_type is not None and appmsg_type.text == "6"
            return False
        except Exception:
            return False

    def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理文件消息"""
        # 直接使用FileMessage类处理消息
        return FileMessage.from_dict(data, self.client)
