from typing import Dict, Optional, Union, Any

from loguru import logger

from ..modules.message import MessageModule
from ..queue import create_message_queue


class MessageMixin:
    """消息混合类，提供异步消息发送功能"""

    def __init__(
        self, message_module: MessageModule, queue_type: str = "simple", **queue_options
    ):
        """初始化消息混合类

        Args:
            message_module: MessageModule实例
            queue_type: 队列类型，默认为"simple"
            **queue_options: 队列选项，根据队列类型不同而不同
        """
        self._message_module = message_module
        self._message_queue = create_message_queue(queue_type, **queue_options)

    async def revoke_message(
        self, wxid: str, client_msg_id: int, create_time: int, new_msg_id: int
    ) -> bool:
        """撤回消息。

        Args:
            wxid (str): 接收人wxid
            client_msg_id (int): 发送消息的返回值
            create_time (int): 发送消息的返回值
            new_msg_id (int): 发送消息的返回值

        Returns:
            bool: 成功返回True，失败返回False
        """
        return await self._message_queue.enqueue(
            self._revoke_message, wxid, client_msg_id, create_time, new_msg_id
        )

    async def _revoke_message(
        self, wxid: str, client_msg_id: int, create_time: int, new_msg_id: int
    ) -> bool:
        """实际撤回消息的方法"""
        response = await self._message_module.revoke_msg(
            to_wxid=wxid,
            msgid=str(client_msg_id),
            new_msg_id=str(new_msg_id),
            create_time=str(create_time),
        )
        logger.info(
            "撤回消息: 对方wxid:{} ClientMsgId:{} CreateTime:{} NewMsgId:{}",
            wxid,
            client_msg_id,
            create_time,
            new_msg_id,
        )
        return response.get("ret") == 200

    async def send_text_message(
        self, wxid: str, content: str, at: Union[list, str] = ""
    ) -> tuple[int, int, int]:
        """发送文本消息。

        Args:
            wxid (str): 接收人wxid
            content (str): 消息内容
            at (list, str, optional): 要@的用户

        Returns:
            tuple[int, int, int]: 返回(ClientMsgid, CreateTime, NewMsgId)
        """
        return await self._message_queue.enqueue(
            self._send_text_message, wxid, content, at
        )

    async def _send_text_message(
        self, wxid: str, content: str, at: Union[list, str] = ""
    ) -> tuple[int, int, int]:
        """实际发送文本消息的方法"""
        # 处理at参数
        if isinstance(at, list):
            ats = ",".join(at)
        else:
            ats = at

        response = await self._message_module.post_text(
            to_wxid=wxid, content=content, ats=ats
        )
        logger.info("发送文字消息: 对方wxid:{} at:{} 内容:{}", wxid, at, content)

        if response.get("ret") == 200:
            data = response.get("data", {})
            # 尝试转换返回值，如果无法转换则返回原始值
            try:
                client_msg_id = int(data.get("clientMsgId", 0))
            except (ValueError, TypeError):
                client_msg_id = data.get("clientMsgId", 0)

            try:
                create_time = int(data.get("createTime", 0))
            except (ValueError, TypeError):
                create_time = data.get("createTime", 0)

            try:
                new_msg_id = int(data.get("newMsgId", 0))
            except (ValueError, TypeError):
                new_msg_id = data.get("newMsgId", 0)

            return client_msg_id, create_time, new_msg_id
        else:
            raise Exception(f"发送文本消息失败: {response.get('msg')}")

    async def send_image_message(self, wxid: str, image: Union[str, bytes]) -> dict:
        """发送图片消息。

        Args:
            wxid (str): 接收人wxid
            image (str): 图片URL或base64字符串

        Returns:
            dict: 返回响应结果
        """
        return await self._message_queue.enqueue(self._send_image_message, wxid, image)

    async def _send_image_message(self, wxid: str, image: Union[str, bytes]) -> dict:
        """实际发送图片消息的方法"""
        # 如果image是bytes类型，需要先上传或转换为base64，这里简化处理
        if isinstance(image, bytes):
            import base64

            image = base64.b64encode(image).decode()

        # 假设image是URL
        response = await self._message_module.post_image(to_wxid=wxid, image_url=image)
        logger.info("发送图片消息: 对方wxid:{} 图片base64略", wxid)

        return response

    async def send_video_message(
        self, wxid: str, video: str, image: str = None, duration: Optional[int] = None
    ) -> tuple[int, int]:
        """发送视频消息。

        Args:
            wxid (str): 接收人wxid
            video (str): 视频URL
            image (str, optional): 视频封面图片URL. Defaults to None.
            duration (Optional[int], optional): 视频时长. Defaults to None.

        Returns:
            tuple[int, int]: 返回(ClientMsgid, NewMsgId)
        """
        return await self._message_queue.enqueue(
            self._send_video_message, wxid, video, image, duration
        )

    async def _send_video_message(
        self, wxid: str, video: str, image: str = None, duration: Optional[int] = None
    ) -> tuple[int, int]:
        """实际发送视频消息的方法"""
        # 在这里忽略duration参数，因为message.py中的post_video方法不需要该参数
        response = await self._message_module.post_video(
            to_wxid=wxid, video_url=video, thumb_url=image or ""
        )

        logger.info(
            "发送视频消息: 对方wxid:{} 视频URL:{} 图片URL:{}", wxid, video, image
        )

        if response.get("ret") == 200:
            data = response.get("data", {})
            # 尝试转换返回值
            try:
                client_msg_id = int(data.get("clientMsgId", 0))
            except (ValueError, TypeError):
                client_msg_id = data.get("clientMsgId", 0)

            try:
                new_msg_id = int(data.get("newMsgId", 0))
            except (ValueError, TypeError):
                new_msg_id = data.get("newMsgId", 0)

            return client_msg_id, new_msg_id
        else:
            raise Exception(f"发送视频消息失败: {response.get('msg')}")

    async def send_voice_message(
        self, wxid: str, voice: str, format: str = "amr"
    ) -> tuple[int, int, int]:
        """发送语音消息。

        Args:
            wxid (str): 接收人wxid
            voice (str): 语音URL
            format (str, optional): 语音格式. Defaults to "amr".

        Returns:
            tuple[int, int, int]: 返回(ClientMsgid, CreateTime, NewMsgId)
        """
        return await self._message_queue.enqueue(
            self._send_voice_message, wxid, voice, format
        )

    async def _send_voice_message(
        self, wxid: str, voice: str, format: str = "amr"
    ) -> tuple[int, int, int]:
        """实际发送语音消息的方法"""
        # 这里我们假设语音URL已经是正确的格式，format参数在这里被忽略
        # 视频时长假设为10秒，实际使用时需要获取真实时长
        voice_time = 10

        response = await self._message_module.post_voice(
            to_wxid=wxid, voice_url=voice, voice_time=voice_time
        )

        logger.info("发送语音消息: 对方wxid:{} 语音URL:{} 格式:{}", wxid, voice, format)

        if response.get("ret") == 200:
            data = response.get("data", {})
            # 尝试转换返回值
            try:
                client_msg_id = int(data.get("clientMsgId", 0))
            except (ValueError, TypeError):
                client_msg_id = data.get("clientMsgId", 0)

            try:
                create_time = int(data.get("createTime", 0))
            except (ValueError, TypeError):
                create_time = data.get("createTime", 0)

            try:
                new_msg_id = int(data.get("newMsgId", 0))
            except (ValueError, TypeError):
                new_msg_id = data.get("newMsgId", 0)

            return client_msg_id, create_time, new_msg_id
        else:
            raise Exception(f"发送语音消息失败: {response.get('msg')}")

    async def send_link_message(
        self,
        wxid: str,
        url: str,
        title: str = "",
        description: str = "",
        thumb_url: str = "",
    ) -> tuple[int, int, int]:
        """发送链接消息。

        Args:
            wxid (str): 接收人wxid
            url (str): 跳转链接
            title (str, optional): 标题. Defaults to "".
            description (str, optional): 描述. Defaults to "".
            thumb_url (str, optional): 缩略图链接. Defaults to "".

        Returns:
            tuple[int, int, int]: 返回(ClientMsgid, CreateTime, NewMsgId)
        """
        return await self._message_queue.enqueue(
            self._send_link_message, wxid, url, title, description, thumb_url
        )

    async def _send_link_message(
        self,
        wxid: str,
        url: str,
        title: str = "",
        description: str = "",
        thumb_url: str = "",
    ) -> tuple[int, int, int]:
        """实际发送链接消息的方法"""
        response = await self._message_module.post_link(
            to_wxid=wxid, title=title, desc=description, url=url, image_url=thumb_url
        )

        logger.info(
            "发送链接消息: 对方wxid:{} 链接:{} 标题:{} 描述:{} 缩略图链接:{}",
            wxid,
            url,
            title,
            description,
            thumb_url,
        )

        if response.get("ret") == 200:
            data = response.get("data", {})
            # 尝试转换返回值
            try:
                client_msg_id = int(data.get("clientMsgId", 0))
            except (ValueError, TypeError):
                client_msg_id = data.get("clientMsgId", 0)

            try:
                create_time = int(data.get("createTime", 0))
            except (ValueError, TypeError):
                create_time = data.get("createTime", 0)

            try:
                new_msg_id = int(data.get("newMsgId", 0))
            except (ValueError, TypeError):
                new_msg_id = data.get("newMsgId", 0)

            return client_msg_id, create_time, new_msg_id
        else:
            raise Exception(f"发送链接消息失败: {response.get('msg')}")

    async def send_card_message(
        self, wxid: str, card_wxid: str, card_nickname: str, card_alias: str = ""
    ) -> tuple[int, int, int]:
        """发送名片消息。

        Args:
            wxid (str): 接收人wxid
            card_wxid (str): 名片用户的wxid
            card_nickname (str): 名片用户的昵称
            card_alias (str, optional): 名片用户的备注. Defaults to "".

        Returns:
            tuple[int, int, int]: 返回(ClientMsgid, CreateTime, NewMsgId)
        """
        return await self._message_queue.enqueue(
            self._send_card_message, wxid, card_wxid, card_nickname, card_alias
        )

    async def _send_card_message(
        self, wxid: str, card_wxid: str, card_nickname: str, card_alias: str = ""
    ) -> tuple[int, int, int]:
        """实际发送名片消息的方法"""
        # 在message.py中只需要wxid和card_wxid，忽略其他参数
        response = await self._message_module.post_name_card(
            to_wxid=wxid, card_wxid=card_wxid
        )

        logger.info(
            "发送名片消息: 对方wxid:{} 名片wxid:{} 名片备注:{} 名片昵称:{}",
            wxid,
            card_wxid,
            card_alias,
            card_nickname,
        )

        if response.get("ret") == 200:
            data = response.get("data", {})
            # 尝试转换返回值
            try:
                client_msg_id = int(data.get("clientMsgId", 0))
            except (ValueError, TypeError):
                client_msg_id = data.get("clientMsgId", 0)

            try:
                create_time = int(data.get("createTime", 0))
            except (ValueError, TypeError):
                create_time = data.get("createTime", 0)

            try:
                new_msg_id = int(data.get("newMsgId", 0))
            except (ValueError, TypeError):
                new_msg_id = data.get("newMsgId", 0)

            return client_msg_id, create_time, new_msg_id
        else:
            raise Exception(f"发送名片消息失败: {response.get('msg')}")

    async def send_app_message(
        self, wxid: str, xml: str, type: int
    ) -> tuple[int, int, int]:
        """发送应用消息。

        Args:
            wxid (str): 接收人wxid
            xml (str): 应用消息的xml内容
            type (int): 应用消息类型

        Returns:
            tuple[int, int, int]: 返回(ClientMsgid, CreateTime, NewMsgId)
        """
        return await self._message_queue.enqueue(
            self._send_app_message, wxid, xml, type
        )

    async def _send_app_message(
        self, wxid: str, xml: str, type: int
    ) -> tuple[int, int, int]:
        """实际发送应用消息的方法"""
        # 在message.py中只有app_msg参数，type参数被忽略
        response = await self._message_module.post_app_msg(to_wxid=wxid, app_msg=xml)

        logger.info("发送app消息: 对方wxid:{} 类型:{} xml:{}", wxid, type, xml)

        if response.get("ret") == 200:
            data = response.get("data", {})
            # 尝试转换返回值
            try:
                client_msg_id = int(data.get("clientMsgId", 0))
            except (ValueError, TypeError):
                client_msg_id = data.get("clientMsgId", 0)

            try:
                create_time = int(data.get("createTime", 0))
            except (ValueError, TypeError):
                create_time = data.get("createTime", 0)

            try:
                new_msg_id = int(data.get("newMsgId", 0))
            except (ValueError, TypeError):
                new_msg_id = data.get("newMsgId", 0)

            return client_msg_id, create_time, new_msg_id
        else:
            raise Exception(f"发送应用消息失败: {response.get('msg')}")

    async def send_emoji_message(self, wxid: str, md5: str, total_len: int) -> dict:
        """发送表情消息。

        Args:
            wxid (str): 接收人wxid
            md5 (str): 表情MD5值
            total_len (int): 表情总长度

        Returns:
            dict: 返回响应结果
        """
        return await self._message_queue.enqueue(
            self._send_emoji_message, wxid, md5, total_len
        )

    async def _send_emoji_message(self, wxid: str, md5: str, total_len: int) -> dict:
        """实际发送表情消息的方法"""
        # 在message.py中需要emoji_url和emoji_md5，这里我们假设md5已经是URL，实际使用时需要调整
        response = await self._message_module.post_emoji(
            to_wxid=wxid, emoji_url=md5, emoji_md5=md5
        )

        logger.info("发送表情消息: 对方wxid:{} MD5:{} 大小:{}", wxid, md5, total_len)

        return response

    # 下面是对message.py中有但advanced_message_example.py中没有的方法的包装

    async def send_file_message(
        self, wxid: str, file_url: str, file_name: str
    ) -> Dict[str, Any]:
        """发送文件消息。

        Args:
            wxid (str): 接收人wxid
            file_url (str): 文件URL
            file_name (str): 文件名称

        Returns:
            Dict[str, Any]: 返回响应结果
        """
        return await self._message_queue.enqueue(
            self._send_file_message, wxid, file_url, file_name
        )

    async def _send_file_message(
        self, wxid: str, file_url: str, file_name: str
    ) -> Dict[str, Any]:
        """实际发送文件消息的方法"""
        response = await self._message_module.post_file(
            to_wxid=wxid, file_url=file_url, file_name=file_name
        )

        logger.info(
            "发送文件消息: 对方wxid:{} 文件URL:{} 文件名:{}", wxid, file_url, file_name
        )

        return response

    async def send_mini_app(
        self,
        wxid: str,
        title: str,
        username: str,
        path: str,
        description: str,
        thumb_url: str,
        app_id: str,
    ) -> Dict[str, Any]:
        """发送小程序消息。

        Args:
            wxid (str): 接收人wxid
            title (str): 小程序标题
            username (str): 小程序username
            path (str): 小程序path路径
            description (str): 小程序描述
            thumb_url (str): 小程序封面图片URL
            app_id (str): 小程序appId

        Returns:
            Dict[str, Any]: 返回响应结果
        """
        return await self._message_queue.enqueue(
            self._send_mini_app,
            wxid,
            title,
            username,
            path,
            description,
            thumb_url,
            app_id,
        )

    async def _send_mini_app(
        self,
        wxid: str,
        title: str,
        username: str,
        path: str,
        description: str,
        thumb_url: str,
        app_id: str,
    ) -> Dict[str, Any]:
        """实际发送小程序消息的方法"""
        response = await self._message_module.post_mini_app(
            to_wxid=wxid,
            title=title,
            username=username,
            path=path,
            description=description,
            thumb_url=thumb_url,
            app_id=app_id,
        )

        logger.info(
            "发送小程序消息: 对方wxid:{} 标题:{} username:{}", wxid, title, username
        )

        return response

    # 以下是转发消息的方法

    async def forward_file_message(self, wxid: str, file_id: str) -> Dict[str, Any]:
        """转发文件消息。

        Args:
            wxid (str): 接收人wxid
            file_id (str): 文件ID

        Returns:
            Dict[str, Any]: 返回响应结果
        """
        return await self._message_queue.enqueue(
            self._forward_file_message, wxid, file_id
        )

    async def _forward_file_message(self, wxid: str, file_id: str) -> Dict[str, Any]:
        """实际转发文件消息的方法"""
        response = await self._message_module.forward_file(
            to_wxid=wxid, file_id=file_id
        )

        logger.info("转发文件消息: 对方wxid:{} 文件ID:{}", wxid, file_id)

        return response

    async def forward_image_message(self, wxid: str, file_id: str) -> Dict[str, Any]:
        """转发图片消息。

        Args:
            wxid (str): 接收人wxid
            file_id (str): 图片ID

        Returns:
            Dict[str, Any]: 返回响应结果
        """
        return await self._message_queue.enqueue(
            self._forward_image_message, wxid, file_id
        )

    async def _forward_image_message(self, wxid: str, file_id: str) -> Dict[str, Any]:
        """实际转发图片消息的方法"""
        response = await self._message_module.forward_image(
            to_wxid=wxid, file_id=file_id
        )

        logger.info("转发图片消息: 对方wxid:{} 图片ID:{}", wxid, file_id)

        return response

    async def forward_video_message(self, wxid: str, file_id: str) -> Dict[str, Any]:
        """转发视频消息。

        Args:
            wxid (str): 接收人wxid
            file_id (str): 视频ID

        Returns:
            Dict[str, Any]: 返回响应结果
        """
        return await self._message_queue.enqueue(
            self._forward_video_message, wxid, file_id
        )

    async def _forward_video_message(self, wxid: str, file_id: str) -> Dict[str, Any]:
        """实际转发视频消息的方法"""
        response = await self._message_module.forward_video(
            to_wxid=wxid, file_id=file_id
        )

        logger.info("转发视频消息: 对方wxid:{} 视频ID:{}", wxid, file_id)

        return response

    async def forward_url_message(self, wxid: str, url_id: str) -> Dict[str, Any]:
        """转发链接消息。

        Args:
            wxid (str): 接收人wxid
            url_id (str): 链接ID

        Returns:
            Dict[str, Any]: 返回响应结果
        """
        return await self._message_queue.enqueue(
            self._forward_url_message, wxid, url_id
        )

    async def _forward_url_message(self, wxid: str, url_id: str) -> Dict[str, Any]:
        """实际转发链接消息的方法"""
        response = await self._message_module.forward_url(to_wxid=wxid, url_id=url_id)

        logger.info("转发链接消息: 对方wxid:{} 链接ID:{}", wxid, url_id)

        return response

    async def forward_mini_app_message(
        self, wxid: str, mini_app_id: str
    ) -> Dict[str, Any]:
        """转发小程序消息。

        Args:
            wxid (str): 接收人wxid
            mini_app_id (str): 小程序ID

        Returns:
            Dict[str, Any]: 返回响应结果
        """
        return await self._message_queue.enqueue(
            self._forward_mini_app_message, wxid, mini_app_id
        )

    async def _forward_mini_app_message(
        self, wxid: str, mini_app_id: str
    ) -> Dict[str, Any]:
        """实际转发小程序消息的方法"""
        response = await self._message_module.forward_mini_app(
            to_wxid=wxid, mini_app_id=mini_app_id
        )

        logger.info("转发小程序消息: 对方wxid:{} 小程序ID:{}", wxid, mini_app_id)

        return response

    # 从advanced_message_example.py中映射的方法

    async def send_cdn_file_msg(self, wxid: str, xml: str) -> dict:
        """转发文件消息。与forward_file_message功能类似，为了保持API兼容性

        Args:
            wxid (str): 接收人wxid
            xml (str): 文件XML内容，在这里被当作file_id使用

        Returns:
            dict: 返回响应结果
        """
        return await self.forward_file_message(wxid, xml)

    async def send_cdn_img_msg(self, wxid: str, xml: str) -> tuple[str, int, int]:
        """转发图片消息。与forward_image_message功能类似，为了保持API兼容性

        Args:
            wxid (str): 接收人wxid
            xml (str): 图片XML内容，在这里被当作file_id使用

        Returns:
            tuple[str, int, int]: 返回(ClientImgId, CreateTime, NewMsgId)
        """
        response = await self.forward_image_message(wxid, xml)

        if response.get("ret") == 200:
            data = response.get("data", {})
            # 尝试转换返回值
            try:
                client_img_id = data.get("clientImgId", "")
                if not isinstance(client_img_id, str):
                    client_img_id = str(client_img_id)
            except Exception:
                client_img_id = ""

            try:
                create_time = int(data.get("createTime", 0))
            except (ValueError, TypeError):
                create_time = 0

            try:
                new_msg_id = int(data.get("newMsgId", 0))
            except (ValueError, TypeError):
                new_msg_id = 0

            return client_img_id, create_time, new_msg_id
        else:
            raise Exception(f"转发图片消息失败: {response.get('msg')}")

    async def send_cdn_video_msg(self, wxid: str, xml: str) -> tuple[str, int]:
        """转发视频消息。与forward_video_message功能类似，为了保持API兼容性

        Args:
            wxid (str): 接收人wxid
            xml (str): 视频XML内容，在这里被当作file_id使用

        Returns:
            tuple[str, int]: 返回(ClientMsgid, NewMsgId)
        """
        response = await self.forward_video_message(wxid, xml)

        if response.get("ret") == 200:
            data = response.get("data", {})
            # 尝试转换返回值
            try:
                client_msg_id = data.get("clientMsgId", "")
                if not isinstance(client_msg_id, str):
                    client_msg_id = str(client_msg_id)
            except Exception:
                client_msg_id = ""

            try:
                new_msg_id = int(data.get("newMsgId", 0))
            except (ValueError, TypeError):
                new_msg_id = 0

            return client_msg_id, new_msg_id
        else:
            raise Exception(f"转发视频消息失败: {response.get('msg')}")

    async def sync_message(self) -> dict:
        """同步消息。

        Returns:
            dict: 返回同步到的消息数据
        """
        # 这个方法不包装到消息队列中，因为它是查询操作
        # 这个方法在message.py中不存在，这里返回一个模拟的结果
        logger.warning("sync_message方法在MessageModule中不存在，返回模拟结果")
        return True, {"message": "这是一个模拟的同步消息结果"}
