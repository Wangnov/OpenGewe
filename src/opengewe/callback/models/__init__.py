"""消息模型模块

此模块提供了各种微信消息类型的模型类，用于统一处理和表示微信消息。
"""

# 导入基础消息类
from opengewe.callback.models.base import BaseMessage

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
