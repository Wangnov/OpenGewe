from typing import Dict


class PersonalModule:
    """个人模块"""

    def __init__(self, client):
        self.client = client

    def get_profile(self) -> Dict:
        """获取个人资料"""
        return self.client.request("/personal/profile")

    def get_qrcode(self) -> Dict:
        """获取自己的二维码"""
        return self.client.request("/personal/qrcode")

    def get_device_records(self) -> Dict:
        """获取设备记录"""
        return self.client.request("/personal/deviceRecords")

    def set_privacy(self, privacy_settings: Dict) -> Dict:
        """隐私设置"""
        return self.client.request("/personal/setPrivacy", privacy_settings)

    def update_profile(self, profile: Dict) -> Dict:
        """修改个人信息"""
        return self.client.request("/personal/updateProfile", profile)

    def update_avatar(self, avatar_path: str) -> Dict:
        """修改头像"""
        data = {"avatarPath": avatar_path}
        return self.client.request("/personal/updateAvatar", data)
