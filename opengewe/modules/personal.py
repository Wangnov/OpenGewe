from typing import Dict, Optional, Any


class PersonalModule:
    """异步个人信息模块"""

    def __init__(self, client):
        self.client = client

    async def get_profile(self) -> Dict[str, Any]:
        """获取个人资料

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/personal/getProfile", data)

    async def update_profile(
        self,
        nickname: Optional[str] = None,
        signature: Optional[str] = None,
        country: Optional[str] = None,
        province: Optional[str] = None,
        city: Optional[str] = None,
        sex: Optional[str] = None,
    ) -> Dict[str, Any]:
        """修改个人信息

        Args:
            nickname (Optional[str], optional): 昵称. Defaults to None.
            signature (Optional[str], optional): 个性签名. Defaults to None.
            country (Optional[str], optional): 国家. Defaults to None.
            province (Optional[str], optional): 省份. Defaults to None.
            city (Optional[str], optional): 城市. Defaults to None.
            sex (Optional[str], optional): 性别 1:男 2:女. Defaults to None.

        Returns:
            Dict[str, Any]: 接口返回结果
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
        return await self.client.request("/personal/updateProfile", data)

    async def update_head_img(self, head_img_url: str) -> Dict[str, Any]:
        """修改头像

        Args:
            head_img_url (str): 头像的图片地址

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "headImgUrl": head_img_url}
        return await self.client.request("/personal/updateHeadImg", data)

    async def get_qr_code(self) -> Dict[str, Any]:
        """获取自己的二维码

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/personal/getQrCode", data)

    async def privacy_settings(self, option: int, open: bool) -> Dict[str, Any]:
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
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "option": option, "open": open}
        return await self.client.request("/personal/privacySettings", data)

    async def get_safety_info(self) -> Dict[str, Any]:
        """获取设备记录

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/personal/getSafetyInfo", data)
