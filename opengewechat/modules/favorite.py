from typing import Dict


class FavoriteModule:
    """收藏夹模块"""

    def __init__(self, client):
        self.client = client

    def sync_favorites(self) -> Dict:
        """同步收藏夹"""
        return self.client.request("/favorite/sync")

    def get_favorites(self) -> Dict:
        """获取收藏夹内容"""
        return self.client.request("/favorite/list")

    def delete_favorite(self, favorite_id: str) -> Dict:
        """删除收藏夹"""
        data = {"favoriteId": favorite_id}
        return self.client.request("/favorite/delete", data)
