"""事件管理器桥接模块

重新导出opengewe.utils.event_manager中的EventManager类，
为插件提供导入兼容性。
"""

from opengewe.utils.event_manager import EventManager

# 重新导出EventManager
__all__ = ["EventManager"]
