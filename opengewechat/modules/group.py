from typing import Dict, List


class GroupModule:
    """群模块"""

    def __init__(self, client):
        self.client = client

    def create_group(self, wxids: List[str]) -> Dict:
        """创建微信群"""
        data = {"wxids": wxids}
        return self.client.request("/group/create", data)

    def update_group_name(self, chatroom_id: str, name: str) -> Dict:
        """修改群名称"""
        data = {"chatroomId": chatroom_id, "name": name}
        return self.client.request("/group/updateName", data)

    def update_group_remark(self, chatroom_id: str, remark: str) -> Dict:
        """修改群备注"""
        data = {"chatroomId": chatroom_id, "remark": remark}
        return self.client.request("/group/updateRemark", data)

    def update_my_nickname(self, chatroom_id: str, nickname: str) -> Dict:
        """修改我在群内的昵称"""
        data = {"chatroomId": chatroom_id, "nickname": nickname}
        return self.client.request("/group/updateMyNickname", data)

    def invite_members(self, chatroom_id: str, wxids: List[str]) -> Dict:
        """邀请/添加进群"""
        data = {"chatroomId": chatroom_id, "wxids": wxids}
        return self.client.request("/group/inviteMembers", data)

    def remove_members(self, chatroom_id: str, wxids: List[str]) -> Dict:
        """删除群成员"""
        data = {"chatroomId": chatroom_id, "wxids": wxids}
        return self.client.request("/group/removeMembers", data)

    def quit_group(self, chatroom_id: str) -> Dict:
        """退出群聊"""
        data = {"chatroomId": chatroom_id}
        return self.client.request("/group/quit", data)

    def dissolve_group(self, chatroom_id: str) -> Dict:
        """解散群聊"""
        data = {"chatroomId": chatroom_id}
        return self.client.request("/group/dissolve", data)

    def get_group_info(self, chatroom_id: str) -> Dict:
        """获取群信息"""
        data = {"chatroomId": chatroom_id}
        return self.client.request("/group/info", data)

    def get_members(self, chatroom_id: str) -> Dict:
        """获取群成员列表"""
        data = {"chatroomId": chatroom_id}
        return self.client.request("/group/members", data)

    def get_member_details(self, chatroom_id: str, wxid: str) -> Dict:
        """获取群成员详情"""
        data = {"chatroomId": chatroom_id, "wxid": wxid}
        return self.client.request("/group/memberDetails", data)

    def get_announcement(self, chatroom_id: str) -> Dict:
        """获取群公告"""
        data = {"chatroomId": chatroom_id}
        return self.client.request("/group/announcement", data)

    def set_announcement(self, chatroom_id: str, announcement: str) -> Dict:
        """设置群公告"""
        data = {"chatroomId": chatroom_id, "announcement": announcement}
        return self.client.request("/group/setAnnouncement", data)

    def accept_invitation(self, ticket: str) -> Dict:
        """同意进群"""
        data = {"ticket": ticket}
        return self.client.request("/group/acceptInvitation", data)

    def add_member_as_friend(
        self, chatroom_id: str, wxid: str, message: str = ""
    ) -> Dict:
        """添加群成员为好友"""
        data = {"chatroomId": chatroom_id, "wxid": wxid, "message": message}
        return self.client.request("/group/addMemberAsFriend", data)

    def get_qrcode(self, chatroom_id: str) -> Dict:
        """获取群二维码"""
        data = {"chatroomId": chatroom_id}
        return self.client.request("/group/qrcode", data)

    def save_to_contacts(self, chatroom_id: str) -> Dict:
        """群保存到通讯录"""
        data = {"chatroomId": chatroom_id}
        return self.client.request("/group/saveToContacts", data)

    def admin_operation(self, chatroom_id: str, wxid: str, op_type: int) -> Dict:
        """管理员操作"""
        data = {"chatroomId": chatroom_id, "wxid": wxid, "opType": op_type}
        return self.client.request("/group/adminOperation", data)

    def set_top(self, chatroom_id: str, is_top: bool) -> Dict:
        """聊天置顶"""
        data = {"chatroomId": chatroom_id, "isTop": is_top}
        return self.client.request("/group/setTop", data)

    def set_mute(self, chatroom_id: str, is_mute: bool) -> Dict:
        """设置消息免打扰"""
        data = {"chatroomId": chatroom_id, "isMute": is_mute}
        return self.client.request("/group/setMute", data)

    def scan_to_join(self, qrcode: str) -> Dict:
        """扫码进群"""
        data = {"qrcode": qrcode}
        return self.client.request("/group/scanToJoin", data)

    def confirm_join_request(self, ticket: str, approve: bool) -> Dict:
        """确认进群申请"""
        data = {"ticket": ticket, "approve": approve}
        return self.client.request("/group/confirmJoinRequest", data)
