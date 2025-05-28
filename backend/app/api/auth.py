"""
认证相关API路由
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.session_manager import get_admin_session
from ..core.security import (
    security_manager,
    rate_limiter,
    get_current_active_user,
    security,
)
from ..models.admin import Admin, AdminLoginLog, LoginStatus
from ..schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
)
from opengewe.logger import init_default_logger, get_logger

init_default_logger()
logger = get_logger(__name__)


router = APIRouter()


@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(
    request: Request,
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_admin_session),
):
    """
    用户登录接口

    - **username**: 用户名
    - **password**: 密码
    - **remember**: 是否记住登录状态
    """
    # 获取客户端信息
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")

    # 检查速率限制
    rate_limit_key = f"login_{client_ip}_{login_data.username}"
    if rate_limiter.is_rate_limited(rate_limit_key):
        logger.warning(f"登录尝试次数过多: {login_data.username} from {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="登录尝试次数过多，请稍后再试",
        )

    # 查询用户
    stmt = select(Admin).where(Admin.username == login_data.username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # 记录失败尝试
        rate_limiter.record_attempt(rate_limit_key)
        await _log_login_attempt(
            session, None, client_ip, user_agent, LoginStatus.FAILED, "用户不存在"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    # 检查用户状态
    if not user.is_active:
        await _log_login_attempt(
            session, user.id, client_ip, user_agent, LoginStatus.FAILED, "用户已被禁用"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="账户已被禁用"
        )

    # 验证密码
    if not security_manager.verify_password(login_data.password, user.hashed_password):
        # 记录失败尝试
        rate_limiter.record_attempt(rate_limit_key)
        await _log_login_attempt(
            session, user.id, client_ip, user_agent, LoginStatus.FAILED, "密码错误"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    # 登录成功，生成令牌
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "is_superadmin": user.is_superadmin,
    }

    access_token = security_manager.create_access_token(token_data)
    refresh_token = security_manager.create_refresh_token(token_data)

    # 更新最后登录时间
    user.last_login_at = datetime.now(timezone.utc)
    await session.commit()

    # 记录成功登录
    await _log_login_attempt(
        session, user.id, client_ip, user_agent, LoginStatus.SUCCESS, None
    )

    logger.info(f"用户登录成功: {user.username} from {client_ip}")

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=security_manager.settings.jwt_expiration_hours * 3600,
        user={
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "is_superadmin": user.is_superadmin,
            "last_login_at": user.last_login_at.isoformat()
            if user.last_login_at
            else None,
        },
    )


@router.post("/refresh", response_model=LoginResponse, summary="刷新令牌")
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_admin_session),
):
    """
    刷新访问令牌

    - **refresh_token**: 刷新令牌
    """
    try:
        # 验证刷新令牌
        payload = security_manager.verify_token(refresh_data.refresh_token)

        # 检查令牌类型
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的刷新令牌"
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌中缺少用户信息"
            )

        # 查询用户
        stmt = select(Admin).where(Admin.id == int(user_id))
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在或已被禁用"
            )

        # 生成新的令牌
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "is_superadmin": user.is_superadmin,
        }

        access_token = security_manager.create_access_token(token_data)
        new_refresh_token = security_manager.create_refresh_token(token_data)

        return LoginResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=security_manager.settings.jwt_expiration_hours * 3600,
            user={
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "is_superadmin": user.is_superadmin,
                "last_login_at": user.last_login_at.isoformat()
                if user.last_login_at
                else None,
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"刷新令牌失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的刷新令牌"
        )


@router.post("/change-password", summary="修改密码")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
):
    """
    修改当前用户密码

    - **old_password**: 原密码
    - **new_password**: 新密码
    - **confirm_password**: 确认新密码
    """
    # 验证新密码确认
    password_data.validate_passwords_match()

    # 查询当前用户
    stmt = select(Admin).where(Admin.id == current_user["id"])
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    # 验证原密码
    if not security_manager.verify_password(
        password_data.old_password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="原密码错误"
        )

    # 更新密码
    user.hashed_password = security_manager.get_password_hash(
        password_data.new_password
    )
    user.updated_at = datetime.now(timezone.utc)

    await session.commit()

    logger.info(f"用户修改密码成功: {user.username}")

    return {"message": "密码修改成功"}


@router.get("/me", summary="获取当前用户信息")
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """获取当前登录用户的详细信息"""
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "is_superadmin": current_user["is_superadmin"],
    }


@router.post("/logout", summary="用户登出")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    用户登出

    注意：由于使用的是无状态JWT，实际的令牌失效需要在客户端处理
    """
    # 在实际应用中，可以将令牌加入黑名单
    # 这里仅返回成功消息
    return {"message": "登出成功"}


async def _log_login_attempt(
    session: AsyncSession,
    admin_id: int,
    login_ip: str,
    user_agent: str,
    status: LoginStatus,
    failure_reason: str = None,
):
    """记录登录尝试"""
    try:
        log_entry = AdminLoginLog(
            admin_id=admin_id,
            login_ip=login_ip,
            user_agent=user_agent,
            status=status,
            failure_reason=failure_reason,
        )
        session.add(log_entry)
        await session.commit()
    except Exception as e:
        logger.error(f"记录登录日志失败: {e}")
        await session.rollback()
