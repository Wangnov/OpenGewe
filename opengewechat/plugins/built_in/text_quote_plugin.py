"""文字引用插件

此插件为message模块增加一个发送引用消息的方法。
"""

from typing import Dict, Optional, Any
import html
from opengewechat.plugins.base_plugin import BasePlugin
from opengewechat.message.models import BaseMessage
from opengewechat.client import GewechatClient


class TextQuotePlugin(BasePlugin):
    """文字引用插件

    为message模块增加一个send_text_quote方法，用于发送引用文字消息。

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
        self.name = "TextQuotePlugin"
        self.description = (
            "为message模块增加一个send_text_quote方法，用于发送引用文字消息"
        )
        self.version = "0.1.0"

    def on_load(self) -> None:
        """插件加载时调用

        为message模块增加send_text_quote方法
        """
        super().on_load()
        if self.client and hasattr(self.client, "message"):
            # 动态扩展message模块
            self.client.message.send_text_quote = self.send_text_quote

    def on_unload(self) -> None:
        """插件卸载时调用

        移除message模块中的send_text_quote方法
        """
        super().on_unload()
        if (
            self.client
            and hasattr(self.client, "message")
            and hasattr(self.client.message, "send_text_quote")
        ):
            delattr(self.client.message, "send_text_quote")

    def can_handle(self, message: BaseMessage) -> bool:
        """判断是否可以处理该消息

        本插件不处理消息，仅提供方法

        Args:
            message: 消息对象

        Returns:
            是否可以处理该消息
        """
        return False

    def send_text_quote(
        self,
        content: str,
        quote_message_raw_data: Dict[str, Any],
        to_wxid: Optional[str] = None,
    ) -> Dict:
        """发送引用文字消息

        Args:
            content (str): 要发送的文字内容
            quote_message_raw_data (Dict[str, Any]): 被引用消息的原始数据(message.raw_data属性)
            to_wxid (Optional[str], optional): 接收人的wxid，不提供时自动从raw_data中获取

        Returns:
            Dict: Gewechat返回结果
        """
        if (
            not self.client
            or not hasattr(self.client, "message")
            or not hasattr(self.client.message, "send_appmsg")
        ):
            return {"ret": 500, "msg": "Client或message模块不存在", "data": None}

        # 从原始数据中获取接收者wxid
        if to_wxid is None:
            data = quote_message_raw_data.get("Data", {})
            from_user_data = data.get("FromUserName", {})
            from_wxid = (
                from_user_data.get("string", "")
                if isinstance(from_user_data, dict)
                else ""
            )

            # 处理群消息情况
            if "@chatroom" in from_wxid:
                # 如果是群消息，从Content中提取发送者wxid
                content_data = data.get("Content", {})
                msg_content = (
                    content_data.get("string", "")
                    if isinstance(content_data, dict)
                    else ""
                )
                if ":" in msg_content:
                    parts = msg_content.split(":", 1)
                    if len(parts) == 2:
                        # # 记录发送者wxid，但仍然回复到群ID
                        # sender_wxid = parts[0].strip()
                        # 使用原群ID而不是发送者wxid，确保回复发送到群里
                        to_wxid = from_wxid
            else:
                # 普通消息直接回复发送者
                to_wxid = from_wxid

        # 如果仍未获取到有效的to_wxid
        if not to_wxid:
            return {
                "ret": 500,
                "msg": "未提供有效的接收者wxid，且无法从消息中提取",
                "data": None,
            }

        # 从原始数据中提取需要的信息构建XML
        appmsg_xml = self._build_quote_xml(content, quote_message_raw_data)

        # 调用send_appmsg方法发送
        return self.client.message.send_appmsg(to_wxid, appmsg_xml)

    def _build_quote_xml(
        self,
        content: str,
        quote_message_raw_data: Dict[str, Any],
    ) -> str:
        """构建引用消息的XML结构

        Args:
            content (str): 要发送的文字内容
            quote_message_raw_data (str): 被引用消息的原始数据

        Returns:
            str: 引用消息的XML结构
        """
        # 从原始数据中提取信息
        # 处理传入的JSON数据
        if isinstance(quote_message_raw_data, str):
            try:
                import json

                quote_message_raw_data = json.loads(quote_message_raw_data)
            except json.JSONDecodeError:
                return {"ret": 500, "msg": "无效的JSON数据", "data": None}

        data = quote_message_raw_data.get("Data", {})

        # 获取被引用消息的类型
        quote_msg_type = data.get("MsgType", 1)

        # 获取被引用消息的ID
        quote_msg_id = data.get("NewMsgId", "")

        # 获取被引用消息的创建时间
        quote_msg_createtime = data.get("CreateTime", 0)

        # 获取发送者信息
        from_user_data = data.get("FromUserName", {})
        quote_sender_wxid = (
            from_user_data.get("string", "") if isinstance(from_user_data, dict) else ""
        )

        # 处理群消息的发送者
        quote_sender_name = ""
        content_data = data.get("Content", {})
        msg_content = (
            content_data.get("string", "") if isinstance(content_data, dict) else ""
        )

        # 处理群消息中的发送者信息
        if "@chatroom" in quote_sender_wxid:
            if ":" in msg_content:
                parts = msg_content.split(":", 1)
                if len(parts) == 2:
                    quote_sender_wxid = parts[0].strip()
                    msg_content = parts[1].strip()

        # 如果是群消息但没有发送者名称，使用wxid作为名称
        if not quote_sender_name:
            quote_sender_name = quote_sender_wxid

        # 处理消息内容
        processed_content = self._process_xml_content(msg_content)

        # 构建引用消息XML
        appmsg_xml = f"""
        <appmsg appid="" sdkver="0">
        <title>{content}</title>
        <type>57</type>
        <refermsg>
            <type>{quote_msg_type}</type>
            <svrid>{quote_msg_id}</svrid>
            <fromusr>{quote_sender_wxid}</fromusr>
            <chatusr />
            <displayname>{quote_sender_name}</displayname>
            <content>{processed_content}</content>
            <createtime>{quote_msg_createtime}</createtime>
        </refermsg>
    </appmsg>
        """

        # 移除XML中的多余空白和换行，保持格式整洁
        return appmsg_xml.strip()

    def _process_xml_content(self, content: str) -> str:
        """处理XML格式的内容，确保正确转义

        Args:
            content (str): 原始XML内容

        Returns:
            str: 处理后的内容
        """
        try:
            # 先尝试解析XML
            if content.strip().startswith("<") and ">" in content:
                # 如果内容看起来像XML
                # 不直接解析，直接转义所有XML标签
                return html.escape(content)
            else:
                # 非XML内容直接返回
                return content
        except Exception:
            # 解析失败时，直接返回原内容
            return content
