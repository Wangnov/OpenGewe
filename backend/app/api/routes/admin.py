"""管理员路由

提供管理员登录、用户管理等功能。
"""

from fastapi import APIRouter, Depends, Query, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from datetime import timedelta
from pydantic import BaseModel, EmailStr, Field
import asyncio

from opengewe.logger import get_logger

from backend.app.api.deps import (
    standard_response,
    service_result_to_response,
    admin_required,
    get_current_active_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from backend.app.services.admin_service import AdminService
from backend.app.models.user import User
from backend.app.db.session import get_db_session as get_db

# 创建路由实例
router = APIRouter()

# 获取日志记录器
logger = get_logger("API.Admin")


# 获取管理员数据库会话的依赖函数
async def get_admin_db():
    """获取管理员数据库会话"""
    async for session in get_db(is_admin=True):
        yield session


# 用户创建模型
class UserCreate(BaseModel):
    """用户创建模型"""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    is_admin: bool = False
    is_active: bool = True


# 用户更新模型
class UserUpdate(BaseModel):
    """用户更新模型"""

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None


# 密码更新模型
class PasswordChange(BaseModel):
    """密码修改模型"""

    old_password: str
    new_password: str = Field(..., min_length=6)


@router.post("/login", response_model=Dict[str, Any])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_admin_db),
):
    """管理员登录

    Args:
        form_data: 表单数据，包含用户名和密码
        db: 数据库会话

    Returns:
        Dict: 包含访问令牌的标准响应
    """
    logger.info(f"用户 {form_data.username} 尝试登录")
    print(f"[Debug] 登录尝试: 用户名={form_data.username}, 密码={form_data.password}")

    # 获取用户
    user = await User.get_by_username(form_data.username)

    if not user:
        logger.warning(f"用户 {form_data.username} 登录失败：用户不存在")
        print(f"[Debug] 登录失败: 用户 {form_data.username} 不存在")
        return standard_response(1, "无效的用户名或密码")

    # 输出用户信息和密码哈希进行调试
    print(f"[Debug] 用户信息: ID={user.id}, 哈希密码={user.hashed_password}")

    # 验证密码
    password_valid = user.verify_password(form_data.password)
    print(f"[Debug] 密码验证结果: {password_valid}")

    if not password_valid:
        logger.warning(f"用户 {form_data.username} 登录失败：密码错误")
        print(f"[Debug] 登录失败: 密码错误")
        return standard_response(1, "无效的用户名或密码")

    if not user.is_active:
        logger.warning(f"用户 {form_data.username} 登录失败：账户已禁用")
        return standard_response(1, "账户已被禁用")

    # 创建访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    logger.info(f"用户 {form_data.username} 登录成功")
    return standard_response(
        0,
        "登录成功",
        {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
            },
        },
    )


@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """获取当前用户信息

    Args:
        current_user: 当前用户

    Returns:
        Dict: 包含用户信息的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求获取个人信息")

    return standard_response(
        0,
        "获取用户信息成功",
        {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "is_admin": current_user.is_admin,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at,
            "last_login": current_user.last_login,
        },
    )


@router.put("/me/password", response_model=Dict[str, Any])
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_admin_db),
):
    """修改当前用户密码

    Args:
        password_data: 密码修改数据
        current_user: 当前用户
        db: 数据库会话

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"用户 {current_user.username} 请求修改密码")

    # 验证旧密码
    if not current_user.verify_password(password_data.old_password):
        logger.warning(f"用户 {current_user.username} 修改密码失败：旧密码错误")
        return standard_response(1, "旧密码错误")

    # 更新密码
    current_user.set_password(password_data.new_password)
    await current_user.save(db)

    logger.info(f"用户 {current_user.username} 密码修改成功")
    return standard_response(0, "密码修改成功")


