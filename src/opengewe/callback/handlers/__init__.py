"""消息处理器包

此包包含各种消息类型的处理器，用于解析和处理微信消息。
"""

# 导入基础处理器
from opengewe.callback.handlers.base import BaseHandler

# 导入文本消息处理器
from opengewe.callback.handlers.text import (
    TextMessageHandler,
    QuoteHandler,
)

# 导入媒体消息处理器
from opengewe.callback.handlers.media import (
    ImageMessageHandler,
    VoiceMessageHandler,
    VideoMessageHandler,
    EmojiMessageHandler,
)

# 导入联系人相关处理器
from opengewe.callback.handlers.contact import (
    CardHandler,
    FriendRequestHandler,
    ContactUpdateHandler,
    ContactDeletedHandler,
)

# 导入文件相关处理器
from opengewe.callback.handlers.file import (
    FileNoticeMessageHandler,
    FileMessageHandler,
)

# 导入链接相关处理器
from opengewe.callback.handlers.link import (
    LinkMessageHandler,
    FinderHandler,
    MiniappHandler,
)

# 导入位置消息处理器
from opengewe.callback.handlers.location import LocationMessageHandler

# 导入群聊消息处理器
from opengewe.callback.handlers.group import (
    GroupInviteMessageHandler,
    GroupInvitedMessageHandler,
    GroupInfoUpdateHandler,
    GroupTodoHandler,
    GroupRemovedMessageHandler,
    GroupKickMessageHandler,
    GroupDismissMessageHandler,
)

# 导入系统消息处理器
from opengewe.callback.handlers.system import (
    SysmsgHandler,
    OfflineHandler,
    SyncHandler,
)

# 导入支付相关处理器
from opengewe.callback.handlers.payment import (
    TransferHandler,
    RedPacketHandler,
)

# 默认处理器列表
DEFAULT_HANDLERS = [
    TextMessageHandler,
    ImageMessageHandler,
    VoiceMessageHandler,
    VideoMessageHandler,
    LocationMessageHandler,
    CardHandler,
    EmojiMessageHandler,
    LinkMessageHandler,
    FileNoticeMessageHandler,
    FileMessageHandler,
    ContactUpdateHandler,
    ContactDeletedHandler,
    FriendRequestHandler,
    MiniappHandler,
    QuoteHandler,
    FinderHandler,
    GroupInviteMessageHandler,
    GroupInvitedMessageHandler,
    GroupInfoUpdateHandler,
    GroupTodoHandler,
    GroupRemovedMessageHandler,
    GroupKickMessageHandler,
    GroupDismissMessageHandler,
    SysmsgHandler,
    OfflineHandler,
    TransferHandler,
    RedPacketHandler,
    SyncHandler,
]

__all__ = [
    "BaseHandler",
    "DEFAULT_HANDLERS",
]
