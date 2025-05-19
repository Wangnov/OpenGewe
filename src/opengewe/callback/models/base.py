import time
from dataclasses import dataclass, field
from typing import Dict, Any
from opengewe.callback.types import MessageType


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
    from_wxid: str = ""  # 来自哪个聊天的ID
    to_wxid: str = ""  # 接收者ID
    content: str = ""  # 消息内容
    sender_wxid: str = ""  # 实际发送者微信ID
    raw_data: Dict[str, Any] = field(default_factory=dict)  # 原始数据

    @property
    def is_group_message(self) -> bool:
        """判断是否为群聊消息"""
        # 检查from_wxid和to_wxid是否包含@chatroom
        if "@chatroom" in self.from_wxid or "@chatroom" in self.to_wxid:
            return True
        return False

    @property
    def is_self_message(self) -> bool:
        """判断是否为自己发送的消息"""
        if self.from_wxid == self.wxid:
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
        2. 识别真实发送者ID并更新from_wxid
        3. 去除content中的发送者前缀
        """
        # 如果不是群消息，写好sender_wxid后直接返回
        self.sender_wxid = self.from_wxid
        if not self.is_group_message:
            return

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
                    self.sender_wxid = sender_id
                    self.content = real_content
