from opengewe.utils.plugin_base import PluginBase
from opengewe.utils.decorators import on_text_message
from opengewe.callback.models.text import TextMessage
from opengewe.client import GeweClient


class KnowledgeBaseAssistant(PluginBase):
    """智能知识库助手"""
    name = "KnowledgeBaseAssistant"
    description = "根据关键词从知识库检索信息"
    author = "Roo"
    version = "0.1.0"

    def __init__(self, config):
        super().__init__(config)
        # 模拟知识库
        self.knowledge_base = {
            "如何报销": "请访问 a.com/reimbursement 提交报销申请。",
            "wifi密码": "公司WiFi密码是 a-b-c-d。",
            "打印机": "打印机驱动下载地址：a.com/printer-drivers",
        }
        self.command_keywords = ["帮助", "知识库"]

    @on_text_message
    async def handle_knowledge_query(self, client: GeweClient, message: TextMessage):
        """处理知识库查询"""
        content = message.text.strip()
        triggered_keyword = None

        for keyword in self.command_keywords:
            if content.startswith(keyword):
                triggered_keyword = keyword
                break

        if not triggered_keyword:
            return

        query = content[len(triggered_keyword):].strip()

        if not query:
            await client.send_text_message(
                wxid=message.from_wxid,
                content=f"请输入您想查询的内容，例如：{triggered_keyword} 如何报销"
            )
            return

        answer = self.knowledge_base.get(query, "抱歉，没有找到相关信息。您可以尝试其他关键词。")

        reply_content = f"【知识库助手】\n查询: {query}\n答案: {answer}"

        await client.send_text_message(
            wxid=message.from_wxid,
            content=reply_content
        )
