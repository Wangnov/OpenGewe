"""
异常处理模块
用于定义自定义异常类型和全局异常处理
"""

from typing import Any, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException


class BaseOpenGeweException(Exception):
    """OpenGewe应用程序的基础异常类"""
    def __init__(
        self,
        status_code: int,
        message: str,
        detail: Optional[Any] = None,
        error_code: Optional[str] = None
    ):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        self.error_code = error_code
        super().__init__(message)


class DatabaseException(BaseOpenGeweException):
    """数据库相关异常"""
    def __init__(
        self,
        message: str = "数据库操作异常",
        detail: Optional[Any] = None,
        error_code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            detail=detail,
            error_code=error_code or "DATABASE_ERROR"
        )


class ConfigException(BaseOpenGeweException):
    """配置相关异常"""
    def __init__(
        self,
        message: str = "配置错误",
        detail: Optional[Any] = None,
        error_code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            detail=detail,
            error_code=error_code or "CONFIG_ERROR"
        )


class PluginException(BaseOpenGeweException):
    """插件相关异常"""
    def __init__(
        self,
        message: str = "插件错误",
        detail: Optional[Any] = None,
        error_code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            detail=detail,
            error_code=error_code or "PLUGIN_ERROR"
        )


class GeweClientException(BaseOpenGeweException):
    """GeweClient相关异常"""
    def __init__(
        self,
        message: str = "GeweClient错误",
        detail: Optional[Any] = None,
        error_code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            detail=detail,
            error_code=error_code or "GEWE_CLIENT_ERROR"
        )


class NotFoundError(BaseOpenGeweException):
    """资源未找到异常"""
    def __init__(
        self,
        message: str = "资源未找到",
        detail: Optional[Any] = None,
        error_code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            detail=detail,
            error_code=error_code or "NOT_FOUND"
        )


class PermissionDenied(BaseOpenGeweException):
    """权限拒绝异常"""
    def __init__(
        self,
        message: str = "权限拒绝",
        detail: Optional[Any] = None,
        error_code: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            detail=detail,
            error_code=error_code or "PERMISSION_DENIED"
        )


def register_exception_handlers(app: FastAPI) -> None:
    """
    注册全局异常处理器
    
    Args:
        app: FastAPI应用实例
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """处理HTTP异常"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.detail,
                "code": f"HTTP_{exc.status_code}"
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """处理请求验证异常"""
        errors = []
        for error in exc.errors():
            loc = " -> ".join(str(loc_item) for loc_item in error.get("loc", []))
            errors.append({
                "location": loc,
                "message": error.get("msg", "验证错误"),
                "type": error.get("type", "")
            })
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "message": "请求数据验证失败",
                "code": "VALIDATION_ERROR",
                "errors": errors
            }
        )
    
    @app.exception_handler(BaseOpenGeweException)
    async def opengewe_exception_handler(request: Request, exc: BaseOpenGeweException) -> JSONResponse:
        """处理OpenGewe自定义异常"""
        content = {
            "status": "error",
            "message": exc.message,
            "code": exc.error_code
        }
        
        if exc.detail:
            content["detail"] = exc.detail
            
        return JSONResponse(
            status_code=exc.status_code,
            content=content
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        """处理SQLAlchemy异常"""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "数据库操作错误",
                "code": "DATABASE_ERROR",
                "detail": str(exc)
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """处理所有其他未捕获的异常"""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "服务器内部错误",
                "code": "INTERNAL_SERVER_ERROR",
                "detail": str(exc)
            }
        ) 