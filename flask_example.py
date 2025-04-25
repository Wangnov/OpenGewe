"""
Flask服务器示例：使用opengewechat.message处理微信回调消息
"""

from flask import Flask, request, jsonify, send_from_directory
import logging
import os
from opengewechat import MessageFactory, GewechatClient, MessageType

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
app_id = "wx_s-dMlUFNk56cmVraJ59Q6"
token = "e534251fa40b4981adf611d73f48ccac"

# 创建 GewechatClient 实例
client = GewechatClient(
    base_url,
    download_url,
    callback_url,
    app_id,
    token,
)
# 创建消息工厂，设置线程池大小
factory = MessageFactory(client, max_workers=20)

# 方法2：从目录加载外部插件
# 确保plugins目录存在
if os.path.exists("./plugins"):
    plugins = factory.load_plugins_from_directory("./plugins")
    logger.info(f"从外部目录加载了 {len(plugins)} 个插件")

# 启用所有插件
for plugin in factory.get_all_plugins():
    factory.enable_plugin(plugin.name)


def on_message(message):
    # 获取message对象的所有属性
    attrs = [
        attr
        for attr in dir(message)
        if not attr.startswith("_")
        # and attr != "raw_data"
        and attr != "from_dict"
    ]
    # 构建属性信息字符串
    attr_info = []
    for attr in attrs:
        try:
            value = getattr(message, attr)
            attr_info.append(f"{attr}={value}")
        except Exception as e:
            attr_info.append(f"{attr}=<获取失败: {str(e)}>")
    # 打印所有属性信息
    logger.info(f"收到{message.type.name}消息: {', '.join(attr_info)}")

    if message.type == MessageType.TEXT:
        if message.text == "测试":
            client.message.send_text(message.from_user, "测试成功")

        if message.text == "语音":
            result = client.utils.convert_audio_to_silk(
                "/root/opengewechat/downloads/test.wav",
                "/root/opengewechat/downloads",
            )
            print(result)
            client.message.send_voice(
                message.from_user,
                "http://14.103.138.115:5432/download/test.silk",
                result["duration"],
            )


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

        # 异步处理消息，立即返回响应，不阻塞HTTP请求
        factory.process_async(data)

        # 直接返回成功，异步处理消息不会影响响应速度
        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.exception(f"处理回调消息时出错: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):
    """
    文件下载接口
    支持两种方式：
    1. /download/文件名 - 直接通过URL路径下载
    2. /download?file=文件名 - 通过查询参数下载
    """
    # 检查是否通过查询参数传递文件名
    query_filename = request.args.get("file")
    target_filename = query_filename if query_filename else filename

    if not target_filename:
        return jsonify({"status": "error", "message": "文件路径不能为空"}), 400

    # 安全检查：防止路径遍历攻击
    if ".." in target_filename or target_filename.startswith("/"):
        return jsonify({"status": "error", "message": "非法的文件路径"}), 403

    download_dir = "./downloads"
    file_path = os.path.join(download_dir, target_filename)

    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return jsonify({"status": "error", "message": "文件不存在"}), 404

    # 设置自定义文件名（如果提供）
    custom_filename = request.args.get("filename")
    if custom_filename:
        return send_from_directory(
            download_dir,
            target_filename,
            as_attachment=True,
            download_name=custom_filename,
        )

    # 正常下载文件
    return send_from_directory(download_dir, target_filename)


# 保留原有的接口以保持兼容性
@app.route("/download", methods=["GET"])
def download():
    """下载接口,下载downloads文件夹内的内容，例如/download?file=test.wav就会下载test.wav文件"""
    return download_file("")


@app.route("/status", methods=["GET"])
def status():
    """健康检查接口"""
    return jsonify({"status": "running"})


if __name__ == "__main__":
    logger.info("启动Gewechat回调服务器...")
    app.run(host="0.0.0.0", port=5432, debug=True)
