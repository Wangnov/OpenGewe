from typing import Dict


class AccountModule:
    """账号管理"""

    def __init__(self, client):
        self.client = client

    def reconnection(self) -> Dict:
        """断线重连

        Summary:
            当系统返回账号已离线，但是手机顶部还显示ipad在线，可用此接口尝试重连。
            若返回错误/失败则必须重新调用登录流程。
            本接口非常用接口，可忽略。

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {  # 登录成功时返回
                        "uuid": str,  # 登录ID
                        "headImgUrl": str,  # 头像链接
                        "nickName": str,  # 昵称
                        "expiredTime": int,  # 过期时间
                        "status": int,  # 登录状态
                        "loginInfo": {
                            "uin": int,  # uin
                            "wxid": str,  # 微信ID
                            "nickName": str,  # 昵称
                            "mobile": str,  # 手机号
                            "alias": str  # 微信号
                        }
                    }
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/login/reconnection", data)

    def logout(self) -> Dict:
        """退出登录

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/login/logout", data)

    def check_online(self) -> Dict:
        """检查是否在线

        Summary:
            响应结果的data=true则是在线，反之为离线

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": bool  # 是否在线
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/login/checkOnline", data)
