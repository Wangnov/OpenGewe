"""插件系统

此包提供了opengewechat的插件扩展功能，允许用户编写和加载自定义插件。
"""

from opengewechat.plugins.base_plugin import BasePlugin
from opengewechat.plugins.plugin_manager import PluginManager
from opengewechat.plugins.built_in import __all__ as builtin_plugins_names
from opengewechat.plugins.built_in import *  # noqa: F403

# 构建__all__列表
__all__ = ["BasePlugin", "PluginManager"] + builtin_plugins_names
