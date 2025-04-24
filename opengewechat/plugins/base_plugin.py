"""插件基类

此模块定义了插件的基本接口，所有自定义插件必须继承此类。
"""

from typing import Optional
from opengewechat.client import GewechatClient
from opengewechat.message.models import BaseMessage


class BasePlugin:
    """插件基类

    所有自定义插件必须继承此类，并实现其方法。

    Attributes:
        name: 插件名称
        description: 插件描述
        version: 插件版本
        enabled: 插件是否启用
        client: GewechatClient实例，用于发送消息等操作
    """

    def __init__(self, client: Optional[GewechatClient] = None):
        """初始化插件

        Args:
            client: GewechatClient实例，用于发送消息等操作
        """
        self.name = self.__class__.__name__
        self.description = "插件基类"
        self.version = "0.1.0"
        self.enabled = False
        self.client = client

    def can_handle(self, message: BaseMessage) -> bool:
        """判断是否可以处理该消息

        Args:
            message: 消息对象

        Returns:
            是否可以处理该消息
        """
        return False

    def handle(self, message: BaseMessage) -> None:
        """处理消息

        Args:
            message: 消息对象
        """
        pass

    def on_enable(self) -> None:
        """插件启用时调用"""
        self.enabled = True

    def on_disable(self) -> None:
        """插件禁用时调用"""
        self.enabled = False

    def on_unload(self) -> None:
        """插件卸载时调用"""
        pass

    def on_load(self) -> None:
        """插件加载时调用"""
        pass

    def __str__(self) -> str:
        return f"{self.name} v{self.version} ({'启用' if self.enabled else '禁用'})"
