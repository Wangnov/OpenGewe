from typing import Dict


class MessageModule:
    """消息模块"""

    def __init__(self, client):
        self.client = client

    def download_image(self, xml: str, image_type: int = 2) -> Dict:
        """下载图片

        Summary:
            下载图片，支持高清图片、常规图片和缩略图。注意 如果下载图片失败，可尝试下载另外两种图片类型，并非所有图片都会有高清、常规图片

        Args:
            xml (str): 回调消息中的XML
            image_type (int, optional): 下载的图片类型 1:高清图片 2:常规图片 3:缩略图. Defaults to 2.

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "fileUrl": str  # 图片链接地址，7天有效
                    }
                }
        """
        data = {"appId": self.client.app_id, "xml": xml, "type": image_type}
        return self.client.request("/message/downloadImage", data)

    def download_voice(self, xml: str, msg_id: int) -> Dict:
        """下载语音

        Summary:
            下载语音文件

        Args:
            xml (str): 回调消息中的XML
            msg_id (int): 回调消息中的msgId

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "fileUrl": str  # 语音文件链接地址，7天有效
                    }
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "xml": xml, "msgId": msg_id}
        return self.client.request("/message/downloadVoice", data)

    def download_video(self, xml: str) -> Dict:
        """下载视频

        Summary:
            下载视频文件

        Args:
            xml (str): 回调消息中的XML

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "fileUrl": str  # 视频文件链接地址，7天有效
                    }
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "xml": xml}
        return self.client.request("/message/downloadVideo", data)

    def download_file(self, xml: str) -> Dict:
        """下载文件

        Summary:
            下载文件

        Args:
            xml (str): 回调消息中的XML

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "fileUrl": str  # 文件链接地址，7天有效
                    }
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "xml": xml}
        return self.client.request("/message/downloadFile", data)

    def download_emoji(self, md5: str) -> Dict:
        """下载语音

        Summary:
            下载emoji文件

        Args:
            md5 (str): 回调消息中的md5

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "url": str  # emoji表情链接地址，7天有效
                    }
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "md5": md5}
        return self.client.request("/message/downloadEmojiMd5", data)

    def download_cdn(
        self,
        aes_key: str,
        file_id: str,
        file_type: str,
        total_size: str,
        suffix: str = "",
    ) -> Dict:
        """下载cdn文件

        Summary:
            下载cdn文件，支持多种文件类型下载
            注意：如果是下载图片失败，可尝试下载另外两种图片类型，并非所有图片都会有高清、常规图片

        Args:
            aes_key (str): cdn的aeskey
            file_id (str): cdn的fileid
            file_type (str): 下载的文件类型 1：高清图片 2：常规图片 3：缩略图 4：视频 5：文件
            total_size (str): 文件大小
            suffix (str, optional): 下载类型为文件时，传文件的后缀（例：doc）

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "fileUrl": str  # 文件链接地址，7天有效
                    }
                }
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {
            "appId": self.client.app_id,
            "aesKey": aes_key,
            "fileId": file_id,
            "type": file_type,
            "totalSize": total_size,
            "suffix": suffix,
        }
        return self.client.request("/message/downloadCdn", data)

    def send_text(self, to_wxid: str, content: str, at_wxid_list: list = []) -> Dict:
        """发送文字消息

        Summary:
            发送文字消息，群消息可@群成员
            在群内发送消息@某人时，content中需包含@xxx

        Args:
            to_wxid (str): 好友/群的ID
            content (str): 消息内容
            at_wxid_list (list, optional): @的好友，多个英文逗号分隔。群主或管理员@全部的人，则填写'notify@all'. Defaults to [].

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "content": content,
        }
        if at_wxid_list != []:
            data["ats"] = at_wxid_list
        return self.client.request("/message/postText", data)

    def send_file(self, to_wxid: str, file_url: str, file_name: str) -> Dict:
        """发送文件消息

        Args:
            to_wxid (str): 好友/群的ID
            file_url (str): 文件链接
            file_name (str): 文件名

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "fileUrl": file_url,
            "fileName": file_name,
        }
        return self.client.request("/message/postFile", data)

    def send_image(self, to_wxid: str, image_url: str) -> Dict:
        """发送图片消息

        Summary:
            发送图片接口会返回cdn相关的信息，如有需求同一张图片发送多次，第二次及以后发送时可使用接口返回的
            cdn信息拼装xml调用转发图片接口，这样可以缩短发送时间

        Args:
            to_wxid (str): 好友/群的ID
            image_url (str): 图片链接

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": null,  # 消息类型
                        "aesKey": str,  # cdn相关的aeskey
                        "fileId": str,  # cdn相关的fileid
                        "length": int,  # 图片文件大小
                        "width": int,  # 图片宽度
                        "height": int,  # 图片高度
                        "md5": str  # 图片md5
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "imgUrl": image_url,
        }
        return self.client.request("/message/postImage", data)

    def send_voice(self, to_wxid: str, voice_url: str, voice_duration: int) -> Dict:
        """发送语音消息

        Args:
            to_wxid (str): 好友/群的ID
            voice_url (str): 语音文件的链接，仅支持silk格式
            voice_duration (int): 语音时长，单位毫秒

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "voiceUrl": voice_url,
            "voiceDuration": voice_duration,
        }
        return self.client.request("/message/postVoice", data)

    def send_video(
        self, to_wxid: str, video_url: str, thumb_url: str, video_duration: int
    ) -> Dict:
        """发送视频消息

        Summary:
            发送视频接口会返回cdn相关的信息，如有需求同一个视频发送多次，第二次及以后发送时可使用接口返回的
            cdn信息拼装xml调用转发视频接口，这样可以缩短发送时间

        Args:
            to_wxid (str): 好友/群的ID
            video_url (str): 视频的链接
            thumb_url (str): 缩略图的链接
            video_duration (int): 视频的播放时长，单位秒

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": null,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": null,  # 消息类型
                        "aesKey": str,  # cdn相关的aeskey
                        "fileId": str,  # cdn相关的fileid
                        "length": int  # 视频文件大小
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "videoUrl": video_url,
            "thumbUrl": thumb_url,
            "videoDuration": video_duration,
        }
        return self.client.request("/message/postVideo", data)

    def send_link(
        self, to_wxid: str, title: str, desc: str, url: str, image_url: str = ""
    ) -> Dict:
        """发送链接消息

        Args:
            to_wxid (str): 好友/群的ID
            title (str): 链接标题
            desc (str): 链接描述
            url (str): 链接地址
            image_url (str, optional): 链接缩略图地址. Defaults to "".

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "title": title,
            "desc": desc,
            "linkUrl": url,
            "thumbUrl": image_url,
        }
        return self.client.request("/message/postLink", data)

    def send_card(self, to_wxid: str, card_wxid: str, nick_name: str) -> Dict:
        """发送名片消息

        Args:
            to_wxid (str): 好友/群的ID
            card_wxid (str): 名片的wxid
            nick_name (str): 名片的昵称

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "nameCardWxid": card_wxid,
            "nickName": nick_name,
        }
        return self.client.request("/message/postNameCard", data)

    def send_emoji(self, to_wxid: str, emoji_md5: str, emoji_size: int) -> Dict:
        """发送emoji消息

        Args:
            to_wxid (str): 好友/群的ID
            emoji_md5 (str): emoji图片的md5
            emoji_size (int): emoji的文件大小

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "emojiMd5": emoji_md5,
            "emojiSize": emoji_size,
        }
        return self.client.request("/message/postEmoji", data)

    def send_appmsg(self, to_wxid: str, app_msg: str) -> Dict:
        """发送appmsg消息

        Summary:
            本接口可用于发送所有包含<appmsg>节点的消息，例如：音乐分享、视频号、引用消息等等

        Args:
            to_wxid (str): 好友/群的ID
            app_msg (str): 回调消息中的appmsg节点内容

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "appmsg": app_msg,
        }
        return self.client.request("/message/postAppMsg", data)

    def send_miniapp(
        self,
        to_wxid: str,
        mini_app_id: str,
        user_name: str,
        title: str,
        cover_img_url: str,
        page_path: str,
        display_name: str,
    ) -> Dict:
        """发送小程序消息

        Args:
            to_wxid (str): 好友/群的ID
            mini_app_id (str): 小程序ID
            user_name (str): 归属的用户ID
            title (str): 小程序标题
            cover_img_url (str): 小程序封面图链接
            page_path (str): 小程序打开的地址
            display_name (str): 小程序名称

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """

        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "miniAppId": mini_app_id,
            "userName": user_name,
            "title": title,
            "coverImgUrl": cover_img_url,
            "pagePath": page_path,
            "displayName": display_name,
        }
        return self.client.request("/message/postMiniApp", data)

    def forward_file(self, to_wxid: str, xml: str) -> Dict:
        """转发文件

        Args:
            to_wxid (str): 好友/群的ID
            xml (str): 文件消息的xml

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "xml": xml,
        }
        return self.client.request("/message/forwardFile", data)

    def forward_image(self, to_wxid: str, xml: str) -> Dict:
        """转发图片

        Summary:
            若通过发送图片消息获取cdn信息后可替换xml中的aeskey、cdnthumbaeskey、cdnthumburl、cdnmidimgurl、length、md5等参数来进行转发

        Args:
            to_wxid (str): 好友/群的ID
            xml (str): 图片消息的xml

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": null,  # 消息类型
                        "aesKey": str,  # cdn相关的aeskey
                        "fileId": str,  # cdn相关的fileid
                        "length": int,  # 图片文件大小
                        "width": int,  # 图片宽度
                        "height": int,  # 图片高度
                        "md5": str  # 图片md5
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "xml": xml,
        }
        return self.client.request("/message/forwardImage", data)

    def forward_video(self, to_wxid: str, xml: str) -> Dict:
        """转发视频

        Summary:
            若通过发送视频消息获取cdn信息后可替换xml中的aeskey、cdnthumbaeskey、cdnvideourl、cdnthumburl、length等参数来进行转发

        Args:
            to_wxid (str): 好友/群的ID
            xml (str): 视频消息的xml

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": null,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": null,  # 消息类型
                        "aesKey": str,  # cdn相关的aeskey
                        "fileId": str,  # cdn相关的fileid
                        "length": int  # 视频文件大小
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "xml": xml,
        }
        return self.client.request("/message/forwardVideo", data)

    def forward_link(self, to_wxid: str, xml: str) -> Dict:
        """转发链接

        Args:
            to_wxid (str): 好友/群的ID
            xml (str): 链接消息的xml

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "xml": xml,
        }
        return self.client.request("/message/forwardUrl", data)

    def forward_miniapp(self, to_wxid: str, xml: str, cover_img_url: str) -> Dict:
        """转发小程序

        Args:
            to_wxid (str): 好友/群的ID
            xml (str): 小程序消息的xml
            cover_img_url (str): 小程序封面图链接

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "toWxid": str,  # 接收人的wxid
                        "createTime": int,  # 发送时间
                        "msgId": int,  # 消息ID
                        "newMsgId": int,  # 消息ID
                        "type": int  # 消息类型
                    }
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "xml": xml,
            "coverImgUrl": cover_img_url,
        }
        return self.client.request("/message/forwardMiniApp", data)

    def revoke_message(
        self, to_wxid: str, msg_id: str, new_msg_id: str, create_time: str
    ) -> Dict:
        """撤回消息

        Args:
            to_wxid (str): 好友/群的ID
            msg_id (str): 发送类接口返回的msgId
            new_msg_id (str): 发送类接口返回的newMsgId
            create_time (str): 发送类接口返回的createTime

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str   # 返回信息
                }
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "msgId": msg_id,
            "newMsgId": new_msg_id,
            "createTime": create_time,
        }
        return self.client.request("/message/revokeMsg", data)
