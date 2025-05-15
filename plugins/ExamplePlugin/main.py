import tomllib
import os
import traceback
from loguru import logger
from datetime import datetime

from utils.plugin_base import PluginBase
from utils.decorators import (
    on_text_message,
    on_at_message,
    on_voice_message,
    on_image_message,
    on_video_message,
    on_file_message,
    on_quote_message,
    on_pat_message,
    on_emoji_message,
    schedule,
)


class ExamplePlugin(PluginBase):
    """示例插件，展示如何使用装饰器和事件处理"""

    description = "示例插件"
    author = "Wangnov"
    version = "1.0.0"

    # 同步初始化
    def __init__(self):
        super().__init__()

        # 默认启用插件，即使读取配置文件失败
        self.enable = True

        # 获取配置文件路径
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        try:
            with open(config_path, "rb") as f:
                config = tomllib.load(f)

            # 读取基本配置
            basic_config = config.get("basic", {})
            config_enable = basic_config.get("enable", True)  # 默认为True

            self.enable = config_enable

        except Exception as e:
            logger.error(f"加载ExamplePlugin配置文件失败: {e}")
            logger.error(traceback.format_exc())
            # 如果配置文件读取失败，仍然启用插件
            self.enable = True
            logger.warning("配置读取失败，默认启用插件")

    # 异步初始化
    async def async_init(self):
        logger.info("ExamplePlugin 异步初始化完成")
        logger.info(f"当前插件状态: {'启用' if self.enable else '禁用'}")
        return

    @on_text_message(priority=99)
    async def handle_text(self, client, message):
        if not self.enable:
            logger.debug("插件已禁用，忽略文本消息")
            return  # 如果插件未启用，直接返回

        try:
            logger.info(f"收到了文本消息。消息对象: {message}")
            # 这里可以添加具体的消息处理逻辑
        except Exception as e:
            logger.error(f"处理文本消息时出错: {e}")
            logger.error(traceback.format_exc())

    @on_at_message(priority=50)
    async def handle_at(self, client, message):
        if not self.enable:
            return
        try:
            logger.info(
                f"收到了被@消息，中等优先级。消息内容: {message.content if hasattr(message, 'content') else '无内容'}"
            )
        except Exception as e:
            logger.error(f"处理@消息时出错: {e}")
            logger.error(traceback.format_exc())

    @on_voice_message()
    async def handle_voice(self, client, message):
        if not self.enable:
            return
        logger.info("收到了语音消息，最低优先级")

    @on_image_message
    async def handle_image(self, client, message):
        if not self.enable:
            return
        logger.info("收到了图片消息")

    @on_video_message
    async def handle_video(self, client, message):
        if not self.enable:
            return
        logger.info("收到了视频消息")

    @on_file_message
    async def handle_file(self, client, message):
        if not self.enable:
            return
        logger.info("收到了文件消息")

    @on_quote_message
    async def handle_quote(self, client, message):
        if not self.enable:
            return
        logger.info("收到了引用消息")

    @on_pat_message
    async def handle_pat(self, client, message):
        if not self.enable:
            return
        logger.info("收到了拍一拍消息")

    @on_emoji_message
    async def handle_emoji(self, client, message):
        if not self.enable:
            return
        logger.info("收到了表情消息")

    @schedule("interval", seconds=5)
    async def periodic_task(self, client):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not self.enable:
            logger.debug(f"[{current_time}] 插件已禁用，跳过定时任务")
            return
        try:
            logger.info(f"[{current_time}] 我每5秒执行一次")
        except Exception as e:
            logger.error(f"执行定时任务出错: {e}")
            logger.error(traceback.format_exc())

    @schedule("cron", hour=8, minute=30, second=30)
    async def daily_task(self, client):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not self.enable:
            logger.debug(f"[{current_time}] 插件已禁用，跳过每日任务")
            return
        try:
            logger.info(f"[{current_time}] 我每天早上8点30分30秒执行")
        except Exception as e:
            logger.error(f"执行每日任务出错: {e}")
            logger.error(traceback.format_exc())

    @schedule("date", run_date="2025-05-15 16:54:00")
    async def new_year_task(self, client):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not self.enable:
            logger.debug(f"[{current_time}] 插件已禁用，跳过指定日期任务")
            return
        try:
            logger.info(f"[{current_time}] 我在执行指定日期任务")
        except Exception as e:
            logger.error(f"执行指定日期任务出错: {e}")
            logger.error(traceback.format_exc())
