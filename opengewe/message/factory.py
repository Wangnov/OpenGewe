from typing import Dict, List, Any, Optional, Type, Callable, Set, Coroutine, Union
import json
import logging
import asyncio
from functools import partial

from opengewe.message.types import MessageType
from opengewe.message.models import BaseMessage
from opengewe.message.handlers import DEFAULT_HANDLERS, BaseHandler

# 异步处理器类型定义
AsyncHandlerResult = Union[BaseMessage, None]
AsyncHandlerCoroutine = Coroutine[Any, Any, AsyncHandlerResult]
AsyncMessageCallback = Callable[[BaseMessage], Coroutine[Any, Any, Any]]


class MessageFactory:
    """异步消息处理工厂

    用于识别和处理各种微信回调消息类型，返回统一的消息对象。

    提供了注册自定义处理器的方法，使用者可以根据需要扩展支持的消息类型。

    Attributes:
        handlers: 已注册的消息处理器列表
        client: GeweClient实例
        on_message_callback: 消息处理回调函数
        plugin_manager: 插件管理器实例，用于管理插件
        _tasks: 正在进行的异步任务集合
    """

    def __init__(self, client=None):
        """初始化消息工厂

        Args:
            client: GeweClient实例，用于获取base_url和download_url，以便下载媒体文件
        """
        self.handlers: List[BaseHandler] = []
        self.client = client
        self.on_message_callback: Optional[AsyncMessageCallback] = None
        self._tasks: Set[asyncio.Task] = set()
        # 插件管理器将在后续步骤中实现
        self.plugin_manager = None

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

    def register_callback(self, callback: AsyncMessageCallback) -> None:
        """注册消息处理回调函数

        Args:
            callback: 异步回调函数，接收BaseMessage对象作为参数
        """
        self.on_message_callback = callback

    async def process(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理消息

        根据消息内容找到合适的处理器进行处理，返回处理后的消息对象。
        如果注册了回调函数，会在处理完成后调用回调函数。
        同时，会将消息传递给所有已启用的插件进行处理。

        Args:
            data: 原始消息数据，通常是从回调接口接收到的JSON数据

        Returns:
            处理后的消息对象，如果没有找到合适的处理器则返回None
        """
        # 遍历所有处理器，找到第一个可以处理该消息的处理器
        message = None
        for handler in self.handlers:
            if await handler.can_handle(data):
                message = await handler.handle(data)
                break

        # 如果没有找到合适的处理器，返回一个通用消息
        if message is None and data.get("TypeName") in [
            "AddMsg",
            "ModContacts",
            "DelContacts",
            "Offline",
        ]:
            message = BaseMessage(
                type=MessageType.UNKNOWN,
                app_id=data.get("Appid", ""),
                wxid=data.get("Wxid", ""),
                typename=data.get("TypeName", ""),
                raw_data=data,
            )

        # 如果获取到了消息对象
        if message:
            # 如果注册了回调函数，创建任务异步调用回调函数
            if self.on_message_callback:
                task = asyncio.create_task(self._execute_callback(message))
                self._tasks.add(task)
                task.add_done_callback(self._tasks.discard)

            # 将消息传递给所有已启用的插件进行处理
            if self.plugin_manager:
                task = asyncio.create_task(self.plugin_manager.process_message(message))
                self._tasks.add(task)
                task.add_done_callback(self._tasks.discard)

        return message

    async def _execute_callback(self, message: BaseMessage) -> None:
        """异步执行回调函数

        Args:
            message: 处理后的消息对象
        """
        try:
            await self.on_message_callback(message)
        except Exception as e:
            logging.error(f"处理消息回调时出错: {e}")

    async def process_json(self, json_data: str) -> Optional[BaseMessage]:
        """处理JSON格式的消息

        Args:
            json_data: JSON格式的消息数据

        Returns:
            处理后的消息对象，如果JSON解析失败或没有找到合适的处理器则返回None
        """
        try:
            data = json.loads(json_data)
            return await self.process(data)
        except json.JSONDecodeError:
            logging.error(f"JSON解析失败: {json_data}")
            return None
        except Exception as e:
            logging.error(f"处理消息时出错: {e}")
            return None

    def process_async(self, data: Dict[str, Any]) -> asyncio.Task:
        """异步处理消息，不等待结果

        创建一个任务来处理消息，立即返回任务对象

        Args:
            data: 原始消息数据，通常是从回调接口接收到的JSON数据

        Returns:
            asyncio.Task: 消息处理任务
        """
        task = asyncio.create_task(self.process(data))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    def process_json_async(self, json_data: str) -> asyncio.Task:
        """异步处理JSON格式的消息，不等待结果

        Args:
            json_data: JSON格式的消息数据

        Returns:
            asyncio.Task: 消息处理任务
        """
        task = asyncio.create_task(self.process_json(json_data))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    # 以下是插件系统相关方法，将在后续步骤中实现完整功能

    async def load_plugin(self, plugin_cls: Type) -> bool:
        """异步加载插件

        Args:
            plugin_cls: 插件类，必须是BasePlugin的子类

        Returns:
            是否成功加载插件
        """
        try:
            if self.plugin_manager:
                return await self.plugin_manager.register_plugin(plugin_cls)
            return False
        except Exception as e:
            logging.error(f"加载插件失败: {e}")
            return False

    async def load_plugins_from_directory(
        self, directory: str, prefix: str = ""
    ) -> List:
        """从目录异步加载插件

        Args:
            directory: 插件目录路径
            prefix: 模块前缀

        Returns:
            加载的插件列表
        """
        if self.plugin_manager:
            return await self.plugin_manager.load_plugins_from_directory(
                directory, prefix
            )
        return []
