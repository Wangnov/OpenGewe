"""日志格式化模块

提供各种日志格式化函数，处理特殊消息格式，如XML、JSON等。
"""

import re
import json
from typing import Dict, Any
import xml.dom.minidom as minidom
from xml.parsers.expat import ExpatError

# 存储全局日志级别的变量，将由logger.config模块设置
GLOBAL_LOG_LEVEL = "INFO"


def should_escape_message(message: str) -> bool:
    """判断消息是否需要特殊处理

    识别XML或JSON格式的消息，防止格式化错误。

    Args:
        message: 日志消息

    Returns:
        是否需要特殊处理
    """
    if not isinstance(message, str):
        return False

    # 检查是否可能包含XML内容
    if (
        message.strip().startswith("<") and message.strip().endswith(">")
    ) or "<xml>" in message:
        return True

    # 检查是否可能包含JSON内容
    if (message.strip().startswith("{") and message.strip().endswith("}")) or (
        message.strip().startswith("[") and message.strip().endswith("]")
    ):
        try:
            json.loads(message)
            return True
        except json.JSONDecodeError:
            pass

    # 检查是否包含ANSI颜色代码（避免重复应用颜色）
    if re.search(r"\x1b\[\d+m", message):
        return True

    # 检查是否包含loguru格式标记
    if re.search(r"<[a-z]+>.*</[a-z]+>", message):
        return True

    # 检查是否是超长消息（超过500字符）
    if len(message) > 500:
        return True

    return False


def format_console_message(record: Dict[str, Any]) -> str:
    """格式化控制台消息

    对于特殊消息（XML、JSON等）进行特殊处理，避免格式化问题。

    Args:
        record: 日志记录

    Returns:
        格式化后的消息
    """
    message = record["message"]

    if not isinstance(message, str):
        return message

    # 处理可能的XML内容
    if (
        message.strip().startswith("<") and message.strip().endswith(">")
    ) or "<xml>" in message:
        try:
            # 尝试格式化XML
            dom = minidom.parseString(message)
            pretty_xml = dom.toprettyxml(indent="  ")
            return f"[XML内容] {pretty_xml}"
        except ExpatError:
            pass

    # 处理可能的JSON内容
    if (message.strip().startswith("{") and message.strip().endswith("}")) or (
        message.strip().startswith("[") and message.strip().endswith("]")
    ):
        try:
            # 尝试格式化JSON
            parsed = json.loads(message)
            pretty_json = json.dumps(parsed, ensure_ascii=False, indent=2)
            return f"[JSON内容] {pretty_json}"
        except json.JSONDecodeError:
            pass

    # 处理超长消息
    if len(message) > 500:
        # 检查全局日志级别，仅在非DEBUG级别时折叠消息
        if GLOBAL_LOG_LEVEL not in ["DEBUG", "TRACE"]:
            preview = message[:200] + "..." + message[-200:]
            return (
                f"[长消息] ({len(message)} 字符): {preview} [使用DEBUG级别查看完整内容]"
            )
        # 在DEBUG或TRACE级别时，显示完整消息
        return message

    return message


def format_file_message(record: Dict[str, Any]) -> str:
    """格式化文件消息

    对于特殊消息（XML、JSON等）进行特殊处理，确保可读性。

    Args:
        record: 日志记录

    Returns:
        格式化后的消息
    """
    message = record["message"]

    if not isinstance(message, str):
        return message

    # 处理可能的XML内容
    if (
        message.strip().startswith("<") and message.strip().endswith(">")
    ) or "<xml>" in message:
        try:
            # 尝试格式化XML
            dom = minidom.parseString(message)
            pretty_xml = dom.toprettyxml(indent="  ")
            return f"\nXML内容:\n{pretty_xml}"
        except ExpatError:
            pass

    # 处理可能的JSON内容
    if (message.strip().startswith("{") and message.strip().endswith("}")) or (
        message.strip().startswith("[") and message.strip().endswith("]")
    ):
        try:
            # 尝试格式化JSON
            parsed = json.loads(message)
            pretty_json = json.dumps(parsed, ensure_ascii=False, indent=2)
            return f"\nJSON内容:\n{pretty_json}"
        except json.JSONDecodeError:
            pass

    return message


# 日志级别对应的emoji
LEVEL_EMOJIS = {
    "TRACE": "🔍",
    "DEBUG": "🐛",
    "INFO": "ℹ️ ",
    "SUCCESS": "✅",
    "WARNING": "⚠️ ",
    "ERROR": "❌",
    "CRITICAL": "🔥",
}


def format_level(level_name: str) -> str:
    """格式化日志级别，添加emoji并居中显示

    Args:
        level_name: 日志级别名称

    Returns:
        格式化的级别文本
    """
    emoji = LEVEL_EMOJIS.get(level_name, "")
    return f"{level_name} {emoji}"


def color_level(level: str) -> str:
    """根据日志级别返回彩色级别字符串

    Args:
        level: 日志级别

    Returns:
        带颜色的级别字符串
    """
    colors = {
        "TRACE": "<cyan>{}</cyan>",
        "DEBUG": "<blue>{}</blue>",
        "INFO": "<bold>{}</bold>",
        "SUCCESS": "<green>{}</green>",
        "WARNING": "<yellow>{}</yellow>",
        "ERROR": "<red>{}</red>",
        "CRITICAL": "<bold><red>{}</red></bold>",
    }

    # 应用颜色
    color_format = colors.get(level, "{}")
    return color_format.format(format_level(level))
