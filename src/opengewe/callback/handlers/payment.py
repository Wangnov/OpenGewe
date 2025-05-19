"""支付相关消息处理器"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional

from opengewe.callback.models import BaseMessage, TransferMessage, RedPacketMessage
from opengewe.callback.handlers.base import BaseHandler


class TransferHandler(BaseHandler):
    """转账消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为转账消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 转账消息类型为49
        if data["Data"].get("MsgType") != 49:
            return False

        # 获取内容进一步判断
        content = data["Data"].get("Content", {}).get("string", "")
        try:
            if content:
                root = ET.fromstring(content)
                appmsg = root.find("appmsg")
                if appmsg is not None:
                    # 转账消息的类型标识为2000
                    type_node = appmsg.find("type")
                    return type_node is not None and type_node.text == "2000"
        except Exception:
            pass

        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理转账消息"""
        # 直接使用TransferMessage类处理消息
        return TransferMessage.from_dict(data)


class RedPacketHandler(BaseHandler):
    """红包消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为红包消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 红包消息类型为49
        if data["Data"].get("MsgType") != 49:
            return False

        # 获取内容进一步判断
        content = data["Data"].get("Content", {}).get("string", "")
        try:
            if content:
                root = ET.fromstring(content)
                appmsg = root.find("appmsg")
                if appmsg is not None:
                    # 红包消息的类型标识为2001(普通红包)或2002(群红包)
                    type_node = appmsg.find("type")
                    return type_node is not None and type_node.text in ["2001", "2002"]
        except Exception:
            pass

        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理红包消息"""
        # 直接使用RedPacketMessage类处理消息
        return RedPacketMessage.from_dict(data)
