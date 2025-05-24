"""
应用配置管理
"""
from functools import lru_cache
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import field_validator
try:
    import tomllib
except ImportError:
    import tomli as tomllib


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    app_name: str = "OpenGewe WebPanel"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # 安全配置
    secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    password_min_length: int = 8
    max_login_attempts: int = 5
    
    # 数据库配置
    database_url: str
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # Redis配置
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 10
    
    # CORS配置
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # WebSocket配置
    websocket_heartbeat_interval: int = 30
    
    # OpenGewe配置
    opengewe_log_level: str = "INFO"
    opengewe_log_path: str = "./logs"
    
    # Webhook配置
    webhook_ip_whitelist: Optional[List[str]] = None
    webhook_verify_signature: bool = True
    
    @field_validator('cors_origins')
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


def load_toml_config(config_path: str = "main_config.toml") -> dict:
    """加载TOML配置文件"""
    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        return {} 