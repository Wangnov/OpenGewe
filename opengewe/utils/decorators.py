"""装饰器模块

提供用于消息处理和定时任务的装饰器。兼容XYBot和XXXBot插件系统的写法。
"""

from functools import wraps
from typing import Callable, Union

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from opengewe.message.types import MessageType

# 创建调度器实例
scheduler = AsyncIOScheduler()


def schedule(
    trigger: Union[str, CronTrigger, IntervalTrigger], **trigger_args
) -> Callable:
    """
    定时任务装饰器

    例子:

    - @schedule('interval', seconds=30)
    - @schedule('cron', hour=8, minute=30, second=30)
    - @schedule('date', run_date='2024-01-01 00:00:00')

    Args:
        trigger: 触发器类型，可以是'interval'、'cron'或'date'，也可以是触发器实例
        trigger_args: 触发器参数

    Returns:
        装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        job_id = f"{func.__module__}.{func.__qualname__}"

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            return await func(self, *args, **kwargs)

        setattr(wrapper, "_is_scheduled", True)
        setattr(wrapper, "_schedule_trigger", trigger)
        setattr(wrapper, "_schedule_args", trigger_args)
        setattr(wrapper, "_job_id", job_id)

        return wrapper

    return decorator


def add_job_safe(
    scheduler: AsyncIOScheduler,
    job_id: str,
    func: Callable,
    client,
    trigger: Union[str, CronTrigger, IntervalTrigger],
    **trigger_args,
) -> None:
    """添加函数到定时任务中，如果存在则先删除现有的任务

    Args:
        scheduler: 调度器实例
        job_id: 任务ID
        func: 要执行的函数
        client: GeweClient实例
        trigger: 触发器类型或实例
        trigger_args: 触发器参数
    """
    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass
    scheduler.add_job(func, trigger, args=[client], id=job_id, **trigger_args)


def remove_job_safe(scheduler: AsyncIOScheduler, job_id: str) -> None:
    """从定时任务中移除任务

    Args:
        scheduler: 调度器实例
        job_id: 任务ID
    """
    try:
        scheduler.remove_job(job_id)
    except Exception:
        pass


def _create_message_handler(message_type: MessageType, priority: int = 50) -> Callable:
    """创建消息处理器装饰器

    Args:
        message_type: 消息类型
        priority: 处理优先级(0-99)，数字越小优先级越高

    Returns:
        装饰器函数
    """

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", message_type)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_text_message(priority: Union[int, Callable] = 50) -> Callable:
    """文本消息装饰器

    用于处理文本消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):  # 无参数调用时
        f = priority
        setattr(f, "_message_type", MessageType.TEXT)
        setattr(f, "_priority", 50)
        return f

    # 有参数调用时
    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.TEXT)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_at_message(priority: Union[int, Callable] = 50) -> Callable:
    """被@消息装饰器

    用于处理被@消息的装饰器。暂未实现。计划通过wrap的方式直接检查message的is_at属性。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """

    return


def on_image_message(priority: Union[int, Callable] = 50) -> Callable:
    """图片消息装饰器

    用于处理图片消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.IMAGE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.IMAGE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_voice_message(priority: Union[int, Callable] = 50) -> Callable:
    """语音消息装饰器

    用于处理语音消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.VOICE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.VOICE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_emoji_message(priority: Union[int, Callable] = 50) -> Callable:
    """表情消息装饰器

    用于处理表情消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.EMOJI)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.EMOJI)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_file_message(priority: Union[int, Callable] = 50) -> Callable:
    """文件消息装饰器

    用于处理文件消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.FILE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.FILE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_quote_message(priority: Union[int, Callable] = 50) -> Callable:
    """引用消息装饰器

    用于处理引用消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.QUOTE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.QUOTE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_video_message(priority: Union[int, Callable] = 50) -> Callable:
    """视频消息装饰器

    用于处理视频消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.VIDEO)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.VIDEO)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_pat_message(priority: Union[int, Callable] = 50) -> Callable:
    """拍一拍消息装饰器

    用于处理拍一拍消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.PAT)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.PAT)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_link_message(priority: Union[int, Callable] = 50) -> Callable:
    """链接消息装饰器

    用于处理链接消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.LINK)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.LINK)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_system_message(priority: Union[int, Callable] = 50) -> Callable:
    """系统消息装饰器

    用于处理各种系统消息的装饰器，包括群信息变更等。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.UNKNOWN)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.UNKNOWN)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_other_message(priority: Union[int, Callable] = 50) -> Callable:
    """任意消息装饰器

    用于处理任何类型消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", None)  # None表示处理所有类型
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", None)  # None表示处理所有类型
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


# 以下是根据MessageType枚举扩充的装饰器，无法与XYBot或XXXBot兼容，除非他们对源代码进行扩展


