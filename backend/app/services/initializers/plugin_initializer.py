"""
插件初始化服务

负责在应用启动时检查并初始化插件配置
"""

from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from ...core.session_manager import admin_session, session_manager
from ..bot_manager import bot_manager
from ...models.admin import GlobalPlugin
from ...models.bot import BotInfo, BotPlugin
from opengewe.logger import init_default_logger, get_logger

init_default_logger()
logger = get_logger(__name__)


async def initialize_plugins() -> None:
    """
    初始化插件配置

    检查所有可用插件，为它们创建数据库配置记录
    """
    logger.info("开始初始化插件配置...")

    # 先加载可用插件
    await bot_manager._load_available_plugins()
    available_plugins = bot_manager.get_available_plugins()

    if not available_plugins:
        logger.info("没有发现可用插件")
        return

    logger.info(f"发现 {len(available_plugins)} 个可用插件: {available_plugins}")

    async with admin_session() as session:
        # 初始化全局插件配置
        await _initialize_global_plugins(session, available_plugins)

        # 初始化机器人插件配置
        await _initialize_bot_plugins(session, available_plugins)

        await session.commit()

    logger.info("插件配置初始化完成")


async def _initialize_global_plugins(
    session: AsyncSession, available_plugins: List[str]
) -> None:
    """初始化全局插件配置"""
    logger.info("初始化全局插件配置...")

    for plugin_name in available_plugins:
        # 检查是否已存在全局配置
        stmt = select(GlobalPlugin).where(GlobalPlugin.plugin_name == plugin_name)
        result = await session.execute(stmt)
        existing_plugin = result.scalar_one_or_none()

        if not existing_plugin:
            # 创建新的全局插件配置
            global_plugin = GlobalPlugin(
                plugin_name=plugin_name,
                is_globally_enabled=True,  # 默认启用
                global_config_json=None,
            )
            session.add(global_plugin)
            logger.info(f"创建全局插件配置: {plugin_name}")
        else:
            logger.debug(f"全局插件配置已存在: {plugin_name}")


async def _initialize_bot_plugins(
    session: AsyncSession, available_plugins: List[str]
) -> None:
    """为所有机器人初始化插件配置"""
    logger.info("初始化机器人插件配置...")

    # 获取所有机器人
    stmt = select(BotInfo)
    result = await session.execute(stmt)
    bots = result.scalars().all()

    if not bots:
        logger.info("没有发现机器人，跳过机器人插件配置初始化")
        return

    for bot in bots:
        logger.info(f"为机器人 {bot.gewe_app_id} 初始化插件配置...")

        # 使用机器人专用会话
        async with session_manager.get_bot_session(bot.gewe_app_id) as bot_session:
            for plugin_name in available_plugins:
                # 检查是否已存在机器人插件配置
                stmt = select(BotPlugin).where(
                    and_(
                        BotPlugin.gewe_app_id == bot.gewe_app_id,
                        BotPlugin.plugin_name == plugin_name,
                    )
                )
                result = await bot_session.execute(stmt)
                existing_bot_plugin = result.scalar_one_or_none()

                if not existing_bot_plugin:
                    # 创建新的机器人插件配置
                    bot_plugin = BotPlugin(
                        gewe_app_id=bot.gewe_app_id,
                        plugin_name=plugin_name,
                        is_enabled=True,  # 默认启用
                        config_json=None,
                    )
                    bot_session.add(bot_plugin)
                    logger.info(
                        f"为机器人 {bot.gewe_app_id} 创建插件配置: {plugin_name}"
                    )
                else:
                    logger.debug(
                        f"机器人 {bot.gewe_app_id} 的插件配置已存在: {plugin_name}"
                    )

            await bot_session.commit()


async def get_plugin_status() -> Dict[str, Any]:
    """获取插件状态信息"""
    try:
        # 加载可用插件
        await bot_manager._load_available_plugins()
        available_plugins = bot_manager.get_available_plugins()

        async with admin_session() as session:
            # 获取全局插件配置
            global_stmt = select(GlobalPlugin)
            global_result = await session.execute(global_stmt)
            global_plugins = {
                plugin.plugin_name: plugin.is_globally_enabled
                for plugin in global_result.scalars().all()
            }

            # 获取机器人信息
            bot_stmt = select(BotInfo)
            bot_result = await session.execute(bot_stmt)
            bots = bot_result.scalars().all()

            bot_plugin_status = {}
            for bot in bots:
                async with session_manager.get_bot_session(
                    bot.gewe_app_id
                ) as bot_session:
                    bot_plugin_stmt = select(BotPlugin).where(
                        BotPlugin.gewe_app_id == bot.gewe_app_id
                    )
                    bot_plugin_result = await bot_session.execute(bot_plugin_stmt)
                    bot_plugins = {
                        plugin.plugin_name: plugin.is_enabled
                        for plugin in bot_plugin_result.scalars().all()
                    }
                    bot_plugin_status[bot.gewe_app_id] = bot_plugins

            return {
                "available_plugins": available_plugins,
                "global_plugins": global_plugins,
                "bot_plugins": bot_plugin_status,
                "summary": {
                    "total_available": len(available_plugins),
                    "total_global_enabled": sum(global_plugins.values()),
                    "total_bots": len(bots),
                },
            }

    except Exception as e:
        logger.error(f"获取插件状态失败: {e}", exc_info=True)
        return {"error": str(e)}
