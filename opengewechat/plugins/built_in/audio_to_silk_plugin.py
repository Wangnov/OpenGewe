"""音频转Silk插件

此插件提供音频文件转换为微信语音所需的silk格式的功能。
支持将常见音频格式（如MP3、WAV等）转换为Silk格式，以便通过微信发送语音消息。
"""

import os
import av
import pilk
import tempfile
from pathlib import Path
from typing import Optional, Dict, Tuple

from opengewechat.plugins.base_plugin import BasePlugin
from opengewechat.client import GewechatClient


class AudioToSilkPlugin(BasePlugin):
    """音频转Silk插件

    为utils模块增加一个convert_audio_to_silk方法，用于将音频文件转换为silk格式。

    Attributes:
        name: 插件名称
        description: 插件描述
        version: 插件版本
    """

    def __init__(self, client: Optional[GewechatClient] = None):
        """初始化插件

        Args:
            client: GewechatClient实例
        """
        super().__init__(client)
        self.name = "AudioToSilkPlugin"
        self.description = (
            "为utils模块增加一个convert_audio_to_silk方法，用于将音频文件转换为silk格式"
        )
        self.version = "0.1.0"

    def on_load(self) -> None:
        """插件加载时调用

        为client增加utils属性（如果不存在），然后为utils增加convert_audio_to_silk方法
        """
        super().on_load()
        if self.client:
            # 如果client没有utils属性，创建一个空的对象
            if not hasattr(self.client, "utils"):
                self.client.utils = type("Utils", (), {})()

            # 动态扩展utils模块
            self.client.utils.convert_audio_to_silk = self.convert_audio_to_silk

    def on_unload(self) -> None:
        """插件卸载时调用

        移除utils模块中的convert_audio_to_silk方法
        """
        super().on_unload()
        if (
            self.client
            and hasattr(self.client, "utils")
            and hasattr(self.client.utils, "convert_audio_to_silk")
        ):
            delattr(self.client.utils, "convert_audio_to_silk")

    def can_handle(self, message) -> bool:
        """判断是否可以处理该消息

        本插件不处理消息，仅提供方法

        Args:
            message: 消息对象

        Returns:
            是否可以处理该消息
        """
        return False

    def _audio_to_pcm(self, input_path: str) -> Tuple[str, int, int]:
        """将音频文件转换为PCM格式

        Args:
            input_path: 输入音频文件路径

        Returns:
            Tuple[str, int, int]: PCM文件临时路径、音频时长（毫秒）和采样率
        """
        # 创建临时文件用于存储PCM数据
        tmp_pcm = tempfile.NamedTemporaryFile(suffix=".pcm", delete=False)
        tmp_pcm_path = tmp_pcm.name
        tmp_pcm.close()

        # 使用PyAV加载音频
        container = av.open(input_path)
        audio = container.streams.audio[0]

        # 获取原始采样率
        original_sample_rate = audio.codec_context.sample_rate

        # 计算总时长（毫秒）
        duration_ms = int(float(audio.duration * 1000) / audio.time_base)

        # 创建重采样器，保持原始采样率，转换为单声道, S16格式
        resampler = av.AudioResampler(
            format="s16", layout="mono", rate=original_sample_rate
        )

        # 创建PCM输出
        with open(tmp_pcm_path, "wb") as pcm_file:
            # 解码音频为PCM
            for frame in container.decode(audio):
                # 重采样为原始采样率，单声道，S16格式
                frame.pts = None
                for new_frame in resampler.resample(frame):
                    # 获取PCM数据
                    pcm_data = new_frame.to_ndarray()
                    pcm_file.write(pcm_data.tobytes())

        return tmp_pcm_path, duration_ms, original_sample_rate

    def _adjust_duration(self, duration_ms: int) -> int:
        """调整音频时长在有效范围内

        Args:
            duration_ms: 原始音频时长（毫秒）

        Returns:
            int: 调整后的时长，确保在1000-60000毫秒之间
        """
        if duration_ms < 1000:
            return 1000
        elif duration_ms > 60000:
            return 60000
        return duration_ms

    def convert_audio_to_silk(self, input_path: str, output_dir: str) -> Dict:
        """将音频文件转换为Silk格式

        Args:
            input_path: 输入音频文件路径
            output_dir: 输出目录

        Returns:
            Dict: 转换结果
                {
                    "success": bool,  # 是否成功
                    "file_path": str,  # 生成的文件路径
                    "duration": int,   # 语音时长（毫秒）
                    "message": str     # 结果信息
                }
        """
        try:
            # 检查输入文件是否存在
            if not os.path.exists(input_path):
                return {
                    "success": False,
                    "file_path": None,
                    "duration": 0,
                    "message": f"输入文件不存在: {input_path}",
                }

            # 确保输出目录存在
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # 生成输出文件名
            input_filename = os.path.basename(input_path)
            output_filename = os.path.splitext(input_filename)[0] + ".silk"
            output_path = os.path.join(output_dir, output_filename)

            # 将音频转换为PCM，同时获取原始采样率
            pcm_path, duration_ms, sample_rate = self._audio_to_pcm(input_path)

            try:
                # 将PCM转换为Silk，使用原始音频的采样率
                duration_ms = pilk.encode(
                    pcm_path, output_path, pcm_rate=sample_rate, tencent=True
                )

                # 调整时长确保在有效范围内
                duration_ms = self._adjust_duration(duration_ms * 1000)

                return {
                    "success": True,
                    "file_path": output_path,
                    "duration": duration_ms,
                    "message": "音频转换成功",
                }
            finally:
                # 清理临时PCM文件
                if os.path.exists(pcm_path):
                    os.unlink(pcm_path)

        except Exception as e:
            return {
                "success": False,
                "file_path": None,
                "duration": 0,
                "message": f"转换过程中出错: {str(e)}",
            }
