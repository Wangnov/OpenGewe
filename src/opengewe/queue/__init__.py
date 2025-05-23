"""
OpenGewe消息队列模块

提供不同类型的消息队列实现，用于异步处理微信消息和其他后台任务。
支持简单队列和高级队列（基于Celery）两种处理模式。
"""

from typing import Literal, Optional, Any

from celery import Celery

from .base import BaseMessageQueue, QueueError, WorkerNotFoundError
from .simple import SimpleMessageQueue
from .advanced import AdvancedMessageQueue, create_celery_app, celery
from opengewe.logger import get_logger

# 获取队列日志记录器
logger = get_logger("opengewe.queue")


def create_message_queue(
    queue_type: Literal["simple", "advanced"] = "simple",
    delay: float = 1.0,
    broker: str = "redis://localhost:6379/0",
    backend: str = "redis://localhost:6379/0",
    queue_name: str = "opengewe_messages",
    celery_app: Optional[Celery] = None,
    **extra_options: Any,
) -> BaseMessageQueue:
    """创建消息队列实例

    根据指定的队列类型创建相应的消息队列处理器。

    Args:
        queue_type: 队列类型，"simple" 或 "advanced"
        delay: 简单队列的消息处理间隔，单位为秒
        broker: 高级队列的消息代理URI
        backend: 高级队列的结果存储URI
        queue_name: 高级队列的队列名称
        celery_app: 可选的Celery应用实例
        **extra_options: 额外的队列选项

    Returns:
        BaseMessageQueue: 消息队列实例

    Raises:
        ValueError: 当指定了不支持的队列类型时
        QueueError: 创建队列实例失败时
    """
    try:
        if queue_type == "simple":
            logger.info(f"创建简单队列，处理延迟: {delay}秒")
            return SimpleMessageQueue(delay=delay, **extra_options)
        elif queue_type == "advanced":
            logger.info(f"创建高级队列，消息代理: {broker}, 队列名: {queue_name}")
            return AdvancedMessageQueue(
                broker=broker,
                backend=backend,
                queue_name=queue_name,
                celery_app=celery_app,
                **extra_options,
            )
        else:
            raise ValueError(f"不支持的队列类型: {queue_type}")
    except Exception as e:
        error_msg = f"创建消息队列失败: {str(e)}"
        logger.error(error_msg)
        raise QueueError(error_msg) from e


__all__ = [
    "BaseMessageQueue",
    "SimpleMessageQueue",
    "AdvancedMessageQueue",
    "create_message_queue",
    "create_celery_app",
    "celery",
    "QueueError",
    "WorkerNotFoundError",
]
