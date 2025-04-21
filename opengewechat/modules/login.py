from typing import Dict


class LoginModule:
    """登录模块"""

    def __init__(self, client):
        self.client = client

    def get_token(self) -> Dict:
        """获取Token(步骤1)"""
        response = self.client.request("/tools/getTokenId")
        if response["ret"] == 200 and "data" in response:
            self.client.token = response["data"]["token"]
            return response["data"]
        else:
            return response

    def get_qrcode(self, app_id: str = "") -> Dict:
        """获取登录二维码(步骤2)
        获取到二维码后，需要显示二维码，并等待用户扫码
        Args:
            app_id: 设备ID，首次登录传空，之后传接口返回的appId
        """
        data = {"appId": app_id} if app_id else {"appId": self.client.app_id}
        response = self.client.request("/login/getLoginQrCode", data)
        if response["ret"] == 200 and "data" in response:
            self.client.uuid = response["data"]["uuid"]
            self.client.qrImgBase64 = response["data"]["qrImgBase64"]
            return response["data"]
        else:
            return response

    def login(self) -> Dict:
        """执行登录(步骤3)
        该步骤需要循环执行，直到返回的data.status为2且data.loginInfo不为None，即为登录成功
        Args:
            app_id: 设备ID
            uuid: 取码返回的uuid
            captch_code: 扫码后手机提示输入的验证码(如有)
        """
        data = {"appId": self.client.app_id, "uuid": self.client.uuid}
        # todo 待完善
        # if self.client.captch_code:
        #     data["captchCode"] = self.client.captch_code
        response = self.client.request("/login/checkLogin", data)
        if (
            response["ret"] == 200
            and "data" in response
            and "status" in response["data"]
            and response["data"]["status"] == 2
            and "loginInfo" in response["data"]
            and response["data"]["loginInfo"] is not None
        ):
            # 登录成功后，清空uuid和qrImgBase64
            self.client.uuid = None
            self.client.qrImgBase64 = None
            return response["data"], True
        else:
            return response, False

    def set_callback(self) -> Dict:
        """设置消息回调地址"""
        data = {"token": self.client.token, "callbackUrl": self.client.callback_url}
        response = self.client.request("/tools/setCallback", data)
        return response

    def get_device_list(self) -> Dict:
        """查看设备列表"""
        response = self.client.request("/login/deviceList")
        if response["ret"] == 200 and "data" in response:
            return response["data"]
        else:
            return response
