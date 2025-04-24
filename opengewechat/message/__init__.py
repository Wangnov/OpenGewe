"""消息模块

此模块提供了处理微信各种消息的工具和模型类。
"""

# 导入消息类型
from opengewechat.message.types import MessageType

# 导入消息模型
from opengewechat.message.models import *  # noqa: F403

# 导入消息工厂
from opengewechat.message.factory import MessageFactory
from opengewechat.message.handlers import BaseHandler

__all__ = [
    "MessageType",
    "MessageFactory",
    "BaseHandler",
]
