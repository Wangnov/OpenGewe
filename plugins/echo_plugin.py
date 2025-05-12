"""回音插件

此插件会重复用户发送的文本消息。
"""

from opengewechat import BasePlugin
from opengewechat.message.models import BaseMessage, TextMessage
from opengewechat.message.types import MessageType


class EchoPlugin(BasePlugin):
    """回音插件

    当收到文本消息时，回复相同的内容。
    """

    def __init__(self, client=None):
        """初始化回音插件

        Args:
            client: GewechatClient实例，用于发送消息
        """
        super().__init__(client)
        self.name = "EchoPlugin"
        self.description = "回音插件，当收到文本消息时，回复相同的内容"
        self.version = "0.1.0"

    def can_handle(self, message: BaseMessage) -> bool:
        """判断是否可以处理该消息

        任何文本消息都可以处理。

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

        # 任何文本消息都可以处理
        return True

    def handle(self, message: BaseMessage) -> None:
        """处理消息

        回复相同的内容。

        Args:
            message: 消息对象
        """
        if not self.client:
            return

        # 确保是文本消息
        if not isinstance(message, TextMessage):
            return

        # 获取消息内容
        content = message.content

        # 发送回复
        self.client.message.send_text(message.to_wxid, f"你说了: {content}")
