"""
API路由模块
"""

from fastapi import APIRouter
from .auth import router as auth_router
from .bots import router as bots_router
from .webhooks import router as webhooks_router
from .proxy import router as proxy_router
from .admin.config import router as admin_config_router
from .admin.plugins import router as admin_plugins_router

# 创建主API路由器
api_router = APIRouter(prefix="/api/v1")

# 注册子路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(bots_router, prefix="/bots", tags=["机器人管理"])
api_router.include_router(
    webhooks_router, prefix="/webhooks", tags=["Webhooks"])
api_router.include_router(proxy_router, prefix="/proxy", tags=["代理服务"])
api_router.include_router(
    admin_config_router, prefix="/admin/config", tags=["后台-配置管理"]
)
api_router.include_router(
    admin_plugins_router, prefix="/admin/plugins", tags=["后台-插件管理"]
)

__all__ = ["api_router"]
