# OpenGewe

![版本](https://img.shields.io/badge/版本-0.2.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-brightgreen)
![协议](https://img.shields.io/badge/协议-MIT-green)

> 基于 GeWeAPI 和 GeWe 私有部署方案的异步 Python 微信机器人框架，提供高性能的微信自动化解决方案

## 简介

OpenGewe 是一个基于 [GeWeAPI](https://geweapi.com) 的微信机器人框架，专注于提供个人微信二次开发能力。本框架采用微信iPad协议登录，提供稳定、安全的微信API访问能力。

**请注意：** 项目配套的前后端管理面板仍在积极开发中，将在未来的版本中提供。


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
- 📦 **轻量化安装** - 支持基础和完整两种安装方式，按需选择功能

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

OpenGewe 提供两种安装方式，您可以根据自己的需求选择：

### 🔸 基础安装（推荐给大多数用户）

适合只需要基础功能的用户，安装包更小，依赖更少：

```bash
# 使用 pip 安装基础版本
pip install opengewe

# 或从源码安装基础功能
git clone https://github.com/Wangnov/OpenGewe.git
cd OpenGewe
pip install -r requirements.txt
pip install -e .
```

**基础版本包含的功能：**
- ✅ 完整的微信机器人功能
- ✅ 简单消息队列 (SimpleMessageQueue)
- ✅ 插件系统
- ✅ 日志系统
- ✅ 任务调度器
- ✅ 所有API模块（登录、消息、群聊等）

**基础版本不包含：**
- ❌ 高级消息队列 (AdvancedMessageQueue)
- ❌ Celery 分布式任务处理
- ❌ Redis/RabbitMQ 支持

### 🔸 完整安装（需要高级功能的用户）

适合需要分布式处理、高并发场景的用户：

```bash
# 使用 pip 安装完整版本（推荐）
pip install opengewe[advanced]

# 或使用完整依赖文件
git clone https://github.com/Wangnov/OpenGewe.git
cd OpenGewe
pip install -r requirements-advanced.txt
pip install -e .

# 或手动安装依赖
pip install opengewe
pip install celery redis amqp joblib lz4
```

**完整版本额外包含：**
- ✅ 高级消息队列 (AdvancedMessageQueue)
- ✅ Celery 分布式任务处理
- ✅ Redis/RabbitMQ 消息代理支持
- ✅ 高性能序列化 (joblib + lz4)

### 📋 依赖对比

| 依赖包 | 基础安装 | 完整安装 | 用途 |
|--------|----------|----------|------|
| qrcode | ✅ | ✅ | 二维码生成 |
| aiohttp | ✅ | ✅ | 异步HTTP客户端 |
| pytz | ✅ | ✅ | 时区处理 |
| apscheduler | ✅ | ✅ | 任务调度 |
| loguru | ✅ | ✅ | 日志记录 |
| tomli | ✅ | ✅ | TOML配置解析 |
| celery | ❌ | ✅ | 分布式任务队列 |
| redis | ❌ | ✅ | Redis客户端 |
| amqp | ❌ | ✅ | AMQP协议支持 |
| joblib | ❌ | ✅ | 高效序列化 |
| lz4 | ❌ | ✅ | 快速压缩 |

### 🤔 如何选择？

**选择基础安装，如果您：**
- 是新用户，想快速体验
- 项目规模较小
- 单机部署
- 消息量不大
- 不需要分布式处理

**选择完整安装，如果您：**
- 需要生产环境部署
- 需要分布式处理
- 高并发场景
- 需要消息持久化
- 多worker协作

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
        queue_type="simple",  # 消息队列类型：simple（基础安装）或 advanced（完整安装）
    )
    
    # 发送文本消息
    await client.send_text_message("filehelper", "你好，这是一条测试消息")
    
    # 获取通讯录列表
    contacts = await client.contact.get_contact_list()
    
    # 关闭客户端
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 消息队列使用

OpenGewe 支持两种消息队列模式，根据您的安装方式自动选择：

#### 简单队列模式（基础安装）
```python
from opengewe import GeweClient

# 创建使用简单队列的客户端
client = GeweClient(
    base_url="your_base_url",
    token="your_token",
    app_id="your_app_id",
    queue_type="simple",  # 使用简单队列
    delay=1.0,  # 消息发送间隔（秒）
)
```

#### 高级队列模式（完整安装）
```python
from opengewe import GeweClient

# 创建使用高级队列的客户端（需要 pip install opengewe[advanced]）
client = GeweClient(
    base_url="your_base_url", 
    token="your_token",
    app_id="your_app_id",
    queue_type="advanced",  # 使用高级队列
    broker="redis://localhost:6379/0",  # Redis/RabbitMQ 地址
    backend="redis://localhost:6379/0",  # 结果存储地址
    queue_name="opengewe_messages",  # 队列名称
)
```

#### 队列功能对比

| 功能特性 | 简单队列 | 高级队列 |
|----------|----------|----------|
| 安装要求 | 基础安装 | 完整安装 |
| 部署复杂度 | 简单 | 需要 Redis/RabbitMQ |
| 分布式支持 | ❌ | ✅ |
| 消息持久化 | ❌ | ✅ |
| 多 Worker | ❌ | ✅ |
| 高并发 | 适中 | 高性能 |
| 适用场景 | 小型项目、单机 | 生产环境、分布式 |

#### 错误处理示例
```python
try:
    # 尝试创建高级队列
    client = GeweClient(
        base_url="your_base_url",
        token="your_token", 
        app_id="your_app_id",
        queue_type="advanced"
    )
except ImportError as e:
    print("高级队列功能不可用，请安装: pip install opengewe[advanced]")
    # 降级到简单队列
    client = GeweClient(
        base_url="your_base_url",
        token="your_token",
        app_id="your_app_id", 
        queue_type="simple"
    )
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
# 简单队列配置
delay = 1.0

# 高级队列配置（仅当 queue_type = "advanced" 时需要）
# broker = "redis://localhost:6379/0"
# backend = "redis://localhost:6379/0" 
# queue_name = "opengewe_messages"

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

## 许可协议 (License)

本项目采用 **GNU Affero General Public License v3.0 (AGPL-3.0)** 许可协议。

这是一个自由软件、强著佐权的许可证。简单来说，它保障了您拥有以下核心自由，并要求您在特定情况下履行相应义务：

* **自由使用**：您可以出于任何目的自由地运行此软件。
* **自由修改**：您可以自由地研究其工作原理，并根据您的需求修改源代码。
* **强制共享 (强著佐权)**：如果您分发（convey）本软件的修改版本，您**必须**以同样的 AGPL-3.0 许可证发布您的修改，并提供完整的源代码。这确保了整个社区都能从您的改进中受益。
* **网络服务条款 (AGPL 核心)**：这是 AGPL 与其他许可证最关键的区别。如果您在服务器上运行本软件的修改版，并通过网络（例如网站、API）向公众提供服务，您**也必须**向所有能够远程交互的用户提供您修改后版本的完整源代码的访问方式。
* **无担保**：本软件按“原样”提供，不提供任何形式的明示或暗示的担保。

选择 AGPL-3.0 协议是为了确保本软件及其所有衍生版本都能永久保持开放和自由，鼓励社区合作，并防止其在不回馈社区的情况下被用于闭源的商业网络服务中。

您可以在项目根目录的 `LICENSE` 文件中找到完整的协议文本。

## 免责声明

本项目仅供学习研究使用，请勿用于非法用途。使用本项目导致的任何问题与开发者无关。请遵守微信使用条款和相关法律法规。

## 联系方式

有问题或建议？请在GitHub上提交Issue或Pull Request。
