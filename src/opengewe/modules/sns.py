from typing import Dict, List, Any


class SnsModule:
    """异步朋友圈模块

    朋友圈相关接口，包括朋友圈发布、点赞、评论等功能。注意：该模块为付费功能，需要判断is_gewe才能使用。

    在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

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
        #     print("朋友圈模块为付费功能，需要付费版gewe才能使用")
        #     return False
        return True

    async def like_sns(self, sns_id: int, oper_type: int, wxid: str) -> Dict[str, Any]:
        """点赞/取消点赞

        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

        Args:
            sns_id: 朋友圈ID
            oper_type: 操作类型，1点赞 2取消点赞
            wxid: 朋友圈作者的wxid

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "snsId": sns_id,
            "operType": oper_type,
            "wxid": wxid,
        }
        return await self.client.request("/sns/likeSns", data)

    async def del_sns(self, sns_id: int) -> Dict[str, Any]:
        """删除朋友圈

        Args:
            sns_id: 朋友圈ID

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "snsId": sns_id}
        return await self.client.request("/sns/delSns", data)

    async def sns_visible_scope(self, option: int) -> Dict[str, Any]:
        """设置朋友圈可见范围

        Args:
            option: 朋友圈可见范围选项，可选值：
                    1: 全部
                    2: 最近半年
                    3: 最近一个月
                    4: 最近三天

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "option": option}
        return await self.client.request("/sns/snsVisibleScope", data)

    async def stranger_visibility_enabled(self, open: bool) -> Dict[str, Any]:
        """是否允许陌生人查看朋友圈

        Args:
            open: 是否允许陌生人查看朋友圈

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "open": open}
        return await self.client.request("/sns/strangerVisibilityEnabled", data)

    async def sns_set_privacy(self, sns_id: int, privacy: bool) -> Dict[str, Any]:
        """设置某条朋友圈为隐私/公开

        Args:
            sns_id: 朋友圈ID
            privacy: 是否为隐私朋友圈

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "snsId": sns_id, "privacy": privacy}
        return await self.client.request("/sns/snsSetPrivacy", data)

    async def download_sns_video(self, xml: str) -> Dict[str, Any]:
        """下载朋友圈视频

        Args:
            xml: 朋友圈视频XML

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "xml": xml}
        return await self.client.request("/sns/downloadSnsVideo", data)

    async def send_text_sns(
        self,
        content: str,
        allow_wxids: List[str] = None,
        at_wxids: List[str] = None,
        disable_wxids: List[str] = None,
        privacy: bool = False,
        allow_tag_ids: List[str] = None,
        disable_tag_ids: List[str] = None,
    ) -> Dict[str, Any]:
        """发送文字朋友圈

        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

        Args:
            content: 朋友圈文字内容
            allow_wxids: 允许查看的好友wxid列表，默认为空
            at_wxids: 提醒谁看的好友wxid列表，默认为空
            disable_wxids: 不允许查看的好友wxid列表，默认为空
            privacy: 是否为私密朋友圈，默认为False
            allow_tag_ids: 允许查看的标签id列表，默认为空
            disable_tag_ids: 不允许查看的标签id列表，默认为空

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "content": content,
            "privacy": privacy,
            "allowWxIds": allow_wxids or [],
            "atWxIds": at_wxids or [],
            "disableWxIds": disable_wxids or [],
            "allowTagIds": allow_tag_ids or [],
            "disableTagIds": disable_tag_ids or [],
        }
        return await self.client.request("/sns/sendTextSns", data)

    async def send_img_sns(
        self,
        content: str,
        img_urls: List[str],
        allow_wxids: List[str] = None,
        at_wxids: List[str] = None,
        disable_wxids: List[str] = None,
        privacy: bool = False,
        allow_tag_ids: List[str] = None,
        disable_tag_ids: List[str] = None,
    ) -> Dict[str, Any]:
        """发送图片朋友圈

        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

        Args:
            content: 朋友圈文字内容
            img_urls: 图片url列表
            allow_wxids: 允许查看的好友wxid列表，默认为空
            at_wxids: 提醒谁看的好友wxid列表，默认为空
            disable_wxids: 不允许查看的好友wxid列表，默认为空
            privacy: 是否为私密朋友圈，默认为False
            allow_tag_ids: 允许查看的标签id列表，默认为空
            disable_tag_ids: 不允许查看的标签id列表，默认为空

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "content": content,
            "imgUrls": img_urls,
            "privacy": privacy,
            "allowWxIds": allow_wxids or [],
            "atWxIds": at_wxids or [],
            "disableWxIds": disable_wxids or [],
            "allowTagIds": allow_tag_ids or [],
            "disableTagIds": disable_tag_ids or [],
        }
        return await self.client.request("/sns/sendImgSns", data)

    async def send_video_sns(
        self,
        content: str,
        video_url: str,
        thumb_url: str,
        allow_wxids: List[str] = None,
        at_wxids: List[str] = None,
        disable_wxids: List[str] = None,
        privacy: bool = False,
        allow_tag_ids: List[str] = None,
        disable_tag_ids: List[str] = None,
    ) -> Dict[str, Any]:
        """发送视频朋友圈

        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

        Args:
            content: 朋友圈文字内容
            video_url: 视频url
            thumb_url: 视频封面图url
            allow_wxids: 允许查看的好友wxid列表，默认为空
            at_wxids: 提醒谁看的好友wxid列表，默认为空
            disable_wxids: 不允许查看的好友wxid列表，默认为空
            privacy: 是否为私密朋友圈，默认为False
            allow_tag_ids: 允许查看的标签id列表，默认为空
            disable_tag_ids: 不允许查看的标签id列表，默认为空

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "content": content,
            "videoUrl": video_url,
            "thumbUrl": thumb_url,
            "privacy": privacy,
            "allowWxIds": allow_wxids or [],
            "atWxIds": at_wxids or [],
            "disableWxIds": disable_wxids or [],
            "allowTagIds": allow_tag_ids or [],
            "disableTagIds": disable_tag_ids or [],
        }
        return await self.client.request("/sns/sendVideoSns", data)

    async def send_url_sns(
        self,
        content: str,
        url: str,
        title: str,
        allow_wxids: List[str] = None,
        at_wxids: List[str] = None,
        disable_wxids: List[str] = None,
        privacy: bool = False,
        allow_tag_ids: List[str] = None,
        disable_tag_ids: List[str] = None,
    ) -> Dict[str, Any]:
        """发送链接朋友圈

        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

        Args:
            content: 朋友圈文字内容
            url: 链接url
            title: 链接标题
            allow_wxids: 允许查看的好友wxid列表，默认为空
            at_wxids: 提醒谁看的好友wxid列表，默认为空
            disable_wxids: 不允许查看的好友wxid列表，默认为空
            privacy: 是否为私密朋友圈，默认为False
            allow_tag_ids: 允许查看的标签id列表，默认为空
            disable_tag_ids: 不允许查看的标签id列表，默认为空

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "content": content,
            "url": url,
            "title": title,
            "privacy": privacy,
            "allowWxIds": allow_wxids or [],
            "atWxIds": at_wxids or [],
            "disableWxIds": disable_wxids or [],
            "allowTagIds": allow_tag_ids or [],
            "disableTagIds": disable_tag_ids or [],
        }
        return await self.client.request("/sns/sendUrlSns", data)

    async def upload_sns_image(self, image_url: str) -> Dict[str, Any]:
        """上传朋友圈图片

        Args:
            image_url: 图片URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "imageUrl": image_url}
        return await self.client.request("/sns/uploadSnsImage", data)

    async def upload_sns_video(self, video_url: str, thumb_url: str) -> Dict[str, Any]:
        """上传朋友圈视频

        Args:
            video_url: 视频URL
            thumb_url: 视频封面图URL

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "videoUrl": video_url,
            "thumbUrl": thumb_url,
        }
        return await self.client.request("/sns/uploadSnsVideo", data)

    async def forward_sns(self, sns_id: int, wxid: str) -> Dict[str, Any]:
        """转发朋友圈

        Args:
            sns_id: 朋友圈ID
            wxid: 朋友圈作者wxid

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "snsId": sns_id, "wxid": wxid}
        return await self.client.request("/sns/forwardSns", data)

    async def sns_list(
        self, max_id: int = 0, decrypt: bool = True, first_page_md5: str = ""
    ) -> Dict[str, Any]:
        """自己的朋友圈列表

        Args:
            max_id: 翻页参数，默认为0表示获取最新一页，后续传接口返回的maxId
            decrypt: 是否需要解密，默认为True
            first_page_md5: 首页md5，默认为空字符串

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "maxId": max_id,
            "decrypt": decrypt,
            "firstPageMd5": first_page_md5,
        }
        return await self.client.request("/sns/snsList", data)

    async def contacts_sns_list(
        self, wxid: str, max_id: int = 0, decrypt: bool = True, first_page_md5: str = ""
    ) -> Dict[str, Any]:
        """联系人的朋友圈列表

        Args:
            wxid: 联系人wxid
            max_id: 翻页参数，默认为0表示获取最新一页，后续传接口返回的maxId
            decrypt: 是否需要解密，默认为True
            first_page_md5: 首页md5，默认为空字符串

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "wxid": wxid,
            "maxId": max_id,
            "decrypt": decrypt,
            "firstPageMd5": first_page_md5,
        }
        return await self.client.request("/sns/contactsSnsList", data)

    async def sns_details(self, sns_id: int, wxid: str) -> Dict[str, Any]:
        """某条朋友圈详情

        Args:
            sns_id: 朋友圈ID
            wxid: 朋友圈作者wxid

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {"appId": self.client.app_id, "snsId": sns_id, "wxid": wxid}
        return await self.client.request("/sns/snsDetails", data)

    async def comment_sns(
        self, sns_id: int, wxid: str, content: str, reply_comment_id: int = None, delete: bool = False
    ) -> Dict[str, Any]:
        """评论/删除评论

        Args:
            sns_id: 朋友圈ID
            wxid: 朋友圈作者的wxid
            content: 评论内容
            reply_comment_id: 回复的评论ID，默认为None表示直接评论朋友圈
            delete: 是否删除评论，默认为False

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "snsId": sns_id,
            "wxid": wxid,
            "content": content,
            "delete": delete,
        }

        if reply_comment_id is not None:
            data["replyCommentId"] = reply_comment_id

        return await self.client.request("/sns/commentSns", data)

    async def send_finder_sns(
        self,
        content: str,
        finder_username: str,
        allow_wxids: List[str] = None,
        at_wxids: List[str] = None,
        disable_wxids: List[str] = None,
        privacy: bool = False,
        allow_tag_ids: List[str] = None,
        disable_tag_ids: List[str] = None,
    ) -> Dict[str, Any]:
        """发送视频号朋友圈

        Args:
            content: 朋友圈文字内容
            finder_username: 视频号用户名
            allow_wxids: 允许查看的好友wxid列表，默认为空
            at_wxids: 提醒谁看的好友wxid列表，默认为空
            disable_wxids: 不允许查看的好友wxid列表，默认为空
            privacy: 是否为私密朋友圈，默认为False
            allow_tag_ids: 允许查看的标签id列表，默认为空
            disable_tag_ids: 不允许查看的标签id列表，默认为空

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "content": content,
            "finderUsername": finder_username,
            "privacy": privacy,
            "allowWxIds": allow_wxids or [],
            "atWxIds": at_wxids or [],
            "disableWxIds": disable_wxids or [],
            "allowTagIds": allow_tag_ids or [],
            "disableTagIds": disable_tag_ids or [],
        }
        return await self.client.request("/sns/sendFinderSns", data)