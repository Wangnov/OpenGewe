"""表情包标注插件

此插件用于检测引用的表情包消息，并记录表情包的标注内容。
当收到以"标注"开头的引用表情包消息时，将提取表情包的MD5值和标注内容，
并将其保存到项目根目录的emoji_explain.json文件中。
"""

import os
import json
import re
import html
import logging
from pathlib import Path
from typing import Dict, Optional, Any

from opengewechat.plugins.base_plugin import BasePlugin
from opengewechat.message.models import BaseMessage


class EmojiAnnotationPlugin(BasePlugin):
    """表情包标注插件

    检测引用的表情包消息，并记录表情包的标注内容。
    """

    def __init__(self, client=None):
        """初始化表情包标注插件

        Args:
            client: GewechatClient实例
        """
        super().__init__(client)
        self.name = "EmojiAnnotationPlugin"
        self.description = "表情包标注插件，记录表情包的标注内容"
        self.version = "1.0.0"
        self.enabled = True  # 默认启用
        
        # 设置日志
        self.logger = logging.getLogger("emoji_annotation")
        self.logger.setLevel(logging.INFO)
        # 防止日志重复输出
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # emoji_explain.json 文件路径
        self.json_file = Path(os.getcwd()) / "emoji_explain.json"
        
        # 加载现有的标注数据
        self.emoji_annotations = self._load_annotations()

    def _load_annotations(self) -> Dict[str, str]:
        """加载现有的表情包标注数据

        Returns:
            Dict[str, str]: 表情包MD5和标注内容的字典
        """
        if self.json_file.exists():
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"加载表情包标注数据失败: {e}")
                return {}
        return {}

    def _save_annotations(self) -> None:
        """保存表情包标注数据到JSON文件"""
        try:
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump(self.emoji_annotations, f, ensure_ascii=False, indent=4)
            self.logger.info(f"表情包标注数据已保存到: {self.json_file}")
        except Exception as e:
            self.logger.error(f"保存表情包标注数据失败: {e}")

    def _extract_emoji_md5(self, content: str) -> Optional[str]:
        """从内容中提取表情包的MD5值

        Args:
            content: 消息内容

        Returns:
            Optional[str]: 表情包的MD5值，如果不是表情包则返回None
        """
        # 对XML转义内容进行解码
        content = html.unescape(content)
        
        # 使用正则表达式提取emoji标签中的md5属性
        emoji_pattern = r'<emoji\s+md5="([a-f0-9]+)"'
        match = re.search(emoji_pattern, content)
        
        if match:
            return match.group(1)
        return None

    def _is_quote_message(self, message: BaseMessage) -> bool:
        """判断消息是否为引用消息

        Args:
            message: 消息对象

        Returns:
            bool: 是否为引用消息
        """
        # 检查消息类型是否为49 (应用消息)
        if message.raw_data.get("Data", {}).get("MsgType") != 49:
            return False
        
        # 检查XML内容中是否包含refermsg标签
        content = message.raw_data.get("Data", {}).get("Content", {}).get("string", "")
        return "<refermsg>" in content

    def _extract_title(self, content: str) -> Optional[str]:
        """从消息内容中提取title标签的内容

        Args:
            content: 消息内容

        Returns:
            Optional[str]: title标签的内容
        """
        title_pattern = r'<title>(.*?)</title>'
        match = re.search(title_pattern, content)
        
        if match:
            return match.group(1)
        return None

    def _extract_refer_content(self, content: str) -> Optional[str]:
        """从引用消息中提取被引用内容

        Args:
            content: 消息内容

        Returns:
            Optional[str]: 被引用的内容
        """
        content_pattern = r'<content>(.*?)</content>'
        match = re.search(content_pattern, content)
        
        if match:
            return match.group(1)
        return None

    def _extract_appmsg(self, content: str) -> Optional[str]:
        """从消息内容中提取appmsg标签

        Args:
            content: 消息内容

        Returns:
            Optional[str]: appmsg标签的内容
        """
        # 提取完整的appmsg标签
        appmsg_pattern = r'(<appmsg.*?</appmsg>)'
        match = re.search(appmsg_pattern, content, re.DOTALL)
        
        if match:
            return match.group(1)
        return None

    def _build_reply_xml(self, original_appmsg: str, emoji_md5: str, annotation_text: str) -> str:
        """构建回复消息的XML结构

        Args:
            original_appmsg: 原始appmsg标签内容
            emoji_md5: 表情包MD5
            annotation_text: 标注内容

        Returns:
            str: 回复消息的XML结构
        """
        # 替换title标签内容
        reply_content = f"表情包：{emoji_md5} 已成功设置标签为：{annotation_text}"
        
        # 使用正则表达式替换title标签内容
        modified_appmsg = re.sub(
            r'<title>.*?</title>',
            f'<title>{reply_content}</title>',
            original_appmsg
        )
        
        return modified_appmsg

    def can_handle(self, message: BaseMessage) -> bool:
        """判断是否可以处理该消息

        Args:
            message: 消息对象

        Returns:
            bool: 是否可以处理该消息
        """
        # 判断是否为引用消息
        if not self._is_quote_message(message):
            return False
        
        # 提取消息内容
        content = message.raw_data.get("Data", {}).get("Content", {}).get("string", "")
        
        # 提取title
        title = self._extract_title(content)
        if not title or not title.startswith("标注"):
            return False
        
        # 提取被引用的内容
        refer_content = self._extract_refer_content(content)
        if not refer_content:
            return False
        
        # 检查是否为表情包
        emoji_md5 = self._extract_emoji_md5(refer_content)
        
        return emoji_md5 is not None

    def handle(self, message: BaseMessage) -> None:
        """处理消息，提取表情包标注内容并保存

        Args:
            message: 消息对象
        """
        try:
            # 提取消息内容
            content = message.raw_data.get("Data", {}).get("Content", {}).get("string", "")
            
            # 提取title
            title = self._extract_title(content)
            if not title:
                return
            
            # 从title中提取标注内容
            # 去掉开头的"标注"，并去除前后空格
            annotation_text = title[2:].strip()
            
            # 提取被引用的内容
            refer_content = self._extract_refer_content(content)
            if not refer_content:
                return
            
            # 提取表情包MD5
            emoji_md5 = self._extract_emoji_md5(refer_content)
            if not emoji_md5:
                return
            
            # 记录表情包标注
            self.emoji_annotations[emoji_md5] = annotation_text
            
            # 保存到JSON文件
            self._save_annotations()
            
            self.logger.info(f"已记录表情包标注: {emoji_md5} -> {annotation_text}")
            
            # 发送回复消息
            self._send_reply_message(message, emoji_md5, annotation_text)
        except Exception as e:
            self.logger.error(f"处理表情包标注消息时出错: {e}")

    def _send_reply_message(self, original_message: BaseMessage, emoji_md5: str, annotation_text: str) -> None:
        """发送表情包标注成功的回复消息

        Args:
            original_message: 原始消息对象
            emoji_md5: 表情包MD5
            annotation_text: 标注内容
        """
        if not self.client or not hasattr(self.client, "message") or not hasattr(self.client.message, "send_appmsg"):
            self.logger.error("无法发送回复消息，client或message模块不存在")
            return
            
        try:
            # 提取原始消息内容
            content = original_message.raw_data.get("Data", {}).get("Content", {}).get("string", "")
            
            # 提取appmsg标签
            original_appmsg = self._extract_appmsg(content)
            if not original_appmsg:
                self.logger.error("无法提取appmsg标签")
                return
                
            # 构建回复消息XML
            reply_xml = self._build_reply_xml(original_appmsg, emoji_md5, annotation_text)
            
            # 确定接收者wxid
            # 从原始数据中获取接收者wxid
            data = original_message.raw_data.get("Data", {})
            from_user_data = data.get("FromUserName", {})
            from_wxid = (
                from_user_data.get("string", "")
                if isinstance(from_user_data, dict)
                else ""
            )

            # 处理群消息情况
            to_wxid = from_wxid
            
            # 调用send_appmsg方法发送回复消息
            result = self.client.message.send_appmsg(to_wxid, reply_xml)
            
            if result.get("ret") == 0:
                self.logger.info("表情包标注成功回复消息已发送")
            else:
                self.logger.error(f"发送回复消息失败: {result}")
        except Exception as e:
            self.logger.error(f"发送回复消息时出错: {e}")

    def on_enable(self) -> None:
        """插件启用时调用"""
        super().on_enable()
        self.logger.info("EmojiAnnotationPlugin 已启用")

    def on_disable(self) -> None:
        """插件禁用时调用"""
        super().on_disable()
        self.logger.info("EmojiAnnotationPlugin 已禁用") 