from dataclasses import dataclass
from typing import Dict, Any, Optional, TYPE_CHECKING
import xml.etree.ElementTree as ET

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import MediaBaseMessage
from opengewe.logger import get_logger

# 使用TYPE_CHECKING条件导入，只用于类型注解
if TYPE_CHECKING:
    from opengewe.client import GeweClient

logger = get_logger("Callback")


@dataclass
class ImageMessage(MediaBaseMessage):
    """图片消息"""
    img_download_url: str = ""  # 图片下载链接
    img_buffer: bytes = b""  # 图片buffer
    
    # 设置消息类型类变量
    message_type = MessageType.IMAGE
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理图片消息特有数据"""
        # 如果提供了GeweClient实例，使用API获取下载链接
        if client:
            # 尝试下载高清图片
            self.img_download_url = await self._download_media(
                client, client.message.download_image, self.content, type=1
            )
            
            # 如果高清图片下载失败，尝试下载常规图片
            if not self.img_download_url:
                self.img_download_url = await self._download_media(
                    client, client.message.download_image, self.content, type=2
                )
                
            # 如果常规图片下载失败，尝试下载缩略图
            if not self.img_download_url:
                self.img_download_url = await self._download_media(
                    client, client.message.download_image, self.content, type=3
                )
        
        # 获取缩略图数据
        if "Data" in data and "ImgBuf" in data["Data"] and "buffer" in data["Data"]["ImgBuf"]:
            import base64
            try:
                self.img_buffer = base64.b64decode(data["Data"]["ImgBuf"]["buffer"])
            except Exception:
                pass


@dataclass
class VoiceMessage(MediaBaseMessage):
    """语音消息"""
    voice_url: str = ""  # 语音文件URL
    voice_length: int = 0  # 语音长度(毫秒)
    voice_buffer: bytes = b""  # 语音buffer
    voice_md5: str = ""  # 语音MD5值
    aes_key: str = ""  # AES密钥
    
    # 设置消息类型类变量
    message_type = MessageType.VOICE

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
            logger.error(f"保存语音文件失败: {e}")
            return ""
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理语音消息特有数据"""
        try:
            # 解析XML获取语音信息
            root = ET.fromstring(self.content)
            voice_node = root.find("voicemsg")
            if voice_node is not None:
                self.voice_url = voice_node.get("voiceurl", "")
                self.voice_length = int(voice_node.get("voicelength", "0"))
                self.aes_key = voice_node.get("aeskey", "")

                # 如果提供了GeweClient实例，使用API获取下载链接
                if client:
                    self.voice_url = await self._download_media(
                        client, client.message.download_voice, self.content, msg_id=self.msg_id
                    )
        except Exception:
            pass

        # 获取语音数据
        if "Data" in data and "ImgBuf" in data["Data"] and "buffer" in data["Data"]["ImgBuf"]:
            import base64
            try:
                self.voice_buffer = base64.b64decode(data["Data"]["ImgBuf"]["buffer"])
            except Exception:
                pass


@dataclass
class VideoMessage(MediaBaseMessage):
    """视频消息"""
    video_url: str = ""  # 视频URL
    thumbnail_url: str = ""  # 缩略图URL
    play_length: int = 0  # 播放时长(秒)
    video_md5: str = ""  # 视频MD5值
    aes_key: str = ""  # AES密钥
    
    # 设置消息类型类变量
    message_type = MessageType.VIDEO
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理视频消息特有数据"""
        try:
            # 解析XML获取视频信息
            root = ET.fromstring(self.content)
            video_node = root.find("videomsg")
            if video_node is not None:
                self.video_url = video_node.get("cdnvideourl", "")
                self.thumbnail_url = video_node.get("cdnthumburl", "")
                self.play_length = int(video_node.get("playlength", "0"))
                self.aes_key = video_node.get("aeskey", "")
                self.video_md5 = video_node.get("md5", "")

                # 如果提供了GeweClient实例，使用API获取下载链接
                if client:
                    self.video_url = await self._download_media(
                        client, client.message.download_video, self.content
                    )
        except Exception:
            pass


@dataclass
class EmojiMessage(MediaBaseMessage):
    """表情消息"""
    emoji_md5: str = ""  # 表情MD5值
    emoji_url: str = ""  # 表情URL
    
    # 设置消息类型类变量
    message_type = MessageType.EMOJI
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理表情消息特有数据"""
        try:
            # 解析XML获取表情信息
            root = ET.fromstring(self.content)
            emoji_node = root.find("emoji")
            if emoji_node is not None:
                self.emoji_md5 = emoji_node.get("md5", "")
                self.emoji_url = emoji_node.get("cdnurl", "")
        except Exception:
            pass
