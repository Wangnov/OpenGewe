from dataclasses import dataclass
from typing import Dict, Any
import xml.etree.ElementTree as ET
import logging

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import BaseMessage


@dataclass
class TextMessage(BaseMessage):
    """文本消息"""

    text: str = ""  # 文本内容

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TextMessage":
        """从字典创建文本消息对象"""
        try:
            msg = cls(
                type=MessageType.TEXT,
                app_id=data.get("Appid", ""),
                wxid=data.get("Wxid", ""),
                typename=data.get("TypeName", ""),
                raw_data=data,
            )

            if "Data" in data:
                msg_data = data["Data"]
                msg.msg_id = str(msg_data.get("MsgId", ""))
                msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
                msg.create_time = msg_data.get("CreateTime", 0)

                if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                    msg.from_wxid = msg_data["FromUserName"]["string"]

                if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                    msg.to_wxid = msg_data["ToUserName"]["string"]

                if "Content" in msg_data and "string" in msg_data["Content"]:
                    msg.content = msg_data["Content"]["string"]
                    msg.text = msg_data["Content"]["string"]

                    # 处理群消息发送者
                    msg._process_group_message()
                    # 同步更新text字段
                    msg.text = msg.content

            return msg
        except Exception as e:
            logging.error(f"TextMessage.from_dict处理失败: {e}", exc_info=True)
            raise


@dataclass
class QuoteMessage(BaseMessage):
    """引用消息"""

    text: str = ""  # 文本内容
    quoted_msg_id: str = ""  # 被引用消息ID
    quoted_content: str = ""  # 被引用消息内容

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuoteMessage":
        """从字典创建引用消息对象"""
        try:
            msg = cls(
                type=MessageType.QUOTE,
                app_id=data.get("Appid", ""),
                wxid=data.get("Wxid", ""),
                typename=data.get("TypeName", ""),
                raw_data=data,
            )

            if "Data" in data:
                msg_data = data["Data"]
                msg.msg_id = str(msg_data.get("MsgId", ""))
                msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
                msg.create_time = msg_data.get("CreateTime", 0)

                if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                    msg.from_wxid = msg_data["FromUserName"]["string"]

                if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                    msg.to_wxid = msg_data["ToUserName"]["string"]

                if "Content" in msg_data and "string" in msg_data["Content"]:
                    msg.content = msg_data["Content"]["string"]

                    # 处理群消息发送者
                    msg._process_group_message()

                    # 解析引用消息内容
                    try:
                        root = ET.fromstring(msg.content)
                        # 获取引用的消息内容
                        title_node = root.find(".//title")
                        if title_node is not None and title_node.text:
                            msg.quoted_content = title_node.text

                        # 获取引用消息ID
                        msg_source_node = root.find(".//refermsg/svrid")
                        if msg_source_node is not None and msg_source_node.text:
                            msg.quoted_msg_id = msg_source_node.text

                        # 获取当前消息文本内容
                        content_node = root.find(".//content")
                        if content_node is not None and content_node.text:
                            msg.text = content_node.text
                    except Exception as e:
                        # 解析失败时记录异常信息但不影响消息处理
                        logging.error(f"解析引用消息XML失败: {e}", exc_info=True)

            return msg
        except Exception as e:
            logging.error(f"QuoteMessage.from_dict处理失败: {e}", exc_info=True)
            raise
