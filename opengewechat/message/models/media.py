from dataclasses import dataclass
from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET

from opengewechat.message.types import MessageType
from opengewechat.message.models.base import BaseMessage
from opengewechat.client import GewechatClient


@dataclass
class ImageMessage(BaseMessage):
    """图片消息"""

    img_download_url: str = ""  # 图片下载链接
    img_buffer: bytes = b""  # 图片buffer

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], client: Optional[GewechatClient] = None
    ) -> "ImageMessage":
        """从字典创建图片消息对象

        Args:
            data: 原始数据
            client: GewechatClient实例，用于下载图片
        """
        msg = cls(
            type=MessageType.IMAGE,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_user = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_user = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 如果提供了GewechatClient实例，使用API获取下载链接
                try:
                    if client and msg.content:
                        # 调用下载图片接口获取文件URL
                        try:
                            download_result = client.message.download_image(
                                msg.content, 1
                            )
                            # 下载高清图片成功
                            if (
                                download_result
                                and download_result.get("ret") == 200
                                and "data" in download_result
                            ):
                                file_url = download_result["data"].get("fileUrl", "")
                                if file_url:
                                    if client.is_gewe:
                                        msg.img_download_url = file_url
                                    elif client.download_url:
                                        msg.img_download_url = (
                                            f"{client.download_url}/{file_url}"
                                        )
                            else:
                                # 下载常规图片
                                download_result = client.message.download_image(
                                    msg.content, 2
                                )
                                if (
                                    download_result
                                    and download_result.get("ret") == 200
                                    and "data" in download_result
                                ):
                                    file_url = download_result["data"].get(
                                        "fileUrl", ""
                                    )
                                    if file_url:
                                        if client.is_gewe:
                                            msg.img_download_url = file_url
                                        elif client.download_url:
                                            msg.img_download_url = (
                                                f"{client.download_url}/{file_url}"
                                            )
                                else:
                                    # 下载缩略图
                                    download_result = client.message.download_image(
                                        msg.content, 3
                                    )
                                    if (
                                        download_result
                                        and download_result.get("ret") == 200
                                        and "data" in download_result
                                    ):
                                        file_url = download_result["data"].get(
                                            "fileUrl", ""
                                        )
                                        if file_url:
                                            if client.is_gewe:
                                                msg.img_download_url = file_url
                                            elif client.download_url:
                                                msg.img_download_url = (
                                                    f"{client.download_url}/{file_url}"
                                                )
                        except Exception:
                            # 下载失败不影响消息处理
                            pass
                except Exception:
                    pass

            # 获取缩略图数据
            if "ImgBuf" in msg_data and "buffer" in msg_data["ImgBuf"]:
                import base64

                try:
                    msg.img_buffer = base64.b64decode(msg_data["ImgBuf"]["buffer"])
                except Exception:
                    pass

        return msg


@dataclass
class VoiceMessage(BaseMessage):
    """语音消息"""

    voice_url: str = ""  # 语音文件URL
    voice_length: int = 0  # 语音长度(毫秒)
    voice_buffer: bytes = b""  # 语音buffer
    voice_md5: str = ""  # 语音MD5值
    aes_key: str = ""  # AES密钥

    def save_voice_buffer_to_silk(self, filename: str = None) -> str:
        """将语音buffer保存为silk文件

        Args:
            filename: 文件名，如果为None，则使用消息ID作为文件名

        Returns:
            保存后的文件路径，如果保存失败则返回空字符串
        """
        import os
        import hashlib

        if not self.voice_buffer:
            return ""

        if not filename:
            # 使用消息ID或生成一个基于内容的临时文件名
            if self.msg_id:
                filename = f"voice_{self.msg_id}.silk"
            else:
                # 使用buffer内容的哈希值作为文件名
                hash_obj = hashlib.md5(self.voice_buffer)
                filename = f"voice_{hash_obj.hexdigest()}.silk"

        # 确保filename有.silk扩展名
        if not filename.endswith(".silk"):
            filename += ".silk"

        # 确保下载目录存在
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)

        filepath = os.path.join(download_dir, filename)

        try:
            with open(filepath, "wb") as f:
                f.write(self.voice_buffer)
            return filepath
        except Exception as e:
            print(f"保存语音文件失败: {e}")
            return ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any], client=None) -> "VoiceMessage":
        """从字典创建语音消息对象

        Args:
            data: 原始数据
            client: GewechatClient实例，用于下载语音
        """
        msg = cls(
            type=MessageType.VOICE,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_user = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_user = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取语音信息
                try:
                    root = ET.fromstring(msg.content)
                    voice_node = root.find("voicemsg")
                    if voice_node is not None:
                        msg.voice_url = voice_node.get("voiceurl", "")
                        msg.voice_length = int(voice_node.get("voicelength", "0"))
                        msg.aes_key = voice_node.get("aeskey", "")

                        # 如果提供了GewechatClient实例，使用API获取下载链接
                        if client and msg.content:
                            # 调用下载语音接口获取文件URL
                            try:
                                download_result = client.message.download_voice(
                                    msg.content
                                )
                                if (
                                    download_result
                                    and download_result.get("ret") == 200
                                    and "data" in download_result
                                ):
                                    file_url = download_result["data"].get(
                                        "fileUrl", ""
                                    )
                                    if file_url and client.download_url:
                                        msg.voice_url = (
                                            f"{client.download_url}?url={file_url}"
                                        )
                            except Exception:
                                # 下载失败不影响消息处理
                                pass
                except Exception:
                    pass

            # 获取语音数据
            if "ImgBuf" in msg_data and "buffer" in msg_data["ImgBuf"]:
                import base64

                try:
                    msg.voice_buffer = base64.b64decode(msg_data["ImgBuf"]["buffer"])
                except Exception:
                    pass

        return msg


@dataclass
class VideoMessage(BaseMessage):
    """视频消息"""

    video_url: str = ""  # 视频URL
    thumbnail_url: str = ""  # 缩略图URL
    play_length: int = 0  # 播放时长(秒)
    video_md5: str = ""  # 视频MD5值
    aes_key: str = ""  # AES密钥

    @classmethod
    def from_dict(cls, data: Dict[str, Any], client=None) -> "VideoMessage":
        """从字典创建视频消息对象

        Args:
            data: 原始数据
            client: GewechatClient实例，用于下载视频
        """
        msg = cls(
            type=MessageType.VIDEO,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_user = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_user = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取视频信息
                try:
                    root = ET.fromstring(msg.content)
                    video_node = root.find("videomsg")
                    if video_node is not None:
                        msg.video_url = video_node.get("cdnvideourl", "")
                        msg.thumbnail_url = video_node.get("cdnthumburl", "")
                        msg.play_length = int(video_node.get("playlength", "0"))
                        msg.aes_key = video_node.get("aeskey", "")
                        msg.video_md5 = video_node.get("md5", "")

                        # 如果提供了GewechatClient实例，使用API获取下载链接
                        if client and msg.content:
                            # 调用下载视频接口获取文件URL
                            try:
                                download_result = client.message.download_video(
                                    msg.content
                                )
                                if (
                                    download_result
                                    and download_result.get("ret") == 200
                                    and "data" in download_result
                                ):
                                    file_url = download_result["data"].get(
                                        "fileUrl", ""
                                    )
                                    if file_url and client.download_url:
                                        msg.video_url = (
                                            f"{client.download_url}?url={file_url}"
                                        )
                            except Exception:
                                # 下载失败不影响消息处理
                                pass
                except Exception:
                    pass

        return msg


@dataclass
class EmojiMessage(BaseMessage):
    """表情消息"""

    emoji_md5: str = ""  # 表情MD5值
    emoji_url: str = ""  # 表情URL

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmojiMessage":
        """从字典创建表情消息对象"""
        msg = cls(
            type=MessageType.EMOJI,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_user = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_user = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取表情信息
                try:
                    root = ET.fromstring(msg.content)
                    emoji_node = root.find("emoji")
                    if emoji_node is not None:
                        msg.emoji_md5 = emoji_node.get("md5", "")
                        msg.emoji_url = emoji_node.get("cdnurl", "")
                except Exception:
                    pass

        return msg


@dataclass
class FinderMessage(BaseMessage):
    """视频号消息"""

    finder_id: str = ""  # 视频号ID
    finder_username: str = ""  # 视频号用户名
    finder_nickname: str = ""  # 视频号昵称
    object_id: str = ""  # 内容ID
    object_type: str = ""  # 内容类型，例如视频、直播等
    object_title: str = ""  # 内容标题
    object_desc: str = ""  # 内容描述
    cover_url: str = ""  # 封面URL
    url: str = ""  # 分享链接URL

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FinderMessage":
        """从字典创建视频号消息对象"""
        msg = cls(
            type=MessageType.FINDER,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

        if "Data" in data:
            msg_data = data["Data"]
            msg.msg_id = str(msg_data.get("MsgId", ""))
            msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
            msg.create_time = msg_data.get("CreateTime", 0)

            if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                msg.from_user = msg_data["FromUserName"]["string"]

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_user = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取视频号信息
                try:
                    root = ET.fromstring(msg.content)
                    appmsg = root.find("appmsg")
                    if appmsg is not None:
                        # 获取视频号ID
                        finder_info = appmsg.find("finderFeed")
                        if finder_info is not None:
                            msg.finder_id = finder_info.get("id", "")
                            msg.finder_username = finder_info.get("username", "")
                            msg.finder_nickname = finder_info.get("nickname", "")
                            msg.object_id = finder_info.get("objectId", "")
                            msg.object_type = finder_info.get("objectType", "")
                            msg.object_title = finder_info.get("title", "")
                            msg.object_desc = finder_info.get("desc", "")
                            msg.cover_url = finder_info.get("coverUrl", "")

                        # 获取URL
                        url_node = appmsg.find("url")
                        if url_node is not None and url_node.text:
                            msg.url = url_node.text
                except Exception:
                    pass

        return msg
