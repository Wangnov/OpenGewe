"""
配置管理模块
用于加载和验证应用程序的配置

此模块提供从TOML文件加载配置，并通过Pydantic进行数据验证
"""

from functools import lru_cache
import os
from typing import List, Dict, Any, Optional, Union

import tomllib
from pydantic import BaseModel, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """数据库配置模型"""
    type: str = "sqlite"
    sqlite_file: str = "./backend.db"
    mysql_user: Optional[str] = None
    mysql_password: Optional[str] = None
    mysql_host: Optional[str] = None
    mysql_port: Optional[int] = 3306
    mysql_database: Optional[str] = None
    connect_args: Dict[str, Any] = {}
    
    @field_validator("type")
    def validate_db_type(cls, v):
        """验证数据库类型"""
        allowed = ["sqlite", "mysql"]
        if v not in allowed:
            raise ValueError(f"数据库类型必须是以下之一: {', '.join(allowed)}")
        return v
    
    @property
    def connection_string(self) -> str:
        """根据配置生成数据库连接字符串"""
        if self.type == "sqlite":
            return f"sqlite:///{self.sqlite_file}"
        elif self.type == "mysql":
            return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        return ""


class RedisSettings(BaseModel):
    """Redis配置模型"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str = ""
    prefix: str = "opengewe:"


class QueueSettings(BaseModel):
    """队列配置模型"""
    queue_type: str = "simple"
    broker: Optional[str] = None
    backend: Optional[str] = None
    name: str = "opengewe_messages"
    concurrency: int = 4
    
    @field_validator("queue_type")
    def validate_queue_type(cls, v):
        """验证队列类型"""
        allowed = ["simple", "advanced"]
        if v not in allowed:
            raise ValueError(f"队列类型必须是以下之一: {', '.join(allowed)}")
        return v


class GeweSettings(BaseModel):
    """Gewe API配置模型"""
    base_url: str
    download_url: str = ""
    callback_url: str = ""
    app_id: str = ""
    token: str = ""
    is_gewe: bool = True


class PluginsSettings(BaseModel):
    """插件配置模型"""
    plugins_dir: str = "plugins"
    enabled_plugins: List[str] = []
    disabled_plugins: List[str] = []


class LoggingSettings(BaseModel):
    """日志配置模型"""
    level: str = "INFO"
    format: str = "color"
    rotation: str = "500 MB"
    retention: str = "10 days"
    compression: str = "zip"
    path: str = "./logs"
    stdout: bool = True
    
    @field_validator("level")
    def validate_log_level(cls, v):
        """验证日志级别"""
        allowed = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"日志级别必须是以下之一: {', '.join(allowed)}")
        return v.upper()
    
    @field_validator("format")
    def validate_log_format(cls, v):
        """验证日志格式"""
        allowed = ["color", "json", "simple"]
        if v.lower() not in allowed:
            raise ValueError(f"日志格式必须是以下之一: {', '.join(allowed)}")
        return v.lower()


class BackendSettings(BaseModel):
    """后端服务配置模型"""
    host: str = "0.0.0.0"
    port: int = 5433
    debug: bool = False
    secret_key: str = "your-secret-key-here"
    cors_origins: List[Union[str, AnyHttpUrl]] = ["*"]
    enable_docs: bool = True
    docs_url: str = "/docs"
    enable_redis: bool = False
    enable_admin: bool = True


class Settings(BaseSettings):
    """应用程序总配置"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
    
    # 子配置部分
    backend: BackendSettings = BackendSettings()
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    queue: QueueSettings = QueueSettings()
    gewe: GeweSettings = None  # 必填
    plugins: PluginsSettings = PluginsSettings()
    logging: LoggingSettings = LoggingSettings()
    
    # 缓存的配置数据
    _config_data: Dict[str, Any] = {}
    
    @classmethod
    def from_toml(cls, toml_path: str = "main_config.toml") -> "Settings":
        """从TOML文件加载配置"""
        if not os.path.exists(toml_path):
            raise FileNotFoundError(f"配置文件 {toml_path} 不存在")
        
        with open(toml_path, "rb") as f:
            config_data = tomllib.load(f)
        
        # 创建设置实例并存储原始配置数据
        settings = cls(**config_data)
        settings._config_data = config_data
        return settings
    
    def get_raw_config(self) -> Dict[str, Any]:
        """获取原始配置数据"""
        return self._config_data


@lru_cache()
def get_settings(config_path: str = "main_config.toml") -> Settings:
    """
    获取应用程序配置的单例实例
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置实例
    """
    return Settings.from_toml(config_path) 