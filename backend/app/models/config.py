"""配置数据模型模块

定义系统配置和用户偏好设置的数据结构和操作方法。
"""

import json
from typing import Dict, List, Optional, Any, Union

from sqlalchemy import Column, String, Text, select, update

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DatabaseManager

# 获取日志记录器
logger = get_logger("Config")


class Config(Base):
    """配置模型

    存储系统配置和用户偏好设置。
    """

    key = Column(String(100), unique=True, index=True, nullable=False, comment="配置键")
    value = Column(Text, nullable=True, comment="配置值(JSON格式)")
    category = Column(String(50), index=True, nullable=False, comment="配置类别")
    description = Column(Text, nullable=True, comment="配置描述")

    @property
    def value_parsed(self) -> Any:
        """获取解析后的值

        Returns:
            Any: 解析后的值
        """
        if not self.value:
            return None
        try:
            return json.loads(self.value)
        except json.JSONDecodeError:
            logger.error(f"配置 {self.key} 的值解析失败")
            return self.value

    @value_parsed.setter
    def value_parsed(self, value: Any) -> None:
        """设置解析后的值

        Args:
            value: 要设置的值
        """
        if isinstance(value, (dict, list)):
            self.value = json.dumps(value, ensure_ascii=False)
        elif value is None:
            self.value = None
        else:
            self.value = json.dumps(value, ensure_ascii=False)

    def to_dict(self) -> Dict[str, Any]:
        """将模型转换为字典

        Returns:
            Dict[str, Any]: 模型字典表示
        """
        result = super().to_dict()
        result["value"] = self.value_parsed
        return result

    @classmethod
    async def get_all(cls) -> List["Config"]:
        """获取所有配置

        Returns:
            List[Config]: 配置列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(select(Config))
                return result.scalars().all()
            except Exception as e:
                logger.error(f"获取所有配置失败: {e}")
                return []

    @classmethod
    async def get_by_category(cls, category: str) -> List["Config"]:
        """获取指定类别的所有配置

        Args:
            category: 配置类别

        Returns:
            List[Config]: 配置列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(
                    select(Config).where(Config.category == category)
                )
                return result.scalars().all()
            except Exception as e:
                logger.error(f"获取类别 {category} 配置失败: {e}")
                return []

    @classmethod
    async def get_by_key(cls, key: str) -> Optional["Config"]:
        """通过键获取配置

        Args:
            key: 配置键

        Returns:
            Optional[Config]: 配置对象，如果不存在则为None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(select(Config).where(Config.key == key))
                return result.scalars().first()
            except Exception as e:
                logger.error(f"通过键获取配置失败: {e}")
                return None

    @classmethod
    async def get_value(cls, key: str, default: Any = None) -> Any:
        """获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            Any: 配置值，如果不存在则返回默认值
        """
        config = await cls.get_by_key(key)
        if not config:
            return default
        return config.value_parsed

    @classmethod
    async def set_value(
        cls,
        key: str,
        value: Any,
        category: str = "general",
        description: Optional[str] = None,
    ) -> bool:
        """设置配置值

        Args:
            key: 配置键
            value: 配置值
            category: 配置类别
            description: 配置描述

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 检查是否已存在
                config = await cls.get_by_key(key)

                if config:
                    # 更新现有配置
                    data = {"value": json.dumps(value, ensure_ascii=False)}
                    if category:
                        data["category"] = category
                    if description:
                        data["description"] = description

                    await session.execute(
                        update(Config).where(Config.key == key).values(**data)
                    )
                else:
                    # 创建新配置
                    config = Config(
                        key=key,
                        category=category,
                        description=description,
                    )
                    config.value_parsed = value
                    session.add(config)

                await session.commit()
                logger.debug(f"配置 {key} 已设置")
                return True
            except Exception as e:
                logger.error(f"设置配置值失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def delete(cls, key: str) -> bool:
        """删除配置

        Args:
            key: 配置键

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                config = await cls.get_by_key(key)
                if not config:
                    logger.warning(f"配置 {key} 不存在")
                    return False

                await session.delete(config)
                await session.commit()
                logger.info(f"配置 {key} 已删除")
                return True
            except Exception as e:
                logger.error(f"删除配置失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def get_dict_by_category(cls, category: str) -> Dict[str, Any]:
        """获取指定类别的配置字典

        Args:
            category: 配置类别

        Returns:
            Dict[str, Any]: 配置字典
        """
        configs = await cls.get_by_category(category)
        result = {}
        for config in configs:
            result[config.key] = config.value_parsed
        return result

    @classmethod
    async def set_dict(cls, config_dict: Dict[str, Any], category: str) -> bool:
        """批量设置配置

        Args:
            config_dict: 配置字典
            category: 配置类别

        Returns:
            bool: 操作是否成功
        """
        success = True
        for key, value in config_dict.items():
            result = await cls.set_value(key, value, category)
            if not result:
                success = False
        return success

    @classmethod
    async def ensure_defaults(
        cls, defaults: Dict[str, Dict[str, Union[Any, str]]]
    ) -> None:
        """确保默认配置存在

        Args:
            defaults: 默认配置字典，格式为 {key: {"value": Any, "category": str, "description": str}}
        """
        for key, config in defaults.items():
            # 检查是否已存在
            existing = await cls.get_by_key(key)
            if not existing:
                # 创建默认配置
                await cls.set_value(
                    key=key,
                    value=config.get("value"),
                    category=config.get("category", "general"),
                    description=config.get("description"),
                )
                logger.debug(f"创建默认配置: {key}")

        logger.info("默认配置检查完成")
