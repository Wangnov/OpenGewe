from typing import Dict, List, Optional, Union, Any, Tuple


class FinderModule:
    """视频号模块

    视频号相关接口，包括视频号关注、评论、浏览、发布等功能。注意：该模块为付费功能，需要判断is_gewe才能使用。

    Args:
        client: GewechatClient实例
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

    def follow(self, finder_username: str) -> Dict:
        """关注视频号

        Args:
            finder_username: 视频号用户名

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "finderUsername": finder_username
        }
        return self.client.request("/gewe/v2/api/finder/follow", data)

    def comment(self, vid: str, content: str) -> Dict:
        """评论视频号视频

        Args:
            vid: 视频ID
            content: 评论内容

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "vid": vid,
            "content": content
        }
        return self.client.request("/gewe/v2/api/finder/comment", data)

    def view(self, vid: str) -> Dict:
        """浏览视频号视频

        Args:
            vid: 视频ID

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "vid": vid
        }
        return self.client.request("/gewe/v2/api/finder/view", data)

    def get_user_profile(self, finder_username: str) -> Dict:
        """获取用户主页信息

        Args:
            finder_username: 视频号用户名

        Returns:
            Dict: 响应结果，包含用户信息和视频列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "finderUsername": finder_username
        }
        return self.client.request("/gewe/v2/api/finder/userProfile", data)

    def get_follow_list(self, page: int = 1, page_size: int = 20) -> Dict:
        """获取关注列表

        Args:
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict: 响应结果，包含关注的视频号列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "page": page,
            "pageSize": page_size
        }
        return self.client.request("/gewe/v2/api/finder/followList", data)

    def get_message_list(self, page: int = 1, page_size: int = 20) -> Dict:
        """获取消息列表

        Args:
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict: 响应结果，包含视频号消息列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "page": page,
            "pageSize": page_size
        }
        return self.client.request("/gewe/v2/api/finder/messageList", data)

    def get_comment_list(self, vid: str, page: int = 1, page_size: int = 20) -> Dict:
        """获取评论列表

        Args:
            vid: 视频ID
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict: 响应结果，包含视频评论列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "vid": vid,
            "page": page,
            "pageSize": page_size
        }
        return self.client.request("/gewe/v2/api/finder/commentList", data)

    def get_like_and_favorite_list(self, page: int = 1, page_size: int = 20) -> Dict:
        """获取赞与收藏的视频列表

        Args:
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict: 响应结果，包含点赞和收藏的视频列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "page": page,
            "pageSize": page_size
        }
        return self.client.request("/gewe/v2/api/finder/likeAndFavoriteList", data)

    def search(self, keyword: str, page: int = 1, page_size: int = 20) -> Dict:
        """搜索视频号

        Args:
            keyword: 搜索关键词
            page: 页码，默认第1页
            page_size: 每页数量，默认20条

        Returns:
            Dict: 响应结果，包含搜索结果列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "keyword": keyword,
            "page": page,
            "pageSize": page_size
        }
        return self.client.request("/gewe/v2/api/finder/search", data)

    def create_finder(self, name: str, intro: str = "", avatar_url: str = "") -> Dict:
        """创建视频号

        Args:
            name: 视频号名称
            intro: 视频号介绍，默认为空
            avatar_url: 视频号头像URL，默认为空

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "name": name
        }
        
        if intro:
            data["intro"] = intro
            
        if avatar_url:
            data["avatarUrl"] = avatar_url
            
        return self.client.request("/gewe/v2/api/finder/create", data)

    def sync_private_messages(self, finder_username: str) -> Dict:
        """同步视频号私信消息

        Args:
            finder_username: 视频号用户名

        Returns:
            Dict: 响应结果，包含私信消息列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "finderUsername": finder_username
        }
        return self.client.request("/gewe/v2/api/finder/syncPrivateMessages", data)

    def like_by_id(self, vid: str) -> Dict:
        """根据ID点赞视频

        Args:
            vid: 视频ID

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "vid": vid
        }
        return self.client.request("/gewe/v2/api/finder/likeById", data)

    def heart_by_id(self, vid: str) -> Dict:
        """根据ID点小红心

        Args:
            vid: 视频ID

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "vid": vid
        }
        return self.client.request("/gewe/v2/api/finder/heartById", data)

    def get_my_finder_info(self) -> Dict:
        """获取我的视频号信息

        Returns:
            Dict: 响应结果，包含我的视频号详细信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id
        }
        return self.client.request("/gewe/v2/api/finder/myFinderInfo", data)

    def update_my_finder_info(self, name: str = None, intro: str = None, avatar_url: str = None) -> Dict:
        """修改我的视频号信息

        Args:
            name: 视频号名称，默认不修改
            intro: 视频号介绍，默认不修改
            avatar_url: 视频号头像URL，默认不修改

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id
        }
        
        if name is not None:
            data["name"] = name
            
        if intro is not None:
            data["intro"] = intro
            
        if avatar_url is not None:
            data["avatarUrl"] = avatar_url
            
        return self.client.request("/gewe/v2/api/finder/updateMyFinderInfo", data)

    def send_finder_message(self, finder_username: str, content: str) -> Dict:
        """发送视频号消息

        Args:
            finder_username: 视频号用户名
            content: 消息内容

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "finderUsername": finder_username,
            "content": content
        }
        return self.client.request("/gewe/v2/api/finder/sendFinderMessage", data)

    def send_finder_moment(self, content: str, media_urls: List[str] = None) -> Dict:
        """发送视频号朋友圈

        Args:
            content: 朋友圈内容
            media_urls: 媒体文件URL列表，默认为空

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "content": content
        }
        
        if media_urls:
            data["mediaUrls"] = media_urls
            
        return self.client.request("/gewe/v2/api/finder/sendFinderMoment", data)

    def get_private_chat_user_info(self, finder_username: str) -> Dict:
        """获取私信人信息

        Args:
            finder_username: 视频号用户名

        Returns:
            Dict: 响应结果，包含私信用户的详细信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "finderUsername": finder_username
        }
        return self.client.request("/gewe/v2/api/finder/getPrivateChatUserInfo", data)
        
    def send_private_text_message(self, finder_username: str, content: str) -> Dict:
        """发送私信文本消息

        Args:
            finder_username: 视频号用户名
            content: 文本消息内容

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "finderUsername": finder_username,
            "content": content
        }
        return self.client.request("/gewe/v2/api/finder/sendPrivateTextMessage", data)
        
    def send_private_image_message(self, finder_username: str, image_url: str) -> Dict:
        """发送私信图片消息

        Args:
            finder_username: 视频号用户名
            image_url: 图片URL

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "finderUsername": finder_username,
            "imageUrl": image_url
        }
        return self.client.request("/gewe/v2/api/finder/sendPrivateImageMessage", data)
        
    def scan_follow(self, qrcode_url: str) -> Dict:
        """扫码关注视频号

        Args:
            qrcode_url: 二维码URL

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "qrcodeUrl": qrcode_url
        }
        return self.client.request("/gewe/v2/api/finder/scanFollow", data)
        
    def search_and_follow(self, keyword: str) -> Dict:
        """搜索并关注视频号

        Args:
            keyword: 搜索关键词

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "keyword": keyword
        }
        return self.client.request("/gewe/v2/api/finder/searchAndFollow", data)
        
    def scan_view(self, qrcode_url: str) -> Dict:
        """扫码浏览视频号

        Args:
            qrcode_url: 二维码URL

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "qrcodeUrl": qrcode_url
        }
        return self.client.request("/gewe/v2/api/finder/scanView", data)
        
    def scan_comment(self, qrcode_url: str, content: str) -> Dict:
        """扫码评论视频号

        Args:
            qrcode_url: 二维码URL
            content: 评论内容

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "qrcodeUrl": qrcode_url,
            "content": content
        }
        return self.client.request("/gewe/v2/api/finder/scanComment", data)
        
    def scan_like(self, qrcode_url: str) -> Dict:
        """扫码点赞视频号

        Args:
            qrcode_url: 二维码URL

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "qrcodeUrl": qrcode_url
        }
        return self.client.request("/gewe/v2/api/finder/scanLike", data)
        
    def scan_heart(self, qrcode_url: str) -> Dict:
        """扫码点小红心

        Args:
            qrcode_url: 二维码URL

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "qrcodeUrl": qrcode_url
        }
        return self.client.request("/gewe/v2/api/finder/scanHeart", data)
        
    def delay_like_heart(self, vid: str, delay_seconds: int = 60, action_type: str = "like") -> Dict:
        """延迟点赞、小红心

        Args:
            vid: 视频ID
            delay_seconds: 延迟秒数，默认60秒
            action_type: 动作类型，"like"为点赞，"heart"为点小红心，默认为"like"

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "vid": vid,
            "delaySeconds": delay_seconds,
            "actionType": action_type
        }
        return self.client.request("/gewe/v2/api/finder/delayLikeHeart", data)
        
    def scan_login_assistant(self, qrcode_url: str) -> Dict:
        """扫码登录视频号助手

        Args:
            qrcode_url: 二维码URL

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "qrcodeUrl": qrcode_url
        }
        return self.client.request("/gewe/v2/api/finder/scanLoginAssistant", data)
        
    def scan_get_video_detail(self, qrcode_url: str) -> Dict:
        """扫码获取视频详情

        Args:
            qrcode_url: 二维码URL

        Returns:
            Dict: 响应结果，包含视频详情信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "qrcodeUrl": qrcode_url
        }
        return self.client.request("/gewe/v2/api/finder/scanGetVideoDetail", data)
        
    def get_my_finder_qrcode(self) -> Dict:
        """获取我的视频号二维码

        Returns:
            Dict: 响应结果，包含视频号二维码URL
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id
        }
        return self.client.request("/gewe/v2/api/finder/myFinderQrcode", data)
        
    def upload_cdn_video(self, video_url: str, thumb_url: str = None, title: str = None) -> Dict:
        """上传CDN视频

        Args:
            video_url: 视频URL
            thumb_url: 缩略图URL，默认为空
            title: 视频标题，默认为空

        Returns:
            Dict: 响应结果，包含上传后的视频信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "videoUrl": video_url
        }
        
        if thumb_url:
            data["thumbUrl"] = thumb_url
            
        if title:
            data["title"] = title
            
        return self.client.request("/gewe/v2/api/finder/uploadCdnVideo", data)
        
    def publish_cdn_video(self, video_id: str, title: str = None, description: str = None, tags: List[str] = None) -> Dict:
        """发布CDN视频

        Args:
            video_id: 视频ID，通过upload_cdn_video获取
            title: 视频标题，默认为空
            description: 视频描述，默认为空
            tags: 视频标签列表，默认为空

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "videoId": video_id
        }
        
        if title:
            data["title"] = title
            
        if description:
            data["description"] = description
            
        if tags:
            data["tags"] = tags
            
        return self.client.request("/gewe/v2/api/finder/publishCdnVideo", data)
        
    def publish_video(self, video_url: str, thumb_url: str = None, title: str = None, 
                     description: str = None, tags: List[str] = None) -> Dict:
        """发布视频

        Args:
            video_url: 视频URL
            thumb_url: 缩略图URL，默认为空
            title: 视频标题，默认为空
            description: 视频描述，默认为空
            tags: 视频标签列表，默认为空

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "videoUrl": video_url
        }
        
        if thumb_url:
            data["thumbUrl"] = thumb_url
            
        if title:
            data["title"] = title
            
        if description:
            data["description"] = description
            
        if tags:
            data["tags"] = tags
            
        return self.client.request("/gewe/v2/api/finder/publishVideo", data)
        
    def publish_video_new(self, video_url: str, thumb_url: str = None, title: str = None,
                        description: str = None, tags: List[str] = None, location: str = None) -> Dict:
        """发布视频-新

        Args:
            video_url: 视频URL
            thumb_url: 缩略图URL，默认为空
            title: 视频标题，默认为空
            description: 视频描述，默认为空
            tags: 视频标签列表，默认为空
            location: 位置信息，默认为空

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "视频号模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "videoUrl": video_url
        }
        
        if thumb_url:
            data["thumbUrl"] = thumb_url
            
        if title:
            data["title"] = title
            
        if description:
            data["description"] = description
            
        if tags:
            data["tags"] = tags
            
        if location:
            data["location"] = location
            
        return self.client.request("/gewe/v2/api/finder/publishVideoNew", data) 