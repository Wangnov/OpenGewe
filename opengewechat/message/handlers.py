"""消息处理器模块（兼容层）

此模块提供了向后兼容性，从新的handlers包中导入并重新导出处理器类。
为了保持现有代码的兼容性，未来请直接从opengewechat.message.handlers包中导入。
"""

# 导入基础处理器
from opengewechat.message.handlers import *  # noqa: F403
