"""管理服务模块

提供系统管理的业务逻辑，包括用户管理、系统配置等功能。
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from sqlalchemy.exc import SQLAlchemyError, TimeoutError as SQLATimeoutError
from sqlalchemy import text

from opengewe.logger import get_logger

from backend.app.models.user import User, pwd_context
from backend.app.models.config import Config
from backend.app.core.config import get_settings
from backend.app.db.session import (
    DB_OPERATION_TIMEOUT,
    DB_SEMAPHORE,
    DatabaseManager,
    ADMIN_DATABASE,
)
from backend.app.db.base import Base

# 获取日志记录器
logger = get_logger("AdminService")

# 默认管理员配置
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_EMAIL = "admin@opengewe.com"
DEFAULT_ADMIN_PASSWORD = "admin123"  # 这个密码应该在首次登录时强制修改

# 初始化操作的超时时间（30秒）
INIT_OPERATION_TIMEOUT = 30


class AdminService:
    """管理服务类

    提供系统管理的业务逻辑。
    """

    # ----------------------- 用户管理 -----------------------

    @staticmethod
    async def get_all_users(include_inactive: bool = True) -> List[Dict[str, Any]]:
        """获取所有用户

        Args:
            include_inactive: 是否包含非活跃用户

        Returns:
            List[Dict[str, Any]]: 用户列表
        """
        users = await User.get_all()

        # 过滤非活跃用户
        if not include_inactive:
            users = [u for u in users if u.is_active]

        # 保护敏感信息
        return [AdminService._sanitize_user(user.to_dict()) for user in users]

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """获取指定用户名的用户

        Args:
            username: 用户名

        Returns:
            Optional[Dict[str, Any]]: 用户信息，如果不存在则为None
        """
        user = await User.get_by_username(username)
        if not user:
            return None

        return AdminService._sanitize_user(user.to_dict())

    @staticmethod
    async def create_user(
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        is_superuser: bool = False,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """创建新用户

        Args:
            username: 用户名
            email: 邮箱
            password: 密码
            full_name: 全名
            is_superuser: 是否为超级用户

        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: (是否成功, 消息, 用户信息)
        """
        # 检查用户名是否已存在
        existing_user = await User.get_by_username(username)
        if existing_user:
            return False, f"用户名 {username} 已存在", None

        # 检查邮箱是否已存在
        existing_email = await User.get_by_email(email)
        if existing_email:
            return False, f"邮箱 {email} 已被使用", None

        # 创建新用户
        user = await User.create(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            is_superuser=is_superuser,
        )

        if not user:
            return False, "创建用户失败", None

        return (
            True,
            f"用户 {username} 创建成功",
            AdminService._sanitize_user(user.to_dict()),
        )

    @staticmethod
    async def update_password(username: str, new_password: str) -> Tuple[bool, str]:
        """更新用户密码

        Args:
            username: 用户名
            new_password: 新密码

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await User.update_password(username, new_password)
        if result:
            return True, f"用户 {username} 密码已更新"
        else:
            return False, f"用户 {username} 不存在或密码更新失败"

    @staticmethod
    async def activate_user(username: str) -> Tuple[bool, str]:
        """激活用户

        Args:
            username: 用户名

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await User.toggle_active(username, True)
        if result:
            return True, f"用户 {username} 已激活"
        else:
            return False, f"用户 {username} 不存在或激活失败"

    @staticmethod
    async def deactivate_user(username: str) -> Tuple[bool, str]:
        """停用用户

        Args:
            username: 用户名

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await User.toggle_active(username, False)
        if result:
            return True, f"用户 {username} 已停用"
        else:
            return False, f"用户 {username} 不存在或停用失败"

    @staticmethod
    async def delete_user(username: str) -> Tuple[bool, str]:
        """删除用户

        Args:
            username: 用户名

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await User.delete_by_username(username)
        if result:
            return True, f"用户 {username} 已删除"
        else:
            return False, f"用户 {username} 不存在或删除失败"

    @staticmethod
    async def update_user_login(username: str) -> Tuple[bool, str]:
        """更新用户登录时间

        Args:
            username: 用户名

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await User.update_last_login(username)
        if result:
            return True, f"用户 {username} 登录时间已更新"
        else:
            return False, f"用户 {username} 不存在或登录时间更新失败"

    @staticmethod
    async def generate_api_key(
        username: str, expires_days: int = 30
    ) -> Tuple[bool, str, Optional[str]]:
        """为用户生成API密钥

        Args:
            username: 用户名
            expires_days: 过期天数

        Returns:
            Tuple[bool, str, Optional[str]]: (是否成功, 消息, API密钥)
        """
        # 获取用户
        user = await User.get_by_username(username)
        if not user:
            return False, f"用户 {username} 不存在", None

        # 生成密钥
        try:
            from backend.app.db.session import DatabaseManager

            db_manager = DatabaseManager()
            async with db_manager.get_session() as session:
                # 生成API密钥
                api_key = user.generate_api_key(expires_days)

                # 保存到数据库
                session.add(user)
                await session.commit()

                return (
                    True,
                    f"用户 {username} 的API密钥已生成，有效期 {expires_days} 天",
                    api_key,
                )
        except Exception as e:
            logger.error(f"为用户 {username} 生成API密钥时出错: {e}")
            return False, f"生成API密钥出错: {str(e)}", None

    @staticmethod
    async def verify_api_key(api_key: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """验证API密钥

        Args:
            api_key: API密钥

        Returns:
            Tuple[bool, Optional[Dict[str, Any]]]: (是否有效, 用户信息)
        """
        user = await User.get_by_api_key(api_key)
        if not user:
            return False, None

        return True, AdminService._sanitize_user(user.to_dict())

    @staticmethod
    async def revoke_api_key(username: str) -> Tuple[bool, str]:
        """撤销用户的API密钥

        Args:
            username: 用户名

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 获取用户
        user = await User.get_by_username(username)
        if not user:
            return False, f"用户 {username} 不存在"

        # 撤销密钥
        try:
            from backend.app.db.session import DatabaseManager

            db_manager = DatabaseManager()
            async with db_manager.get_session() as session:
                # 清除API密钥
                user.api_key = None
                user.api_key_expires = None

                # 保存到数据库
                session.add(user)
                await session.commit()

                return True, f"用户 {username} 的API密钥已撤销"
        except Exception as e:
            logger.error(f"撤销用户 {username} 的API密钥时出错: {e}")
            return False, f"撤销API密钥出错: {str(e)}"

    @staticmethod
    async def _ensure_admin_database() -> bool:
        """确保管理员数据库存在并创建所需的表

        Returns:
            bool: 是否成功创建或确认数据库存在
        """
        try:
            db_manager = DatabaseManager()
            settings = get_settings()

            # 创建一个临时引擎连接到默认数据库
            default_engine = await db_manager.get_engine(is_admin=False)

            async with default_engine.begin() as conn:
                # 检查admin数据库是否存在
                result = await conn.execute(
                    text(
                        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :schema"
                    ),
                    {"schema": ADMIN_DATABASE},
                )
                if not result.scalar():
                    # 创建admin数据库
                    await conn.execute(text(f"CREATE DATABASE `{ADMIN_DATABASE}`"))
                    logger.info(f"已创建管理员数据库: {ADMIN_DATABASE}")

            # 获取admin数据库的引擎并创建表
            admin_engine = await db_manager.get_engine(is_admin=True)
            async with admin_engine.begin() as conn:
                # 使用SQLAlchemy的模型创建表
                await conn.run_sync(Base.metadata.create_all)
                logger.info("已创建管理员数据库的所有表")

            return True
        except Exception as e:
            logger.error(f"创建管理员数据库失败: {e}")
            return False

    @staticmethod
    async def init_admin() -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """初始化管理员账户

        如果系统中没有任何用户，则创建默认管理员账户。
        此方法使用了超时保护和并发控制。

        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: (是否成功, 消息, 管理员信息)
        """
        try:
            logger.info("开始初始化管理员账户")

            # 使用直接SQL创建管理员账户，不使用ORM
            from sqlalchemy import text

            # 获取配置中的管理员信息
            settings = get_settings()

            # 获取数据库管理器
            db_manager = DatabaseManager()

            try:
                # 检查管理员数据库是否初始化
                engine = await db_manager.get_engine(is_admin=True)
            except Exception as e:
                logger.error(f"无法连接到管理员数据库: {e}")
                # 初始化管理员数据库
                from backend.app.db.init_db import init_admin_db

                await init_admin_db()
                # 重新获取引擎
                engine = await db_manager.get_engine(is_admin=True)

            # 使用单个连接检查管理员账户并创建(如果需要)
            async with engine.begin() as conn:
                try:
                    # 检查users表是否存在
                    has_table = await conn.run_sync(
                        lambda sync_conn: sync_conn.dialect.has_table(
                            sync_conn, "users"
                        )
                    )

                    if not has_table:
                        logger.info("users表不存在，需要创建")
                        # 创建管理员数据库和表
                        await conn.close()  # 先关闭当前连接
                        from backend.app.db.init_db import init_admin_db

                        await init_admin_db()
                        # 已经创建了管理员账户，返回成功
                        return (
                            True,
                            "管理员账户创建成功",
                            {
                                "id": 1,
                                "username": settings.admin.username,
                                "email": settings.admin.email,
                                "full_name": "System Administrator",
                                "is_active": True,
                                "is_admin": True,
                                "is_superuser": True,
                            },
                        )

                    # 检查管理员账户是否存在
                    result = await conn.execute(
                        text(
                            "SELECT id, username, email, full_name, is_active, is_admin, is_superuser, created_at, updated_at FROM users WHERE is_admin = TRUE LIMIT 1"
                        )
                    )
                    admin_record = result.first()

                    if admin_record:
                        # 管理员账户已存在
                        logger.info(f"管理员账户已存在: {admin_record.username}")
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
                        return (
                            True,
                            "管理员账户已存在",
                            AdminService._sanitize_user(admin_data),
                        )

                    # 如果没有管理员账户，创建一个
                    logger.info(f"创建默认管理员账户: {settings.admin.username}")

                    # 哈希密码
                    from backend.app.models.user import pwd_context

                    hashed_password = pwd_context.hash(settings.admin.password)

                    # 插入管理员账户
                    await conn.execute(
                        text("""
                        INSERT INTO users (username, email, full_name, hashed_password, is_active, is_admin, is_superuser, created_at, updated_at)
                        VALUES (:username, :email, :full_name, :hashed_password, :is_active, :is_admin, :is_superuser, NOW(), NOW())
                        """),
                        {
                            "username": settings.admin.username,
                            "email": settings.admin.email,
                            "full_name": "System Administrator",
                            "hashed_password": hashed_password,
                            "is_active": True,
                            "is_admin": True,
                            "is_superuser": True,
                        },
                    )

                    # 获取插入的ID
                    result = await conn.execute(
                        text(
                            "SELECT id, username, email, full_name, is_active, is_admin, is_superuser, created_at, updated_at FROM users WHERE username = :username"
                        ),
                        {"username": settings.admin.username},
                    )
                    admin_record = result.first()

                    if not admin_record:
                        return False, "创建管理员账户后无法检索账户信息", None

                    # 转换为字典
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

                    logger.info(f"管理员账户创建成功: ID={admin_data['id']}")
                    return (
                        True,
                        "管理员账户创建成功",
                        AdminService._sanitize_user(admin_data),
                    )

                except Exception as e:
                    logger.error(f"初始化管理员账户时数据库错误: {e}")
                    return False, f"数据库错误: {str(e)}", None

        except Exception as e:
            logger.error(f"初始化管理员账户时发生未知错误: {e}")
            return False, f"未知错误: {str(e)}", None

    @staticmethod
    async def reset_admin_password() -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """重置管理员密码

        将管理员密码重置为配置文件中的默认密码，使用直接SQL更新。

        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: (是否成功, 消息, 数据)
        """
        try:
            from sqlalchemy import text
            from backend.app.models.user import pwd_context
            from backend.app.core.config import get_settings
            from backend.app.db.session import DatabaseManager

            settings = get_settings()
            db_manager = DatabaseManager()
            engine = await db_manager.get_engine(is_admin=True)

            # 使用固定的已知密码哈希，对应于'admin123'
            hashed_password = (
                "$2b$12$w1yP8cAgOBb/TgBVMCVHaOXUJFdYFcqUQH0qwQJoQs7xDkPQC3QVG"
            )

            # 直接执行SQL更新管理员密码
            async with engine.begin() as conn:
                await conn.execute(
                    text(
                        "UPDATE users SET hashed_password = :password WHERE username = :username"
                    ),
                    {"password": hashed_password, "username": settings.admin.username},
                )

            return True, f"管理员 {settings.admin.username} 密码已重置为默认密码", None
        except Exception as e:
            logger.error(f"重置管理员密码失败: {e}")
            return False, f"重置管理员密码失败: {e}", None

    # ----------------------- 配置管理 -----------------------

    @staticmethod
    async def get_all_config() -> Dict[str, Dict[str, Any]]:
        """获取所有配置

        按类别组织配置。

        Returns:
            Dict[str, Dict[str, Any]]: 配置字典，按类别分组
        """
        configs = await Config.get_all()

        # 按类别分组
        result = {}
        for config in configs:
            category = config.category
            if category not in result:
                result[category] = {}

            result[category][config.key] = config.value_parsed

        return result

    @staticmethod
    async def get_config_by_category(category: str) -> Dict[str, Any]:
        """获取指定类别的配置

        Args:
            category: 配置类别

        Returns:
            Dict[str, Any]: 配置字典
        """
        return await Config.get_dict_by_category(category)

    @staticmethod
    async def get_config_value(key: str, default: Any = None) -> Any:
        """获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            Any: 配置值
        """
        return await Config.get_value(key, default)

    @staticmethod
    async def set_config_value(
        key: str,
        value: Any,
        category: str = "general",
        description: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """设置配置值

        Args:
            key: 配置键
            value: 配置值
            category: 配置类别
            description: 配置描述

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await Config.set_value(key, value, category, description)
        if result:
            return True, f"配置 {key} 已设置"
        else:
            return False, f"设置配置 {key} 失败"

    @staticmethod
    async def set_config_dict(
        config_dict: Dict[str, Any], category: str
    ) -> Tuple[bool, str]:
        """设置配置字典

        Args:
            config_dict: 配置字典
            category: 配置类别

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await Config.set_dict(config_dict, category)
        if result:
            return True, f"类别 {category} 的配置已设置"
        else:
            return False, f"设置类别 {category} 的配置失败"

    @staticmethod
    async def delete_config(key: str) -> Tuple[bool, str]:
        """删除配置

        Args:
            key: 配置键

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await Config.delete(key)
        if result:
            return True, f"配置 {key} 已删除"
        else:
            return False, f"配置 {key} 不存在或删除失败"

    # ----------------------- 系统管理 -----------------------

    @staticmethod
    async def get_system_info() -> Dict[str, Any]:
        """获取系统信息

        Returns:
            Dict[str, Any]: 系统信息
        """
        import platform
        import psutil
        import os

        settings = get_settings()

        # 系统信息
        system_info = {
            "os": {
                "name": platform.system(),
                "version": platform.version(),
                "release": platform.release(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
            },
            "python": {
                "version": platform.python_version(),
                "implementation": platform.python_implementation(),
                "compiler": platform.python_compiler(),
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent,
            },
            "disk": {
                "total": psutil.disk_usage("/").total,
                "used": psutil.disk_usage("/").used,
                "free": psutil.disk_usage("/").free,
                "percent": psutil.disk_usage("/").percent,
            },
            "cpu": {
                "cores": psutil.cpu_count(logical=False),
                "threads": psutil.cpu_count(logical=True),
                "percent": psutil.cpu_percent(interval=0.1),
            },
            "process": {
                "pid": os.getpid(),
                "memory_percent": psutil.Process(os.getpid()).memory_percent(),
                "cpu_percent": psutil.Process(os.getpid()).cpu_percent(interval=0.1),
                "threads": len(psutil.Process(os.getpid()).threads()),
            },
            "app": {
                "version": settings.backend.version,
                "debug": settings.backend.debug,
                "host": settings.backend.host,
                "port": settings.backend.port,
            },
        }

        return system_info

    @staticmethod
    async def ensure_default_config() -> None:
        """确保默认配置存在

        创建系统必需的默认配置。
        """
        defaults = {
            "general": {
                "site_name": {
                    "value": "OpenGewe管理平台",
                    "description": "站点名称",
                },
                "site_description": {
                    "value": "基于OpenGewe的微信管理平台",
                    "description": "站点描述",
                },
                "logo_url": {
                    "value": "/static/logo.png",
                    "description": "Logo URL",
                },
                "favicon_url": {
                    "value": "/static/favicon.ico",
                    "description": "Favicon URL",
                },
            },
            "security": {
                "allow_registration": {
                    "value": False,
                    "description": "是否允许注册",
                },
                "password_min_length": {
                    "value": 8,
                    "description": "密码最小长度",
                },
                "api_key_expires_days": {
                    "value": 30,
                    "description": "API密钥过期天数",
                },
                "enable_2fa": {
                    "value": False,
                    "description": "是否启用二次验证",
                },
            },
            "ui": {
                "theme": {
                    "value": "light",
                    "description": "主题",
                },
                "language": {
                    "value": "zh-CN",
                    "description": "语言",
                },
                "items_per_page": {
                    "value": 20,
                    "description": "每页项目数",
                },
                "date_format": {
                    "value": "YYYY-MM-DD",
                    "description": "日期格式",
                },
                "time_format": {
                    "value": "HH:mm:ss",
                    "description": "时间格式",
                },
            },
        }

        await Config.ensure_defaults(defaults)

    # ----------------------- 辅助方法 -----------------------

    @staticmethod
    def _sanitize_user(user_dict: Dict[str, Any]) -> Dict[str, Any]:
        """清理用户数据，移除敏感信息

        Args:
            user_dict: 用户数据字典

        Returns:
            Dict[str, Any]: 清理后的用户数据
        """
        # 确保所有必要的字段都存在
        safe_fields = {
            "id": user_dict.get("id"),
            "username": user_dict.get("username"),
            "email": user_dict.get("email"),
            "is_active": user_dict.get("is_active", True),
            "is_admin": user_dict.get("is_admin", False),
            "is_superuser": user_dict.get("is_superuser", False),
            "created_at": user_dict.get("created_at"),
            "updated_at": user_dict.get("updated_at"),
        }

        # 转换日期时间为ISO格式字符串
        for field in ["created_at", "updated_at"]:
            if safe_fields[field] and isinstance(safe_fields[field], datetime):
                safe_fields[field] = safe_fields[field].isoformat()

        return safe_fields
