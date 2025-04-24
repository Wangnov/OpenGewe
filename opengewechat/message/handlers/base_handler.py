"""消息处理器基类"""

from typing import Dict, Any, Optional
from opengewechat.client import GewechatClient
from opengewechat.message.models import BaseMessage


class BaseHandler:
    """消息处理器基类"""

    def __init__(self, client: Optional[GewechatClient] = None):
        """初始化处理器

        Args:
            client: GewechatClient实例，用于获取下载链接和执行下载操作
        """
        self.client = client

    def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否可以处理该消息"""
        return False

    def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理消息"""
        return None
