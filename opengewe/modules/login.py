from typing import Dict, Tuple, Any


class LoginModule:
    """异步登录模块"""

    def __init__(self, client):
        self.client = client

    async def get_token(self) -> Tuple[Dict[str, Any], bool]:
        """获取token

        Summary:
            获取token

        Returns:
            Tuple[Dict[str, Any], bool]: 结果和成功标志
        """
        response = await self.client.request("/tools/getTokenId")
        if response["ret"] == 200 and "data" in response:
            self.client.token = response["data"]
            return response["data"], True
        else:
            return response, False

    async def get_qrcode(self, app_id: str = "") -> Tuple[Dict[str, Any], bool]:
        """获取登录二维码

        Summary:
            appId参数为设备ID，首次登录传空，会自动触发创建设备，掉线后重新登录则必须传接口返回的appId
            取码时传的appId需要与上次登录扫码的微信一致，否则会导致登录失败
            响应结果中的qrImgBase64为微信二维码图片的base64，前端需要将二维码图片展示给用户并进行手机扫码操作。
            （或使用响应结果中的qrData生成二维码）

        Args:
            app_id: 设备ID，首次登录传空，之后传接口返回的appId

        Returns:
            Tuple[Dict[str, Any], bool]: 结果和成功标志
        """
        data = {"appId": app_id} if app_id else {"appId": self.client.app_id}
        response = await self.client.request("/login/getLoginQrCode", data)
        if response["ret"] == 200 and "data" in response:
            self.client.app_id = response["data"]["appId"]
            self.client.uuid = response["data"]["uuid"]
            self.client.login_url = response["data"]["qrData"]
            return response["data"], True
        else:
            return response, False

    async def dialog_login(
        self, region_id: str, proxy_ip: str = ""
    ) -> Tuple[Dict[str, Any], bool]:
        """弹框登录

        Summary:
            本接口一般用于主动下线后，需要重新登录时使用，和取码登录区别在于，一个是手机需要扫码，另一个是手机弹框确认登录。
            调用本接口后手机会弹框确认登录页面，点确认后调用执行登录接口检测是否登录成功。

            regionId：微信登陆地区ID，登录时请选择最近的地区，目前支持以下地区：
            110000:北京市, 120000:天津市, 130000:河北省, 140000:山西省
            310000:上海市, 320000:江苏省, 330000:浙江省, 340000:安徽省
            350000:福建省, 360000:江西省, 370000:山东省, 410000:河南省
            420000:湖北省, 430000:湖南省, 440000:广东省, 460000:海南省
            500000:重庆市, 510000:四川省, 530000:云南省, 610000:陕西省

            若目前支持的regionId中没有您所在的地区，可以自行采购socks5协议代理IP，填写到proxyIp参数中。

            使用本接口登录并非100%成功，本接口返回失败后，可通过扫码登录的方式登录。
            以下几种情况无法使用本接口登录：手机点击退出登录、新设备登录次日、官方风控下线。

        Args:
            region_id (str): 微信登录地区ID，如："320000"
            proxy_ip (str, optional): 代理IP 格式：socks5://username:password@123.2.2.2. Defaults to "".

        Returns:
            Tuple[Dict[str, Any], bool]: 结果和成功标志
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }, False

        data = {"appId": self.client.app_id, "regionId": region_id, "proxyIp": proxy_ip}

        response = await self.client.request("/login/dialogLogin", data)
        if response["ret"] == 200 and "data" in response:
            # 更新客户端的appId和uuid
            self.client.app_id = response["data"]["appId"]
            self.client.uuid = response["data"]["uuid"]
            return response, True
        else:
            return response, False

    async def check_login(self) -> Tuple[Dict[str, Any], bool]:
        """执行登录

        Summary:
            获取到登录二维码后需每间隔5s调用本接口来判断是否登录成功
            新设备登录平台，次日凌晨会掉线一次，重新登录时需调用获取二维码且传appId取码，登录成功后则可以长期在线
            登录成功后请保存appId与wxid的对应关系，后续接口中会用到

            该步骤需要循环执行，直到返回的data.status为2且data.loginInfo不为None，即为登录成功

        Returns:
            Tuple[Dict[str, Any], bool]: 结果和成功标志
        """
        data = {"appId": self.client.app_id, "uuid": self.client.uuid}
        # 如果captch_code为空，则不传
        if self.client.captch_code:
            data["captchCode"] = self.client.captch_code

        response = await self.client.request("/login/checkLogin", data)
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

    async def set_callback(self) -> Tuple[Dict[str, Any], bool]:
        """设置消息回调地址

        Summary:
            设置消息回调地址，用于接收微信消息

        Returns:
            Tuple[Dict[str, Any], bool]: 结果和成功标志

        注意：因为Gewe运行在容器中，所以所设置的callback_url不可为127.0.0.1
        """
        data = {"token": self.client.token, "callbackUrl": self.client.callback_url}
        response = await self.client.request("/tools/setCallback", data)
        if response["ret"] == 200:
            return response, True
        else:
            if "127.0.0.1" in self.client.callback_url:
                return {"ret": 500, "msg": "回调地址不可为127.0.0.1"}, False
            else:
                return response, False

    async def get_device_list(self) -> Tuple[Dict[str, Any], bool]:
        """查看设备列表

        Summary:
            返回当前Gewe容器内已经持久化的设备appId列表
            这些设备只有在容器销毁后才会消失，否则会持久化存在
            （tu1h镜像则不会持久化，容器重启即重置appId列表）

        Returns:
            Tuple[Dict[str, Any], bool]: 结果和成功标志
        """
        response = await self.client.request("/login/deviceList")
        try:
            if response["ret"] == 200 and "data" in response:
                return response["data"], True
            else:
                return response, False
        except TypeError:
            return {"ret": 500, "msg": "请等待gewe容器启动完成再运行本脚本"}, False
