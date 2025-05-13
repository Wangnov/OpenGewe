from typing import Dict, List, Union, Any


class GroupModule:
    """异步群组模块"""

    def __init__(self, client):
        self.client = client

    async def create_chatroom(self, wxids: List[str]) -> Dict[str, Any]:
        """创建微信群

        Summary:
            创建微信群时最少要选择两位微信好友

        Args:
            wxids (List[str]): 好友的wxid列表，至少2个

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "wxids": wxids}
        return await self.client.request("/group/createChatroom", data)

    async def modify_chatroom_name(
        self, chatroom_id: str, chatroom_name: str
    ) -> Dict[str, Any]:
        """修改群名称

        Summary:
            修改完群名称后若发现手机未展示修改后的名称，可能是手机缓存未刷新，
            手机聊天框多切换几次会刷新。

        Args:
            chatroom_id (str): 群ID
            chatroom_name (str): 群名称

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "chatroomName": chatroom_name,
        }
        return await self.client.request("/group/modifyChatroomName", data)

    async def modify_chatroom_remark(
        self, chatroom_id: str, chatroom_remark: str
    ) -> Dict[str, Any]:
        """修改群备注

        Summary:
            群备注仅自己可见。
            修改完群备注后若发现手机未展示修改后的备注，可能是手机缓存未刷新，
            手机聊天框多切换几次会刷新。

        Args:
            chatroom_id (str): 群ID
            chatroom_remark (str): 群备注

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "chatroomRemark": chatroom_remark,
        }
        return await self.client.request("/group/modifyChatroomRemark", data)

    async def modify_chatroom_nickname_for_self(
        self, chatroom_id: str, nickname: str
    ) -> Dict[str, Any]:
        """修改我在群内的昵称

        Args:
            chatroom_id (str): 群ID
            nickname (str): 群昵称

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "nickName": nickname,
        }
        return await self.client.request("/group/modifyChatroomNickNameForSelf", data)

    async def invite_member(
        self, chatroom_id: str, wxids: Union[List[str], str], reason: str = ""
    ) -> Dict[str, Any]:
        """邀请/添加进群

        Args:
            chatroom_id (str): 群ID
            wxids (Union[List[str], str]): 邀请进群的好友wxid，列表或者多个英文逗号分隔的字符串
            reason (str, optional): 邀请进群的说明. Defaults to "".

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if isinstance(wxids, list):
            wxids = ",".join(wxids)

        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "wxids": wxids,
            "reason": reason,
        }
        return await self.client.request("/group/inviteMember", data)

    async def remove_member(
        self, chatroom_id: str, wxids: Union[List[str], str]
    ) -> Dict[str, Any]:
        """删除群成员

        Args:
            chatroom_id (str): 群ID
            wxids (Union[List[str], str]): 删除的群成员wxid，列表或者多个英文逗号分隔的字符串

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if isinstance(wxids, list):
            wxids = ",".join(wxids)

        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "wxids": wxids,
        }
        return await self.client.request("/group/removeMember", data)

    async def quit_chatroom(self, chatroom_id: str) -> Dict[str, Any]:
        """退出群聊

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return await self.client.request("/group/quitChatroom", data)

    async def get_chatroom_info(self, chatroom_id: str) -> Dict[str, Any]:
        """获取群信息

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return await self.client.request("/group/getChatroomInfo", data)

    async def get_chatroom_member_list(self, chatroom_id: str) -> Dict[str, Any]:
        """获取群成员列表

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return await self.client.request("/group/getChatroomMemberList", data)

    async def get_chatroom_member_detail(
        self, chatroom_id: str, member_wxids: List[str]
    ) -> Dict[str, Any]:
        """获取群成员详情

        Args:
            chatroom_id (str): 群ID
            member_wxids (List[str]): 群成员wxid列表

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "memberWxids": member_wxids,
        }
        return await self.client.request("/group/getChatroomMemberDetail", data)

    async def get_chatroom_announcement(self, chatroom_id: str) -> Dict[str, Any]:
        """获取群公告

        Args:
            chatroom_id (str): 群ID

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "chatroomId": chatroom_id}
        return await self.client.request("/group/getChatroomAnnouncement", data)

    async def set_chatroom_announcement(
        self, chatroom_id: str, content: str
    ) -> Dict[str, Any]:
        """设置群公告

        Args:
            chatroom_id (str): 群ID
            content (str): 公告内容

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "chatroomId": chatroom_id,
            "content": content,
        }
        return await self.client.request("/group/setChatroomAnnouncement", data)
