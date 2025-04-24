from typing import Dict


class LoginModule:
    """登录模块"""

    def __init__(self, client):
        self.client = client

    def get_token(self) -> Dict:
        """获取token

        Summary:
            获取token
        """
        response = self.client.request("/tools/getTokenId")
        if response["ret"] == 200 and "data" in response:
            self.client.token = response["data"]
            return response["data"], True
        else:
            return response, False

    def get_qrcode(self, app_id: str = "") -> Dict:
        """获取登录二维码

        Summary:
            appId参数为设备ID，首次登录传空，会自动触发创建设备，掉线后重新登录则必须传接口返回的appId，注意同一个号避免重复创建设备，以免触发官方风控
            取码时传的appId需要与上次登录扫码的微信一致，否则会导致登录失败
            响应结果中的qrImgBase64为微信二维码图片的base64，前端需要将二维码图片展示给用户并进行手机扫码操作（PS: 扫码后调用步骤2，手机上才显示登录）。（或使用响应结果中的qrData生成二维码）

        Args:
            app_id: 设备ID，首次登录传空，之后传接口返回的appId
        """
        data = {"appId": app_id} if app_id else {"appId": self.client.app_id}
        response = self.client.request("/login/getLoginQrCode", data)
        if response["ret"] == 200 and "data" in response:
            self.client.app_id = response["data"]["appId"]
            self.client.uuid = response["data"]["uuid"]
            self.client.login_url = response["data"]["qrData"]
            return response["data"], True
        else:
            return response, False

    def check_login(self) -> Dict:
        """执行登录

        Summary:

            获取到登录二维码后需每间隔5s调用本接口来判断是否登录成功
            新设备登录平台，次日凌晨会掉线一次，重新登录时需调用获取二维码且传appId取码，登录成功后则可以长期在线
            登录成功后请保存appId与wxid的对应关系，后续接口中会用到

            该步骤需要循环执行，直到返回的data.status为2且data.loginInfo不为None，即为登录成功

        Args:
            app_id: 设备ID
            uuid: 取码返回的uuid
            captch_code: 扫码后手机提示输入的验证码(如有)
        """
        data = {"appId": self.client.app_id, "uuid": self.client.uuid}
        # todo 待完善，如果captch_code为空，则不传
        if self.client.captch_code:
            data["captchCode"] = self.client.captch_code
        response = self.client.request("/login/checkLogin", data)
        if (
            response["ret"] == 200
            and "data" in response
            and "status" in response["data"]
            and response["data"]["status"] == 2
            and "loginInfo" in response["data"]
            and response["data"]["loginInfo"] is not None
        ):
            # 登录成功后，清空uuid、login_url和captch_code
            self.client.uuid = None
            self.client.login_url = None
            self.client.captch_code = None
            return response["data"], True
        else:
            return response, False

    def set_callback(self) -> Dict:
        """设置消息回调地址

        Summary:
            设置消息回调地址，用于接收微信消息

        Args:
            token: 登录token
            callback_url: 回调地址
        注意：因为Gewechat运行在容器中，所以所设置的callback_url不可为127.0.0.1
        """
        data = {"token": self.client.token, "callbackUrl": self.client.callback_url}
        response = self.client.request("/tools/setCallback", data)
        if response["ret"] == 200:
            return response, True
        else:
            if "127.0.0.1" in self.client.callback_url:
                return {"ret": 500, "msg": "回调地址不可为127.0.0.1"}, False
            else:
                return response, False

    def get_device_list(self) -> Dict:
        """查看设备列表

        Summary:
            返回当前Gewechat容器内已经持久化的设备appId列表，这些设备只有在容器销毁后才会消失，否则会持久化存在（tu1h镜像则不会持久化，容器重启即重置appId列表）
        """
        response = self.client.request("/login/deviceList")
        try:
            if response["ret"] == 200 and "data" in response:
                return response["data"], True
            else:
                return response, False
        except TypeError:
            return {"ret": 500, "msg": "请等待gewechat容器启动完成再运行本脚本"}, False
