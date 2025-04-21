# OpenGewechat

OpenGewechat 是一个用于 Gewechat API 的 Python 客户端，提供对象化的接口调用方式。

## 安装

```bash
pip install -e .
```

## 功能模块

- 登录模块：支持获取 Token、扫码登录、设置回调等功能
- 联系人模块：支持获取通讯录、搜索好友、添加/删除好友等功能
- 群组模块：支持创建群组、管理群成员、设置群公告等功能 
- 消息模块：支持发送各类消息（文本、图片、文件、链接等）和下载图片
- 标签模块：支持添加/删除标签、管理好友标签等功能
- 个人模块：支持获取个人资料、设置头像等功能
- 收藏模块：支持同步和管理收藏夹内容
- 账号模块：支持断线重连、退出登录等功能

## 使用示例

```python
import time
from opengewechat import GewechatClient

# 创建客户端实例，需要提供API基础URL和下载URL
client = GewechatClient(
    base_url="https://api.gewechat.com",
    download_url="https://download.gewechat.com"
)

# 获取并设置token
token_response = client.login.get_token()
if token_response["ret"] == 200:
    client.set_token(token_response["data"])

# 获取登录二维码
qrcode_response = client.login.get_qrcode()
if qrcode_response["ret"] == 200:
    data = qrcode_response["data"]
    app_id = data["appId"]
    uuid = data["uuid"]
    qrcode_url = data["qrData"]
    print(f"请用微信扫描二维码: {qrcode_url}")

# 循环检查登录状态
login_success = False
for _ in range(10):  # 尝试10次，每次间隔5秒
    login_response = client.login.login(app_id, uuid)
    if login_response["ret"] == 200:
        data = login_response["data"]
        status = data.get("status")
        if status == 2 and data.get("loginInfo"):  # 登录成功
            login_success = True
            print("登录成功!")
            wxid = data["loginInfo"]["wxid"]
            break
    time.sleep(5)

# 设置回调地址
if login_success:
    client.login.set_callback("http://your-callback-url.com/callback")
    
    # 发送文本消息
    message_response = client.message.send_text("wxid_friend123", "你好，这是测试消息")
    if message_response["ret"] == 200:
        print("消息发送成功")
    
    # 下载图片 (使用download_url)
    image_response = client.message.download_image("message_id_123456")
    if image_response["ret"] == 200:
        print("图片下载成功")
```

## 详细文档

请参考 [Gewechat API 文档](https://apifox.com/apidoc/shared/69ba62ca-cb7d-437e-85e4-6f3d3df271b1) 