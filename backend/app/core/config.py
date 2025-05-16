"""
配置管理模块
用于加载和验证应用程序的配置

此模块提供从TOML文件加载配置，并通过Pydantic进行数据验证
"""

from functools import lru_cache
import os
from typing import List, Dict, Any, Optional, Union, Set

import tomli
from pydantic import BaseModel, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """数据库配置模型"""

    mysql_host: str
    mysql_port: int = 3306
    mysql_user: str
    mysql_password: str
    mysql_database_prefix: str = "opengewe_"
    auto_create_schema: bool = True
    manage_schema: bool = True
    connect_args: Dict[str, Any] = {}

    def get_connection_string(self, schema_name: Optional[str] = None) -> str:
        """根据配置生成数据库连接字符串

        Args:
            schema_name: 可选的schema名称

        Returns:
            str: 数据库连接字符串
        """
        # 使用给定的schema或默认数据库
        db_name = schema_name or "mysql"
        return f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{db_name}"


class DeviceSettings(BaseModel):
    """单个设备的配置模型"""

    name: str
    base_url: str
    download_url: str = ""
    callback_url: str = ""
    app_id: str
    token: str
    is_gewe: bool = True


class DevicesSettings(BaseModel):
    """所有设备的配置模型"""

    __root__: Dict[str, DeviceSettings]

    def __init__(self, **data):
        # 处理从TOML读取的嵌套结构
        devices_data = data.get("devices", {})
        super().__init__(__root__=devices_data)

    def __getitem__(self, key: str) -> DeviceSettings:
        """通过设备ID获取设备配置"""
        if key in self.__root__:
            return self.__root__[key]
        raise KeyError(f"设备ID '{key}' 不存在")

    def get(self, key: str, default=None) -> Optional[DeviceSettings]:
        """安全地获取设备配置"""
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self) -> Set[str]:
        """获取所有设备ID"""
        return set(self.__root__.keys())

    def items(self):
        """获取所有设备ID和配置"""
        return self.__root__.items()

    def get_default_device_id(self) -> str:
        """获取默认设备ID"""
        # 优先使用名为'default'的设备
        if "default" in self.__root__:
            return "default"
        # 或使用第一个设备
        if self.__root__:
            return next(iter(self.__root__))
        raise ValueError("无可用设备配置")


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
    devices: DevicesSettings = None  # 必填
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
            config_data = tomli.load(f)

        # 创建设置实例并存储原始配置数据
        settings = cls(**config_data)
        settings._config_data = config_data
        return settings

    def get_raw_config(self) -> Dict[str, Any]:
        """获取原始配置数据"""
        return self._config_data

    def get_device_ids(self) -> List[str]:
        """获取所有配置的设备ID"""
        return list(self.devices.keys())

    def get_device(self, device_id: Optional[str] = None) -> DeviceSettings:
        """获取指定设备配置，如果未指定则返回默认设备"""
        if not device_id:
            device_id = self.devices.get_default_device_id()
        return self.devices[device_id]

    def get_schema_name(self, device_id: str) -> str:
        """根据设备ID生成数据库schema名称"""
        # 去除非字母数字字符，避免SQL注入和非法schema名称
        safe_device_id = "".join(c for c in device_id if c.isalnum() or c == "_")
        return f"{self.database.mysql_database_prefix}{safe_device_id}"


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
