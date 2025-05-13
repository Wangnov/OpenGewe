import logging
import tomllib  # 确保导入tomllib以读取配置文件
import os  # 确保导入os模块
import traceback  # 添加缺失的traceback导入

from opengewe.utils.decorators import schedule
from opengewe.utils.plugin_base import PluginBase
from opengewe.utils.decorators import (
    on_text_message,
    on_at_message,
    on_voice_message,
    on_image_message,
    on_video_message,
    on_file_message,
    on_quote_message,
    on_pat_message,
    on_emoji_message,
)


class ExamplePlugin(PluginBase):
    """示例插件，展示如何使用装饰器和事件处理"""

    description = "示例插件"
    author = "Wangnov"
    version = "1.0.0"

    # 同步初始化
    def __init__(self):
        super().__init__()

        # 获取配置文件路径
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        try:
            with open(config_path, "rb") as f:
                config = tomllib.load(f)

            # 读取基本配置
            basic_config = config.get("basic", {})
            self.enable = basic_config.get("enable", False)  # 读取插件开关

        except Exception:
            logging.error(f"加载ExamplePlugin配置文件失败: {traceback.format_exc()}")
            self.enable = False  # 如果加载失败，禁用插件

    # 异步初始化
    async def async_init(self):
        logging.info("ExamplePlugin 异步初始化完成")
        return

    @on_text_message(priority=99)
    async def handle_text(self, client, message):
        if not self.enable:
            return  # 如果插件未启用，直接返回
        logging.info("收到了文本消息。")

    @on_at_message(priority=50)
    async def handle_at(self, client, message):
        if not self.enable:
            return
        logging.info("收到了被@消息，中等优先级")

    @on_voice_message()
    async def handle_voice(self, client, message):
        if not self.enable:
            return
        logging.info("收到了语音消息，最低优先级")

    @on_image_message
    async def handle_image(self, client, message):
        if not self.enable:
            return
        logging.info("收到了图片消息")

    @on_video_message
    async def handle_video(self, client, message):
        if not self.enable:
            return
        logging.info("收到了视频消息")

    @on_file_message
    async def handle_file(self, client, message):
        if not self.enable:
            return
        logging.info("收到了文件消息")

    @on_quote_message
    async def handle_quote(self, client, message):
        if not self.enable:
            return
        logging.info("收到了引用消息")

    @on_pat_message
    async def handle_pat(self, client, message):
        if not self.enable:
            return
        logging.info("收到了拍一拍消息")

    @on_emoji_message
    async def handle_emoji(self, client, message):
        if not self.enable:
            return
        logging.info("收到了表情消息")

    @schedule("interval", seconds=5)
    async def periodic_task(self, client):
        if not self.enable:
            return
        logging.info("我每5秒执行一次")

    @schedule("cron", hour=8, minute=30, second=30)
    async def daily_task(self, client):
        if not self.enable:
            return
        logging.info("我每天早上8点30分30秒执行")

    @schedule("date", run_date="2025-01-29 00:00:00")
    async def new_year_task(self, client):
        if not self.enable:
            return
        logging.info("我在2025年1月29日执行")
