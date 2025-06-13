"""
Celery 任务定义模块

这里集中定义所有可由Celery worker异步执行的任务。
每个任务都应该是独立的、可重入的，并且只接受可序列化的参数。
"""

import asyncio
from typing import Dict, Any, Union

from opengewe.client import GeweClient
from opengewe.logger import get_logger

logger = get_logger("CeleryTasks")


def run_async_task(coro):
    """
    安全地运行异步任务，自动处理事件循环。

    此函数通过始终在新事件循环中运行协程来确保线程安全和避免与现有事件循环的冲突。
    这在从同步代码（如Celery任务）调用异步代码时特别有用。
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def register_tasks(celery_app):
    """动态注册Celery任务

    Raises:
        ValueError: 如果celery_app为None，则无法注册任务
    """
    if celery_app is None:
        raise ValueError("无法注册Celery任务，因为celery_app为None")

    @celery_app.task(name="opengewe.queue.tasks.send_text_message_task")
    def send_text_message_task(
        client_config: Dict[str, Any],
        wxid: str,
        content: str,
        at: Union[list, str] = "",
    ) -> tuple:
        logger.info(f"执行发送文本消息任务: to={wxid}, content='{content[:20]}...'")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.post_text(to_wxid=wxid, content=content, ats=at)

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            data = response.get("data", {})
            client_msg_id = int(data.get("clientMsgId", 0))
            create_time = int(data.get("createTime", 0))
            new_msg_id = int(data.get("newMsgId", 0))
            return client_msg_id, create_time, new_msg_id
        else:
            error_msg = f"发送文本消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.send_image_message_task")
    def send_image_message_task(
        client_config: Dict[str, Any], wxid: str, image: Union[str, bytes]
    ) -> Dict[str, Any]:
        logger.info(f"执行发送图片消息任务: to={wxid}")
        client = GeweClient(**client_config)

        async def run_async():
            if isinstance(image, bytes):
                import base64
                img_data = base64.b64encode(image).decode()
            else:
                img_data = image
            return await client.message.post_image(to_wxid=wxid, image_url=img_data)

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            return response
        else:
            error_msg = f"发送图片消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.send_video_message_task")
    def send_video_message_task(
        client_config: Dict[str, Any],
        wxid: str,
        video: str,
        image: str = None,
        duration: int = None,
    ) -> tuple:
        logger.info(f"执行发送视频消息任务: to={wxid}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.post_video(
                to_wxid=wxid, video_url=video, thumb_url=image or ""
            )

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            data = response.get("data", {})
            client_msg_id = int(data.get("clientMsgId", 0))
            new_msg_id = int(data.get("newMsgId", 0))
            return client_msg_id, new_msg_id
        else:
            error_msg = f"发送视频消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.send_voice_message_task")
    def send_voice_message_task(
        client_config: Dict[str, Any], wxid: str, voice: str, format: str = "amr"
    ) -> tuple:
        logger.info(f"执行发送语音消息任务: to={wxid}")
        client = GeweClient(**client_config)

        async def run_async():
            voice_time = 10
            return await client.message.post_voice(
                to_wxid=wxid, voice_url=voice, voice_time=voice_time
            )

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            data = response.get("data", {})
            client_msg_id = int(data.get("clientMsgId", 0))
            create_time = int(data.get("createTime", 0))
            new_msg_id = int(data.get("newMsgId", 0))
            return client_msg_id, create_time, new_msg_id
        else:
            error_msg = f"发送语音消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.send_link_message_task")
    def send_link_message_task(
        client_config: Dict[str, Any],
        wxid: str,
        url: str,
        title: str = "",
        description: str = "",
        thumb_url: str = "",
    ) -> tuple:
        logger.info(f"执行发送链接消息任务: to={wxid}, url={url}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.post_link(
                to_wxid=wxid, title=title, desc=description, url=url, image_url=thumb_url
            )

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            data = response.get("data", {})
            client_msg_id = int(data.get("clientMsgId", 0))
            create_time = int(data.get("createTime", 0))
            new_msg_id = int(data.get("newMsgId", 0))
            return client_msg_id, create_time, new_msg_id
        else:
            error_msg = f"发送链接消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.send_card_message_task")
    def send_card_message_task(
        client_config: Dict[str, Any],
        wxid: str,
        card_wxid: str,
        card_nickname: str,
        card_alias: str = "",
    ) -> tuple:
        logger.info(f"执行发送名片消息任务: to={wxid}, card_wxid={card_wxid}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.post_name_card(to_wxid=wxid, card_wxid=card_wxid)

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            data = response.get("data", {})
            client_msg_id = int(data.get("clientMsgId", 0))
            create_time = int(data.get("createTime", 0))
            new_msg_id = int(data.get("newMsgId", 0))
            return client_msg_id, create_time, new_msg_id
        else:
            error_msg = f"发送名片消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.send_app_message_task")
    def send_app_message_task(
        client_config: Dict[str, Any], wxid: str, xml: str, type: int
    ) -> tuple:
        logger.info(f"执行发送应用消息任务: to={wxid}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.post_app_msg(to_wxid=wxid, app_msg=xml)

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            data = response.get("data", {})
            client_msg_id = int(data.get("clientMsgId", 0))
            create_time = int(data.get("createTime", 0))
            new_msg_id = int(data.get("newMsgId", 0))
            return client_msg_id, create_time, new_msg_id
        else:
            error_msg = f"发送应用消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.send_emoji_message_task")
    def send_emoji_message_task(
        client_config: Dict[str, Any], wxid: str, md5: str, total_len: int
    ) -> Dict[str, Any]:
        logger.info(f"执行发送表情消息任务: to={wxid}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.post_emoji(
                to_wxid=wxid, emoji_url=md5, emoji_md5=md5
            )

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            return response
        else:
            error_msg = f"发送表情消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.send_file_message_task")
    def send_file_message_task(
        client_config: Dict[str, Any], wxid: str, file_url: str, file_name: str
    ) -> Dict[str, Any]:
        logger.info(f"执行发送文件消息任务: to={wxid}, file_name={file_name}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.post_file(
                to_wxid=wxid, file_url=file_url, file_name=file_name
            )

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            return response
        else:
            error_msg = f"发送文件消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.send_mini_app_task")
    def send_mini_app_task(
        client_config: Dict[str, Any],
        wxid: str,
        title: str,
        username: str,
        path: str,
        description: str,
        thumb_url: str,
        app_id: str,
    ) -> Dict[str, Any]:
        logger.info(f"执行发送小程序消息任务: to={wxid}, title={title}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.post_mini_app(
                to_wxid=wxid,
                title=title,
                username=username,
                path=path,
                description=description,
                thumb_url=thumb_url,
                app_id=app_id,
            )

        response = run_async_task(run_async())

        if response.get("ret") == 200:
            return response
        else:
            error_msg = f"发送小程序消息失败: {response.get('msg')}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @celery_app.task(name="opengewe.queue.tasks.forward_file_message_task")
    def forward_file_message_task(
        client_config: Dict[str, Any], wxid: str, file_id: str
    ) -> Dict[str, Any]:
        logger.info(f"执行转发文件消息任务: to={wxid}, file_id={file_id}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.forward_file(to_wxid=wxid, file_id=file_id)
        response = run_async_task(run_async())
        if response.get("ret") == 200:
            return response
        else:
            raise Exception(f"转发文件消息失败: {response.get('msg')}")

    @celery_app.task(name="opengewe.queue.tasks.forward_image_message_task")
    def forward_image_message_task(
        client_config: Dict[str, Any], wxid: str, file_id: str
    ) -> Dict[str, Any]:
        logger.info(f"执行转发图片消息任务: to={wxid}, file_id={file_id}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.forward_image(to_wxid=wxid, file_id=file_id)
        response = run_async_task(run_async())
        if response.get("ret") == 200:
            return response
        else:
            raise Exception(f"转发图片消息失败: {response.get('msg')}")

    @celery_app.task(name="opengewe.queue.tasks.forward_video_message_task")
    def forward_video_message_task(
        client_config: Dict[str, Any], wxid: str, file_id: str
    ) -> Dict[str, Any]:
        logger.info(f"执行转发视频消息任务: to={wxid}, file_id={file_id}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.forward_video(to_wxid=wxid, file_id=file_id)
        response = run_async_task(run_async())
        if response.get("ret") == 200:
            return response
        else:
            raise Exception(f"转发视频消息失败: {response.get('msg')}")

    @celery_app.task(name="opengewe.queue.tasks.forward_url_message_task")
    def forward_url_message_task(
        client_config: Dict[str, Any], wxid: str, url_id: str
    ) -> Dict[str, Any]:
        logger.info(f"执行转发链接消息任务: to={wxid}, url_id={url_id}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.forward_url(to_wxid=wxid, url_id=url_id)
        response = run_async_task(run_async())
        if response.get("ret") == 200:
            return response
        else:
            raise Exception(f"转发链接消息失败: {response.get('msg')}")

    @celery_app.task(name="opengewe.queue.tasks.forward_mini_app_message_task")
    def forward_mini_app_message_task(
        client_config: Dict[str, Any], wxid: str, mini_app_id: str
    ) -> Dict[str, Any]:
        logger.info(f"执行转发小程序消息任务: to={wxid}, mini_app_id={mini_app_id}")
        client = GeweClient(**client_config)

        async def run_async():
            return await client.message.forward_mini_app(to_wxid=wxid, mini_app_id=mini_app_id)
        response = run_async_task(run_async())
        if response.get("ret") == 200:
            return response
        else:
            raise Exception(f"转发小程序消息失败: {response.get('msg')}")
