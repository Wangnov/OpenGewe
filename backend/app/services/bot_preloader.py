"""
Bot预加载服务

在应用启动时主动创建和初始化所有bot客户端，确保插件和定时任务立即生效
"""

from typing import Dict, Any
from sqlalchemy import select
from loguru import logger

from ..core.session_manager import admin_session
from .bot_manager import bot_manager
from ..models.bot import BotInfo


class BotPreloader:
    """Bot预加载服务"""

    def __init__(self):
        self._preload_completed = False

    async def preload_all_bots(self) -> Dict[str, Any]:
        """预加载所有配置的bot客户端"""
        if self._preload_completed:
            logger.debug("Bot预加载已完成，跳过重复执行")
            return {"status": "already_completed"}

        logger.info("开始预加载所有bot客户端...")

        try:
            # 获取所有配置的bot
            async with admin_session() as session:
                stmt = select(BotInfo)
                result = await session.execute(stmt)
                bots = result.scalars().all()

                if not bots:
                    logger.info("没有发现配置的bot，跳过预加载")
                    self._preload_completed = True
                    return {"status": "no_bots", "loaded_count": 0}

                logger.info(f"发现 {len(bots)} 个配置的bot，开始预加载...")

                # 预加载每个bot客户端
                loaded_count = 0
                failed_bots = []

                for bot in bots:
                    try:
                        logger.info(f"预加载bot客户端: {bot.gewe_app_id}")

                        # 主动创建客户端（这会触发插件加载和定时任务注册）
                        client = await bot_manager.get_client(bot.gewe_app_id, session)

                        if client:
                            loaded_count += 1
                            logger.info(f"成功预加载bot: {bot.gewe_app_id}")
                        else:
                            failed_bots.append(bot.gewe_app_id)
                            logger.warning(f"预加载bot失败: {bot.gewe_app_id}")

                    except Exception as e:
                        failed_bots.append(bot.gewe_app_id)
                        logger.error(
                            f"预加载bot {bot.gewe_app_id} 时出错: {e}", exc_info=True
                        )

                self._preload_completed = True

                result = {
                    "status": "completed",
                    "total_bots": len(bots),
                    "loaded_count": loaded_count,
                    "failed_count": len(failed_bots),
                    "failed_bots": failed_bots,
                }

                if failed_bots:
                    logger.warning(
                        f"Bot预加载完成，成功 {loaded_count}/{len(bots)} 个，失败的bot: {failed_bots}"
                    )
                else:
                    logger.info(
                        f"所有bot预加载完成，成功加载 {loaded_count} 个bot客户端"
                    )

                return result

        except Exception as e:
            logger.error(f"Bot预加载过程中发生异常: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}

    def is_preload_completed(self) -> bool:
        """检查预加载是否已完成"""
        return self._preload_completed

    async def get_preload_status(self) -> Dict[str, Any]:
        """获取预加载状态"""
        if not self._preload_completed:
            return {"status": "not_started"}

        # 获取当前已加载的客户端信息
        clients_info = {}
        for gewe_app_id in bot_manager._clients.keys():
            try:
                client = bot_manager._clients[gewe_app_id]
                clients_info[gewe_app_id] = {
                    "has_plugin_manager": hasattr(client, "plugin_manager"),
                    "plugin_count": len(client.plugin_manager.plugins)
                    if hasattr(client, "plugin_manager")
                    else 0,
                }
            except Exception as e:
                clients_info[gewe_app_id] = {"error": str(e)}

        return {
            "status": "completed",
            "loaded_clients": list(bot_manager._clients.keys()),
            "clients_info": clients_info,
        }


# 全局预加载服务实例
# 创建全局实例
bot_preloader = BotPreloader()
