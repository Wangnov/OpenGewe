from opengewe.utils.plugin_base import PluginBase
from opengewe.utils.decorators import on_text_message
from opengewe.callback.models.text import TextMessage
from opengewe.client import GeweClient


class KeywordMonitor(PluginBase):
    """关键词舆情监控"""
    name = "关键词舆情监控"
    description = "监控群聊中的关键词并发送提醒"
    author = "Roo"
    version = "0.1.1"

    def __init__(self, config):
        super().__init__(config)
        self.keywords = self.config.get("keywords", [])
        self.alert_to_wxid = self.config.get("alert_to_wxid")

    @on_text_message
    async def handle_keyword_monitoring(self, client: GeweClient, message: TextMessage):
        """处理关键词监控"""
        if not self.alert_to_wxid or not self.keywords:
            self.logger.warning("未配置关键词或提醒对象，插件未激活。")
            return

        if not message.is_group_message:
            return

        for keyword in self.keywords:
            if keyword in message.content:
                room_id = message.from_wxid
                sender_id = message.sender_wxid

                # 设置默认值，以防API请求失败
                room_name = room_id
                sender_name = sender_id

                try:
                    # 1. 获取群聊名称 (使用更可靠的专用方法)
                    room_info_res = await client.group.get_chatroom_info(chatroom_id=room_id)
                    if room_info_res.get("ret") == 200 and "data" in room_info_res:
                        room_data = room_info_res["data"]
                        # 尝试从多个可能的键获取群名，提高兼容性
                        room_name = room_data.get("name") or room_data.get("nickName", room_id)

                    # 2. 获取成员昵称 (优化解析逻辑，增加备选字段)
                    member_info_res = await client.group.get_chatroom_member_detail(chatroom_id=room_id, member_wxids=[sender_id])
                    print(member_info_res)
                    if member_info_res.get("ret") == 200 and "data" in member_info_res:
                        member_list = member_info_res.get("data", [])
                        if member_list:
                            # remark是备注, nickName是微信昵称, 作为备选
                            sender_name = member_list[0].get("remark") or member_list[0].get("nickName", sender_id)

                except Exception as e:
                    self.logger.error(f"获取群聊或成员信息时出错: {e}", exc_info=True)

                alert_message = (
                    f"【舆情警报】\n"
                    f"群聊: {room_name}\n"
                    f"发言人: {sender_name}\n"
                    f"关键词: {keyword}\n"
                    f"内容: {message.content}"
                )
                try:
                    await client.send_text_message(
                        wxid=self.alert_to_wxid,
                        content=alert_message
                    )
                    self.logger.info(f"已发送关键词 '{keyword}' 的警报。")
                except Exception as e:
                    self.logger.error(f"发送警报失败: {e}")
                break
