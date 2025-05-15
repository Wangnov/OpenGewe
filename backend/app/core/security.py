"""
安全配置模块
用于处理认证、授权和密码哈希
"""

import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import get_settings


# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2密码Bearer令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None,
    scopes: Optional[list] = None
) -> str:
    """
    创建JWT访问令牌
    
    Args:
        subject: 令牌主题(通常是用户ID)
        expires_delta: 过期时间增量
        scopes: 权限作用域列表
        
    Returns:
        编码后的JWT令牌
    """
    settings = get_settings()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "iat": datetime.utcnow()
    }
    
    # 添加权限作用域
    if scopes:
        to_encode["scopes"] = scopes
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.backend.secret_key, 
        algorithm="HS256"
    )
    
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码与哈希密码是否匹配
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
        
    Returns:
        密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    对密码进行哈希处理
    
    Args:
        password: 明文密码
        
    Returns:
        哈希后的密码
    """
    return pwd_context.hash(password)


def generate_secure_token(length: int = 32) -> str:
    """
    生成安全随机令牌
    
    Args:
        length: 令牌长度(以字节为单位)
        
    Returns:
        安全随机令牌
    """
    return secrets.token_hex(length)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    从令牌获取当前用户
    
    Args:
        token: JWT令牌
        
    Returns:
        当前用户信息
        
    Raises:
        HTTPException: 如果令牌无效或过期
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    settings = get_settings()
    
    try:
        payload = jwt.decode(
            token, 
            settings.backend.secret_key, 
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # 这里应该返回完整的用户对象，但这需要数据库查询
        # 在实际代码中，应该添加用户检索逻辑
        return {"user_id": user_id, "scopes": payload.get("scopes", [])}
    
    except JWTError:
        raise credentials_exception


def configure_cors(app: FastAPI) -> None:
    """
    配置CORS(跨域资源共享)
    
    Args:
        app: FastAPI应用实例
    """
    from fastapi.middleware.cors import CORSMiddleware
    
    settings = get_settings()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 