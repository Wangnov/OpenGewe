"""消息处理器基类"""

from typing import Dict, Any, Optional, TYPE_CHECKING
from opengewe.callback.models import BaseMessage

# 使用TYPE_CHECKING条件导入
if TYPE_CHECKING:
    from opengewe.client import GeweClient


class BaseHandler:
    """消息处理器基类"""

    def __init__(self, client: Optional["GeweClient"] = None):
        """初始化处理器

        Args:
            client: GeweClient实例，用于获取下载链接和执行下载操作
        """
        self.client = client

    async def can_handle(self, data: Dict[str, Any]) -> bool:
        """判断是否可以处理该消息"""
        return False

    async def handle(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理消息"""
        return None

    @staticmethod
    def extract_xml_content(data: Dict[str, Any]) -> str:
        """从群聊消息中提取XML内容

        处理群聊中消息格式为"wxid_xxx:<xml>...</xml>"的情况，
        提取出纯XML内容便于后续解析

        Args:
            data: 原始消息数据

        Returns:
            处理后的XML内容
        """
        content = data.get("Data", {}).get("Content", {}).get("string", "")
        if not content:
            return ""

        # 检查是否为群消息
        from_wxid = data.get("Data", {}).get("FromUserName", {}).get("string", "")
        if "@chatroom" in from_wxid and ":" in content:
            # 尝试分离非XML前缀
            parts = content.split(":", 1)
            if len(parts) == 2 and "<" in parts[1]:
                return parts[1].strip()

        return content
