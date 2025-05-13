from typing import Dict, Any


class MessageModule:
    """异步消息模块"""

    def __init__(self, client):
        self.client = client

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

    async def send_text(
        self, to_wxid: str, content: str, at_wxid_list: list = []
    ) -> Dict[str, Any]:
        """发送文字消息

        Summary:
            发送文字消息，群消息可@群成员
            在群内发送消息@某人时，content中需包含@xxx

        Args:
            to_wxid (str): 接收人/群wxid
            content (str): 消息文本内容
            at_wxid_list (list, optional): @的wxid列表. Defaults to [].

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxids": [to_wxid],
            "content": content,
            "atWxids": at_wxid_list,
        }
        return await self.client.request("/message/sendText", data)

    async def send_image(self, to_wxid: str, image_url: str) -> Dict[str, Any]:
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
        return await self.client.request("/message/sendImage", data)

    async def send_file(
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
        return await self.client.request("/message/sendFile", data)

    async def send_link(
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
        return await self.client.request("/message/sendLink", data)

    async def revoke_message(
        self, to_wxid: str, msg_id: str, new_msg_id: str, create_time: str
    ) -> Dict[str, Any]:
        """撤回消息

        Summary:
            撤回消息

        Args:
            to_wxid (str): 接收人/群wxid
            msg_id (str): 消息id
            new_msg_id (str): 新消息id
            create_time (str): 消息创建时间

        Returns:
            Dict[str, Any]: 接口返回结果
        """
        data = {
            "appId": self.client.app_id,
            "toWxid": to_wxid,
            "msgid": msg_id,
            "newMsgId": new_msg_id,
            "createTime": create_time,
        }
        return await self.client.request("/message/revokeMsg", data)
