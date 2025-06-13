import asyncio
import json
import os
import shlex
import uuid
from datetime import datetime, timedelta

from opengewe.utils.plugin_base import PluginBase
from opengewe.utils.decorators import on_text_message, scheduler, add_job_safe, remove_job_safe
from opengewe.callback.models.text import TextMessage
from opengewe.client import GeweClient

class ScheduledTaskNotifier(PluginBase):
    """动态定时任务提醒"""
    name = "动态定时任务提醒"
    description = "通过聊天指令动态添加、管理定时或轮询任务，并使用持久化存储确保任务不丢失。"
    author = "Roo"
    version = "0.2.3"

    def __init__(self, config):
        super().__init__(config)
        self.client: GeweClient = None
        self.tasks_file = os.path.join(os.path.dirname(__file__), "tasks.json")
        self.tasks = {}  # {job_id: task_info}
        self.command_prefix = self.config.get("command_prefix", "提醒")

    async def on_enable(self, client: GeweClient):
        """插件启用时，启动调度器并加载任务"""
        self.client = client
        if not scheduler.running:
            scheduler.start()
            self.logger.info("APScheduler 已启动。")
        
        await self._load_tasks()
        self.logger.info(f"定时任务插件已启用，加载了 {len(self.tasks)} 个任务。")

    async def on_disable(self):
        """插件禁用时，保存任务"""
        await self._save_tasks()
        self.logger.info("定时任务插件已禁用。")

    async def _load_tasks(self):
        """从文件加载并重新调度任务"""
        if not os.path.exists(self.tasks_file):
            self.tasks = {}
            return

        try:
            with open(self.tasks_file, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"加载任务文件失败: {e}")
            self.tasks = {}
            return

        now = datetime.now(scheduler.timezone)
        ids_to_remove = []
        for job_id, task in self.tasks.items():
            trigger = task.get("trigger")
            trigger_args = task.get("trigger_args", {})
            
            if trigger == "date":
                run_date = datetime.fromisoformat(trigger_args.get("run_date"))
                if run_date <= now:
                    self.logger.info(f"任务 {job_id} 已过期，自动移除。")
                    ids_to_remove.append(job_id)
                    continue
            
            add_job_safe(
                scheduler,
                job_id=job_id,
                func=self._execute_task,
                client=self.client,
                trigger=trigger,
                args=(self.client, job_id),
                **trigger_args
            )
        
        if ids_to_remove:
            for job_id in ids_to_remove:
                del self.tasks[job_id]
            await self._save_tasks()

    async def _save_tasks(self):
        """将任务状态保存到文件"""
        try:
            with open(self.tasks_file, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=4, ensure_ascii=False)
        except IOError as e:
            self.logger.error(f"保存任务文件失败: {e}")

    async def _execute_task(self, client: GeweClient, job_id: str):
        """执行具体的发送任务"""
        task = self.tasks.get(job_id)
        if not task:
            self.logger.warning(f"任务 {job_id} 未找到，可能已被移除。")
            remove_job_safe(scheduler, job_id)
            return

        try:
            await client.send_text_message(
                wxid=task["to_wxid"],
                content=f"【{task['task_type']}】\n{task['message']}"
            )
            self.logger.info(f"成功执行任务 {job_id}: {task['message']}")
        except Exception as e:
            self.logger.error(f"执行任务 {job_id} 失败: {e}")

        if task.get("trigger") == "date":
            if job_id in self.tasks:
                del self.tasks[job_id]
                await self._save_tasks()
                self.logger.info(f"一次性任务 {job_id} 已完成并移除。")

    @on_text_message
    async def handle_commands(self, client: GeweClient, message: TextMessage):
        """处理用户指令"""
        parts = message.content.strip().split(maxsplit=1)
        if not parts or parts[0] != self.command_prefix:
            return

        if len(parts) == 1:
            await client.send_text_message(message.from_wxid, self._get_help_text())
            return

        try:
            args = shlex.split(parts[1])
            command = args[0]
            
            if command in ["定时", "添加定时"]:
                await self._handle_add_date_task(message, args[1:])
            elif command in ["轮询", "添加轮询"]:
                await self._handle_add_interval_task(message, args[1:])
            elif command in ["查看", "列表"]:
                await self._handle_list_tasks(message)
            elif command in ["删除", "取消"]:
                await self._handle_delete_task(message, args[1:])
            else:
                await client.send_text_message(message.from_wxid, self._get_help_text())

        except Exception as e:
            self.logger.error(f"处理指令失败: {e}", exc_info=True)
            await client.send_text_message(message.from_wxid, f"指令处理失败: {e}")

    def _get_help_text(self):
        return f"""--- 定时提醒插件帮助 ---
指令格式: {self.command_prefix} [命令] [参数]

1. 添加定时任务:
   {self.command_prefix} 定时 "YYYY-MM-DD HH:MM:SS" "提醒内容"
   示例: {self.command_prefix} 定时 "2025-12-31 23:59:59" "新年快乐！"

2. 添加轮询任务:
   {self.command_prefix} 轮询 [秒数] "提醒内容"
   示例: {self.command_prefix} 轮询 3600 "该喝水了！"

3. 查看所有任务:
   {self.command_prefix} 查看

4. 删除任务:
   {self.command_prefix} 删除 [任务ID]
   (任务ID可通过“查看”指令获取)
"""

    async def _handle_add_date_task(self, message: TextMessage, args: list):
        if len(args) != 2:
            await self.client.send_text_message(message.from_wxid, "格式错误！\n正确格式: 定时 \"YYYY-MM-DD HH:MM:SS\" \"提醒内容\"")
            return
        
        try:
            run_date_str = args[0]
            # 解析为 naive datetime
            naive_run_date = datetime.strptime(run_date_str, "%Y-%m-%d %H:%M:%S")
            # 直接赋予调度器的时区信息
            run_date = naive_run_date.replace(tzinfo=scheduler.timezone)
            content = args[1]
            
            if run_date <= datetime.now(scheduler.timezone):
                await self.client.send_text_message(message.from_wxid, "错误：不能设置一个过去的时间点。")
                return

            job_id = str(uuid.uuid4())
            task_info = {
                "job_id": job_id,
                "task_type": "定时提醒",
                "creator": message.sender_wxid,
                "to_wxid": message.from_wxid,
                "message": content,
                "trigger": "date",
                "trigger_args": {"run_date": run_date.isoformat()}
            }
            
            add_job_safe(scheduler, job_id, self._execute_task, self.client, "date", args=(self.client, job_id), run_date=run_date)
            self.tasks[job_id] = task_info
            await self._save_tasks()

            await self.client.send_text_message(message.from_wxid, f"定时任务已添加！\nID: {job_id}\n时间: {run_date.strftime('%Y-%m-%d %H:%M:%S %Z')}\n内容: {content}")

        except ValueError:
            await self.client.send_text_message(message.from_wxid, "时间格式错误！请使用 'YYYY-MM-DD HH:MM:SS' 格式。")
        except Exception as e:
            await self.client.send_text_message(message.from_wxid, f"添加任务失败: {e}")

    async def _handle_add_interval_task(self, message: TextMessage, args: list):
        if len(args) != 2:
            await self.client.send_text_message(message.from_wxid, "格式错误！\n正确格式: 轮询 [秒数] \"提醒内容\"")
            return

        try:
            interval_seconds = int(args[0])
            content = args[1]

            if interval_seconds <= 0:
                await self.client.send_text_message(message.from_wxid, "错误：间隔秒数必须大于0。")
                return

            job_id = str(uuid.uuid4())
            task_info = {
                "job_id": job_id,
                "task_type": "轮询提醒",
                "creator": message.sender_wxid,
                "to_wxid": message.from_wxid,
                "message": content,
                "trigger": "interval",
                "trigger_args": {"seconds": interval_seconds}
            }

            add_job_safe(scheduler, job_id, self._execute_task, self.client, "interval", args=(self.client, job_id), seconds=interval_seconds)
            self.tasks[job_id] = task_info
            await self._save_tasks()

            await self.client.send_text_message(message.from_wxid, f"轮询任务已添加！\nID: {job_id}\n间隔: {interval_seconds}秒\n内容: {content}")

        except ValueError:
            await self.client.send_text_message(message.from_wxid, "间隔秒数必须是纯数字。")
        except Exception as e:
            await self.client.send_text_message(message.from_wxid, f"添加任务失败: {e}")

    async def _handle_list_tasks(self, message: TextMessage):
        if not self.tasks:
            await self.client.send_text_message(message.from_wxid, "当前没有已安排的任务。")
            return

        reply = "--- 当前任务列表 ---\n"
        for job_id, task in self.tasks.items():
            reply += f"\nID: {job_id}\n"
            reply += f"类型: {task['task_type']}\n"
            reply += f"内容: {task['message']}\n"
            if task['trigger'] == 'date':
                run_date = datetime.fromisoformat(task['trigger_args']['run_date'])
                reply += f"执行时间: {run_date.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            elif task['trigger'] == 'interval':
                seconds = task['trigger_args']['seconds']
                reply += f"执行间隔: {seconds}秒\n"
        
        await self.client.send_text_message(message.from_wxid, reply.strip())

    async def _handle_delete_task(self, message: TextMessage, args: list):
        if len(args) != 1:
            await self.client.send_text_message(message.from_wxid, "格式错误！\n正确格式: 删除 [任务ID]")
            return
        
        job_id_to_delete = args[0]
        if job_id_to_delete not in self.tasks:
            await self.client.send_text_message(message.from_wxid, f"错误：未找到ID为 {job_id_to_delete} 的任务。")
            return
            
        # 权限检查：只有创建者可以删除
        # if self.tasks[job_id_to_delete]['creator'] != message.sender_wxid:
        #     await self.client.send_text_message(message.from_wxid, "错误：您没有权限删除此任务。")
        #     return

        remove_job_safe(scheduler, job_id_to_delete)
        del self.tasks[job_id_to_delete]
        await self._save_tasks()

        await self.client.send_text_message(message.from_wxid, f"任务 {job_id_to_delete} 已成功删除。")