@router.get("/users", response_model=Dict[str, Any])
async def list_users(
    page: int = Query(1, description="页码"),
    limit: int = Query(10, description="每页数量"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    current_user: User = Depends(admin_required),
):
    """获取用户列表

    Args:
        page: 页码
        limit: 每页数量
        keyword: 搜索关键词
        current_user: 当前管理员用户

    Returns:
        Dict: 包含用户列表的标准响应
    """
    logger.info(
        f"管理员 {current_user.username} 请求获取用户列表，页码 {page}，每页 {limit}，关键词 {keyword}"
    )

    result = await AdminService.get_users(page, limit, keyword)
    return service_result_to_response(result)


@router.post("/users", response_model=Dict[str, Any])
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(admin_required),
):
    """创建新用户

    Args:
        user_data: 用户创建数据
        current_user: 当前管理员用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求创建用户 {user_data.username}")

    result = await AdminService.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        is_admin=user_data.is_admin,
        is_active=user_data.is_active,
    )

    return service_result_to_response(result)


@router.get("/users/{user_id}", response_model=Dict[str, Any])
async def get_user(
    user_id: int = Path(..., description="用户ID"),
    current_user: User = Depends(admin_required),
):
    """获取用户详情

    Args:
        user_id: 用户ID
        current_user: 当前管理员用户

    Returns:
        Dict: 包含用户详情的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求获取用户 {user_id} 的详情")

    result = await AdminService.get_user_by_id(user_id)
    return service_result_to_response(result)


@router.put("/users/{user_id}", response_model=Dict[str, Any])
async def update_user(
    user_data: UserUpdate,
    user_id: int = Path(..., description="用户ID"),
    current_user: User = Depends(admin_required),
):
    """更新用户信息

    Args:
        user_data: 用户更新数据
        user_id: 用户ID
        current_user: 当前管理员用户

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info(f"管理员 {current_user.username} 请求更新用户 {user_id}")

    # 防止管理员自降权限
    if current_user.id == user_id and user_data.is_admin is False:
        logger.warning(f"管理员 {current_user.username} 尝试撤销自己的管理员权限")
        return standard_response(1, "不能撤销自己的管理员权限")

    # 收集要更新的字段
    update_data = {}
    if user_data.username:
        update_data["username"] = user_data.username
    if user_data.email:
        update_data["email"] = user_data.email
    if user_data.password:
        update_data["password"] = user_data.password
    if user_data.is_admin is not None:
        update_data["is_admin"] = user_data.is_admin
    if user_data.is_active is not None:
        update_data["is_active"] = user_data.is_active

    result = await AdminService.update_user(user_id, update_data)
    return service_result_to_response(result)


@router.delete("/users/{user_id}", response_model=Dict[str, Any])
async def delete_user(
    user_id: int = Path(..., description="用户ID"),
    current_user: User = Depends(admin_required),
):
    """删除用户

    Args:
        user_id: 用户ID
        current_user: 当前管理员用户

    Returns:
        Dict: 操作结果的标准响应
    """
    # 防止管理员删除自己
    if current_user.id == user_id:
        logger.warning(f"管理员 {current_user.username} 尝试删除自己")
        return standard_response(1, "不能删除自己的账户")

    logger.info(f"管理员 {current_user.username} 请求删除用户 {user_id}")

    result = await AdminService.delete_user(user_id)
    return service_result_to_response(result)


@router.post("/init", response_model=Dict[str, Any])
async def init_admin():
    """初始化管理员账户

    仅当系统中没有任何用户时才能执行此操作

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info("请求初始化管理员账户")

    result = await AdminService.init_admin()
    return service_result_to_response(result)


