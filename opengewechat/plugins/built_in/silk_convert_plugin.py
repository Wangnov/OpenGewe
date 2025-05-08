"""音频转Silk插件

此插件提供音频文件转换为微信语音所需的silk格式的功能。
支持将常见音频格式（如MP3、WAV等）转换为Silk格式，以便通过微信发送语音消息。
同时也支持将Silk格式转换回常见音频格式。
需安装FFmpeg
"""

import os
import pilk
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Dict, Tuple, Literal

from opengewechat.plugins.base_plugin import BasePlugin
from opengewechat.client import GewechatClient


class SilkConvertPlugin(BasePlugin):
    """Silk格式转换插件

    为utils模块增加convert_audio_to_silk和convert_silk_to_audio方法，
    用于音频与silk格式之间的相互转换。

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
        self.description = "为utils模块增加音频与silk格式之间的相互转换方法"
        self.version = "0.1.1"

    def on_load(self) -> None:
        """插件加载时调用

        为client增加utils属性（如果不存在），然后为utils增加convert_audio_to_silk和convert_silk_to_audio方法
        """
        super().on_load()
        if self.client:
            # 如果client没有utils属性，创建一个空的对象
            if not hasattr(self.client, "utils"):
                self.client.utils = type("Utils", (), {})()

            # 动态扩展utils模块
            self.client.utils.convert_audio_to_silk = self.convert_audio_to_silk
            self.client.utils.convert_silk_to_audio = self.convert_silk_to_audio

    def on_unload(self) -> None:
        """插件卸载时调用

        移除utils模块中的convert_audio_to_silk和convert_silk_to_audio方法
        """
        super().on_unload()
        if self.client and hasattr(self.client, "utils"):
            if hasattr(self.client.utils, "convert_audio_to_silk"):
                delattr(self.client.utils, "convert_audio_to_silk")
            if hasattr(self.client.utils, "convert_silk_to_audio"):
                delattr(self.client.utils, "convert_silk_to_audio")

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
        """将音频文件转换为PCM格式，使用FFmpeg命令行工具

        Args:
            input_path: 输入音频文件路径

        Returns:
            Tuple[str, int, int]: PCM文件临时路径、音频时长（毫秒）和采样率
        """
        # 创建临时文件用于存储PCM数据
        tmp_pcm = tempfile.NamedTemporaryFile(suffix=".pcm", delete=False)
        tmp_pcm_path = tmp_pcm.name
        tmp_pcm.close()

        # 先获取音频文件信息
        probe_cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=sample_rate",
            "-of",
            "json",
            input_path,
        ]

        try:
            probe_result = subprocess.run(
                probe_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # 解析JSON输出
            import json

            info = json.loads(probe_result.stdout)

            # 获取采样率和时长
            try:
                # 尝试从音频流获取采样率
                original_sample_rate = int(info["streams"][0]["sample_rate"])
            except (KeyError, IndexError, ValueError):
                # 如果失败，使用默认采样率24000
                original_sample_rate = 24000

            try:
                # 获取时长（秒）并转换为毫秒
                duration_sec = float(info["format"]["duration"])
                duration_ms = int(duration_sec * 1000)
            except (KeyError, ValueError):
                # 如果无法获取时长，使用默认值
                duration_ms = 0
        except subprocess.CalledProcessError:
            # 如果ffprobe失败，使用默认值
            original_sample_rate = 24000
            duration_ms = 0

        # 转换为PCM (signed 16-bit little-endian, 单声道)
        convert_cmd = [
            "ffmpeg",
            "-i",
            input_path,
            "-f",
            "s16le",  # 输出格式：16位有符号小端PCM
            "-acodec",
            "pcm_s16le",  # 编码器
            "-ar",
            str(original_sample_rate),  # 保持原始采样率
            "-ac",
            "1",  # 单声道
            "-y",  # 覆盖输出文件
            tmp_pcm_path,
        ]

        try:
            subprocess.run(
                convert_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg转换失败: {e.stderr.decode('utf-8')}")

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

    def convert_silk_to_audio(
        self,
        input_path: str,
        output_dir: str,
        format: Literal["mp3", "m4a", "wav"] = "mp3",
    ) -> Dict:
        """将Silk格式音频文件转换为常规音频格式

        Args:
            input_path: 输入Silk文件路径
            output_dir: 输出目录
            format: 输出格式，支持"mp3"、"m4a"和"wav"，默认为"mp3"

        Returns:
            Dict: 转换结果
                {
                    "success": bool,  # 是否成功
                    "file_path": str,  # 生成的文件路径
                    "message": str     # 结果信息
                }
        """
        try:
            # 检查输入文件是否存在
            if not os.path.exists(input_path):
                return {
                    "success": False,
                    "file_path": None,
                    "message": f"输入文件不存在: {input_path}",
                }

            # 确保输出目录存在
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # 生成输出文件名
            input_filename = os.path.basename(input_path)
            output_filename = os.path.splitext(input_filename)[0] + f".{format}"
            output_path = os.path.join(output_dir, output_filename)

            # 创建临时文件用于存储PCM数据
            with tempfile.NamedTemporaryFile(suffix=".pcm", delete=False) as tmp_pcm:
                pcm_path = tmp_pcm.name

            try:
                # 将Silk解码为PCM，默认使用24000的采样率
                sample_rate = 24000
                pilk.decode(input_path, pcm_path)

                # 使用ffmpeg将PCM转换为目标格式
                try:
                    self._pcm_to_audio(pcm_path, output_path, sample_rate, format)
                except Exception as e:
                    # 如果首选格式失败，尝试回退到wav格式
                    if format != "wav":
                        fallback_output = os.path.splitext(output_path)[0] + ".wav"
                        self._pcm_to_audio(
                            pcm_path, fallback_output, sample_rate, "wav"
                        )
                        return {
                            "success": True,
                            "file_path": fallback_output,
                            "message": f"无法使用{format}格式，已转换为wav格式。原始错误: {str(e)}",
                        }
                    else:
                        raise

                return {
                    "success": True,
                    "file_path": output_path,
                    "message": f"Silk转换为{format}格式成功",
                }
            finally:
                # 清理临时PCM文件
                if os.path.exists(pcm_path):
                    os.unlink(pcm_path)

        except Exception as e:
            return {
                "success": False,
                "file_path": None,
                "message": f"转换过程中出错: {str(e)}",
            }

    def _pcm_to_audio(
        self, pcm_path: str, output_path: str, sample_rate: int, format: str
    ) -> None:
        """将PCM数据转换为指定的音频格式，使用FFmpeg以最高质量设置

        Args:
            pcm_path: PCM文件路径
            output_path: 输出音频文件路径
            sample_rate: PCM数据的采样率
            format: 输出格式，支持"mp3"、"m4a"和"wav"
        """
        # 针对不同格式设置最高质量参数
        if format == "mp3":
            # 对MP3使用最高质量设置
            quality_args = [
                "-codec:a",
                "libmp3lame",
                "-qscale:a",
                "0",  # 最高质量 (0-9, 0最好)
                "-b:a",
                "256k",  # 最高比特率
            ]
        elif format == "m4a":
            # 对M4A/AAC使用高质量设置
            quality_args = [
                "-codec:a",
                "aac",
                "-b:a",
                "256k",  # 高比特率
                "-vbr",
                "5",  # 高质量VBR模式 (1-5, 5最好)
            ]
        elif format == "wav":
            # 对WAV使用无损设置
            quality_args = ["-codec:a", "pcm_s16le", "-ar", str(sample_rate)]
        else:
            # 默认高质量设置
            quality_args = ["-codec:a", "aac", "-b:a", "256k"]

        # 构建FFmpeg命令
        cmd = [
            "ffmpeg",
            "-f",
            "s16le",  # 输入格式：有符号16位小端PCM
            "-ar",
            str(sample_rate),  # 采样率
            "-ac",
            "1",  # 通道数：单声道
            "-i",
            pcm_path,  # 输入文件
            *quality_args,  # 质量参数
            "-y",  # 覆盖输出文件
            output_path,  # 输出文件
        ]

        # 执行FFmpeg命令
        try:
            subprocess.run(
                cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg转换失败: {e.stderr.decode('utf-8')}")


if __name__ == "__main__":
    plugin = SilkConvertPlugin()
    result = plugin.convert_silk_to_audio(
        "/root/opengewechat/downloads/voice_2039114913.silk",
        "/root/opengewechat/downloads",
    )
    print(result)
