"""
统一的Session管理器

解决session管理混乱和依赖注入问题，提供类型安全的session API
"""

from typing import AsyncGenerator, Dict, Any
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy import text
from loguru import logger

from .config import get_settings
from .bases import BotBase


class SessionManager:
    """统一的Session管理器"""

    def __init__(self):
        self.settings = get_settings()
        self._engines: Dict[str, AsyncEngine] = {}
        self._session_makers: Dict[str, async_sessionmaker] = {}
        self._initialized = False

    async def initialize(self):
        """初始化session管理器"""
        if self._initialized:
            return

        # 创建主数据库引擎（admin_data）
        await self._create_main_engine()
        self._initialized = True
        logger.info("SessionManager初始化完成")

    async def _create_main_engine(self):
        """创建主数据库引擎"""
        engine = create_async_engine(
            self.settings.database_url,
            pool_size=self.settings.database_pool_size,
            max_overflow=self.settings.database_max_overflow,
            echo=self.settings.database_echo_sql,
            future=True,
        )

        session_maker = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

        self._engines["admin_data"] = engine
        self._session_makers["admin_data"] = session_maker

        logger.info("主数据库引擎已创建")

    async def create_bot_engine(self, gewe_app_id: str) -> AsyncEngine:
        """为机器人创建专用数据库引擎"""
        schema_name = self._get_bot_schema_name(gewe_app_id)

        if schema_name in self._engines:
            return self._engines[schema_name]

        # 构建机器人专用数据库URL
        base_url = self.settings.database_url.rsplit("/", 1)[0]
        bot_db_url = f"{base_url}/{schema_name}"

        engine = create_async_engine(
            bot_db_url,
            pool_size=5,
            max_overflow=10,
            echo=self.settings.database_echo_sql,
            future=True,
        )

        session_maker = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

        self._engines[schema_name] = engine
        self._session_makers[schema_name] = session_maker

        logger.info(f"机器人 {gewe_app_id} 的数据库引擎已创建: {schema_name}")
        return engine

    async def create_bot_schema(self, gewe_app_id: str) -> str:
        """为机器人创建数据库Schema"""
        schema_name = self._get_bot_schema_name(gewe_app_id)

        # 使用主数据库连接创建新Schema
        async with self.get_admin_session() as session:
            try:
                # 创建数据库Schema
                await session.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS {schema_name}")
                )
                await session.commit()

                logger.info(f"数据库Schema已创建: {schema_name}")

                # 创建对应的引擎
                await self.create_bot_engine(gewe_app_id)

                # 在新Schema中创建表结构
                await self._create_bot_tables(schema_name)

                return schema_name

            except Exception as e:
                await session.rollback()
                logger.error(f"创建机器人Schema失败: {e}")
                raise

    async def _create_bot_tables(self, schema_name: str):
        """在机器人Schema中创建表结构"""
        if schema_name not in self._engines:
            raise ValueError(f"Schema {schema_name} 的引擎不存在")

        engine = self._engines[schema_name]

        async with engine.begin() as conn:
            await conn.run_sync(BotBase.metadata.create_all)
            logger.info(f"机器人表结构已创建: {schema_name}")

    def _get_bot_schema_name(self, gewe_app_id: str) -> str:
        """获取机器人Schema名称"""
        return (
            f"bot_{gewe_app_id.replace('@', '_').replace('.', '_').replace('-', '_')}"
        )

    # FastAPI依赖注入专用函数
    async def get_admin_session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """获取管理员数据库会话（用于FastAPI依赖注入）"""
        if not self._initialized:
            await self.initialize()

        session_maker = self._session_makers["admin_data"]
        async with session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Admin session错误: {e}")
                raise
            finally:
                await session.close()

    async def get_bot_session_dependency(
        self, gewe_app_id: str
    ) -> AsyncGenerator[AsyncSession, None]:
        """获取机器人数据库会话（用于FastAPI依赖注入）"""
        if not self._initialized:
            await self.initialize()

        schema_name = self._get_bot_schema_name(gewe_app_id)

        # 确保机器人引擎存在
        if schema_name not in self._session_makers:
            await self.create_bot_engine(gewe_app_id)

        session_maker = self._session_makers[schema_name]
        async with session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Bot session错误 {gewe_app_id}: {e}")
                raise
            finally:
                await session.close()

    # 上下文管理器专用函数
    @asynccontextmanager
    async def get_admin_session(self) -> AsyncGenerator[AsyncSession, None]:
        """获取管理员数据库会话（上下文管理器）"""
        if not self._initialized:
            await self.initialize()

        session_maker = self._session_makers["admin_data"]
        async with session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Admin session错误: {e}")
                raise

    @asynccontextmanager
    async def get_bot_session(
        self, gewe_app_id: str
    ) -> AsyncGenerator[AsyncSession, None]:
        """获取机器人数据库会话（上下文管理器）"""
        if not self._initialized:
            await self.initialize()

        schema_name = self._get_bot_schema_name(gewe_app_id)

        # 确保机器人引擎存在
        if schema_name not in self._session_makers:
            await self.create_bot_engine(gewe_app_id)

        session_maker = self._session_makers[schema_name]
        async with session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Bot session错误 {gewe_app_id}: {e}")
                raise

    # 事务管理辅助函数
    async def execute_in_admin_session(self, func, *args, **kwargs) -> Any:
        """在管理员session中执行函数"""
        async with self.get_admin_session() as session:
            result = await func(session, *args, **kwargs)
            await session.commit()
            return result

    async def execute_in_bot_session(
        self, gewe_app_id: str, func, *args, **kwargs
    ) -> Any:
        """在机器人session中执行函数"""
        async with self.get_bot_session(gewe_app_id) as session:
            result = await func(session, *args, **kwargs)
            await session.commit()
            return result

    # 连接池管理
    async def get_pool_status(self) -> Dict[str, Any]:
        """获取连接池状态"""
        status = {}
        for name, engine in self._engines.items():
            pool = engine.pool
            status[name] = {
                "size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "invalidated": pool.invalidated(),
            }
        return status

    async def close_all(self):
        """关闭所有数据库连接"""
        for name, engine in self._engines.items():
            await engine.dispose()
            logger.info(f"数据库引擎已关闭: {name}")

        self._engines.clear()
        self._session_makers.clear()
        self._initialized = False


# 全局session管理器实例
session_manager = SessionManager()


# FastAPI依赖注入函数（无装饰器）
async def get_admin_session() -> AsyncGenerator[AsyncSession, None]:
    """获取管理员数据库会话（FastAPI依赖注入专用）"""
    async for session in session_manager.get_admin_session_dependency():
        yield session


async def get_bot_session_func(gewe_app_id: str) -> AsyncGenerator[AsyncSession, None]:
    """获取机器人数据库会话（FastAPI依赖注入专用）"""
    async for session in session_manager.get_bot_session_dependency(gewe_app_id):
        yield session


# 便捷的上下文管理器函数
def admin_session():
    """获取管理员session的上下文管理器"""
    return session_manager.get_admin_session()


def bot_session(gewe_app_id: str):
    """获取机器人session的上下文管理器"""
    return session_manager.get_bot_session(gewe_app_id)
