from typing import Dict, Any


class FinderModule:
    """异步视频号模块

    视频号相关接口，包括视频号关注、评论、浏览、发布等功能。注意：该模块为付费功能，需要判断is_gewe才能使用。

    Args:
        client: GeweClient实例
    """

    def __init__(self, client):
        self.client = client

    def _check_is_gewe(self) -> bool:
        """检查是否为付费版gewe

        Returns:
            bool: 是否为付费版gewe
        """
        if not self.client.is_gewe:
            print("视频号模块为付费功能，需要付费版gewe才能使用")
            return False
        return True

    async def follow(self, finder_username: str) -> Dict[str, Any]:
        """关注视频号

        Args:
            finder_username: 视频号用户名

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "finderUsername": finder_username}
        return await self.client.request("/gewe/v2/api/finder/follow", data)

    async def comment(self, vid: str, content: str) -> Dict[str, Any]:
        """评论视频号视频

        Args:
            vid: 视频ID
            content: 评论内容

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "vid": vid, "content": content}
        return await self.client.request("/gewe/v2/api/finder/comment", data)

    async def view(self, vid: str) -> Dict[str, Any]:
        """浏览视频号视频

        Args:
            vid: 视频ID

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "vid": vid}
        return await self.client.request("/gewe/v2/api/finder/view", data)

    async def get_user_profile(self, finder_username: str) -> Dict[str, Any]:
        """获取用户主页信息

        Args:
            finder_username: 视频号用户名

        Returns:
            Dict[str, Any]: 接口返回结果，包含用户信息和视频列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "finderUsername": finder_username}
        return await self.client.request("/gewe/v2/api/finder/userProfile", data)

    async def get_follow_list(
        self, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """获取关注列表

        Args:
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict[str, Any]: 接口返回结果，包含关注的视频号列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "page": page, "pageSize": page_size}
        return await self.client.request("/gewe/v2/api/finder/followList", data)

    async def get_message_list(
        self, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """获取消息列表

        Args:
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict[str, Any]: 接口返回结果，包含视频号消息列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "page": page, "pageSize": page_size}
        return await self.client.request("/gewe/v2/api/finder/messageList", data)

    async def get_comment_list(
        self, vid: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """获取评论列表

        Args:
            vid: 视频ID
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict[str, Any]: 接口返回结果，包含视频评论列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "vid": vid,
            "page": page,
            "pageSize": page_size,
        }
        return await self.client.request("/gewe/v2/api/finder/commentList", data)

    async def search(
        self, keyword: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """搜索视频号

        Args:
            keyword: 搜索关键词
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict[str, Any]: 接口返回结果，包含搜索结果列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "keyword": keyword,
            "page": page,
            "pageSize": page_size,
        }
        return await self.client.request("/gewe/v2/api/finder/search", data)
