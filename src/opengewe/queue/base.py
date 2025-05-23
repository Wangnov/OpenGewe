from abc import ABC, abstractmethod
from typing import Any, Callable, Awaitable, TypeVar, Dict

# 定义泛型类型
T = TypeVar("T")


class QueueError(Exception):
    """队列操作异常"""

    pass


class WorkerNotFoundError(QueueError):
    """没有可用的Celery worker异常"""

    pass


class BaseMessageQueue(ABC):
    """消息队列的基本接口

    所有消息队列实现必须继承此基类，实现消息入队和处理功能。
    """

    @abstractmethod
    async def enqueue(
        self, func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any
    ) -> T:
        """将消息添加到队列并等待处理结果

        Args:
            func: 要执行的异步函数
            *args: 函数的位置参数
            **kwargs: 函数的关键字参数

        Returns:
            T: 函数执行的结果

        Raises:
            QueueError: 队列操作失败
        """
        pass

    @abstractmethod
    async def start_processing(self) -> None:
        """开始处理队列中的消息

        初始化消息处理器并开始监听队列

        Raises:
            QueueError: 启动处理器失败时
        """
        pass

    @abstractmethod
    async def stop_processing(self) -> None:
        """停止处理队列中的消息

        关闭消息处理器并释放相关资源

        Raises:
            QueueError: 停止处理器失败时
        """
        pass

    @property
    @abstractmethod
    def is_processing(self) -> bool:
        """返回当前是否正在处理消息

        Returns:
            bool: 如果处理器正在运行则返回True，否则返回False
        """
        pass

    @abstractmethod
    async def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态信息

        Returns:
            Dict[str, Any]: 包含队列当前状态的字典，至少应包含：
                - queue_size: 当前队列中的消息数量
                - processing: 是否正在处理消息
                - worker_count: 工作线程/进程数量
                - processed_messages: 已处理的消息总数
        """
        pass

    @abstractmethod
    async def clear_queue(self) -> int:
        """清空当前队列中的所有待处理消息

        Returns:
            int: 被清除的消息数量

        Raises:
            QueueError: 清空队列失败时
        """
        pass
