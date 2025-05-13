from typing import Dict, List, Union, Any


class ContactModule:
    """异步联系人模块"""

    def __init__(self, client):
        self.client = client

    async def fetch_contacts_list(self) -> Dict[str, Any]:
        """获取通讯录列表

        Summary:
            本接口为长耗时接口，耗时时间根据好友数量递增，若接口返回超时可通过获取通讯录列表缓存接口获取响应结果。
            本接口返回的群聊仅为保存到通讯录中的群聊，若想获取会话列表中的所有群聊，需要通过消息订阅做二次处理。

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/contacts/fetchContactsList", data)

    async def fetch_contacts_list_cache(self) -> Dict[str, Any]:
        """获取通讯录列表缓存

        Summary:
            获取通讯录列表缓存，若无缓存则同步获取通讯录列表，与获取通讯录列表接口返回格式一致。

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/contacts/fetchContactsListCache", data)

    async def get_brief_info(self, wxids: Union[List[str], str]) -> Dict[str, Any]:
        """获取群/好友简要信息

        Args:
            wxids (Union[List[str], str]): 好友的wxid列表或逗号分隔的字符串

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "wxids": wxids}
        return await self.client.request("/contacts/getBriefInfo", data)

    async def get_detail_info(self, wxids: Union[List[str], str]) -> Dict[str, Any]:
        """获取群/好友详细信息

        Args:
            wxids (Union[List[str], str]): 好友的wxid列表或逗号分隔的字符串

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "wxids": wxids}
        return await self.client.request("/contacts/getDetailInfo", data)

    async def search(self, contacts_info: str) -> Dict[str, Any]:
        """搜索好友

        Summary:
            搜索的联系人信息若已经是好友，响应结果的v3则为好友的wxid。
            本接口返回的数据可通过添加联系人接口发送添加好友请求。

        Args:
            contacts_info (str): 搜索的联系人信息，微信号、手机号等

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "contactsInfo": contacts_info}
        return await self.client.request("/contacts/search", data)

    async def add_contacts(
        self, scene: int, option: int, v3: str, v4: str, content: str = ""
    ) -> Dict[str, Any]:
        """添加联系人/同意添加好友

        Summary:
            本接口建议在线3天后再进行调用。
            好友添加成功后，会通过回调消息推送一条包含v3的消息，可用于判断好友是否添加成功。

        Args:
            scene (int): 添加来源，同意添加好友时传回调消息xml中的scene值。
                        添加好友时的枚举值如下：
                        3：微信号搜索
                        4：QQ好友
                        8：来自群聊
                        15：手机号

            option (int): 操作类型，2添加好友 3同意好友 4拒绝好友
            v3 (str): 通过搜索或回调消息获取到的v3
            v4 (str): 通过搜索或回调消息获取到的v4
            content (str, optional): 添加好友时的招呼语. Defaults to "".

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "scene": scene,
            "option": option,
            "v3": v3,
            "v4": v4,
            "content": content,
        }
        return await self.client.request("/contacts/addContacts", data)

    async def delete_friend(self, wxid: str) -> Dict[str, Any]:
        """删除好友

        Args:
            wxid (str): 删除好友的wxid

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "wxid": wxid}
        return await self.client.request("/contacts/deleteFriend", data)

    async def set_friend_permissions(self, wxid: str, chat_only: bool) -> Dict[str, Any]:
        """设置好友仅聊天

        Args:
            wxid (str): 好友的wxid
            chat_only (bool): 是否仅聊天

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "wxid": wxid, "chatOnly": chat_only}
        return await self.client.request("/contacts/setFriendPermissions", data)

    async def set_friend_remark(self, wxid: str, remark: str) -> Dict[str, Any]:
        """设置好友备注

        Args:
            wxid (str): 好友的wxid
            remark (str): 要设置的备注名

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "wxid": wxid, "remark": remark}
        return await self.client.request("/contacts/setFriendRemark", data)

    async def get_phone_address_list(self) -> Dict[str, Any]:
        """获取手机通讯录

        Summary:
            获取手机通讯录联系人列表

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/contacts/getPhoneAddressList", data)

    async def upload_phone_address_list(self, contacts: List[Dict]) -> Dict[str, Any]:
        """上传手机通讯录

        Args:
            contacts (List[Dict]): 通讯录联系人列表，每个联系人包含姓名和手机号

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "contacts": contacts}
        return await self.client.request("/contacts/uploadPhoneAddressList", data)

    async def check_relation(self, wxids: list) -> Dict[str, Any]:
        """检测好友关系

        Args:
            wxids (list): 要检查的wxid列表

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "wxids": wxids}
        return await self.client.request("/contacts/checkRelation", data)
