"""
OpenGewe消息队列模块

提供不同类型的消息队列实现，用于异步处理微信消息和其他后台任务。
支持简单队列和高级队列（基于Celery）两种处理模式。
"""

from typing import Literal, Optional, Any

from .base import BaseMessageQueue, QueueError, WorkerNotFoundError
from .simple import SimpleMessageQueue
from opengewe.logger import init_default_logger, get_logger

init_default_logger()
# 获取队列日志记录器
logger = get_logger("opengewe.queue")

# 尝试导入高级队列相关功能
try:
    from .advanced import AdvancedMessageQueue
    from .app import create_celery_app, celery_app as celery
    from celery import Celery

    ADVANCED_AVAILABLE = True
    logger.debug("高级消息队列功能可用")
except ImportError as e:
    logger.debug(f"高级消息队列功能不可用: {e}")
    # 创建占位符类和函数
    AdvancedMessageQueue = None
    create_celery_app = None
    celery = None
    Celery = None
    ADVANCED_AVAILABLE = False


def create_message_queue(
    queue_type: Literal["simple", "advanced"] = "simple",
    delay: float = 1.0,
    broker: str = "redis://localhost:6379/0",
    backend: str = "redis://localhost:6379/0",
    queue_name: str = "opengewe_messages",
    celery_app: Optional[Any] = None,
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
        ImportError: 当advanced模式不可用但被请求时
    """
    try:
        if queue_type == "simple":
            logger.info(f"创建简单队列，处理延迟: {delay}秒")
            return SimpleMessageQueue(delay=delay, **extra_options)
        elif queue_type == "advanced":
            if not ADVANCED_AVAILABLE:
                error_msg = (
                    "高级消息队列功能不可用！\n"
                    "请安装所需依赖: pip install opengewe[advanced]\n"
                    "或者安装单个包: pip install celery redis amqp joblib lz4\n"
                    "如果不需要高级功能，请使用 queue_type='simple'"
                )
                logger.error(error_msg)
                raise ImportError(error_msg)

            logger.info(f"创建高级队列，消息代理: {broker}, 队列名: {queue_name}")
            return AdvancedMessageQueue(
                broker=broker,
                backend=backend,
                queue_name=queue_name,
                **extra_options,
            )
        else:
            raise ValueError(f"不支持的队列类型: {queue_type}")
    except Exception as e:
        error_msg = f"创建消息队列失败: {str(e)}"
        logger.error(error_msg)
        if isinstance(e, ImportError):
            raise e  # 重新抛出ImportError，保持原始错误信息
        raise QueueError(error_msg) from e


# 动态构建__all__列表
__all__ = [
    "BaseMessageQueue",
    "SimpleMessageQueue",
    "create_message_queue",
    "QueueError",
    "WorkerNotFoundError",
]

# 只有在高级功能可用时才导出相关符号
if ADVANCED_AVAILABLE:
    __all__.extend(
        [
            "AdvancedMessageQueue",
            "create_celery_app",
            "celery_app",
        ]
    )