def on_miniapp_message(priority: Union[int, Callable] = 50) -> Callable:
    """小程序消息装饰器

    用于处理小程序消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.MINIAPP)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.MINIAPP)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_revoke_message(priority: Union[int, Callable] = 50) -> Callable:
    """撤回消息装饰器

    用于处理撤回消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.REVOKE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.REVOKE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_file_notice_message(priority: Union[int, Callable] = 50) -> Callable:
    """文件通知消息装饰器

    用于处理文件发送通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.FILE_NOTICE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.FILE_NOTICE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_card_message(priority: Union[int, Callable] = 50) -> Callable:
    """名片消息装饰器

    用于处理名片消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.CARD)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.CARD)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_friend_request_message(priority: Union[int, Callable] = 50) -> Callable:
    """好友请求消息装饰器

    用于处理好友添加请求通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.FRIEND_REQUEST)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.FRIEND_REQUEST)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_contact_update_message(priority: Union[int, Callable] = 50) -> Callable:
    """联系人更新消息装饰器

    用于处理好友通过验证及好友资料变更的通知消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.CONTACT_UPDATE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.CONTACT_UPDATE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_transfer_message(priority: Union[int, Callable] = 50) -> Callable:
    """转账消息装饰器

    用于处理转账消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.TRANSFER)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.TRANSFER)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_red_packet_message(priority: Union[int, Callable] = 50) -> Callable:
    """红包消息装饰器

    用于处理红包消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.RED_PACKET)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.RED_PACKET)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_finder_message(priority: Union[int, Callable] = 50) -> Callable:
    """视频号消息装饰器

    用于处理视频号消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.FINDER)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.FINDER)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_location_message(priority: Union[int, Callable] = 50) -> Callable:
    """位置消息装饰器

    用于处理地理位置消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.LOCATION)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.LOCATION)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_invite_message(priority: Union[int, Callable] = 50) -> Callable:
    """群聊邀请确认消息装饰器

    用于处理群聊邀请确认通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_INVITE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_INVITE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_invited_message(priority: Union[int, Callable] = 50) -> Callable:
    """被邀请入群消息装饰器

    用于处理群聊邀请的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_INVITED)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_INVITED)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_removed_message(priority: Union[int, Callable] = 50) -> Callable:
    """被移除群聊消息装饰器

    用于处理被移除群聊通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_REMOVED)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_REMOVED)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_kick_message(priority: Union[int, Callable] = 50) -> Callable:
    """踢出群聊消息装饰器

    用于处理踢出群聊通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_KICK)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_KICK)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_dismiss_message(priority: Union[int, Callable] = 50) -> Callable:
    """解散群聊消息装饰器

    用于处理解散群聊通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_DISMISS)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_DISMISS)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_rename_message(priority: Union[int, Callable] = 50) -> Callable:
    """群重命名消息装饰器

    用于处理修改群名称的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_RENAME)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_RENAME)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_owner_change_message(priority: Union[int, Callable] = 50) -> Callable:
    """群主变更消息装饰器

    用于处理更换群主通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_OWNER_CHANGE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_OWNER_CHANGE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_info_update_message(priority: Union[int, Callable] = 50) -> Callable:
    """群信息更新消息装饰器

    用于处理群信息变更通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_INFO_UPDATE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_INFO_UPDATE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_announcement_message(priority: Union[int, Callable] = 50) -> Callable:
    """群公告消息装饰器

    用于处理发布群公告的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_ANNOUNCEMENT)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_ANNOUNCEMENT)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_todo_message(priority: Union[int, Callable] = 50) -> Callable:
    """群待办消息装饰器

    用于处理群待办的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_TODO)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_TODO)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_sync_message(priority: Union[int, Callable] = 50) -> Callable:
    """同步消息装饰器

    用于处理同步消息的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.SYNC)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.SYNC)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_contact_deleted_message(priority: Union[int, Callable] = 50) -> Callable:
    """联系人删除消息装饰器

    用于处理删除好友通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.CONTACT_DELETED)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.CONTACT_DELETED)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_group_quit_message(priority: Union[int, Callable] = 50) -> Callable:
    """退出群聊消息装饰器

    用于处理退出群聊的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.GROUP_QUIT)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.GROUP_QUIT)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator


def on_offline_message(priority: Union[int, Callable] = 50) -> Callable:
    """掉线通知消息装饰器

    用于处理掉线通知的装饰器。

    Args:
        priority: 处理优先级(0-99)或函数，默认为50

    Returns:
        装饰器函数
    """
    if callable(priority):
        f = priority
        setattr(f, "_message_type", MessageType.OFFLINE)
        setattr(f, "_priority", 50)
        return f

    def decorator(func: Callable) -> Callable:
        setattr(func, "_message_type", MessageType.OFFLINE)
        setattr(func, "_priority", min(max(priority, 0), 99))
        return func

    return decorator
