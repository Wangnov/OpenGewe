"""消息模型模块

此模块提供了各种微信消息类型的模型类，用于统一处理和表示微信消息。
"""

# 导入基础消息类
from opengewechat.message.models.base import BaseMessage

# 导入文本相关消息类
from opengewechat.message.models.text import TextMessage, QuoteMessage

# 导入媒体相关消息类
from opengewechat.message.models.media import (
    ImageMessage,
    VoiceMessage,
    VideoMessage,
    EmojiMessage,
    FinderMessage,
)

# 导入链接相关消息类
from opengewechat.message.models.link import (
    LinkMessage,
    MiniappMessage,
)

# 导入文件相关消息类
from opengewechat.message.models.file import (
    FileNoticeMessage,
    FileMessage,
)

# 导入位置相关消息类
from opengewechat.message.models.location import LocationMessage

# 导入系统相关消息类
from opengewechat.message.models.system import (
    RevokeMessage,
    PatMessage,
    OfflineMessage,
    SyncMessage,
)

# 导入联系人相关消息类
from opengewechat.message.models.contact import (
    CardMessage,
    FriendRequestMessage,
    ContactUpdateMessage,
    ContactDeletedMessage,
)

# 导入群相关消息类
from opengewechat.message.models.group import (
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

# 导入支付相关消息类
from opengewechat.message.models.payment import (
    TransferMessage,
    RedPacketMessage,
)

# 导出所有消息类型
__all__ = [
    "BaseMessage",
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
    "RevokeMessage",
    "PatMessage",
    "OfflineMessage",
    "SyncMessage",
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
    "TransferMessage",
    "RedPacketMessage",
    "FinderMessage",
]
