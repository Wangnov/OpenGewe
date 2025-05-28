"""
应用配置管理
"""

import os
import shutil
from functools import lru_cache
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from opengewe.logger import init_default_logger, get_logger

init_default_logger()
logger = get_logger(__name__)
try:
    import tomllib
except ImportError:
    import tomli as tomllib


def ensure_config_file() -> str:
    """确保配置文件存在，如果不存在则复制示例文件"""
    config_path = "main_config.toml"
    example_path = "main_config_example.toml"

    # 从webpanel目录向上查找配置文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

    config_file = os.path.join(project_root, config_path)
    example_file = os.path.join(project_root, example_path)

    if not os.path.exists(config_file):
        if os.path.exists(example_file):
            shutil.copy2(example_file, config_file)
            logger.info(f"配置文件不存在，已从 {example_path} 复制到 {config_path}")
        else:
            raise FileNotFoundError(
                f"配置文件 {config_path} 和示例文件 {example_path} 都不存在"
            )

    return config_file


def load_toml_config() -> dict:
    """加载TOML配置文件"""
    config_file = ensure_config_file()

    try:
        with open(config_file, "rb") as f:
            config = tomllib.load(f)
            return config
    except Exception as e:
        logger.info(f"加载配置文件失败: {e}")
        return {}


def validate_mysql_config(db_config: dict) -> None:
    """验证MySQL配置的完整性"""
    required_fields = ["host", "port", "username", "password", "database"]
    missing_fields = [field for field in required_fields if not db_config.get(field)]

    if missing_fields:
        raise ValueError(
            f"MySQL配置缺失必要字段: {', '.join(missing_fields)}。"
            f"请在配置文件的[webpanel.database]部分设置这些字段。"
        )


def build_database_url(db_config: dict) -> str:
    """根据配置构建数据库URL - 仅支持MySQL"""
    db_type = db_config.get("type", "mysql")

    if db_type == "sqlite":
        raise ValueError(
            "不支持SQLite数据库。此项目需要schema支持，请使用MySQL数据库。"
            "请在配置文件中将[webpanel.database]的type设置为'mysql'并提供相应的连接信息。"
        )
    elif db_type == "mysql":
        # 验证MySQL配置
        validate_mysql_config(db_config)

        username = db_config["username"]
        password = db_config["password"]
        host = db_config["host"]
        port = db_config["port"]
        database = db_config["database"]

        return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
    else:
        raise ValueError(
            f"不支持的数据库类型: {db_type}。仅支持MySQL数据库。"
            "请在配置文件中将[webpanel.database]的type设置为'mysql'。"
        )


