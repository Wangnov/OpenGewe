"""
插件管理相关的Pydantic schemas
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PluginMetadata(BaseModel):
    """插件元数据模型"""
    name: str = Field(..., description="插件名称")
    description: Optional[str] = Field(None, description="插件描述")
    author: Optional[str] = Field("佚名", description="插件作者")
    version: Optional[str] = Field("未知", description="插件版本")
    readme: Optional[str] = Field(None, description="插件的README内容")
    config_schema: Optional[Dict[str, Any]] = Field(
        None, description="插件的默认配置（从config.toml读取）")


class GlobalPluginInfo(PluginMetadata):
    """全局插件信息模型（包含启用状态）"""
    plugin_id: str = Field(..., description="插件的唯一标识符（即文件夹名）")
    is_globally_enabled: bool = Field(..., description="是否全局启用")


class GlobalPluginInfoResponse(BaseModel):
    """获取所有全局插件信息的响应模型"""
    status: str = "success"
    data: List[GlobalPluginInfo]


class UpdateGlobalPluginRequest(BaseModel):
    """更新全局插件状态的请求模型"""
    is_globally_enabled: bool


class BotPluginConfig(BaseModel):
    """机器人特定插件配置"""
    is_enabled: bool = Field(True, description="该机器人是否启用此插件")
    config_json: Optional[Dict[str, Any]] = Field(
        None, description="该机器人的特定插件配置")


class MergedPluginConfigResponse(BaseModel):
    """合并后的插件配置响应模型"""
    status: str = "success"
    data: Dict[str, Any]
    message: str = "成功获取合并后的插件配置"
