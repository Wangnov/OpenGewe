"""
时区工具函数

提供统一的时区处理功能
"""

from datetime import datetime, timezone
import pytz
from loguru import logger


def get_app_timezone() -> timezone:
    """
    获取应用时区（固定使用中国上海时区）

    Returns:
        timezone: 时区对象
    """
    try:
        # 直接使用中国上海时区，不再依赖配置
        return pytz.timezone("Asia/Shanghai")
    except pytz.UnknownTimeZoneError:
        # 如果出现异常（理论上不会发生，因为'Asia/Shanghai'是有效的时区），回退到UTC
        logger.warning("无法识别时区 'Asia/Shanghai'，回退到UTC")
        return timezone.utc


def now_with_timezone() -> datetime:
    """
    获取当前时间（带时区信息）

    Returns:
        datetime: 当前时间
    """
    app_tz = get_app_timezone()
    return datetime.now(app_tz)


def utc_now() -> datetime:
    """
    获取UTC当前时间

    Returns:
        datetime: UTC当前时间
    """
    return datetime.now(timezone.utc)


def to_app_timezone(dt: datetime) -> datetime:
    """
    将datetime转换为应用时区

    Args:
        dt: 要转换的datetime对象

    Returns:
        datetime: 转换后的datetime对象
    """
    app_tz = get_app_timezone()

    if dt.tzinfo is None:
        # 如果没有时区信息，假设为UTC
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(app_tz)


def to_utc(dt: datetime) -> datetime:
    """
    将datetime转换为UTC时区

    Args:
        dt: 要转换的datetime对象

    Returns:
        datetime: UTC时区的datetime对象
    """
    if dt.tzinfo is None:
        # 如果没有时区信息，假设为应用时区
        app_tz = get_app_timezone()
        dt = dt.replace(tzinfo=app_tz)

    return dt.astimezone(timezone.utc)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    格式化datetime为字符串

    Args:
        dt: 要格式化的datetime对象
        format_str: 格式字符串

    Returns:
        str: 格式化后的字符串
    """
    # 转换为应用时区
    app_dt = to_app_timezone(dt)
    return app_dt.strftime(format_str)


def ensure_timezone(dt: datetime, assume_utc: bool = True) -> datetime:
    """
    确保datetime对象具有时区信息

    Args:
        dt: 要检查的datetime对象
        assume_utc: 如果没有时区信息时，是否假设为UTC

    Returns:
        datetime: 带时区信息的datetime对象
    """
    if dt.tzinfo is None:
        if assume_utc:
            return dt.replace(tzinfo=timezone.utc)
        else:
            app_tz = get_app_timezone()
            return dt.replace(tzinfo=app_tz)
    return dt


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    解析字符串为datetime对象

    Args:
        dt_str: 时间字符串
        format_str: 格式字符串

    Returns:
        datetime: 解析后的datetime对象（UTC时区）
    """
    dt = datetime.strptime(dt_str, format_str)
    app_tz = get_app_timezone()

    # 假设输入的字符串是应用时区的时间
    dt = dt.replace(tzinfo=app_tz)

    # 转换为UTC
    return to_utc(dt)
