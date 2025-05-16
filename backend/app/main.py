"""
主应用入口

初始化FastAPI应用程序，加载路由、中间件和事件处理程序。
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from opengewe.logger import get_logger
from backend.app.core.config import get_settings
from backend.app.core.middleware import setup_middlewares
from backend.app.core.device import get_device_id_dependency
from backend.app.db.init_db import init_all_db
from backend.app.gewe import client_manager
from backend.app.utils.logger_config import setup_logger

# 初始化日志
setup_logger()
logger = get_logger("App")

# 加载应用配置
settings = get_settings()


def create_application() -> FastAPI:
    """创建并配置FastAPI应用程序

    Returns:
        FastAPI: 配置好的应用实例
    """
    # 创建应用
    app = FastAPI(
        title="OpenGewe API",
        description="OpenGewe微信管理平台API",
        version="0.1.0",
        docs_url=settings.backend.docs_url if settings.backend.enable_docs else None,
        redoc_url="/redoc" if settings.backend.enable_docs else None,
    )

    # 设置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 设置自定义中间件
    setup_middlewares(app)

    # 注册路由
    from backend.app.api.routes import api_router

    app.include_router(api_router)

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

    # 设置启动和关闭事件
    @app.on_event("startup")
    async def startup_db():
        """应用启动时初始化数据库"""
        logger.info("初始化数据库...")
        await init_all_db()
        logger.success("数据库初始化完成")

    @app.on_event("startup")
    async def startup_gewe_client_manager():
        """应用启动时初始化GeweClient管理器"""
        logger.info("初始化GeweClient管理器...")
        await client_manager.start()
        logger.success("GeweClient管理器初始化完成")

    @app.on_event("shutdown")
    async def shutdown_db():
        """应用关闭时清理数据库资源"""
        from backend.app.db.session import DatabaseManager

        logger.info("关闭数据库连接...")
        db_manager = DatabaseManager()
        await db_manager.close()
        logger.success("数据库连接已关闭")

    @app.on_event("shutdown")
    async def shutdown_gewe_client_manager():
        """应用关闭时清理GeweClient资源"""
        logger.info("关闭GeweClient管理器...")
        await client_manager.stop()
        logger.success("GeweClient管理器已关闭")

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
