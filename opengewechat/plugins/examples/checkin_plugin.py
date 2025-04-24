"""签到插件

此插件用于处理签到功能，当收到文本消息"签到"时，回复"签到成功"。
"""

from opengewechat.plugins.base_plugin import BasePlugin
from opengewechat.message.models import BaseMessage, TextMessage
from opengewechat.message.types import MessageType


class CheckinPlugin(BasePlugin):
    """签到插件

    当收到文本消息"签到"时，回复"签到成功"。
    """

    def __init__(self, client=None):
        """初始化签到插件

        Args:
            client: GewechatClient实例，用于发送消息
        """
        super().__init__(client)
        self.name = "CheckinPlugin"
        self.description = "签到插件，当收到文本消息'签到'时，回复'签到成功'"
        self.version = "0.1.0"

    def can_handle(self, message: BaseMessage) -> bool:
        """判断是否可以处理该消息

        当消息类型为文本，且内容为"签到"时，可以处理。

        Args:
            message: 消息对象

        Returns:
            是否可以处理该消息
        """
        # 检查是否为文本消息
        if message.type != MessageType.TEXT:
            return False

        # 转换为文本消息对象
        if not isinstance(message, TextMessage):
            return False

        # 检查消息内容是否为"签到"
        return message.content == "签到"

    def handle(self, message: BaseMessage) -> None:
        """处理消息

        回复"签到成功"。

        Args:
            message: 消息对象
        """
        if not self.client:
            return

        # 文本消息的接收者可能是群聊或个人
        to_wxid = message.room_wxid if message.is_group_message else message.from_user

        # 发送回复
        self.client.message.send_text(to_wxid, "签到成功")

        # 你也可以记录签到信息到数据库等操作
