"""
Webhook相关API路由
"""

import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from loguru import logger

from ..core.database import get_admin_session, get_bot_session
from ..core.security import verify_webhook_source
from ..models.bot import BotInfo, RawCallbackLog
from ..schemas.bot import WebhookPayload


router = APIRouter()


@router.post("/{bot_schema_id}", summary="接收机器人Webhook")
async def receive_webhook(
    bot_schema_id: str,
    payload: WebhookPayload,
    request: Request,
    session: AsyncSession = Depends(get_admin_session),
):
    """
    接收来自GeWeAPI的Webhook回调

    - **bot_schema_id**: 机器人Schema标识符
    - **payload**: Webhook负载数据
    """
    # 验证Webhook来源
    await verify_webhook_source(request)

    try:
        # 解析Schema ID到bot_wxid
        # bot_schema_id格式: bot_wxid 或 gewe_app_id
        bot_wxid = None

        # 首先尝试按gewe_app_id查找
        stmt = select(BotInfo).where(BotInfo.gewe_app_id == payload.Appid)
        result = await session.execute(stmt)
        bot = result.scalar_one_or_none()

        if bot:
            bot_wxid = bot.bot_wxid
        else:
            # 如果按app_id找不到，尝试直接使用bot_schema_id作为bot_wxid
            if bot_schema_id.startswith("bot_"):
                bot_wxid = bot_schema_id[4:]  # 去掉'bot_'前缀
            else:
                bot_wxid = bot_schema_id

            # 验证bot_wxid是否存在
            stmt = select(BotInfo).where(BotInfo.bot_wxid == bot_wxid)
            result = await session.execute(stmt)
            bot = result.scalar_one_or_none()

            if not bot:
                logger.warning(
                    f"未找到机器人: schema_id={bot_schema_id}, app_id={payload.Appid}"
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
                )

        # 提取消息信息
        data = payload.Data
        msg_id = data.get("MsgId")
        new_msg_id = data.get("NewMsgId")
        from_wxid = (
            data.get("FromUserName", {}).get("string")
            if data.get("FromUserName")
            else None
        )
        to_wxid = (
            data.get("ToUserName", {}).get("string") if data.get("ToUserName") else None
        )

        # 使用机器人专用数据库存储原始回调数据
        async with get_bot_session(bot_wxid) as bot_session:
            raw_log = RawCallbackLog(
                bot_wxid=bot_wxid,
                gewe_appid=payload.Appid,
                type_name=payload.TypeName,
                msg_id=str(msg_id) if msg_id else None,
                new_msg_id=str(new_msg_id) if new_msg_id else None,
                from_wxid=from_wxid,
                to_wxid=to_wxid,
                raw_json_data=json.dumps(payload.model_dump(), ensure_ascii=False),
                processed=False,
            )

            bot_session.add(raw_log)
            await bot_session.commit()

            logger.info(
                f"Webhook消息已存储: bot={bot_wxid}, type={payload.TypeName}, msg_id={msg_id}"
            )

        # TODO: 分发给OpenGewe MessageFactory进行处理
        # client = await bot_client_manager.get_client(bot_wxid)
        # await client.message_factory.process(payload.model_dump())

        # TODO: 实时推送给前端WebSocket连接
        # await websocket_manager.broadcast_to_bot_subscribers(
        #     bot_wxid,
        #     {
        #         "type": "new_message",
        #         "data": payload.model_dump()
        #     }
        # )

        # 更新机器人最后在线时间
        bot.last_seen_at = datetime.now(timezone.utc)
        if not bot.is_online:
            bot.is_online = True
        await session.commit()

        return {"status": "ok", "message": "Webhook处理成功"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理Webhook失败: {e}")
        logger.error(f"Payload: {payload.model_dump()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Webhook处理失败"
        )


@router.get("/test/{bot_wxid}", summary="测试Webhook连接")
async def test_webhook(
    bot_wxid: str, session: AsyncSession = Depends(get_admin_session)
):
    """
    测试Webhook连接状态

    用于验证机器人与后台的连接是否正常
    """
    # 验证机器人是否存在
    stmt = select(BotInfo).where(BotInfo.bot_wxid == bot_wxid)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    try:
        # 检查最近的Webhook消息
        async with get_bot_session(bot_wxid) as bot_session:
            # 查询最近5条消息
            stmt = (
                select(RawCallbackLog)
                .where(RawCallbackLog.bot_wxid == bot_wxid)
                .order_by(RawCallbackLog.received_at.desc())
                .limit(5)
            )

            result = await bot_session.execute(stmt)
            recent_messages = result.scalars().all()

            webhook_status = {
                "bot_wxid": bot_wxid,
                "is_online": bot.is_online,
                "last_seen_at": bot.last_seen_at.isoformat()
                if bot.last_seen_at
                else None,
                "recent_message_count": len(recent_messages),
                "recent_messages": [
                    {
                        "id": msg.id,
                        "type_name": msg.type_name,
                        "received_at": msg.received_at.isoformat(),
                        "processed": msg.processed,
                    }
                    for msg in recent_messages
                ],
            }

            return webhook_status

    except Exception as e:
        logger.error(f"测试Webhook连接失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="测试连接失败"
        )


@router.post("/manual-trigger/{bot_wxid}", summary="手动触发消息处理")
async def manual_trigger_processing(
    bot_wxid: str, limit: int = 10, session: AsyncSession = Depends(get_admin_session)
):
    """
    手动触发未处理消息的处理

    用于调试或重新处理失败的消息
    """
    # 验证机器人是否存在
    stmt = select(BotInfo).where(BotInfo.bot_wxid == bot_wxid)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    try:
        processed_count = 0

        async with get_bot_session(bot_wxid) as bot_session:
            # 查询未处理的消息
            stmt = (
                select(RawCallbackLog)
                .where(
                    and_(
                        RawCallbackLog.bot_wxid == bot_wxid,
                        RawCallbackLog.processed is False,
                    )
                )
                .order_by(RawCallbackLog.received_at.asc())
                .limit(limit)
            )

            result = await bot_session.execute(stmt)
            unprocessed_messages = result.scalars().all()

            for message in unprocessed_messages:
                try:
                    # TODO: 重新处理消息
                    # payload = json.loads(message.raw_json_data)
                    # client = await bot_client_manager.get_client(bot_wxid)
                    # await client.message_factory.process(payload)

                    # 标记为已处理
                    message.processed = True
                    processed_count += 1

                except Exception as e:
                    logger.error(f"处理消息失败: {message.id}, error: {e}")

            await bot_session.commit()

            return {
                "message": f"成功处理 {processed_count} 条消息",
                "processed_count": processed_count,
                "total_unprocessed": len(unprocessed_messages),
            }

    except Exception as e:
        logger.error(f"手动触发处理失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="处理失败"
        )
