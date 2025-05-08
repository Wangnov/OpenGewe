"""内置插件包

此包中包含了OpenGewechat的内置插件。
"""

from opengewechat.plugins.built_in.text_quote_plugin import TextQuotePlugin
from opengewechat.plugins.built_in.message_logger_plugin import MessageLoggerPlugin
from opengewechat.plugins.built_in.silk_convert_plugin import SilkConvertPlugin
from opengewechat.plugins.built_in.emoji_annotation_plugin import EmojiAnnotationPlugin

__all__ = [
    "TextQuotePlugin",
    "MessageLoggerPlugin",
    "SilkConvertPlugin",
    "EmojiAnnotationPlugin",
]
