# OpenGeWechat

![Logo](https://github.com/Devo919/Gewechat/raw/main/logo.png)

> 基于Gewechat和Gewe的开源微信机器人框架，提供简单易用的微信自动化解决方案

## 项目状态

⚠️ **注意：由于[Gewechat](https://github.com/Devo919/Gewechat)原项目暂停维护，本项目目前也处于暂停状态。**

## 简介

OpenGeWechat是一个基于[Gewechat](https://github.com/Devo919/Gewechat)的微信机器人框架，专注于提供个人微信二次开发能力。本框架采用微信iPad协议登录（非HOOK破解桌面端），提供稳定、安全的微信API访问能力。

## 主要特性

- ‼️ **消息回调**：完全实现Gewechat31种回调消息类型的检测
- 💬 **消息收发**：支持文本、图片、语音、视频等多种消息类型
- 👥 **群管理**：自动入群、退群、邀请好友、群成员管理等
- 🤖 **自动回复**：设置关键词自动回复，支持正则表达式
- 🔌 **插件系统**：可扩展的插件架构，轻松开发自定义功能
- 🔄 **API集成**：提供RESTful API，方便与其他系统集成
- 📊 **数据分析**：消息记录分析，用户行为统计等功能
- 📱 **朋友圈操作(Gewe)**：支持发布朋友圈内容、浏览朋友圈等
- 💾 **收藏管理**：微信收藏内容的获取与管理
- 📺 **视频号交互(Gewe)**：支持视频号相关的操作

## 兼容性说明

本项目完全兼容Gewechat付费版本[Gewe](https://geweapi.com)。由于原项目暂停维护，我们建议用户转向使用Gewe以获得持续的支持和更新。使用Gewe API只需修改`base_url`为：`http://api.geweapi.com/gewe/v2/api`，系统会自动识别并切换到付费版模式。

## 迁移到Gewe

如果您希望继续使用本项目的功能，可以按照以下步骤迁移到Gewe:

1. 访问[Gewe官方网站](https://geweapi.com)注册账号
2. 获取Gewe的API密钥
3. 在配置中将`base_url`修改为Gewe API地址：`http://api.geweapi.com/gewe/v2/api`
4. 使用Gewe提供的token和其他凭据

## 安装与使用

### 环境要求

- Python 3.11+

### 安装步骤

```bash
# 克隆项目
git clone https://github.com/yourusername/opengewechat.git

# 进入项目目录
cd opengewechat

# 安装依赖
pip install -r requirements.txt

# 或者使用pip直接安装(无效，暂未上传到PYPI)
pip install opengewechat
```

### 基本使用

```python
from opengewechat import GewechatClient

# 创建客户端实例
client = GewechatClient(
    base_url="http://your_gewechat_server:2531/v2/api",  # Gewechat服务的基础URL
    download_url="http://your_gewechat_server:2532/download",  # 下载链接的基础URL
    callback_url="http://your_callback_server/callback",  # 回调服务器URL
    app_id="",  # 首次登录传空，后续登录使用登录成功后返回的app_id
    token="",  # 首次登录传空，后续登录使用登录成功后返回的token
)

# 执行登录流程
client.start_login()

# 发送文本消息
client.message.send_text("filehelper", "你好，这是一条测试消息")

# 获取通讯录列表
contacts = client.contact.get_contact_list()
```

也可以使用login.py作为示例登录

### 消息回调

使用flask_example.py作为示例回调服务器

也可以自行搭建其他回调服务器

### 使用付费版Gewe

```python
from opengewechat import GewechatClient

# 创建Gewe客户端实例
client = GewechatClient(
    base_url="http://api.geweapi.com/gewe/v2/api",  # Gewe API地址
    download_url="",  # Gewe无需传入下载链接头
    callback_url="http://your_callback_server/callback",  # 您的回调服务器
    app_id="your_app_id",  # Gewe提供的app_id
    token="your_token",  # Gewe提供的token
    debug=False  
)

# 使用方式与开源版本相同
```

## 插件开发

OpenGeWechat提供了强大的插件系统，您可以通过继承`BasePlugin`类来创建自定义插件：

```python
from opengewechat.plugins import BasePlugin

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__(
            name="my_plugin",
            description="My custom plugin",
            version="1.0.0",
            author="Your Name"
        )
    
    def on_message(self, message):
        if "hello" in message.content:
            message.reply("Hello from my plugin!")

# 注册插件
from opengewechat.plugins import PluginManager
PluginManager.register_plugin(MyPlugin())
```

## 模块说明

OpenGeWechat包含以下核心模块：

- **login**: 登录相关功能
- **contact**: 通讯录管理
- **group**: 群聊管理
- **message**: 消息收发
- **tag**: 标签管理
- **personal**: 个人信息管理
- **favorite**: 收藏功能
- **account**: 账号管理
- **sns**: 朋友圈功能
- **finder**: 视频号功能

## 贡献指南

由于项目暂停维护，我们目前不接受新的贡献请求。但您可以Fork本项目进行个人修改和改进。

## 致谢

- 特别感谢[Gewechat](https://github.com/Devo919/Gewechat)项目及其开发者提供的基础框架
- 感谢所有对本项目提供支持和反馈的用户

## 许可证

本项目采用[MIT LICENSE](LICENSE)。

## 免责声明

本项目仅供学习研究使用，请勿用于非法用途。使用本项目导致的任何问题与开发者无关。请遵守微信使用条款和相关法律法规。
