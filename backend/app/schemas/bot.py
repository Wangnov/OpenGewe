"""
机器人相关的Pydantic schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class BotBase(BaseModel):
    """机器人基础模型"""

    gewe_app_id: str = Field(
        ..., min_length=1, max_length=100, description="GeWe应用ID"
    )
    gewe_token: str = Field(..., min_length=1, max_length=255, description="GeWe Token")
    callback_url_override: Optional[str] = Field(
        None, max_length=500, description="回调URL覆盖"
    )


class BotCreateRequest(BotBase):
    """创建机器人请求"""

    @field_validator("gewe_app_id")
    @classmethod
    def validate_gewe_app_id(cls, v):
        """验证GeWe应用ID格式"""
        v = v.strip()
        if not v:
            raise ValueError("GeWe应用ID不能为空")
        return v

    @field_validator("gewe_token")
    @classmethod
    def validate_gewe_token(cls, v):
        """验证GeWe Token格式"""
        v = v.strip()
        if not v:
            raise ValueError("GeWe Token不能为空")
        return v


class BotUpdateRequest(BaseModel):
    """更新机器人请求"""

    gewe_token: Optional[str] = Field(
        None, min_length=1, max_length=255, description="GeWe Token"
    )
    callback_url_override: Optional[str] = Field(
        None, max_length=500, description="回调URL覆盖"
    )
    is_online: Optional[bool] = Field(None, description="在线状态")


class BotResponse(BaseModel):
    """机器人响应"""

    gewe_app_id: str = Field(..., description="GeWe应用ID")
    nickname: Optional[str] = Field(None, description="昵称")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    big_head_img_url: Optional[str] = Field(None, description="大头像URL")
    small_head_img_url: Optional[str] = Field(None, description="小头像URL")
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

    gewe_app_id: str = Field(..., description="GeWe应用ID")
    is_online: bool = Field(..., description="是否在线")
    last_seen_at: Optional[datetime] = Field(None, description="最后在线时间")
    message_count_24h: int = Field(0, description="24小时消息数量")
    contact_count: int = Field(0, description="联系人数量")
    group_count: int = Field(0, description="群聊数量")


class ContactResponse(BaseModel):
    """联系人响应"""

    id: int = Field(..., description="联系人ID")
    gewe_app_id: str = Field(..., description="GeWe应用ID")
    contact_wxid: str = Field(..., description="联系人微信ID")
    contact_type: str = Field(..., description="联系人类型")
    nickname: Optional[str] = Field(None, description="昵称")
    remark: Optional[str] = Field(None, description="备注")
    alias: Optional[str] = Field(None, description="别名")
    big_head_img_url: Optional[str] = Field(None, description="大头像URL")
    small_head_img_url: Optional[str] = Field(None, description="小头像URL")
    signature: Optional[str] = Field(None, description="个性签名")
    sex: Optional[int] = Field(None, description="性别（0-未知, 1-男, 2-女）")
    country: Optional[str] = Field(None, description="国家")
    province: Optional[str] = Field(None, description="省份")
    city: Optional[str] = Field(None, description="城市")
    is_deleted: bool = Field(..., description="是否已删除")
    last_updated: datetime = Field(..., description="最后更新时间")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True


class GroupMemberResponse(BaseModel):
    """群成员响应"""

    id: int = Field(..., description="群成员ID")
    gewe_app_id: str = Field(..., description="GeWe应用ID")
    group_wxid: str = Field(..., description="群聊微信ID")
    member_wxid: str = Field(..., description="成员微信ID")
    nickname: Optional[str] = Field(None, description="昵称")
    display_name: Optional[str] = Field(None, description="群内显示名")
    big_head_img_url: Optional[str] = Field(None, description="大头像URL")
    small_head_img_url: Optional[str] = Field(None, description="小头像URL")
    is_admin: bool = Field(..., description="是否为群管理员")
    is_owner: bool = Field(..., description="是否为群主")
    join_time: Optional[datetime] = Field(None, description="加入时间")
    is_active: bool = Field(..., description="是否活跃")
    last_updated: datetime = Field(..., description="最后更新时间")

    class Config:
        from_attributes = True


class BotPluginResponse(BaseModel):
    """机器人插件响应"""

    id: int = Field(..., description="插件配置ID")
    gewe_app_id: str = Field(..., description="GeWe应用ID")
    plugin_name: str = Field(..., description="插件名称")
    is_enabled: bool = Field(..., description="是否启用")
    config_json: Optional[str] = Field(None, description="配置JSON")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True


class SnsPostResponse(BaseModel):
    """朋友圈响应"""

    id: int = Field(..., description="朋友圈ID")
    gewe_app_id: str = Field(..., description="GeWe应用ID")
    sns_id: int = Field(..., description="朋友圈消息ID")
    author_wxid: str = Field(..., description="作者微信ID")
    content: Optional[str] = Field(None, description="内容")
    media_urls: Optional[str] = Field(None, description="媒体URL（JSON格式）")
    post_type: str = Field(..., description="朋友圈类型")
    like_count: int = Field(..., description="点赞数")
    comment_count: int = Field(..., description="评论数")
    create_time: datetime = Field(..., description="创建时间")
    privacy_settings: Optional[str] = Field(None, description="隐私设置（JSON格式）")
    raw_data: Optional[str] = Field(None, description="原始数据（JSON格式）")

    class Config:
        from_attributes = True


class WebhookPayload(BaseModel):
    """Webhook负载模型"""

    Appid: Optional[str] = Field(None, min_length=1, description="应用ID")
    TypeName: Optional[str] = Field(None, min_length=1, description="类型名称")
    Data: Optional[dict] = Field(None, description="数据内容")

    # GeWeAPI测试消息字段
    testMsg: Optional[str] = Field(None, description="测试消息内容")
    token: Optional[str] = Field(None, description="测试消息token")

    @field_validator("Appid")
    @classmethod
    def validate_appid(cls, v):
        """验证应用ID格式"""
        if v is not None:
            v = v.strip() if v else ""
            if not v:
                raise ValueError("应用ID不能为空")
        return v

    def is_test_message(self) -> bool:
        """判断是否为测试消息"""
        return self.testMsg is not None and self.token is not None

    def is_normal_message(self) -> bool:
        """判断是否为正常消息"""
        return (
            self.Appid is not None
            and self.TypeName is not None
            and self.Data is not None
        )


class RawCallbackLogResponse(BaseModel):
    """原始回调日志响应"""

    id: int = Field(..., description="消息ID")
    received_at: datetime = Field(..., description="接收时间")
    gewe_appid: str = Field(..., description="GeWe应用ID")
    type_name: str = Field(..., description="消息类型")
    msg_id: Optional[str] = Field(None, description="消息ID")
    new_msg_id: Optional[str] = Field(None, description="新消息ID")
    from_wxid: Optional[str] = Field(None, description="发送者微信ID")
    to_wxid: Optional[str] = Field(None, description="接收者微信ID")
    raw_json_data: str = Field(..., description="原始JSON数据")
    processed: bool = Field(..., description="是否已处理")

    class Config:
        from_attributes = True
