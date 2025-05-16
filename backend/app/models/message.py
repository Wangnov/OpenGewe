"""微信消息数据模型模块

定义微信消息的数据结构和操作方法。
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, delete, select

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DatabaseManager

# 获取日志记录器
logger = get_logger("WechatMessage")


class WechatMessage(Base):
    """微信消息模型

    存储来自微信的回调消息。
    """

    # 表名将自动生成为wechatmessage

    msg_id = Column(Integer, index=True, comment="消息唯一ID（整型）")
    sender_wxid = Column(String(40), index=True, comment="消息发送人wxid")
    from_wxid = Column(String(40), index=True, comment="消息来源wxid")
    msg_type = Column(Integer, comment="消息类型（整型编码）")
    content = Column(Text, comment="消息内容")
    timestamp = Column(DateTime, default=datetime.now, index=True, comment="消息时间戳")
    is_group = Column(Boolean, default=False, comment="是否群消息")

    @classmethod
    async def save_message(
        cls,
        msg_id: int,
        sender_wxid: str,
        from_wxid: str,
        msg_type: int,
        content: str,
        is_group: bool = False,
    ) -> bool:
        """保存消息到数据库

        Args:
            msg_id: 消息ID
            sender_wxid: 发送者ID
            from_wxid: 来源ID
            msg_type: 消息类型
            content: 消息内容
            is_group: 是否群消息

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                message = WechatMessage(
                    msg_id=msg_id,
                    sender_wxid=sender_wxid,
                    from_wxid=from_wxid,
                    msg_type=msg_type,
                    content=content,
                    is_group=is_group,
                    timestamp=datetime.now(),
                )
                session.add(message)
                await session.commit()
                logger.debug(f"已保存消息: {msg_id}")
                return True
            except Exception as e:
                logger.error(f"保存消息失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def get_messages(
        cls,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        sender_wxid: Optional[str] = None,
        from_wxid: Optional[str] = None,
        msg_type: Optional[int] = None,
        is_group: Optional[bool] = None,
        limit: int = 100,
    ) -> List["WechatMessage"]:
        """查询消息记录

        Args:
            start_time: 开始时间
            end_time: 结束时间
            sender_wxid: 发送者ID
            from_wxid: 来源ID
            msg_type: 消息类型
            is_group: 是否群消息
            limit: 最大返回数量

        Returns:
            List[WechatMessage]: 消息列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                query = (
                    select(WechatMessage)
                    .order_by(WechatMessage.timestamp.desc())
                    .limit(limit)
                )

                if start_time:
                    query = query.where(WechatMessage.timestamp >= start_time)
                if end_time:
                    query = query.where(WechatMessage.timestamp <= end_time)
                if sender_wxid:
                    query = query.where(WechatMessage.sender_wxid == sender_wxid)
                if from_wxid:
                    query = query.where(WechatMessage.from_wxid == from_wxid)
                if msg_type is not None:
                    query = query.where(WechatMessage.msg_type == msg_type)
                if is_group is not None:
                    query = query.where(WechatMessage.is_group == is_group)

                result = await session.execute(query)
                return result.scalars().all()
            except Exception as e:
                logger.error(f"查询消息失败: {e}")
                return []

    @classmethod
    async def cleanup_old_messages(cls, days: int = 3) -> bool:
        """清理指定天数前的旧消息

        Args:
            days: 保留天数，默认3天

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 计算指定天数前的时间
                cutoff_date = datetime.now() - timedelta(days=days)
                # 删除旧消息
                await session.execute(
                    delete(WechatMessage).where(WechatMessage.timestamp < cutoff_date)
                )
                await session.commit()
                logger.info(f"已清理{days}天前的旧消息")
                return True
            except Exception as e:
                logger.error(f"清理旧消息失败: {e}")
                await session.rollback()
                return False


class MessageCleanupTask:
    """消息自动清理任务

    定期清理旧消息，保持数据库大小可控。
    """

    def __init__(self, days: int = 3, interval: int = 86400):
        """初始化清理任务

        Args:
            days: 保留消息的天数，默认3天
            interval: 清理间隔(秒)，默认1天
        """
        self.days = days
        self.interval = interval
        self.task = None
        self.logger = get_logger("MessageCleanup")

    async def _cleanup_loop(self):
        """清理循环任务"""
        while True:
            try:
                await WechatMessage.cleanup_old_messages(self.days)
                self.logger.debug(f"下次消息清理将在{self.interval}秒后执行")
            except Exception as e:
                self.logger.error(f"执行消息清理任务时出错: {e}")
            # 等待下一次执行
            await asyncio.sleep(self.interval)

    def start(self):
        """启动清理任务"""
        if self.task is None or self.task.done():
            self.task = asyncio.create_task(self._cleanup_loop())
            self.logger.info(
                f"消息清理任务已启动 (保留{self.days}天的消息，每{self.interval}秒清理一次)"
            )

    async def stop(self):
        """停止清理任务"""
        if self.task and not self.task.done():
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            self.logger.info("消息清理任务已停止")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.stop()
