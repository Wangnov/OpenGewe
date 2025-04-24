"""消息模型模块（兼容层）

为了向后兼容性，我们从新的opengewechat.message.models包中导入消息模型类。
请在新代码中直接使用opengewechat.message.models包中的类。
"""

# 导入所有消息模型
from opengewechat.message.models import *  # noqa: F403
