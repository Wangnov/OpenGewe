from opengewe.utils.plugin_base import PluginBase
from opengewe.utils.decorators import on_text_message
from opengewe.callback.models.text import TextMessage
from opengewe.client import GeweClient
import json


class KnowledgeBaseAssistant(PluginBase):
    """智能知识库助手"""
    name = "知识库助手"
    description = "根据关键词从知识库检索信息，并@提问者进行回复"
    author = "Roo"
    version = "0.3.1"

    def __init__(self, config):
        super().__init__(config)
        self.knowledge_base = self.config.get("knowledge_base", {})
        self.command_keywords = self.config.get("command_keywords", ["帮助", "知识库"])
        print("--- KnowledgeBaseAssistant 插件已加载 ---")
        print(f"关键词: {self.command_keywords}")
        print(f"知识库条目数: {len(self.knowledge_base)}")

    @on_text_message
    async def handle_knowledge_query(self, client: GeweClient, message: TextMessage):
        """处理知识库查询"""
        print("\n--- 收到新消息，进入知识库查询处理 ---")
        content = message.content.strip()
        print(f"原始消息内容: {content}")
        triggered_keyword = None

        for keyword in self.command_keywords:
            if content.startswith(keyword):
                triggered_keyword = keyword
                break

        if not triggered_keyword:
            print("未匹配到关键词，处理结束。")
            return

        print(f"匹配到关键词: {triggered_keyword}")
        query = content[len(triggered_keyword):].strip()
        print(f"解析出的查询语句: '{query}'")
        
        reply_to_wxid = message.from_wxid
        at_wxid = ""
        sender_name = ""

        if message.is_group_message:
            print("是群聊消息，准备获取成员信息...")
            at_wxid = message.sender_wxid
            print(f"群ID (from_wxid): {message.from_wxid}")
            print(f"发送者ID (sender_wxid): {at_wxid}")
            try:
                print("--> 正在调用 client.group.get_chatroom_member_detail...")
                member_info_res = await client.group.get_chatroom_member_detail(
                    chatroom_id=message.from_wxid, member_wxids=[at_wxid]
                )
                print(f"<-- API返回: {json.dumps(member_info_res, indent=2, ensure_ascii=False)}")
                if member_info_res.get("ret") == 200 and "data" in member_info_res:
                    member_list = member_info_res.get("data", [])
                    if member_list:
                        sender_name = member_list[0].get("remark") or member_list[0].get("nickName", "")
                        print(f"成功获取到发送者昵称: {sender_name}")
                    else:
                        print("API调用成功，但返回的成员列表为空。")
                else:
                    print("API调用失败或返回数据格式不正确。")
            except Exception as e:
                self.logger.error(f"获取群成员 '{at_wxid}' 信息失败: {e}", exc_info=True)
                print(f"!!! 获取群成员信息时发生异常: {e}")

        if not query:
            reply_content = f"请输入您想查询的内容，例如：{triggered_keyword} 如何报销"
            if sender_name:
                reply_content = f"@{sender_name} {reply_content}"
            
            print(f"--> 准备发送空查询提示: to='{reply_to_wxid}', at='{at_wxid}', content='{reply_content}'")
            await client.send_text_message(
                wxid=reply_to_wxid,
                content=reply_content,
                at=at_wxid
            )
            print("<-- 空查询提示已发送。处理结束。")
            return

        answer = self.knowledge_base.get(query, "抱歉，没有找到相关信息。您可以尝试其他关键词。")
        print(f"从知识库查找到的答案: {answer}")

        reply_content = f"【知识库助手】\n查询: {query}\n答案: {answer}"
        if sender_name:
            reply_content = f"@{sender_name}\n{reply_content}"

        print(f"--> 准备发送最终回复: to='{reply_to_wxid}', at='{at_wxid}', content='{reply_content}'")
        await client.send_text_message(
            wxid=reply_to_wxid,
            content=reply_content,
            at=at_wxid
        )
        print("<-- 最终回复已发送。处理结束。")
