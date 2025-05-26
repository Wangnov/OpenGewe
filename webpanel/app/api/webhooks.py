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


@router.post("/callback", summary="接收机器人Webhook")
async def receive_webhook(
    payload: WebhookPayload,
    request: Request,
    session: AsyncSession = Depends(get_admin_session),
):
    """
    接收来自GeWeAPI的Webhook回调

    - **payload**: Webhook负载数据，包含Appid字段用于标识机器人
    """
    # 验证Webhook来源
    await verify_webhook_source(request)

    try:
        # 从payload中提取gewe_app_id
        gewe_app_id = payload.Appid

        if not gewe_app_id:
            logger.warning("Webhook payload中缺少Appid字段")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="缺少必需的Appid字段"
            )

        # 查找机器人信息
        stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
        result = await session.execute(stmt)
        bot = result.scalar_one_or_none()

        if not bot:
            logger.warning(f"未找到机器人: gewe_app_id={gewe_app_id}")
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
        async with get_bot_session(gewe_app_id) as bot_session:
            raw_log = RawCallbackLog(
                bot_wxid=bot.bot_wxid,
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
                f"Webhook消息已存储: gewe_app_id={gewe_app_id}, bot_wxid={bot.bot_wxid}, type={payload.TypeName}, msg_id={msg_id}"
            )

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


@router.get("/test/{gewe_app_id}", summary="测试Webhook连接")
async def test_webhook(
    gewe_app_id: str, session: AsyncSession = Depends(get_admin_session)
):
    """
    测试Webhook连接状态

    用于验证机器人与后台的连接是否正常
    """
    # 验证机器人是否存在
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    try:
        # 检查最近的Webhook消息
        async with get_bot_session(gewe_app_id) as bot_session:
            # 查询最近5条消息
            stmt = (
                select(RawCallbackLog)
                .where(RawCallbackLog.bot_wxid == bot.bot_wxid)
                .order_by(RawCallbackLog.received_at.desc())
                .limit(5)
            )

            result = await bot_session.execute(stmt)
            recent_messages = result.scalars().all()

            webhook_status = {
                "gewe_app_id": gewe_app_id,
                "bot_wxid": bot.bot_wxid,
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


@router.post("/manual-trigger/{gewe_app_id}", summary="手动触发消息处理")
async def manual_trigger_processing(
    gewe_app_id: str,
    limit: int = 10,
    session: AsyncSession = Depends(get_admin_session),
):
    """
    手动触发未处理消息的处理

    用于调试或重新处理失败的消息
    """
    # 验证机器人是否存在
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    try:
        processed_count = 0

        async with get_bot_session(gewe_app_id) as bot_session:
            # 查询未处理的消息
            stmt = (
                select(RawCallbackLog)
                .where(
                    and_(
                        RawCallbackLog.bot_wxid == bot.bot_wxid,
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
                    # 标记为已处理（实际处理逻辑需要与OpenGewe集成）
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
