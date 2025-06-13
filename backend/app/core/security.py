"""
安全认证和授权
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from .config import get_settings
from .database import get_admin_session
from opengewe.logger import init_default_logger, get_logger

init_default_logger()
logger = get_logger(__name__)


# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer认证
security = HTTPBearer()


class SecurityManager:
    """安全管理器"""

    def __init__(self):
        self.settings = get_settings()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """获取密码哈希"""
        return pwd_context.hash(password)

    def create_access_token(self, data: Dict[str, Any]) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            hours=self.settings.jwt_expiration_hours
        )
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, self.settings.secret_key, algorithm=self.settings.jwt_algorithm
        )
        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        """验证令牌"""
        try:
            payload = jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=[self.settings.jwt_algorithm],
            )
            return payload
        except JWTError as e:
            logger.warning(f"JWT验证失败: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证令牌",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """创建刷新令牌（有效期更长）"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"exp": expire, "type": "refresh"})

        encoded_jwt = jwt.encode(
            to_encode, self.settings.secret_key, algorithm=self.settings.jwt_algorithm
        )
        return encoded_jwt


# 全局安全管理器实例
security_manager = SecurityManager()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_admin_session),
) -> Dict[str, Any]:
    """获取当前用户（依赖注入）"""
    token = credentials.credentials
    payload = security_manager.verify_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌中缺少用户信息"
        )

    # 这里后续会从数据库中获取用户信息
    # 目前先返回基本信息
    return {
        "id": user_id,
        "username": payload.get("username"),
        "is_superadmin": payload.get("is_superadmin", False),
    }


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """获取当前活跃用户"""
    # 这里后续可以添加用户状态检查
    return current_user


async def require_superadmin(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """要求超级管理员权限"""
    if not current_user.get("is_superadmin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="需要超级管理员权限"
        )
    return current_user


class RateLimiter:
    """简单的速率限制器"""

    def __init__(self):
        self.attempts: Dict[str, list] = {}
        self.settings = get_settings()

    def is_rate_limited(self, identifier: str, window_minutes: int = 15) -> bool:
        """检查是否触发速率限制"""
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(minutes=window_minutes)

        if identifier not in self.attempts:
            self.attempts[identifier] = []

        # 清理过期记录
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier] if attempt > window_start
        ]

        # 检查是否超过限制
        return len(self.attempts[identifier]) >= self.settings.max_login_attempts

    def record_attempt(self, identifier: str):
        """记录尝试"""
        now = datetime.now(timezone.utc)
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        self.attempts[identifier].append(now)


# 全局速率限制器
rate_limiter = RateLimiter()


async def verify_webhook_source(request: Request) -> bool:
    """验证Webhook来源"""
    settings = get_settings()

    # 获取客户端IP
    client_ip = request.client.host
    if hasattr(request, "headers"):
        # 检查代理头
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            client_ip = real_ip

    # IP白名单检查
    if settings.webhook_ip_whitelist:
        if client_ip not in settings.webhook_ip_whitelist:
            logger.warning(f"Webhook请求来自未授权IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="IP地址未授权"
            )

    # 这里可以添加更多验证逻辑
    # 比如签名验证等

    return True


def validate_password_strength(password: str) -> bool:
    """验证密码强度"""
    settings = get_settings()

    if len(password) < settings.password_min_length:
        return False

    # 可以添加更多密码强度检查
    # 比如必须包含大小写字母、数字、特殊字符等

    return True
