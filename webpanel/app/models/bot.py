"""
机器人相关数据模型
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Boolean, Text, DateTime, Integer, Enum, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
import enum

from ..core.database import Base


class ContactType(enum.Enum):
    """联系人类型枚举"""

    FRIEND = "friend"
    GROUP = "group"
    GH = "gh"
    WECHAT = "wechat"


class PostType(enum.Enum):
    """朋友圈类型枚举"""

    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    LINK = "link"
    FINDER = "finder"


class BotInfo(Base):
    """机器人信息表"""

    __tablename__ = "bot_info"

    bot_wxid: Mapped[str] = mapped_column(String(50), primary_key=True)
    gewe_app_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    gewe_token: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[Optional[str]] = mapped_column(String(100))
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    big_head_img_url: Mapped[Optional[str]] = mapped_column(Text)
    small_head_img_url: Mapped[Optional[str]] = mapped_column(Text)
    is_online: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    callback_url_override: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<BotInfo(bot_wxid='{self.bot_wxid}', nickname='{self.nickname}', gewe_app_id='{self.gewe_app_id}', gewe_token='{self.gewe_token}')>"


class RawCallbackLog(Base):
    """原始回调消息表"""

    __tablename__ = "raw_callback_log"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    received_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    bot_wxid: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    gewe_appid: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    type_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    msg_id: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    new_msg_id: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    from_wxid: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    to_wxid: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    raw_json_data: Mapped[str] = mapped_column(Text, nullable=False)  # JSON数据
    processed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    def __repr__(self) -> str:
        return f"<RawCallbackLog(bot_wxid='{self.bot_wxid}', type='{self.type_name}', raw_json_data='{self.raw_json_data}')>"


class Contact(Base):
    """联系人表"""

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    bot_wxid: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    gewe_app_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    contact_wxid: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    contact_type: Mapped[ContactType] = mapped_column(
        Enum(ContactType), nullable=False, index=True
    )
    nickname: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    remark: Mapped[Optional[str]] = mapped_column(String(200))
    alias: Mapped[Optional[str]] = mapped_column(String(100))
    big_head_img_url: Mapped[Optional[str]] = mapped_column(Text)
    small_head_img_url: Mapped[Optional[str]] = mapped_column(Text)
    signature: Mapped[Optional[str]] = mapped_column(Text)
    sex: Mapped[Optional[int]] = mapped_column(Integer)  # 0-未知, 1-男, 2-女
    country: Mapped[Optional[str]] = mapped_column(String(50))
    province: Mapped[Optional[str]] = mapped_column(String(50))
    city: Mapped[Optional[str]] = mapped_column(String(50))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<Contact(bot_wxid='{self.bot_wxid}', gewe_app_id='{self.gewe_app_id}', contact_wxid='{self.contact_wxid}', contact_type='{self.contact_type}', nickname='{self.nickname}')>"


class GroupMember(Base):
    """群成员表"""

    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    bot_wxid: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    gewe_app_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    group_wxid: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    member_wxid: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    nickname: Mapped[Optional[str]] = mapped_column(String(200))
    display_name: Mapped[Optional[str]] = mapped_column(String(200))
    big_head_img_url: Mapped[Optional[str]] = mapped_column(Text)
    small_head_img_url: Mapped[Optional[str]] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    is_owner: Mapped[bool] = mapped_column(Boolean, default=False)
    join_time: Mapped[Optional[datetime]] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<GroupMember(bot_wxid='{self.bot_wxid}', gewe_app_id='{self.gewe_app_id}', group_wxid='{self.group_wxid}', member_wxid='{self.member_wxid}', nickname='{self.nickname}')>"


class BotPlugin(Base):
    """机器人插件配置表"""

    __tablename__ = "bot_plugins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bot_wxid: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    gewe_app_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    plugin_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    config_json: Mapped[Optional[str]] = mapped_column(Text)  # JSON配置
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<BotPlugin(bot_wxid='{self.bot_wxid}', gewe_app_id='{self.gewe_app_id}', plugin_name='{self.plugin_name}')>"


class SnsPost(Base):
    """朋友圈记录表"""

    __tablename__ = "sns_posts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    bot_wxid: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    gewe_app_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    sns_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    author_wxid: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    content: Mapped[Optional[str]] = mapped_column(Text)
    media_urls: Mapped[Optional[str]] = mapped_column(Text)  # JSON数组
    post_type: Mapped[PostType] = mapped_column(
        Enum(PostType), nullable=False, index=True
    )
    like_count: Mapped[int] = mapped_column(Integer, default=0)
    comment_count: Mapped[int] = mapped_column(Integer, default=0)
    create_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    privacy_settings: Mapped[Optional[str]] = mapped_column(Text)  # JSON配置
    raw_data: Mapped[Optional[str]] = mapped_column(Text)  # 原始JSON数据

    def __repr__(self) -> str:
        return f"<SnsPost(bot_wxid='{self.bot_wxid}', gewe_app_id='{self.gewe_app_id}', sns_id={self.sns_id}, author='{self.author_wxid}')>"
