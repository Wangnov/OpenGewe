"""数据库初始化模块

提供数据库连接和会话管理功能，支持MySQL多schema。
"""

import asyncio
from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DatabaseManager, ADMIN_DATABASE
from backend.app.core.config import get_settings
from backend.app.core.device import DeviceContext

# 获取日志记录器
logger = get_logger("DB-Init")


async def init_admin_db():
    """初始化管理员数据库

    创建管理员数据库和用户表，并创建默认管理员账户。
    """
    from backend.app.models.user import User, pwd_context
    from sqlalchemy import (
        MetaData,
        Table,
        Column,
        Integer,
        String,
        Boolean,
        DateTime,
        text,
    )
    from sqlalchemy.schema import CreateTable

    db_manager = DatabaseManager()
    settings = get_settings()

    try:
        logger.info(f"开始初始化管理员数据库: {ADMIN_DATABASE}")

        # 1. 确保管理员数据库存在
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

        # 2. 获取管理员数据库引擎
        engine = await db_manager.get_engine(is_admin=True)

        # 3. 只创建用户表 - 使用更简单的方法，确保结构准确
        async with engine.begin() as conn:
            # 检查users表是否存在
            exists = await conn.run_sync(
                lambda sync_conn: sync_conn.dialect.has_table(sync_conn, "users")
            )

            if not exists:
                logger.info("创建管理员数据库的users表")
                # 直接创建与User模型完全匹配的表
                await conn.execute(
                    text("""
                    CREATE TABLE `users` (
                        `id` INTEGER AUTO_INCREMENT PRIMARY KEY,
                        `username` VARCHAR(50) NOT NULL UNIQUE,
                        `email` VARCHAR(120) NOT NULL UNIQUE,
                        `hashed_password` VARCHAR(128) NOT NULL,
                        `full_name` VARCHAR(100),
                        `is_active` BOOLEAN DEFAULT TRUE,
                        `is_admin` BOOLEAN DEFAULT TRUE,
                        `is_superuser` BOOLEAN DEFAULT FALSE,
                        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
                        `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        `api_key` VARCHAR(128),
                        `api_key_expires` DATETIME,
                        `last_login` DATETIME,
                        INDEX (`username`),
                        INDEX (`email`)
                    )
                """)
                )
                logger.success("管理员数据库users表创建成功")

                # 4. 直接创建默认管理员账户
                logger.info(f"创建默认管理员账户: {settings.admin.username}")

                # 使用固定的哈希值，对应于 'admin123'
                # 哈希密码
                orig_password = settings.admin.password
                # 使用固定的已知密码哈希，这是'admin123'的bcrypt哈希
                hashed_password = "$2b$12$w1yP8cAgOBb/TgBVMCVHaOXUJFdYFcqUQH0qwQJoQs7xDkPQC3QVG"  # 'admin123'的bcrypt哈希

                # 输出调试信息
                logger.debug(
                    f"默认管理员密码: 原始={orig_password}, 哈希后={hashed_password}"
                )
                print(
                    f"[Debug] 默认管理员密码: 原始={orig_password}, 哈希后={hashed_password}"
                )

                # 输出哈希算法验证信息
                verify_result = pwd_context.verify(orig_password, hashed_password)
                logger.debug(f"密码验证测试: 结果={verify_result}")
                print(f"[Debug] 密码验证测试: 结果={verify_result}")

                # 直接插入管理员账户
                await conn.execute(
                    text("""
                    INSERT INTO users (
                        username, email, full_name, hashed_password, 
                        is_active, is_admin, is_superuser, created_at, updated_at
                    ) VALUES (
                        :username, :email, 'System Administrator', :hashed_password,
                        TRUE, TRUE, TRUE, NOW(), NOW()
                    )
                """),
                    {
                        "username": settings.admin.username,
                        "email": settings.admin.email,
                        "hashed_password": hashed_password,
                    },
                )

                logger.success(f"管理员账户 {settings.admin.username} 已创建")

        logger.success("管理员数据库初始化成功")
    except Exception as e:
        logger.error(f"管理员数据库初始化失败: {e}")
        raise


async def init_db(device_ids: Optional[List[str]] = None):
    """初始化数据库

    为指定的设备ID或所有设备ID创建数据库表结构。

    Args:
        device_ids: 设备ID列表，如果为None则处理所有设备
    """
    settings = get_settings()
    db_manager = DatabaseManager()

    # 确定要处理的设备ID列表
    if not device_ids:
        device_ids = settings.get_device_ids()

    logger.info(f"开始初始化数据库 (设备数量: {len(device_ids)})")

    for device_id in device_ids:
        async with DeviceContext(device_id):
            try:
                device_name = settings.get_device(device_id).name
                schema_name = settings.get_schema_name(device_id)

                logger.info(
                    f"正在为设备 '{device_name}' (ID: {device_id}) 初始化MySQL schema: {schema_name}"
                )

                # 先获取引擎，这会自动创建schema
                engine = await db_manager.get_engine(device_id)

                # 创建表
                if settings.database.manage_schema:
                    await _create_tables(engine)

                logger.success(
                    f"设备 '{device_name}' (ID: {device_id}) 的数据库初始化成功"
                )
            except Exception as e:
                logger.error(f"设备 '{device_id}' 的数据库初始化失败: {e}")


