"""
调度器管理器

简化的调度器管理，专注于核心功能
"""

from typing import Dict, Any, Optional
from loguru import logger

try:
    from opengewe.utils.decorators import scheduler
except ImportError:
    scheduler = None
    logger.warning("无法导入opengewe调度器，调度器管理功能将受限")


class SchedulerManager:
    """调度器管理器单例"""

    _instance: Optional["SchedulerManager"] = None
    _initialized: bool = False

    def __new__(cls) -> "SchedulerManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            SchedulerManager._initialized = True
            logger.debug("调度器管理器初始化完成")

    def ensure_scheduler_started(self) -> bool:
        """确保调度器已启动"""
        if scheduler is None:
            logger.error("调度器不可用，无法启动")
            return False

        try:
            if not scheduler.running:
                logger.info(f"启动定时任务调度器，时区: {scheduler.timezone}")
                scheduler.start()
                logger.info("定时任务调度器启动成功")
                return True
            else:
                logger.debug("定时任务调度器已在运行中")
                return True
        except Exception as e:
            logger.error(f"启动调度器失败: {e}", exc_info=True)
            return False

    def is_scheduler_running(self) -> bool:
        """检查调度器是否正在运行"""
        if scheduler is None:
            return False
        return scheduler.running

    def get_scheduler_status(self) -> Dict[str, Any]:
        """获取调度器状态信息"""
        if scheduler is None:
            return {"available": False, "running": False, "error": "调度器不可用"}

        try:
            all_jobs = scheduler.get_jobs()
            jobs_info = []

            for job in all_jobs:
                job_info = {
                    "id": job.id,
                    "next_run_time": job.next_run_time.isoformat()
                    if job.next_run_time
                    else None,
                    "trigger": str(job.trigger),
                    "func_name": f"{job.func.__module__}.{job.func.__qualname__}"
                    if hasattr(job.func, "__qualname__")
                    else str(job.func),
                }
                jobs_info.append(job_info)

            return {
                "available": True,
                "running": scheduler.running,
                "timezone": str(scheduler.timezone),
                "total_jobs": len(all_jobs),
                "jobs": jobs_info,
            }
        except Exception as e:
            return {"available": True, "running": False, "error": str(e)}

    def log_jobs_summary(self) -> None:
        """记录任务摘要"""
        if scheduler is None:
            logger.warning("调度器不可用，无法获取任务摘要")
            return

        try:
            jobs = scheduler.get_jobs()
            if not jobs:
                logger.debug("当前没有定时任务")
                return

            logger.info(f"定时任务摘要 (共{len(jobs)}个):")
            for job in jobs:
                next_run = (
                    job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
                    if job.next_run_time
                    else "未设置"
                )
                logger.info(f"  [{job.id}] 下次执行: {next_run}")
        except Exception as e:
            logger.error(f"获取任务摘要失败: {e}")


# 全局调度器管理器实例
scheduler_manager = SchedulerManager()
