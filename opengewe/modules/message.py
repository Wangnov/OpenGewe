from typing import Dict, List, Any


class MessageModule:
    """异步消息模块"""

    def __init__(self, client):
        self.client = client

    async def download_file(self, xml: str) -> Dict[str, Any]:
        """下载文件

        Summary:
            下载文件

        Args:
            xml (str): 回调消息中的XML

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "xml": xml}
        return await self.client.request("/message/downloadFile", data)

    async def download_image(self, xml: str, image_type: int = 2) -> Dict[str, Any]:
        """下载图片

        Summary:
            下载图片，支持高清图片、常规图片和缩略图。注意 如果下载图片失败，可尝试下载另外两种图片类型，并非所有图片都会有高清、常规图片

        Args:
            xml (str): 回调消息中的XML
            image_type (int, optional): 下载的图片类型 1:高清图片 2:常规图片 3:缩略图. Defaults to 2.

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "xml": xml, "type": image_type}
        return await self.client.request("/message/downloadImage", data)

    async def download_voice(self, xml: str, msg_id: int) -> Dict[str, Any]:
        """下载语音

        Summary:
            下载语音文件

        Args:
            xml (str): 回调消息中的XML
            msg_id (int): 回调消息中的msgId

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "xml": xml, "msgId": msg_id}
        return await self.client.request("/message/downloadVoice", data)

    async def download_video(self, xml: str) -> Dict[str, Any]:
        """下载视频

        Summary:
            下载视频文件

        Args:
            xml (str): 回调消息中的XML

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "xml": xml}
        return await self.client.request("/message/downloadVideo", data)

    async def download_emoji_md5(self, xml: str) -> Dict[str, Any]:
        """下载emoji

        Summary:
            下载emoji表情

        Args:
            xml (str): 回调消息中的XML

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "xml": xml}
        return await self.client.request("/message/downloadEmojiMd5", data)

    async def download_cdn(self, url: str) -> Dict[str, Any]:
        """cdn下载

        Summary:
            通过CDN下载文件

        Args:
            url (str): cdn链接地址

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {"appId": self.client.app_id, "url": url}
        return await self.client.request("/message/downloadCdn", data)

    async def post_text(
        self, to_wxid: str, content: str, ats: str = ""
    ) -> Dict[str, Any]:
        """发送文字消息

        Summary:
            发送文字消息，群消息可@群成员
            在群内发送消息@某人时，content中需包含@xxx

        Args:
            to_wxid (str): 接收人/群wxid
            content (str): 消息文本内容
            ats (str, optional): @的wxid列表，多个用逗号分隔. Defaults to "".

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "content": content,
            "ats": ats,
        }
        return await self.client.request("/message/postText", data)

    async def post_file(
        self, to_wxid: str, file_url: str, file_name: str
    ) -> Dict[str, Any]:
        """发送文件消息

        Summary:
            发送文件消息

        Args:
            to_wxid (str): 接收人/群wxid
            file_url (str): 文件url地址
            file_name (str): 文件名称

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "fileUrl": file_url,
            "fileName": file_name,
        }
        return await self.client.request("/message/postFile", data)

    async def post_image(self, to_wxid: str, image_url: str) -> Dict[str, Any]:
        """发送图片消息

        Summary:
            发送图片消息

        Args:
            to_wxid (str): 接收人/群wxid
            image_url (str): 图片url地址

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {"appId": self.client.app_id, "toWxid": to_wxid, "imageUrl": image_url}
        return await self.client.request("/message/postImage", data)

    async def post_voice(self, to_wxid: str, voice_url: str, voice_time: int) -> Dict[str, Any]:
        """发送语音消息

        Summary:
            发送语音消息

        Args:
            to_wxid (str): 接收人/群wxid
            voice_url (str): 语音url地址
            voice_time (int): 语音时长，单位秒

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "voiceUrl": voice_url,
            "voiceTime": voice_time,
        }
        return await self.client.request("/message/postVoice", data)

    async def post_video(self, to_wxid: str, video_url: str, thumb_url: str = "") -> Dict[str, Any]:
        """发送视频消息

        Summary:
            发送视频消息

        Args:
            to_wxid (str): 接收人/群wxid
            video_url (str): 视频url地址
            thumb_url (str, optional): 视频封面图片url地址. Defaults to "".

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "videoUrl": video_url,
            "thumbUrl": thumb_url,
        }
        return await self.client.request("/message/postVideo", data)

    async def post_link(
        self, to_wxid: str, title: str, desc: str, url: str, image_url: str = ""
    ) -> Dict[str, Any]:
        """发送链接消息

        Summary:
            发送链接消息

        Args:
            to_wxid (str): 接收人/群wxid
            title (str): 链接标题
            desc (str): 链接描述
            url (str): 跳转链接
            image_url (str, optional): 链接图片. Defaults to "".

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "title": title,
            "desc": desc,
            "url": url,
            "imageUrl": image_url,
        }
        return await self.client.request("/message/postLink", data)

    async def post_name_card(self, to_wxid: str, card_wxid: str) -> Dict[str, Any]:
        """发送名片消息

        Summary:
            发送名片消息

        Args:
            to_wxid (str): 接收人/群wxid
            card_wxid (str): 名片用户的wxid

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "cardWxid": card_wxid,
        }
        return await self.client.request("/message/postNameCard", data)

    async def post_emoji(self, to_wxid: str, emoji_url: str, emoji_md5: str = "") -> Dict[str, Any]:
        """发送emoji消息

        Summary:
            发送emoji表情消息

        Args:
            to_wxid (str): 接收人/群wxid
            emoji_url (str): emoji表情url地址
            emoji_md5 (str, optional): emoji表情md5值. Defaults to "".

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "emojiUrl": emoji_url,
            "emojiMd5": emoji_md5,
        }
        return await self.client.request("/message/postEmoji", data)

    async def post_app_msg(self, to_wxid: str, app_msg: str) -> Dict[str, Any]:
        """发送appmsg消息

        Summary:
            发送应用消息

        Args:
            to_wxid (str): 接收人/群wxid
            app_msg (str): appmsg消息内容

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "appMsg": app_msg,
        }
        return await self.client.request("/message/postAppMsg", data)

    async def post_mini_app(
        self, 
        to_wxid: str, 
        title: str, 
        username: str, 
        path: str, 
        description: str, 
        thumb_url: str,
        app_id: str
    ) -> Dict[str, Any]:
        """发送小程序消息

        Summary:
            发送小程序消息

        Args:
            to_wxid (str): 接收人/群wxid
            title (str): 小程序标题
            username (str): 小程序username
            path (str): 小程序path路径
            description (str): 小程序描述
            thumb_url (str): 小程序封面图片url
            app_id (str): 小程序appId

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "title": title,
            "username": username,
            "path": path,
            "description": description,
            "thumbUrl": thumb_url,
            "appid": app_id,
        }
        return await self.client.request("/message/postMiniApp", data)

    async def forward_file(self, to_wxid: str, file_id: str) -> Dict[str, Any]:
        """转发文件

        Summary:
            转发文件消息

        Args:
            to_wxid (str): 接收人/群wxid
            file_id (str): 文件id

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "fileId": file_id,
        }
        return await self.client.request("/message/forwardFile", data)

    async def forward_image(self, to_wxid: str, file_id: str) -> Dict[str, Any]:
        """转发图片

        Summary:
            转发图片消息

        Args:
            to_wxid (str): 接收人/群wxid
            file_id (str): 图片id

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "fileId": file_id,
        }
        return await self.client.request("/message/forwardImage", data)

    async def forward_video(self, to_wxid: str, file_id: str) -> Dict[str, Any]:
        """转发视频

        Summary:
            转发视频消息

        Args:
            to_wxid (str): 接收人/群wxid
            file_id (str): 视频id

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "fileId": file_id,
        }
        return await self.client.request("/message/forwardVideo", data)

    async def forward_url(self, to_wxid: str, url_id: str) -> Dict[str, Any]:
        """转发链接

        Summary:
            转发链接消息

        Args:
            to_wxid (str): 接收人/群wxid
            url_id (str): 链接id

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "urlId": url_id,
        }
        return await self.client.request("/message/forwardUrl", data)

    async def forward_mini_app(self, to_wxid: str, mini_app_id: str) -> Dict[str, Any]:
        """转发小程序

        Summary:
            转发小程序消息

        Args:
            to_wxid (str): 接收人/群wxid
            mini_app_id (str): 小程序id

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "miniAppId": mini_app_id,
        }
        return await self.client.request("/message/forwardMiniApp", data)

    async def revoke_msg(
        self, to_wxid: str, msgid: str, new_msg_id: str, create_time: str
    ) -> Dict[str, Any]:
        """撤回消息

        Summary:
            撤回消息

        Args:
            to_wxid (str): 接收人/群wxid
            msgid (str): 消息id
            new_msg_id (str): 新消息id
            create_time (str): 消息创建时间

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "msgid": msgid,
            "newMsgId": new_msg_id,
            "createTime": create_time,
        }
        return await self.client.request("/message/revokeMsg", data)

    async def send_finder_msg(self, finder_username: str, content: str) -> Dict[str, Any]:
        """发送视频号消息

        Summary:
            发送视频号私信消息

        Args:
            finder_username (str): 视频号用户名
            content (str): 消息内容

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        if not self.client.is_gewe:
            return {
                "ret": 403,
                "msg": "该接口仅限付费版gewe调用，详情请见gewe文档：http://doc.geweapi.com/",
                "data": None,
            }
        data = {
            "appId": self.client.app_id,
            "finderUsername": finder_username,
            "content": content,
        }
        return await self.client.request("/message/sendFinderMsg", data)