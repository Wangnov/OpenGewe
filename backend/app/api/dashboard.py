"""
仪表盘统计API
"""

from datetime import datetime, timezone, time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from ..core.session_manager import get_admin_session, admin_session, session_manager
from ..models.bot import BotInfo, BotPlugin, RawCallbackLog
from ..models.admin import GlobalPlugin
from ..services.message_logger import message_logger
from ..utils.timezone_utils import get_app_timezone
from opengewe.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/stats", summary="获取仪表盘统计数据")
async def get_dashboard_stats(
    session: AsyncSession = Depends(get_admin_session)
):
    """
    获取仪表盘统计数据
    
    返回：
    - 在线机器人数量
    - 已启用插件数量
    - 今日回调消息数
    - 今日发送消息数
    """
    try:
        # 1. 统计在线机器人数（10分钟内有活动）
        from datetime import timedelta
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=10)
        
        online_bots_stmt = select(func.count(BotInfo.gewe_app_id)).where(
            and_(
                BotInfo.is_online == True,
                BotInfo.last_seen_at >= cutoff_time
            )
        )
        online_bots_result = await session.execute(online_bots_stmt)
        online_bots_count = online_bots_result.scalar() or 0
        
        # 2. 统计已启用插件数（去重）
        # 获取全局启用的插件
        global_plugins_stmt = select(GlobalPlugin.plugin_name).where(
            GlobalPlugin.is_globally_enabled == True
        )
        global_plugins_result = await session.execute(global_plugins_stmt)
        global_plugin_names = set(row[0] for row in global_plugins_result.all())
        
        # 获取所有机器人启用的插件（需要从各个机器人数据库查询）
        enabled_plugin_names = set()
        
        # 获取所有机器人ID
        bot_ids_stmt = select(BotInfo.gewe_app_id)
        bot_ids_result = await session.execute(bot_ids_stmt)
        bot_ids = [row[0] for row in bot_ids_result.all()]
        
        for bot_id in bot_ids:
            try:
                async with session_manager.get_bot_session(bot_id) as bot_session:
                    bot_plugins_stmt = select(BotPlugin.plugin_name).where(
                        BotPlugin.is_enabled == True
                    )
                    bot_plugins_result = await bot_session.execute(bot_plugins_stmt)
                    bot_plugin_names = [row[0] for row in bot_plugins_result.all()]
                    
                    # 只添加全局也启用的插件
                    for plugin_name in bot_plugin_names:
                        if plugin_name in global_plugin_names:
                            enabled_plugin_names.add(plugin_name)
                            
            except Exception as e:
                logger.error(f"查询机器人 {bot_id} 插件失败: {e}")
                continue
        
        enabled_plugins_count = len(enabled_plugin_names)
        
        # 3. 统计今日回调消息数
        # 获取应用时区的今天开始时间
        app_tz = get_app_timezone()
        now = datetime.now(app_tz)
        today_start = datetime.combine(now.date(), time.min, app_tz)
        today_start_utc = today_start.astimezone(timezone.utc)
        
        total_callbacks = 0
        for bot_id in bot_ids:
            try:
                async with session_manager.get_bot_session(bot_id) as bot_session:
                    callback_stmt = select(func.count(RawCallbackLog.id)).where(
                        RawCallbackLog.received_at >= today_start_utc
                    )
                    callback_result = await bot_session.execute(callback_stmt)
                    count = callback_result.scalar() or 0
                    total_callbacks += count
                    
            except Exception as e:
                logger.error(f"查询机器人 {bot_id} 回调数量失败: {e}")
                continue
        
        # 4. 统计今日发送消息数（使用message_logger服务）
        today_sent_count = await message_logger.get_today_sent_count()
        
        # 返回统计结果
        return {
            "online_bots": online_bots_count,
            "enabled_plugins": enabled_plugins_count,
            "today_callbacks": total_callbacks,
            "today_sent_messages": today_sent_count
        }
        
    except Exception as e:
        logger.error(f"获取仪表盘统计数据失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取统计数据失败"
        ) 