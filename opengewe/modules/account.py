from typing import Dict, Any


class AccountModule:
    """异步账号管理模块"""

    def __init__(self, client):
        self.client = client

    async def reconnection(self) -> Dict[str, Any]:
        """断线重连

        Summary:
            当系统返回账号已离线，但是手机顶部还显示ipad在线，可用此接口尝试重连。
            若返回错误/失败则必须重新调用登录流程。
            本接口非常用接口，可忽略。

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/login/reconnection", data)

    async def check_online(self) -> Dict[str, Any]:
        """检查是否在线

        Summary:
            响应结果的data=true则是在线，反之为离线

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/login/checkOnline", data)
        
    async def dialog_login(self, content: str = "") -> Dict[str, Any]:
        """弹框登录

        Args:
            content (str, optional): 内容. Defaults to "".

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "content": content}
        return await self.client.request("/login/dialogLogin", data)

    async def logout(self) -> Dict[str, Any]:
        """退出登录

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/login/logout", data)
