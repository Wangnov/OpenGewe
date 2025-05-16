"""插件数据模型模块

定义插件的数据结构和操作方法。
"""

import json
from typing import Dict, List, Optional, Any

from sqlalchemy import Column, String, Boolean, Text, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DatabaseManager

# 获取日志记录器
logger = get_logger("Plugin")


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
    async def get_all(cls) -> List["Plugin"]:
        """获取所有插件

        Returns:
            List[Plugin]: 插件列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(select(Plugin))
                return result.scalars().all()
            except Exception as e:
                logger.error(f"获取所有插件失败: {e}")
                return []

    @classmethod
    async def get_by_name(cls, name: str) -> Optional["Plugin"]:
        """通过名称获取插件

        Args:
            name: 插件名称

        Returns:
            Optional[Plugin]: 插件对象，如果不存在则为None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(
                    select(Plugin).where(Plugin.name == name)
                )
                return result.scalars().first()
            except Exception as e:
                logger.error(f"通过名称获取插件失败: {e}")
                return None

    @classmethod
    async def get_enabled(cls) -> List["Plugin"]:
        """获取所有已启用的插件

        Returns:
            List[Plugin]: 已启用的插件列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(select(Plugin).where(Plugin.enabled))
                return result.scalars().all()
            except Exception as e:
                logger.error(f"获取已启用插件失败: {e}")
                return []

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
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 检查是否已存在
                existing = await cls.get_by_name(name)
                if existing:
                    logger.warning(f"插件 {name} 已存在")
                    return None

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
            except Exception as e:
                logger.error(f"创建插件失败: {e}")
                await session.rollback()
                return None

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
        should_close = session is None
        if session is None:
            db_manager = DatabaseManager()
            session = db_manager.get_session()

        try:
            config_json = json.dumps(config, ensure_ascii=False)

            # 更新配置
            await session.execute(
                update(Plugin).where(Plugin.name == name).values(config=config_json)
            )

            if should_close:
                await session.commit()

            logger.debug(f"插件 {name} 配置已更新")
            return True
        except Exception as e:
            logger.error(f"更新插件配置失败: {e}")
            if should_close:
                await session.rollback()
            return False

    @classmethod
    async def toggle_enabled(cls, name: str, enabled: bool) -> bool:
        """切换插件启用状态

        Args:
            name: 插件名称
            enabled: 是否启用

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                await session.execute(
                    update(Plugin).where(Plugin.name == name).values(enabled=enabled)
                )
                await session.commit()

                status = "启用" if enabled else "禁用"
                logger.info(f"插件 {name} 已{status}")
                return True
            except Exception as e:
                logger.error(f"切换插件状态失败: {e}")
                await session.rollback()
                return False
