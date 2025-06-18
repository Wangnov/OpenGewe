"""
OpenGewe WebPanel 主应用入口
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import traceback
from datetime import datetime, timezone

import subprocess
import sys
import os
import signal
from app.core.config import get_settings
from app.core.session_manager import session_manager
from app.api import api_router
from sqlalchemy import text
from opengewe.logger import init_default_logger, get_logger

# 获取正确的配置文件路径（相对于backend目录的上级目录）
config_file_path = os.path.join(
    os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "main_config.toml"
)
init_default_logger(config_file=config_file_path)
logger = get_logger(__name__)

celery_worker_process = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    启动时执行初始化操作，关闭时执行清理操作
    """
    global celery_worker_process
    settings = get_settings()

    # 启动时的初始化操作
    logger.info("========== OpenGewe WebPanel 启动中 ==========")
    logger.info(f"应用名称: {settings.app_name}")
    logger.info(f"版本: {settings.app_version}")
    logger.info(f"调试模式: {settings.debug}")

    try:
        # 确保数据库存在
        logger.info("检查并创建数据库...")
        await settings.ensure_database_ready()

        # 初始化数据库表结构
        logger.info("初始化数据库表结构...")

        # 初始化session管理器
        await session_manager.initialize()

        # 创建管理员数据库的表结构
        from app.core.bases import AdminBase

        admin_engine = session_manager._engines["admin_data"]
        async with admin_engine.begin() as conn:
            await conn.run_sync(AdminBase.metadata.create_all)

        logger.info("数据库表结构初始化完成")

        # 初始化配置系统（将TOML配置迁移到数据库）
        try:
            from app.services.initializers.config_initializer import config_initializer
            from app.services.config_manager import config_manager

            logger.info("初始化配置系统...")
            config_init_success = await config_initializer.initialize_config()

            if config_init_success:
                logger.info("配置系统初始化完成")
            else:
                logger.warning("配置系统初始化部分失败，将使用文件配置作为回退")

            # 检查是否需要启动Celery worker
            queue_config = await config_manager.get_config("queue")
            if queue_config and queue_config.get("queue_type") == "advanced":
                logger.info("检测到高级队列配置，尝试启动Celery worker...")
                try:
                    # 使用subprocess在后台启动worker
                    # 注意：这里的python路径可能需要根据实际环境调整
                    python_executable = sys.executable
                    command = [
                        python_executable,
                        "-m",
                        "opengewe.queue.celery_worker",
                        "--type",
                        "redis",  # 或者从配置中读取
                    ]
                    # 使用preexec_fn=os.setsid在新的进程会话中启动Celery
                    # 这样可以确保在主进程退出时，能够终止整个进程组
                    celery_worker_process = subprocess.Popen(
                        command,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        preexec_fn=os.setsid,
                    )
                    logger.info(
                        f"Celery worker已在新的进程组中启动，PGID: {os.getpgid(celery_worker_process.pid)}"
                    )
                except Exception as e:
                    logger.error(f"启动Celery worker失败: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"配置系统初始化失败: {e}", exc_info=True)
            logger.warning("将继续使用文件配置系统")

        # 初始化机器人配置（从配置文件）
        try:
            from app.services.initializers.bot_initializer import (
                initialize_bots_from_config,
            )

            await initialize_bots_from_config()
        except Exception as e:
            logger.error(f"机器人配置初始化失败: {e}", exc_info=True)
            # 机器人初始化失败不影响应用启动

        # 初始化插件配置
        try:
            from app.services.initializers.plugin_initializer import initialize_plugins

            await initialize_plugins()
        except Exception as e:
            logger.error(f"插件配置初始化失败: {e}", exc_info=True)
            # 插件初始化失败不影响应用启动

        # 确保调度器启动
        try:
            from app.utils.scheduler_manager import scheduler_manager

            if not scheduler_manager.is_scheduler_running():
                logger.info("启动定时任务调度器...")
                scheduler_manager.ensure_scheduler_started()
        except Exception as e:
            logger.error(f"调度器启动失败: {e}", exc_info=True)

        # 预加载所有bot客户端（重要：确保插件和定时任务立即生效）
        try:
            from app.services.bot_preloader import bot_preloader

            logger.info("开始预加载bot客户端...")
            preload_result = await bot_preloader.preload_all_bots()

            if preload_result["status"] == "completed":
                logger.info(
                    f"Bot预加载完成：成功 {preload_result['loaded_count']}/{preload_result['total_bots']} 个"
                )

                # 记录调度器任务摘要
                scheduler_manager.log_jobs_summary()
            elif preload_result["status"] == "no_bots":
                logger.info("没有配置的bot需要预加载")
            else:
                logger.warning(f"Bot预加载结果: {preload_result}")

        except Exception as e:
            logger.error(f"Bot预加载失败: {e}", exc_info=True)
            # 预加载失败不影响应用启动，但会影响定时任务的即时生效

        # 初始化管理员账号
        try:
            from app.services.initializers import initialize_admin

            logger.info("初始化管理员账号...")
            await initialize_admin()
        except Exception as e:
            logger.error(f"管理员账号初始化失败: {e}", exc_info=True)
            # 管理员初始化失败不影响应用启动

        # TODO: 初始化Redis连接
        # await init_redis_connection()

        # TODO: 启动后台任务队列
        # await start_background_tasks()

        logger.info("========== OpenGewe WebPanel 启动完成 ==========")

    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        logger.error(traceback.format_exc())
        raise

    # yield 控制权回到应用
    yield

    # 关闭时的清理操作
    logger.info("========== OpenGewe WebPanel 关闭中 ==========")

    # 停止Celery worker子进程组
    if celery_worker_process:
        pgid = os.getpgid(celery_worker_process.pid)
        logger.info(f"正在停止Celery worker进程组 (PGID: {pgid})...")
        try:
            os.killpg(pgid, signal.SIGTERM)
            celery_worker_process.wait(timeout=5)
            logger.info("Celery worker进程组已成功终止")
        except ProcessLookupError:
            logger.warning(f"Celery worker进程组 (PGID: {pgid}) 已不存在，可能已手动关闭")
        except subprocess.TimeoutExpired:
            logger.warning(f"Celery worker进程组 (PGID: {pgid}) 终止超时，强制终止")
            os.killpg(pgid, signal.SIGKILL)
        except Exception as e:
            logger.error(f"停止Celery worker进程组时出错: {e}", exc_info=True)

    try:
        # 关闭数据库连接
        await session_manager.close_all()
        logger.info("数据库连接已关闭")

        # TODO: 关闭Redis连接
        # await close_redis_connection()

        # TODO: 停止后台任务
        # await stop_background_tasks()

        # TODO: 清理GeweClient实例
        # await bot_client_manager.close_all()

        logger.info("========== OpenGewe WebPanel 关闭完成 ==========")

    except Exception as e:
        logger.error(f"应用关闭时出错: {e}")
        logger.error(traceback.format_exc())


# 创建FastAPI应用实例
def create_app() -> FastAPI:
    """创建并配置FastAPI应用"""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="OpenGewe 多微信机器人管理后台",
        lifespan=lifespan,  # 使用最新的lifespan参数
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
    )

    # 配置CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册API路由
    app.include_router(api_router)

    # 添加全局异常处理器
    setup_exception_handlers(app)

    # 添加健康检查端点
    setup_health_check(app)

    return app


