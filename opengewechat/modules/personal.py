from typing import Dict, Optional


class PersonalModule:
    """个人模块"""

    def __init__(self, client):
        self.client = client

    def get_profile(self) -> Dict:
        """获取个人资料

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "alias": str,  # 微信号
                        "wxid": str,  # 微信ID
                        "nickName": str,  # 昵称
                        "mobile": str,  # 绑定的手机号
                        "uin": int,  # uin
                        "sex": int,  # 性别
                        "province": str,  # 省份
                        "city": str,  # 城市
                        "signature": str,  # 签名
                        "country": str,  # 国家
                        "bigHeadImgUrl": str,  # 大尺寸头像
                        "smallHeadImgUrl": str,  # 小尺寸头像
                        "regCountry": str,  # 注册国家
                        "snsBgImg": str  # 朋友圈背景图
                    }
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/personal/getProfile", data)

    def update_profile(
        self,
        nickname: Optional[str] = None,
        signature: Optional[str] = None,
        country: Optional[str] = None,
        province: Optional[str] = None,
        city: Optional[str] = None,
        sex: Optional[str] = None,
    ) -> Dict:
        """修改个人信息

        Args:
            nickname (Optional[str], optional): 昵称. Defaults to None.
            signature (Optional[str], optional): 个性签名. Defaults to None.
            country (Optional[str], optional): 国家. Defaults to None.
            province (Optional[str], optional): 省份. Defaults to None.
            city (Optional[str], optional): 城市. Defaults to None.
            sex (Optional[str], optional): 性别 1:男 2:女. Defaults to None.

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id}
        if nickname is not None:
            data["nickName"] = nickname
        if signature is not None:
            data["signature"] = signature
        if country is not None:
            data["country"] = country
        if province is not None:
            data["province"] = province
        if city is not None:
            data["city"] = city
        if sex is not None:
            data["sex"] = sex
        return self.client.request("/personal/updateProfile", data)

    def update_head_img(self, head_img_url: str) -> Dict:
        """修改头像

        Args:
            head_img_url (str): 头像的图片地址

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "headImgUrl": head_img_url}
        return self.client.request("/personal/updateHeadImg", data)

    def get_qr_code(self) -> Dict:
        """获取自己的二维码

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "qrCode": str  # 二维码base64编码
                    }
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/personal/getQrCode", data)

    def privacy_settings(self, option: int, open: bool) -> Dict:
        """隐私设置

        Args:
            option (int): 隐私设置的选项
                4: 加我为朋友时需要验证
                7: 向我推荐通讯录朋友
                8: 添加我的方式 手机号
                25: 添加我的方式 微信号
                38: 添加我的方式 群聊
                39: 添加我的方式 我的二维码
                40: 添加我的方式 名片
            open (bool): 开关

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "option": option, "open": open}
        return self.client.request("/personal/privacySettings", data)

    def get_safety_info(self) -> Dict:
        """获取设备记录

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "list": List[Dict]  # 设备记录列表，包含以下字段:
                            uuid (str): 设备ID
                            deviceName (str): 设备名称
                            deviceType (str): 设备类型
                            lastTime (int): 最后操作时间
                    }
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/personal/getSafetyInfo", data)
