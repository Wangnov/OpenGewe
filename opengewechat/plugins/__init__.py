"""插件系统

此包提供了opengewechat的插件扩展功能，允许用户编写和加载自定义插件。
"""

from opengewechat.plugins.base_plugin import BasePlugin
from opengewechat.plugins.plugin_manager import PluginManager
from opengewechat.plugins.message_logger_plugin import MessageLoggerPlugin

__all__ = ["BasePlugin", "PluginManager", "MessageLoggerPlugin"]
