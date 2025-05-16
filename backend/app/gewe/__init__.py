"""GeweClient集成包

提供与OpenGewe库的集成功能，包括客户端工厂、客户端管理器和依赖项函数。
"""

# 导入客户端工厂
from backend.app.gewe.client_factory import create_client, verify_client_config

# 导入客户端管理器
from backend.app.gewe.client_manager import GeweClientManager, client_manager

# 导入依赖项函数
from backend.app.gewe.dependencies import get_gewe_client, get_optional_gewe_client

__all__ = [
    # 客户端工厂
    "create_client",
    "verify_client_config",
    # 客户端管理器
    "GeweClientManager",
    "client_manager",
    # 依赖项函数
    "get_gewe_client",
    "get_optional_gewe_client",
]
