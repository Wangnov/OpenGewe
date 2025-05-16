"""Alembic环境配置

该文件配置Alembic如何连接到数据库以及如何运行迁移。
支持SQLAlchemy异步操作和多schema环境。
"""

import asyncio
import os
from logging.config import fileConfig
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

# 添加项目根目录到sys.path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# 引入模型基类
from backend.app.db.base import Base

# 确保所有模型都被导入到Base中
# 根据项目情况可能需要导入所有模型
import backend.app.models  # noqa

# 这是Alembic Config对象，它提供了访问alembic.ini设置的值
config = context.config

# 读取配置文件的logger配置
fileConfig(config.config_file_name)

# 设置MetaData对象以供Alembic使用
target_metadata = Base.metadata

# 开发过程中使用的默认URL
default_url = "mysql+aiomysql://root:123456@localhost:3306/dev"  # 默认使用本地mysql


def get_url():
    """获取数据库连接URL

    尝试从配置获取URL，如果失败则使用默认URL

    Returns:
        str: 数据库连接URL
    """
    try:
        from backend.app.core.config import get_settings
        from backend.app.core.device import DeviceContext

        settings = get_settings()
        device_id = settings.devices.get_default_device_id()
        schema_name = settings.get_schema_name(device_id)
        return settings.database.get_connection_string(schema_name)
    except Exception:
        # 如果配置获取失败，使用默认URL
        return os.getenv("DATABASE_URL", default_url)


def run_migrations_offline():
    """离线运行迁移

    此函数用于在不实际获取数据库连接的情况下生成迁移脚本。
    对于生成向版本控制系统提交的SQL脚本非常有用。
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """执行迁移

    Args:
        connection: 数据库连接对象
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """在线运行迁移

    此函数在实际连接到数据库的情况下运行迁移。
    支持异步操作。
    """
    # 获取URL
    url = get_url()

    # 替换配置中的URL
    config_section = config.get_section(config.config_ini_section)
    config_section["sqlalchemy.url"] = url

    # 创建引擎
    connectable = AsyncEngine(
        engine_from_config(
            config_section,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    # 执行迁移
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    # 关闭引擎
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # 使用asyncio运行异步迁移函数
    asyncio.run(run_migrations_online())
