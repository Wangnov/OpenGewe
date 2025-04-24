from typing import Dict, List, Any, Optional, Type, Callable
import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

from opengewechat.message.types import MessageType
from opengewechat.message.models import BaseMessage
from opengewechat.message.handlers import BaseHandler, DEFAULT_HANDLERS
from opengewechat.plugins import PluginManager


class MessageFactory:
    """消息处理工厂

    用于识别和处理各种微信回调消息类型，返回统一的消息对象。

    提供了注册自定义处理器的方法，使用者可以根据需要扩展支持的消息类型。

    Attributes:
        handlers: 已注册的消息处理器列表
        client: GewechatClient实例
        on_message_callback: 消息处理回调函数
        executor: 线程池执行器，用于异步处理消息
        plugin_manager: 插件管理器实例，用于管理插件
    """

    def __init__(self, client=None, max_workers=10):
        """初始化消息工厂

        Args:
            client: GewechatClient实例，用于获取base_url和download_url，以便下载媒体文件
            max_workers: 线程池中的最大工作线程数，默认为10
        """
        self.handlers: List[BaseHandler] = []
        self.client = client
        self.on_message_callback: Optional[Callable[[BaseMessage], Any]] = None
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.plugin_manager = PluginManager(client)

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
        同时，会将消息传递给所有已启用的插件进行处理。

        Args:
            data: 原始消息数据，通常是从回调接口接收到的JSON数据

        Returns:
            处理后的消息对象，如果没有找到合适的处理器则返回None
        """
        # 遍历所有处理器，找到第一个可以处理该消息的处理器
        message = None
        for handler in self.handlers:
            if handler.can_handle(data):
                message = handler.handle(data)
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
            # 如果注册了回调函数，在新线程中异步调用回调函数
            if self.on_message_callback:
                self.executor.submit(self._execute_callback, message)

            # 将消息传递给所有已启用的插件进行处理
            self.executor.submit(self.plugin_manager.process_message, message)

        return message

    def _execute_callback(self, message: BaseMessage) -> None:
        """在单独的线程中执行回调函数

        Args:
            message: 处理后的消息对象
        """
        try:
            self.on_message_callback(message)
        except Exception as e:
            logging.error(f"处理消息回调时出错: {e}")

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

    def process_async(self, data: Dict[str, Any]) -> None:
        """异步处理消息

        将消息处理任务提交到线程池，立即返回，不会阻塞主线程

        Args:
            data: 原始消息数据，通常是从回调接口接收到的JSON数据
        """
        self.executor.submit(self.process, data)

    def process_json_async(self, json_data: str) -> None:
        """异步处理JSON格式的消息

        Args:
            json_data: JSON格式的消息数据
        """
        self.executor.submit(self.process_json, json_data)

    # 以下是插件系统相关方法

    def load_plugin(self, plugin_cls: Type) -> bool:
        """加载插件

        Args:
            plugin_cls: 插件类，必须是BasePlugin的子类

        Returns:
            是否成功加载插件
        """
        try:
            self.plugin_manager.register_plugin(plugin_cls)
            return True
        except Exception as e:
            logging.error(f"加载插件失败: {e}")
            return False

    def load_plugins_from_directory(self, directory: str, prefix: str = "") -> List:
        """从目录加载插件

        Args:
            directory: 插件目录路径
            prefix: 模块前缀

        Returns:
            加载的插件列表
        """
        return self.plugin_manager.load_plugins_from_directory(directory, prefix)

    def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件

        Args:
            plugin_name: 插件名称

        Returns:
            是否成功启用插件
        """
        return self.plugin_manager.enable_plugin(plugin_name)

    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件

        Args:
            plugin_name: 插件名称

        Returns:
            是否成功禁用插件
        """
        return self.plugin_manager.disable_plugin(plugin_name)

    def get_all_plugins(self) -> List:
        """获取所有插件

        Returns:
            所有插件列表
        """
        return self.plugin_manager.get_all_plugins()

    def get_enabled_plugins(self) -> List:
        """获取所有已启用的插件

        Returns:
            已启用的插件列表
        """
        return self.plugin_manager.get_enabled_plugins()
