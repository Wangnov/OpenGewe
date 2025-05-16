"""数据库会话管理模块

提供数据库连接和会话管理功能，支持MySQL多schema。
"""

import asyncio
from typing import Dict, Optional, AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
    AsyncEngine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from opengewe.logger import get_logger
from opengewe.utils.singleton import Singleton
from backend.app.core.config import get_settings
from backend.app.core.device import get_current_device_id

# 获取日志记录器
logger = get_logger("DB")


class DatabaseManager(metaclass=Singleton):
    """数据库管理器，负责创建和管理数据库连接

    支持MySQL数据库连接。
    使用单例模式确保只有一个数据库连接实例。
    支持多schema隔离不同设备的数据。
    """

    _instance = None

    def __new__(cls):
        """创建单例实例并初始化数据库连接"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_manager()
        return cls._instance

    def _init_manager(self):
        """初始化管理器状态"""
        self.engines: Dict[str, AsyncEngine] = {}
        self.session_factories: Dict[str, async_scoped_session] = {}
        self.initialized_schemas: set = set()
        self.settings = get_settings()

    async def get_engine(self, device_id: Optional[str] = None) -> AsyncEngine:
        """获取数据库引擎

        如果device_id未提供，将使用当前上下文中的device_id或默认设备

        Args:
            device_id: 设备ID，用于确定使用哪个schema

        Returns:
            AsyncEngine: SQLAlchemy异步引擎

        Raises:
            OperationalError: 无法连接到MySQL数据库
            Exception: 其他数据库错误
        """
        # 确定device_id
        device_id = (
            device_id
            or get_current_device_id()
            or self.settings.devices.get_default_device_id()
        )

        # 如果引擎已经存在，直接返回
        if device_id in self.engines:
            return self.engines[device_id]

        # 创建新引擎
        try:
            # MySQL模式，每个设备使用独立schema
            schema_name = self.settings.get_schema_name(device_id)

            # 首先连接到默认数据库
            db_url = self.settings.database.get_connection_string()
            engine = create_async_engine(db_url, echo=False, future=True)

            # 检查并创建schema
            if self.settings.database.auto_create_schema:
                await self._ensure_schema_exists(engine, schema_name)

            # 创建并返回连接到特定schema的引擎
            schema_url = self.settings.database.get_connection_string(schema_name)
            schema_engine = create_async_engine(schema_url, echo=False, future=True)
            self.engines[device_id] = schema_engine
            return schema_engine

        except OperationalError as e:
            error_msg = f"无法连接到MySQL数据库: {str(e)}"
            logger.error(error_msg)
            raise OperationalError(
                f"MySQL连接失败: {str(e)}. 请检查数据库设置和连接。", params={}, orig=e
            )
        except Exception as e:
            error_msg = f"创建数据库引擎失败 (device_id={device_id}): {str(e)}"
            logger.error(error_msg)
            raise

    async def _ensure_schema_exists(
        self, engine: AsyncEngine, schema_name: str
    ) -> bool:
        """确保schema存在，如果不存在则创建

        Args:
            engine: 用于执行SQL的引擎
            schema_name: 要检查或创建的schema名称

        Returns:
            bool: 是否成功确保schema存在
        """
        if schema_name in self.initialized_schemas:
            return True

        try:
            async with engine.begin() as conn:
                # 检查schema是否存在
                result = await conn.execute(
                    text(
                        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :schema"
                    ),
                    {"schema": schema_name},
                )
                schema_exists = result.scalar() is not None

                if not schema_exists:
                    # 创建schema
                    logger.info(f"创建新的数据库schema: {schema_name}")
                    await conn.execute(text(f"CREATE DATABASE `{schema_name}`"))

                self.initialized_schemas.add(schema_name)
                return True
        except Exception as e:
            logger.error(f"确保schema存在失败 ({schema_name}): {e}")
            return False

    async def get_session_factory(
        self, device_id: Optional[str] = None
    ) -> async_scoped_session:
        """获取会话工厂

        Args:
            device_id: 设备ID，用于确定使用哪个schema

        Returns:
            async_scoped_session: 会话工厂
        """
        # 确定device_id
        device_id = (
            device_id
            or get_current_device_id()
            or self.settings.devices.get_default_device_id()
        )

        # 如果会话工厂已经存在，直接返回
        if device_id in self.session_factories:
            return self.session_factories[device_id]

        # 获取引擎并创建会话工厂
        engine = await self.get_engine(device_id)
        session_factory = async_scoped_session(
            sessionmaker(engine, class_=AsyncSession, expire_on_commit=False),
            scopefunc=asyncio.current_task,
        )
        self.session_factories[device_id] = session_factory
        return session_factory

    def get_session(self, device_id: Optional[str] = None) -> AsyncSession:
        """获取数据库会话

        如果device_id未提供，将使用当前上下文中的device_id

        Args:
            device_id: 可选的设备ID，用于指定schema

        Returns:
            AsyncSession: SQLAlchemy异步会话
        """
        # 这里使用同步方法创建会话，但实际的数据库操作是异步的
        device_id = (
            device_id
            or get_current_device_id()
            or self.settings.devices.get_default_device_id()
        )

        async def _get_session_async():
            session_factory = await self.get_session_factory(device_id)
            return session_factory()

        # 创建一个临时event loop来获取会话实例
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果当前在事件循环中，我们创建一个future任务
            fut = asyncio.create_task(_get_session_async())
            # 但我们不能等待它完成，因为这会阻塞事件循环
            # 所以我们返回一个特殊的代理对象
            return AsyncSessionProxy(fut)
        else:
            # 如果没有运行中的事件循环，我们可以运行一个新的
            return loop.run_until_complete(_get_session_async())

    async def close(self):
        """关闭所有数据库连接"""
        for device_id, engine in self.engines.items():
            await engine.dispose()
            logger.info(f"已关闭设备 '{device_id}' 的数据库连接")
        self.engines.clear()
        self.session_factories.clear()
        logger.info("所有数据库连接已关闭")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.close()


class AsyncSessionProxy:
    """异步会话代理，用于在同步代码中使用异步会话

    这个类代理所有方法调用到真正的AsyncSession实例，
    但会将调用推迟到实际实例可用时。
    """

    def __init__(self, session_future):
        self._session_future = session_future
        self._real_session = None

    async def _get_real_session(self):
        if self._real_session is None:
            self._real_session = await self._session_future
        return self._real_session

    def __getattr__(self, name):
        async def _proxied_method(*args, **kwargs):
            session = await self._get_real_session()
            method = getattr(session, name)

            if callable(method):
                return await method(*args, **kwargs)
            return method

        return _proxied_method


# 提供简便的获取会话函数，用于依赖注入
async def get_db_session(
    device_id: Optional[str] = None,
) -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话的辅助函数

    用于依赖注入场景，每个请求获取一个新的会话。
    如果不提供device_id，则使用当前上下文中的device_id。

    Args:
        device_id: 可选的设备ID，用于指定schema

    Yields:
        AsyncSession: 数据库会话
    """
    # 使用当前上下文中的设备ID或传入的设备ID
    device_id = device_id or get_current_device_id()

    # 创建数据库管理器实例
    db_manager = DatabaseManager()

    # 获取会话工厂
    session_factory = await db_manager.get_session_factory(device_id)
    session = session_factory()

    try:
        yield session
    finally:
        await session.close()
