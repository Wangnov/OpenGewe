"""API路由包

收集并导出所有API路由。
"""

from fastapi import APIRouter

from backend.app.api.routes import webhook, plugins, files, robots, system, admin

# 创建主路由器
api_router = APIRouter()

# 注册所有子路由器
api_router.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
api_router.include_router(plugins.router, prefix="/plugins", tags=["plugins"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(robots.router, prefix="/robots", tags=["robots"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])


# 添加健康检查路由
@api_router.get("/health", tags=["system"])
async def health_check():
    """健康检查端点"""
    return {"status": "ok"}
