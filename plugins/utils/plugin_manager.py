"""插件管理器桥接模块

重新导出opengewe.utils.plugin_manager中的PluginManager类，
为插件提供导入兼容性。
"""

from opengewe.utils.plugin_manager import PluginManager

# 重新导出PluginManager
__all__ = ["PluginManager"] 