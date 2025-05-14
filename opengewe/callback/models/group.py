from dataclasses import dataclass, field
from typing import Dict, Any, List
import xml.etree.ElementTree as ET
import re

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import BaseMessage


@dataclass
class GroupInviteMessage(BaseMessage):
    """群聊邀请确认通知消息"""

    group_name: str = ""  # 群聊名称
    inviter_nickname: str = ""  # 邀请人昵称
    invite_url: str = ""  # 邀请链接

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupInviteMessage":
        """从字典创建群聊邀请确认通知消息对象"""
        msg = cls(
            type=MessageType.GROUP_INVITE,
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

                # 解析XML获取群邀请确认信息
                try:
                    root = ET.fromstring(msg.content)
                    # 检查是否为appmsg消息
                    if root.tag == "msg":
                        appmsg_node = root.find("appmsg")
                        if appmsg_node is not None:
                            # 获取标题（邀请你加入群聊）
                            title_node = appmsg_node.find("title")
                            if title_node is not None and title_node.text:
                                if "邀请你加入群聊" in title_node.text:
                                    # 获取描述信息
                                    des_node = appmsg_node.find("des")
                                    if des_node is not None and des_node.text:
                                        # 解析描述中的邀请人和群名
                                        des_text = des_node.text
                                        try:
                                            # 格式通常为 "XXX"邀请你加入群聊"YYY"，进入可查看详情。
                                            parts = des_text.split('"')
                                            if len(parts) >= 4:
                                                msg.inviter_nickname = parts[1]
                                                msg.group_name = parts[3]
                                        except Exception:
                                            pass

                                    # 获取邀请链接
                                    url_node = appmsg_node.find("url")
                                    if url_node is not None and url_node.text:
                                        msg.invite_url = url_node.text
                except Exception:
                    pass

        return msg


@dataclass
class GroupInvitedMessage(BaseMessage):
    """群聊邀请消息"""

    group_name: str = ""  # 群聊名称
    group_id: str = ""  # 群聊ID
    inviter_wxid: str = ""  # 邀请人微信ID
    inviter_nickname: str = ""  # 邀请人昵称
    invited_wxids: List[str] = field(default_factory=list)  # 被邀请人微信ID列表
    other_members: List[str] = field(default_factory=list)  # 群聊中的其他成员昵称
    other_members_wxids: List[str] = field(
        default_factory=list
    )  # 群聊中的其他成员微信ID

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupInvitedMessage":
        """从字典创建群聊邀请消息对象"""
        msg = cls(
            type=MessageType.GROUP_INVITED,
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
                # 群ID通常就是群消息的from_wxid
                if "@chatroom" in msg.from_wxid:
                    msg.group_id = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取群邀请信息
                try:
                    root = ET.fromstring(msg.content)
                    # 检查是否为系统消息
                    if root.tag == "sysmsg":
                        sysmsg_type = root.get("type", "")

                        # 处理sysmsgtemplate类型的群邀请消息
                        if sysmsg_type == "sysmsgtemplate":
                            template_node = root.find(".//template")
                            if (
                                template_node is not None
                                and template_node.text
                                and "邀请你加入了群聊" in template_node.text
                            ):
                                # 获取邀请人信息
                                username_link = root.find(".//link[@name='username']")
                                if username_link is not None:
                                    member_node = username_link.find(
                                        ".//memberlist/member"
                                    )
                                    if member_node is not None:
                                        # 获取邀请人wxid
                                        username_node = member_node.find("username")
                                        if (
                                            username_node is not None
                                            and username_node.text
                                        ):
                                            msg.inviter_wxid = username_node.text.strip(
                                                "![CDATA[]]"
                                            )

                                        # 获取邀请人昵称
                                        nickname_node = member_node.find("nickname")
                                        if (
                                            nickname_node is not None
                                            and nickname_node.text
                                        ):
                                            msg.inviter_nickname = (
                                                nickname_node.text.strip("![CDATA[]]")
                                            )

                                # 获取其他群成员信息
                                others_link = root.find(".//link[@name='others']")
                                if others_link is not None:
                                    members = others_link.findall(".//member")
                                    for member in members:
                                        # 获取成员昵称
                                        nickname_node = member.find("nickname")
                                        if (
                                            nickname_node is not None
                                            and nickname_node.text
                                        ):
                                            # 清理CDATA标记并添加成员昵称
                                            msg.other_members.append(
                                                nickname_node.text.strip("![CDATA[]]")
                                            )

                                        # 获取成员wxid
                                        username_node = member.find("username")
                                        if (
                                            username_node is not None
                                            and username_node.text
                                        ):
                                            # 清理CDATA标记并添加成员wxid
                                            msg.other_members_wxids.append(
                                                username_node.text.strip("![CDATA[]]")
                                            )
                except Exception:
                    pass

        return msg


@dataclass
class GroupRemovedMessage(BaseMessage):
    """被移除群聊通知消息"""

    group_id: str = ""  # 群聊ID
    operator_nickname: str = ""  # 操作者昵称

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupRemovedMessage":
        """从字典创建被移除群聊通知消息对象"""
        msg = cls(
            type=MessageType.GROUP_REMOVED,
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
                # 群ID通常就是群消息的from_wxid
                if "@chatroom" in msg.from_wxid:
                    msg.group_id = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理简单格式的"你被XXX移出群聊"消息
                if msg.content.startswith("你被") and msg.content.endswith("移出群聊"):
                    # 提取操作者昵称
                    try:
                        nickname = msg.content[
                            2:-4
                        ]  # 去掉前面的"你被"和后面的"移出群聊"
                        if nickname.startswith('"') and nickname.endswith('"'):
                            nickname = nickname[1:-1]  # 去掉引号
                        msg.operator_nickname = nickname
                    except Exception:
                        pass
                    return msg

        return msg


@dataclass
class GroupKickMessage(BaseMessage):
    """踢出群聊通知消息"""

    group_id: str = ""  # 群聊ID
    group_name: str = ""  # 群聊名称
    operator_wxid: str = ""  # 操作者微信ID
    operator_nickname: str = ""  # 操作者昵称
    kicked_wxids: List[str] = field(default_factory=list)  # 被踢出成员的微信ID列表
    kicked_nicknames: List[str] = field(default_factory=list)  # 被踢出成员的昵称列表

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupKickMessage":
        """从字典创建踢出群聊通知消息对象"""
        msg = cls(
            type=MessageType.GROUP_KICK,
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
                # 群ID通常就是群消息的from_wxid
                if "@chatroom" in msg.from_wxid:
                    msg.group_id = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 解析XML获取踢人信息
                try:
                    # 处理xml前缀
                    if ":" in msg.content and "<" in msg.content:
                        parts = msg.content.split(":", 1)
                        if len(parts) == 2 and "<" in parts[1]:
                            msg.content = parts[1]

                    root = ET.fromstring(msg.content)
                    # 检查是否为系统消息
                    if root.tag == "sysmsg":
                        # 尝试获取操作者信息
                        operator_node = root.find(".//link")
                        if operator_node is not None:
                            msg.operator_nickname = operator_node.get("name", "")
                            msg.operator_wxid = operator_node.get("username", "")

                        # 获取被踢人信息
                        deluser_nodes = root.findall(".//deluser")
                        for deluser in deluser_nodes:
                            wxid = deluser.get("username", "")
                            if wxid:
                                msg.kicked_wxids.append(wxid)

                            nickname = deluser.get("nickname", "")
                            if nickname:
                                msg.kicked_nicknames.append(nickname)

                        # 尝试获取群名称
                        group_name_node = root.find(".//brandname")
                        if group_name_node is not None and group_name_node.text:
                            msg.group_name = group_name_node.text
                except Exception:
                    pass

        return msg


@dataclass
class GroupDismissMessage(BaseMessage):
    """解散群聊通知消息"""

    group_id: str = ""  # 群聊ID
    group_name: str = ""  # 群聊名称
    operator_wxid: str = ""  # 操作者微信ID
    operator_nickname: str = ""  # 操作者昵称

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupDismissMessage":
        """从字典创建解散群聊通知消息对象"""
        msg = cls(
            type=MessageType.GROUP_DISMISS,
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
                # 群ID通常就是群消息的from_wxid
                if "@chatroom" in msg.from_wxid:
                    msg.group_id = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 解析解散群聊信息
                try:
                    # 处理xml前缀
                    if ":" in msg.content and "<" in msg.content:
                        parts = msg.content.split(":", 1)
                        if len(parts) == 2 and "<" in parts[1]:
                            xml_content = parts[1]

                    root = ET.fromstring(xml_content)
                    # 检查是否为系统消息
                    if root.tag == "sysmsg":
                        sysmsg_type = root.get("type", "")

                        # 处理sysmsgtemplate类型的解散群聊通知
                        if sysmsg_type == "sysmsgtemplate":
                            template_node = root.find(".//template")
                            if (
                                template_node is not None
                                and template_node.text
                                and "已解散该群聊" in template_node.text
                            ):
                                # 查找操作者信息
                                link_node = root.find(".//link[@name='identity']")
                                if link_node is not None:
                                    member_node = link_node.find(".//member")
                                    if member_node is not None:
                                        # 获取操作者wxid
                                        username_node = member_node.find("username")
                                        if (
                                            username_node is not None
                                            and username_node.text
                                        ):
                                            msg.operator_wxid = username_node.text

                                        # 获取操作者昵称
                                        nickname_node = member_node.find("nickname")
                                        if (
                                            nickname_node is not None
                                            and nickname_node.text
                                        ):
                                            msg.operator_nickname = nickname_node.text

                        # 处理原有方式的解散群聊通知
                        else:
                            # 尝试获取操作者信息
                            if "解散了该群聊" in msg.content:
                                operator_node = root.find(".//link")
                                if operator_node is not None:
                                    msg.operator_nickname = operator_node.get(
                                        "name", ""
                                    )
                                    msg.operator_wxid = operator_node.get(
                                        "username", ""
                                    )

                            # 尝试获取群名称
                            group_name_node = root.find(".//brandname")
                            if group_name_node is not None and group_name_node.text:
                                msg.group_name = group_name_node.text
                except Exception:
                    pass

        return msg


@dataclass
class GroupRenameMessage(BaseMessage):
    """修改群名称消息"""

    group_id: str = ""  # 群聊ID
    old_name: str = ""  # 旧群名称
    new_name: str = ""  # 新群名称
    operator_wxid: str = ""  # 操作者微信ID
    operator_nickname: str = ""  # 操作者昵称

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupRenameMessage":
        """从字典创建修改群名称消息对象"""
        msg = cls(
            type=MessageType.GROUP_RENAME,
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
                # 群ID通常就是群消息的from_wxid
                if "@chatroom" in msg.from_wxid:
                    msg.group_id = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                if msg.content.startswith("你修改群名为"):
                    # 从消息内容中提取新群名
                    match = re.search(r'你修改群名为"(.+?)"', msg.content)
                    if match:
                        msg.new_name = match.group(1)
                        # 由于是"你"修改的群名，所以操作者就是当前用户
                        msg.operator_wxid = msg.wxid
                        msg.operator_nickname = (
                            "你"  # 这里可以后续从用户信息中获取真实昵称
                        )
                    # 解析修改群名称信息
                    try:
                        # 处理xml前缀
                        if ":" in msg.content and "<" in msg.content:
                            parts = msg.content.split(":", 1)
                            if len(parts) == 2 and "<" in parts[1]:
                                xml_content = parts[1]

                        root = ET.fromstring(xml_content)
                        # 检查是否为系统消息
                        if root.tag == "sysmsg":
                            sysmsg_type = root.get("type", "")

                            # 处理sysmsgtemplate类型的群名称修改通知
                            if sysmsg_type == "sysmsgtemplate":
                                template_node = root.find(".//template")
                                if (
                                    template_node is not None
                                    and template_node.text
                                    and "修改群名为" in template_node.text
                                ):
                                    # 查找操作者信息
                                    user_link_node = root.find(
                                        ".//link[@name='username']"
                                    )
                                    if user_link_node is not None:
                                        member_node = user_link_node.find(".//member")
                                        if member_node is not None:
                                            # 获取操作者wxid
                                            username_node = member_node.find("username")
                                            if (
                                                username_node is not None
                                                and username_node.text
                                            ):
                                                msg.operator_wxid = username_node.text

                                            # 获取操作者昵称
                                            nickname_node = member_node.find("nickname")
                                            if (
                                                nickname_node is not None
                                                and nickname_node.text
                                            ):
                                                msg.operator_nickname = (
                                                    nickname_node.text
                                                )

                                    # 获取新群名称
                                    remark_link_node = root.find(
                                        ".//link[@name='remark']"
                                    )
                                    if remark_link_node is not None:
                                        member_node = remark_link_node.find(".//member")
                                        if member_node is not None:
                                            nickname_node = member_node.find("nickname")
                                            if (
                                                nickname_node is not None
                                                and nickname_node.text
                                            ):
                                                msg.new_name = nickname_node.text

                            # 处理传统的rename类型消息
                            else:
                                # 尝试获取群名称变更信息
                                rename_node = root.find("rename")
                                if rename_node is not None:
                                    # 获取操作者信息
                                    operator_node = rename_node.find("operator")
                                    if operator_node is not None:
                                        msg.operator_wxid = operator_node.get(
                                            "wxid", ""
                                        )
                                        msg.operator_nickname = operator_node.get(
                                            "nickname", ""
                                        )

                                    # 获取新旧群名称
                                    from_name_node = rename_node.find("from")
                                    if (
                                        from_name_node is not None
                                        and from_name_node.text
                                    ):
                                        msg.old_name = from_name_node.text

                                    to_name_node = rename_node.find("to")
                                    if to_name_node is not None and to_name_node.text:
                                        msg.new_name = to_name_node.text
                    except Exception:
                        pass

        return msg


@dataclass
class GroupOwnerChangeMessage(BaseMessage):
    """更换群主通知消息"""

    group_id: str = ""  # 群聊ID
    group_name: str = ""  # 群聊名称
    old_owner_wxid: str = ""  # 原群主微信ID
    old_owner_nickname: str = ""  # 原群主昵称
    new_owner_wxid: str = ""  # 新群主微信ID
    new_owner_nickname: str = ""  # 新群主昵称

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupOwnerChangeMessage":
        """从字典创建更换群主通知消息对象"""
        msg = cls(
            type=MessageType.GROUP_OWNER_CHANGE,
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
                # 群ID通常就是群消息的from_wxid
                if "@chatroom" in msg.from_wxid:
                    msg.group_id = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]
                # 解析更换群主信息
                # 你成为了新群主
                if msg.content == "你已成为新群主":
                    # 10000消息是你成为了新群主
                    msg.group_id = msg.from_wxid
                    msg.new_owner_wxid = msg.to_wxid
                    return msg
                else:
                    # 处理xml前缀
                    if ":" in msg.content and "<" in msg.content:
                        parts = msg.content.split(":", 1)
                        if len(parts) == 2 and "<" in parts[1]:
                            msg.content = parts[1]

                    root = ET.fromstring(msg.content)
                    # 检查是否为系统消息
                    if root.tag == "sysmsg":
                        sysmsg_type = root.get("type", "")

                        # 处理sysmsgtemplate类型的更换群主通知
                        if sysmsg_type == "sysmsgtemplate":
                            template_node = root.find(".//template")
                            if (
                                template_node is not None
                                and template_node.text
                                and "已成为新群主" in template_node.text
                            ):
                                # 查找新群主信息
                                link_node = root.find(".//link[@name='ownername']")
                                if link_node is not None:
                                    member_node = link_node.find(".//member")
                                    if member_node is not None:
                                        # 获取新群主wxid
                                        username_node = member_node.find("username")
                                        if (
                                            username_node is not None
                                            and username_node.text
                                        ):
                                            msg.new_owner_wxid = username_node.text

                                        # 获取新群主昵称
                                        nickname_node = member_node.find("nickname")
                                        if (
                                            nickname_node is not None
                                            and nickname_node.text
                                        ):
                                            msg.new_owner_nickname = nickname_node.text

                        # 处理chtransfer类型的更换群主通知(原有逻辑)
                        elif sysmsg_type == "chtransfer":
                            transfer_node = root.find("chtransfer")
                            if transfer_node is not None:
                                # 获取新群主信息
                                to_node = transfer_node.find("to")
                                if to_node is not None:
                                    msg.new_owner_wxid = to_node.get("id", "")
                                    msg.new_owner_nickname = to_node.get("name", "")

                                # 获取原群主信息
                                from_node = transfer_node.find("from")
                                if from_node is not None:
                                    msg.old_owner_wxid = from_node.get("id", "")
                                    msg.old_owner_nickname = from_node.get("name", "")

        return msg


@dataclass
class GroupInfoUpdateMessage(BaseMessage):
    """群信息变更通知消息"""

    group_id: str = ""  # 群聊ID
    group_name: str = ""  # 群聊名称
    member_count: int = 0  # 成员数量
    admin_wxids: List[str] = field(default_factory=list)  # 管理员微信ID列表
    owner_wxid: str = ""  # 群主微信ID
    group_notice: str = ""  # 群公告
    update_type: str = ""  # 更新类型(member, admin, owner, notice)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupInfoUpdateMessage":
        """从字典创建群信息变更通知消息对象"""
        msg = cls(
            type=MessageType.GROUP_INFO_UPDATE,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]

            # ModContacts消息的结构不同，从Data中直接获取群信息
            if isinstance(msg_data, dict):
                # 获取群ID
                if "UserName" in msg_data and "string" in msg_data["UserName"]:
                    msg.group_id = msg_data["UserName"]["string"]

                # 获取群名称
                if "NickName" in msg_data and "string" in msg_data["NickName"]:
                    msg.group_name = msg_data["NickName"]["string"]

                # 获取群公告
                if "Announcement" in msg_data and "string" in msg_data["Announcement"]:
                    msg.group_notice = msg_data["Announcement"]["string"]
                    msg.update_type = "notice"

                # 获取成员数量
                if "MemberCount" in msg_data:
                    try:
                        msg.member_count = int(msg_data["MemberCount"])
                        if not msg.update_type:
                            msg.update_type = "member"
                    except (ValueError, TypeError):
                        pass

                # 获取群主
                if (
                    "ChatRoomOwner" in msg_data
                    and "string" in msg_data["ChatRoomOwner"]
                ):
                    msg.owner_wxid = msg_data["ChatRoomOwner"]["string"]
                    if not msg.update_type:
                        msg.update_type = "owner"

                # 获取管理员列表
                if "ChatRoomAdminList" in msg_data:
                    admin_list = msg_data["ChatRoomAdminList"]
                    if isinstance(admin_list, list):
                        for admin in admin_list:
                            if isinstance(admin, dict) and "string" in admin:
                                msg.admin_wxids.append(admin["string"])
                                if not msg.update_type:
                                    msg.update_type = "admin"

        return msg


@dataclass
class GroupAnnouncementMessage(BaseMessage):
    """发布群公告消息"""

    group_id: str = ""  # 群聊ID
    group_name: str = ""  # 群聊名称
    announcement: str = ""  # 公告内容
    operator_wxid: str = ""  # 操作者微信ID
    operator_nickname: str = ""  # 操作者昵称

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupAnnouncementMessage":
        """从字典创建发布群公告消息对象"""
        msg = cls(
            type=MessageType.GROUP_ANNOUNCEMENT,
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
                # 群ID通常就是群消息的from_wxid
                if "@chatroom" in msg.from_wxid:
                    msg.group_id = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 解析群公告信息
                try:
                    # 处理xml前缀
                    if ":" in msg.content and "<" in msg.content:
                        parts = msg.content.split(":", 1)
                        if len(parts) == 2 and "<" in parts[1]:
                            msg.content = parts[1]

                    root = ET.fromstring(msg.content)
                    # 检查是否为系统消息
                    if root.tag == "sysmsg":
                        # 尝试获取公告信息
                        ann_node = root.find("announcement")
                        if ann_node is not None:
                            # 获取公告内容
                            content_node = ann_node.find("content")
                            if content_node is not None and content_node.text:
                                msg.announcement = content_node.text

                            # 获取发布者信息
                            operator_node = ann_node.find("username")
                            if operator_node is not None and operator_node.text:
                                msg.operator_wxid = operator_node.text

                            nickname_node = ann_node.find("nickname")
                            if nickname_node is not None and nickname_node.text:
                                msg.operator_nickname = nickname_node.text
                except Exception:
                    pass

        return msg


@dataclass
class GroupTodoMessage(BaseMessage):
    """群待办消息"""

    group_id: str = ""  # 群聊ID
    todo_id: str = ""  # 待办ID
    title: str = ""  # 待办标题
    content: str = ""  # 待办内容
    creator_wxid: str = ""  # 创建者微信ID
    creator_nickname: str = ""  # 创建者昵称
    finish_time: int = 0  # 截止时间戳
    todo_action: str = ""  # 待办动作(add/update/finish/delete)
    op: int = 0  # 操作类型
    manager_wxid: str = ""  # 管理者微信ID
    related_msgid: str = ""  # 关联消息ID
    oper_wxid: str = ""  # 操作者微信ID
    scene: str = ""  # 场景
    username: str = ""  # 特定用户名
    template: str = ""  # 消息模板

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupTodoMessage":
        """从字典创建群待办消息对象"""
        msg = cls(
            type=MessageType.GROUP_TODO,
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
                # 群ID通常就是群消息的from_wxid
                if "@chatroom" in msg.from_wxid:
                    msg.group_id = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 解析群待办信息
                try:
                    # 处理xml前缀
                    if ":" in msg.content and "<" in msg.content:
                        parts = msg.content.split(":", 1)
                        if len(parts) == 2 and "<" in parts[1]:
                            msg.content = parts[1]

                    root = ET.fromstring(msg.content)
                    # 检查消息类型
                    if root.tag == "sysmsg":
                        sysmsg_type = root.get("type", "")

                        # 处理roomtoolstips类型的待办消息
                        if sysmsg_type == "roomtoolstips":
                            todo_node = root.find("todo")
                            if todo_node is not None:
                                # 获取操作类型
                                op_node = todo_node.find("op")
                                if op_node is not None and op_node.text:
                                    try:
                                        msg.op = int(op_node.text)
                                    except ValueError:
                                        pass

                                # 获取待办ID
                                todoid_node = todo_node.find("todoid")
                                if todoid_node is not None and todoid_node.text:
                                    msg.todo_id = todoid_node.text.strip("![CDATA[]]")

                                # 获取用户名
                                username_node = todo_node.find("username")
                                if username_node is not None and username_node.text:
                                    msg.username = username_node.text.strip(
                                        "![CDATA[]]"
                                    )

                                # 获取时间
                                time_node = todo_node.find("time")
                                if time_node is not None and time_node.text:
                                    try:
                                        msg.finish_time = int(time_node.text)
                                    except ValueError:
                                        pass

                                # 获取标题
                                title_node = todo_node.find("title")
                                if title_node is not None and title_node.text:
                                    msg.title = title_node.text.strip("![CDATA[]]")

                                # 获取创建者
                                creator_node = todo_node.find("creator")
                                if creator_node is not None and creator_node.text:
                                    msg.creator_wxid = creator_node.text.strip(
                                        "![CDATA[]]"
                                    )

                                # 获取关联消息ID
                                related_msgid_node = todo_node.find("related_msgid")
                                if (
                                    related_msgid_node is not None
                                    and related_msgid_node.text
                                ):
                                    msg.related_msgid = related_msgid_node.text.strip(
                                        "![CDATA[]]"
                                    )

                                # 获取管理者
                                manager_node = todo_node.find("manager")
                                if manager_node is not None and manager_node.text:
                                    msg.manager_wxid = manager_node.text.strip(
                                        "![CDATA[]]"
                                    )

                                # 获取场景
                                scene_node = todo_node.find("scene")
                                if scene_node is not None and scene_node.text:
                                    msg.scene = scene_node.text.strip("![CDATA[]]")

                                # 获取操作者
                                oper_node = todo_node.find("oper")
                                if oper_node is not None and oper_node.text:
                                    msg.oper_wxid = oper_node.text.strip("![CDATA[]]")

                                # 获取模板
                                template_node = todo_node.find("template")
                                if template_node is not None and template_node.text:
                                    msg.template = template_node.text.strip(
                                        "![CDATA[]]"
                                    )

                                # 根据场景设置待办动作
                                if msg.scene == "altertodo_set":
                                    msg.todo_action = "add"

                        # 处理传统的todo类型消息
                        elif sysmsg_type == "todo":
                            todo_node = root.find("todo")
                            if todo_node is not None:
                                # 获取待办ID
                                todo_id_node = todo_node.find("id")
                                if todo_id_node is not None and todo_id_node.text:
                                    msg.todo_id = todo_id_node.text

                                # 获取待办标题
                                title_node = todo_node.find("title")
                                if title_node is not None and title_node.text:
                                    msg.title = title_node.text

                                # 获取待办内容
                                content_node = todo_node.find("content")
                                if content_node is not None and content_node.text:
                                    msg.content = content_node.text

                                # 获取创建者信息
                                from_node = todo_node.find("from")
                                if from_node is not None:
                                    from_wxid = from_node.get("id", "")
                                    from_name = from_node.get("name", "")
                                    if from_wxid:
                                        msg.creator_wxid = from_wxid
                                    if from_name:
                                        msg.creator_nickname = from_name

                                # 获取截止时间
                                finish_time_node = todo_node.find("finishtime")
                                if (
                                    finish_time_node is not None
                                    and finish_time_node.text
                                ):
                                    try:
                                        msg.finish_time = int(finish_time_node.text)
                                    except ValueError:
                                        pass

                                # 获取待办动作
                                action_node = todo_node.find("action")
                                if action_node is not None and action_node.text:
                                    msg.todo_action = action_node.text
                except Exception:
                    pass

        return msg


@dataclass
class GroupQuitMessage(BaseMessage):
    """退出群聊消息"""

    group_id: str = ""  # 群聊ID
    user_wxid: str = ""  # 退出用户的微信ID

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GroupQuitMessage":
        """从字典创建退出群聊消息对象"""
        msg = cls(
            type=MessageType.GROUP_QUIT,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            # DelContacts消息结构简单，只需要获取删除的UserName
            msg.group_id = data["Data"]

            # 当前用户退出了群聊
            if "@chatroom" in msg.group_id:
                # 退出用户是自己
                msg.user_wxid = data.get("Wxid", "")

        return msg
