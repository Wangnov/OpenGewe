"""插件基类桥接模块

重新导出opengewe.utils.plugin_base中的PluginBase类，
为插件提供导入兼容性。
"""

from opengewe.utils.plugin_base import PluginBase

# 重新导出PluginBase类
__all__ = ["PluginBase"]
