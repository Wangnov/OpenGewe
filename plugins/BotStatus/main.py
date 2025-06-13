from opengewe.utils.plugin_base import PluginBase
from opengewe.utils.decorators import on_text_message, on_at_message
from opengewe.client import GeweClient
from opengewe.logger import get_logger
from opengewe.callback.models.text import TextMessage
import re

logger = get_logger(__name__)


class BotStatus(PluginBase):
    """一个简单的插件，用于响应机器人的状态查询"""
    description = "机器人状态查询插件"
    author = "Roo"
    version = "1.0.0"

    def __init__(self, config: dict):
        super().__init__(config)
        # 从注入的配置中读取设置
        plugin_config = self.config.get("BotStatus", {})
        self.enable = plugin_config.get("enable", True)
        self.commands = plugin_config.get("commands", ["status", "bot"])
        self.status_message = plugin_config.get(
            "status_message", "Bot is running.")
        logger.info("BotStatus 插件已加载")

    async def _send_status_message(self, bot: GeweClient, message: TextMessage):
        """发送状态消息"""
        # 这里的 self.version 来自 PluginBase
        out_message = (
            f"{self.status_message}\n"
            f"Plugin Version: {self.version}\n"
            "Project: OpenGewe"
        )

        if message.is_group_message:
            await bot.send_at_message(message.from_wxid, f"\n{out_message}", [message.sender_wxid])
        else:
            await bot.send_text_message(message.from_wxid, out_message)

    @on_text_message(priority=50)
    async def handle_text(self, bot: GeweClient, message: TextMessage):
        if not self.enable:
            return True

        content = message.content.strip()
        command = content.split(" ")[0]

        if command in self.commands:
            await self._send_status_message(bot, message)
            return False

        return True

    @on_at_message(priority=50)
    async def handle_at(self, bot: GeweClient, message: TextMessage):
        if not self.enable:
            return True

        content = message.content.strip()
        # 简单处理，移除@xxx部分
        command = re.split(r'[\s\u2005]+', content)

        if len(command) > 1 and command[1] in self.commands:
            await self._send_status_message(bot, message)
            return False

        return True
