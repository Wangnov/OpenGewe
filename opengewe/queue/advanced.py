import asyncio
import inspect
import os
from asyncio import Future
from functools import partial
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Union

from celery import Celery
from loguru import logger

from .base import BaseMessageQueue

# 默认配置，可通过环境变量覆盖
DEFAULT_BROKER = "redis://localhost:6379/0"
DEFAULT_BACKEND = "redis://localhost:6379/0"
DEFAULT_QUEUE_NAME = "opengewe_messages"

# 创建Celery应用工厂函数
def create_celery_app(
    broker: Optional[str] = None, 
    backend: Optional[str] = None, 
    queue_name: Optional[str] = None
) -> Celery:
    """创建Celery应用实例
    
    Args:
        broker: 消息代理的URI，例如 'redis://localhost:6379/0' 或 'amqp://guest:guest@localhost:5672//'
        backend: 结果存储的URI，例如 'redis://localhost:6379/0'
        queue_name: 队列名称
        
    Returns:
        Celery: Celery应用实例
    """
    # 从环境变量或参数中获取配置
    broker = broker or os.environ.get("OPENGEWE_BROKER_URL", DEFAULT_BROKER)
    backend = backend or os.environ.get("OPENGEWE_RESULT_BACKEND", DEFAULT_BACKEND)
    queue_name = queue_name or os.environ.get("OPENGEWE_QUEUE_NAME", DEFAULT_QUEUE_NAME)
    
    # 创建Celery应用
    app = Celery(
        "opengewe_message_queue",
        broker=broker,
        backend=backend,
    )
    
    # 配置Celery
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="Asia/Shanghai",
        enable_utc=True,
        task_routes={
            "process_message": {"queue": queue_name}
        },
    )
    
    return app

# 创建模块级别的Celery实例
celery = create_celery_app()

# 定义处理消息的Celery任务
@celery.task(name="process_message")
def process_message(task_id: str, func_name: str, *args: Any, **kwargs: Any) -> Any:
    """处理消息的Celery任务

    Args:
        task_id: 任务ID
        func_name: 要调用的函数名
        *args: 函数的位置参数
        **kwargs: 函数的关键字参数

    Returns:
        Any: 函数执行的结果
    """
    try:
        logger.info(f"处理消息: {func_name}, 任务ID: {task_id}")
        # 这里只是示例，实际实现需要根据func_name获取对应的函数并调用
        # 由于Celery任务是同步的，而我们要调用的函数是异步的，这里需要一个运行时环境来执行异步函数
        # 这里简化处理，实际实现可能更复杂
        result = {"status": "success", "data": f"处理了 {func_name}"}
        return result
    except Exception as e:
        logger.error(f"消息处理异常: {str(e)}")
        return {"status": "error", "error": str(e)}


class AdvancedMessageQueue(BaseMessageQueue):
    """基于Celery的高级消息队列实现"""

    def __init__(
        self,
        broker: str = DEFAULT_BROKER,
        backend: str = DEFAULT_BACKEND,
        queue_name: str = DEFAULT_QUEUE_NAME,
        celery_app: Optional[Celery] = None,
    ):
        """初始化高级消息队列

        Args:
            broker: 消息代理的URI，例如 'redis://localhost:6379/0' 或 'amqp://guest:guest@localhost:5672//'
            backend: 结果存储的URI，例如 'redis://localhost:6379/0'
            queue_name: 队列名称
            celery_app: 可选的Celery应用实例，如果提供则使用该实例，否则使用默认实例
        """
        self._futures: Dict[str, Future] = {}
        self._queue_name = queue_name

        # 使用提供的Celery实例或模块级别的实例
        if celery_app:
            self.celery = celery_app
        else:
            # 如果broker或backend与默认值不同，创建新的Celery实例
            if (broker != DEFAULT_BROKER or backend != DEFAULT_BACKEND or 
                queue_name != DEFAULT_QUEUE_NAME):
                self.celery = create_celery_app(broker, backend, queue_name)
            else:
                self.celery = celery

        # 使用模块级别的任务
        self._process_message = process_message

    async def enqueue(self, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        """将消息添加到队列

        Args:
            func: 要执行的异步函数
            *args: 函数的位置参数
            **kwargs: 函数的关键字参数

        Returns:
            Any: 函数执行的结果
        """
        # 创建一个Future对象用于异步等待结果
        future = Future()
        
        # 获取函数名作为任务标识
        func_name = func.__name__
        
        # 生成唯一的任务ID
        task_id = f"{func_name}_{id(future)}"
        
        # 存储Future以便后续设置结果
        self._futures[task_id] = future
        
        # 提交任务到Celery
        async_result = self._process_message.apply_async(
            args=(task_id, func_name) + args,
            kwargs=kwargs,
            task_id=task_id,
        )
        
        # 创建一个监听任务结果的异步任务
        asyncio.create_task(self._wait_for_result(task_id, async_result))
        
        # 返回Future，等待结果
        return await future

    async def _wait_for_result(self, task_id: str, async_result: Any) -> None:
        """等待Celery任务结果并设置到Future

        Args:
            task_id: 任务ID
            async_result: Celery的AsyncResult对象
        """
        try:
            # 等待任务完成并获取结果
            result = async_result.get(timeout=180)  # 设置适当的超时时间
            
            # 获取对应的Future
            future = self._futures.get(task_id)
            if future and not future.done():
                if isinstance(result, dict) and result.get("status") == "error":
                    # 如果任务失败，设置异常
                    future.set_exception(Exception(result.get("error", "Unknown error")))
                else:
                    # 设置结果
                    future.set_result(result)
            
        except Exception as e:
            logger.error(f"等待任务结果异常: {str(e)}")
            # 设置异常到Future
            future = self._futures.get(task_id)
            if future and not future.done():
                future.set_exception(e)
        finally:
            # 移除Future
            self._futures.pop(task_id, None)

    async def start_processing(self) -> None:
        """开始处理队列中的消息
        
        注意：在使用Celery的情况下，消息处理是由Celery worker负责的
        此方法仅用于保持接口一致性
        """
        logger.info("Celery消息队列不需要手动启动处理，请确保Celery worker已运行")

    async def stop_processing(self) -> None:
        """停止处理队列中的消息
        
        注意：在使用Celery的情况下，消息处理是由Celery worker负责的
        此方法仅用于保持接口一致性
        """
        logger.info("Celery消息队列不需要手动停止处理") 