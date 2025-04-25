from typing import Dict, List, Union


class ContactModule:
    """联系人模块"""

    def __init__(self, client):
        self.client = client

    def fetch_contacts_list(self) -> Dict:
        """获取通讯录列表

        Summary:
            本接口为长耗时接口，耗时时间根据好友数量递增，若接口返回超时可通过获取通讯录列表缓存接口获取响应结果。
            本接口返回的群聊仅为保存到通讯录中的群聊，若想获取会话列表中的所有群聊，需要通过消息订阅做二次处理。

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "friends": List[str],  # 好友的wxid
                        "chatrooms": List[str],  # 保存到通讯录中群聊的ID
                        "ghs": List[str]  # 关注的公众号ID
                    }
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/contacts/fetchContactsList", data)

    def fetch_contacts_list_cache(self) -> Dict:
        """获取通讯录列表缓存

        Summary:
            获取通讯录列表缓存，若无缓存则同步获取通讯录列表，与获取通讯录列表接口返回格式一致。

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "friends": List[str],  # 好友的wxid
                        "chatrooms": List[str],  # 保存到通讯录中群聊的ID
                        "ghs": List[str]  # 关注的公众号ID
                    }
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/contacts/fetchContactsListCache", data)

    def search(self, contacts_info: str) -> Dict:
        """搜索好友

        Summary:
            搜索的联系人信息若已经是好友，响应结果的v3则为好友的wxid。
            本接口返回的数据可通过添加联系人接口发送添加好友请求。

        Args:
            contacts_info (str): 搜索的联系人信息，微信号、手机号等

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "v3": str,  # 搜索好友的v3，添加好友时使用
                        "nickName": str,  # 搜索好友的昵称
                        "sex": int,  # 搜索好友的性别
                        "signature": str,  # 搜索好友的签名
                        "bigHeadImgUrl": str,  # 搜索好友的大尺寸头像
                        "smallHeadImgUrl": str,  # 搜索好友的小尺寸头像
                        "v4": str  # 搜索好友的v4，添加好友时使用
                    }
                }
        """
        data = {"appId": self.client.app_id, "contactsInfo": contacts_info}
        return self.client.request("/contacts/search", data)

    def add_contacts(
        self, scene: int, option: int, v3: str, v4: str, content: str = ""
    ) -> Dict:
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
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "scene": scene,
            "option": option,
            "v3": v3,
            "v4": v4,
            "content": content,
        }
        return self.client.request("/contacts/addContacts", data)

    def delete_friend(self, wxid: str) -> Dict:
        """删除好友

        Args:
            wxid (str): 删除好友的wxid

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "wxid": wxid}
        return self.client.request("/contacts/deleteFriend", data)

    def upload_phone_address_list(self, contacts: List[Dict]) -> Dict:
        """上传手机通讯录

        Args:
            contacts (List[Dict]): 通讯录联系人列表，每个联系人包含姓名和手机号

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "contacts": contacts}
        return self.client.request("/contacts/uploadPhoneAddressList", data)

    def get_brief_info(self, wxids: Union[List[str], str]) -> Dict:
        """获取群/好友简要信息

        Args:
            wxids (Union[List[str], str]): 好友的wxid列表

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": [
                        {
                            "userName": str,  # 好友的wxid
                            "nickName": str,  # 好友的昵称
                            "pyInitial": str,  # 好友昵称的拼音首字母
                            "quanPin": str,  # 好友昵称的全拼
                            "sex": int,  # 好友的性别
                            "remark": str,  # 好友备注
                            "remarkPyInitial": str,  # 好友备注的拼音首字母
                            "remarkQuanPin": str,  # 好友备注的全拼
                            "signature": str,  # 好友的签名
                            "alias": str,  # 好友的微信号
                            "snsBgImg": str,  # 朋友圈背景图链接
                            "country": str,  # 国家
                            "bigHeadImgUrl": str,  # 大尺寸头像链接
                            "smallHeadImgUrl": str,  # 小尺寸头像链接
                            "description": str,  # 好友的描述
                            "cardImgUrl": str,  # 好友描述的图片链接
                            "labelList": str,  # 好友的标签ID
                            "province": str,  # 省份
                            "city": str,  # 城市
                            "phoneNumList": List[str]  # 好友的手机号码
                        }
                    ]
                }
        """
        data = {"appId": self.client.app_id, "wxids": wxids}
        return self.client.request("/contacts/getBriefInfo", data)

    def get_detail_info(self, wxids: Union[List[str], str]) -> Dict:
        """获取群/好友详细信息

        Args:
            wxids (Union[List[str], str]): 好友的wxid列表

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": [
                        {
                            "userName": str,  # 好友的wxid
                            "nickName": str,  # 好友的昵称
                            "pyInitial": str,  # 好友昵称的拼音首字母
                            "quanPin": str,  # 好友昵称的全拼
                            "sex": int,  # 好友的性别
                            "remark": str,  # 好友备注
                            "remarkPyInitial": str,  # 好友备注的拼音首字母
                            "remarkQuanPin": str,  # 好友备注的全拼
                            "signature": str,  # 好友的签名
                            "alias": str,  # 好友的微信号
                            "snsBgImg": str,  # 朋友圈背景图链接
                            "country": str,  # 国家
                            "bigHeadImgUrl": str,  # 大尺寸头像链接
                            "smallHeadImgUrl": str,  # 小尺寸头像链接
                            "description": str,  # 好友的描述
                            "cardImgUrl": str,  # 好友描述的图片链接
                            "labelList": str,  # 好友的标签ID
                            "province": str,  # 省份
                            "city": str,  # 城市
                            "phoneNumList": List[str]  # 好友的手机号码
                        }
                    ]
                }
        """
        data = {"appId": self.client.app_id, "wxids": wxids}
        return self.client.request("/contacts/getDetailInfo", data)

    def set_friend_permissions(self, wxid: str, chat_only: bool) -> Dict:
        """设置好友仅聊天

        Args:
            wxid (str): 好友的wxid
            chat_only (bool): 是否仅聊天

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "wxid": wxid, "chatOnly": chat_only}
        return self.client.request("/contacts/setFriendPermissions", data)

    def set_friend_remark(self, wxid: str, remark: str) -> Dict:
        """设置好友备注

        Args:
            wxid (str): 好友的wxid
            remark (str): 备注的备注

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "wxid": wxid, "remark": remark}
        return self.client.request("/contacts/setFriendRemark", data)

    def get_phone_address_list(self) -> Dict:
        """获取手机通讯录列表

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": [
                        {
                            "name": str,  # 通讯录联系人名称
                            "phoneNumber": str,  # 手机号码
                            "wxContacts": List[Dict]  # 微信中存在的联系人信息
                        }
                    ]
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/contacts/getPhoneAddressList", data)

    def check_relation(self, wxids: list) -> Dict:
        """检测好友关系

        Summary:
            检测好友关系，支持批量检测

        Args:
            wxids (list): 好友的wxid列表，最多支持20个wxid

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": [
                        {
                            "wxid": str,  # 好友的wxid
                            "relation": int  # 0:正常 1:删除 2:拉黑
                        }
                    ]
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "wxids": wxids}
        return self.client.request("/contacts/checkRelation", data)

    def im_search(self, scene: int, content: str) -> Dict:
        """搜索企微

        Summary:
            搜索企微，支持企微二维码搜索

        Args:
            scene (int): 搜索类型 1：企微二维码
            content (str): 企微二维码信息

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "nickName": str,  # 昵称
                        "sex": int,  # 性别
                        "signature": str,  # 签名
                        "bigHeadImgUrl": str,  # 大头像链接
                        "smallHeadImgUrl": str,  # 小头像链接
                        "v3": str,  # v3
                        "v4": str  # v4
                    }
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "scene": scene, "content": content}
        return self.client.request("/im/search", data)

    def im_add(self, v3: str, v4: str) -> Dict:
        """添加企微好友

        Summary:
            添加企微好友，需要先搜索获取v3和v4

        Args:
            v3 (str): 搜索接口返回的v3
            v4 (str): 搜索接口返回的v4

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str  # 返回信息
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "v3": v3, "v4": v4}
        return self.client.request("/im/add", data)

    def im_sync(self) -> Dict:
        """同步企微好友

        Summary:
            同步企微好友列表

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": [
                        {
                            "userName": str,  # 企微号
                            "nickName": str,  # 昵称
                            "remark": str,  # 备注
                            "bigHeadImg": str,  # 大头像
                            "smallHeadImg": str,  # 小头像
                            "appId": str,  # appid
                            "descWordingId": str  # 所在企业id
                        }
                    ]
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id}
        return self.client.request("/im/sync", data)

    def im_detail(self, to_user_name: str) -> Dict:
        """获取企微好友详情

        Summary:
            获取企微好友详细信息

        Args:
            to_user_name (str): 企微好友的userName

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "userName": str,  # 企微号
                        "nickName": str,  # 昵称
                        "remark": str,  # 备注
                        "bigHeadImg": str,  # 头像地址
                        "smallHeadImg": str,  # 头像地址小
                        "appId": str,  # appid
                        "descWordingId": str,  # 企业id
                        "wording": str,  # 企业名称
                        "wordingPinyin": str,  # 企业名称拼音
                        "wordingQuanpin": str  # 企业名称全拼
                    }
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "toUserName": to_user_name}
        return self.client.request("/im/detail", data)
