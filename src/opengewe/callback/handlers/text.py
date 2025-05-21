"""文本相关消息处理器"""

from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET

from opengewe.callback.models import BaseMessage, TextMessage, QuoteMessage
from opengewe.callback.handlers.base import BaseHandler
from opengewe.logger import get_logger

# 获取客户端日志记录器
logger = get_logger("GeweClient")

class TextMessageHandler(BaseHandler):
    """文本消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为文本消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 文本消息类型为1
        return data["Data"].get("MsgType") == 1

    async def handle(self, data: Dict[str, Any]) -> Optional[TextMessage]:
        """处理文本消息"""
        try:
            logger.debug(f"TextMessageHandler开始处理消息: {data.get('TypeName')}")
            message = TextMessage.from_dict(data)
            logger.debug(f"TextMessageHandler成功创建消息对象: {message.text[:20] if message.text else 'Empty text'}")
            return message
        except Exception as e:
            logger.error(f"TextMessageHandler处理消息时出错: {e}", exc_info=True)
            return None


class QuoteHandler(BaseHandler):
    """引用消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
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
            # 处理可能包含非XML前缀的内容（如"chatroom:"或"wxid_xxx:\n"）
            xml_content = content

            # 处理群聊消息中的发送者前缀
            if ":" in content and "<" in content:
                # 尝试分离发送者ID和实际内容
                parts = content.split(":", 1)
                if len(parts) == 2 and "<" in parts[1]:
                    # 去除可能的换行符
                    xml_content = parts[1].strip()

            root = ET.fromstring(xml_content)
            appmsg = root.find(".//appmsg")
            if appmsg is None:
                return False

            type_elem = appmsg.find("type")
            return type_elem is not None and type_elem.text == "57"
        except Exception as e:
            logger.error(f"QuoteHandler判断消息类型时出错: {e}", exc_info=True)
            return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理引用消息"""
        try:
            logger.debug("QuoteHandler开始处理消息")
            # 直接使用QuoteMessage类处理消息
            message = QuoteMessage.from_dict(data)
            logger.debug("QuoteHandler成功创建消息对象")
            return message
        except Exception as e:
            logger.error(f"QuoteHandler处理消息时出错: {e}", exc_info=True)
            return None
