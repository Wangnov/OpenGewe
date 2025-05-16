"""数据库模型包

导出所有数据库模型类。
"""

from backend.app.models.message import WechatMessage, MessageCleanupTask
from backend.app.models.contact import Contact
from backend.app.models.group_member import GroupMember
from backend.app.models.plugin import Plugin
from backend.app.models.robot import Robot
from backend.app.models.user import User
from backend.app.models.config import Config

__all__ = [
    "WechatMessage",
    "MessageCleanupTask",
    "Contact",
    "GroupMember",
    "Plugin",
    "Robot",
    "User",
    "Config",
]
