"""
配置初始化器
"""

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from typing import Dict, Any
from pathlib import Path

from ...services.config_manager import config_manager
from opengewe.logger import get_logger

logger = get_logger(__name__)


class ConfigInitializer:
    """配置初始化器"""

    # 需要迁移到数据库的配置段（排除gewe_apps）
    MIGRATE_SECTIONS = ["plugins", "queue", "logging", "webpanel"]

    def __init__(self, config_file_path: str = None):
        """
        初始化配置初始化器

        Args:
            config_file_path: 配置文件路径，默认为main_config.toml
        """
        if config_file_path is None:
            # 默认配置文件路径
            self.config_file_path = (
                Path(__file__).parent.parent.parent.parent.parent / "main_config.toml"
            )
        else:
            self.config_file_path = Path(config_file_path)

    def load_toml_config(self) -> Dict[str, Any]:
        """
        从TOML文件加载配置

        Returns:
            配置字典
        """
        try:
            if not self.config_file_path.exists():
                logger.warning(f"配置文件不存在: {self.config_file_path}")
                return {}

            with open(self.config_file_path, "rb") as f:
                config = tomllib.load(f)

            logger.info(f"成功加载配置文件: {self.config_file_path}")
            return config

        except Exception as e:
            logger.error(f"加载配置文件失败 {self.config_file_path}: {e}")
            return {}

    async def initialize_config(self) -> bool:
        """
        初始化配置，将TOML配置迁移到数据库

        Returns:
            是否成功初始化
        """
        try:
            logger.info("开始初始化配置...")

            # 加载TOML配置
            toml_config = self.load_toml_config()
            if not toml_config:
                logger.warning("没有找到有效的配置文件，跳过配置初始化")
                return True

            # 获取现有数据库配置
            existing_configs = await config_manager.get_all_configs()

            success_count = 0
            total_count = 0

            # 迁移指定的配置段
            for section_name in self.MIGRATE_SECTIONS:
                total_count += 1

                if section_name not in toml_config:
                    logger.debug(f"TOML文件中没有配置段: {section_name}")
                    continue

                # 检查数据库中是否已存在该配置
                if section_name in existing_configs:
                    logger.debug(f"配置段已存在于数据库中，跳过迁移: {section_name}")
                    success_count += 1
                    continue

                # 迁移配置段到数据库
                section_config = toml_config[section_name]
                if await config_manager.set_config(section_name, section_config):
                    logger.info(f"成功迁移配置段到数据库: {section_name}")
                    success_count += 1
                else:
                    logger.error(f"迁移配置段失败: {section_name}")

            logger.info(
                f"配置初始化完成，成功迁移 {success_count}/{total_count} 个配置段"
            )
            return success_count == total_count

        except Exception as e:
            logger.error(f"配置初始化失败: {e}")
            return False

    async def migrate_section(self, section_name: str, force: bool = False) -> bool:
        """
        迁移单个配置段

        Args:
            section_name: 配置段名称
            force: 是否强制覆盖已存在的配置

        Returns:
            是否成功迁移
        """
        try:
            if section_name not in self.MIGRATE_SECTIONS:
                logger.error(f"配置段不在迁移列表中: {section_name}")
                return False

            # 加载TOML配置
            toml_config = self.load_toml_config()
            if section_name not in toml_config:
                logger.error(f"TOML文件中没有配置段: {section_name}")
                return False

            # 检查数据库中是否已存在
            existing_config = await config_manager.get_config(section_name)
            if existing_config and not force:
                logger.warning(f"配置段已存在，使用force=True强制覆盖: {section_name}")
                return False

            # 迁移配置
            section_config = toml_config[section_name]
            if await config_manager.set_config(section_name, section_config):
                logger.info(f"成功迁移配置段: {section_name}")
                return True
            else:
                logger.error(f"迁移配置段失败: {section_name}")
                return False

        except Exception as e:
            logger.error(f"迁移配置段异常 {section_name}: {e}")
            return False

    async def get_migration_status(self) -> Dict[str, Any]:
        """
        获取迁移状态

        Returns:
            迁移状态信息
        """
        try:
            toml_config = self.load_toml_config()
            db_configs = await config_manager.get_all_configs()

            status = {
                "config_file_exists": self.config_file_path.exists(),
                "config_file_path": str(self.config_file_path),
                "migrate_sections": self.MIGRATE_SECTIONS,
                "sections_in_file": [],
                "sections_in_db": list(db_configs.keys()),
                "migrated_sections": [],
                "pending_sections": [],
            }

            if toml_config:
                status["sections_in_file"] = [
                    s for s in self.MIGRATE_SECTIONS if s in toml_config
                ]

                for section in self.MIGRATE_SECTIONS:
                    if section in toml_config and section in db_configs:
                        status["migrated_sections"].append(section)
                    elif section in toml_config and section not in db_configs:
                        status["pending_sections"].append(section)

            return status

        except Exception as e:
            logger.error(f"获取迁移状态失败: {e}")
            return {
                "error": str(e),
                "config_file_exists": False,
                "migrate_sections": self.MIGRATE_SECTIONS,
            }


# 全局配置初始化器实例
config_initializer = ConfigInitializer()
