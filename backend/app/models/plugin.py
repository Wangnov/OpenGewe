"""插件数据模型模块

定义插件的数据结构和操作方法。
"""

import json
from typing import Dict, List, Optional, Any
import asyncio

from sqlalchemy import Column, String, Boolean, Text, select, update, exc
from sqlalchemy.ext.asyncio import AsyncSession

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DB_SEMAPHORE

# 获取日志记录器
logger = get_logger("Plugin")

# 最大重试次数
MAX_RETRIES = 3
# 重试延迟（秒）
RETRY_DELAY = 0.5


class Plugin(Base):
    """插件模型

    存储插件的基本信息和配置。
    """

    name = Column(
        String(100), unique=True, index=True, nullable=False, comment="插件名称"
    )
    display_name = Column(String(100), nullable=False, comment="显示名称")
    description = Column(Text, nullable=True, comment="插件描述")
    version = Column(String(20), nullable=False, comment="插件版本")
    enabled = Column(Boolean, default=False, comment="是否启用")
    config = Column(Text, nullable=True, comment="插件配置(JSON格式)")
    path = Column(String(255), nullable=False, comment="插件路径")
    author = Column(String(100), nullable=True, comment="插件作者")

    @property
    def config_dict(self) -> Dict[str, Any]:
        """获取配置字典

        Returns:
            Dict[str, Any]: 配置字典
        """
        if not self.config:
            return {}
        try:
            return json.loads(self.config)
        except json.JSONDecodeError:
            logger.error(f"插件 {self.name} 的配置解析失败")
            return {}

    @config_dict.setter
    def config_dict(self, value: Dict[str, Any]) -> None:
        """设置配置字典

        Args:
            value: 配置字典
        """
        self.config = json.dumps(value, ensure_ascii=False)

    def to_dict(self) -> Dict[str, Any]:
        """将模型转换为字典

        Returns:
            Dict[str, Any]: 模型字典表示
        """
        result = super().to_dict()
        result["config"] = self.config_dict
        return result

    @classmethod
    async def _execute_with_retry(
        cls, operation_name: str, operation_func, *args, **kwargs
    ):
        """执行数据库操作并自动重试

        处理常见的数据库连接错误并尝试重试操作。

        Args:
            operation_name: 操作名称，用于日志记录
            operation_func: 要执行的异步函数
            args: 传递给操作函数的位置参数
            kwargs: 传递给操作函数的关键字参数

        Returns:
            操作函数的返回值或在失败时的默认值
        """
        retries = 0

        # 记录操作开始
        logger.debug(f"开始执行数据库操作: {operation_name}")

        while retries < MAX_RETRIES:
            semaphore_acquired = False
            try:
                # 获取信号量以限制并发数据库操作
                async with DB_SEMAPHORE:
                    semaphore_acquired = True
                    # 执行操作并返回结果
                    result = await operation_func(*args, **kwargs)
                    logger.debug(f"数据库操作成功: {operation_name}")
                    return result
            except (
                exc.OperationalError,
                exc.ResourceClosedError,
                exc.StatementError,
            ) as e:
                retries += 1
                if retries < MAX_RETRIES:
                    logger.warning(
                        f"{operation_name}失败（第{retries}次尝试）: {e}, 将在 {RETRY_DELAY * retries} 秒后重试"
                    )
                    await asyncio.sleep(RETRY_DELAY * retries)  # 增加重试延迟
                else:
                    logger.error(f"{operation_name}失败，已达到最大重试次数: {e}")
            except Exception as e:
                logger.error(f"{operation_name}失败: {e}")
                break
            finally:
                if not semaphore_acquired:
                    # 如果在获取信号量之前失败，确保不会影响其他操作
                    logger.debug(f"操作 {operation_name} 未获取信号量或已释放")

        # 记录操作结束但失败
        logger.warning(f"数据库操作 {operation_name} 失败后退出重试循环")

        # 根据操作函数的返回类型提供合适的默认值
        if operation_name.startswith("获取"):
            if "all" in operation_name.lower():
                return []  # 对于获取列表的操作返回空列表
            else:
                return None  # 对于获取单个对象的操作返回None
        else:
            return False  # 对于更新/创建等操作返回False表示失败

    @classmethod
    async def get_all(cls) -> List["Plugin"]:
        """获取所有插件

        Returns:
            List[Plugin]: 插件列表
        """

        async def _get_all():
            from backend.app.db import async_db_session

            async with async_db_session() as session:
                result = await session.execute(select(Plugin))
                return result.scalars().all()

        return await cls._execute_with_retry("获取所有插件", _get_all)

    @classmethod
    async def get_by_name(cls, name: str) -> Optional["Plugin"]:
        """通过名称获取插件

        Args:
            name: 插件名称

        Returns:
            Optional[Plugin]: 插件对象，如果不存在则为None
        """

        async def _get_by_name():
            from backend.app.db import async_db_session

            async with async_db_session() as session:
                result = await session.execute(
                    select(Plugin).where(Plugin.name == name)
                )
                return result.scalars().first()

        return await cls._execute_with_retry(f"获取插件 {name}", _get_by_name)

    @classmethod
    async def get_enabled(cls) -> List["Plugin"]:
        """获取所有已启用的插件

        Returns:
            List[Plugin]: 已启用的插件列表
        """

        async def _get_enabled():
            from backend.app.db import async_db_session

            async with async_db_session() as session:
                result = await session.execute(select(Plugin).where(Plugin.enabled))
                return result.scalars().all()

        return await cls._execute_with_retry("获取已启用插件", _get_enabled)

    @classmethod
    async def create(
        cls,
        name: str,
        display_name: str,
        description: str,
        version: str,
        path: str,
        enabled: bool = False,
        config: Dict[str, Any] = None,
        author: str = None,
    ) -> Optional["Plugin"]:
        """创建新插件

        Args:
            name: 插件名称
            display_name: 显示名称
            description: 描述
            version: 版本
            path: 插件路径
            enabled: 是否启用
            config: 配置
            author: 作者

        Returns:
            Optional[Plugin]: 创建的插件对象，失败则为None
        """

        # 首先进行重试包装的检查操作，因为多次调用get_by_name会导致连接问题
        async def _check_existing():
            from backend.app.db import async_db_session

            async with async_db_session() as session:
                result = await session.execute(
                    select(Plugin).where(Plugin.name == name)
                )
                return result.scalars().first()

        # 使用重试机制检查是否已存在
        existing = await cls._execute_with_retry(
            f"检查插件 {name} 是否存在", _check_existing
        )
        if existing:
            logger.warning(f"插件 {name} 已存在")
            return None

        async def _create():
            from backend.app.db import async_db_session

            async with async_db_session() as session:
                # 创建新插件
                plugin = Plugin(
                    name=name,
                    display_name=display_name,
                    description=description,
                    version=version,
                    path=path,
                    enabled=enabled,
                    author=author,
                )

                # 设置配置
                if config:
                    plugin.config_dict = config

                session.add(plugin)
                await session.commit()
                await session.refresh(plugin)
                logger.info(f"插件 {name} 创建成功")
                return plugin

        return await cls._execute_with_retry(f"创建插件 {name}", _create)

    @classmethod
    async def update_config(
        cls, name: str, config: Dict[str, Any], session: Optional[AsyncSession] = None
    ) -> bool:
        """更新插件配置

        Args:
            name: 插件名称
            config: 新配置
            session: 可选的会话对象

        Returns:
            bool: 操作是否成功
        """
        # 如果提供了外部会话，使用它，否则创建新会话
        if session is not None:
            # 使用外部提供的会话
            try:
                config_json = json.dumps(config, ensure_ascii=False)
                await session.execute(
                    update(Plugin).where(Plugin.name == name).values(config=config_json)
                )
                # 不提交，由调用者决定何时提交
                logger.debug(f"插件 {name} 配置已更新（使用外部会话）")
                return True
            except Exception as e:
                logger.error(f"更新插件配置失败: {e}")
                return False
        else:
            # 创建新会话
            async def _update_config():
                from backend.app.db import async_db_session

                async with async_db_session() as session:
                    config_json = json.dumps(config, ensure_ascii=False)
                    await session.execute(
                        update(Plugin)
                        .where(Plugin.name == name)
                        .values(config=config_json)
                    )
                    await session.commit()
                    logger.debug(f"插件 {name} 配置已更新")
                    return True

            return await cls._execute_with_retry(
                f"更新插件 {name} 配置", _update_config
            )

    @classmethod
    async def toggle_enabled(cls, name: str, enabled: bool) -> bool:
        """切换插件启用状态

        Args:
            name: 插件名称
            enabled: 是否启用

        Returns:
            bool: 操作是否成功
        """

        async def _toggle_enabled():
            from backend.app.db import async_db_session

            async with async_db_session() as session:
                await session.execute(
                    update(Plugin).where(Plugin.name == name).values(enabled=enabled)
                )
                await session.commit()

                status = "启用" if enabled else "禁用"
                logger.info(f"插件 {name} 已{status}")
                return True

        return await cls._execute_with_retry(
            f"{'启用' if enabled else '禁用'}插件 {name}", _toggle_enabled
        )
