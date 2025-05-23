# OpenGewe

![版本](https://img.shields.io/badge/版本-0.1.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-brightgreen)
![协议](https://img.shields.io/badge/协议-MIT-green)

> 基于 GeWeAPI 和 GeWe 私有部署方案的异步 Python 微信机器人框架，提供高性能的微信自动化解决方案

## 简介

OpenGewe 是一个基于 [GeWeAPI](https://geweapi.com) 的微信机器人框架，专注于提供个人微信二次开发能力。本框架采用微信iPad协议登录，提供稳定、安全的微信API访问能力。


## 主要特性

- 🚀 **完全异步** - 使用原生 asyncio 实现，支持高并发和大数据量处理
- 📨 **全面消息处理** - 实现所有31种回调消息类型的处理
- 💬 **多媒体支持** - 支持文本、图片、语音、视频等多种消息类型
- 👥 **完整群管理** - 自动入群、退群、邀请好友、群成员管理等
- 🔌 **插件系统** - 可扩展的插件架构，支持动态加载/卸载插件
- 🔄 **API集成** - 提供RESTful API，方便与其他系统集成
- 📊 **消息队列** - 支持简单队列和高级队列（Celery）两种消息处理模式
- 📱 **朋友圈操作** - 支持发布朋友圈内容、浏览朋友圈等
- 🎵 **视频号交互** - 支持视频号相关的操作

## 兼容性说明

⚠️ **注意：由于原免费私有部署方案[Gewechat](https://github.com/Devo919/Gewechat)原项目暂停维护，本项目虽然兼容Gewechat，但不推荐使用。**

本项目**计划**完全兼容Gewechat付费版本[GeWeAPI](https://geweapi.com)。由于原项目暂停维护，我们建议用户转向使用GeWeAPI以获得持续的支持和更新。使用GeWeAPI只需修改`base_url`为：`http://www.geweapi.com/gewe/v2/api`，系统会自动识别并切换到付费版模式。

## 迁移到GeWeAPI

如果您希望继续使用本项目的功能，可以按照以下步骤迁移到GeWeAPI:

1. 访问[GeWeAPI官方网站](https://geweapi.com)注册账号
2. 获取GeWeAPI的token
3. 在配置中将`base_url`修改为Gewe API地址：`http://www.geweapi.com/gewe/v2/api` 或备用地址（GeWeAPI管理后台中显示的）
4. 在GeWeAPI管理后台中扫码登录微信账号，获得app_id
5. 在GeWeAPI管理后台中对此token设置回调服务器的地址

## 安装

### 从PyPI安装

```bash
pip install opengewe
```

### 从源码安装

```bash
git clone https://github.com/Wangnov/OpenGewe.git
cd OpenGewe
pip install -e .
```

## 快速开始

### 基本使用

```python
import asyncio
from opengewe import GeweClient

async def main():
    # 创建客户端实例
    client = GeweClient(
        base_url="http://www.geweapi.com/gewe/v2/api",  # GeWeAPI服务的基础URL，GeWe服务器只要没有问题就不会变化。极少数情况下可能会变化，可在GeWeAPI管理后台查看最新的base_url
        download_url="",  # 使用GeWeAPI无需填写
        callback_url="",  # 在GeWeAPI设置回调服务器URL，此处无需设置
        app_id="your_app_id",  # 在GeWeAPI登录成功后返回的app_id
        token="your_token",  # 在GeWeAPI创建的token
        is_gewe=True,  # 使用付费版GeWeAPI
    )
    
    # 发送文本消息
    await client.send_text("filehelper", "你好，这是一条测试消息")
    
    # 获取通讯录列表
    contacts = await client.contact.get_contact_list()
    
    # 关闭客户端
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 配置文件

OpenGewe 使用 TOML 格式的配置文件，默认为 `main_config.toml`：

```toml
[gewe_apps]
# 多设备配置
[gewe_apps.1]
name = "默认设备"
base_url = "http://www.geweapi.com/gewe/v2/api"
app_id = "your_app_id"
token = "your_token"
is_gewe = true

[plugins]
plugins_dir = "plugins"
enabled_plugins = ["ExamplePlugin"]

[queue]
queue_type = "simple"  # 可选 "simple" 或 "advanced"

[logging]
level = "INFO"
format = "color"
path = "./logs"
stdout = true
```

### 命令行工具

OpenGewe提供了一个简单的命令行工具，可以通过以下方式启动：

```bash
# 显示版本信息
opengewe version

# 启动客户端（使用配置文件中的设置）
opengewe client --config main_config.toml --device 1
```

## 插件开发

创建一个自定义插件：

1. 在 `plugins` 目录下创建插件文件夹
2. 编写插件主类，继承 `PluginBase`
3. 可以使用装饰器注册消息处理和定时任务，也可以直接引入opengewe的handler模块来注册消息处理
4. 在配置文件中启用插件
5. 可以以兼容XYBot和XXXBot的插件格式来编写

示例插件：

```python
from utils.plugin_base import PluginBase
from utils.decorators import on_text_message, schedule

class MyPlugin(PluginBase):
    """自定义插件示例"""
    
    description = "这是我的第一个插件"
    author = "您的名字"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.enable = True
        
    @on_text_message()
    async def handle_text(self, client, message):
        if message.text == "你好":
            await client.send_text(message.from_wxid, "你好！我是OpenGewe机器人")
    
    @schedule("interval", minutes=30)
    async def periodic_task(self, client):
        # 执行定期任务的代码
        pass
```

## 模块说明

OpenGewe包含以下核心模块：

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

可以Fork本项目进行修改和改进

## 致谢

- 特别感谢[Gewechat](https://github.com/Devo919/Gewechat)项目的开源精神
- 感谢[XYBot](https://github.com/HenryXiaoYang/XYBotV2)项目的异步实现给本项目以启发
- 感谢[XXXBot](https://github.com/NanSsye/xxxbot-pad)项目的管理后台前端实现给本项目以启发，和丰富的插件开发生态
- 感谢所有对本项目提供支持和反馈的用户

## 许可证

本项目采用 [MIT 许可证](LICENSE)

## 免责声明

本项目仅供学习研究使用，请勿用于非法用途。使用本项目导致的任何问题与开发者无关。请遵守微信使用条款和相关法律法规。

## 联系方式

有问题或建议？请在GitHub上提交Issue或Pull Request。
