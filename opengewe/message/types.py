from enum import Enum, auto


class MessageType(Enum):
    """微信消息类型枚举"""

    # 基础消息类型
    TEXT = auto()  # 文本消息
    IMAGE = auto()  # 图片消息
    VOICE = auto()  # 语音消息
    VIDEO = auto()  # 视频消息
    EMOJI = auto()  # emoji表情
    LINK = auto()  # 公众号链接
    FILE_NOTICE = auto()  # 文件消息（发送文件的通知）
    FILE = auto()  # 文件消息（文件发送完成）
    CARD = auto()  # 名片消息
    FRIEND_REQUEST = auto()  # 好友添加请求通知
    CONTACT_UPDATE = auto()  # 好友通过验证及好友资料变更的通知消息
    MINIAPP = auto()  # 小程序消息
    QUOTE = auto()  # 引用消息
    TRANSFER = auto()  # 转账消息
    RED_PACKET = auto()  # 红包消息
    FINDER = auto()  # 视频号消息
    LOCATION = auto()  # 地理位置

    # 系统消息类型
    REVOKE = auto()  # 撤回消息
    PAT = auto()  # 拍一拍消息
    GROUP_INVITE = auto()  # 群聊邀请确认通知
    GROUP_INVITED = auto()  # 群聊邀请
    GROUP_REMOVED = auto()  # 被移除群聊通知
    GROUP_KICK = auto()  # 踢出群聊通知
    GROUP_DISMISS = auto()  # 解散群聊通知
    GROUP_RENAME = auto()  # 修改群名称
    GROUP_OWNER_CHANGE = auto()  # 更换群主通知
    GROUP_INFO_UPDATE = auto()  # 群信息变更通知
    GROUP_ANNOUNCEMENT = auto()  # 发布群公告
    GROUP_TODO = auto()  # 群待办
    SYNC = auto()  # 同步消息

    # 其他类型
    CONTACT_DELETED = auto()  # 删除好友通知
    GROUP_QUIT = auto()  # 退出群聊
    OFFLINE = auto()  # 掉线通知
    UNKNOWN = auto()  # 未知消息类型

    @classmethod
    def get_typename_map(cls):
        """获取类型名称与枚举值的映射"""
        return {
            "AddMsg": {
                "TEXT": cls.TEXT,
                "IMAGE": cls.IMAGE,
                "VOICE": cls.VOICE,
                "VIDEO": cls.VIDEO,
                "EMOJI": cls.EMOJI,
                "LINK": cls.LINK,
                "FILE_NOTICE": cls.FILE_NOTICE,
                "FILE": cls.FILE,
                "CARD": cls.CARD,
                "FRIEND_REQUEST": cls.FRIEND_REQUEST,
                "MINIAPP": cls.MINIAPP,
                "QUOTE": cls.QUOTE,
                "TRANSFER": cls.TRANSFER,
                "RED_PACKET": cls.RED_PACKET,
                "FINDER": cls.FINDER,
                "LOCATION": cls.LOCATION,
                "REVOKE": cls.REVOKE,
                "PAT": cls.PAT,
                "GROUP_INVITE": cls.GROUP_INVITE,
                "GROUP_INVITED": cls.GROUP_INVITED,
                "GROUP_REMOVED": cls.GROUP_REMOVED,
                "GROUP_KICK": cls.GROUP_KICK,
                "GROUP_DISMISS": cls.GROUP_DISMISS,
                "GROUP_RENAME": cls.GROUP_RENAME,
                "GROUP_OWNER_CHANGE": cls.GROUP_OWNER_CHANGE,
                "GROUP_ANNOUNCEMENT": cls.GROUP_ANNOUNCEMENT,
                "GROUP_TODO": cls.GROUP_TODO,
                "SYNC": cls.SYNC,
            },
            "ModContacts": {
                "CONTACT_UPDATE": cls.CONTACT_UPDATE,
                "GROUP_INFO_UPDATE": cls.GROUP_INFO_UPDATE,
            },
            "DelContacts": {
                "CONTACT_DELETED": cls.CONTACT_DELETED,
                "GROUP_QUIT": cls.GROUP_QUIT,
            },
            "Offline": {
                "OFFLINE": cls.OFFLINE,
            },
        }
