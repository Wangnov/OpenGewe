from typing import Dict, List


class ContactModule:
    """联系人模块"""

    def __init__(self, client):
        self.client = client

    def get_contacts(self) -> Dict:
        """获取通讯录列表"""
        return self.client.request("/contact/list")

    def get_contacts_cache(self) -> Dict:
        """获取通讯录列表缓存"""
        return self.client.request("/contact/listCache")

    def search_friend(self, keyword: str) -> Dict:
        """搜索好友"""
        data = {"keyword": keyword}
        return self.client.request("/contact/search", data)

    def add_contact(self, wxid: str, message: str = "") -> Dict:
        """添加联系人/同意添加好友"""
        data = {"wxid": wxid, "message": message}
        return self.client.request("/contact/add", data)

    def delete_friend(self, wxid: str) -> Dict:
        """删除好友"""
        data = {"wxid": wxid}
        return self.client.request("/contact/delete", data)

    def upload_phone_contacts(self, contacts: List[Dict]) -> Dict:
        """上传手机通讯录"""
        data = {"contacts": contacts}
        return self.client.request("/contact/uploadPhoneContacts", data)

    def get_brief_info(self, wxid: str) -> Dict:
        """获取群/好友简要信息"""
        data = {"wxid": wxid}
        return self.client.request("/contact/briefInfo", data)

    def get_detail_info(self, wxid: str) -> Dict:
        """获取群/好友详细信息"""
        data = {"wxid": wxid}
        return self.client.request("/contact/detailInfo", data)

    def set_chat_only(self, wxid: str, is_chat_only: bool) -> Dict:
        """设置好友仅聊天"""
        data = {"wxid": wxid, "isChatOnly": is_chat_only}
        return self.client.request("/contact/setChatOnly", data)

    def set_remark(self, wxid: str, remark: str) -> Dict:
        """设置好友备注"""
        data = {"wxid": wxid, "remark": remark}
        return self.client.request("/contact/setRemark", data)

    def get_phone_contacts(self) -> Dict:
        """获取手机通讯录"""
        return self.client.request("/contact/phoneContacts")
