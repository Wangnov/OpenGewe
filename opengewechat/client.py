import requests
from typing import Dict, Optional
import time
from opengewechat.modules.login import LoginModule
from opengewechat.modules.contact import ContactModule
from opengewechat.modules.group import GroupModule
from opengewechat.modules.message import MessageModule
from opengewechat.modules.tag import TagModule
from opengewechat.modules.personal import PersonalModule
from opengewechat.modules.favorite import FavoriteModule
from opengewechat.modules.account import AccountModule
from opengewechat.modules.sns import SnsModule
from opengewechat.modules.finder import FinderModule
import qrcode


class GewechatClient:
    """GewechatAPI客户端

    Args:
        base_url: 调用Gewechat服务的基础URL，通常为http://Gewechat部署的镜像ip:2531/v2/api
        download_url: 从Gewechat镜像中下载内容的URL，通常为http://Gewechat部署的镜像ip:2532/download。注意：如果你需要生成的下载链接为公网可以访问，则需要使用公网IP或域名
        callback_url: 自行搭建的回调服务器URL，用于接收微信发来的回调消息，注意: 回调地址不可为127.0.0.1
        app_id: 需在Gewechat镜像内登录的设备ID
        token: 登录token
        debug: 是否开启调试模式，默认关闭
        is_gewe: 是否使用付费版gewe，默认为False，当base_url是 http://api.geweapi.com/gewe/v2/api 时自动设为True


    Methods:
        start_login(): 执行预设好的登录流程
        set_token(): 设置token
        set_app_id(): 设置app_id
        request(): 核心方法，与Gewechat镜像交互，发送API请求

    Modules:
        login: 登录模块
        contact: 通讯录模块
        group: 群聊模块
        message: 消息模块
        tag: 标签模块
        personal: 个人信息模块
        favorite: 收藏模块
        account: 账号模块
        sns: 朋友圈模块
        finder: 视频号模块
    """

    def __init__(
        self,
        base_url,
        download_url,
        callback_url,
        app_id,
        token,
        debug=False,
        is_gewe=False,
    ):
        self.base_url = base_url
        self.download_url = download_url
        self.callback_url = callback_url
        self.token = token
        self.app_id = app_id
        # 登录过程中缓存的变量
        self.uuid = None
        self.login_url = None
        self.captch_code = None
        # DEBUG
        self.debug = debug
        # 判断是否为付费版gewe
        self.is_gewe = is_gewe
        if base_url == "http://api.geweapi.com/gewe/v2/api":
            self.is_gewe = True
        # 初始化各模块
        self.login = LoginModule(self)
        self.contact = ContactModule(self)
        self.group = GroupModule(self)
        self.message = MessageModule(self)
        self.tag = TagModule(self)
        self.personal = PersonalModule(self)
        self.favorite = FavoriteModule(self)
        self.account = AccountModule(self)
        self.sns = SnsModule(self)
        self.finder = FinderModule(self)

    def __str__(self):
        return f"GewechatClient(base_url={self.base_url}, download_url={self.download_url}, callback_url={self.callback_url}, app_id={self.app_id}, token={self.token})"

    def set_token(self, token: str) -> None:
        """设置API令牌"""
        self.token = token

    def set_app_id(self, app_id: str) -> None:
        """设置应用ID"""
        self.app_id = app_id

    def request(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """发送API请求"""
        headers = {"X-GEWE-TOKEN": self.token} if self.token else {}
        headers["Content-Type"] = "application/json"

        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, headers=headers, json=data or {})
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return e
        # DEBUG用: 打印请求的url和请求体
        if self.debug:
            print(f"请求的url: {url}")
            print(f"请求的请求体: {data}")
            print(f"请求的headers: {headers}")
            print(f"请求的响应: {response.json()}")
        return response.json()

    def start_login(self):
        """这是一个预先写好的循环式终端登录流程，如在登录流程中出现问题，请自己执行login模块中的对应方法补全

        首次登录请将app_id和token传空以获取，之后登录请传入上一次登录返回的app_id和token"""
        print("\n✨✨✨ 正在执行Gewechat微信登录流程 ✨✨✨\n")
        # 检查登录设备，顺便查token可用性
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 📱 步骤 0: 检查登录设备并验证 Token 可用性        ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        device_list = self.login.get_device_list()
        token_available = False
        if device_list[1]:
            print("✅ 获取登录设备的 appId 列表成功！Token 可用！")
            print("📋 已登录设备 app_id 列表: ")
            print(device_list[0])
            token_available = True
            if self.app_id not in device_list[0] and self.app_id != "":
                print(
                    f'❌ 传入的 app_id: {self.app_id} 不在已登录设备的列表中\n   请传入正确的 app_id。如需登录新设备，请传入 app_id = ""'
                )
                return
        else:
            if (
                device_list[0]["ret"] == 500
                and "不可用或已过期" in device_list[0]["msg"]
            ):
                print(
                    f"⚠️ 设置的 token: {self.token} 已过期或不可用，即将重新获取 token..."
                )
            elif (
                device_list[0]["ret"] == 500
                and "header:X-GEWE-TOKEN 不可为空" in device_list[0]["msg"]
            ):
                print("⚠️ token 为空，即将重新获取 token...")
            else:
                print(device_list[0])
                return
        # 获取token
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 🔑 步骤 1: 获取 Token                             ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        if not token_available:
            if self.login.get_token()[1]:
                print(f"✅ 获取新 token 成功！Token 已设置: {self.token}")
            else:
                print(self.login.get_token()[0])
                return
        else:
            print("✅ Token 可用，跳过获取 token")
        # 获取设备的appId和登录所需的uuid、登录二维码
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 📲 步骤 2: 获取设备的 appId、uuid 和登录二维码    ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        get_qrcode_result, get_qrcode_success = self.login.get_qrcode()
        if get_qrcode_success:
            print("✅ 获取二维码成功！")
            print(f"📱 app_id 已设置: {self.app_id}")
            print(f"🔑 uuid 已设置: {self.uuid}")
            print(f"🔗 登录链接: {self.login_url}")
            # 终端打印图片二维码
            try:
                # 使用qrcode库在终端显示二维码
                print("\n📱 请扫描下面的二维码登录: ")
                # 直接使用登录URL生成二维码
                qr = qrcode.QRCode()
                qr.add_data(self.login_url)
                qr.make(fit=True)
                qr.print_ascii(invert=True)
            except Exception as e:
                print(f"❌ 打印二维码时出错: {e}")
                print("⚠️ 请使用登录链接自行生成二维码后，使用微信扫描二维码登录")

            # 检测是否登录成功
            print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("┃ 🔄 步骤 3: 检测登录状态                           ┃")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

            while True:
                check_login_result = self.login.check_login()
                if check_login_result[1]:
                    print("✅ 登录成功！")
                    break
                elif check_login_result[0]["data"]["nickName"] is not None:
                    print(
                        f"👤 已检测到微信用户: {check_login_result[0]['data']['nickName']} 扫码成功\n   请在手机上点击确认登录按钮...\n   ⏱️ 剩余操作时间: {check_login_result[0]['data']['expiredTime']}秒"
                    )
                    time.sleep(3)
                else:
                    if check_login_result[0]["data"]["expiredTime"] is None:
                        print("❌ 登录失败，执行登录超时！请重新执行登录流程")
                        return
                    else:
                        print(
                            f"⏳ 等待扫码登录中... ⏱️ 剩余操作时间: {check_login_result[0]['data']['expiredTime']}秒"
                        )
                        time.sleep(3)
        else:
            if get_qrcode_result["ret"] == 500:
                if get_qrcode_result["msg"] == "微信已登录，请勿重复登录。":
                    print(f"⚠️ {get_qrcode_result['msg']}")
                    print("尝试设置回调服务器...")
                elif (
                    get_qrcode_result.get("data")
                    and get_qrcode_result["data"].get("msg")
                    == "已达到最大客户端数量操作"
                ):
                    print(
                        "❌ 每个 token 只能登录两个 app_id（即使两个 app_id 是同一个微信）\n   请删除容器后重新创建容器，自动重置 token 后再进行操作 \n 参考命令： \n docker stop gewe && docker rm gewe && docker run -itd -v /root/temp:/root/temp -p 2531:2531 -p 2532:2532 -p 63799:6379 --restart=always --privileged=true --name=gewe gewe /usr/sbin/init"
                    )
                    return
                else:
                    print(get_qrcode_result)
                    return
            else:
                print(get_qrcode_result)
                return
        # 设置回调
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 📡 步骤 4: 设置回调服务器                         ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        if self.login.set_callback()[1]:
            print("✅ 设置回调成功")
            print(f"🔗 回调服务器: {self.callback_url}")
            print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("┃ 🎉 登录流程结束，请妥善保管以下登录参数:          ┃")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            print(
                "{\n"
                + f"  'base_url': '{self.base_url}',\n"
                + f"  'download_url': '{self.download_url}',\n"
                + f"  'callback_url': '{self.callback_url}',\n"
                + f"  'app_id': '{self.app_id}',\n"
                + f"  'token': '{self.token}'\n"
                + "}"
            )
            print("\n💡 如需使用该微信发送消息，请传入相同的参数进行实例化")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        else:
            print(self.login.set_callback()[0])
            return
