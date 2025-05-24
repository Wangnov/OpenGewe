"""
机器人相关的Pydantic schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class BotBase(BaseModel):
    """机器人基础模型"""
    gewe_app_id: str = Field(..., min_length=1, max_length=100, description="GeWe应用ID")
    gewe_token: str = Field(..., min_length=1, max_length=255, description="GeWe Token")
    callback_url_override: Optional[str] = Field(None, max_length=500, description="回调URL覆盖")


class BotCreateRequest(BotBase):
    """创建机器人请求"""
    
    @field_validator('gewe_app_id')
    @classmethod
    def validate_gewe_app_id(cls, v):
        """验证GeWe应用ID格式"""
        v = v.strip()
        if not v:
            raise ValueError('GeWe应用ID不能为空')
        return v
    
    @field_validator('gewe_token')
    @classmethod
    def validate_gewe_token(cls, v):
        """验证GeWe Token格式"""
        v = v.strip()
        if not v:
            raise ValueError('GeWe Token不能为空')
        return v


class BotUpdateRequest(BaseModel):
    """更新机器人请求"""
    gewe_token: Optional[str] = Field(None, min_length=1, max_length=255, description="GeWe Token")
    callback_url_override: Optional[str] = Field(None, max_length=500, description="回调URL覆盖")
    is_online: Optional[bool] = Field(None, description="在线状态")


class BotResponse(BaseModel):
    """机器人响应"""
    bot_wxid: str = Field(..., description="机器人微信ID")
    gewe_app_id: str = Field(..., description="GeWe应用ID")
    nickname: Optional[str] = Field(None, description="昵称")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    qr_code_url: Optional[str] = Field(None, description="二维码URL")
    is_online: bool = Field(..., description="是否在线")
    last_seen_at: Optional[datetime] = Field(None, description="最后在线时间")
    callback_url_override: Optional[str] = Field(None, description="回调URL覆盖")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True


class BotListResponse(BaseModel):
    """机器人列表响应"""
    bots: list[BotResponse] = Field(..., description="机器人列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")


class BotStatusResponse(BaseModel):
    """机器人状态响应"""
    bot_wxid: str = Field(..., description="机器人微信ID")
    is_online: bool = Field(..., description="是否在线")
    last_seen_at: Optional[datetime] = Field(None, description="最后在线时间")
    message_count_24h: int = Field(0, description="24小时消息数量")
    contact_count: int = Field(0, description="联系人数量")
    group_count: int = Field(0, description="群聊数量")


class ContactResponse(BaseModel):
    """联系人响应"""
    id: int = Field(..., description="联系人ID")
    bot_wxid: str = Field(..., description="机器人微信ID")
    contact_wxid: str = Field(..., description="联系人微信ID")
    contact_type: str = Field(..., description="联系人类型")
    nickname: Optional[str] = Field(None, description="昵称")
    remark: Optional[str] = Field(None, description="备注")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    is_deleted: bool = Field(..., description="是否已删除")
    last_updated: datetime = Field(..., description="最后更新时间")
    
    class Config:
        from_attributes = True


class WebhookPayload(BaseModel):
    """Webhook负载模型"""
    Appid: str = Field(..., description="应用ID")
    TypeName: str = Field(..., description="类型名称")
    Data: dict = Field(..., description="数据内容")


class MessageResponse(BaseModel):
    """消息响应"""
    id: int = Field(..., description="消息ID")
    type_name: str = Field(..., description="消息类型")
    from_wxid: Optional[str] = Field(None, description="发送者微信ID")
    to_wxid: Optional[str] = Field(None, description="接收者微信ID")
    content: Optional[str] = Field(None, description="消息内容")
    received_at: datetime = Field(..., description="接收时间")
    processed: bool = Field(..., description="是否已处理")
    
    class Config:
        from_attributes = True 