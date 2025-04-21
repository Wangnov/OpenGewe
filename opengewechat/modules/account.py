from typing import Dict


class AccountModule:
    """账号管理"""

    def __init__(self, client):
        self.client = client

    def reconnect(self) -> Dict:
        """断线重连"""
        return self.client.request("/account/reconnect")

    def logout(self) -> Dict:
        """退出"""
        return self.client.request("/account/logout")

    def check_online(self) -> Dict:
        """检查是否在线"""
        return self.client.request("/account/checkOnline")
