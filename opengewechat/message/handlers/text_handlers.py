"""文本相关消息处理器"""

from typing import Dict, Any, Optional

from opengewechat.message.models import BaseMessage, TextMessage, QuoteMessage
from opengewechat.message.handlers.base_handler import BaseHandler


class TextMessageHandler(BaseHandler):
    """文本消息处理器"""

    def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为文本消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 文本消息类型为1
        return data["Data"].get("MsgType") == 1

    def handle(self, data: Dict[str, Any]) -> Optional[TextMessage]:
        """处理文本消息"""
        return TextMessage.from_dict(data)


class QuoteHandler(BaseHandler):
    """引用消息处理器"""

    def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为引用消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 引用消息的类型为49，且appmsg.type为57
        if data["Data"].get("MsgType") != 49:
            return False

        content = data["Data"].get("Content", {}).get("string", "")
        try:
            import xml.etree.ElementTree as ET

            root = ET.fromstring(content)
            appmsg = root.find(".//appmsg")
            if appmsg is None:
                return False

            type_elem = appmsg.find("type")
            return type_elem is not None and type_elem.text == "57"
        except Exception:
            return False

    def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理引用消息"""
        # 直接使用QuoteMessage类处理消息
        return QuoteMessage.from_dict(data)
