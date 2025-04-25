# OpenGewechat

OpenGewechat 是一个基于Gewechat的Python微信机器人框架，支持个人微信的自动化操作。该包提供了简单易用的API，帮助开发者快速实现微信自动化功能。

## 特性

- 完整的微信API封装，支持登录、消息收发、群管理等功能
- 31种微信消息类型的标准化处理
- 模块化设计，易于扩展
- 简洁的API接口，降低使用门槛
- 完善的类型提示，提高开发效率

## 安装

```bash
pip install opengewechat
```

## 快速开始

### 基础使用

```python
from opengewechat import GewechatClient

# 初始化客户端
client = GewechatClient(
    base_url="http://gewechat部署的镜像ip:2531/v2/api",
    download_url="http://gewechat部署的镜像ip:2532/download",
    callback_url="http://你的回调服务器地址:端口/callback",
    app_id="",  # 首次登录传空
    token=""    # 首次登录传空
)

# 登录微信
client.start_login()

# 发送文本消息
client.message.send_text("filehelper", "Hello, World!")
```

### 处理回调消息

```python
from flask import Flask, request
from opengewechat import MessageFactory, MessageType

app = Flask(__name__)
factory = MessageFactory()

@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    message = factory.process_json(data)
    
    if message:
        if message.type == MessageType.TEXT:
            print(f"收到文本消息: {message.text}")
        elif message.type == MessageType.IMAGE:
            print(f"收到图片消息: {message.url}")
    
    return "success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## 主要模块

### 客户端(Client)

`GewechatClient` 是包的核心类，提供了所有API的调用入口，主要功能包括：

- 初始化各个功能模块
- 管理登录状态和Token
- 处理API请求

### 功能模块(Modules)

包含8个主要功能模块，每个模块负责特定的功能区域：

- `login`: 登录、二维码获取、登录状态检查
- `message`: 发送各类消息（文本、图片、文件等）
- `contact`: 通讯录管理（好友列表、添加好友等）
- `group`: 群聊管理（创建群聊、邀请成员等）
- `tag`: 标签管理
- `personal`: 个人信息管理
- `favorite`: 收藏管理
- `account`: 账号管理

### 消息处理(Message)

消息模块提供了对微信回调消息的处理能力：

- `MessageFactory`: 消息工厂，负责识别和处理各类消息
- `MessageType`: 消息类型枚举，定义了所有支持的消息类型
- `BaseHandler`: 消息处理基类，用于自定义消息处理逻辑

## 示例

### 自动回复消息

```python
from flask import Flask, request
from opengewechat import GewechatClient, MessageFactory, MessageType

app = Flask(__name__)

client = GewechatClient(
    base_url="http://gewechat部署的镜像ip:2531/v2/api",
    download_url="http://gewechat部署的镜像ip:2532/download",
    callback_url="http://你的回调服务器地址:端口/callback",
    app_id="你的app_id",
    token="你的token"
)

factory = MessageFactory()

@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    message = factory.process_json(data)
    
    if message and message.type == MessageType.TEXT:
        # 自动回复
        if message.from_user != client.app_id:  # 避免回复自己
            client.message.send_text(message.from_user, f"收到您的消息：{message.text}")
    
    return "success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 自定义消息处理器

```python
from opengewechat import MessageFactory, BaseHandler, MessageType, BaseMessage
from dataclasses import dataclass

# 自定义消息模型
@dataclass
class CustomMessage(BaseMessage):
    custom_field: str = ""

# 自定义处理器
class CustomHandler(BaseHandler):
    def can_handle(self, data):
        # 自定义判断逻辑
        return data.get("TypeName") == "CustomType"
    
    def handle(self, data):
        message = CustomMessage(type=MessageType.UNKNOWN)
        message.custom_field = data.get("CustomField", "")
        return message

# 注册自定义处理器
factory = MessageFactory()
factory.register_handler(CustomHandler)
```

## 插件系统

OpenGewechat 现在支持插件系统，让你可以轻松扩展功能。以下是使用插件系统的示例：

### 创建自定义插件

创建一个自定义插件，只需继承 `BasePlugin` 类并实现相应方法：

```python
from opengewechat import BasePlugin
from opengewechat.message.models import BaseMessage, TextMessage
from opengewechat.message.types import MessageType

class MyPlugin(BasePlugin):
    def __init__(self, client=None):
        super().__init__(client)
        self.name = "MyPlugin"
        self.description = "我的自定义插件"
        self.version = "0.1.0"
    
    def can_handle(self, message: BaseMessage) -> bool:
        # 检查是否为文本消息
        if message.type != MessageType.TEXT:
            return False
        
        if not isinstance(message, TextMessage):
            return False
        
        # 处理特定内容的消息
        return message.content == "你好"
    
    def handle(self, message: BaseMessage) -> None:
        if not self.client:
            return
        
        # 文本消息的接收者可能是群聊或个人
        to_wxid = message.room_wxid if message.room_wxid else message.wxid
        
        # 发送回复
        self.client.message.send_text(to_wxid, "你好啊！")
```

### 加载和使用插件

```python
from opengewechat import GewechatClient, MessageFactory
from my_plugins import MyPlugin

# 创建客户端和消息工厂
client = GewechatClient(...)
factory = MessageFactory(client)

# 加载插件
factory.load_plugin(MyPlugin)

# 或者从目录加载所有插件
factory.load_plugins_from_directory("./plugins")

# 启用插件
factory.enable_plugin("MyPlugin")

# 获取所有插件
all_plugins = factory.get_all_plugins()
for plugin in all_plugins:
    print(f"插件: {plugin.name}, 状态: {'启用' if plugin.enabled else '禁用'}")
```

## 待办事项

- [ ] 实现31种消息类型的完整模型参数，包括：
  - 文本消息
  - 图片消息
  - 语音消息
  - 视频消息
  - 小程序消息
  - 链接消息
  - 文件消息
  - 位置消息
  - 名片消息
  - 系统消息（群创建、成员变更等）
  - 撤回消息
  - 引用消息
  - 表情消息
  - 公众号消息
  - 群邀请消息
  - 转账消息
  - 红包消息
  - 拍一拍消息
  - 朋友圈消息
  - 好友变更消息
  - 联系人信息变更
  - 其他消息类型

## 语音消息处理

### 保存语音缓冲区为Silk文件

接收到的语音消息有时会包含语音buffer数据，您可以使用VoiceMessage类的`save_voice_buffer_to_silk()`方法将其保存为silk文件：

```python
def on_message(message: BaseMessage) -> None:
    # 处理语音消息
    if message.type == MessageType.VOICE:
        voice_msg = message  # 类型已经是VoiceMessage
        
        # 检查是否有语音buffer
        if voice_msg.voice_buffer:
            # 将语音buffer保存为silk文件
            filepath = voice_msg.save_voice_buffer_to_silk()
            if filepath:
                print(f"语音文件已保存到: {filepath}")
```

完整示例请参考 [examples/save_voice_to_silk.py](examples/save_voice_to_silk.py)。

## 贡献

欢迎提交Issue和Pull Request，共同改进OpenGewechat！

## 许可证

本项目采用 MIT 许可证。

