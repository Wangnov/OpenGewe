"""
分离的SQLAlchemy Base类定义

为了避免在错误的数据库中创建表，我们为管理员相关表和机器人相关表
使用不同的Base类，确保表只在对应的数据库中创建。
"""

from sqlalchemy.orm import DeclarativeBase


class AdminBase(DeclarativeBase):
    """
    管理员数据库Base类

    用于以下表：
    - admins (管理员)
    - admin_login_logs (管理员登录日志)
    - global_plugins (全局插件配置)
    - bot_info (机器人信息)
    """

    pass


class BotBase(DeclarativeBase):
    """
    机器人数据库Base类

    用于以下表：
    - raw_callback_log (原始回调日志)
    - contacts (联系人)
    - group_members (群成员)
    - bot_plugins (机器人插件配置)
    - sns_posts (朋友圈记录)
    """

    pass


# 向后兼容的Base类（已弃用）
# 为了不破坏现有代码，暂时保留，但建议使用AdminBase或BotBase
Base = AdminBase
