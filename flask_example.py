"""
Flask服务器示例
"""

from flask import Flask, request, jsonify, send_from_directory
import logging
import os
import shutil
import tomllib
from opengewechat import MessageFactory, GewechatClient, MessageType

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 验证main_config.toml配置文件是否存在，如果不存在则复制main_config_example.toml文件到当前目录
if not os.path.exists("main_config.toml"):
    logger.error("main_config.toml配置文件不存在，请检查文件是否存在")
    shutil.copy("main_config_example.toml", "main_config.toml")
    logger.info(
        "已复制main_config_example.toml文件到当前目录，请修改main_config.toml文件后重新启动"
    )
    exit(1)

# 从main_config.toml配置文件中读取配置参数，参数配置的说明详见main_config.toml文件中的说明
with open("main_config.toml", "rb") as f:
    config = tomllib.load(f)

base_url = config["gewe"]["base_url"]
download_url = config["gewe"]["download_url"]
callback_url = config["gewe"]["callback_url"]
app_id = config["gewe"]["app_id"]
token = config["gewe"]["token"]
is_gewe = config["gewe"]["is_gewe"]
# 创建 GewechatClient 实例
client = GewechatClient(
    base_url, download_url, callback_url, app_id, token, is_gewe=is_gewe
)
# 创建消息工厂，设置线程池大小
factory = MessageFactory(client, max_workers=20)

# 获取所有已加载的内置插件名称列表，避免重复加载
loaded_plugin_names = [p.name for p in factory.get_all_plugins()]
logger.info(f"已加载的内置插件: {loaded_plugin_names}")

# # 方法2：从目录加载外部插件（避免重复加载内置插件）
# if os.path.exists("./plugins"):
#     # 只加载不在已加载列表中的外部插件
#     plugins = factory.load_plugins_from_directory("./plugins")

#     # 计算新加载的插件数量
#     new_plugin_names = [p.name for p in plugins if p.name not in loaded_plugin_names]
#     logger.info(
#         f"从外部目录加载了 {len(new_plugin_names)} 个新插件: {new_plugin_names}"
#     )

# 启用所有插件
for plugin in factory.get_all_plugins():
    factory.enable_plugin(plugin.name)


# 消息回调函数
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
    logger.info(
        f"收到 {'群' if message.is_group_message else '好友'} {message.type.name} 消息: {', '.join(attr_info)}"
    )

    if message.type == MessageType.TEXT:
        if message.text == "测试":
            client.message.send_text(message.from_wxid, "测试成功")

        if message.text == "语音":
            result = client.utils.convert_audio_to_silk(
                "/root/opengewechat/downloads/test.wav",
                "/root/opengewechat/downloads",
            )
            print(result)
            client.message.send_voice(
                message.from_wxid,
                "http://ip:5432/download/test.silk",
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
