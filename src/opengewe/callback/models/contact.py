from dataclasses import dataclass, field
from typing import Dict, Any, Optional, TYPE_CHECKING
import xml.etree.ElementTree as ET
import re

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import ContactBaseMessage, BaseMessage

if TYPE_CHECKING:
    from opengewe.client import GeweClient


@dataclass
class CardMessage(ContactBaseMessage):
    """名片消息"""
    alias: str = ""  # 微信号
    username: str = ""  # 用户名
    avatar_url: str = ""  # 头像URL
    province: str = ""  # 省份
    city: str = ""  # 城市
    sign: str = ""  # 个性签名
    sex: int = 0  # 性别，0未知，1男，2女
    
    # 设置消息类型类变量
    message_type = MessageType.CARD
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理名片消息特有数据"""
        # 解析XML获取名片信息
        try:
            root = ET.fromstring(self.content)
            msg_node = root.find("msg")
            if msg_node is not None:
                # 从msg节点获取基本信息
                self.username = msg_node.get("username", "")
                self.nickname = msg_node.get("nickname", "")
                self.alias = msg_node.get("alias", "")
                self.province = msg_node.get("province", "")
                self.city = msg_node.get("city", "")
                self.sign = msg_node.get("sign", "")
                try:
                    self.sex = int(msg_node.get("sex", "0"))
                except ValueError:
                    pass

                # 获取头像URL
                img_node = msg_node.find("img")
                if img_node is not None:
                    self.avatar_url = img_node.get("url", "")
        except Exception:
            pass


@dataclass
class FriendRequestMessage(ContactBaseMessage):
    """好友添加请求消息"""
    stranger_wxid: str = ""  # 陌生人微信ID
    scene: int = 0  # 添加场景
    ticket: str = ""  # 验证票据
    content: str = ""  # 验证消息内容
    source: str = ""  # 来源
    alias: str = ""  # 微信号
    antispam_ticket: str = ""  # 反垃圾票据
    big_head_img_url: str = ""  # 大头像URL
    small_head_img_url: str = ""  # 小头像URL
    
    # 设置消息类型类变量
    message_type = MessageType.FRIEND_REQUEST
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理好友请求特有数据"""
        try:
            root = ET.fromstring(self.content)
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
                    if value is not None and not getattr(self, field):
                        if field == "scene" and value:
                            try:
                                setattr(self, field, int(value))
                            except (ValueError, TypeError):
                                pass
                        else:
                            setattr(self, field, value)

                # 方式2: 从内部XML元素获取
                if not (self.stranger_wxid and self.nickname and self.ticket):
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
                            if not getattr(self, field):
                                if field == "scene" and elem.text:
                                    try:
                                        setattr(self, field, int(elem.text))
                                    except (ValueError, TypeError):
                                        pass
                                else:
                                    setattr(self, field, elem.text)

                # 方式3: 如果还没有找到stranger_wxid，尝试从内容中提取
                if not self.stranger_wxid:
                    # 尝试多种可能的格式
                    patterns = [
                        r'fromusername="([^"]+)"',
                        r'username="([^"]+)"',
                        r'encryptusername="([^"]+)"',
                    ]

                    for pattern in patterns:
                        match = re.search(pattern, self.content)
                        if match:
                            self.stranger_wxid = match.group(1)
                            break

                # 方式4: 检查用户名是否在self.content中直接出现
                if not self.stranger_wxid and "wxid_" in self.content:
                    match = re.search(r"(wxid_[a-zA-Z0-9_-]+)", self.content)
                    if match:
                        self.stranger_wxid = match.group(1)

                # 方式5: 从XML内容直接提取完整的用户名
                if not self.nickname and "fromnickname" in self.content:
                    match = re.search(r'fromnickname="([^"]+)"', self.content)
                    if match:
                        self.nickname = match.group(1)
        except Exception as e:
            # 记录异常信息到raw_data，便于调试
            self.raw_data["xml_parse_error"] = str(e)

        # 检查PushContent字段，可能包含发送者昵称和请求内容
        if "Data" in data:
            push_content = data["Data"].get("PushContent", "")
            if isinstance(push_content, str) and not self.nickname:
                # 格式通常为 "昵称 : [名片]姓名" 或 "昵称请求添加你为朋友"
                name_match = re.match(r"^([^:]+)(?:\s*:|请求)", push_content)
                if name_match:
                    self.nickname = name_match.group(1).strip()


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
    
    # 设置消息类型类变量
    message_type = MessageType.CONTACT_UPDATE
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理联系人更新特有数据"""
        if "Data" in data:
            msg_data = data["Data"]
            
            # ModContacts消息的结构不同，从Data中直接获取联系人信息
            if isinstance(msg_data, dict):
                # 获取基础信息
                self.username = msg_data.get("UserName", {}).get("string", "")

                # 判断是否为群聊
                self.is_chatroom = "@chatroom" in self.username

                # 设置联系人类型
                try:
                    self.user_type = int(msg_data.get("Type", 0))
                except (ValueError, TypeError):
                    pass

                # 获取昵称
                if "NickName" in msg_data and "string" in msg_data["NickName"]:
                    self.nickname = msg_data["NickName"]["string"]

                # 获取备注
                if "Remark" in msg_data and "string" in msg_data["Remark"]:
                    self.remark = msg_data["Remark"]["string"]

                # 获取微信号
                if "Alias" in msg_data and "string" in msg_data["Alias"]:
                    self.alias = msg_data["Alias"]["string"]

                # 获取签名
                if "Signature" in msg_data and "string" in msg_data["Signature"]:
                    self.signature = msg_data["Signature"]["string"]

                # 获取省份
                if "Province" in msg_data and "string" in msg_data["Province"]:
                    self.province = msg_data["Province"]["string"]

                # 获取城市
                if "City" in msg_data and "string" in msg_data["City"]:
                    self.city = msg_data["City"]["string"]

                # 获取国家
                if "Country" in msg_data and "string" in msg_data["Country"]:
                    self.country = msg_data["Country"]["string"]

                # 获取性别
                try:
                    self.sex = int(msg_data.get("Sex", 0))
                except (ValueError, TypeError):
                    pass

                # 获取头像URL
                if "HeadImgUrl" in msg_data and "string" in msg_data["HeadImgUrl"]:
                    self.avatar_url = msg_data["HeadImgUrl"]["string"]

                # 构建联系人信息字典
                self.contact_info = {
                    "username": self.username,
                    "nickname": self.nickname,
                    "remark": self.remark,
                    "alias": self.alias,
                    "signature": self.signature,
                    "province": self.province,
                    "city": self.city,
                    "country": self.country,
                    "sex": self.sex,
                    "avatar_url": self.avatar_url,
                    "is_chatroom": self.is_chatroom,
                    "user_type": self.user_type,
                }


@dataclass
class ContactDeletedMessage(BaseMessage):
    """联系人删除消息"""
    username: str = ""  # 被删除联系人的用户名
    is_chatroom: bool = False  # 是否为群聊
    
    # 设置消息类型类变量
    message_type = MessageType.CONTACT_DELETED
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理联系人删除特有数据"""
        if "Data" in data:
            # 处理两种可能的数据结构
            if (
                isinstance(data["Data"], dict)
                and "UserName" in data["Data"]
                and "string" in data["Data"]["UserName"]
            ):
                # 结构为 {"UserName": {"string": "wxid_xxx"}}
                self.username = data["Data"]["UserName"]["string"]
            else:
                # 结构为直接的字符串或其他格式
                self.username = str(data["Data"])

            # 判断是否为群聊
            self.is_chatroom = "@chatroom" in self.username
