from dataclasses import dataclass
from typing import Dict, Any
import xml.etree.ElementTree as ET

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import BaseMessage


@dataclass
class RevokeMessage(BaseMessage):
    """撤回消息"""

    revoke_msg_id: str = ""  # 被撤回的消息ID
    replace_msg: str = ""  # 替换消息
    notify_msg: str = ""  # 通知消息

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RevokeMessage":
        """从字典创建撤回消息对象"""
        msg = cls(
            type=MessageType.REVOKE,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_wxid = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 解析XML获取撤回信息
                try:
                    root = ET.fromstring(msg.content)
                    if root.tag == "sysmsg" and root.get("type") == "revokemsg":
                        revoke_node = root.find("revokemsg")
                        if revoke_node is not None:
                            # 获取被撤回的消息ID
                            msg_id_node = revoke_node.find("newmsgid")
                            if msg_id_node is not None and msg_id_node.text:
                                msg.revoke_msg_id = msg_id_node.text

                            # 获取替换消息
                            replace_node = revoke_node.find("replacemsg")
                            if replace_node is not None and replace_node.text:
                                msg.replace_msg = replace_node.text
                                msg.notify_msg = replace_node.text
                except Exception:
                    pass

        return msg


@dataclass
class PatMessage(BaseMessage):
    """拍一拍消息"""

    from_username: str = ""  # 发送拍一拍的用户wxid
    chat_username: str = ""  # 聊天对象wxid
    patted_username: str = ""  # 被拍的用户wxid
    pat_suffix: str = ""  # 拍一拍后缀
    pat_suffix_version: str = ""  # 拍一拍后缀版本
    template: str = ""  # 拍一拍模板消息

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PatMessage":
        """从字典创建拍一拍消息对象"""
        msg = cls(
            type=MessageType.PAT,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_wxid = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取拍一拍信息
                try:
                    root = ET.fromstring(msg.content)
                    if root.tag == "sysmsg" and root.get("type") == "pat":
                        pat_node = root.find("pat")
                        if pat_node is not None:
                            # 获取拍一拍相关信息
                            from_username_node = pat_node.find("fromusername")
                            msg.from_username = (
                                from_username_node.text
                                if from_username_node is not None
                                and from_username_node.text
                                else ""
                            )

                            chat_username_node = pat_node.find("chatusername")
                            msg.chat_username = (
                                chat_username_node.text
                                if chat_username_node is not None
                                and chat_username_node.text
                                else ""
                            )

                            patted_username_node = pat_node.find("pattedusername")
                            msg.patted_username = (
                                patted_username_node.text
                                if patted_username_node is not None
                                and patted_username_node.text
                                else ""
                            )

                            pat_suffix_node = pat_node.find("patsuffix")
                            msg.pat_suffix = (
                                pat_suffix_node.text
                                if pat_suffix_node is not None and pat_suffix_node.text
                                else ""
                            )

                            pat_suffix_version_node = pat_node.find("patsuffixversion")
                            msg.pat_suffix_version = (
                                pat_suffix_version_node.text
                                if pat_suffix_version_node is not None
                                and pat_suffix_version_node.text
                                else ""
                            )

                            template_node = pat_node.find("template")
                            if template_node is not None and template_node.text:
                                msg.template = template_node.text
                except Exception:
                    pass

        return msg


@dataclass
class SyncMessage(BaseMessage):
    """同步消息"""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SyncMessage":
        """从字典创建同步消息对象"""
        msg = cls(
            type=MessageType.SYNC,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_wxid = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

        return msg


@dataclass
class OfflineMessage(BaseMessage):
    """掉线通知消息"""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OfflineMessage":
        """从字典创建掉线通知消息对象"""
        msg = cls(
            type=MessageType.OFFLINE,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        return msg
