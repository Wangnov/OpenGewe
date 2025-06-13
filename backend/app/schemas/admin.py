"""
管理员相关的Pydantic schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class AdminBase(BaseModel):
    """管理员基础模型"""

    username: str = Field(..., min_length=1, max_length=50, description="用户名")
    full_name: Optional[str] = Field(None, max_length=100, description="全名")
    is_superadmin: bool = Field(False, description="是否为超级管理员")
    is_active: bool = Field(True, description="是否激活")


class AdminCreate(AdminBase):
    """创建管理员请求"""

    password: str = Field(..., min_length=8, description="密码")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        """验证用户名格式"""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("用户名只能包含字母、数字、下划线和短横线")
        return v


class AdminUpdate(BaseModel):
    """更新管理员请求"""

    full_name: Optional[str] = Field(None, max_length=100, description="全名")
    is_superadmin: Optional[bool] = Field(None, description="是否为超级管理员")
    is_active: Optional[bool] = Field(None, description="是否激活")
    password: Optional[str] = Field(None, min_length=8, description="新密码")


class AdminResponse(AdminBase):
    """管理员响应"""

    id: int = Field(..., description="管理员ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    last_login_at: Optional[datetime] = Field(None, description="最后登录时间")

    class Config:
        from_attributes = True


class AdminListResponse(BaseModel):
    """管理员列表响应"""

    admins: list[AdminResponse] = Field(..., description="管理员列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")


class AdminLoginLogResponse(BaseModel):
    """管理员登录日志响应"""

    id: int = Field(..., description="日志ID")
    admin_id: int = Field(..., description="管理员ID")
    login_ip: Optional[str] = Field(None, description="登录IP")
    user_agent: Optional[str] = Field(None, description="用户代理")
    login_at: datetime = Field(..., description="登录时间")
    status: str = Field(..., description="登录状态")
    failure_reason: Optional[str] = Field(None, description="失败原因")

    class Config:
        from_attributes = True


class GlobalPluginBase(BaseModel):
    """全局插件基础模型"""

    plugin_name: str = Field(..., min_length=1, max_length=100, description="插件名称")
    is_globally_enabled: bool = Field(True, description="是否全局启用")
    global_config_json: Optional[str] = Field(None, description="全局配置JSON")


class GlobalPluginCreate(GlobalPluginBase):
    """创建全局插件请求"""

    pass


class GlobalPluginUpdate(BaseModel):
    """更新全局插件请求"""

    is_globally_enabled: Optional[bool] = Field(None, description="是否全局启用")
    global_config_json: Optional[str] = Field(None, description="全局配置JSON")


class GlobalPluginResponse(GlobalPluginBase):
    """全局插件响应"""

    id: int = Field(..., description="插件ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class GlobalPluginListResponse(BaseModel):
    """全局插件列表响应"""

    plugins: list[GlobalPluginResponse] = Field(..., description="插件列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
