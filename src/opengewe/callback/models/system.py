from dataclasses import dataclass
from typing import Dict, Any, Optional, TYPE_CHECKING
import xml.etree.ElementTree as ET

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import SystemBaseMessage

if TYPE_CHECKING:
    from opengewe.client import GeweClient


@dataclass
class RevokeMessage(SystemBaseMessage):
    """撤回消息"""
    revoke_msg_id: str = ""  # 被撤回的消息ID
    replace_msg: str = ""  # 替换消息
    notify_msg: str = ""  # 通知消息
    
    # 设置消息类型类变量
    message_type = MessageType.REVOKE
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理撤回消息特有数据"""
        # 解析XML获取撤回信息
        try:
            root = ET.fromstring(self.content)
            if root.tag == "sysmsg" and root.get("type") == "revokemsg":
                revoke_node = root.find("revokemsg")
                if revoke_node is not None:
                    # 获取被撤回的消息ID
                    msg_id_node = revoke_node.find("newmsgid")
                    if msg_id_node is not None and msg_id_node.text:
                        self.revoke_msg_id = msg_id_node.text

                    # 获取替换消息
                    replace_node = revoke_node.find("replacemsg")
                    if replace_node is not None and replace_node.text:
                        self.replace_msg = replace_node.text
                        self.notify_msg = replace_node.text
        except Exception:
            pass


@dataclass
class PatMessage(SystemBaseMessage):
    """拍一拍消息"""
    from_username: str = ""  # 发送拍一拍的用户wxid
    chat_username: str = ""  # 聊天对象wxid
    patted_username: str = ""  # 被拍的用户wxid
    pat_suffix: str = ""  # 拍一拍后缀
    pat_suffix_version: str = ""  # 拍一拍后缀版本
    template: str = ""  # 拍一拍模板消息
    
    # 设置消息类型类变量
    message_type = MessageType.PAT
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理拍一拍消息特有数据"""
        try:
            root = ET.fromstring(self.content)
            if root.tag == "sysmsg" and root.get("type") == "pat":
                pat_node = root.find("pat")
                if pat_node is not None:
                    # 获取拍一拍相关信息
                    from_username_node = pat_node.find("fromusername")
                    self.from_username = (
                        from_username_node.text
                        if from_username_node is not None
                        and from_username_node.text
                        else ""
                    )

                    chat_username_node = pat_node.find("chatusername")
                    self.chat_username = (
                        chat_username_node.text
                        if chat_username_node is not None
                        and chat_username_node.text
                        else ""
                    )

                    patted_username_node = pat_node.find("pattedusername")
                    self.patted_username = (
                        patted_username_node.text
                        if patted_username_node is not None
                        and patted_username_node.text
                        else ""
                    )

                    pat_suffix_node = pat_node.find("patsuffix")
                    self.pat_suffix = (
                        pat_suffix_node.text
                        if pat_suffix_node is not None and pat_suffix_node.text
                        else ""
                    )

                    pat_suffix_version_node = pat_node.find("patsuffixversion")
                    self.pat_suffix_version = (
                        pat_suffix_version_node.text
                        if pat_suffix_version_node is not None
                        and pat_suffix_version_node.text
                        else ""
                    )

                    template_node = pat_node.find("template")
                    if template_node is not None and template_node.text:
                        self.template = template_node.text
        except Exception:
            pass


@dataclass
class SyncMessage(SystemBaseMessage):
    """同步消息"""
    
    # 设置消息类型类变量
    message_type = MessageType.SYNC
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理同步消息特有数据"""
        # 同步消息没有特殊数据需要处理
        pass


@dataclass
class OfflineMessage(SystemBaseMessage):
    """掉线通知消息"""
    
    # 设置消息类型类变量
    message_type = MessageType.OFFLINE
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理掉线通知消息特有数据"""
        # 掉线通知消息没有特殊数据需要处理
        pass
