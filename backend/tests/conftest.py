"""
pytest 配置文件，包含共享的 fixtures
"""

from app.models.admin import Admin
from app.core.security import security_manager
from app.core.bases import AdminBase
from app.core.config import Settings
import os
import sys
from typing import AsyncGenerator, Generator
from datetime import datetime, timezone
from pathlib import Path

# 导入 toml 解析器（兼容不同 Python 版本）
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Python < 3.11

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_test_config():
    """加载测试配置文件"""
    # 尝试按优先级加载配置文件
    config_paths = [
        Path(__file__).parent / "test_config.toml",  # tests目录下
        Path(__file__).parent.parent / "test_config.toml",  # backend目录下
        Path(os.environ.get("TEST_CONFIG_PATH", ""))  # 环境变量指定的路径
    ]

    for config_path in config_paths:
        if config_path.exists():
            with open(config_path, "rb") as f:
                return tomllib.load(f)

    # 如果没有找到配置文件，使用默认配置（向后兼容）
    print("警告：未找到 test_config.toml 文件，使用默认测试配置")
    print("建议：复制 test_config.example.toml 为 test_config.toml 并修改配置")

    return {
        "test_database": {
            "type": "mysql",
            "host": "localhost",
            "port": 3306,
            "username": "root",
            "password": "wangnov1",
            "database": "opengewe_test",
            "echo_sql": False
        },
        "test_redis": {
            "host": "localhost",
            "port": 6379,
            "db": 1
        },
        "test_auth": {
            "secret_key": "test-secret-key-for-testing-only",
            "jwt_expiration_hours": 1
        },
        "test_settings": {
            "debug": True
        }
    }


# 测试专用配置
class TestSettings(Settings):
    """测试环境配置"""

    def __init__(self):
        # 加载测试配置
        config = load_test_config()

        # 数据库配置
        db_config = config["test_database"]
        database_url = f"mysql+aiomysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

        # Redis配置
        redis_config = config["test_redis"]
        redis_password = f":{redis_config.get('password')}@" if redis_config.get(
            'password') else ""
        redis_url = f"redis://{redis_password}{redis_config['host']}:{redis_config['port']}/{redis_config['db']}"

        # 认证配置
        auth_config = config["test_auth"]

        # 初始化父类
        super().__init__(
            database_url=database_url,
            secret_key=auth_config["secret_key"],
            jwt_expiration_hours=auth_config["jwt_expiration_hours"],
            debug=config["test_settings"]["debug"],
            redis_url=redis_url,
        )

        # 存储测试数据库配置（供其他地方使用）
        self.db_config = db_config


# 移除自定义 event_loop fixture，使用 pytest-asyncio 的默认行为
# pytest-asyncio 会自动为每个异步测试创建事件循环


@pytest.fixture
def test_settings():
    """测试配置"""
    return TestSettings()


@pytest_asyncio.fixture
async def test_db_engine(test_settings):
    """创建测试数据库引擎"""
    # 确保测试数据库存在
    await ensure_test_database_exists(test_settings)

    # 创建引擎
    engine = create_async_engine(
        test_settings.database_url,
        echo=False,
        future=True,
    )

    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(AdminBase.metadata.create_all)

    yield engine

    # 清理：删除所有表
    async with engine.begin() as conn:
        await conn.run_sync(AdminBase.metadata.drop_all)

    await engine.dispose()


async def ensure_test_database_exists(settings: TestSettings):
    """确保测试数据库存在"""
    import aiomysql

    db_config = settings.db_config
    connection = await aiomysql.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["username"],
        password=db_config["password"],
        autocommit=True
    )

    try:
        cursor = await connection.cursor()

        # 删除并重新创建测试数据库
        await cursor.execute(f"DROP DATABASE IF EXISTS `{db_config['database']}`")
        await cursor.execute(
            f"CREATE DATABASE `{db_config['database']}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )

        await cursor.close()
    finally:
        connection.close()


@pytest_asyncio.fixture
async def test_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """创建测试数据库会话"""
    session_maker = async_sessionmaker(
        bind=test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
def test_client(test_settings, test_db_engine) -> Generator[TestClient, None, None]:
    """创建同步测试客户端"""
    # 创建一个新的应用实例用于测试
    from main import create_app
    from app.core.config import get_settings
    from app.core.session_manager import get_admin_session

    # 创建测试应用
    test_app = create_app()

    # 覆盖依赖
    test_app.dependency_overrides[get_settings] = lambda: test_settings

    # 为测试创建专用的session管理器
    test_session_maker = async_sessionmaker(
        bind=test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def override_get_admin_session():
        async with test_session_maker() as session:
            yield session

    test_app.dependency_overrides[get_admin_session] = override_get_admin_session

    with TestClient(test_app) as client:
        yield client

    # 清理
    test_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(test_settings, test_db_engine) -> AsyncGenerator[AsyncClient, None]:
    """创建异步测试客户端"""
    from main import create_app
    from app.core.config import get_settings
    from app.core.session_manager import session_manager, get_admin_session

    # 创建测试应用
    test_app = create_app()

    # 覆盖依赖
    test_app.dependency_overrides[get_settings] = lambda: test_settings

    # 为测试创建专用的session管理器
    test_session_maker = async_sessionmaker(
        bind=test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def override_get_admin_session():
        async with test_session_maker() as session:
            yield session

    test_app.dependency_overrides[get_admin_session] = override_get_admin_session

    # 初始化session管理器（用于测试）
    await session_manager.initialize()
    session_manager._engines["admin_data"] = test_db_engine
    session_manager._session_makers["admin_data"] = test_session_maker

    # 使用 ASGITransport 创建 AsyncClient
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # 清理
    test_app.dependency_overrides.clear()
    await session_manager.close_all()


@pytest_asyncio.fixture
async def test_user(test_session: AsyncSession) -> Admin:
    """创建测试用户"""
    user = Admin(
        username="testuser",
        hashed_password=security_manager.get_password_hash("testpassword123"),
        full_name="Test User",
        is_superadmin=False,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def test_superadmin(test_session: AsyncSession) -> Admin:
    """创建测试超级管理员"""
    admin = Admin(
        username="testadmin",
        hashed_password=security_manager.get_password_hash("adminpassword123"),
        full_name="Test Admin",
        is_superadmin=True,
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    test_session.add(admin)
    await test_session.commit()
    await test_session.refresh(admin)

    return admin


@pytest.fixture
def auth_headers(test_user: Admin) -> dict:
    """创建认证请求头"""
    token_data = {
        "sub": str(test_user.id),
        "username": test_user.username,
        "is_superadmin": test_user.is_superadmin,
    }
    access_token = security_manager.create_access_token(token_data)

    return {
        "Authorization": f"Bearer {access_token}"
    }


@pytest.fixture
def admin_auth_headers(test_superadmin: Admin) -> dict:
    """创建超级管理员认证请求头"""
    token_data = {
        "sub": str(test_superadmin.id),
        "username": test_superadmin.username,
        "is_superadmin": test_superadmin.is_superadmin,
    }
    access_token = security_manager.create_access_token(token_data)

    return {
        "Authorization": f"Bearer {access_token}"
    }


@pytest.fixture(autouse=True)
def clear_rate_limiter():
    """自动清理速率限制器的状态"""
    from app.core.security import rate_limiter
    # 每个测试前清理
    rate_limiter.attempts.clear()
    yield
    # 每个测试后也清理
    rate_limiter.attempts.clear()


# 配置 pytest-asyncio
pytest_plugins = ('pytest_asyncio',)