@router.get("/check-init", response_model=Dict[str, Any])
async def check_admin_init():
    """检查管理员账户是否已初始化，并在必要时初始化

    此接口用于前端检查管理员账户状态，如果没有管理员账户，则自动初始化

    Returns:
        Dict: 包含管理员账户状态的标准响应
    """
    logger.info("检查管理员账户状态")

    try:
        # 使用单一优化的SQL查询，直接检查管理员账户
        from sqlalchemy import text
        from backend.app.db.session import DatabaseManager, DB_OPERATION_TIMEOUT

        db_manager = DatabaseManager()

        # 使用更长的超时时间
        async with asyncio.timeout(DB_OPERATION_TIMEOUT * 2):
            # 获取引擎直接连接
            engine = await db_manager.get_engine(is_admin=True)
            async with engine.connect() as conn:
                try:
                    # 更简单的查询：直接检查管理员账户是否存在
                    logger.debug("执行管理员账户检查查询")
                    result = await conn.execute(
                        text(
                            "SELECT id, username, email, full_name, is_active, is_admin, is_superuser, created_at, updated_at FROM users WHERE is_admin = TRUE LIMIT 1"
                        )
                    )
                    admin_record = result.first()

                    if admin_record:
                        # 管理员账户已存在
                        admin_data = {
                            "id": admin_record.id,
                            "username": admin_record.username,
                            "email": admin_record.email,
                            "full_name": admin_record.full_name,
                            "is_active": admin_record.is_active,
                            "is_admin": admin_record.is_admin,
                            "is_superuser": admin_record.is_superuser,
                            "created_at": admin_record.created_at.isoformat()
                            if admin_record.created_at
                            else None,
                            "updated_at": admin_record.updated_at.isoformat()
                            if admin_record.updated_at
                            else None,
                        }

                        logger.info(f"管理员账户已存在: {admin_data['username']}")
                        return standard_response(
                            0,
                            "管理员账户已存在",
                            {
                                "initialized": True,
                                "admin": AdminService._sanitize_user(admin_data),
                                "status": "success",
                                "detail": "已初始化",
                            },
                        )
                    else:
                        # 检查表是否存在但没有管理员账户
                        has_table = await conn.run_sync(
                            lambda sync_conn: sync_conn.dialect.has_table(
                                sync_conn, "users"
                            )
                        )

                        if not has_table:
                            logger.info("users表不存在，需要初始化管理员数据库")
                        else:
                            logger.info(
                                "users表存在但没有管理员账户，需要初始化管理员账户"
                            )

                        # 初始化管理员账户
                        await conn.close()  # 确保连接正确关闭
                        logger.info("正在初始化管理员账户")
                        success, message, admin_info = await AdminService.init_admin()

                        if not success:
                            logger.error(f"初始化管理员账户失败: {message}")
                            return standard_response(
                                1,
                                message,
                                {
                                    "initialized": False,
                                    "error": message,
                                    "status": "error",
                                    "detail": "初始化失败",
                                },
                            )

                        logger.success("管理员账户初始化成功")
                        return standard_response(
                            0,
                            "管理员账户初始化成功",
                            {
                                "initialized": True,
                                "admin": admin_info,
                                "status": "success",
                                "detail": "初始化成功",
                            },
                        )
                except Exception as e:
                    logger.error(f"查询管理员账户时数据库错误: {e}")
                    raise

    except asyncio.TimeoutError as e:
        logger.error(f"检查管理员账户状态超时: {e}")
        return standard_response(
            1,
            "检查管理员账户状态超时",
            {
                "initialized": False,
                "error": "操作超时，请稍后重试",
                "status": "error",
                "detail": "操作超时",
            },
        )
    except Exception as e:
        logger.error(f"检查管理员账户状态时发生错误: {e}")
        # 在检查失败的情况下尝试初始化
        try:
            logger.info("检查失败，尝试直接初始化管理员账户")
            success, message, admin_info = await AdminService.init_admin()

            if not success:
                return standard_response(
                    1,
                    f"检查管理员状态失败，尝试初始化也失败: {str(e)}",
                    {
                        "initialized": False,
                        "error": str(e),
                        "status": "error",
                        "detail": "数据库操作失败",
                    },
                )

            return standard_response(
                0,
                "管理员账户初始化成功",
                {
                    "initialized": True,
                    "admin": admin_info,
                    "status": "success",
                    "detail": "初始化成功",
                },
            )
        except Exception as inner_e:
            logger.error(f"尝试初始化管理员账户时发生错误: {inner_e}")
            return standard_response(
                1,
                f"无法检查或初始化管理员账户: {str(e)}; {str(inner_e)}",
                {
                    "initialized": False,
                    "error": f"{str(e)}; {str(inner_e)}",
                    "status": "error",
                    "detail": "严重错误",
                },
            )


@router.post("/reset-password", response_model=Dict[str, Any])
async def reset_admin_password():
    """重置管理员密码为默认密码

    此接口用于将管理员密码重置为配置文件中的默认密码

    Returns:
        Dict: 操作结果的标准响应
    """
    logger.info("开始重置管理员密码")

    result = await AdminService.reset_admin_password()
    return service_result_to_response(result)
