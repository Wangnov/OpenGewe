"""群聊相关消息处理器"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional

from opengewe.callback.models import (
    BaseMessage,
    GroupInvitedMessage,
    GroupInfoUpdateMessage,
    GroupTodoMessage,
    GroupInviteMessage,
    GroupRemovedMessage,
    GroupKickMessage,
    GroupDismissMessage,
)
from opengewe.callback.handlers.base import BaseHandler


class GroupInviteMessageHandler(BaseHandler):
    """群聊邀请确认通知消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为群聊邀请确认通知消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 群聊邀请确认通知类型为49
        if data["Data"].get("MsgType") != 49:
            return False

        # 获取Content内容
        content = data["Data"].get("Content", {}).get("string", "")
        if not content:
            return False

        # 解析XML，判断是否包含"邀请你加入群聊"
        try:
            root = ET.fromstring(content)
            # 检查是否为msg格式且有appmsg子节点
            if root.tag != "msg":
                return False

            appmsg_node = root.find("appmsg")
            if appmsg_node is None:
                return False

            # 检查标题是否包含"邀请你加入群聊"
            title_node = appmsg_node.find("title")
            if title_node is None or not title_node.text:
                return False

            return "邀请你加入群聊" in title_node.text
        except Exception:
            return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理群聊邀请确认通知消息"""
        # 直接使用GroupInviteMessage类处理消息
        return GroupInviteMessage.from_dict(data)


class GroupInvitedMessageHandler(BaseHandler):
    """群聊邀请消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为群聊邀请消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 群聊邀请消息类型为49，且需要解析Content中的XML
        if data["Data"].get("MsgType") != 10002:
            return False

        # 获取Content内容
        content = data["Data"].get("Content", {}).get("string", "")
        if not content:
            return False
        # 解析XML
        try:
            # 处理可能包含非XML前缀的内容（如"chatroom:"）
            xml_content = content
            if ":" in content and "<" in content:
                # 尝试分离非XML前缀
                parts = content.split(":", 1)
                if len(parts) == 2 and "<" in parts[1]:
                    xml_content = parts[1]

            root = ET.fromstring(xml_content)
            # 检查是否为系统消息模板
            if root.tag != "sysmsg" or root.get("type") != "sysmsgtemplate":
                return False

            # 查找模板内容
            template_node = root.find(".//template")
            if template_node is not None and template_node.text:
                # 检查是否包含邀请加入群聊的模板
                return "邀请你加入了群聊" in template_node.text

            return False
        except Exception:
            return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理群聊邀请消息"""
        # 直接使用GroupInvitedMessage类处理消息
        return GroupInvitedMessage.from_dict(data)


class GroupInfoUpdateHandler(BaseHandler):
    """群信息变更通知处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为群信息变更通知"""
        if data.get("TypeName") != "ModContacts":
            return False

        if "Data" not in data:
            return False

        # 判断是否为群聊信息（群ID通常以@chatroom结尾）
        if "UserName" in data["Data"] and "string" in data["Data"]["UserName"]:
            username = data["Data"]["UserName"]["string"]
            return "@chatroom" in username

        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理群信息变更通知"""
        # 直接使用GroupInfoUpdateMessage类处理消息
        return await GroupInfoUpdateMessage.from_dict(data)


class GroupTodoHandler(BaseHandler):
    """群待办消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为群待办消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        msg_data = data.get("Data", {})
        # 先检查MsgType是否是系统消息类型10000或10002
        if msg_data.get("MsgType") not in [10000, 10002]:
            return False

        # 获取Content内容
        content = ""
        if "Content" in msg_data and "string" in msg_data["Content"]:
            content = msg_data["Content"]["string"]

        if not content:
            return False

        # 确保我们可以处理所有类型的群待办消息
        # 1. 直接检查关键字
        if "todo" in content.lower() or "待办" in content:
            return True

        # 2. 检查XML结构
        try:
            # 处理可能包含非XML前缀的内容
            xml_content = content
            if ":" in content and "<" in content:
                parts = content.split(":", 1)
                if len(parts) == 2 and "<" in parts[1]:
                    xml_content = parts[1]

            root = ET.fromstring(xml_content)

            # 检查是否为roomtoolstips类型的系统消息
            if root.tag == "sysmsg" and root.get("type") == "roomtoolstips":
                todo_node = root.find("todo")
                if todo_node is not None:
                    return True

            # 检查是否为传统todo类型的系统消息
            if root.tag == "sysmsg" and root.get("type") == "todo":
                return True

        except Exception:
            # 如果XML解析失败，依然检查原始内容
            if "<todo>" in content and "</todo>" in content:
                return True

        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理群待办消息"""
        # 直接使用GroupTodoMessage类处理消息
        return GroupTodoMessage.from_dict(data)


class GroupRemovedMessageHandler(BaseHandler):
    """被移除群聊消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为被移除群聊消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 系统消息类型为10000
        if data["Data"].get("MsgType") != 10000:
            return False

        content = data["Data"].get("Content", {}).get("string", "")
        return "移出了群聊" in content

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理被移除群聊消息"""
        try:
            message = GroupRemovedMessage.from_dict(data)
            return message
        except Exception as e:
            return None


class GroupKickMessageHandler(BaseHandler):
    """踢出群聊消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为踢出群聊消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 系统消息类型为10000
        if data["Data"].get("MsgType") != 10000:
            return False

        content = data["Data"].get("Content", {}).get("string", "")
        return "将" in content and "移出了群聊" in content

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理踢出群聊消息"""
        try:
            message = GroupKickMessage.from_dict(data)
            return message
        except Exception as e:
            return None


class GroupDismissMessageHandler(BaseHandler):
    """解散群聊消息处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为解散群聊消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 系统消息类型为10000
        if data["Data"].get("MsgType") != 10000:
            return False

        content = data["Data"].get("Content", {}).get("string", "")
        return "群主已解散群聊" in content

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理解散群聊消息"""
        try:
            message = GroupDismissMessage.from_dict(data)
            return message
        except Exception as e:
            return None
