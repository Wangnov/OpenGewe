"""
配置管理服务
"""

from typing import Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from ..models.main_config import MainConfig
from ..core.session_manager import session_manager
from opengewe.logger import init_default_logger, get_logger

init_default_logger()
logger = get_logger(__name__)


class ConfigManager:
    """配置管理器"""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_version: Dict[str, int] = {}

    async def get_config(self, section_name: str) -> Optional[Dict[str, Any]]:
        """
        获取配置段

        Args:
            section_name: 配置段名称

        Returns:
            配置数据字典或None
        """
        try:
            # 先检查缓存
            if section_name in self._cache:
                logger.debug(f"从缓存获取配置段: {section_name}")
                return self._cache[section_name]

            # 从数据库获取
            async with session_manager.get_admin_session() as session:
                stmt = select(MainConfig).where(MainConfig.section_name == section_name)
                result = await session.execute(stmt)
                config = result.scalar_one_or_none()

                if config:
                    logger.debug(f"从数据库获取配置段: {section_name}")
                    self._cache[section_name] = config.config_json
                    self._cache_version[section_name] = config.version
                    return config.config_json

                logger.debug(f"配置段不存在: {section_name}")
                return None

        except SQLAlchemyError as e:
            logger.error(f"获取配置段失败 {section_name}: {e}")
            return None

    async def set_config(
        self,
        section_name: str,
        config_data: Dict[str, Any],
        validate_func: Optional[callable] = None,
    ) -> bool:
        """
        设置配置段

        Args:
            section_name: 配置段名称
            config_data: 配置数据
            validate_func: 配置验证函数

        Returns:
            是否成功
        """
        try:
            # 配置验证
            if validate_func and not validate_func(config_data):
                logger.error(f"配置验证失败: {section_name}")
                return False

            async with session_manager.get_admin_session() as session:
                # 查找现有配置
                stmt = select(MainConfig).where(MainConfig.section_name == section_name)
                result = await session.execute(stmt)
                config = result.scalar_one_or_none()

                if config:
                    # 更新现有配置
                    config.config_json = config_data
                    config.version += 1
                    logger.info(f"更新配置段: {section_name}, 版本: {config.version}")
                else:
                    # 创建新配置
                    config = MainConfig(
                        section_name=section_name, config_json=config_data, version=1
                    )
                    session.add(config)
                    logger.info(f"创建配置段: {section_name}")

                await session.commit()

                # 更新缓存
                self._cache[section_name] = config_data
                self._cache_version[section_name] = config.version

                return True

        except SQLAlchemyError as e:
            logger.error(f"设置配置段失败 {section_name}: {e}")
            return False

    async def delete_config(self, section_name: str) -> bool:
        """
        删除配置段

        Args:
            section_name: 配置段名称

        Returns:
            是否成功
        """
        try:
            async with session_manager.get_admin_session() as session:
                stmt = select(MainConfig).where(MainConfig.section_name == section_name)
                result = await session.execute(stmt)
                config = result.scalar_one_or_none()

                if config:
                    session.delete(config)
                    await session.commit()

                    # 清除缓存
                    self._cache.pop(section_name, None)
                    self._cache_version.pop(section_name, None)

                    logger.info(f"删除配置段: {section_name}")
                    return True

                logger.warning(f"配置段不存在，无法删除: {section_name}")
                return False

        except SQLAlchemyError as e:
            logger.error(f"删除配置段失败 {section_name}: {e}")
            return False

    async def get_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有配置段

        Returns:
            所有配置段的字典
        """
        try:
            async with session_manager.get_admin_session() as session:
                stmt = select(MainConfig)
                result = await session.execute(stmt)
                configs = result.scalars().all()

                result_dict = {}
                for config in configs:
                    result_dict[config.section_name] = config.config_json
                    # 更新缓存
                    self._cache[config.section_name] = config.config_json
                    self._cache_version[config.section_name] = config.version

                logger.debug(f"获取所有配置段，共 {len(result_dict)} 个")
                return result_dict

        except SQLAlchemyError as e:
            logger.error(f"获取所有配置段失败: {e}")
            return {}

    def clear_cache(self, section_name: Optional[str] = None):
        """
        清除缓存

        Args:
            section_name: 指定配置段名称，None表示清除所有缓存
        """
        if section_name:
            self._cache.pop(section_name, None)
            self._cache_version.pop(section_name, None)
            logger.debug(f"清除配置段缓存: {section_name}")
        else:
            self._cache.clear()
            self._cache_version.clear()
            logger.debug("清除所有配置缓存")

    def get_cache_status(self) -> Dict[str, Any]:
        """
        获取缓存状态

        Returns:
            缓存状态信息
        """
        return {
            "cached_sections": list(self._cache.keys()),
            "cache_versions": self._cache_version.copy(),
            "cache_size": len(self._cache),
        }


# 全局配置管理器实例
config_manager = ConfigManager()
