"""插件基类模块

提供插件基类，定义插件的生命周期方法和基本属性。
"""

from abc import ABC
from typing import Set
import logging
from opengewe.utils.decorators import scheduler, add_job_safe, remove_job_safe


class PluginBase(ABC):
    """插件基类

    所有插件都应该继承此类。插件会在启用时自动注册事件处理器和定时任务。

    示例:

    ```python
    class MyPlugin(PluginBase):
        description = "我的插件描述"
        author = "插件作者"
        version = "1.0.0"

        @on_text_message
        async def handle_text(self, client, message):
            # 处理文本消息
            pass

        @schedule("interval", seconds=60)
        async def periodic_task(self, client):
            # 每分钟执行一次
            pass
    ```
    """

    # 插件元数据（子类应该重写这些属性）
    description: str = "暂无描述"
    author: str = "未知"
    version: str = "1.0.0"

    def __init__(self):
        """初始化插件实例"""
        self.enabled: bool = False
        self._scheduled_jobs: Set[str] = set()

    async def on_enable(self, client=None) -> None:
        """插件启用时调用

        此方法会在插件启用时被调用，用于注册定时任务和执行初始化操作。

        Args:
            client: GeweClient实例
        """
        self.enabled = True

        # 注册定时任务
        for method_name in dir(self):
            method = getattr(self, method_name)
            if hasattr(method, "_is_scheduled"):
                job_id = getattr(method, "_job_id")
                trigger = getattr(method, "_schedule_trigger")
                trigger_args = getattr(method, "_schedule_args")

                add_job_safe(scheduler, job_id, method, client, trigger, **trigger_args)
                self._scheduled_jobs.add(job_id)

        if self._scheduled_jobs:
            logging.info(
                "插件 {} 已加载定时任务: {}",
                self.__class__.__name__,
                self._scheduled_jobs,
            )

    async def on_disable(self) -> None:
        """插件禁用时调用

        此方法会在插件禁用时被调用，用于清理资源和取消定时任务。
        """
        self.enabled = False

        # 移除定时任务
        for job_id in self._scheduled_jobs:
            remove_job_safe(scheduler, job_id)
        if self._scheduled_jobs:
            logging.info("已卸载定时任务: {}", self._scheduled_jobs)
        self._scheduled_jobs.clear()

    async def async_init(self) -> None:
        """插件异步初始化

        此方法会在插件启用后被调用，用于执行需要异步的初始化操作。
        子类可以覆盖此方法以实现自定义的异步初始化逻辑。
        """
        pass
