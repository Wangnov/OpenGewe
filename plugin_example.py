"""插件系统示例

此脚本展示了如何使用opengewechat的插件系统。
"""

import logging
import os
from flask import Flask, request, jsonify

from opengewechat import GewechatClient, MessageFactory, BasePlugin
from opengewechat.message.models import BaseMessage, TextMessage
from opengewechat.message.types import MessageType

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 创建Gewechat客户端
# 请替换为你自己的配置
client = GewechatClient(
    base_url="http://你的Gewechat镜像IP:2531/v2/api",
    download_url="http://你的Gewechat镜像IP:2532/download",
    callback_url="http://你的回调服务器IP:5000/callback",
    app_id="",  # 首次登录留空
    token="",  # 首次登录留空
    debug=True,  # 是否开启调试模式
)

# 创建消息工厂
factory = MessageFactory(client)


# 自定义一个天气插件示例
class WeatherPlugin(BasePlugin):
    """天气插件

    当收到文本消息"天气 城市名"时，返回该城市的天气信息。
    """

    def __init__(self, client=None):
        super().__init__(client)
        self.name = "WeatherPlugin"
        self.description = (
            "天气插件，当收到文本消息'天气 城市名'时，返回该城市的天气信息"
        )
        self.version = "0.1.0"

    def can_handle(self, message: BaseMessage) -> bool:
        if message.type != MessageType.TEXT:
            return False

        if not isinstance(message, TextMessage):
            return False

        return message.content.startswith("天气 ")

    def handle(self, message: BaseMessage) -> None:
        if not self.client:
            return

        # 获取城市名
        city = message.content.replace("天气 ", "").strip()

        # 这里应该调用天气API获取实际天气信息
        # 出于演示目的，我们直接返回固定消息
        weather_info = f"{city}今天天气晴朗，温度25-30℃，适合出行。"

        # 文本消息的接收者可能是群聊或个人
        to_wxid = message.room_wxid if message.room_wxid else message.wxid

        # 发送回复
        self.client.message.send_text(to_wxid, weather_info)


# 加载并启用插件
def setup_plugins():
    # 方法1：直接加载内置插件类
    factory.load_plugin(WeatherPlugin)

    # 方法2：从目录加载外部插件
    # 确保plugins目录存在
    if os.path.exists("./plugins"):
        plugins = factory.load_plugins_from_directory("./plugins")
        logger.info(f"从外部目录加载了 {len(plugins)} 个插件")

    # 启用所有插件
    for plugin in factory.get_all_plugins():
        factory.enable_plugin(plugin.name)
        logger.info(f"已加载并启用插件: {plugin}")


# 消息回调函数
def message_callback(message: BaseMessage):
    """消息回调函数

    当收到消息时，此函数会被调用。

    Args:
        message: 消息对象
    """
    logger.info(f"收到消息: {message}")


# 注册消息回调
factory.register_callback(message_callback)


# 回调接口
@app.route("/callback", methods=["POST"])
def callback():
    """Gewechat回调接口

    接收Gewechat发来的消息，并交给消息工厂处理。
    """
    data = request.json
    factory.process_async(data)
    return jsonify({"status": "success"})


if __name__ == "__main__":
    # 执行登录流程
    client.start_login()

    # 设置插件
    setup_plugins()

    # 启动Flask应用
    app.run(host="0.0.0.0", port=5000)
