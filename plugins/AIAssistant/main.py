import asyncio
from openai import AsyncOpenAI
from opengewe.utils.plugin_base import PluginBase
from opengewe.utils.decorators import on_text_message
from opengewe.callback.models.text import TextMessage
from opengewe.client import GeweClient

class AIAssistant(PluginBase):
    """AI对话助手"""
    name = "AI对话助手"
    description = "在私聊中通过特定指令开启和关闭对话模式，提供基于大语言模型的智能对话能力。"
    author = "Wangnov"
    version = "1.1.0"

    def __init__(self, config):
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url")
        self.model = self.config.get("model", "gpt-4o")
        self.system_prompt = self.config.get("system_prompt", "你是一个乐于助人的AI助手。")
        self.trigger_word = self.config.get("trigger_word", "AI")
        
        self.conversation_history = {}  # {wxid: [messages]}
        self.session_status = {} # {wxid: bool}
        self.history_limit = self.config.get("history_limit", 10)

        if not self.api_key or not self.base_url:
            self.logger.error("缺少 API Key 或 Base URL，AI助手插件无法正常工作。")
            self.ai_client = None
        else:
            self.ai_client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    @on_text_message
    async def handle_ai_chat(self, client: GeweClient, message: TextMessage):
        if message.is_group_message or self.ai_client is None:
            return

        user_wxid = message.from_wxid
        user_input = message.content.strip()

        # 指令处理：开启/关闭对话模式
        if user_input == self.trigger_word:
            is_active = self.session_status.get(user_wxid, False)
            if not is_active:
                self.session_status[user_wxid] = True
                self.conversation_history[user_wxid] = [] # 开启新对话时清空历史
                await client.send_text_message(user_wxid, "AI对话模式已开启，您可以开始提问了。")
            else:
                self.session_status[user_wxid] = False
                await client.send_text_message(user_wxid, "AI对话模式已关闭。")
            return

        # 如果不处于对话模式，则不响应
        if not self.session_status.get(user_wxid, False):
            return

        # 初始化或获取对话历史
        history = self.conversation_history.setdefault(user_wxid, [])
        
        # 添加当前用户消息到历史
        history.append({"role": "user", "content": user_input})

        # 保持历史记录在限制内
        if len(history) > self.history_limit:
            history = history[-self.history_limit:]
            self.conversation_history[user_wxid] = history

        messages_to_send = [{"role": "system", "content": self.system_prompt}] + history

        try:
            response_stream = await self.ai_client.chat.completions.create(
                model=self.model,
                messages=messages_to_send,
                stream=True
            )

            full_response = ""
            buffer = ""
            last_send_time = asyncio.get_event_loop().time()

            async for chunk in response_stream:
                if chunk.choices[0].delta.content:
                    buffer += chunk.choices[0].delta.content
                    full_response += chunk.choices[0].delta.content
                    
                    current_time = asyncio.get_event_loop().time()
                    if (current_time - last_send_time > 0.8) or len(buffer) > 50:
                        if buffer:
                            await client.send_text_message(user_wxid, buffer)
                            buffer = ""
                        last_send_time = current_time
            
            if buffer:
                await client.send_text_message(user_wxid, buffer)

            if full_response:
                history.append({"role": "assistant", "content": full_response})

        except Exception as e:
            self.logger.error(f"请求AI模型失败: {e}", exc_info=True)
            await client.send_text_message(user_wxid, "抱歉，AI助手暂时无法连接，请稍后再试。")