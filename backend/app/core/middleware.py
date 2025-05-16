"""中间件模块

提供FastAPI应用程序使用的各种中间件。
"""

import time
from typing import Callable, Optional

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from opengewe.logger import get_logger
from backend.app.core.device import get_device_id_from_request, set_current_device_id

logger = get_logger("Middleware")


class DeviceContextMiddleware(BaseHTTPMiddleware):
    """设备上下文中间件

    自动从请求中提取设备ID并设置到当前上下文中，以便后续处理使用。
    """

    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 尝试提取设备ID
        try:
            # 从请求头或查询参数中获取设备ID
            device_id = request.headers.get("X-Device-ID")
            if not device_id:
                device_id = request.query_params.get("device_id")

            # 如果提供了设备ID，设置它
            if device_id:
                try:
                    # 验证设备ID
                    device_id = await get_device_id_from_request(request, device_id)
                    # 设置到上下文中
                    set_current_device_id(device_id)
                    logger.debug(f"请求使用设备ID: {device_id}")
                except Exception as e:
                    logger.warning(f"设备ID验证失败: {e}")
                    # 如果验证失败，不设置设备ID，将使用默认设备

            # 处理请求
            response = await call_next(request)
            return response

        finally:
            # 清除上下文
            set_current_device_id(None)


class RequestLogMiddleware(BaseHTTPMiddleware):
    """请求日志中间件

    记录每个请求的处理时间和结果。
    """

    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # 获取请求设备ID（如果有）
        device_id = (
            request.headers.get("X-Device-ID")
            or request.query_params.get("device_id")
            or "default"
        )

        # 记录请求开始
        logger.debug(f"[{device_id}] {request.method} {request.url.path} - 开始处理")

        try:
            # 处理请求
            response = await call_next(request)

            # 计算处理时间
            process_time = (time.time() - start_time) * 1000
            logger.info(
                f"[{device_id}] {request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms"
            )

            # 添加处理时间到响应头
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            return response

        except Exception as e:
            # 处理异常
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"[{device_id}] {request.method} {request.url.path} - 500 - {process_time:.2f}ms - {str(e)}"
            )
            raise


def setup_middlewares(app: FastAPI):
    """设置所有中间件

    Args:
        app: FastAPI应用实例
    """
    # 注意中间件的添加顺序很重要，它决定了中间件的执行顺序
    # 最后添加的中间件最先执行

    # 请求日志中间件
    app.add_middleware(RequestLogMiddleware)

    # 设备上下文中间件
    app.add_middleware(DeviceContextMiddleware)
