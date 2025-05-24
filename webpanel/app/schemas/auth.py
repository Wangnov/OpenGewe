"""
认证相关的Pydantic schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=1, max_length=50, description="用户名")
    password: str = Field(..., min_length=1, description="密码")
    remember: bool = Field(False, description="记住登录状态")


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(..., description="令牌过期时间（秒）")
    user: dict = Field(..., description="用户信息")


class TokenPayload(BaseModel):
    """JWT令牌负载"""
    sub: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    is_superadmin: bool = Field(False, description="是否为超级管理员")
    exp: datetime = Field(..., description="过期时间")


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求"""
    refresh_token: str = Field(..., description="刷新令牌")


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., min_length=1, description="原密码")
    new_password: str = Field(..., min_length=8, description="新密码")
    confirm_password: str = Field(..., min_length=8, description="确认新密码")
    
    def validate_passwords_match(self):
        """验证两次密码输入是否一致"""
        if self.new_password != self.confirm_password:
            raise ValueError("新密码与确认密码不一致")
        return True 