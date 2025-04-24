"""
Flask服务器示例：使用opengewechat.message处理微信回调消息
"""

from flask import Flask, request, jsonify
import logging
from opengewechat.message import MessageFactory, MessageType
from opengewechat.client import GewechatClient

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 配置参数
base_url = "http://14.103.138.115:2531/v2/api"
download_url = "http://14.103.138.115:2532/download"
callback_url = "http://14.103.138.115:5432/callback"
app_id = "wx_cwP_BogkA4zaHyP8k5aEt"
token = "cd3382cb2e5145128db30342df28a6a5"
# 创建 GewechatClient 实例
client = GewechatClient(
    base_url,
    download_url,
    callback_url,
    app_id,
    token,
)
# 创建消息工厂
factory = MessageFactory(client)


# 消息处理回调函数
def on_message(message):
    """处理所有类型的消息"""
    logger.info(
        f"收到消息: 类型={message.type.name}, 发送者={message.from_user}, 接收者={message.to_user}, RAW消息内容={message.raw_data}"
    )

    # 根据消息类型做不同处理
    if message.type == MessageType.TEXT:
        logger.info(f"文本内容: {message.text}")
        # 这里可以添加更多处理逻辑，如关键词回复等
    elif message.type == MessageType.EMOJI:
        logger.info(f"表情内容: {message.emoji_md5}")
    elif message.type == MessageType.IMAGE:
        logger.info(f"图片下载链接: {message.img_download_url}")
        # 可以进一步处理图片，如保存到本地、转发等

    elif message.type == MessageType.VOICE:
        logger.info(
            f"语音长度: {message.voice_length}ms, 下载链接: {message.voice_url}"
        )

    elif message.type == MessageType.FILE:
        logger.info("收到文件消息")
        # 处理文件消息

    elif message.type == MessageType.GROUP_RENAME:
        logger.info("群名称被修改")
        # 记录群名称变更

    elif message.type == MessageType.OFFLINE:
        logger.warning("微信账号掉线，wxid={message.wxid}")
        # 可以发送通知给管理员


# 注册消息回调
factory.register_callback(on_message)


@app.route("/callback", methods=["POST"])
def webhook():
    """微信回调接口"""
    try:
        # 获取JSON数据
        data = request.get_json()

        if not data:
            logger.error("接收到无效的请求数据")
            return jsonify({"status": "error", "message": "无效的请求数据"}), 400

        # 处理消息
        message = factory.process(data)

        if not message:
            logger.warning(f"无法识别的消息类型: {data.get('TypeName')}")

        # 返回成功，避免微信重试
        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.exception(f"处理回调消息时出错: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    """健康检查接口"""
    return jsonify({"status": "running"})


if __name__ == "__main__":
    logger.info("启动Gewechat回调服务器...")
    app.run(host="0.0.0.0", port=5432, debug=True)
