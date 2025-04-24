"""位置相关消息处理器"""
from typing import Dict, Any, Optional

from opengewechat.message.models import BaseMessage, LocationMessage
from opengewechat.message.handlers.base_handler import BaseHandler


class LocationMessageHandler(BaseHandler):
    """地理位置消息处理器"""

    def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为地理位置消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 地理位置消息类型为48
        return data["Data"].get("MsgType") == 48

    def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理地理位置消息"""
        # 直接使用LocationMessage类处理消息
        return LocationMessage.from_dict(data)
