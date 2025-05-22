from typing import Dict, List, Any


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
        # if not self.client.is_gewe:
        #     print("视频号模块为付费功能，需要付费版gewe才能使用")
        #     return False
        return True

    async def follow(
        self,
        my_username: str,
        my_role_type: int,
        to_username: str,
        op_type: int = 1,
        search_info: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """关注视频号

        Args:
            my_username (str): 自己的username
            my_role_type (int): 自己的roletype
            to_username (str): 对方的username
            op_type (int, optional): 操作类型，1表示关注，2表示取消关注. Defaults to 1.
            search_info (Dict[str, str], optional): 如果是通过搜索渠道关注，则需要传入搜索接口返回的cookies、searchId、docId. Defaults to None.

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "myUserName": my_username,
            "myRoleType": my_role_type,
            "toUserName": to_username,
            "opType": op_type
        }
        
        # 如果提供了搜索信息，添加到请求数据中
        if search_info:
            data["searchInfo"] = search_info
            
        return await self.client.request("/finder/follow", data)

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
        return await self.client.request("/finder/comment", data)

    async def browse(self, vid: str) -> Dict[str, Any]:
        """浏览视频号视频

        Args:
            vid: 视频ID

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "vid": vid}
        return await self.client.request("/finder/browse", data)

    async def publish_finder_web(
        self,
        video_url: str,
        description: str = "",
        thumb_url: str = "",
        location: str = "",
        at_wxids: List[str] = None,
        goods_id: str = "",
        webview_url: str = "",
        webview_url_hash: str = "",
    ) -> Dict[str, Any]:
        """发布视频-新

        Args:
            video_url: 视频URL
            description: 视频描述
            thumb_url: 视频封面图URL
            location: 位置信息
            at_wxids: @的好友wxid列表
            goods_id: 商品ID
            webview_url: 网页链接
            webview_url_hash: 网页链接hash

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "videoUrl": video_url,
            "description": description,
            "thumbUrl": thumb_url,
            "location": location,
            "atWxids": at_wxids or [],
            "goodsId": goods_id,
            "webviewUrl": webview_url,
            "webviewUrlHash": webview_url_hash,
        }
        return await self.client.request("/finder/publishFinderWeb", data)

    async def user_page(self, finder_username: str) -> Dict[str, Any]:
        """用户主页

        Args:
            finder_username: 视频号用户名

        Returns:
            Dict[str, Any]: 接口返回结果，包含用户信息和视频列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "finderUsername": finder_username}
        return await self.client.request("/finder/userPage", data)

    async def follow_list(
        self, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """关注列表

        Args:
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict[str, Any]: 接口返回结果，包含关注的视频号列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "page": page, "pageSize": page_size}
        return await self.client.request("/finder/followList", data)

    async def mention_list(
        self, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """消息列表

        Args:
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict[str, Any]: 接口返回结果，包含视频号消息列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "page": page, "pageSize": page_size}
        return await self.client.request("/finder/mentionList", data)

    async def comment_list(
        self, vid: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """评论列表

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
        return await self.client.request("/finder/commentList", data)

    async def like_fav_list(
        self, option: int, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """获取赞与收藏的视频列表

        Args:
            option: 类型 1:点赞的视频列表 2:收藏的视频列表
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict[str, Any]: 接口返回结果，包含列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "option": option,
            "page": page,
            "pageSize": page_size,
        }
        return await self.client.request("/finder/likeFavList", data)

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
        return await self.client.request("/finder/search", data)

    async def create_finder(self, nickname: str, intro: str = "") -> Dict[str, Any]:
        """创建视频号

        Args:
            nickname: 昵称
            intro: 简介

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "nickname": nickname,
            "intro": intro,
        }
        return await self.client.request("/finder/createFinder", data)

    async def sync_private_letter_msg(self, username: str) -> Dict[str, Any]:
        """同步私信消息

        Args:
            username: 视频号用户名

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "username": username}
        return await self.client.request("/finder/syncPrivateLetterMsg", data)

    async def id_fav(self, id: str, vid: str, status: bool = True) -> Dict[str, Any]:
        """根据id点赞

        Args:
            id: ID
            vid: 视频ID
            status: 状态，默认True表示点赞，False表示取消点赞

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "id": id, "vid": vid, "status": status}
        return await self.client.request("/finder/idFav", data)

    async def id_like(self, id: str, vid: str, status: bool = True) -> Dict[str, Any]:
        """根据id点小红心

        Args:
            id: ID
            vid: 视频ID
            status: 状态，默认True表示点赞，False表示取消点赞

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "id": id, "vid": vid, "status": status}
        return await self.client.request("/finder/idLike", data)

    async def get_profile(self) -> Dict[str, Any]:
        """获取我的视频号信息

        Returns:
            Dict[str, Any]: 接口返回结果，包含视频号信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id}
        return await self.client.request("/finder/getProfile", data)

    async def update_profile(
        self, nickname: str = "", intro: str = "", head_img_url: str = ""
    ) -> Dict[str, Any]:
        """修改我的视频号信息

        Args:
            nickname: 昵称
            intro: 简介
            head_img_url: 头像URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "nickname": nickname,
            "intro": intro,
            "headImgUrl": head_img_url,
        }
        return await self.client.request("/finder/updateProfile", data)

    async def contact_list(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """获取私信人信息

        Args:
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "page": page, "pageSize": page_size}
        return await self.client.request("/finder/contactList", data)

    async def post_private_letter(
        self, username: str, content: str
    ) -> Dict[str, Any]:
        """发私信文本消息

        Args:
            username: 视频号用户名
            content: 消息内容

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "username": username,
            "content": content,
        }
        return await self.client.request("/finder/postPrivateLetter", data)

    async def post_private_letter_img(
        self, username: str, img_url: str
    ) -> Dict[str, Any]:
        """发私信图片消息

        Args:
            username: 视频号用户名
            img_url: 图片URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "username": username, "imgUrl": img_url}
        return await self.client.request("/finder/postPrivateLetterImg", data)

    async def scan_follow(self, url: str) -> Dict[str, Any]:
        """扫码关注

        Args:
            url: 二维码URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "url": url}
        return await self.client.request("/finder/scanFollow", data)

    async def search_follow(self, keyword: str) -> Dict[str, Any]:
        """搜索并关注

        Args:
            keyword: 搜索关键词

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "keyword": keyword}
        return await self.client.request("/finder/searchFollow", data)

    async def scan_browse(self, url: str) -> Dict[str, Any]:
        """扫码浏览

        Args:
            url: 二维码URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "url": url}
        return await self.client.request("/finder/scanBrowse", data)

    async def scan_comment(self, url: str, content: str) -> Dict[str, Any]:
        """扫码评论

        Args:
            url: 二维码URL
            content: 评论内容

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "url": url, "content": content}
        return await self.client.request("/finder/scanComment", data)

    async def scan_fav(self, url: str) -> Dict[str, Any]:
        """扫码点赞

        Args:
            url: 二维码URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "url": url}
        return await self.client.request("/finder/scanFav", data)

    async def scan_like(self, url: str) -> Dict[str, Any]:
        """扫码点小红心

        Args:
            url: 二维码URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "url": url}
        return await self.client.request("/finder/scanLike", data)

    async def finder_opt(
        self, vid: str, username: str, option: int, event_id: str, delay: int = 0
    ) -> Dict[str, Any]:
        """延迟点赞、小红心

        Args:
            vid: 视频ID
            username: 视频号用户名
            option: 操作类型 1:点赞 2:点小红心
            event_id: 事件ID
            delay: 延迟时间，单位秒

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "vid": vid,
            "username": username,
            "option": option,
            "eventId": event_id,
            "delay": delay,
        }
        return await self.client.request("/finder/finderOpt", data)

    async def scan_login_channels(self, url: str) -> Dict[str, Any]:
        """扫码登录视频号助手

        Args:
            url: 二维码URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "url": url}
        return await self.client.request("/finder/scanLoginChannels", data)

    async def scan_qr_code(self, url: str) -> Dict[str, Any]:
        """扫码获取视频详情

        Args:
            url: 二维码URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "url": url}
        return await self.client.request("/finder/scanQrCode", data)

    async def get_qr_code(self) -> Dict[str, Any]:
        """我的视频号二维码

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id}
        return await self.client.request("/finder/getQrCode", data)

    async def upload_finder_video(
        self, video_url: str, thumb_url: str
    ) -> Dict[str, Any]:
        """上传CDN视频

        Args:
            video_url: 视频URL
            thumb_url: 视频封面图URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "videoUrl": video_url,
            "thumbUrl": thumb_url,
        }
        return await self.client.request("/finder/uploadFinderVideo", data)

    async def publish_finder_cdn(
        self,
        finder_media_id: str,
        description: str = "",
        location: str = "",
        at_wxids: List[str] = None,
        goods_id: str = "",
        webview_url: str = "",
        webview_url_hash: str = "",
    ) -> Dict[str, Any]:
        """发布CDN视频

        Args:
            finder_media_id: 视频媒体ID
            description: 视频描述
            location: 位置信息
            at_wxids: @的好友wxid列表
            goods_id: 商品ID
            webview_url: 网页链接
            webview_url_hash: 网页链接hash

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "finderMediaId": finder_media_id,
            "description": description,
            "location": location,
            "atWxids": at_wxids or [],
            "goodsId": goods_id,
            "webviewUrl": webview_url,
            "webviewUrlHash": webview_url_hash,
        }
        return await self.client.request("/finder/publishFinderCdn", data)
        