"""API依赖项模块

提供所有API路由共享的依赖项函数，包括认证、权限检查和标准响应格式化。
"""

from typing import Dict, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from opengewe.logger import get_logger
from backend.app.core.config import get_settings
from backend.app.models.user import User
from backend.app.db.session import get_db
from backend.app.gewe.dependencies import get_gewe_client

# 获取设置
settings = get_settings()

# 获取日志记录器
logger = get_logger("API.Deps")

# 创建OAuth2认证方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

# JWT相关配置
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1天
ALGORITHM = "HS256"


def standard_response(code: int = 0, msg: str = "操作成功", data: Any = None) -> Dict:
    """生成标准API响应格式

    Args:
        code: 状态码，0表示成功，非0表示错误
        msg: 响应消息
        data: 响应数据

    Returns:
        Dict: 格式化的响应字典
    """
    return {"code": code, "msg": msg, "data": data if data is not None else {}}


def service_result_to_response(result: Tuple[bool, str, Any]) -> Dict:
    """将服务层返回结果转换为标准API响应

    服务层函数通常返回(success, message, data)三元组，
    此函数将其转换为标准的API响应格式。

    Args:
        result: 服务层返回的(success, message, data)三元组

    Returns:
        Dict: 标准API响应
    """
    success, message, data = result
    code = 0 if success else 1  # 成功时code为0，失败时为1
    return standard_response(code, message, data)


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT访问令牌

    Args:
        data: 要编码的数据
        expires_delta: 令牌有效期

    Returns:
        str: 编码的JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.backend.secret_key, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前已认证用户

    Args:
        token: JWT访问令牌
        db: 数据库会话

    Returns:
        User: 当前用户模型实例

    Raises:
        HTTPException: 认证失败时抛出
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的身份凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 解码JWT令牌
        payload = jwt.decode(token, settings.backend.secret_key, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        logger.warning("JWT认证失败")
        raise credentials_exception

    # 从数据库获取用户
    user = await User.get_by_id(db, int(user_id))
    if user is None:
        logger.warning(f"用户ID {user_id} 不存在")
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前活跃用户（未被禁用）

    Args:
        current_user: 当前已认证用户

    Returns:
        User: 当前活跃用户

    Raises:
        HTTPException: 用户被禁用时抛出
    """
    if not current_user.is_active:
        logger.warning(f"用户 {current_user.username} 已被禁用")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="用户已被禁用"
        )
    return current_user


async def admin_required(current_user: User = Depends(get_current_active_user)) -> User:
    """检查用户是否具有管理员权限

    Args:
        current_user: 当前活跃用户

    Returns:
        User: 具有管理员权限的用户

    Raises:
        HTTPException: 用户不是管理员时抛出
    """
    if not current_user.is_admin:
        logger.warning(f"用户 {current_user.username} 尝试访问管理员功能但权限不足")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="权限不足，需要管理员权限"
        )
    return current_user
