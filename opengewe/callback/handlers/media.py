"""媒体相关消息处理器"""

from typing import Dict, Any, Optional

from opengewe.callback.models import (
    ImageMessage,
    VoiceMessage,
    VideoMessage,
    EmojiMessage,
)
from opengewe.callback.handlers.base import BaseHandler


class ImageMessageHandler(BaseHandler):
    """图片消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为图片消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 图片消息类型为3
        return data["Data"].get("MsgType") == 3

    async def handle(self, data: Dict[str, Any]) -> Optional[ImageMessage]:
        """处理图片消息"""
        return await ImageMessage.from_dict(data, self.client)


class VoiceMessageHandler(BaseHandler):
    """语音消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为语音消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 语音消息类型为34
        return data["Data"].get("MsgType") == 34

    async def handle(self, data: Dict[str, Any]) -> Optional[VoiceMessage]:
        """处理语音消息"""
        return await VoiceMessage.from_dict(data, self.client)


class VideoMessageHandler(BaseHandler):
    """视频消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为视频消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 视频消息类型为43
        return data["Data"].get("MsgType") == 43

    async def handle(self, data: Dict[str, Any]) -> Optional[VideoMessage]:
        """处理视频消息"""
        return await VideoMessage.from_dict(data, self.client)


class EmojiMessageHandler(BaseHandler):
    """表情消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为表情消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 表情消息类型为47
        return data["Data"].get("MsgType") == 47

    async def handle(self, data: Dict[str, Any]) -> Optional[EmojiMessage]:
        """处理表情消息"""
        return await EmojiMessage.from_dict(data)
