from typing import Dict, List, Any


class TagModule:
    """异步标签模块"""

    def __init__(self, client):
        self.client = client

    async def add_tag(self, label_name: str) -> Dict[str, Any]:
        """添加标签

        Summary:
            标签名称不存在则是添加标签，如果标签名称已经存在，此接口会直接返回标签名及ID

        Args:
            label_name (str): 标签名称

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "labelName": label_name}
        return await self.client.request("/label/add", data)

    async def delete_tag(self, label_ids: str) -> Dict[str, Any]:
        """删除标签

        Args:
            label_ids (str): 标签ID，多个以逗号分隔

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "labelIds": label_ids}
        return await self.client.request("/label/delete", data)

    async def list(self) -> Dict[str, Any]:
        """标签列表

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id}
        return await self.client.request("/label/list", data)

    async def modify_member_list(
        self, wx_ids: List[str], label_ids: str
    ) -> Dict[str, Any]:
        """修改好友标签

        Summary:
            由于好友标签信息存储在用户客户端，因此每次在修改时都需要进行全量修改。
            例如：好友A（wxid_123）已有标签ID为1和2，
            添加标签ID为3时，需传参：label_ids="1,2,3"，wx_ids=["wxid_123"]
            删除标签ID为1时，需传参：label_ids="2,3"，wx_ids=["wxid_123"]

        Args:
            wx_ids (List[str]): 要修改标签的好友wxid列表
            label_ids (str): 标签ID，多个以逗号分隔

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "wxIds": wx_ids, "labelIds": label_ids}
        return await self.client.request("/label/modifyMemberList", data)