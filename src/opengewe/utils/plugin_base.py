"""插件基类模块

提供插件基类，定义插件的生命周期方法和基本属性。
"""

from abc import ABC
from typing import Set
import sys
import inspect
from opengewe.utils.decorators import scheduler, add_job_safe, remove_job_safe
from opengewe.logger import get_logger

# 在日志系统加载前确保loguru已被拦截
try:
    from opengewe.logger.utils import intercept_plugin_loguru

    # 尝试拦截loguru
    intercept_plugin_loguru()
except ImportError:
    # 无法导入拦截函数，可能是循环导入
    pass

# 获取插件基类日志记录器
logger = get_logger("PluginBase")


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

        # 强制拦截插件导入的loguru，确保日志正确标记
        try:
            from loguru import logger as loguru_logger

            # 检查logger是否已被正确拦截
            if not hasattr(loguru_logger, "_original_logger"):
                # 如果没有，尝试再次拦截
                try:
                    from opengewe.logger.utils import intercept_plugin_loguru

                    intercept_plugin_loguru()
                except ImportError:
                    # 无法导入，可能是循环导入
                    pass
        except ImportError:
            # loguru可能未安装
            pass

        # 创建插件特有的日志记录器
        plugin_name = self.__class__.__name__

        # 设置模块的__plugin_name__变量，帮助日志系统识别插件
        module = sys.modules.get(self.__class__.__module__)
        if module:
            setattr(module, "__plugin_name__", plugin_name)

        # 创建插件专用logger
        self.logger = get_logger(f"Plugins.{plugin_name}")

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
            self.logger.debug(
                "已加载定时任务: {}",
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
            self.logger.debug("已卸载定时任务: {}", self._scheduled_jobs)
        self._scheduled_jobs.clear()

    async def async_init(self) -> None:
        """插件异步初始化

        此方法会在插件启用后被调用，用于执行需要异步的初始化操作。
        子类可以覆盖此方法以实现自定义的异步初始化逻辑。
        """
        pass
