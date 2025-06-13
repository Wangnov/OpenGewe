"""
数据库连接和管理

重构后的简化版本，主要负责向后兼容性
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from .session_manager import session_manager
from .bases import AdminBase as Base, BotBase  # 向后兼容

# 向后兼容的导出
__all__ = ["Base", "BotBase", "db_manager", "get_admin_session", "get_bot_session"]


class DatabaseManager:
    """数据库管理器（向后兼容）"""

    def __init__(self):
        self._session_manager = session_manager

    async def create_bot_schema(self, gewe_app_id: str) -> str:
        """为机器人创建数据库Schema"""
        return await self._session_manager.create_bot_schema(gewe_app_id)

    async def create_bot_engine(self, gewe_app_id: str):
        """为机器人创建专用数据库引擎"""
        return await self._session_manager.create_bot_engine(gewe_app_id)

    async def close_all(self):
        """关闭所有数据库连接"""
        await self._session_manager.close_all()


# 全局数据库管理器实例（向后兼容）
db_manager = DatabaseManager()


# 向后兼容的session函数
async def get_admin_session() -> AsyncGenerator[AsyncSession, None]:
    """获取管理员数据库会话（向后兼容）"""
    async for session in session_manager.get_admin_session_dependency():
        yield session


async def get_bot_session(gewe_app_id: str) -> AsyncGenerator[AsyncSession, None]:
    """获取机器人数据库会话（向后兼容）"""
    async for session in session_manager.get_bot_session_dependency(gewe_app_id):
        yield session
