import asyncio
from asyncio import Future, Queue, sleep
from typing import Any, Awaitable, Callable, Tuple

from loguru import logger

from .base import BaseMessageQueue


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