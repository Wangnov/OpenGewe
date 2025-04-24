from typing import Dict


class FavoriteModule:
    """收藏夹模块"""

    def __init__(self, client):
        self.client = client

    def sync_favorites(self, sync_key: str = "") -> Dict:
        """同步收藏夹

        Summary:
            响应结果中会包含已删除的的收藏夹记录，通过flag=1来判断已删除

        Args:
            sync_key (str, optional): 翻页key，首次传空，获取下一页传接口返回的syncKey. Defaults to "".

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "syncKey": str,  # 翻页key
                        "list": [
                            {
                                "favId": int,  # 收藏夹ID
                                "type": int,  # 收藏内容类型
                                "flag": int,  # 收藏夹标识
                                "updateTime": int  # 收藏时间
                            }
                        ]
                    }
                }
        """
        data = {"appId": self.client.app_id, "syncKey": sync_key}
        return self.client.request("/favor/sync", data)

    def get_favorite_content(self, fav_id: int) -> Dict:
        """获取收藏夹内容

        Args:
            fav_id (int): 收藏夹ID

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "favId": int,  # 收藏夹ID
                        "status": int,  # 状态
                        "flag": int,  # 收藏夹标识
                        "updateTime": int,  # 更新时间
                        "content": str  # 收藏的内容
                    }
                }
        """
        data = {"appId": self.client.app_id, "favId": fav_id}
        return self.client.request("/favor/getContent", data)

    def delete_favorite(self, fav_id: int) -> Dict:
        """删除收藏夹

        Args:
            fav_id (int): 收藏夹ID

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "favId": fav_id}
        return self.client.request("/favor/delete", data)
