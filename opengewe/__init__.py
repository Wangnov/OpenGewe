"""OpenGewe - 基于Gewe的异步微信API框架

OpenGewe是一个用于与Gewe微信第三方API交互的异步Python库，
提供了高性能的微信自动化解决方案。

该库使用asyncio提供全异步API，适用于高并发应用场景。
"""

__version__ = "0.0.1"

from opengewe.client import GeweClient

__all__ = ["GeweClient"]
