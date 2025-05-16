"""API路由包

收集并导出所有API路由。
"""

from fastapi import APIRouter

# 创建主路由器
api_router = APIRouter()

# 导入并包含子路由器
# 随着项目发展，可以添加更多的路由模块
# from .users import router as users_router
# from .messages import router as messages_router

# api_router.include_router(users_router, prefix="/users", tags=["users"])
# api_router.include_router(messages_router, prefix="/messages", tags=["messages"])


# 添加健康检查路由
@api_router.get("/health", tags=["system"])
async def health_check():
    """健康检查端点"""
    return {"status": "ok"}
