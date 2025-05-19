"""位置相关消息处理器"""

from typing import Dict, Any, Optional

from opengewe.callback.models import BaseMessage, LocationMessage
from opengewe.callback.handlers.base import BaseHandler


class LocationMessageHandler(BaseHandler):
    """地理位置消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为地理位置消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 地理位置消息类型为48
        return data["Data"].get("MsgType") == 48

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理地理位置消息"""
        # 直接使用LocationMessage类处理消息
        return LocationMessage.from_dict(data)
