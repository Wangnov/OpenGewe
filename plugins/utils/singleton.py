"""单例模式桥接模块

重新导出opengewe.utils.singleton中的Singleton元类，
为插件提供导入兼容性。
"""

from opengewe.utils.singleton import Singleton

# 重新导出Singleton元类
__all__ = ["Singleton"] 