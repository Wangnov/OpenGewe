from dataclasses import dataclass, field
from typing import Dict, Any
import xml.etree.ElementTree as ET
import re

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import BaseMessage


@dataclass
class CardMessage(BaseMessage):
    """名片消息"""

    nickname: str = ""  # 昵称
    alias: str = ""  # 微信号
    username: str = ""  # 用户名
    avatar_url: str = ""  # 头像URL
    province: str = ""  # 省份
    city: str = ""  # 城市
    sign: str = ""  # 个性签名
    sex: int = 0  # 性别，0未知，1男，2女

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CardMessage":
        """从字典创建名片消息对象"""
        msg = cls(
            type=MessageType.CARD,
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

                # 解析XML获取名片信息
                try:
                    root = ET.fromstring(msg.content)
                    msg_node = root.find("msg")
                    if msg_node is not None:
                        # 从msg节点获取基本信息
                        msg.username = msg_node.get("username", "")
                        msg.nickname = msg_node.get("nickname", "")
                        msg.alias = msg_node.get("alias", "")
                        msg.province = msg_node.get("province", "")
                        msg.city = msg_node.get("city", "")
                        msg.sign = msg_node.get("sign", "")
                        try:
                            msg.sex = int(msg_node.get("sex", "0"))
                        except ValueError:
                            pass

                        # 获取头像URL
                        img_node = msg_node.find("img")
                        if img_node is not None:
                            msg.avatar_url = img_node.get("url", "")
                except Exception:
                    pass

        return msg


@dataclass
class FriendRequestMessage(BaseMessage):
    """好友添加请求消息"""

    nickname: str = ""  # 昵称
    stranger_wxid: str = ""  # 陌生人微信ID
    scene: int = 0  # 添加场景
    ticket: str = ""  # 验证票据
    content: str = ""  # 验证消息内容
    source: str = ""  # 来源
    alias: str = ""  # 微信号
    antispam_ticket: str = ""  # 反垃圾票据
    big_head_img_url: str = ""  # 大头像URL
    small_head_img_url: str = ""  # 小头像URL

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FriendRequestMessage":
        """从字典创建好友添加请求消息对象"""
        msg = cls(
            type=MessageType.FRIEND_REQUEST,
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

                # 解析XML获取好友请求信息
                try:
                    root = ET.fromstring(msg.content)
                    # 检查消息类型 - 支持多种可能的格式
                    if root.tag == "msg":
                        # 方式1: 从属性获取
                        attrs_map = {
                            "fromusername": "stranger_wxid",
                            "fromnickname": "nickname",
                            "content": "content",
                            "scene": "scene",
                            "ticket": "ticket",
                            "encryptusername": "ticket",
                            "sourceusername": "source",
                            "sourcenickname": "source",
                            "alias": "alias",
                            "antispamticket": "antispam_ticket",
                            "bigheadimgurl": "big_head_img_url",
                            "smallheadimgurl": "small_head_img_url",
                        }

                        # 处理属性
                        for attr, field in attrs_map.items():
                            value = root.get(attr)
                            if value is not None and not getattr(msg, field):
                                if field == "scene" and value:
                                    try:
                                        setattr(msg, field, int(value))
                                    except (ValueError, TypeError):
                                        pass
                                else:
                                    setattr(msg, field, value)

                        # 方式2: 从内部XML元素获取
                        if not (msg.stranger_wxid and msg.nickname and msg.ticket):
                            tags_map = {
                                "username": "stranger_wxid",
                                "nickname": "nickname",
                                "content": "content",
                                "alias": "alias",
                                "scene": "scene",
                                "ticket": "ticket",
                                "encryptusername": "ticket",
                                "source": "source",
                                "sourceusername": "source",
                                "antispamticket": "antispam_ticket",
                                "bigheadimgurl": "big_head_img_url",
                                "smallheadimgurl": "small_head_img_url",
                            }

                            # 搜索所有元素
                            for elem in root.findall(".//*"):
                                if elem.tag in tags_map and elem.text:
                                    field = tags_map[elem.tag]
                                    if not getattr(msg, field):
                                        if field == "scene" and elem.text:
                                            try:
                                                setattr(msg, field, int(elem.text))
                                            except (ValueError, TypeError):
                                                pass
                                        else:
                                            setattr(msg, field, elem.text)

                        # 方式3: 如果还没有找到stranger_wxid，尝试从内容中提取
                        if not msg.stranger_wxid:
                            # 尝试多种可能的格式
                            patterns = [
                                r'fromusername="([^"]+)"',
                                r'username="([^"]+)"',
                                r'encryptusername="([^"]+)"',
                            ]

                            for pattern in patterns:
                                match = re.search(pattern, msg.content)
                                if match:
                                    msg.stranger_wxid = match.group(1)
                                    break

                        # 方式4: 检查用户名是否在msg.content中直接出现
                        if not msg.stranger_wxid and "wxid_" in msg.content:
                            match = re.search(r"(wxid_[a-zA-Z0-9_-]+)", msg.content)
                            if match:
                                msg.stranger_wxid = match.group(1)

                        # 方式5: 从XML内容直接提取完整的用户名
                        if not msg.nickname and "fromnickname" in msg.content:
                            match = re.search(r'fromnickname="([^"]+)"', msg.content)
                            if match:
                                msg.nickname = match.group(1)

                except Exception as e:
                    # 记录异常信息到raw_data，便于调试
                    msg.raw_data["xml_parse_error"] = str(e)

            # 检查PushContent字段，可能包含发送者昵称和请求内容
            push_content = msg_data.get("PushContent", "")
            if isinstance(push_content, str) and not msg.nickname:
                # 格式通常为 "昵称 : [名片]姓名" 或 "昵称请求添加你为朋友"
                name_match = re.match(r"^([^:]+)(?:\s*:|请求)", push_content)
                if name_match:
                    msg.nickname = name_match.group(1).strip()

        return msg


@dataclass
class ContactUpdateMessage(BaseMessage):
    """联系人更新消息"""

    contact_info: Dict[str, Any] = field(default_factory=dict)  # 联系人信息
    user_type: int = 0  # 用户类型
    username: str = ""  # 用户名
    nickname: str = ""  # 昵称
    remark: str = ""  # 备注
    alias: str = ""  # 微信号
    avatar_url: str = ""  # 头像URL
    sex: int = 0  # 性别
    signature: str = ""  # 签名
    province: str = ""  # 省份
    city: str = ""  # 城市
    country: str = ""  # 国家
    is_chatroom: bool = False  # 是否为群聊

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactUpdateMessage":
        """从字典创建联系人更新消息对象"""
        msg = cls(
            type=MessageType.CONTACT_UPDATE,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]

            # ModContacts消息的结构不同，从Data中直接获取联系人信息
            if isinstance(msg_data, dict):
                # 获取基础信息
                msg.username = msg_data.get("UserName", {}).get("string", "")

                # 判断是否为群聊
                msg.is_chatroom = "@chatroom" in msg.username

                # 设置联系人类型
                try:
                    msg.user_type = int(msg_data.get("Type", 0))
                except (ValueError, TypeError):
                    pass

                # 获取昵称
                if "NickName" in msg_data and "string" in msg_data["NickName"]:
                    msg.nickname = msg_data["NickName"]["string"]

                # 获取备注
                if "Remark" in msg_data and "string" in msg_data["Remark"]:
                    msg.remark = msg_data["Remark"]["string"]

                # 获取微信号
                if "Alias" in msg_data and "string" in msg_data["Alias"]:
                    msg.alias = msg_data["Alias"]["string"]

                # 获取签名
                if "Signature" in msg_data and "string" in msg_data["Signature"]:
                    msg.signature = msg_data["Signature"]["string"]

                # 获取省份
                if "Province" in msg_data and "string" in msg_data["Province"]:
                    msg.province = msg_data["Province"]["string"]

                # 获取城市
                if "City" in msg_data and "string" in msg_data["City"]:
                    msg.city = msg_data["City"]["string"]

                # 获取国家
                if "Country" in msg_data and "string" in msg_data["Country"]:
                    msg.country = msg_data["Country"]["string"]

                # 获取性别
                try:
                    msg.sex = int(msg_data.get("Sex", 0))
                except (ValueError, TypeError):
                    pass

                # 获取头像URL
                if "HeadImgUrl" in msg_data and "string" in msg_data["HeadImgUrl"]:
                    msg.avatar_url = msg_data["HeadImgUrl"]["string"]

                # 构建联系人信息字典
                msg.contact_info = {
                    "username": msg.username,
                    "nickname": msg.nickname,
                    "remark": msg.remark,
                    "alias": msg.alias,
                    "signature": msg.signature,
                    "province": msg.province,
                    "city": msg.city,
                    "country": msg.country,
                    "sex": msg.sex,
                    "avatar_url": msg.avatar_url,
                    "is_chatroom": msg.is_chatroom,
                    "user_type": msg.user_type,
                }

        return msg


@dataclass
class ContactDeletedMessage(BaseMessage):
    """联系人删除消息"""

    username: str = ""  # 被删除联系人的用户名
    is_chatroom: bool = False  # 是否为群聊

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContactDeletedMessage":
        """从字典创建联系人删除消息对象"""
        msg = cls(
            type=MessageType.CONTACT_DELETED,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            # 处理两种可能的数据结构
            if (
                isinstance(data["Data"], dict)
                and "UserName" in data["Data"]
                and "string" in data["Data"]["UserName"]
            ):
                # 结构为 {"UserName": {"string": "wxid_xxx"}}
                msg.username = data["Data"]["UserName"]["string"]
            else:
                # 结构为直接的字符串或其他格式
                msg.username = str(data["Data"])

            # 判断是否为群聊
            msg.is_chatroom = "@chatroom" in msg.username

        return msg
