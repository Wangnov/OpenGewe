"""
Celery 应用实例定义

这个文件是Celery的中央入口点，用于定义和配置Celery应用。
所有任务和worker都应该从这里导入Celery实例，以确保使用的是同一个应用。
"""

from opengewe.logger import get_logger
from celery import Celery

logger = get_logger("CeleryApp")

# 默认配置
DEFAULT_BROKER = "redis://localhost:6379/0"
DEFAULT_BACKEND = "redis://localhost:6379/0"
DEFAULT_QUEUE_NAME = "opengewe_messages"


def create_celery_app(
    broker: str = DEFAULT_BROKER,
    backend: str = DEFAULT_BACKEND,
    queue_name: str = DEFAULT_QUEUE_NAME,
):
    """创建Celery应用实例"""
    app = Celery("opengewe_queue")
    app.conf.update(
        broker_url=broker,
        result_backend=backend,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        imports=("opengewe.queue.tasks",),
        task_routes={
            "opengewe.queue.tasks.*": {"queue": queue_name},
        },
    )
    return app


try:
    # 使用默认配置创建全局Celery应用实例
    celery_app = create_celery_app()
    logger.debug("全局Celery应用实例创建成功。")
except Exception as e:
    celery_app = None
    logger.error(f"创建全局Celery应用实例失败: {e}")
