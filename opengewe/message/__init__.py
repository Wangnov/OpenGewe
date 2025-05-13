"""消息处理包

提供异步消息处理功能，包括消息工厂、处理器和模型定义。
"""

from opengewe.message.models import BaseMessage
from opengewe.message.factory import MessageFactory
from opengewe.message.types import MessageType

__all__ = ["BaseMessage", "MessageFactory", "MessageType"]
