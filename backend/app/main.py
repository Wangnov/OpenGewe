"""
主应用入口

初始化FastAPI应用程序，加载路由、中间件和事件处理程序。
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
import uuid
import psutil
from datetime import datetime
import importlib.metadata
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles

from opengewe.logger import get_logger
from backend.app.core.config import get_settings
from backend.app.core.middleware import setup_middlewares
from backend.app.core.device import get_device_id_dependency
from backend.app.db.init_db import init_all_db
from backend.app.gewe import client_manager
from backend.app.utils.logger_config import setup_logger
from backend.app.services.plugin_service import PluginService

# 尝试从package元数据获取版本号，如果失败则使用默认值
try:
    VERSION = importlib.metadata.version("opengewe")
except importlib.metadata.PackageNotFoundError:
    VERSION = "0.1.0"

# 初始化日志
setup_logger()
logger = get_logger("App")

# 加载应用配置
settings = get_settings()

# 设置应用版本
settings.app_version = os.getenv("APP_VERSION", VERSION)


# 请求ID中间件
class RequestIDMiddleware(BaseHTTPMiddleware):
    """为每个请求添加唯一ID，方便追踪和调试"""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        # 将请求ID添加到请求状态中
        request.state.request_id = request_id

        response = await call_next(request)
        # 添加到响应头
        response.headers["X-Request-ID"] = request_id
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理器

    管理应用的启动和关闭过程，初始化和清理资源。
    """
    # 启动逻辑 - 之前在 startup_db 中
    logger.info("初始化数据库...")
    await init_all_db()
    logger.success("数据库初始化完成")

    # 启动逻辑 - 之前在 startup_gewe_client_manager 中
    logger.info("初始化GeweClient管理器...")
    await client_manager.start()
    logger.success("GeweClient管理器初始化完成")

    # 启动逻辑 - 之前在 startup_plugins 中
    logger.info("正在加载启用的插件...")
    try:
        result = await PluginService.load_enabled_plugins()
        success, message, data = result

        if success:
            loaded_plugins = data.get("loaded", [])
            failed_plugins = data.get("failed", [])

            if loaded_plugins:
                logger.success(
                    f"成功加载 {len(loaded_plugins)} 个插件: {', '.join(loaded_plugins)}"
                )
            if failed_plugins:
                logger.warning(f"加载失败的插件: {', '.join(failed_plugins)}")
        else:
            logger.warning(f"插件加载失败: {message}")
    except Exception as e:
        logger.error(f"加载插件时出错: {e}")

    yield  # 应用运行期间

    # 关闭逻辑 - 之前在 shutdown_db 中
    from backend.app.db.session import DatabaseManager

    logger.info("关闭数据库连接...")
    db_manager = DatabaseManager()
    try:
        # 输出数据库连接状态
        health_info = await db_manager.check_health()
        logger.info(f"关闭前数据库状态: 活跃连接数={health_info['active_connections']}")

        # 关闭所有数据库连接
        await db_manager.close()
        logger.success("数据库连接已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接时出错: {e}")
        # 尝试强制关闭
        try:
            for device_id, engine in list(db_manager.engines.items()):
                await engine.dispose()
                logger.info(f"强制关闭设备 '{device_id}' 的数据库连接")
        except Exception as inner_e:
            logger.error(f"强制关闭数据库连接时出错: {inner_e}")

    # 关闭逻辑 - 之前在 shutdown_gewe_client_manager 中
    logger.info("关闭GeweClient管理器...")
    await client_manager.stop()
    logger.success("GeweClient管理器已关闭")


