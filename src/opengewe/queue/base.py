from abc import ABC, abstractmethod
from typing import Any, Callable, Awaitable, Tuple


class BaseMessageQueue(ABC):
    """消息队列的基本接口"""

    @abstractmethod
    async def enqueue(self, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        """将消息添加到队列

        Args:
            func: 要执行的异步函数
            *args: 函数的位置参数
            **kwargs: 函数的关键字参数

        Returns:
            Any: 函数执行的结果
        """
        pass

    @abstractmethod
    async def start_processing(self) -> None:
        """开始处理队列中的消息"""
        pass

    @abstractmethod
    async def stop_processing(self) -> None:
        """停止处理队列中的消息"""
        pass 