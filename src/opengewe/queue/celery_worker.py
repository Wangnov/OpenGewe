#!/usr/bin/env python
"""
Celery worker 启动脚本

用法:
    python -m opengewe.queue.celery_worker
    
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

if __name__ == "__main__":
    # 设置Celery参数
    concurrency = os.environ.get("OPENGEWE_CONCURRENCY", "4")
    log_level = os.environ.get("OPENGEWE_LOG_LEVEL", "info")
    
    # 准备Celery命令行参数
    argv = [
        "worker",
        f"--concurrency={concurrency}",
        f"--loglevel={log_level}",
    ]
    
    # 启动Celery worker
    celery.worker_main(argv) 