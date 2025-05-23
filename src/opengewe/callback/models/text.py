from dataclasses import dataclass
from typing import Dict, Any, Optional, TYPE_CHECKING
import xml.etree.ElementTree as ET

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import TextBaseMessage
from opengewe.logger import get_logger

# 使用TYPE_CHECKING条件导入
if TYPE_CHECKING:
    from opengewe.client import GeweClient

# 获取客户端日志记录器
logger = get_logger("GeweClient")

@dataclass
class TextMessage(TextBaseMessage):
    """文本消息"""
    
    # 设置消息类型类变量
    message_type = MessageType.TEXT
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理文本消息特有数据"""
        if "Data" in data and "Content" in data["Data"] and "string" in data["Data"]["Content"]:
            self.text = data["Data"]["Content"]["string"]

@dataclass
class QuoteMessage(TextBaseMessage):
    """引用消息"""
    quoted_msg_id: str = ""  # 被引用消息ID
    quoted_content: str = ""  # 被引用消息内容
    
    # 设置消息类型类变量
    message_type = MessageType.QUOTE
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理引用消息特有数据"""
        try:
            # 解析引用消息内容
            root = ET.fromstring(self.content)
            # 获取引用的消息内容
            title_node = root.find(".//title")
            if title_node is not None and title_node.text:
                self.quoted_content = title_node.text

            # 获取引用消息ID
            msg_source_node = root.find(".//refermsg/svrid")
            if msg_source_node is not None and msg_source_node.text:
                self.quoted_msg_id = msg_source_node.text

            # 获取当前消息文本内容
            content_node = root.find(".//content")
            if content_node is not None and content_node.text:
                self.text = content_node.text
        except Exception as e:
            # 解析失败时记录异常信息但不影响消息处理
            logger.error(f"解析引用消息XML失败: {e}", exc_info=True)