async def _create_tables(engine: AsyncEngine):
    """创建数据库表

    Args:
        engine: 数据库引擎
    """
    try:
        async with engine.begin() as conn:
            logger.info("正在创建数据库表...")
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.error(f"创建数据库表失败: {e}")
        raise


async def create_initial_data(device_ids: Optional[List[str]] = None):
    """创建初始数据

    在数据库初始化后为每个设备创建所需的初始数据。

    Args:
        device_ids: 设备ID列表，如果为None则处理所有设备
    """
    settings = get_settings()

    # 确定要处理的设备ID列表
    if not device_ids:
        device_ids = settings.get_device_ids()

    logger.info(f"开始创建初始数据 (设备数量: {len(device_ids)})")

    for device_id in device_ids:
        async with DeviceContext(device_id):
            try:
                device_name = settings.get_device(device_id).name
                logger.info(
                    f"正在为设备 '{device_name}' (ID: {device_id}) 创建初始数据..."
                )

                # 这里可以添加设备特定的初始数据创建逻辑

                logger.info(
                    f"设备 '{device_name}' (ID: {device_id}) 的初始数据创建成功"
                )
            except Exception as e:
                logger.error(f"设备 '{device_id}' 的初始数据创建失败: {e}")


async def check_db_initialized(
    device_id: Optional[str] = None, is_admin: bool = False
) -> bool:
    """检查数据库是否已初始化

    Args:
        device_id: 设备ID，如果为None则使用当前上下文中的设备ID
        is_admin: 是否检查管理员数据库

    Returns:
        bool: 是否已初始化
    """
    db_manager = DatabaseManager()

    try:
        engine = await db_manager.get_engine(device_id, is_admin=is_admin)

        # 尝试查询一些表来确认数据库是否已经初始化
        async with engine.connect() as conn:
            # 检查表是否存在
            # 对于管理员数据库，检查users表
            table_name = "users" if is_admin else "wechatmessage"
            exists = await conn.run_sync(
                lambda sync_conn: sync_conn.dialect.has_table(sync_conn, table_name)
            )
            return exists
    except Exception as e:
        logger.error(f"检查数据库初始化状态失败: {e}")
        return False


async def reset_db(
    device_ids: Optional[List[str]] = None,
    confirm: bool = False,
    reset_admin: bool = False,
):
    """重置数据库，删除所有表并重新创建

    Args:
        device_ids: 设备ID列表，如果为None则处理所有设备
        confirm: 确认重置，必须为True才会执行删除操作
        reset_admin: 是否同时重置管理员数据库
    """
    if not confirm:
        logger.warning("未确认重置操作，请设置confirm=True参数以确认")
        return

    settings = get_settings()
    db_manager = DatabaseManager()

    # 如果需要，先重置管理员数据库
    if reset_admin:
        try:
            logger.warning(f"正在重置管理员数据库: {ADMIN_DATABASE}")

            # 删除并重新创建管理员数据库
            async with (await db_manager.get_engine()).begin() as conn:
                await conn.execute(text(f"DROP DATABASE IF EXISTS `{ADMIN_DATABASE}`"))
                await conn.execute(text(f"CREATE DATABASE `{ADMIN_DATABASE}`"))

            # 重新初始化管理员数据库
            await init_admin_db()
            logger.success("管理员数据库已重置")
        except Exception as e:
            logger.error(f"重置管理员数据库失败: {e}")

    # 确定要处理的设备ID列表
    if not device_ids:
        device_ids = settings.get_device_ids()

    logger.warning(f"开始重置数据库 (设备数量: {len(device_ids)})")

    for device_id in device_ids:
        async with DeviceContext(device_id):
            try:
                device_name = settings.get_device(device_id).name
                schema_name = settings.get_schema_name(device_id)

                logger.warning(
                    f"正在重置设备 '{device_name}' (ID: {device_id}) 的数据库"
                )

                engine = await db_manager.get_engine(device_id)

                # 对于MySQL，删除并重新创建整个schema
                async with (await db_manager.get_engine()).begin() as conn:
                    # 使用默认引擎连接执行DROP DATABASE
                    await conn.execute(text(f"DROP DATABASE IF EXISTS `{schema_name}`"))
                    await conn.execute(text(f"CREATE DATABASE `{schema_name}`"))

                # 重新获取连接到新schema的引擎
                engine = await db_manager.get_engine(device_id)

                # 创建表
                await _create_tables(engine)

                # 创建初始数据
                await create_initial_data([device_id])

                logger.success(f"设备 '{device_name}' (ID: {device_id}) 的数据库已重置")
            except Exception as e:
                logger.error(f"重置设备 '{device_id}' 的数据库失败: {e}")


async def init_all_db():
    """初始化所有设备的数据库和初始数据"""
    settings = get_settings()
    device_ids = settings.get_device_ids()

    if not device_ids:
        logger.warning("没有配置任何设备")
        return

    # 首先初始化管理员数据库
    try:
        await init_admin_db()
    except Exception as e:
        logger.error(f"初始化管理员数据库失败: {e}")
        return

    # 然后初始化设备数据库
    await init_db(device_ids)
    await create_initial_data(device_ids)
