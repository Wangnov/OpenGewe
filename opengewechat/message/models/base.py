import time
from dataclasses import dataclass, field
from typing import Dict, Any
from opengewechat.message.types import MessageType


@dataclass
class BaseMessage:
    """基础消息类"""

    type: MessageType  # 消息类型
    app_id: str  # 设备ID
    wxid: str = ""  # 所属微信ID
    typename: str = ""  # 原始消息类型名
    msg_id: str = ""  # 消息ID
    new_msg_id: str = ""  # 新消息ID
    create_time: int = 0  # 消息创建时间
    from_user: str = ""  # 发送者ID
    to_user: str = ""  # 接收者ID
    content: str = ""  # 消息内容
    raw_data: Dict[str, Any] = field(default_factory=dict)  # 原始数据

    @property
    def is_group_message(self) -> bool:
        """判断是否为群聊消息"""
        if "@chatroom" in self.from_user or "@chatroom" in self.to_user:
            return True
        return False

    @property
    def is_self_message(self) -> bool:
        """判断是否为自己发送的消息"""
        if self.from_user == self.wxid:
            return True
        return False

    @property
    def timestamp(self) -> str:
        """获取可读时间戳"""
        timearray = time.localtime(self.create_time)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearray)
