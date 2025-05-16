"""
设备上下文管理模块

在多设备环境中管理当前活动的设备ID上下文，使数据库会话、API请求等能够访问当前操作的设备。
"""

import asyncio
from contextvars import ContextVar
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request

from backend.app.core.config import get_settings


# 设备ID上下文变量
_device_id_ctx_var: ContextVar[Optional[str]] = ContextVar("device_id", default=None)


def get_current_device_id() -> Optional[str]:
    """获取当前请求的设备ID

    Returns:
        str: 当前上下文设备ID或None
    """
    return _device_id_ctx_var.get()


def set_current_device_id(device_id: Optional[str]) -> None:
    """设置当前上下文的设备ID

    Args:
        device_id: 要设置的设备ID
    """
    _device_id_ctx_var.set(device_id)


class DeviceContext:
    """设备上下文管理器，用于在执行代码块期间维护设备ID上下文"""

    def __init__(self, device_id: str):
        self.device_id = device_id
        self.token = None

    def __enter__(self):
        self.token = _device_id_ctx_var.set(self.device_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _device_id_ctx_var.reset(self.token)

    async def __aenter__(self):
        self.token = _device_id_ctx_var.set(self.device_id)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        _device_id_ctx_var.reset(self.token)


async def get_device_id_from_request(
    request: Request, x_device_id: Optional[str] = Header(None, description="设备ID")
) -> str:
    """从请求中提取设备ID的依赖项函数

    优先级：
    1. 请求头 X-Device-ID
    2. URL查询参数 device_id
    3. 默认设备ID

    Args:
        request: FastAPI 请求对象
        x_device_id: 请求头中的X-Device-ID值

    Returns:
        str: 设备ID

    Raises:
        HTTPException: 如果指定的设备ID不存在
    """
    # 首先检查请求头
    device_id = x_device_id

    # 其次检查查询参数
    if not device_id:
        device_id = request.query_params.get("device_id")

    # 验证设备ID是否有效
    settings = get_settings()

    # 如果没有指定设备ID，使用默认设备
    if not device_id:
        try:
            device_id = settings.devices.get_default_device_id()
        except ValueError:
            raise HTTPException(status_code=500, detail="系统未配置任何设备")

    # 检查设备ID是否存在
    if device_id not in settings.devices.keys():
        raise HTTPException(status_code=404, detail=f"设备ID '{device_id}' 不存在")

    return device_id


async def get_device_id_dependency(
    device_id: str = Depends(get_device_id_from_request),
) -> str:
    """用于路由的设备ID依赖项，自动设置当前上下文的设备ID

    Args:
        device_id: 从请求中提取的设备ID

    Returns:
        str: 设备ID，设置为当前上下文
    """
    set_current_device_id(device_id)
    return device_id


def with_device_id(device_id: str):
    """装饰器：在函数执行期间使用指定的设备ID

    用法示例：
    ```
    @with_device_id("default")
    async def some_function():
        # 函数体内可以访问current_device_id
        pass
    ```

    Args:
        device_id: 要使用的设备ID

    Returns:
        函数装饰器
    """

    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            async with DeviceContext(device_id):
                return await func(*args, **kwargs)

        def sync_wrapper(*args, **kwargs):
            with DeviceContext(device_id):
                return func(*args, **kwargs)

        # 选择适当的包装器根据函数是否为协程
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
