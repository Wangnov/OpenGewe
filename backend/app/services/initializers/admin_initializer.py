"""
管理员账号初始化模块
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from ...core.config import get_settings
from ...core.session_manager import get_admin_session
from ...models.admin import Admin
from ...core.security import security_manager


async def initialize_admin():
    """
    初始化管理员账号

    检查数据库中是否存在管理员账号，如果不存在则创建默认管理员账号
    """
    settings = get_settings()

    # 获取配置中的管理员用户名和密码
    admin_username = getattr(settings, "admin_username", None)
    admin_password = getattr(settings, "admin_password", None)

    if not admin_username or not admin_password:
        logger.warning("未配置管理员用户名或密码，跳过管理员初始化")
        return

    try:
        # 获取数据库会话
        async for session in get_admin_session():
            # 检查是否已存在管理员账号
            stmt = select(Admin).where(Admin.is_superadmin == True)
            result = await session.execute(stmt)
            admin = result.scalar_one_or_none()

            if admin:
                logger.info(f"已存在超级管理员账号: {admin.username}")
                return

            # 创建默认管理员账号
            hashed_password = security_manager.get_password_hash(admin_password)
            new_admin = Admin(
                username=admin_username,
                hashed_password=hashed_password,
                full_name="系统管理员",
                is_superadmin=True,
                is_active=True,
            )

            session.add(new_admin)
            await session.commit()

            logger.info(f"已创建默认管理员账号: {admin_username}")
    except Exception as e:
        logger.error(f"初始化管理员账号失败: {e}")
        # 初始化失败不影响应用启动
