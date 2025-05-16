"""管理服务模块

提供系统管理的业务逻辑，包括用户管理、系统配置等功能。
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from opengewe.logger import get_logger

from backend.app.models.user import User
from backend.app.models.config import Config
from backend.app.core.config import get_settings

# 获取日志记录器
logger = get_logger("AdminService")


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
        """净化用户信息，移除敏感数据

        Args:
            user_dict: 用户字典

        Returns:
            Dict[str, Any]: 净化后的用户字典
        """
        # 移除敏感信息
        if "hashed_password" in user_dict:
            del user_dict["hashed_password"]

        # 转换日期时间为ISO格式
        for key, value in user_dict.items():
            if isinstance(value, datetime):
                user_dict[key] = value.isoformat()

        return user_dict
