import asyncio
import aiohttp
import xml.etree.ElementTree as ET
from openai import AsyncOpenAI
from opengewe.utils.plugin_base import PluginBase
from opengewe.utils.decorators import on_file_message
from opengewe.callback.models.file import FileMessage
from opengewe.client import GeweClient

class FileAnalyzerAssistant(PluginBase):
    """文件分析助手"""
    name = "文件分析助手"
    description = "接收用户发送的txt文件，调用AI模型进行分析总结，并返回结果。"
    author = "Roo"
    version = "1.0.1"

    def __init__(self, config):
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url")
        self.model = self.config.get("model", "gpt-4o")
        self.system_prompt = self.config.get("system_prompt", "你是一个专业的文件分析助手，你的任务是根据用户提供的文本内容，进行简洁、清晰、专业的总结。")
        
        if not self.api_key or not self.base_url:
            self.logger.error("缺少 API Key 或 Base URL，文件分析助手无法正常工作。")
            self.ai_client = None
        else:
            self.ai_client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    @on_file_message
    async def handle_file_analysis(self, client: GeweClient, message: FileMessage):
        if message.is_group_message or self.ai_client is None:
            return {'success': True}

        if not message.file_name.lower().endswith(".txt"):
            await client.send_text_message(message.from_wxid, "抱歉，目前我只支持分析 .txt 格式的文件。")
            return {'success': True}

        await client.send_text_message(message.from_wxid, f"收到文件: {message.file_name}，正在为您分析，请稍候...")

        try:
            # 1. 下载文件
            download_res = await client.message.download_file(xml=message.content)
            if download_res.get("ret") != 200:
                raise Exception(f"下载文件API调用失败: {download_res.get('msg')}")
            
            file_url = download_res.get("data", {}).get("fileUrl")
            if not file_url:
                raise Exception("未能从API响应中获取文件下载链接。")

            # 2. 读取文件内容
            async with aiohttp.ClientSession() as session:
                async with session.get(file_url) as resp:
                    if resp.status != 200:
                        raise Exception(f"下载文件失败，HTTP状态码: {resp.status}")
                    file_content = await resp.text(encoding='utf-8')

            if not file_content:
                await client.send_text_message(message.from_wxid, "文件内容为空，无需分析。")
                return {'success': True}

            # 3. 调用AI进行分析
            messages_to_send = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"请分析并总结以下文本内容：\n\n---\n\n{file_content}"}
            ]

            ai_response = await self.ai_client.chat.completions.create(
                model=self.model,
                messages=messages_to_send,
                stream=False # 分析任务使用非流式，确保结果完整
            )
            
            summary = ai_response.choices[0].message.content

            # 4. 发送分析结果
            reply_content = f"【文件分析报告】\n文件名: {message.file_name}\n\n摘要:\n{summary}"
            await client.send_text_message(message.from_wxid, reply_content)
            return {'success': True}

        except Exception as e:
            self.logger.error(f"处理文件分析任务失败: {e}", exc_info=True)
            await client.send_text_message(message.from_wxid, f"处理文件 '{message.file_name}' 时出错，请稍后再试。")
            return {'success': False, 'error': str(e)}