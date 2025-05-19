"""数据库会话管理模块

提供数据库连接和会话管理功能，支持MySQL多schema。
"""

import asyncio
from typing import Dict, Optional, AsyncGenerator, Any
from contextlib import asynccontextmanager

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

# 创建全局数据库操作信号量，限制并发连接数
# 这有助于防止 "readexactly() called while another coroutine is already waiting for incoming data" 错误
DB_SEMAPHORE = asyncio.Semaphore(5)  # 限制最大并发连接数为5


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
        # 创建管理器锁，保护共享资源
        self.manager_lock = asyncio.Lock()
        # 活跃连接计数器
        self.active_connections = 0
        # 最大活跃连接数
        self.max_active_connections = 20
        # 连接监控
        self.connection_tracker = {}

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
            # 使用管理器锁保护引擎创建过程
            async with self.manager_lock:
                # 再次检查，避免竞态条件
                if device_id in self.engines:
                    return self.engines[device_id]

                # MySQL模式，每个设备使用独立schema
                schema_name = self.settings.get_schema_name(device_id)

                # 优化的连接池配置
                pool_options = {
                    "pool_size": 5,  # 连接池基础大小
                    "max_overflow": 10,  # 允许的额外连接数
                    "pool_timeout": 30,  # 获取连接超时时间（秒）
                    "pool_recycle": 1800,  # 连接回收时间（秒）
                    "pool_pre_ping": True,  # 使用前检查连接是否有效
                    "echo": False,  # 是否打印SQL语句
                    "future": True,  # 使用SQLAlchemy 2.0 API
                }

                # 首先连接到默认数据库
                db_url = self.settings.database.get_connection_string()
                engine = create_async_engine(db_url, **pool_options)

                # 检查并创建schema
                if self.settings.database.auto_create_schema:
                    await self._ensure_schema_exists(engine, schema_name)

                # 创建并返回连接到特定schema的引擎
                schema_url = self.settings.database.get_connection_string(schema_name)
                schema_engine = create_async_engine(schema_url, **pool_options)

                # 记录引擎创建时间
                self.engines[device_id] = schema_engine
                self.connection_tracker[device_id] = {
                    "created_at": asyncio.get_event_loop().time(),
                    "last_used": asyncio.get_event_loop().time(),
                    "activity_count": 0,
                }

                logger.info(
                    f"为设备 '{device_id}' 创建新的数据库引擎，使用schema: {schema_name}"
                )
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

        # 添加重试机制，提高可靠性
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                # 设置超时时间，避免长时间等待
                async with asyncio.timeout(10):  # 10秒超时
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

            except asyncio.TimeoutError:
                if attempt < max_attempts:
                    logger.warning(
                        f"检查/创建schema超时，尝试第{attempt}/{max_attempts}次"
                    )
                    # 指数退避等待
                    await asyncio.sleep(0.5 * (2 ** (attempt - 1)))
                else:
                    logger.error(f"检查/创建schema {schema_name} 失败: 超时")
                    return False
            except Exception as e:
                if attempt < max_attempts:
                    logger.warning(
                        f"确保schema存在失败，尝试第{attempt}/{max_attempts}次: {e}"
                    )
                    # 指数退避等待
                    await asyncio.sleep(0.5 * (2 ** (attempt - 1)))
                else:
                    logger.error(f"确保schema存在失败 ({schema_name}): {e}")
                    return False

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

        # 监控活跃连接数
        if self.active_connections >= self.max_active_connections:
            logger.warning(
                f"活跃连接数达到最大限制 ({self.active_connections}/{self.max_active_connections})，"
                f"请检查是否存在连接泄漏"
            )
            # 尝试清理潜在的旧连接
            await self._do_cleanup()

        # 如果会话工厂已经存在，直接返回
        if device_id in self.session_factories:
            # 更新连接使用统计
            if device_id in self.connection_tracker:
                self.connection_tracker[device_id]["last_used"] = (
                    asyncio.get_event_loop().time()
                )
                self.connection_tracker[device_id]["activity_count"] += 1
            return self.session_factories[device_id]

        # 使用管理器锁保护会话工厂创建过程
        async with self.manager_lock:
            # 再次检查，避免竞态条件
            if device_id in self.session_factories:
                return self.session_factories[device_id]

            # 添加重试机制，提高可靠性
            max_attempts = 3
            last_error = None

            for attempt in range(1, max_attempts + 1):
                try:
                    # 设置超时，避免永久等待
                    async with asyncio.timeout(5):  # 5秒超时
                        # 获取引擎并创建会话工厂
                        engine = await self.get_engine(device_id)

                        # 创建会话配置，使用expire_on_commit=False避免过期问题
                        session_factory = async_scoped_session(
                            sessionmaker(
                                engine,
                                class_=AsyncSession,
                                expire_on_commit=False,
                                # 设置自动提交和自动刷新
                                autocommit=False,
                                autoflush=False,
                            ),
                            scopefunc=asyncio.current_task,
                        )

                        self.session_factories[device_id] = session_factory

                        # 增加活跃连接计数
                        self.active_connections += 1

                        logger.debug(
                            f"为设备 '{device_id}' 创建新的会话工厂，当前活跃连接数: {self.active_connections}"
                        )

                        return session_factory
                except asyncio.TimeoutError:
                    last_error = "创建会话工厂超时"
                    if attempt < max_attempts:
                        logger.warning(
                            f"创建会话工厂超时，尝试第{attempt}/{max_attempts}次"
                        )
                        # 指数退避等待
                        await asyncio.sleep(0.5 * (2 ** (attempt - 1)))
                    else:
                        logger.error(
                            f"创建会话工厂失败 (device_id={device_id}): {last_error}"
                        )
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"创建会话工厂失败，尝试第{attempt}/{max_attempts}次: {e}"
                        )
                        # 指数退避等待
                        await asyncio.sleep(0.5 * (2 ** (attempt - 1)))
                    else:
                        logger.error(f"创建会话工厂失败 (device_id={device_id}): {e}")

            # 如果重试失败，清理可能部分创建的资源
            if device_id in self.engines:
                try:
                    await self.engines[device_id].dispose()
                    del self.engines[device_id]
                except Exception as cleanup_error:
                    logger.error(f"清理失败的引擎资源时出错: {cleanup_error}")

            # 所有尝试都失败，抛出最后一个错误
            if last_error:
                raise Exception(f"创建会话工厂失败: {last_error}")
            else:
                raise Exception("创建会话工厂失败: 未知错误")

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
            # 每次获取会话时记录一下连接使用统计
            if device_id in self.connection_tracker:
                self.connection_tracker[device_id]["last_used"] = (
                    asyncio.get_event_loop().time()
                )
                self.connection_tracker[device_id]["activity_count"] += 1

            session_factory = await self.get_session_factory(device_id)
            session = session_factory()
            return session

        # 创建一个临时event loop来获取会话实例
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果当前在事件循环中，我们创建一个future任务
            fut = asyncio.create_task(_get_session_async())
            # 但我们不能等待它完成，因为这会阻塞事件循环
            # 所以我们返回一个特殊的代理对象
            proxy = AsyncSessionProxy(fut)
            logger.debug(f"通过代理创建会话 (device_id={device_id})")
            return proxy
        else:
            # 如果没有运行中的事件循环，我们可以运行一个新的
            session = loop.run_until_complete(_get_session_async())
            logger.debug(f"直接创建会话 (device_id={device_id})")
            return session

    async def close(self):
        """关闭所有数据库连接"""
        # 记录关闭前状态，用于调试
        total_engines = len(self.engines)
        total_factories = len(self.session_factories)

        logger.info(
            f"开始关闭数据库连接... 引擎数: {total_engines}, 会话工厂数: {total_factories}, 活跃连接数: {self.active_connections}"
        )

        # 先尝试关闭会话工厂
        for device_id, factory in list(self.session_factories.items()):
            try:
                # 修复：factory.remove() 是协程，需要 await
                await factory.remove()
                logger.debug(f"已移除设备 '{device_id}' 的会话工厂")
            except Exception as e:
                logger.error(f"移除设备 '{device_id}' 会话工厂时出错: {e}")

        # 等待一小段时间，确保所有会话都有机会关闭
        await asyncio.sleep(0.5)

        # 然后关闭引擎
        for device_id, engine in list(self.engines.items()):
            try:
                # 获取连接池状态，用于调试
                try:
                    pool = engine.pool
                    logger.debug(
                        f"关闭前连接池状态 (device_id={device_id}): "
                        f"大小={pool.size()}, 已检入={pool.checkedin()}, "
                        f"已检出={pool.checkedout()}, 溢出={pool.overflow()}"
                    )
                except Exception:
                    pass

                # 强制关闭所有连接
                await engine.dispose()
                logger.info(f"已关闭设备 '{device_id}' 的数据库连接")
            except Exception as e:
                logger.error(f"关闭设备 '{device_id}' 数据库连接时出错: {e}")

        # 清理资源
        self.engines.clear()
        self.session_factories.clear()
        self.connection_tracker.clear()

        # 重置活跃连接计数
        active_connections = self.active_connections
        self.active_connections = 0

        logger.info(f"所有数据库连接已关闭，释放了 {active_connections} 个活跃连接")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.close()

    async def check_health(self) -> Dict[str, Any]:
        """检查数据库健康状态

        执行简单查询检查数据库连接是否正常工作，
        并收集连接池状态信息。

        Returns:
            Dict[str, Any]: 健康状态信息
        """
        health_info = {
            "status": "ok",
            "active_connections": self.active_connections,
            "max_connections": self.max_active_connections,
            "engines": {},
            "errors": [],
        }

        for device_id, engine in self.engines.items():
            try:
                # 获取连接池状态
                pool = engine.pool
                engine_info = {
                    "schema": self.settings.get_schema_name(device_id),
                    "pool_size": pool.size(),
                    "checkedin": pool.checkedin(),
                    "checkedout": pool.checkedout(),
                    "overflow": pool.overflow(),
                    "created_at": self.connection_tracker.get(device_id, {}).get(
                        "created_at", 0
                    ),
                    "last_used": self.connection_tracker.get(device_id, {}).get(
                        "last_used", 0
                    ),
                    "activity_count": self.connection_tracker.get(device_id, {}).get(
                        "activity_count", 0
                    ),
                }

                # 尝试执行简单查询以验证连接
                async with engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                    engine_info["connection_test"] = "pass"

                health_info["engines"][device_id] = engine_info
            except Exception as e:
                logger.error(f"设备 '{device_id}' 数据库健康检查失败: {e}")
                health_info["errors"].append(f"设备 '{device_id}': {str(e)}")
                health_info["status"] = "error"

        return health_info

    async def _do_cleanup(self):
        """清理长时间未使用的连接

        当连接数接近最大值时调用此方法，尝试释放闲置连接。
        """
        current_time = asyncio.get_event_loop().time()
        idle_threshold = 300  # 5分钟未使用的连接视为闲置

        cleaned_connections = 0

        # 记录当前连接池状态
        active_before = self.active_connections
        logger.debug(f"开始清理连接 (当前活跃连接数: {active_before})")

        # 检查每个设备的连接使用情况
        for device_id, tracker in list(self.connection_tracker.items()):
            # 如果设备连接长时间未使用，尝试关闭
            if current_time - tracker["last_used"] > idle_threshold:
                logger.debug(
                    f"设备 '{device_id}' 连接已闲置 {current_time - tracker['last_used']:.1f} 秒"
                )

                # 尝试清理会话工厂
                if device_id in self.session_factories:
                    try:
                        # 移除会话工厂
                        await self.session_factories[device_id].remove()
                        del self.session_factories[device_id]
                        logger.debug(f"已移除设备 '{device_id}' 的闲置会话工厂")
                        cleaned_connections += 1
                    except Exception as e:
                        logger.warning(
                            f"移除闲置会话工厂时出错 (device_id={device_id}): {e}"
                        )

                # 如果该设备活动计数较低，尝试关闭引擎
                if tracker["activity_count"] < 10:  # 低活动阈值
                    if device_id in self.engines:
                        try:
                            # 关闭引擎
                            await self.engines[device_id].dispose()
                            del self.engines[device_id]
                            del self.connection_tracker[device_id]
                            logger.info(f"已关闭设备 '{device_id}' 的闲置连接")
                            cleaned_connections += 1
                        except Exception as e:
                            logger.warning(
                                f"关闭闲置引擎时出错 (device_id={device_id}): {e}"
                            )

        # 更新活跃连接计数
        self.active_connections = max(0, self.active_connections - cleaned_connections)

        logger.debug(
            f"连接清理完成 (清理前: {active_before}, 清理后: {self.active_connections})"
        )
        return cleaned_connections


