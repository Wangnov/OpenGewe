from typing import Dict, Any


class FavoriteModule:
    """异步收藏夹模块"""

    def __init__(self, client):
        self.client = client

    async def sync(self, sync_key: str = "") -> Dict[str, Any]:
        """同步收藏夹

        Summary:
            响应结果中会包含已删除的的收藏夹记录，通过flag=1来判断已删除

        Args:
            sync_key (str, optional): 翻页key，首次传空，获取下一页传接口返回的syncKey. Defaults to "".

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "syncKey": sync_key}
        return await self.client.request("/favor/sync", data)

    async def get_content(self, fav_id: int) -> Dict[str, Any]:
        """获取收藏夹内容

        Args:
            fav_id (int): 收藏夹ID

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "favId": fav_id}
        return await self.client.request("/favor/getContent", data)

    async def delete(self, fav_id: int) -> Dict[str, Any]:
        """删除收藏夹

        Args:
            fav_id (int): 收藏夹ID

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "favId": fav_id}
        return await self.client.request("/favor/delete", data)
