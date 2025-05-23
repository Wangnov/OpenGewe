"""消息模型模块

此模块提供了各种微信消息类型的模型类，用于统一处理和表示微信消息。
"""

# 导入基础消息类和抽象类
from opengewe.callback.models.base import (
    BaseMessage, 
    MediaBaseMessage,
    TextBaseMessage,
    FileBaseMessage,
    GroupBaseMessage,
    ContactBaseMessage,
    SystemBaseMessage,
    PaymentBaseMessage
)

# 导入文本相关消息类
from opengewe.callback.models.text import TextMessage, QuoteMessage

# 导入媒体相关消息类
from opengewe.callback.models.media import (
    ImageMessage,
    VoiceMessage,
    VideoMessage,
    EmojiMessage,
)

# 导入链接相关消息类
from opengewe.callback.models.link import (
    LinkMessage,
    MiniappMessage,
    FinderMessage,
)

# 导入文件相关消息类
from opengewe.callback.models.file import (
    FileNoticeMessage,
    FileMessage,
)

# 导入位置相关消息类
from opengewe.callback.models.location import LocationMessage

# 导入联系人相关消息类
from opengewe.callback.models.contact import (
    CardMessage,
    FriendRequestMessage,
    ContactUpdateMessage,
    ContactDeletedMessage,
)

# 导入群聊相关消息类
from opengewe.callback.models.group import (
    GroupInviteMessage,
    GroupInvitedMessage,
    GroupRemovedMessage,
    GroupKickMessage,
    GroupDismissMessage,
    GroupRenameMessage,
    GroupOwnerChangeMessage,
    GroupInfoUpdateMessage,
    GroupAnnouncementMessage,
    GroupTodoMessage,
    GroupQuitMessage,
)

# 导入系统相关消息类
from opengewe.callback.models.system import (
    RevokeMessage,
    PatMessage,
    OfflineMessage,
    SyncMessage,
)

# 导入支付相关消息类
from opengewe.callback.models.payment import (
    TransferMessage,
    RedPacketMessage,
)

# 为保证向后兼容，创建同步版本的from_dict方法
import asyncio
import inspect
import functools
from typing import Dict, Any, Optional, Type, TypeVar, get_type_hints

# 获取消息类列表
_MESSAGE_CLASSES = []
for _name, _cls in globals().copy().items():
    if (
        isinstance(_cls, type) 
        and issubclass(_cls, BaseMessage) 
        and _cls is not BaseMessage
        and not _name.endswith("BaseMessage")  # 排除抽象基类
    ):
        _MESSAGE_CLASSES.append(_cls)

# 创建同步兼容包装器
def _create_sync_from_dict(async_method):
    @functools.wraps(async_method)
    def sync_wrapper(cls, data, client=None):
        """同步版本的from_dict方法，用于向后兼容"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(async_method(cls, data, client))
    
    return classmethod(sync_wrapper)

# 为所有消息类创建同步from_dict方法
for _cls in _MESSAGE_CLASSES:
    # 确保类使用了新的异步from_dict
    if hasattr(_cls, "from_dict") and inspect.iscoroutinefunction(_cls.from_dict.__func__):
        # 类已经有异步from_dict，不需处理
        continue
    
    # 如果类定义了旧的同步from_dict，保存它
    original_from_dict = getattr(_cls, "from_dict", None)
    if original_from_dict and not inspect.iscoroutinefunction(getattr(original_from_dict, "__func__", lambda: None)):
        # 保存原始同步方法为_original_from_dict
        setattr(_cls, "_original_from_dict", original_from_dict)
    
    # 创建同步包装器
    _cls.from_dict = _create_sync_from_dict(BaseMessage.from_dict)

# 清理临时变量，避免污染命名空间
del _name, _cls, _MESSAGE_CLASSES, _create_sync_from_dict, inspect, asyncio, functools

# 导出所有消息类型
__all__ = [
    "BaseMessage",
    "MediaBaseMessage",
    "TextBaseMessage",
    "FileBaseMessage",
    "GroupBaseMessage",
    "ContactBaseMessage",
    "SystemBaseMessage",
    "PaymentBaseMessage",
    "TextMessage",
    "QuoteMessage",
    "ImageMessage",
    "VoiceMessage",
    "VideoMessage",
    "EmojiMessage",
    "LinkMessage",
    "MiniappMessage",
    "FileNoticeMessage",
    "FileMessage",
    "LocationMessage",
    "CardMessage",
    "FriendRequestMessage",
    "ContactUpdateMessage",
    "ContactDeletedMessage",
    "GroupInviteMessage",
    "GroupInvitedMessage",
    "GroupRemovedMessage",
    "GroupKickMessage",
    "GroupDismissMessage",
    "GroupRenameMessage",
    "GroupOwnerChangeMessage",
    "GroupInfoUpdateMessage",
    "GroupAnnouncementMessage",
    "GroupTodoMessage",
    "GroupQuitMessage",
    "RevokeMessage",
    "PatMessage",
    "OfflineMessage",
    "SyncMessage",
    "TransferMessage",
    "RedPacketMessage",
    "FinderMessage",
]
