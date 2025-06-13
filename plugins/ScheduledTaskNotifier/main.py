import asyncio
from opengewe.utils.plugin_base import PluginBase
from opengewe.client import GeweClient


class ScheduledTaskNotifier(PluginBase):
    """定时任务提醒"""
    name = "ScheduledTaskNotifier"
    description = "在指定时间发送提醒消息"
    author = "Roo"
    version = "0.1.0"

    def __init__(self, config):
        super().__init__(config)
        self.tasks = []

    async def on_enable(self, client: GeweClient):
        """插件启用时，启动定时任务"""
        self.client = client
        # 从配置加载任务
        self.tasks = self.config.get("tasks", [])
        if self.tasks:
            asyncio.create_task(self._run_scheduler())

    async def _run_scheduler(self):
        """一个简单的定时任务调度器"""
        self.logger.info("定时任务服务已启动。")
        for task in self.tasks:
            try:
                delay = task.get("delay_seconds", 60)
                message = task.get("message", "这是一个定时提醒！")
                to_wxid = task.get("to_wxid")

                if not to_wxid:
                    self.logger.warning(f"任务 '{message}'缺少 to_wxid，已跳过。")
                    continue

                # 启动一个独立的任务
                asyncio.create_task(
                    self._send_notification(delay, to_wxid, message))

            except Exception as e:
                self.logger.error(f"处理任务时出错: {e}")

    async def _send_notification(self, delay: int, to_wxid: str, message: str):
        """延迟发送通知"""
        self.logger.info(f"任务已计划: {delay}秒后向 {to_wxid} 发送 '{message}'")
        await asyncio.sleep(delay)
        try:
            await self.client.send_text_message(
                wxid=to_wxid,
                content=f"【定时提醒】\n{message}"
            )
            self.logger.info(f"成功向 {to_wxid} 发送提醒: '{message}'")
        except Exception as e:
            self.logger.error(f"发送提醒到 {to_wxid} 失败: {e}")