def setup_exception_handlers(app: FastAPI):
    """设置全局异常处理器"""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """处理请求验证错误"""
        logger.warning(f"请求验证失败: {exc}")

        # 清理错误信息，移除不能被JSON序列化的对象
        errors = exc.errors()
        for error in errors:
            if 'ctx' in error and 'error' in error['ctx']:
                # 将 ValueError 对象转换为字符串
                if isinstance(error['ctx']['error'], Exception):
                    error['ctx']['error'] = str(error['ctx']['error'])

        return JSONResponse(
            status_code=422,
            content={"error": "请求数据验证失败", "details": errors},
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """处理数据库异常"""
        logger.error(f"数据库异常: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": "数据库操作失败", "details": "请联系管理员"},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """处理通用异常"""
        logger.error(f"未处理的异常: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": "服务器内部错误", "details": "请联系管理员"},
        )


def setup_health_check(app: FastAPI):
    """设置健康检查端点"""

    @app.get("/health", tags=["系统"])
    async def health_check():
        """健康检查端点"""
        try:
            # 检查数据库连接
            admin_engine = session_manager._engines.get("admin_data")
            if admin_engine:
                async with admin_engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                db_status = "healthy"
            else:
                db_status = "unavailable"

            # TODO: 检查Redis连接
            redis_status = "unknown"

            # TODO: 检查机器人连接状态
            bot_status = "unknown"

            return {
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "services": {
                    "database": db_status,
                    "redis": redis_status,
                    "bots": bot_status,
                },
            }

        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return JSONResponse(
                status_code=503, content={"status": "unhealthy", "error": str(e)}
            )

    @app.get("/", tags=["系统"])
    async def root():
        """根路径"""
        settings = get_settings()
        return {
            "message": f"欢迎使用 {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs" if settings.debug else "文档在生产环境中不可用",
        }


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info",
    )
