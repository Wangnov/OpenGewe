"""消息处理器模块（兼容层）

此模块提供了向后兼容性，从新的handlers包中导入并重新导出处理器类。
为了保持现有代码的兼容性，未来请直接从opengewechat.message.handlers包中导入。
"""

# 导入基础处理器
from opengewechat.message.handlers.base_handler import BaseHandler  # noqa: F401

# 导入文本消息处理器
from opengewechat.message.handlers.text_handlers import (
    TextMessageHandler,  # noqa: F401
    QuoteHandler,  # noqa: F401
)

# 导入媒体消息处理器
from opengewechat.message.handlers.media_handlers import (
    ImageMessageHandler,  # noqa: F401
    VoiceMessageHandler,  # noqa: F401
    VideoMessageHandler,  # noqa: F401
    EmojiMessageHandler,  # noqa: F401
)

# 导入系统消息处理器
from opengewechat.message.handlers.system_handlers import (
    SysmsgHandler,  # noqa: F401
    OfflineHandler,  # noqa: F401
)

# 导入联系人相关处理器
from opengewechat.message.handlers.contact_handlers import (
    CardHandler,  # noqa: F401
    FriendRequestHandler,  # noqa: F401
    ContactUpdateHandler,  # noqa: F401
    ContactDeletedHandler,  # noqa: F401
)

# 导入群聊相关处理器
from opengewechat.message.handlers.group_handlers import (
    GroupInvitedMessageHandler,  # noqa: F401
    GroupInfoUpdateHandler,  # noqa: F401
    GroupTodoHandler,  # noqa: F401
)

# 导入位置消息处理器
from opengewechat.message.handlers.location_handlers import (
    LocationMessageHandler,  # noqa: F401
)

# 导入文件相关处理器
from opengewechat.message.handlers.file_handlers import (
    FileNoticeMessageHandler,  # noqa: F401
    FileMessageHandler,  # noqa: F401
)

# 导入支付相关处理器
from opengewechat.message.handlers.payment_handlers import (
    TransferHandler,  # noqa: F401
    RedPacketHandler,  # noqa: F401
)

# 导入链接相关处理器
from opengewechat.message.handlers.link_handlers import (
    LinkMessageHandler,  # noqa: F401
    FinderHandler,  # noqa: F401
    MiniappHandler,  # noqa: F401
)

# 默认处理器列表，直接从handlers包中导入
from opengewechat.message.handlers import DEFAULT_HANDLERS  # noqa: F401
