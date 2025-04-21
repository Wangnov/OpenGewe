from typing import Dict, List


class TagModule:
    """标签模块"""

    def __init__(self, client):
        self.client = client

    def add_tag(self, tag_name: str) -> Dict:
        """添加标签"""
        data = {"tagName": tag_name}
        return self.client.request("/tag/add", data)

    def delete_tag(self, tag_id: str) -> Dict:
        """删除标签"""
        data = {"tagId": tag_id}
        return self.client.request("/tag/delete", data)

    def get_tags(self) -> Dict:
        """标签列表"""
        return self.client.request("/tag/list")

    def update_friend_tags(self, wxid: str, tag_ids: List[str]) -> Dict:
        """修改好友标签"""
        data = {"wxid": wxid, "tagIds": tag_ids}
        return self.client.request("/tag/updateFriendTags", data)