def create_application() -> FastAPI:
    """创建并配置FastAPI应用程序

    Returns:
        FastAPI: 配置好的应用实例
    """
    # 创建应用
    app = FastAPI(
        title="OpenGewe API",
        description="OpenGewe微信管理平台API，提供微信机器人管理、插件管理等功能。",
        version=settings.app_version,
        docs_url=settings.backend.docs_url if settings.backend.enable_docs else None,
        redoc_url="/redoc" if settings.backend.enable_docs else None,
        lifespan=lifespan,  # 使用新的生命周期管理器
        openapi_tags=[
            {"name": "webhook", "description": "微信回调接口"},
            {"name": "plugins", "description": "插件管理接口"},
            {"name": "files", "description": "文件管理接口"},
            {"name": "robots", "description": "机器人管理接口"},
            {"name": "system", "description": "系统管理接口"},
            {"name": "admin", "description": "管理员接口"},
            {"name": "device", "description": "设备管理接口"},
        ],
    )

    # 设置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 添加GZip压缩中间件
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # 添加请求ID中间件
    app.add_middleware(RequestIDMiddleware)

    # 添加可信主机中间件（如果配置了trusted_hosts）
    if hasattr(settings.backend, "trusted_hosts") and settings.backend.trusted_hosts:
        app.add_middleware(
            TrustedHostMiddleware, allowed_hosts=settings.backend.trusted_hosts
        )

    # 设置自定义中间件
    setup_middlewares(app)

    # 全局异常处理
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        """HTTP异常处理"""
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.status_code, "msg": exc.detail, "data": {}},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        """请求验证异常处理"""
        return JSONResponse(
            status_code=422,
            content={
                "code": 422,
                "msg": "请求参数验证失败",
                "data": {"errors": exc.errors()},
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """通用异常处理"""
        logger.error(f"未处理的异常: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"code": 500, "msg": "服务器内部错误", "data": {}},
        )

    # 创建并挂载静态文件目录
    try:
        # 创建上传目录（如果不存在）
        uploads_dir = os.path.join("static", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        # 挂载静态文件目录
        app.mount("/static", StaticFiles(directory="static"), name="static")
        logger.info("已挂载静态文件目录")
    except Exception as e:
        logger.warning(f"挂载静态文件目录失败: {e}")

    # 注册路由
    from backend.app.api.routes import api_router

    # 使用版本前缀
    app.include_router(api_router, prefix="/api/v1")

    # 单独注册webhook路由到根路径，使/webhook也能直接访问
    from backend.app.api.routes import webhook

    app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
    logger.info("已注册webhook根路径路由")

    # 添加设备信息路由
    @app.get("/device", tags=["device"])
    async def get_device_info(device_id: str = Depends(get_device_id_dependency)):
        """获取当前设备信息"""
        device = settings.get_device(device_id)
        return {
            "device_id": device_id,
            "name": device.name,
            "app_id": device.app_id,
        }

    # 增强的健康检查端点
    @app.get("/health", tags=["system"])
    async def health_check():
        """系统健康检查端点

        检查系统各组件状态和资源使用情况
        """
        # 检查数据库连接
        db_status = True
        db_error = None
        db_health_info = {}

        try:
            from backend.app.db.session import DatabaseManager

            # 使用数据库管理器的健康检查方法
            db_manager = DatabaseManager()
            db_health_info = await db_manager.check_health()
            db_status = db_health_info["status"] == "ok"
            if not db_status and db_health_info.get("errors"):
                db_error = "; ".join(db_health_info["errors"])
        except Exception as e:
            logger.error(f"数据库健康检查失败: {e}")
            db_status = False
            db_error = str(e)

        # 检查GeweClient状态
        gewe_status = client_manager.is_ready()

        # 检查系统资源
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        # 确定整体状态
        overall_status = "ok"
        if not db_status or not gewe_status:
            overall_status = "degraded"

        return {
            "status": overall_status,
            "version": settings.app_version,
            "timestamp": datetime.now().isoformat(),
            "components": {
                "database": "ok" if db_status else "error",
                "gewe_client": "ok" if gewe_status else "not_ready",
                "api": "ok",
            },
            "errors": {
                "database": db_error if not db_status else None,
            },
            "resources": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent,
            },
            "database": db_health_info,
        }

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host=settings.backend.host,
        port=settings.backend.port,
        reload=settings.backend.debug,
    )
