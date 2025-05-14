"""联系人相关消息处理器"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional

from opengewe.callback.models import (
    BaseMessage,
    FriendRequestMessage,
    CardMessage,
    ContactUpdateMessage,
    ContactDeletedMessage,
)
from opengewe.callback.handlers.base import BaseHandler


class CardHandler(BaseHandler):
    """名片消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为名片消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 名片消息类型为42
        return data["Data"].get("MsgType") == 42

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理名片消息"""
        # 直接使用CardMessage类处理消息
        return CardMessage.from_dict(data)


class FriendRequestHandler(BaseHandler):
    """好友添加请求处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为好友添加请求"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 好友添加请求消息的MsgType有多种可能
        msg_type = data["Data"].get("MsgType")
        if msg_type not in [37, 0, 2, 42]:  # 增加可能的MsgType类型
            return False

        # 检查Content是否包含好友请求信息
        content = data["Data"].get("Content", {}).get("string", "")
        if not content:
            return False

        # 特殊判断：如果FromUserName是"fmessage"，大概率是好友请求
        from_wxid = data["Data"].get("FromUserName", {}).get("string", "")
        if from_wxid == "fmessage":
            return True

        try:
            root = ET.fromstring(content)
            # 检查是否为好友请求格式的XML
            if root.tag == "msg":
                # 方式1: 检查是否有fromusername、encryptusername或antispamticket等属性
                attributes_to_check = [
                    "fromusername",
                    "encryptusername",
                    "ticket",
                    "antispamticket",
                    "sourceusername",
                ]

                for attr in attributes_to_check:
                    if root.get(attr) is not None:
                        return True

                # 方式2: 检查是否有username或encryptusername等元素
                tags_to_check = [
                    "username",
                    "encryptusername",
                    "ticket",
                    "fromusername",
                    "antispamticket",
                ]

                for elem in root.findall(".//*"):
                    if elem.tag in tags_to_check:
                        return True

                # 方式3: 检查XML内容是否包含特定文本
                texts_to_check = [
                    "fromusername",
                    "encryptusername",
                    "ticket",
                    "antispamticket",
                ]

                for text in texts_to_check:
                    if text in content:
                        return True

                # 方式4: 检查是否有brandlist元素，可能表示好友请求
                if root.find(".//brandlist") is not None:
                    return True
        except Exception:
            # 解析失败，可能不是符合格式的XML
            pass

        # 其他特征检查：检查PushContent是否包含好友请求相关文本
        push_content = data["Data"].get("PushContent", "")
        if isinstance(push_content, str) and (
            "请求添加你为朋友" in push_content
            or "请求加你为好友" in push_content
            or "[名片]" in push_content
        ):
            return True

        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理好友添加请求"""
        # 直接使用FriendRequestMessage类处理消息
        return FriendRequestMessage.from_dict(data)


class ContactUpdateHandler(BaseHandler):
    """好友通过验证及好友资料变更通知处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为好友通过验证或好友资料变更通知"""
        if data.get("TypeName") != "ModContacts":
            return False

        if "Data" not in data:
            return False

        # 判断是否为联系人信息（非群聊）
        if "UserName" in data["Data"] and "string" in data["Data"]["UserName"]:
            username = data["Data"]["UserName"]["string"]
            return "@chatroom" not in username

        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理好友通过验证或好友资料变更通知"""
        # 直接使用ContactUpdateMessage类处理消息
        return ContactUpdateMessage.from_dict(data)


class ContactDeletedHandler(BaseHandler):
    """删除好友和退出群聊通知处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为删除好友或退出群聊通知"""
        if data.get("TypeName") != "DelContacts":
            return False

        if "Data" not in data:
            return False

        # 有UserName字段则为可处理的消息
        return "UserName" in data["Data"] and "string" in data["Data"]["UserName"]

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理删除好友或退出群聊通知"""
        # 直接使用ContactDeletedMessage类处理消息
        return ContactDeletedMessage.from_dict(data)
