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
    room_wxid: str = ""  # 群聊ID
    actural_user_wxid: str = ""  # 实际发送者微信ID
    raw_data: Dict[str, Any] = field(default_factory=dict)  # 原始数据

    @property
    def is_group_message(self) -> bool:
        """判断是否为群聊消息"""
        # 如果已经提取了room_wxid，则直接判断
        if self.room_wxid:
            return True
        # 否则检查from_user和to_user是否包含@chatroom
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
    def datetime(self) -> str:
        """获取可读时间戳"""
        timearray = time.localtime(self.create_time)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearray)

    def _process_group_message(self) -> None:
        """处理群消息发送者信息

        在群聊中：
        1. 保存群ID到room_wxid字段
        2. 识别真实发送者ID并更新from_user
        3. 去除content中的发送者前缀
        """
        # 如果不是群消息，直接返回
        if not self.is_group_message:
            return

        # 保存原始群ID到room_wxid
        if "@chatroom" in self.from_user:
            self.room_wxid = self.from_user
        elif "@chatroom" in self.to_user:
            self.room_wxid = self.to_user

        # 处理content中的发送者信息
        if ":" in self.content:
            # 尝试分离发送者ID和实际内容
            parts = self.content.split(":", 1)
            if len(parts) == 2:
                sender_id = parts[0].strip()
                real_content = parts[1].strip()

                # 确保sender_id是一个有效的wxid格式（简单验证）
                if sender_id and (
                    sender_id.startswith("wxid_")
                    or sender_id.endswith("@chatroom")
                    or "@" in sender_id
                ):
                    # 更新发送者和内容
                    self.actural_user_wxid = sender_id
                    self.content = real_content
        else:
            self.actural_user_wxid = self.from_user
