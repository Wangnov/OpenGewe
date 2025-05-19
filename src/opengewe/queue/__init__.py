from typing import Literal, Optional, Union

from celery import Celery

from .base import BaseMessageQueue
from .simple import SimpleMessageQueue
from .advanced import AdvancedMessageQueue, create_celery_app, celery


def create_message_queue(
    queue_type: Literal["simple", "advanced"] = "advanced",
    delay: float = 1.0,
    broker: str = "redis://localhost:6379/0",
    backend: str = "redis://localhost:6379/0",
    queue_name: str = "opengewe_messages",
    celery_app: Optional[Celery] = None,
) -> BaseMessageQueue:
    """创建消息队列实例

    Args:
        queue_type: 队列类型，"simple" 或 "advanced"
        delay: 简单队列的消息处理间隔，单位为秒
        broker: 高级队列的消息代理URI
        backend: 高级队列的结果存储URI
        queue_name: 高级队列的队列名称
        celery_app: 可选的Celery应用实例

    Returns:
        BaseMessageQueue: 消息队列实例
    """
    if queue_type == "simple":
        return SimpleMessageQueue(delay=delay)
    elif queue_type == "advanced":
        return AdvancedMessageQueue(
            broker=broker,
            backend=backend,
            queue_name=queue_name,
            celery_app=celery_app,
        )
    else:
        raise ValueError(f"不支持的队列类型: {queue_type}")


__all__ = [
    "BaseMessageQueue", 
    "SimpleMessageQueue", 
    "AdvancedMessageQueue", 
    "create_message_queue",
    "create_celery_app",
    "celery",
] 