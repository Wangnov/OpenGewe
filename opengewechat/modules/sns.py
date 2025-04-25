from typing import Dict, List


class SnsModule:
    """朋友圈模块

    朋友圈相关接口，包括朋友圈发布、点赞、评论等功能。注意：该模块为付费功能，需要判断is_gewe才能使用。

    在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

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
            print("朋友圈模块为付费功能，需要付费版gewe才能使用")
            return False
        return True

    def like_sns(self, sns_id: int, oper_type: int, wxid: str) -> Dict:
        """点赞/取消点赞

        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

        Args:
            sns_id: 朋友圈ID
            oper_type: 操作类型，1点赞 2取消点赞
            wxid: 朋友圈作者的wxid

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "snsId": sns_id,
            "operType": oper_type,
            "wxid": wxid
        }
        return self.client.request("/gewe/v2/api/sns/likeSns", data)

    def del_sns(self, sns_id: int) -> Dict:
        """删除朋友圈

        Args:
            sns_id: 朋友圈ID

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "snsId": sns_id
        }
        return self.client.request("/gewe/v2/api/sns/delSns", data)

    def set_sns_visible_scope(self, option: int) -> Dict:
        """设置朋友圈可见范围

        Args:
            option: 朋友圈可见范围选项，可选值：
                    1: 全部
                    2: 最近半年
                    3: 最近一个月
                    4: 最近三天

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "option": option
        }
        return self.client.request("/gewe/v2/api/sns/snsVisibleScope", data)

    def set_stranger_visibility(self, enabled: bool) -> Dict:
        """设置是否允许陌生人查看朋友圈

        Args:
            enabled: 是否允许陌生人查看朋友圈

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "enabled": enabled
        }
        return self.client.request("/gewe/v2/api/sns/strangerVisibilityEnabled", data)

    def set_sns_privacy(self, sns_id: int, open: bool) -> Dict:
        """设置某条朋友圈为隐私/公开

        Args:
            sns_id: 朋友圈ID
            open: 是否公开

        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "snsId": sns_id,
            "open": open
        }
        return self.client.request("/gewe/v2/api/sns/snsSetPrivacy", data)

    def download_sns_video(self, sns_xml: str) -> Dict:
        """下载朋友圈视频

        Args:
            sns_xml: 朋友圈的xml内容

        Returns:
            Dict: 响应结果，包含视频下载地址
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}

        data = {
            "appId": self.client.app_id,
            "snsXml": sns_xml
        }
        return self.client.request("/gewe/v2/api/sns/downloadSnsVideo", data)

    def send_text_sns(self, content: str, allow_wxids: List[str] = None, at_wxids: List[str] = None, 
                       disable_wxids: List[str] = None, privacy: bool = False, 
                       allow_tag_ids: List[str] = None, disable_tag_ids: List[str] = None) -> Dict:
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
            Dict: 响应结果，包含朋友圈ID等信息
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
            "disableTagIds": disable_tag_ids or []
        }
        return self.client.request("/gewe/v2/api/sns/sendTextSns", data)
        
    def send_img_sns(self, img_infos: List[Dict], content: str = "", allow_wxids: List[str] = None, 
                     at_wxids: List[str] = None, disable_wxids: List[str] = None, privacy: bool = False, 
                     allow_tag_ids: List[str] = None, disable_tag_ids: List[str] = None) -> Dict:
        """发送图片朋友圈
        
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
        
        Args:
            img_infos: 图片信息列表，通过upload_sns_image方法获取，格式为：
                      [{"fileUrl": "...", "thumbUrl": "...", "fileMd5": "...", "length": 1234, "width": 720, "height": 1280}, ...]
            content: 朋友圈文字内容，默认为空
            allow_wxids: 允许查看的好友wxid列表，默认为空
            at_wxids: 提醒谁看的好友wxid列表，默认为空
            disable_wxids: 不允许查看的好友wxid列表，默认为空
            privacy: 是否为私密朋友圈，默认为False
            allow_tag_ids: 允许查看的标签id列表，默认为空
            disable_tag_ids: 不允许查看的标签id列表，默认为空
            
        Returns:
            Dict: 响应结果，包含朋友圈ID等信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "content": content,
            "privacy": privacy,
            "imgInfos": img_infos,
            "allowWxIds": allow_wxids or [],
            "atWxIds": at_wxids or [],
            "disableWxIds": disable_wxids or [],
            "allowTagIds": allow_tag_ids or [],
            "disableTagIds": disable_tag_ids or []
        }
        return self.client.request("/gewe/v2/api/sns/sendImgSns", data)
        
    def send_video_sns(self, video_info: Dict, content: str = "", allow_wxids: List[str] = None,
                       at_wxids: List[str] = None, disable_wxids: List[str] = None, privacy: bool = False,
                       allow_tag_ids: List[str] = None, disable_tag_ids: List[str] = None) -> Dict:
        """发送视频朋友圈
        
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
        
        Args:
            video_info: 视频信息，通过upload_sns_video方法获取，格式为：
                       {"fileUrl": "...", "thumbUrl": "...", "fileMd5": "...", "length": 1234}
            content: 朋友圈文字内容，默认为空
            allow_wxids: 允许查看的好友wxid列表，默认为空
            at_wxids: 提醒谁看的好友wxid列表，默认为空
            disable_wxids: 不允许查看的好友wxid列表，默认为空
            privacy: 是否为私密朋友圈，默认为False
            allow_tag_ids: 允许查看的标签id列表，默认为空
            disable_tag_ids: 不允许查看的标签id列表，默认为空
            
        Returns:
            Dict: 响应结果，包含朋友圈ID等信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "content": content,
            "privacy": privacy,
            "videoInfo": video_info,
            "allowWxIds": allow_wxids or [],
            "atWxIds": at_wxids or [],
            "disableWxIds": disable_wxids or [],
            "allowTagIds": allow_tag_ids or [],
            "disableTagIds": disable_tag_ids or []
        }
        return self.client.request("/gewe/v2/api/sns/sendVideoSns", data)
        
    def send_url_sns(self, title: str, description: str, link_url: str, thumb_url: str, content: str = "",
                    allow_wxids: List[str] = None, at_wxids: List[str] = None, disable_wxids: List[str] = None,
                    privacy: bool = False, allow_tag_ids: List[str] = None, disable_tag_ids: List[str] = None) -> Dict:
        """发送链接朋友圈
        
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
        
        Args:
            title: 链接标题
            description: 链接描述
            link_url: 链接地址
            thumb_url: 链接缩略图地址
            content: 朋友圈文字内容，默认为空
            allow_wxids: 允许查看的好友wxid列表，默认为空
            at_wxids: 提醒谁看的好友wxid列表，默认为空
            disable_wxids: 不允许查看的好友wxid列表，默认为空
            privacy: 是否为私密朋友圈，默认为False
            allow_tag_ids: 允许查看的标签id列表，默认为空
            disable_tag_ids: 不允许查看的标签id列表，默认为空
            
        Returns:
            Dict: 响应结果，包含朋友圈ID等信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "content": content,
            "privacy": privacy,
            "title": title,
            "description": description,
            "linkUrl": link_url,
            "thumbUrl": thumb_url,
            "allowWxIds": allow_wxids or [],
            "atWxIds": at_wxids or [],
            "disableWxIds": disable_wxids or [],
            "allowTagIds": allow_tag_ids or [],
            "disableTagIds": disable_tag_ids or []
        }
        return self.client.request("/gewe/v2/api/sns/sendUrlSns", data)
        
    def upload_sns_image(self, img_urls: List[str]) -> Dict:
        """上传朋友圈图片
        
        Args:
            img_urls: 图片链接列表，最多9张
            
        Returns:
            Dict: 响应结果，包含上传后的图片信息列表
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "imgUrls": img_urls
        }
        return self.client.request("/gewe/v2/api/sns/uploadSnsImage", data)
        
    def upload_sns_video(self, video_url: str, thumb_url: str) -> Dict:
        """上传朋友圈视频
        
        Args:
            video_url: 视频文件链接
            thumb_url: 视频封面图片链接
            
        Returns:
            Dict: 响应结果，包含上传后的视频信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "videoUrl": video_url,
            "thumbUrl": thumb_url
        }
        return self.client.request("/gewe/v2/api/sns/uploadSnsVideo", data)
        
    def forward_sns(self, sns_xml: str, allow_wxids: List[str] = None, at_wxids: List[str] = None,
                   disable_wxids: List[str] = None, privacy: bool = False,
                   allow_tag_ids: List[str] = None, disable_tag_ids: List[str] = None) -> Dict:
        """转发朋友圈
        
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
        
        Args:
            sns_xml: 朋友圈xml内容，可通过朋友圈列表接口获取
            allow_wxids: 允许查看的好友wxid列表，默认为空
            at_wxids: 提醒谁看的好友wxid列表，默认为空
            disable_wxids: 不允许查看的好友wxid列表，默认为空
            privacy: 是否为私密朋友圈，默认为False
            allow_tag_ids: 允许查看的标签id列表，默认为空
            disable_tag_ids: 不允许查看的标签id列表，默认为空
            
        Returns:
            Dict: 响应结果，包含朋友圈ID等信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "snsXml": sns_xml,
            "privacy": privacy,
            "allowWxIds": allow_wxids or [],
            "atWxIds": at_wxids or [],
            "disableWxIds": disable_wxids or [],
            "allowTagIds": allow_tag_ids or [],
            "disableTagIds": disable_tag_ids or []
        }
        return self.client.request("/gewe/v2/api/sns/forwardSns", data)
        
    def get_sns_list(self, max_id: int = 0, decrypt: bool = True, first_page_md5: str = "") -> Dict:
        """获取自己的朋友圈列表
        
        Args:
            max_id: 分页参数，首次传0，第二页及以后传接口返回的maxId
            decrypt: 是否解密朋友圈内容，默认为True
            first_page_md5: 分页参数，首次传空字符串，第二页及以后传接口返回的firstPageMd5
            
        Returns:
            Dict: 响应结果，包含朋友圈列表信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "maxId": max_id,
            "decrypt": decrypt,
            "firstPageMd5": first_page_md5
        }
        return self.client.request("/gewe/v2/api/sns/snsList", data)
        
    def get_contacts_sns_list(self, wxid: str, max_id: int = 0, decrypt: bool = True, first_page_md5: str = "") -> Dict:
        """获取联系人的朋友圈列表
        
        Args:
            wxid: 联系人的wxid
            max_id: 分页参数，首次传0，第二页及以后传接口返回的maxId
            decrypt: 是否解密朋友圈内容，默认为True
            first_page_md5: 分页参数，首次传空字符串，第二页及以后传接口返回的firstPageMd5
            
        Returns:
            Dict: 响应结果，包含联系人的朋友圈列表信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "wxid": wxid,
            "maxId": max_id,
            "decrypt": decrypt,
            "firstPageMd5": first_page_md5
        }
        return self.client.request("/gewe/v2/api/sns/contactsSnsList", data)
        
    def comment_sns(self, sns_id: int, wxid: str, content: str, reply_comment_id: int = None) -> Dict:
        """评论朋友圈
        
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。
        在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
        
        Args:
            sns_id: 朋友圈ID
            wxid: 朋友圈作者的wxid
            content: 评论内容
            reply_comment_id: 回复的评论ID，如果是直接评论朋友圈，则不需要传此参数
            
        Returns:
            Dict: 响应结果
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "snsId": sns_id,
            "wxid": wxid,
            "content": content
        }
        
        if reply_comment_id is not None:
            data["replyCommentId"] = reply_comment_id
            
        return self.client.request("/gewe/v2/api/sns/commentSns", data)
        
    def get_sns_detail(self, sns_id: int, decrypt: bool = True) -> Dict:
        """获取指定朋友圈详情
        
        Args:
            sns_id: 朋友圈ID
            decrypt: 是否解密朋友圈内容，默认为True
            
        Returns:
            Dict: 响应结果，包含朋友圈详细信息
        """
        if not self._check_is_gewe():
            return {"ret": 500, "msg": "朋友圈模块为付费功能，需要付费版gewe才能使用"}
            
        data = {
            "appId": self.client.app_id,
            "snsId": sns_id,
            "decrypt": decrypt
        }
        return self.client.request("/gewe/v2/api/sns/snsDetail", data) 