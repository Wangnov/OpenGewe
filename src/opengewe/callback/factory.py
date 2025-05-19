from __future__ import annotations
from typing import (
    Dict,
    List,
    Any,
    Optional,
    Type,
    Callable,
    Set,
    Coroutine,
    Union,
    TYPE_CHECKING,
)
import json
import asyncio

from opengewe.logger import get_logger

from opengewe.callback.types import MessageType
from opengewe.callback.models import BaseMessage
from opengewe.callback.handlers import DEFAULT_HANDLERS, BaseHandler

if TYPE_CHECKING:
    from opengewe.client import GeweClient
    from opengewe.utils.plugin_manager import PluginManager

# 获取消息工厂日志记录器
logger = get_logger("MessageFactory")

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

    def __init__(self, client: Optional["GeweClient"] = None):
        """初始化消息工厂

        Args:
            client: GeweClient实例，用于获取base_url和download_url，以便下载媒体文件
        """
        self.handlers: List[BaseHandler] = []
        self.client = client
        self.on_message_callback: Optional[AsyncMessageCallback] = None
        self._tasks: Set[asyncio.Task] = set()
        # 插件管理器将在后续步骤中实现
        self.plugin_manager: Optional["PluginManager"] = None

        # 注册默认的消息处理器
        for handler_cls in DEFAULT_HANDLERS:
            self.register_handler(handler_cls)

        logger.debug(f"消息工厂初始化完成，已注册 {len(self.handlers)} 个消息处理器")

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
        logger.debug(
            f"注册消息回调函数成功: {callback.__name__ if hasattr(callback, '__name__') else str(callback)}"
        )

    def set_plugin_manager(self, plugin_manager: "PluginManager") -> None:
        """设置插件管理器

        Args:
            plugin_manager: 插件管理器实例
        """
        self.plugin_manager = plugin_manager
        logger.debug("插件管理器设置成功")

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
        type_name = data.get("TypeName", "未知")

        logger.debug(
            f"开始处理消息 TypeName={type_name}, Appid={data.get('Appid', '')}"
        )

        matched_handler = None
        for handler in self.handlers:
            try:
                if await handler.can_handle(data):
                    matched_handler = handler.__class__.__name__
                    logger.debug(f"找到匹配的处理器: {matched_handler}")
                    message = await handler.handle(data)
                    if message:
                        logger.debug(
                            f"处理器 {matched_handler} 成功创建消息对象: {message.type.name}"
                        )
                    else:
                        logger.warning(f"处理器 {matched_handler} 返回了空消息对象")
                    break
            except Exception as e:
                logger.error(
                    f"处理器 {handler.__class__.__name__} 处理消息时出错: {e}",
                    exc_info=True,
                )

        if not matched_handler:
            logger.debug(f"没有找到匹配的处理器处理消息 TypeName={type_name}")

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
            logger.debug(f"创建了未知类型的通用消息对象: {type_name}")

        # 如果获取到了消息对象
        if message:
            # 如果注册了回调函数，创建任务异步调用回调函数
            if self.on_message_callback:
                logger.debug(f"准备调用消息回调函数处理 {message.type.name} 消息")
                task = asyncio.create_task(self._execute_callback(message))
                self._tasks.add(task)
                task.add_done_callback(self._tasks.discard)
            else:
                logger.warning("未注册消息回调函数，消息将不会被进一步处理")

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
            logger.debug(f"开始执行消息回调函数: {message.type.name}")
            await self.on_message_callback(message)
            logger.debug(f"消息回调函数执行完成: {message.type.name}")
        except Exception as e:
            logger.error(f"处理消息回调时出错: {e}", exc_info=True)

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
            logger.error(f"JSON解析失败: {json_data}")
            return None
        except Exception as e:
            logger.error(f"处理消息时出错: {e}", exc_info=True)
            return None

    def process_async(self, data: Dict[str, Any]) -> asyncio.Task:
        """异步处理消息，不等待结果

        创建一个任务来处理消息，立即返回任务对象

        Args:
            data: 原始消息数据，通常是从回调接口接收到的JSON数据

        Returns:
            asyncio.Task: 消息处理任务
        """
        logger.debug(f"创建异步任务处理消息 TypeName={data.get('TypeName', '未知')}")
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

    async def process_payload(self, payload: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理回调payload，是process方法的别名

        用于处理webhook回调中的payload数据

        Args:
            payload: 原始消息数据，通常是从回调接口接收到的JSON数据

        Returns:
            处理后的消息对象，如果没有找到合适的处理器则返回None
        """
        return await self.process(payload)

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
            logger.error(f"加载插件失败: {e}")
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
