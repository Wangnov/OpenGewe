#!/usr/bin/env python
"""
Celery worker 启动脚本

用法:
    python -m opengewe.queue.celery_worker
    或者:
    celery -A opengewe.queue.advanced worker --loglevel=info --queues=opengewe_messages

环境变量:
    OPENGEWE_BROKER_URL: Celery broker URL，默认为 "redis://localhost:6379/0"
    OPENGEWE_RESULT_BACKEND: Celery result backend URL，默认为 "redis://localhost:6379/0"
    OPENGEWE_QUEUE_NAME: Celery 队列名称，默认为 "opengewe_messages"
    OPENGEWE_CONCURRENCY: Celery worker 并发数，默认为 4
    OPENGEWE_LOG_LEVEL: 日志级别，默认为 "info"
"""

import os
import sys
from .advanced import celery


def main():
    """启动Celery worker的主函数"""
    # 设置Celery参数
    concurrency = os.environ.get("OPENGEWE_CONCURRENCY", "4")
    log_level = os.environ.get("OPENGEWE_LOG_LEVEL", "info")
    queue_name = os.environ.get("OPENGEWE_QUEUE_NAME", "opengewe_messages")

    print("正在启动OpenGewe Celery Worker...")
    print(f"队列名称: {queue_name}")
    print(f"并发数: {concurrency}")
    print(f"日志级别: {log_level}")
    print(f"Broker: {celery.conf.broker_url}")
    print(f"Backend: {celery.conf.result_backend}")

    # 准备Celery命令行参数
    argv = [
        "worker",
        f"--concurrency={concurrency}",
        f"--loglevel={log_level}",
        f"--queues={queue_name}",
        "--pool=solo" if sys.platform == "win32" else "--pool=prefork",  # Windows兼容性
    ]

    # 启动Celery worker
    try:
        celery.worker_main(argv)
    except KeyboardInterrupt:
        print("\n正在关闭Celery worker...")
    except Exception as e:
        print(f"启动Celery worker时出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
