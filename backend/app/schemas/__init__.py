"""
Pydantic schemas for request/response validation
"""

from .auth import (
    LoginRequest,
    LoginResponse,
    TokenPayload,
    RefreshTokenRequest,
    ChangePasswordRequest,
)
from .admin import (
    AdminCreate,
    AdminUpdate,
    AdminResponse,
    AdminListResponse,
    AdminLoginLogResponse,
    GlobalPluginCreate,
    GlobalPluginUpdate,
    GlobalPluginResponse,
    GlobalPluginListResponse,
)
from .bot import (
    BotCreateRequest,
    BotResponse,
    BotUpdateRequest,
    BotListResponse,
    BotStatusResponse,
    ContactResponse,
    GroupMemberResponse,
    BotPluginResponse,
    SnsPostResponse,
    WebhookPayload,
    RawCallbackLogResponse,
)

__all__ = [
    # Auth schemas
    "LoginRequest",
    "LoginResponse",
    "TokenPayload",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    # Admin schemas
    "AdminCreate",
    "AdminUpdate",
    "AdminResponse",
    "AdminListResponse",
    "AdminLoginLogResponse",
    "GlobalPluginCreate",
    "GlobalPluginUpdate",
    "GlobalPluginResponse",
    "GlobalPluginListResponse",
    # Bot schemas
    "BotCreateRequest",
    "BotResponse",
    "BotUpdateRequest",
    "BotListResponse",
    "BotStatusResponse",
    "ContactResponse",
    "GroupMemberResponse",
    "BotPluginResponse",
    "SnsPostResponse",
    "WebhookPayload",
    "RawCallbackLogResponse",
]