async def ensure_database_exists(db_config: dict) -> None:
    """确保MySQL数据库存在，如果不存在则创建"""
    import aiomysql

    # 验证配置
    validate_mysql_config(db_config)

    host = db_config["host"]
    port = db_config["port"]
    username = db_config["username"]
    password = db_config["password"]
    database = db_config["database"]

    try:
        # 先连接到MySQL服务器（不指定数据库）
        connection = await aiomysql.connect(
            host=host, port=port, user=username, password=password, autocommit=True
        )

        try:
            cursor = await connection.cursor()

            # 检查数据库是否存在
            await cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
                (database,),
            )
            result = await cursor.fetchone()

            if not result:
                # 数据库不存在，创建它
                logger.info(f"数据库 '{database}' 不存在，正在创建...")
                await cursor.execute(
                    f"CREATE DATABASE `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
                logger.info(f"数据库 '{database}' 创建成功")
            else:
                logger.info(f"数据库 '{database}' 已存在")

            await cursor.close()
        finally:
            connection.close()

    except Exception as e:
        raise RuntimeError(
            f"无法连接到MySQL服务器或创建数据库: {e}。"
            f"请确保：\n"
            f"1. MySQL服务器运行正常\n"
            f"2. 连接信息正确 (host={host}, port={port}, user={username})\n"
            f"3. 用户具有创建数据库的权限"
        )


def build_redis_url(redis_config: dict) -> str:
    """根据配置构建Redis URL"""
    host = redis_config.get("host", "localhost")
    port = redis_config.get("port", 6379)
    db = redis_config.get("db", 0)
    password = redis_config.get("password")

    if password:
        return f"redis://:{password}@{host}:{port}/{db}"
    else:
        return f"redis://{host}:{port}/{db}"


class Settings(BaseSettings):
    """应用配置类"""

    # 应用基础配置
    app_name: str = "OpenGewe WebPanel"
    app_version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 5432

    # 安全配置
    secret_key: str = "default-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    password_min_length: int = 8
    max_login_attempts: int = 5

    # 管理员配置
    admin_username: str = "admin"
    admin_password: str = "admin@123"

    # 时区配置
    timezone: str = "Asia/Shanghai"
    use_local_timezone: bool = True

    # 数据库配置 - 强制使用MySQL
    database_url: str = (
        "mysql+aiomysql://opengewe:opengewe123@localhost:3306/opengewe_webpanel"
    )
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_echo_sql: bool = False  # 是否打印SQL语句到控制台

    # Redis配置
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 10

    # CORS配置（硬编码）
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]

    # WebSocket配置
    websocket_heartbeat_interval: int = 30

    # OpenGewe配置
    opengewe_log_level: str = "INFO"
    opengewe_log_path: str = "./logs"

    # Webhook配置
    webhook_ip_whitelist: Optional[List[str]] = None
    webhook_verify_signature: bool = True

    # 数据库配置存储（用于数据库创建）
    db_config: Optional[dict] = None

    def __init__(self, **kwargs):
        # 加载TOML配置
        toml_config = load_toml_config()
        webpanel_config = toml_config.get("webpanel", {})

        # 基础配置
        for key in [
            "secret_key",
            "debug",
            "host",
            "port",
            "timezone",
            "use_local_timezone",
            "admin_username",
            "admin_password",
        ]:
            if key in webpanel_config:
                kwargs.setdefault(key, webpanel_config[key])

                # 验证并构建数据库URL
        if "database" in webpanel_config:
            db_config = webpanel_config["database"]

            # 检查是否尝试使用sqlite
            if db_config.get("type") == "sqlite":
                raise ValueError(
                    "不支持SQLite数据库。此项目需要schema支持，请使用MySQL数据库。\n"
                    "请在main_config.toml的[webpanel.database]部分设置MySQL连接信息：\n"
                    'type = "mysql"\n'
                    'host = "localhost"\n'
                    "port = 3306\n"
                    'username = "your_username"\n'
                    'password = "your_password"\n'
                    'database = "opengewe_webpanel"'
                )

            try:
                database_url = build_database_url(db_config)
                kwargs.setdefault("database_url", database_url)

                # 处理SQL日志配置
                if "echo_sql" in db_config:
                    kwargs.setdefault("database_echo_sql", db_config["echo_sql"])

                # 存储数据库配置以便后续使用
                kwargs.setdefault("db_config", db_config)
            except ValueError as e:
                raise ValueError(f"数据库配置错误: {e}")
        else:
            logger.info("警告: 未找到数据库配置，使用默认MySQL配置")
            # 设置默认的数据库配置
            default_db_config = {
                "type": "mysql",
                "host": "localhost",
                "port": 3306,
                "username": "opengewe",
                "password": "opengewe123",
                "database": "opengewe_webpanel",
            }
            kwargs.setdefault("db_config", default_db_config)

        # 构建Redis URL
        if "redis" in webpanel_config:
            redis_url = build_redis_url(webpanel_config["redis"])
            kwargs.setdefault("redis_url", redis_url)

        super().__init__(**kwargs)

    async def ensure_database_ready(self) -> None:
        """确保数据库准备就绪"""
        await ensure_database_exists(self.db_config)

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, v):
        if isinstance(v, str):
            return [v]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """获取应用配置（单例模式）"""
    return Settings()


def get_gewe_apps_config() -> dict:
    """获取GeWe应用配置"""
    toml_config = load_toml_config()
    return toml_config.get("gewe_apps", {})
