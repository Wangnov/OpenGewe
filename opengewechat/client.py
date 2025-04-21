import requests
from typing import Dict, Optional

from opengewechat.modules.login import LoginModule
from opengewechat.modules.contact import ContactModule
from opengewechat.modules.group import GroupModule
from opengewechat.modules.message import MessageModule
from opengewechat.modules.tag import TagModule
from opengewechat.modules.personal import PersonalModule
from opengewechat.modules.favorite import FavoriteModule
from opengewechat.modules.account import AccountModule


class GewechatClient:
    """格微API客户端"""

    def __init__(self, base_url, download_url, callback_url, app_id, token):
        self.base_url = base_url
        self.download_url = download_url
        self.callback_url = callback_url
        self.token = token
        self.app_id = app_id
        # 登录过程中缓存的变量
        self.uuid = None
        self.qrImgBase64 = None
        # 初始化各模块
        self.login = LoginModule(self)
        self.contact = ContactModule(self)
        self.group = GroupModule(self)
        self.message = MessageModule(self)
        self.tag = TagModule(self)
        self.personal = PersonalModule(self)
        self.favorite = FavoriteModule(self)
        self.account = AccountModule(self)

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
        response = requests.post(url, headers=headers, json=data or {})
        print(response.json())
        return response.json()

    def start_login(self):
        """开始登录"""
        self.login.get_token()
        self.login.get_qrcode()
        self.login.login()
        self.login.set_callback()
