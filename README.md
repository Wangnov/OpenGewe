# OpenGewe

![Logo](http://218.78.116.24:10885/static/img/profile.d88801b1.jpg)

> 基于 GeWeAPI 和 GeWe 私有部署方案 Gewechat 的异步 python 开源微信机器人框架，提供简单易用的微信自动化解决方案

## 项目状态

⚠️ **注意：由于原免费私有部署方案[Gewechat](https://github.com/Devo919/Gewechat)原项目暂停维护，本项目虽然兼容Gewechat，但不推荐使用。**

## 简介

OpenGewe是一个基于[GeWeAPI](https://geweapi.com)的微信机器人框架，专注于提供个人微信二次开发能力。本框架采用微信iPad协议登录（非HOOK破解桌面端），提供稳定、安全的微信API访问能力。

## 主要特性

- 💻 **完全异步**：使用原生异步实现，支持高并发和大数据量吞吐
- ‼️ **消息回调**：完全实现GeWeAPI返回的31种回调消息类型的检测
- 💬 **消息收发**：支持文本、图片、语音、视频等多种消息类型
- 👥 **群管理**：自动入群、退群、邀请好友、群成员管理等
- 🤖 **自动回复**：设置关键词自动回复，支持正则表达式
- 🔌 **插件系统**：可扩展的插件架构，轻松开发自定义功能
- 🔄 **API集成**：提供RESTful API，方便与其他系统集成
- 📊 **数据分析**：消息记录分析，用户行为统计等功能
- 📱 **朋友圈操作**：支持发布朋友圈内容、浏览朋友圈等
- 💾 **收藏管理**：微信收藏内容的获取与管理
- 📺 **视频号交互**：支持视频号相关的操作

## 兼容性说明

本项目**计划**完全兼容Gewechat付费版本[GeWeAPI](https://geweapi.com)。由于原项目暂停维护，我们建议用户转向使用GeWeAPI以获得持续的支持和更新。使用GeWeAPI只需修改`base_url`为：`http://api.geweapi.com/gewe/v2/api`，系统会自动识别并切换到付费版模式。

## 迁移到GeWeAPI

如果您希望继续使用本项目的功能，可以按照以下步骤迁移到GeWeAPI:

1. 访问[GeWeAPI官方网站](https://geweapi.com)注册账号
2. 获取GeWeAPI的token
3. 在配置中将`base_url`修改为Gewe API地址：`http://api.geweapi.com/gewe/v2/api` 或备用地址（GeWeAPI管理后台中显示的）
4. 在GeWeAPI管理后台中扫码登录微信账号，获得app_id
5. 在GeWeAPI管理后台中对此token设置回调服务器的地址

## 安装与使用

### 环境要求

- Python 3.11+

### 安装步骤

```bash
# 克隆项目
git clone https://github.com/yourusername/openGewe.git

# 进入项目目录
cd opengewe

# 安装依赖
pip install -r requirements.txt

# 或者使用pip直接安装(无效，暂未上传到PYPI)
pip install opengewe
```

### 基本使用

```python
from opengewe import GeweClient

# 创建客户端实例
client = GeweClient(
    base_url="http://your_gewe_server:2531/v2/api",  # GeWeAPI服务的基础URL
    download_url="http://your_gewe_server:2532/download",  # 下载链接的基础URL
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

使用fastapi_server.py作为示例回调服务器

也可以自行搭建其他回调服务器

# 使用方式与开源版本相同
```

## 插件开发

OpenGewe提供了强大而灵活的插件系统，让您可以轻松扩展微信机器人的功能。本插件系统不仅功能丰富，还兼容了[XYBot](https://github.com/HenryXiaoYang/XYBotV2)和[XXXBot](https://github.com/NanSsye/xxxbot-pad)的插件格式。

### 插件系统架构

OpenGewe的插件系统基于以下核心组件：

1. **PluginBase 基类**: 所有插件都必须继承此基类，它提供了插件的生命周期管理和基本功能
2. **消息处理装饰器**: 提供了针对不同消息类型的处理器注册机制
3. **计划任务装饰器**: 支持定时任务、周期任务和一次性任务的注册
4. **插件加载器**: 负责动态发现、加载和卸载插件
5. **配置管理**: 为每个插件提供独立的配置机制

### 插件结构

一个标准的OpenGewe插件包含以下文件：

```
MyPlugin/
├── __init__.py           # 空文件或包初始化代码
├── main.py               # 插件主类和核心逻辑
├── config.toml           # 插件配置文件
└── README.md             # 插件说明文档
```

### 开发流程

#### 1. 创建插件目录

在`plugins`目录下创建一个新的文件夹，命名为您的插件名称：

```bash
mkdir -p plugins/MyPlugin
touch plugins/MyPlugin/__init__.py
```

#### 2. 编写插件主类

在`main.py`中创建您的插件主类，继承自`PluginBase`：

```python
from utils.plugin_base import PluginBase
from utils.decorators import on_text_message, schedule

class MyPlugin(PluginBase):
    """我的第一个插件"""
    
    description = "这是我的第一个插件"
    author = "您的名字"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.enable = True  # 默认启用插件
        
    async def async_init(self):
        """异步初始化，可用于连接数据库等操作"""
        return
        
    @on_text_message()
    async def handle_text(self, client, message):
        """处理文本消息"""
        if not self.enable:
            return
            
        if message.text == "你好":
            await client.send_text_message(message.from_wxid, "你好！我是OpenGewe机器人")
    
    @schedule("interval", minutes=30)
    async def periodic_task(self, client):
        """定期执行的任务"""
        if not self.enable:
            return
        # 执行定期任务的代码
```

#### 3. 创建配置文件

为您的插件创建`config.toml`配置文件：

```toml
[basic]
enable = true  # 是否启用插件

[features]
# 您的插件特定配置
greeting_message = "你好！我是OpenGewe机器人"
```

#### 4. 编写说明文档

创建`README.md`文件，详细说明插件的功能、配置和使用方法。

#### 5. 启用插件

在OpenGewe的主配置文件`main_config.toml`中启用您的插件：

```toml
[plugins]
enabled_plugins = ["MyPlugin"]  # 加入您的插件名称
```

### 消息处理装饰器

OpenGewe提供了丰富的消息处理装饰器，用于注册不同类型消息的处理函数：

```python
@on_text_message(priority=50)  # 处理文本消息，优先级为50
async def handle_text(self, client, message):
    pass

@on_at_message()  # 处理@消息
async def handle_at(self, client, message):
    pass

@on_image_message()  # 处理图片消息
async def handle_image(self, client, message):
    pass
```

可用的消息处理装饰器包括：
- `on_text_message`: 文本消息
- `on_at_message`: @消息
- `on_image_message`: 图片消息
- `on_voice_message`: 语音消息
- `on_video_message`: 视频消息
- `on_file_message`: 文件消息
- `on_emoji_message`: 表情消息
- `on_link_message`: 链接消息
- `on_card_message`: 名片消息
- 以及更多群消息和系统消息处理器

### 定时任务装饰器

OpenGewe支持三种类型的定时任务：

```python
@schedule("interval", seconds=30)  # 每30秒执行一次
async def interval_task(self, client):
    pass

@schedule("cron", hour=8, minute=30)  # 每天8:30执行
async def daily_task(self, client):
    pass

@schedule("date", run_date="2025-01-01 00:00:00")  # 在指定时间执行一次
async def one_time_task(self, client):
    pass
```

### 优先级机制

插件可以通过设置优先级来控制消息处理的顺序：

```python
@on_text_message(priority=99)  # 优先级越高，越先处理
async def high_priority_handler(self, client, message):
    pass
```

优先级数值越大，越先被调用。默认优先级为0。

### 与消息队列集成

OpenGewe的插件系统完全兼容高级消息队列模式，确保插件处理大量消息时的稳定性和高效性：

- 在简单队列模式下，消息按序在单一线程中处理
- 在高级队列模式下，消息通过Celery分布式处理，支持高并发

插件开发者无需关心底层队列实现，编写的代码在两种模式下均可正常工作。

### 最佳实践

1. **配置检查**: 始终检查插件是否启用（`self.enable`）再处理消息
2. **异常处理**: 使用`try-except`捕获和记录异常，避免插件崩溃影响主程序
3. **异步编程**: 所有消息处理和定时任务应为异步函数（`async def`）
4. **资源管理**: 在`async_init`中初始化资源，在`on_disable`中释放资源
5. **消息节流**: 避免频繁发送消息，防止微信封号
6. **日志记录**: 使用`logging`模块记录插件活动

### 插件示例

OpenGewe提供了示例插件供您参考：

- **ExamplePlugin**: 演示基本功能和API使用

通过学习示例，您可以快速掌握插件开发的技巧和最佳实践。

### 插件兼容性

OpenGewe通过对message模块重写Mixin的方式，将主要的发送消息的模块接口调用写入消息队列，并将方法名和参数调用包装为和XYBot、XXXBot相同的形式，以供Client实例直接调用。

OpenGewe通过在utils中新增装饰器功能的方式，兼容了XYBot、XXXBot的回调捕获消息方法和定时方法。但OpenGewe的装饰器有更多种类，XYBot、XXXBot的装饰器种类只有有限的几种。

**理论上**可直接迁移XYBot或XXXBot的插件以供OpenGewe使用，而OpenGewe的插件在仅限调用mixin包装后的实例方法、使用不超过XYBot和XXXBot实现范围的装饰器的情况下，同样可以直接供XYBot和XXXBot调用。

### 常见问题

1. **插件不被加载**: 检查目录结构和`main_config.toml`中的配置
2. **消息处理器不触发**: 确认插件已启用且优先级设置正确
3. **定时任务不执行**: 检查调度器配置和任务触发条件
4. **导入错误**: 确保从`utils`包而非`opengewe`直接导入


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

由于项目暂停维护，我们目前不接受新的贡献请求。但您可以Fork本项目进行个人修改和改进。

## 致谢

- 特别感谢[Gewechat](https://github.com/Devo919/Gewechat)项目的开源精神
- 感谢[XYBot](https://github.com/HenryXiaoYang/XYBotV2)项目的异步实现给本项目以启发
- 感谢[XXXBot](https://github.com/NanSsye/xxxbot-pad)项目的管理后台前端实现给本项目以启发，和丰富的插件开发生态
- 感谢所有对本项目提供支持和反馈的用户

## 许可证

本项目采用[MIT LICENSE](LICENSE)。

## 免责声明

本项目仅供学习研究使用，请勿用于非法用途。使用本项目导致的任何问题与开发者无关。请遵守微信使用条款和相关法律法规。
