import asyncio
from asyncio import Future, Queue, sleep
from typing import Any, Awaitable, Callable, Dict

from loguru import logger

from .base import BaseMessageQueue, QueueError


class SimpleMessageQueue(BaseMessageQueue):
    """基于asyncio.Queue的简单消息队列实现"""

    def __init__(self, delay: float = 1.0):
        """初始化消息队列

        Args:
            delay: 消息处理间隔，单位为秒
        """
        self._queue = Queue()
        self._is_processing = False
        self._delay = delay
        self._processed_messages = 0

    @property
    def is_processing(self) -> bool:
        """返回当前是否正在处理消息

        Returns:
            bool: 如果处理器正在运行则返回True，否则返回False
        """
        return self._is_processing

    async def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态信息

        Returns:
            Dict[str, Any]: 包含队列当前状态的字典
        """
        return {
            "queue_size": self._queue.qsize(),
            "processing": self.is_processing,
            "worker_count": 1 if self.is_processing else 0,
            "processed_messages": self._processed_messages,
            "active_tasks": 1 if self.is_processing else 0,
            "scheduled_tasks": self._queue.qsize(),
            "reserved_tasks": 0,
            "pending_futures": 0,  # 简单队列中Future立即处理
            "queue_name": "simple_queue",
            "workers": ["main_worker"] if self.is_processing else [],
        }

    async def clear_queue(self) -> int:
        """清空当前队列中的所有待处理消息

        Returns:
            int: 被清除的消息数量

        Raises:
            QueueError: 清空队列失败时
        """
        try:
            cleared_count = 0
            
            # 清空队列中的所有任务
            while not self._queue.empty():
                try:
                    func, args, kwargs, future = self._queue.get_nowait()
                    # 取消相关的Future
                    if not future.done():
                        future.cancel()
                    cleared_count += 1
                except asyncio.QueueEmpty:
                    break
            
            logger.info(f"已清空简单队列，删除 {cleared_count} 个待处理任务")
            return cleared_count
            
        except Exception as e:
            error_msg = f"清空简单队列失败: {str(e)}"
            logger.error(error_msg)
            raise QueueError(error_msg) from e

    async def enqueue(self, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        """将消息添加到队列

        Args:
            func: 要执行的异步函数
            *args: 函数的位置参数
            **kwargs: 函数的关键字参数

        Returns:
            Any: 函数执行的结果
        """
        future = Future()
        await self._queue.put((func, args, kwargs, future))

        if not self._is_processing:
            asyncio.create_task(self.start_processing())

        return await future

    async def start_processing(self) -> None:
        """开始处理队列中的消息"""
        if self._is_processing:
            return

        self._is_processing = True
        logger.debug("开始处理消息队列")
        
        try:
            while True:
                if self._queue.empty():
                    self._is_processing = False
                    logger.debug("消息队列处理完毕")
                    break

                func, args, kwargs, future = await self._queue.get()
                try:
                    result = await func(*args, **kwargs)
                    future.set_result(result)
                    self._processed_messages += 1
                except Exception as e:
                    logger.error(f"消息处理异常: {str(e)}")
                    future.set_exception(e)
                finally:
                    self._queue.task_done()
                    await sleep(self._delay)  # 消息发送间隔
        except Exception as e:
            logger.error(f"消息队列处理异常: {str(e)}")
            self._is_processing = False

    async def stop_processing(self) -> None:
        """停止处理队列中的消息"""
        self._is_processing = False
        logger.debug("停止处理消息队列") 