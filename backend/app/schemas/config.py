"""
配置管理相关的Pydantic schemas
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class ConfigUpdateRequest(BaseModel):
    """配置更新请求模型"""

    config: Dict[str, Any] = Field(
        ...,
        description="配置数据，必须是有效的JSON对象",
        example={"debug": True, "host": "0.0.0.0", "port": 5432},
    )


class ConfigSectionData(BaseModel):
    """配置段数据模型"""

    section_name: str = Field(..., description="配置段名称")
    config: Dict[str, Any] = Field(..., description="配置数据")


class ConfigSectionResponse(BaseModel):
    """配置段响应模型"""

    status: str = Field(..., description="响应状态")
    data: ConfigSectionData = Field(..., description="配置段数据")
    message: str = Field(..., description="响应消息")


class AllConfigsResponse(BaseModel):
    """所有配置响应模型"""

    status: str = Field(..., description="响应状态")
    data: Dict[str, Dict[str, Any]] = Field(..., description="所有配置段数据")
    message: str = Field(..., description="响应消息")


class MigrationStatusData(BaseModel):
    """迁移状态数据模型"""

    config_file_exists: bool = Field(..., description="配置文件是否存在")
    config_file_path: str = Field(..., description="配置文件路径")
    migrate_sections: List[str] = Field(..., description="需要迁移的配置段列表")
    sections_in_file: List[str] = Field(..., description="文件中存在的配置段")
    sections_in_db: List[str] = Field(..., description="数据库中存在的配置段")
    migrated_sections: List[str] = Field(..., description="已迁移的配置段")
    pending_sections: List[str] = Field(..., description="待迁移的配置段")
    error: Optional[str] = Field(None, description="错误信息")


class ConfigMigrationStatus(BaseModel):
    """配置迁移状态响应模型"""

    status: str = Field(..., description="响应状态")
    data: MigrationStatusData = Field(..., description="迁移状态数据")
    message: str = Field(..., description="响应消息")


class CacheStatusData(BaseModel):
    """缓存状态数据模型"""

    cached_sections: List[str] = Field(..., description="已缓存的配置段")
    cache_versions: Dict[str, int] = Field(..., description="缓存版本信息")
    cache_size: int = Field(..., description="缓存大小")


class CacheStatusResponse(BaseModel):
    """缓存状态响应模型"""

    status: str = Field(..., description="响应状态")
    data: CacheStatusData = Field(..., description="缓存状态数据")
    message: str = Field(..., description="响应消息")


class ConfigValidationResult(BaseModel):
    """配置验证结果模型"""

    valid: bool = Field(..., description="是否验证通过")
    error: Optional[str] = Field(None, description="验证错误信息")
    warnings: Optional[List[str]] = Field(None, description="验证警告信息")


class ConfigSectionInfo(BaseModel):
    """配置段信息模型"""

    section_name: str = Field(..., description="配置段名称")
    description: str = Field(..., description="配置段描述")
    supported: bool = Field(..., description="是否支持数据库存储")
    required_fields: Optional[List[str]] = Field(None, description="必需字段列表")

    class Config:
        json_schema_extra = {
            "example": {
                "section_name": "webpanel",
                "description": "Web面板配置，包含服务器设置、安全配置等",
                "supported": True,
                "required_fields": ["secret_key", "host", "port"],
            }
        }


class ConfigSectionsInfoResponse(BaseModel):
    """配置段信息响应模型"""

    status: str = Field(..., description="响应状态")
    data: List[ConfigSectionInfo] = Field(..., description="配置段信息列表")
    message: str = Field(..., description="响应消息")
