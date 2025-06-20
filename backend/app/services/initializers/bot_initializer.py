"""
机器人配置初始化服务

负责在应用启动时检查并初始化机器人配置
"""

import os
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ...core.session_manager import admin_session, session_manager
from ...models.bot import BotInfo
from opengewe.logger import init_default_logger, get_logger

init_default_logger()
logger = get_logger(__name__)

try:
    import tomllib
except ImportError:
    import tomli as tomllib


async def initialize_bots_from_config() -> None:
    """
    初始化机器人配置

    首先检查数据库中是否已有机器人，如果没有则从main_config.toml中读取配置进行初始化
    """
    logger.info("开始检查机器人配置...")

    async with admin_session() as session:
        # 检查数据库中是否已有机器人
        stmt = select(func.count(BotInfo.gewe_app_id))
        result = await session.execute(stmt)
        bot_count = result.scalar() or 0

        if bot_count > 0:
            logger.info(f"数据库中已存在 {bot_count} 个机器人，跳过配置文件初始化")
            return

        logger.info("数据库中没有机器人配置，开始从配置文件初始化...")

        # 从配置文件读取机器人配置
        config_data = _load_config_file()
        if not config_data:
            logger.warning("未找到有效的机器人配置，跳过初始化")
            return

        gewe_apps = config_data.get("gewe_apps", {})
        if not gewe_apps:
            logger.warning("配置文件中没有gewe_apps配置，跳过初始化")
            return

        # 初始化每个机器人配置
        initialized_count = 0
        for app_key, app_config in gewe_apps.items():
            try:
                success = await _create_bot_from_config(session, app_key, app_config)
                if success:
                    initialized_count += 1
            except Exception as e:
                logger.error(f"初始化机器人配置失败 {app_key}: {e}", exc_info=True)

        if initialized_count > 0:
            await session.commit()
            logger.info(f"成功从配置文件初始化了 {initialized_count} 个机器人")
        else:
            logger.warning("没有成功初始化任何机器人")


def _load_config_file() -> Dict[str, Any]:
    """加载配置文件"""
    # 查找配置文件
    config_paths = [
        "main_config.toml",
        "../main_config.toml",
        "../../main_config.toml",
        "../../../main_config.toml",
    ]

    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, "rb") as f:
                    config = tomllib.load(f)
                    logger.info(f"成功加载配置文件: {config_path}")
                    return config
            except Exception as e:
                logger.error(f"加载配置文件失败 {config_path}: {e}")
                continue

    logger.warning("未找到可用的配置文件")
    return {}


async def _create_bot_from_config(
    session: AsyncSession, app_key: str, app_config: Dict[str, Any]
) -> bool:
    """从配置创建机器人记录"""
    try:
        # 提取必需的配置
        app_id = app_config.get("app_id")
        token = app_config.get("token")
        base_url = app_config.get("base_url")
        name = app_config.get("name", f"机器人_{app_key}")

        if not app_id or not token:
            logger.warning(f"机器人配置 {app_key} 缺少必需的app_id或token，跳过")
            return False

        # 检查是否已存在相同的gewe_app_id
        stmt = select(BotInfo).where(BotInfo.gewe_app_id == app_id)
        result = await session.execute(stmt)
        existing_bot = result.scalar_one_or_none()

        if existing_bot:
            logger.info(f"机器人 {app_id} 已存在，跳过创建")
            return False

        # 创建机器人记录
        bot = BotInfo(
            gewe_app_id=app_id,
            gewe_token=token,
            nickname=name,
            base_url=base_url,
            callback_url_override=app_config.get("callback_url"),
            is_online=False,  # 初始状态为离线
        )

        session.add(bot)

        # 创建机器人专用数据库Schema
        try:
            schema_name = await session_manager.create_bot_schema(app_id)
            logger.info(f"机器人Schema创建成功: {schema_name}")
        except Exception as e:
            logger.error(f"创建机器人Schema失败 {app_id}: {e}")
            # Schema创建失败不影响机器人记录创建，后续可以重试

        logger.info(f"成功创建机器人配置: {app_id} ({name})")
        return True

    except Exception as e:
        logger.error(f"创建机器人配置失败 {app_key}: {e}", exc_info=True)
        return False


async def get_bot_configs_from_file() -> List[Dict[str, Any]]:
    """从配置文件获取机器人配置列表（用于其他地方调用）"""
    config_data = _load_config_file()
    if not config_data:
        return []

    gewe_apps = config_data.get("gewe_apps", {})
    configs = []

    for app_key, app_config in gewe_apps.items():
        if app_config.get("app_id") and app_config.get("token"):
            configs.append(
                {
                    "key": app_key,
                    "app_id": app_config.get("app_id"),
                    "token": app_config.get("token"),
                    "name": app_config.get("name", f"机器人_{app_key}"),
                    "callback_url": app_config.get("callback_url"),
                    "base_url": app_config.get("base_url"),
                    "is_gewe": app_config.get("is_gewe", True),
                }
            )

    return configs
