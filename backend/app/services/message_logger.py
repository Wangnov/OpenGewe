"""
消息日志服务 - 订阅OpenGewe消息发送事件并记录到数据库
"""

import json
import asyncio
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from opengewe.utils.event_emitter import message_event_emitter
from opengewe.logger import get_logger

from ..models.bot import MessageSentLog
from ..core.session_manager import session_manager

logger = get_logger(__name__)


class MessageLoggerService:
    """消息日志服务"""

    _instance: Optional["MessageLoggerService"] = None
    _initialized: bool = False

    def __new__(cls) -> "MessageLoggerService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._subscribed = False
            MessageLoggerService._initialized = True
            logger.info("消息日志服务初始化完成")

    def subscribe_events(self):
        """订阅消息发送事件"""
        if self._subscribed:
            return
        
        # 订阅消息发送事件
        message_event_emitter.on("message_sent", self._on_message_sent)
        self._subscribed = True
        logger.info("已订阅消息发送事件")

    def unsubscribe_events(self):
        """取消订阅事件"""
        if not self._subscribed:
            return
        
        message_event_emitter.off("message_sent", self._on_message_sent)
        self._subscribed = False
        logger.info("已取消订阅消息发送事件")

    async def _on_message_sent(self, event_data: Dict[str, Any]):
        """处理消息发送事件"""
        try:
            app_id = event_data.get("app_id")
            if not app_id:
                logger.warning("消息发送事件缺少app_id")
                return

            # 创建数据库记录
            async with session_manager.get_bot_session(app_id) as session:
                # 准备参数JSON
                params_json = None
                if event_data.get("params"):
                    params_json = json.dumps(event_data["params"], ensure_ascii=False)

                # 创建日志记录
                log_entry = MessageSentLog(
                    gewe_app_id=app_id,
                    method_name=event_data.get("method_name", "unknown"),
                    to_wxid=event_data.get("to_wxid", ""),
                    params_json=params_json
                )

                session.add(log_entry)
                await session.commit()

                logger.debug(
                    f"记录消息发送: app_id={app_id}, "
                    f"method={event_data.get('method_name')}, "
                    f"to={event_data.get('to_wxid')}"
                )

        except Exception as e:
            logger.error(f"记录消息发送失败: {e}", exc_info=True)

    async def get_today_sent_count(self, gewe_app_id: Optional[str] = None) -> int:
        """获取今日发送消息数量"""
        from sqlalchemy import select, func, and_
        from datetime import datetime, time, timezone
        from ..utils.timezone_utils import get_app_timezone, to_app_timezone

        try:
            # 获取应用时区的今天开始时间
            app_tz = get_app_timezone()
            now = datetime.now(app_tz)
            today_start = datetime.combine(now.date(), time.min, app_tz)
            today_start_utc = today_start.astimezone(timezone.utc)

            if gewe_app_id:
                # 查询特定机器人的发送数量
                async with session_manager.get_bot_session(gewe_app_id) as session:
                    stmt = select(func.count(MessageSentLog.id)).where(
                        and_(
                            MessageSentLog.gewe_app_id == gewe_app_id,
                            MessageSentLog.sent_at >= today_start_utc
                        )
                    )
                    result = await session.execute(stmt)
                    return result.scalar() or 0
            else:
                # 查询所有机器人的总发送数量
                total_count = 0
                # 获取所有机器人app_id列表
                from ..models.bot import BotInfo
                from ..core.session_manager import admin_session
                
                async with admin_session() as session:
                    stmt = select(BotInfo.gewe_app_id)
                    result = await session.execute(stmt)
                    app_ids = [row[0] for row in result.all()]
                
                # 查询每个机器人的发送数量
                for app_id in app_ids:
                    try:
                        async with session_manager.get_bot_session(app_id) as bot_session:
                            stmt = select(func.count(MessageSentLog.id)).where(
                                MessageSentLog.sent_at >= today_start_utc
                            )
                            result = await bot_session.execute(stmt)
                            count = result.scalar() or 0
                            total_count += count
                    except Exception as e:
                        logger.error(f"查询机器人 {app_id} 发送数量失败: {e}")
                        continue
                
                return total_count

        except Exception as e:
            logger.error(f"获取今日发送数量失败: {e}", exc_info=True)
            return 0


# 全局消息日志服务实例
message_logger = MessageLoggerService() 