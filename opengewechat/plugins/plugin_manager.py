"""插件管理器

此模块提供了插件管理器，用于加载、启用和禁用插件。
"""

import os
import sys
import importlib
import inspect
import logging
from typing import Dict, List, Type, Optional, Set

from opengewechat.client import GewechatClient
from opengewechat.message.models import BaseMessage
from opengewechat.plugins.base_plugin import BasePlugin


class PluginManager:
    """插件管理器

    负责加载、启用和禁用插件。

    Attributes:
        plugins: 已加载的插件实例字典
        client: GewechatClient实例
    """

    def __init__(
        self, client: Optional[GewechatClient] = None, load_builtin: bool = True
    ):
        """初始化插件管理器

        Args:
            client: GewechatClient实例
            load_builtin: 是否加载内置插件，默认为True
        """
        self.plugins: Dict[str, BasePlugin] = {}
        self.client = client
        self.loaded_modules: Set[str] = set()

        # 加载内置插件
        if load_builtin:
            self._load_builtin_plugins()

    def _load_builtin_plugins(self):
        """加载内置插件"""
        try:
            # 加载消息日志记录插件
            from opengewechat.plugins.message_logger_plugin import MessageLoggerPlugin

            logger_plugin = MessageLoggerPlugin(self.client)
            self.plugins[logger_plugin.name] = logger_plugin
            logger_plugin.on_load()
            logging.info(f"内置插件 {logger_plugin.name} 已加载")
        except Exception as e:
            logging.error(f"加载内置插件时出错: {e}")

    def register_plugin(self, plugin_cls: Type[BasePlugin]) -> BasePlugin:
        """注册插件

        Args:
            plugin_cls: 插件类，必须是BasePlugin的子类

        Returns:
            插件实例

        Raises:
            TypeError: 如果插件类不是BasePlugin的子类
        """
        if not issubclass(plugin_cls, BasePlugin):
            raise TypeError(f"插件必须是BasePlugin的子类，当前类型: {plugin_cls}")

        plugin = plugin_cls(self.client)
        plugin_name = plugin.name

        if plugin_name in self.plugins:
            # 如果已存在同名插件，先卸载旧插件
            self.unload_plugin(plugin_name)

        self.plugins[plugin_name] = plugin
        plugin.on_load()

        return plugin

    def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件

        Args:
            plugin_name: 插件名称

        Returns:
            是否成功启用插件
        """
        if plugin_name not in self.plugins:
            logging.error(f"插件 {plugin_name} 未找到")
            return False

        plugin = self.plugins[plugin_name]
        if plugin.enabled:
            logging.info(f"插件 {plugin_name} 已经处于启用状态")
            return True

        try:
            plugin.on_enable()
            logging.info(f"插件 {plugin_name} 已启用")
            return True
        except Exception as e:
            logging.error(f"启用插件 {plugin_name} 时出错: {e}")
            return False

    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件

        Args:
            plugin_name: 插件名称

        Returns:
            是否成功禁用插件
        """
        if plugin_name not in self.plugins:
            logging.error(f"插件 {plugin_name} 未找到")
            return False

        plugin = self.plugins[plugin_name]
        if not plugin.enabled:
            logging.info(f"插件 {plugin_name} 已经处于禁用状态")
            return True

        try:
            plugin.on_disable()
            logging.info(f"插件 {plugin_name} 已禁用")
            return True
        except Exception as e:
            logging.error(f"禁用插件 {plugin_name} 时出错: {e}")
            return False

    def unload_plugin(self, plugin_name: str) -> bool:
        """卸载插件

        Args:
            plugin_name: 插件名称

        Returns:
            是否成功卸载插件
        """
        if plugin_name not in self.plugins:
            logging.error(f"插件 {plugin_name} 未找到")
            return False

        plugin = self.plugins[plugin_name]
        try:
            if plugin.enabled:
                plugin.on_disable()
            plugin.on_unload()
            del self.plugins[plugin_name]
            logging.info(f"插件 {plugin_name} 已卸载")
            return True
        except Exception as e:
            logging.error(f"卸载插件 {plugin_name} 时出错: {e}")
            return False

    def load_plugin_from_module(self, module_name: str) -> List[BasePlugin]:
        """从模块加载插件

        Args:
            module_name: 模块名称

        Returns:
            加载的插件列表
        """
        try:
            module = importlib.import_module(module_name)
            self.loaded_modules.add(module_name)

            plugins = []
            for name, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, BasePlugin) and cls != BasePlugin:
                    plugin = self.register_plugin(cls)
                    plugins.append(plugin)

            return plugins
        except Exception as e:
            logging.error(f"加载模块 {module_name} 时出错: {e}")
            return []

    def load_plugins_from_directory(
        self, directory: str, prefix: str = ""
    ) -> List[BasePlugin]:
        """从目录加载插件

        Args:
            directory: 插件目录路径
            prefix: 模块前缀

        Returns:
            加载的插件列表
        """
        if not os.path.isdir(directory):
            logging.error(f"目录 {directory} 不存在")
            return []

        # 将目录添加到Python路径
        if directory not in sys.path:
            sys.path.insert(0, directory)

        plugins = []
        for filename in os.listdir(directory):
            if filename.startswith("__") or not filename.endswith(".py"):
                continue

            module_name = filename[:-3]
            if prefix:
                module_name = f"{prefix}.{module_name}"

            plugins.extend(self.load_plugin_from_module(module_name))

        return plugins

    def process_message(self, message: BaseMessage) -> None:
        """处理消息

        使用所有已启用的插件处理消息。

        Args:
            message: 消息对象
        """
        for plugin in list(self.plugins.values()):
            if plugin.enabled and plugin.can_handle(message):
                try:
                    plugin.handle(message)
                except Exception as e:
                    logging.error(f"插件 {plugin.name} 处理消息时出错: {e}")

    def get_enabled_plugins(self) -> List[BasePlugin]:
        """获取所有已启用的插件

        Returns:
            已启用的插件列表
        """
        return [plugin for plugin in self.plugins.values() if plugin.enabled]

    def get_all_plugins(self) -> List[BasePlugin]:
        """获取所有插件

        Returns:
            所有插件列表
        """
        return list(self.plugins.values())

    def configure_message_logger(self, log_dir: str) -> bool:
        """配置消息日志记录插件

        Args:
            log_dir: 日志保存目录

        Returns:
            是否成功配置
        """
        if "MessageLoggerPlugin" not in self.plugins:
            logging.error("消息日志记录插件未加载")
            return False

        try:
            logger_plugin = self.plugins["MessageLoggerPlugin"]
            logger_plugin.change_log_directory(log_dir)
            return True
        except Exception as e:
            logging.error(f"配置消息日志记录插件时出错: {e}")
            return False
