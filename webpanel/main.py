"""
OpenGewe WebPanel 主应用入口
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
import traceback

from app.core.config import get_settings
from app.core.database import db_manager, Base
from app.api import api_router
from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    
    启动时执行初始化操作，关闭时执行清理操作
    """
    settings = get_settings()
    
    # 启动时的初始化操作
    logger.info("========== OpenGewe WebPanel 启动中 ==========")
    logger.info(f"应用名称: {settings.app_name}")
    logger.info(f"版本: {settings.app_version}")
    logger.info(f"调试模式: {settings.debug}")
    
    try:
        # 初始化数据库表结构
        logger.info("初始化数据库表结构...")
        
        # 创建管理员数据库的表结构
        admin_engine = db_manager._engines["admin_data"]
        async with admin_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("数据库表结构初始化完成")
        
        # TODO: 创建默认管理员账户（如果不存在）
        # await create_default_admin()
        
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
    
    try:
        # 关闭数据库连接
        await db_manager.close_all()
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
        openapi_url="/openapi.json" if settings.debug else None
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
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """处理请求验证错误"""
        logger.warning(f"请求验证失败: {exc}")
        return JSONResponse(
            status_code=422,
            content={
                "error": "请求数据验证失败",
                "details": exc.errors()
            }
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        """处理数据库异常"""
        logger.error(f"数据库异常: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "error": "数据库操作失败",
                "details": "请联系管理员"
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """处理通用异常"""
        logger.error(f"未处理的异常: {exc}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "error": "服务器内部错误",
                "details": "请联系管理员"
            }
        )


def setup_health_check(app: FastAPI):
    """设置健康检查端点"""
    
    @app.get("/health", tags=["系统"])
    async def health_check():
        """健康检查端点"""
        try:
            # 检查数据库连接
            admin_engine = db_manager._engines.get("admin_data")
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
                "timestamp": "2024-01-01T00:00:00Z",  # 实际使用时应该使用当前时间
                "services": {
                    "database": db_status,
                    "redis": redis_status,
                    "bots": bot_status
                }
            }
            
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "error": str(e)
                }
            )
    
    @app.get("/", tags=["系统"])
    async def root():
        """根路径"""
        settings = get_settings()
        return {
            "message": f"欢迎使用 {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs" if settings.debug else "文档在生产环境中不可用"
        }


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    ) 