class AsyncSessionProxy:
    """异步会话代理，用于在同步代码中使用异步会话

    这个类代理所有方法调用到真正的AsyncSession实例，
    但会将调用推迟到实际实例可用时。
    """

    def __init__(self, session_future):
        self._session_future = session_future
        self._real_session = None
        self._closed = False
        self._in_transaction = False
        self._lock = asyncio.Lock()  # 添加锁以确保线程安全

    async def _get_real_session(self):
        """获取真实会话实例，确保线程安全"""
        async with self._lock:
            if self._real_session is None:
                try:
                    self._real_session = await self._session_future
                except Exception as e:
                    logger.error(f"获取真实会话实例失败: {e}")
                    raise
            return self._real_session

    async def __aenter__(self):
        """实现异步上下文管理器协议的入口方法

        使AsyncSessionProxy可以用于async with语句
        """
        self._session = await self._get_real_session()
        # 委托给实际会话的__aenter__方法
        if hasattr(self._session, "__aenter__"):
            result = await self._session.__aenter__()
            return result
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """实现异步上下文管理器协议的退出方法

        确保会话在退出上下文时被正确关闭
        """
        try:
            if hasattr(self._session, "__aexit__"):
                await self._session.__aexit__(exc_type, exc_val, exc_tb)

            # 如果在事务中，确保事务被提交或回滚
            if self._in_transaction:
                if exc_type:
                    # 如果有异常，回滚事务
                    await self.rollback()
                else:
                    # 否则提交事务
                    await self.commit()
        finally:
            # 无论如何都要确保会话被关闭
            if not self._closed:
                await self.close()

    def __getattr__(self, name):
        async def _proxied_method(*args, **kwargs):
            if self._closed and name != "close":
                logger.warning(f"尝试在已关闭的会话上调用方法: {name}")
                raise RuntimeError("会话已关闭")

            # 跟踪事务状态
            if name == "begin":
                self._in_transaction = True
            elif name in ["commit", "rollback"]:
                self._in_transaction = False

            try:
                async with self._lock:  # 使用锁保护方法调用
                    session = await self._get_real_session()
                    method = getattr(session, name)

                    if callable(method):
                        result = await method(*args, **kwargs)
                        # 如果是close方法，标记代理为已关闭
                        if name == "close":
                            self._closed = True
                            self._in_transaction = False
                        return result
                    return method
            except Exception as e:
                if name not in ["close", "rollback"]:  # 不要记录关闭和回滚的错误
                    logger.error(f"执行代理方法 {name} 时出错: {e}")
                # 如果在事务中发生错误，尝试回滚
                if self._in_transaction and name != "rollback":
                    self._in_transaction = False
                    try:
                        await self.rollback()
                    except Exception as rollback_error:
                        logger.error(f"执行回滚时出错: {rollback_error}")
                raise

        return _proxied_method

    async def close(self):
        """显式关闭方法，确保会话被关闭"""
        if not self._closed:
            try:
                async with self._lock:  # 使用锁保护关闭操作
                    session = await self._get_real_session()
                    # 如果在事务中，先尝试回滚
                    if self._in_transaction:
                        try:
                            await session.rollback()
                        except Exception as e:
                            logger.warning(f"关闭前回滚事务失败: {e}")
                    await session.close()
                    self._closed = True
                    self._in_transaction = False
                    logger.debug("会话代理成功关闭")
            except Exception as e:
                self._closed = True  # 尽管出错，仍然标记为已关闭，避免再次尝试
                logger.error(f"关闭会话代理时出错: {e}")
                raise


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
    session = None

    # 使用信号量限制并发数据库操作
    async with DB_SEMAPHORE:
        try:
            # 获取会话工厂
            session_factory = await db_manager.get_session_factory(device_id)
            session = session_factory()

            # 添加一些日志以帮助调试
            logger.debug(f"创建新的数据库会话 (device_id={device_id})")

            yield session
        except Exception as e:
            logger.error(f"创建数据库会话失败: {e}")
            raise
        finally:
            # 确保会话一定会被关闭，即使出现异常
            if session:
                try:
                    # 关闭会话
                    await session.close()
                    # 减少活跃连接计数
                    if (
                        hasattr(db_manager, "active_connections")
                        and db_manager.active_connections > 0
                    ):
                        db_manager.active_connections -= 1
                    logger.debug(f"数据库会话成功关闭 (device_id={device_id})")
                except Exception as e:
                    logger.error(f"关闭数据库会话失败: {e}")
                    # 不再尝试直接关闭底层连接，因为SQLAlchemy异步会话没有暴露这个API
                    # 而是通过引擎级别的dispose来处理连接泄漏问题


# 提供一个异步上下文管理器适配器，便于在 async with 语句中使用
@asynccontextmanager
async def async_db_session(
    device_id: Optional[str] = None,
) -> AsyncGenerator[AsyncSession, None]:
    """数据库会话的异步上下文管理器

    提供一个更简洁的方式在 async with 语句中使用数据库会话。

    Example:
        ```python
        async with async_db_session() as session:
            result = await session.execute(query)
            # ...
        ```

    Args:
        device_id: 可选的设备ID，用于指定schema

    Yields:
        AsyncSession: 数据库会话
    """
    async for session in get_db_session(device_id):
        try:
            yield session
        finally:
            # 会话会在get_db_session的finally块中自动关闭
            pass
