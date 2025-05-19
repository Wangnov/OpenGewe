"""系统相关消息处理器"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional

from opengewe.callback.types import MessageType
from opengewe.callback.models import (
    BaseMessage,
    PatMessage,
    RevokeMessage,
    OfflineMessage,
    GroupRemovedMessage,
    GroupRenameMessage,
    GroupOwnerChangeMessage,
    GroupKickMessage,
    GroupDismissMessage,
    GroupAnnouncementMessage,
    GroupInvitedMessage,
)
from opengewe.callback.models.system import SyncMessage
from opengewe.callback.handlers.base import BaseHandler


class SysmsgHandler(BaseHandler):
    """系统消息处理器，用于处理各种系统消息，包括拍一拍(pat)、撤回消息等"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为系统消息"""
        if data.get("TypeName") != "AddMsg":
            return False

        if "Data" not in data:
            return False

        # 处理 MsgType=51 的同步消息
        if data["Data"].get("MsgType") == 51:
            return True

        # 处理 MsgType=49 的群公告消息
        if data["Data"].get("MsgType") == 49:
            content = data["Data"].get("Content", {}).get("string", "")
            if not content:
                return False

            # 检查是否包含群公告特征
            return "<announcement>" in content and "<announcement_id>" in content

        # 处理 MsgType=10002 的系统消息
        if data["Data"].get("MsgType") == 10002:
            # 获取Content内容
            content = data["Data"].get("Content", {}).get("string", "")
            if not content:
                return False

            # 检查是否为群公告
            if "mmchatroombarannouncememt" in content or "<announcement_id>" in content:
                return True

            # 明确排除roomtoolstips类型，让专门的GroupTodoHandler来处理它们
            if '<sysmsg type="roomtoolstips">' in content or "roomtoolstips" in content:
                return False

            # 解析XML获取系统消息类型
            try:
                # 处理xml前缀
                if ":" in content and "<" in content:
                    parts = content.split(":", 1)
                    if len(parts) == 2 and "<" in parts[1]:
                        xml_content = parts[1]
                else:
                    xml_content = content

                root = ET.fromstring(xml_content)
                # 检查是否为系统消息
                if root.tag != "sysmsg":
                    return False

                # 获取系统消息类型
                sysmsg_type = root.get("type")
                if not sysmsg_type:
                    return False

                # 明确排除roomtoolstips类型
                if sysmsg_type == "roomtoolstips":
                    return False

                # 对于sysmsgtemplate类型，检查是否包含任何模板消息
                if sysmsg_type == "sysmsgtemplate":
                    template_node = root.find(".//template")
                    return template_node is not None and template_node.text is not None

                # 支持的其他系统消息类型
                return sysmsg_type in [
                    "pat",
                    "revokemsg",
                    "mmchatroombarannouncememt",
                ]
            except Exception:
                return False

        # 处理 MsgType=10000 的系统消息，包括被移除群聊通知、修改群名、更换群主等
        elif data["Data"].get("MsgType") == 10000:
            # 获取Content内容
            content = data["Data"].get("Content", {}).get("string", "")
            if not content:
                return False

            # 检查是否包含我们支持处理的系统消息
            return (
                ("被" in content and "移出群聊" in content)  # 被移除群聊
                or ("修改群名为" in content)  # 修改群名
                or ("成为新群主" in content)  # 更换群主
            )

        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理系统消息"""
        # 获取Content内容
        content = data["Data"].get("Content", {}).get("string", "")
        msg_type = data["Data"].get("MsgType")

        # 首先检查通用的群公告特征，适用于多种消息类型
        if (
            msg_type in [10002, 49]
            and ("<announcement_id>" in content or "announcement_id" in content)
            and (
                "<mmchatroombarannouncememt>" in content or "<announcement>" in content
            )
        ):
            return GroupAnnouncementMessage.from_dict(data)

        # 处理 MsgType=51 的同步消息
        if data["Data"].get("MsgType") == 51:
            return SyncMessage.from_dict(data)

        # 处理微信使用者自己触发的几个系统消息和别人触发的系统消息的区别
        if (
            data["Data"].get("MsgType") == 10000
            and content.startswith("你被")
            and content.endswith("移出群聊")
        ):
            return GroupRemovedMessage.from_dict(data)

        if data["Data"].get("MsgType") == 10000 and content.endswith("成为新群主"):
            return GroupOwnerChangeMessage.from_dict(data)

        if data["Data"].get("MsgType") == 10002 and "成为新群主" in content:
            return GroupOwnerChangeMessage.from_dict(data)

        if data["Data"].get("MsgType") == 10000 and content.startswith("你修改群名为"):
            return GroupRenameMessage.from_dict(data)

        # 处理群公告消息 - 合并判断逻辑并改进错误处理
        if data["Data"].get("MsgType") == 10002:
            # 先检查内容中是否包含关键字
            if "mmchatroombarannouncememt" in content:
                return GroupAnnouncementMessage.from_dict(data)

            # 冗余检查，确保不会遗漏群公告消息
            if "<sysmsg" in content and "<announcement_id>" in content:
                return GroupAnnouncementMessage.from_dict(data)

            # 如果关键字检查失败，尝试解析XML
            try:
                # 处理可能包含非XML前缀的内容
                xml_content = content
                if ":" in content and "<" in content:
                    parts = content.split(":", 1)
                    if len(parts) == 2 and "<" in parts[1]:
                        xml_content = parts[1]

                root = ET.fromstring(xml_content)
                if root.tag == "sysmsg":
                    sysmsg_type = root.get("type")
                    if sysmsg_type == "mmchatroombarannouncememt":
                        return GroupAnnouncementMessage.from_dict(data)
            except Exception:
                # 额外的检查，防止漏掉某些格式的群公告
                if (
                    "<mmchatroombarannouncememt>" in content
                    and "<announcement_id>" in content
                ):
                    return GroupAnnouncementMessage.from_dict(data)

        # 处理 MsgType=49 的群公告消息
        if data["Data"].get("MsgType") == 49:
            content = data["Data"].get("Content", {}).get("string", "")
            if "<announcement>" in content and "<announcement_id>" in content:
                return GroupAnnouncementMessage.from_dict(data)

        try:
            # 处理可能包含非XML前缀的内容（如"chatroom:"）
            xml_content = content
            if ":" in content and "<" in content:
                # 尝试分离非XML前缀
                parts = content.split(":", 1)
                if len(parts) == 2 and "<" in parts[1]:
                    xml_content = parts[1]

            root = ET.fromstring(xml_content)
            sysmsg_type = root.get("type")

            # 根据系统消息类型创建不同的消息对象
            if sysmsg_type == "pat":
                # 拍一拍消息
                return PatMessage.from_dict(data)
            elif sysmsg_type == "revokemsg":
                # 撤回消息
                return RevokeMessage.from_dict(data)
            elif sysmsg_type == "mmchatroombarannouncememt":
                # 群公告
                return GroupAnnouncementMessage.from_dict(data)
            else:
                # 处理 sysmsgtemplate 类型的系统消息
                if sysmsg_type == "sysmsgtemplate":
                    template_node = root.find(".//template")
                    if template_node is not None and template_node.text:
                        template_text = template_node.text

                        # 判断是哪种类型的系统模板消息
                        if "已成为新群主" in template_text:
                            return GroupOwnerChangeMessage.from_dict(data)
                        elif "已解散该群聊" in template_text:
                            return GroupDismissMessage.from_dict(data)
                        elif "移出了群聊" in template_text:
                            return GroupKickMessage.from_dict(data)
                        elif "修改群名为" in template_text:
                            return GroupRenameMessage.from_dict(data)
                        elif "邀请你加入了群聊" in template_text:
                            return GroupInvitedMessage.from_dict(data)

                # 默认处理为未知系统消息
                return BaseMessage(
                    type=MessageType.UNKNOWN,
                    app_id=data.get("Appid", ""),
                    wxid=data.get("Wxid", ""),
                    typename=data.get("TypeName", ""),
                    from_wxid=data["Data"].get("FromUserName", {}).get("string", ""),
                    to_wxid=data["Data"].get("ToUserName", {}).get("string", ""),
                    content=content,
                    raw_data=data,
                )
        except Exception:
            # 解析失败，返回基本系统消息
            return BaseMessage(
                type=MessageType.UNKNOWN,
                app_id=data.get("Appid", ""),
                wxid=data.get("Wxid", ""),
                typename=data.get("TypeName", ""),
                from_wxid=data["Data"].get("FromUserName", {}).get("string", ""),
                to_wxid=data["Data"].get("ToUserName", {}).get("string", ""),
                content=content,
                raw_data=data,
            )


class OfflineHandler(BaseHandler):
    """掉线通知处理器"""

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否为掉线通知"""
        return data.get("TypeName") == "Offline"

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理掉线通知"""
        # 直接使用OfflineMessage类处理消息
        return OfflineMessage.from_dict(data)
