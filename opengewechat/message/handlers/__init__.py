"""消息处理器包

此包包含各种消息类型的处理器，用于解析和处理微信消息。
"""

# 导入基础处理器
from opengewechat.message.handlers.base_handler import BaseHandler

# 导入文本消息处理器
from opengewechat.message.handlers.text_handlers import (
    TextMessageHandler,
    QuoteHandler,
)

# 导入媒体消息处理器
from opengewechat.message.handlers.media_handlers import (
    ImageMessageHandler,
    VoiceMessageHandler,
    VideoMessageHandler,
    EmojiMessageHandler,
)

# 导入系统消息处理器
from opengewechat.message.handlers.system_handlers import (
    SysmsgHandler,
    OfflineHandler,
)

# 导入联系人相关处理器
from opengewechat.message.handlers.contact_handlers import (
    CardHandler,
    FriendRequestHandler,
    ContactUpdateHandler,
    ContactDeletedHandler,
)

# 导入群聊相关处理器
from opengewechat.message.handlers.group_handlers import (
    GroupInviteMessageHandler,
    GroupInvitedMessageHandler,
    GroupInfoUpdateHandler,
    GroupTodoHandler,
)

# 导入位置消息处理器
from opengewechat.message.handlers.location_handlers import LocationMessageHandler

# 导入文件相关处理器
from opengewechat.message.handlers.file_handlers import (
    FileNoticeMessageHandler,
    FileMessageHandler,
)

# 导入支付相关处理器
from opengewechat.message.handlers.payment_handlers import (
    TransferHandler,
    RedPacketHandler,
)

# 导入链接相关处理器
from opengewechat.message.handlers.link_handlers import (
    LinkMessageHandler,
    FinderHandler,
    MiniappHandler,
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
    GroupInviteMessageHandler,
    GroupInvitedMessageHandler,
    FileNoticeMessageHandler,
    FileMessageHandler,
    GroupTodoHandler,
    SysmsgHandler,
    OfflineHandler,
    GroupInfoUpdateHandler,
    ContactUpdateHandler,
    ContactDeletedHandler,
    FriendRequestHandler,
    MiniappHandler,
    QuoteHandler,
    TransferHandler,
    RedPacketHandler,
    FinderHandler,
]
