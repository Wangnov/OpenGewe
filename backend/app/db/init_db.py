"""数据库初始化模块

提供数据库初始化、表创建和数据迁移功能，支持为每个设备创建独立的schema。
"""

import asyncio
from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DatabaseManager
from backend.app.core.config import get_settings
from backend.app.core.device import DeviceContext

# 获取日志记录器
logger = get_logger("DB-Init")


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


async def check_db_initialized(device_id: Optional[str] = None) -> bool:
    """检查数据库是否已初始化

    Args:
        device_id: 设备ID，如果为None则使用当前上下文中的设备ID

    Returns:
        bool: 是否已初始化
    """
    db_manager = DatabaseManager()

    try:
        engine = await db_manager.get_engine(device_id)

        # 尝试查询一些表来确认数据库是否已经初始化
        async with engine.connect() as conn:
            # 检查表是否存在
            # 这里以wechatmessages表为例
            exists = await conn.run_sync(
                lambda sync_conn: sync_conn.dialect.has_table(
                    sync_conn, "wechatmessage"
                )
            )
            return exists
    except Exception as e:
        logger.error(f"检查数据库初始化状态失败: {e}")
        return False


async def reset_db(device_ids: Optional[List[str]] = None, confirm: bool = False):
    """重置数据库，删除所有表并重新创建

    Args:
        device_ids: 设备ID列表，如果为None则处理所有设备
        confirm: 确认重置，必须为True才会执行删除操作
    """
    if not confirm:
        logger.warning("未确认重置操作，请设置confirm=True参数以确认")
        return

    settings = get_settings()
    db_manager = DatabaseManager()

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

    await init_db(device_ids)
    await create_initial_data(device_ids)
