import aiohttp
import asyncio
from typing import Optional
from opengewe.utils.plugin_base import PluginBase
from opengewe.utils.decorators import on_text_message, add_job_safe, scheduler
from opengewe.client import GeweClient
from opengewe.logger import get_logger
from opengewe.callback.models.text import TextMessage

logger = get_logger(__name__)


class DailyQuote(PluginBase):
    """每日一言插件"""
    description = "获取每日一言"
    author = "Roo"
    version = "1.0.0"

    def __init__(self, config: dict):
        super().__init__(config)
        plugin_config = self.config.get("DailyQuote", {})
        self.enable = plugin_config.get("enable", True)
        self.commands = plugin_config.get("commands", ["一言", "每日一言"])
        self.schedule_enable = plugin_config.get("schedule_enable", False)
        self.schedule_cron = plugin_config.get("schedule_cron", "0 8 * * *")
        self.schedule_chat_ids = plugin_config.get("schedule_chat_ids", [])
        logger.info("DailyQuote 插件已加载")

    async def async_init(self) -> None:
        """异步初始化，用于动态添加定时任务"""
        if self.schedule_enable and self.schedule_chat_ids:
            try:
                cron_parts = self.schedule_cron.split()
                if len(cron_parts) == 5:
                    minute, hour, day, month, day_of_week = cron_parts
                    job_id = f"daily_quote_{self.__class__.__name__}"

                    # 使用 add_job_safe 手动添加定时任务
                    add_job_safe(
                        scheduler,
                        job_id,
                        self._scheduled_quote,
                        self.client,  # client 实例在 on_enable 时被设置
                        trigger='cron',
                        minute=minute,
                        hour=hour,
                        day=day,
                        month=month,
                        day_of_week=day_of_week
                    )
                    logger.info(f"已成功添加每日一言定时任务，cron: '{self.schedule_cron}'")
                else:
                    logger.error(f"无效的 cron 表达式: {self.schedule_cron}")
            except Exception as e:
                logger.error(f"添加每日一言定时任务失败: {e}")

    async def _get_quote(self) -> Optional[str]:
        """从 API 获取一言"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://v1.hitokoto.cn/") as response:
                    if response.status == 200:
                        data = await response.json()
                        return f"{data['hitokoto']} —— {data['from']}"
                    else:
                        logger.error(f"获取一言失败，状态码: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"请求一言 API 时出错: {e}")
            return None

    async def _scheduled_quote(self, bot: GeweClient):
        """定时任务执行的方法"""
        logger.info("执行每日一言定时任务...")
        quote = await self._get_quote()
        if quote:
            for chat_id in self.schedule_chat_ids:
                try:
                    await bot.send_text_message(chat_id, quote)
                    await asyncio.sleep(1)  # 避免发送过快
                except Exception as e:
                    logger.error(f"向 {chat_id} 发送每日一言失败: {e}")

    @on_text_message(priority=50)
    async def handle_text(self, bot: GeweClient, message: TextMessage):
        if not self.enable:
            return True

        content = message.content.strip()

        if content in self.commands:
            quote = await self._get_quote()
            if quote:
                await bot.send_text_message(message.from_wxid, quote)
            else:
                await bot.send_text_message(message.from_wxid, "获取一言失败了，请稍后再试。")
            return False

        return True
