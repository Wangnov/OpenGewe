"""
管理员相关数据模型
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Boolean, Text, DateTime, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from ..core.bases import AdminBase
from ..core.timezone_utils import to_app_timezone


class LoginStatus(enum.Enum):
    """登录状态枚举"""

    SUCCESS = "success"
    FAILED = "failed"


class Admin(AdminBase):
    """管理员表"""

    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    is_superadmin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: to_app_timezone(datetime.now(timezone.utc))
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: to_app_timezone(datetime.now(timezone.utc)),
        onupdate=lambda: to_app_timezone(datetime.now(timezone.utc)),
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"<Admin(id={self.id}, username='{self.username}')>"


class AdminLoginLog(AdminBase):
    """管理员登录日志表"""

    __tablename__ = "admin_login_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    login_ip: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    login_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: to_app_timezone(datetime.now(timezone.utc)),
        index=True,
    )
    status: Mapped[LoginStatus] = mapped_column(Enum(LoginStatus), nullable=False)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"<AdminLoginLog(id={self.id}, admin_id={self.admin_id}, status={self.status})>"


class GlobalPlugin(AdminBase):
    """全局插件配置表"""

    __tablename__ = "global_plugins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plugin_name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    is_globally_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    global_config_json: Mapped[Optional[str]] = mapped_column(Text)  # JSON配置
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: to_app_timezone(datetime.now(timezone.utc))
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: to_app_timezone(datetime.now(timezone.utc)),
        onupdate=lambda: to_app_timezone(datetime.now(timezone.utc)),
    )

    def __repr__(self) -> str:
        return f"<GlobalPlugin(id={self.id}, name='{self.plugin_name}')>"
