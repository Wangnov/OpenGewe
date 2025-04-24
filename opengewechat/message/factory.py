from typing import Dict, List, Any, Optional, Type, Callable
import json
import logging

from opengewechat.message.types import MessageType
from opengewechat.message.models import BaseMessage
from opengewechat.message.handlers import BaseHandler, DEFAULT_HANDLERS


class MessageFactory:
    """消息处理工厂

    用于识别和处理各种微信回调消息类型，返回统一的消息对象。

    提供了注册自定义处理器的方法，使用者可以根据需要扩展支持的消息类型。

    Attributes:
        handlers: 已注册的消息处理器列表
        client: GewechatClient实例
        on_message_callback: 消息处理回调函数
    """

    def __init__(self, client=None):
        """初始化消息工厂

        Args:
            client: GewechatClient实例，用于获取base_url和download_url，以便下载媒体文件
        """
        self.handlers: List[BaseHandler] = []
        self.client = client
        self.on_message_callback: Optional[Callable[[BaseMessage], Any]] = None

        # 注册默认的消息处理器
        for handler_cls in DEFAULT_HANDLERS:
            self.register_handler(handler_cls)

    def register_handler(self, handler_cls: Type[BaseHandler]) -> None:
        """注册消息处理器

        Args:
            handler_cls: 处理器类，必须是BaseHandler的子类
        """
        if not issubclass(handler_cls, BaseHandler):
            raise TypeError(f"处理器必须是BaseHandler的子类，当前类型: {handler_cls}")

        handler = handler_cls(self.client)
        self.handlers.append(handler)

    def register_callback(self, callback: Callable[[BaseMessage], Any]) -> None:
        """注册消息处理回调函数

        Args:
            callback: 回调函数，接收BaseMessage对象作为参数
        """
        self.on_message_callback = callback

    def process(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理消息

        根据消息内容找到合适的处理器进行处理，返回处理后的消息对象。
        如果注册了回调函数，会在处理完成后调用回调函数。

        Args:
            data: 原始消息数据，通常是从回调接口接收到的JSON数据

        Returns:
            处理后的消息对象，如果没有找到合适的处理器则返回None
        """
        # 遍历所有处理器，找到第一个可以处理该消息的处理器
        for handler in self.handlers:
            if handler.can_handle(data):
                message = handler.handle(data)

                # 如果注册了回调函数，调用回调函数
                if message and self.on_message_callback:
                    try:
                        self.on_message_callback(message)
                    except Exception as e:
                        logging.error(f"处理消息回调时出错: {e}")

                return message

        # 如果没有找到合适的处理器，返回一个通用消息
        if data.get("TypeName") in ["AddMsg", "ModContacts", "DelContacts", "Offline"]:
            message = BaseMessage(
                type=MessageType.UNKNOWN,
                app_id=data.get("Appid", ""),
                wxid=data.get("Wxid", ""),
                typename=data.get("TypeName", ""),
                raw_data=data,
            )

            # 如果注册了回调函数，调用回调函数
            if self.on_message_callback:
                try:
                    self.on_message_callback(message)
                except Exception as e:
                    logging.error(f"处理未知消息回调时出错: {e}")

            return message

        return None

    def process_json(self, json_data: str) -> Optional[BaseMessage]:
        """处理JSON格式的消息

        Args:
            json_data: JSON格式的消息数据

        Returns:
            处理后的消息对象，如果JSON解析失败或没有找到合适的处理器则返回None
        """
        try:
            data = json.loads(json_data)
            return self.process(data)
        except json.JSONDecodeError:
            logging.error(f"JSON解析失败: {json_data}")
            return None
        except Exception as e:
            logging.error(f"处理消息时出错: {e}")
            return None
