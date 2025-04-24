from typing import Dict, List, Union


class GroupModule:
    """群模块"""

    def __init__(self, client):
        self.client = client

    def create_chatroom(self, wxids: List[str]) -> Dict:
        """创建微信群

        Summary:
            创建微信群时最少要选择两位微信好友

        Args:
            wxids (List[str]): 好友的wxid列表，至少2个

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "headImgBase64": str,  # 群头像的base64图片
                        "chatroomId": str  # 群ID
                    }
                }
        """
        data = {"appId": self.client.app_id, "wxids": wxids}
        return self.client.request("/group/createChatroom", data)

    def modify_chatroom_name(self, chatroom_id: str, chatroom_name: str) -> Dict:
        """修改群名称

        Summary:
            修改完群名称后若发现手机未展示修改后的名称，可能是手机缓存未刷新，
            手机聊天框多切换几次会刷新。

        Args:
            chatroom_id (str): 群ID
            chatroom_name (str): 群名称

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "chatroomName": chatroom_name,
        }
        return self.client.request("/group/modifyChatroomName", data)

    def modify_chatroom_remark(self, chatroom_id: str, chatroom_remark: str) -> Dict:
        """修改群备注

        Summary:
            群备注仅自己可见。
            修改完群备注后若发现手机未展示修改后的备注，可能是手机缓存未刷新，
            手机聊天框多切换几次会刷新。

        Args:
            chatroom_id (str): 群ID
            chatroom_remark (str): 群备注

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "chatroomRemark": chatroom_remark,
        }
        return self.client.request("/group/modifyChatroomRemark", data)

    def modify_chatroom_nickname_for_self(
        self, chatroom_id: str, nickname: str
    ) -> Dict:
        """修改我在群内的昵称

        Args:
            chatroom_id (str): 群ID
            nickname (str): 群昵称

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "nickName": nickname,
        }
        return self.client.request("/group/modifyChatroomNickNameForSelf", data)

    def invite_member(
        self, chatroom_id: str, wxids: Union[List[str], str], reason: str = ""
    ) -> Dict:
        """邀请/添加进群

        Args:
            chatroom_id (str): 群ID
            wxids (Union[List[str], str]): 邀请进群的好友wxid，列表或者多个英文逗号分隔的字符串
            reason (str, optional): 邀请进群的说明. Defaults to "".

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        if isinstance(wxids, list):
            wxids = ",".join(wxids)

        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "wxids": wxids,
            "reason": reason,
        }
        return self.client.request("/group/inviteMember", data)

    def remove_member(self, chatroom_id: str, wxids: Union[List[str], str]) -> Dict:
        """删除群成员

        Args:
            chatroom_id (str): 群ID
            wxids (Union[List[str], str]): 删除的群成员wxid，列表或者多个英文逗号分隔的字符串

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        if isinstance(wxids, list):
            wxids = ",".join(wxids)

        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "wxids": wxids,
        }
        return self.client.request("/group/removeMember", data)

    def quit_chatroom(self, chatroom_id: str) -> Dict:
        """退出群聊

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return self.client.request("/group/quitChatroom", data)

    def disband_chatroom(self, chatroom_id: str) -> Dict:
        """解散群聊

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return self.client.request("/group/disbandChatroom", data)

    def get_chatroom_info(self, chatroom_id: str) -> Dict:
        """获取群信息

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "chatroomId": str,  # 群ID
                        "nickName": str,  # 群名称
                        "pyInitial": str,  # 群名称的拼音首字母
                        "quanPin": str,  # 群名称的全拼
                        "sex": int,
                        "remark": str,  # 群备注，仅自己可见
                        "remarkPyInitial": str,  # 群备注的拼音首字母
                        "remarkQuanPin": str,  # 群备注的全拼
                        "chatRoomNotify": int,  # 群消息是否提醒
                        "chatRoomOwner": str,  # 群主的wxid
                        "smallHeadImgUrl": str,  # 群头像链接
                        "memberList": [  # 群成员列表
                            {
                                "wxid": str,  # 群成员的wxid
                                "nickName": str,  # 群成员的昵称
                                "inviterUserName": str,  # 邀请人的wxid
                                "memberFlag": int,  # 标识
                                "displayName": str,  # 在本群内的昵称
                                "bigHeadImgUrl": str,  # 大尺寸头像
                                "smallHeadImgUrl": str  # 小尺寸头像
                            }
                        ]
                    }
                }
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return self.client.request("/group/getChatroomInfo", data)

    def get_chatroom_member_list(self, chatroom_id: str) -> Dict:
        """获取群成员列表

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "memberList": [  # 群成员列表
                            {
                                "wxid": str,  # 群成员的wxid
                                "nickName": str,  # 群成员昵称
                                "inviterUserName": str,  # 邀请人的wxid
                                "memberFlag": int,  # 标识
                                "displayName": str,  # 在本群内的昵称
                                "bigHeadImgUrl": str,  # 大尺寸头像
                                "smallHeadImgUrl": str  # 小尺寸头像
                            }
                        ],
                        "chatroomOwner": str,  # 群主的wxid
                        "adminWxid": list  # 管理员的wxid列表
                    }
                }
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return self.client.request("/group/getChatroomMemberList", data)

    def get_chatroom_member_detail(
        self, chatroom_id: str, member_wxids: List[str]
    ) -> Dict:
        """获取群成员详情

        Args:
            chatroom_id (str): 群ID
            member_wxids (List[str]): 群成员的wxid列表

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": [  # 群成员详情列表
                        {
                            "userName": str,  # 群成员的wxid
                            "nickName": str,  # 群成员的昵称
                            "pyInitial": str,  # 群成员昵称的拼音首字母
                            "quanPin": str,  # 群成员昵称的全拼
                            "sex": int,  # 性别
                            "remark": str,  # 备注
                            "remarkPyInitial": str,  # 备注的拼音首字母
                            "remarkQuanPin": str,  # 备注的全拼
                            "chatRoomNotify": int,  # 消息通知
                            "signature": str,  # 签名
                            "alias": str,  # 微信号
                            "snsBgImg": str,  # 朋友圈背景图链接
                            "bigHeadImgUrl": str,  # 大尺寸头像
                            "smallHeadImgUrl": str,  # 小尺寸头像
                            "description": str,  # 描述
                            "cardImgUrl": str,  # 描述的图片链接
                            "labelList": str,  # 标签列表，多个英文逗号分隔
                            "country": str,  # 国家
                            "province": str,  # 省份
                            "city": str,  # 城市
                            "phoneNumList": list,  # 手机号码
                            "friendUserName": str,  # 好友的wxid
                            "inviterUserName": str,  # 邀请人的wxid
                            "memberFlag": int  # 标识
                        }
                    ]
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "memberWxids": member_wxids,
        }
        return self.client.request("/group/getChatroomMemberDetail", data)

    def get_chatroom_announcement(self, chatroom_id: str) -> Dict:
        """获取群公告

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "announcement": str,  # 群公告内容
                        "announcementEditor": str,  # 群公告作者的wxid
                        "publishTime": int  # 群公告发布时间
                    }
                }
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return self.client.request("/group/getChatroomAnnouncement", data)

    def set_chatroom_announcement(self, chatroom_id: str, content: str) -> Dict:
        """设置群公告

        Summary:
            仅群主或管理员可以发布群公告

        Args:
            chatroom_id (str): 群ID
            content (str): 公告内容

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "content": content,
        }
        return self.client.request("/group/setChatroomAnnouncement", data)

    def agree_join_room(self, url: str) -> Dict:
        """同意进群

        Args:
            url (str): 邀请进群回调消息中的url

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "chatroomId": str  # 群ID
                    }
                }
        """
        data = {"appId": self.client.app_id, "url": url}
        return self.client.request("/group/agreeJoinRoom", data)

    def add_group_member_as_friend(
        self, chatroom_id: str, member_wxid: str, content: str = ""
    ) -> Dict:
        """添加群成员为好友

        Summary:
            添加群成员为好友，若对方关闭从群聊添加的权限则添加失败

        Args:
            chatroom_id (str): 群ID
            member_wxid (str): 群成员的wxid
            content (str, optional): 加好友的招呼语. Defaults to "".

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "v3": str  # 添加群成员的v3，通过好友后会通过回调消息返回此值
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "memberWxid": member_wxid,
            "content": content,
        }
        return self.client.request("/group/addGroupMemberAsFriend", data)

    def get_chatroom_qrcode(self, chatroom_id: str) -> Dict:
        """获取群二维码

        Summary:
            在新设备登录后的1-3天内，无法使用本功能。
            在此期间，如果尝试进行获取，您将收到来自微信团队的提醒。
            请注意遵守相关规定。
            生成的群二维码图片7天有效。

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "qrBase64": str,  # 群二维码图片的base64
                        "qrTips": str  # 群二维码的提示
                    }
                }
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return self.client.request("/group/getChatroomQrCode", data)

    def save_contract_list(self, chatroom_id: str, oper_type: int = 3) -> Dict:
        """群保存到通讯录

        Args:
            chatroom_id (str): 群ID
            oper_type (int, optional): 操作类型 3保存到通讯录 2从通讯录移除. Defaults to 3.

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "operType": oper_type,
        }
        return self.client.request("/group/saveContractList", data)

    def admin_operate(self, chatroom_id: str, wxids: List[str], oper_type: int) -> Dict:
        """管理员操作

        Summary:
            添加、删除群管理员，转让群主

        Args:
            chatroom_id (str): 群ID
            wxids (List[str]): 群管理的wxid列表
            oper_type (int): 操作类型
                1：添加群管理（可添加多个微信号）
                2：删除群管理（可删除多个）
                3：转让（只能转让一个微信号）

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "wxids": wxids,
            "operType": oper_type,
        }
        return self.client.request("/group/adminOperate", data)

    def pin_chat(self, chatroom_id: str, top: bool) -> Dict:
        """聊天置顶

        Args:
            chatroom_id (str): 群ID
            top (bool): 是否置顶

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id, "top": top}
        return self.client.request("/group/pinChat", data)

    def set_msg_silence(self, chatroom_id: str, silence: bool) -> Dict:
        """设置消息免打扰

        Args:
            chatroom_id (str): 群ID
            silence (bool): 是否免打扰

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "silence": silence,
        }
        return self.client.request("/group/setMsgSilence", data)

    def join_room_using_qrcode(self, qr_url: str) -> Dict:
        """扫码进群

        Summary:
            qrUrl是通过解析群二维码图片获得的内容

        Args:
            qr_url (str): 二维码的链接

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "chatroomName": str,  # 群名称
                        "html": str,  # html内容
                        "chatroomId": str  # 群ID
                    }
                }
        """
        data = {"appId": self.client.app_id, "qrUrl": qr_url}
        return self.client.request("/group/joinRoomUsingQRCode", data)

    def room_access_apply_check_approve(
        self, chatroom_id: str, new_msg_id: str, msg_content: str
    ) -> Dict:
        """确认进群申请

        Summary:
            群聊开启邀请确认后，有人申请进群时群主和管理员会收到进群申请，
            本接口用于确认进群申请

        Args:
            chatroom_id (str): 群ID
            new_msg_id (str): 消息ID
            msg_content (str): 消息内容

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "newMsgId": new_msg_id,
            "msgContent": msg_content,
        }
        return self.client.request("/group/roomAccessApplyCheckApprove", data)
