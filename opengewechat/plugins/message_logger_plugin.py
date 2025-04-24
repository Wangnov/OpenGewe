"""消息日志记录插件

此插件用于记录所有接收到的消息，保存到日志文件中。
日志按日期归类，默认保存在项目根目录的OGLogs文件夹下。
"""

import os
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from opengewechat.plugins.base_plugin import BasePlugin
from opengewechat.message.models import BaseMessage


class MessageLoggerPlugin(BasePlugin):
    """消息日志记录插件

    记录所有接收到的消息到日志文件中，按日期归类。
    """

    def __init__(self, client=None, log_dir: Optional[str] = None):
        """初始化消息日志记录插件

        Args:
            client: GewechatClient实例
            log_dir: 日志保存目录，默认为项目根目录下的OGLogs文件夹
        """
        super().__init__(client)
        self.name = "MessageLoggerPlugin"
        self.description = "消息日志记录插件，记录所有接收到的消息到日志文件中"
        self.version = "1.0.0"
        self.enabled = True  # 默认启用

        # 设置日志目录
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            # 默认在项目根目录下创建OGLogs文件夹
            self.log_dir = Path(os.getcwd()) / "OGLogs"

        # 确保日志目录存在
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("message_logger")
        self.logger.setLevel(logging.INFO)
        # 防止日志重复输出
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info(
            f"MessageLoggerPlugin 初始化完成，日志保存目录: {self.log_dir}"
        )

    def can_handle(self, message: BaseMessage) -> bool:
        """判断是否可以处理该消息

        本插件可以处理所有类型的消息

        Args:
            message: 消息对象

        Returns:
            始终返回True，表示可以处理所有消息
        """
        return True

    def _get_log_file_path(self) -> Path:
        """获取当前日期的日志文件路径

        Returns:
            日志文件路径
        """
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return self.log_dir / f"{today}.log"

    def _message_to_dict(self, message: BaseMessage) -> Dict[str, Any]:
        """将消息对象转换为字典，用于保存到日志

        Args:
            message: 消息对象

        Returns:
            消息字典
        """
        # 基础信息
        message_dict = {
            "type": str(message.type),
            "datetime": message.datetime,
            "create_time": message.create_time,
            "msg_id": message.msg_id,
            "new_msg_id": message.new_msg_id,
            "from_user": message.from_user,
            "to_user": message.to_user,
            "is_group_message": message.is_group_message,
            "content": message.content,
        }

        # 如果是群消息，添加群ID
        if message.is_group_message and message.room_wxid:
            message_dict["room_wxid"] = message.room_wxid

        # 添加消息类型特有的字段
        specific_attrs = {}

        # 获取消息对象的所有属性，排除基类属性和内置属性
        base_attrs = set(dir(BaseMessage))
        for attr in dir(message):
            if (
                attr not in base_attrs
                and not attr.startswith("_")
                and not callable(getattr(message, attr))
                and attr not in message_dict
            ):
                try:
                    value = getattr(message, attr)
                    # 跳过复杂对象和二进制数据
                    if not isinstance(
                        value, (bytes, bytearray, memoryview)
                    ) and not hasattr(value, "__dict__"):
                        specific_attrs[attr] = str(value)
                except Exception:
                    pass

        if specific_attrs:
            message_dict["specific_attrs"] = specific_attrs

        return message_dict

    def handle(self, message: BaseMessage) -> None:
        """处理消息，记录到日志文件

        Args:
            message: 消息对象
        """
        try:
            # 获取日志文件路径
            log_file = self._get_log_file_path()

            # 将消息转换为字典
            message_dict = self._message_to_dict(message)

            # 将消息保存到日志文件
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(message_dict, ensure_ascii=False) + "\n")

            self.logger.debug(f"消息已记录到日志文件: {log_file}")
        except Exception as e:
            self.logger.error(f"记录消息到日志文件时出错: {e}")

    def on_enable(self) -> None:
        """插件启用时调用"""
        super().on_enable()
        self.logger.info("MessageLoggerPlugin 已启用")

    def on_disable(self) -> None:
        """插件禁用时调用"""
        super().on_disable()
        self.logger.info("MessageLoggerPlugin 已禁用")

    def change_log_directory(self, new_dir: str) -> None:
        """更改日志保存目录

        Args:
            new_dir: 新的日志保存目录
        """
        self.log_dir = Path(new_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"日志保存目录已更改为: {self.log_dir}")
