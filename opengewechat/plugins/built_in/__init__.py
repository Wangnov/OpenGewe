"""内置插件

此包包含opengewechat的内置插件，这些插件提供基本功能。
"""

from opengewechat.plugins.built_in.text_quote_plugin import TextQuotePlugin
from opengewechat.plugins.built_in.message_logger_plugin import MessageLoggerPlugin
from opengewechat.plugins.built_in.silk_convert_plugin import SilkConvertPlugin

__all__ = ["TextQuotePlugin", "MessageLoggerPlugin", "SilkConvertPlugin"]
