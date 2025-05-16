"""群成员数据模型模块

定义微信群成员的数据结构和操作方法。
"""

import json
import time
from typing import Dict, List, Optional, Any

from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    UniqueConstraint,
    select,
)
from sqlalchemy.sql import or_

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DatabaseManager

# 获取日志记录器
logger = get_logger("GroupMember")


class GroupMember(Base):
    """群成员模型

    存储微信群的成员信息。
    """

    __table_args__ = (
        UniqueConstraint("group_wxid", "member_wxid", name="uix_group_member"),
        {"extend_existing": True},
    )

    # 基础字段
    group_wxid = Column(String(40), index=True, nullable=False, comment="群聊wxid")
    member_wxid = Column(String(40), index=True, nullable=False, comment="成员wxid")
    nickname = Column(String(255), comment="成员昵称")
    display_name = Column(String(255), comment="群内显示名")
    avatar = Column(String(1024), comment="头像URL")
    big_head_img_url = Column(String(1024), comment="大头像URL")
    small_head_img_url = Column(String(1024), comment="小头像URL")
    inviter_wxid = Column(String(40), comment="邀请人wxid")
    join_time = Column(Integer, comment="加入时间")
    last_updated = Column(
        Integer, default=lambda: int(time.time()), comment="最后更新时间"
    )
    extra_data = Column(Text, comment="额外数据(JSON格式)")

    def get_extra_data(self) -> Dict[str, Any]:
        """获取额外数据字典"""
        if not self.extra_data:
            return {}
        try:
            return json.loads(self.extra_data)
        except Exception:
            logger.warning(
                f"解析群成员额外数据失败: {self.group_wxid}/{self.member_wxid}"
            )
            return {}

    def set_extra_data(self, data: Dict[str, Any]) -> None:
        """设置额外数据"""
        self.extra_data = json.dumps(data, ensure_ascii=False)

    @classmethod
    async def get_group_members(cls, group_wxid: str) -> List["GroupMember"]:
        """获取群的所有成员

        Args:
            group_wxid: 群聊的wxid

        Returns:
            List[GroupMember]: 群成员列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                query = (
                    select(GroupMember)
                    .where(GroupMember.group_wxid == group_wxid)
                    .order_by(GroupMember.nickname)
                )

                result = await session.execute(query)
                members = result.scalars().all()

                logger.info(f"获取群 {group_wxid} 成员列表: 共{len(members)}人")
                return members
            except Exception as e:
                logger.error(f"获取群 {group_wxid} 成员列表失败: {e}")
                return []

    @classmethod
    async def get_member(
        cls, group_wxid: str, member_wxid: str
    ) -> Optional["GroupMember"]:
        """获取群中的特定成员

        Args:
            group_wxid: 群聊的wxid
            member_wxid: 成员的wxid

        Returns:
            Optional[GroupMember]: 群成员对象，如果不存在则返回None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                query = select(GroupMember).where(
                    GroupMember.group_wxid == group_wxid,
                    GroupMember.member_wxid == member_wxid,
                )

                result = await session.execute(query)
                return result.scalars().first()
            except Exception as e:
                logger.error(f"获取群成员失败 ({group_wxid}/{member_wxid}): {e}")
                return None

    @classmethod
    async def get_member_groups(cls, member_wxid: str) -> List[str]:
        """获取成员所在的所有群

        Args:
            member_wxid: 成员的wxid

        Returns:
            List[str]: 群wxid列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                query = (
                    select(GroupMember.group_wxid)
                    .where(GroupMember.member_wxid == member_wxid)
                    .distinct()
                )

                result = await session.execute(query)
                groups = [row[0] for row in result.fetchall()]

                logger.info(f"获取成员 {member_wxid} 所在的群列表: 共{len(groups)}个群")
                return groups
            except Exception as e:
                logger.error(f"获取成员 {member_wxid} 所在的群列表失败: {e}")
                return []

    @classmethod
    async def save_member(cls, group_wxid: str, member_data: Dict[str, Any]) -> bool:
        """保存单个群成员

        Args:
            group_wxid: 群聊wxid
            member_data: 成员数据

        Returns:
            bool: 是否保存成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 提取成员wxid
                member_wxid = (
                    member_data.get("wxid")
                    or member_data.get("Wxid")
                    or member_data.get("UserName")
                    or ""
                )
                if not member_wxid:
                    logger.error(f"保存群成员失败: 缺少wxid ({group_wxid})")
                    return False

                # 提取基本字段
                nickname = None
                if member_data.get("NickName"):
                    nickname = member_data.get("NickName")
                elif member_data.get("nickname"):
                    nickname = member_data.get("nickname")

                # 提取显示名
                display_name = None
                if member_data.get("DisplayName"):
                    display_name = member_data.get("DisplayName")
                elif member_data.get("display_name"):
                    display_name = member_data.get("display_name")

                # 提取大头像URL
                big_head_img_url = None
                if member_data.get("BigHeadImgUrl"):
                    big_head_img_url = member_data.get("BigHeadImgUrl")
                elif member_data.get("big_head_img_url"):
                    big_head_img_url = member_data.get("big_head_img_url")

                # 提取小头像URL
                small_head_img_url = None
                if member_data.get("SmallHeadImgUrl"):
                    small_head_img_url = member_data.get("SmallHeadImgUrl")
                elif member_data.get("small_head_img_url"):
                    small_head_img_url = member_data.get("small_head_img_url")

                # 处理avatar字段，保持现有逻辑
                avatar = None
                if member_data.get("avatar"):
                    avatar = member_data.get("avatar")
                elif member_data.get("HeadImgUrl"):
                    avatar = member_data.get("HeadImgUrl")
                elif big_head_img_url:
                    avatar = big_head_img_url
                elif small_head_img_url:
                    avatar = small_head_img_url

                # 提取邀请人
                inviter_wxid = member_data.get("InviterUserName") or ""

                # 提取基本字段
                basic_fields = {
                    "nickname": nickname,
                    "display_name": display_name,
                    "avatar": avatar,
                    "big_head_img_url": big_head_img_url,
                    "small_head_img_url": small_head_img_url,
                    "inviter_wxid": inviter_wxid,
                    "last_updated": int(time.time()),
                }

                # 提取额外字段
                extra_data = {}
                for key, value in member_data.items():
                    if key not in [
                        "wxid",
                        "Wxid",
                        "UserName",
                        "NickName",
                        "nickname",
                        "DisplayName",
                        "display_name",
                        "BigHeadImgUrl",
                        "big_head_img_url",
                        "SmallHeadImgUrl",
                        "small_head_img_url",
                        "avatar",
                        "HeadImgUrl",
                        "InviterUserName",
                    ]:
                        extra_data[key] = value

                # 查询是否已存在
                result = await session.execute(
                    select(GroupMember).where(
                        GroupMember.group_wxid == group_wxid,
                        GroupMember.member_wxid == member_wxid,
                    )
                )
                member = result.scalars().first()

                if member:
                    # 更新现有成员
                    for key, value in basic_fields.items():
                        if value is not None:  # 只更新非None的值
                            setattr(member, key, value)
                    member.set_extra_data(extra_data)
                    logger.debug(f"更新群成员: {group_wxid}/{member_wxid}")
                else:
                    # 创建新成员
                    member = GroupMember(
                        group_wxid=group_wxid,
                        member_wxid=member_wxid,
                        **{k: v for k, v in basic_fields.items() if v is not None},
                        extra_data=json.dumps(extra_data, ensure_ascii=False),
                    )
                    session.add(member)
                    logger.debug(f"创建群成员: {group_wxid}/{member_wxid}")

                await session.commit()
                return True
            except Exception as e:
                logger.error(f"保存群成员失败 ({group_wxid}/{member_wxid}): {e}")
                await session.rollback()
                return False

    @classmethod
    async def save_members_batch(
        cls, group_wxid: str, members: List[Dict[str, Any]]
    ) -> bool:
        """批量保存群成员

        Args:
            group_wxid: 群聊wxid
            members: 成员数据列表

        Returns:
            bool: 是否保存成功
        """
        if not members:
            logger.warning(f"没有提供群 {group_wxid} 的成员数据")
            return True

        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                current_time = int(time.time())
                for member_data in members:
                    # 提取成员wxid
                    member_wxid = (
                        member_data.get("wxid")
                        or member_data.get("Wxid")
                        or member_data.get("UserName")
                        or ""
                    )
                    if not member_wxid:
                        logger.warning(f"跳过缺少wxid的群成员: {member_data}")
                        continue

                    # 提取基本字段
                    nickname = None
                    if member_data.get("NickName"):
                        nickname = member_data.get("NickName")
                    elif member_data.get("nickname"):
                        nickname = member_data.get("nickname")

                    # 提取显示名
                    display_name = None
                    if member_data.get("DisplayName"):
                        display_name = member_data.get("DisplayName")
                    elif member_data.get("display_name"):
                        display_name = member_data.get("display_name")

                    # 提取大头像URL
                    big_head_img_url = None
                    if member_data.get("BigHeadImgUrl"):
                        big_head_img_url = member_data.get("BigHeadImgUrl")
                    elif member_data.get("big_head_img_url"):
                        big_head_img_url = member_data.get("big_head_img_url")

                    # 提取小头像URL
                    small_head_img_url = None
                    if member_data.get("SmallHeadImgUrl"):
                        small_head_img_url = member_data.get("SmallHeadImgUrl")
                    elif member_data.get("small_head_img_url"):
                        small_head_img_url = member_data.get("small_head_img_url")

                    # 处理avatar字段，保持现有逻辑
                    avatar = None
                    if member_data.get("avatar"):
                        avatar = member_data.get("avatar")
                    elif member_data.get("HeadImgUrl"):
                        avatar = member_data.get("HeadImgUrl")
                    elif big_head_img_url:
                        avatar = big_head_img_url
                    elif small_head_img_url:
                        avatar = small_head_img_url

                    # 提取邀请人
                    inviter_wxid = member_data.get("InviterUserName") or ""

                    # 提取基本字段
                    basic_fields = {
                        "nickname": nickname,
                        "display_name": display_name,
                        "avatar": avatar,
                        "big_head_img_url": big_head_img_url,
                        "small_head_img_url": small_head_img_url,
                        "inviter_wxid": inviter_wxid,
                        "last_updated": current_time,
                    }

                    # 提取额外字段
                    extra_data = {}
                    for key, value in member_data.items():
                        if key not in [
                            "wxid",
                            "Wxid",
                            "UserName",
                            "NickName",
                            "nickname",
                            "DisplayName",
                            "display_name",
                            "BigHeadImgUrl",
                            "big_head_img_url",
                            "SmallHeadImgUrl",
                            "small_head_img_url",
                            "avatar",
                            "HeadImgUrl",
                            "InviterUserName",
                        ]:
                            extra_data[key] = value

                    # 查询是否已存在
                    result = await session.execute(
                        select(GroupMember).where(
                            GroupMember.group_wxid == group_wxid,
                            GroupMember.member_wxid == member_wxid,
                        )
                    )
                    member = result.scalars().first()

                    if member:
                        # 更新现有成员
                        for key, value in basic_fields.items():
                            if value is not None:  # 只更新非None的值
                                setattr(member, key, value)
                        member.set_extra_data(extra_data)
                    else:
                        # 创建新成员
                        member = GroupMember(
                            group_wxid=group_wxid,
                            member_wxid=member_wxid,
                            **{k: v for k, v in basic_fields.items() if v is not None},
                            extra_data=json.dumps(extra_data, ensure_ascii=False),
                        )
                        session.add(member)

                await session.commit()
                logger.success(f"成功保存群 {group_wxid} 的 {len(members)} 个成员")
                return True
            except Exception as e:
                logger.error(f"批量保存群 {group_wxid} 成员失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def delete_member(cls, group_wxid: str, member_wxid: str) -> bool:
        """从群中删除成员

        Args:
            group_wxid: 群聊wxid
            member_wxid: 成员wxid

        Returns:
            bool: 是否删除成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(
                    select(GroupMember).where(
                        GroupMember.group_wxid == group_wxid,
                        GroupMember.member_wxid == member_wxid,
                    )
                )
                member = result.scalars().first()

                if member:
                    await session.delete(member)
                    await session.commit()
                    logger.info(f"删除群成员: {group_wxid}/{member_wxid}")
                    return True
                else:
                    logger.warning(f"要删除的群成员不存在: {group_wxid}/{member_wxid}")
                    return False
            except Exception as e:
                logger.error(f"删除群成员失败 ({group_wxid}/{member_wxid}): {e}")
                await session.rollback()
                return False

    @classmethod
    async def delete_all_members(cls, group_wxid: str) -> bool:
        """删除群的所有成员

        Args:
            group_wxid: 群聊wxid

        Returns:
            bool: 是否删除成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 使用delete语句批量删除
                from sqlalchemy import delete

                stmt = delete(GroupMember).where(GroupMember.group_wxid == group_wxid)
                await session.execute(stmt)
                await session.commit()

                logger.info(f"删除群 {group_wxid} 的所有成员")
                return True
            except Exception as e:
                logger.error(f"删除群 {group_wxid} 的所有成员失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def get_group_member_count(cls, group_wxid: str) -> int:
        """获取群成员数量

        Args:
            group_wxid: 群聊wxid

        Returns:
            int: 群成员数量
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                from sqlalchemy import func

                result = await session.execute(
                    select(func.count())
                    .select_from(GroupMember)
                    .where(GroupMember.group_wxid == group_wxid)
                )
                return result.scalar() or 0
            except Exception as e:
                logger.error(f"获取群 {group_wxid} 成员数量失败: {e}")
                return 0

    @classmethod
    async def search_in_group(
        cls, group_wxid: str, keyword: str, offset: int = 0, limit: int = 100
    ) -> List["GroupMember"]:
        """在群内搜索成员

        Args:
            group_wxid: 群聊wxid
            keyword: 搜索关键词
            offset: 分页偏移量
            limit: 每页数量

        Returns:
            List[GroupMember]: 匹配的成员列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                query = (
                    select(GroupMember)
                    .where(
                        GroupMember.group_wxid == group_wxid,
                        or_(
                            GroupMember.nickname.contains(keyword),
                            GroupMember.display_name.contains(keyword),
                            GroupMember.member_wxid.contains(keyword),
                        ),
                    )
                    .order_by(GroupMember.nickname)
                    .offset(offset)
                    .limit(limit)
                )

                result = await session.execute(query)
                members = result.scalars().all()

                logger.info(
                    f"在群 {group_wxid} 中搜索 '{keyword}': 找到{len(members)}个匹配成员"
                )
                return members
            except Exception as e:
                logger.error(f"搜索群成员失败 ({group_wxid}, '{keyword}'): {e}")
                return []
