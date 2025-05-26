"""
数据库连接和管理
"""

from typing import AsyncGenerator, Dict
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from loguru import logger

from .config import get_settings


class Base(DeclarativeBase):
    """SQLAlchemy Base类"""

    pass


class DatabaseManager:
    """数据库管理器"""

    def __init__(self):
        self.settings = get_settings()
        self._engines: Dict[str, AsyncEngine] = {}
        self._session_makers: Dict[str, async_sessionmaker] = {}

        # 创建主数据库引擎（admin_data）
        self._create_main_engine()

    def _create_main_engine(self):
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
        schema_name = (
            f"bot_{gewe_app_id.replace('@', '_').replace('.', '_').replace('-', '_')}"
        )

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
        schema_name = (
            f"bot_{gewe_app_id.replace('@', '_').replace('.', '_').replace('-', '_')}"
        )

        # 使用主数据库连接创建新Schema
        async with self._session_makers["admin_data"]() as session:
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

        # 导入机器人相关的表结构并创建

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info(f"机器人表结构已创建: {schema_name}")

    def get_session_maker(self, schema_name: str = "admin_data") -> async_sessionmaker:
        """获取会话制造器"""
        if schema_name not in self._session_makers:
            raise ValueError(f"Schema {schema_name} 的会话制造器不存在")
        return self._session_makers[schema_name]

    async def close_all(self):
        """关闭所有数据库连接"""
        for name, engine in self._engines.items():
            await engine.dispose()
            logger.info(f"数据库引擎已关闭: {name}")

        self._engines.clear()
        self._session_makers.clear()


# 全局数据库管理器实例
db_manager = DatabaseManager()


async def get_db_session(
    schema_name: str = "admin_data",
) -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话（依赖注入用）"""
    session_maker = db_manager.get_session_maker(schema_name)
    async with session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_admin_session() -> AsyncGenerator[AsyncSession, None]:
    """获取管理员数据库会话"""
    async for session in get_db_session("admin_data"):
        yield session


@asynccontextmanager
async def get_bot_session(gewe_app_id: str) -> AsyncGenerator[AsyncSession, None]:
    """获取机器人数据库会话"""
    schema_name = (
        f"bot_{gewe_app_id.replace('@', '_').replace('.', '_').replace('-', '_')}"
    )

    # 确保机器人引擎存在
    if schema_name not in db_manager._session_makers:
        await db_manager.create_bot_engine(gewe_app_id)

    async for session in get_db_session(schema_name):
        yield session
