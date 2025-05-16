"""联系人数据模型模块

定义微信联系人的数据结构和操作方法。
"""

import json
import time
from typing import Dict, List, Optional, Any

from sqlalchemy import Column, String, Integer, Text, select
from sqlalchemy.sql.expression import or_

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DatabaseManager

# 获取日志记录器
logger = get_logger("Contact")


class Contact(Base):
    """联系人模型

    存储微信联系人信息，包括好友、群组、公众号等。
    """

    # 覆盖基类的id字段，使用wxid作为主键
    __table_args__ = {"extend_existing": True}
    id = None

    wxid = Column(String(40), primary_key=True, index=True, comment="微信ID")
    nickname = Column(String(255), index=True, comment="昵称")
    remark = Column(String(255), comment="备注名")
    avatar = Column(String(1024), comment="头像URL")
    big_head_img_url = Column(String(1024), comment="大头像URL")
    small_head_img_url = Column(String(1024), comment="小头像URL")
    alias = Column(String(255), comment="微信号")
    type = Column(String(20), index=True, comment="联系人类型: friend, group, official")
    region = Column(String(100), comment="地区")
    last_updated = Column(
        Integer, default=lambda: int(time.time()), comment="最后更新时间戳"
    )
    extra_data = Column(Text, comment="额外数据(JSON格式)")

    @property
    def is_group(self) -> bool:
        """是否为群聊"""
        return self.type == "group" or (self.wxid and self.wxid.endswith("@chatroom"))

    @property
    def is_official(self) -> bool:
        """是否为公众号"""
        return self.type == "official" or (self.wxid and self.wxid.startswith("gh_"))

    def get_extra_data(self) -> Dict[str, Any]:
        """获取额外数据字典"""
        if not self.extra_data:
            return {}
        try:
            return json.loads(self.extra_data)
        except Exception:
            logger.warning(f"解析联系人 {self.wxid} 的额外数据失败")
            return {}

    def set_extra_data(self, data: Dict[str, Any]) -> None:
        """设置额外数据"""
        self.extra_data = json.dumps(data, ensure_ascii=False)

    @staticmethod
    def determine_type(wxid: str) -> str:
        """根据wxid确定联系人类型"""
        if wxid.endswith("@chatroom"):
            return "group"
        elif wxid.startswith("gh_"):
            return "official"
        else:
            return "friend"

    @classmethod
    async def get_by_wxid(cls, wxid: str) -> Optional["Contact"]:
        """根据wxid获取联系人

        Args:
            wxid: 联系人的wxid

        Returns:
            Contact: 联系人对象，如果不存在则返回None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(
                    select(Contact).where(Contact.wxid == wxid)
                )
                return result.scalars().first()
            except Exception as e:
                logger.error(f"获取联系人失败: {e}")
                return None

    @classmethod
    async def search_contacts(
        cls,
        keyword: Optional[str] = None,
        contact_type: Optional[str] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List["Contact"]:
        """搜索联系人

        Args:
            keyword: 搜索关键词，匹配昵称、备注或微信号
            contact_type: 联系人类型 (friend, group, official)
            offset: 分页偏移量
            limit: 每页数量

        Returns:
            List[Contact]: 联系人列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                query = select(Contact)

                # 添加筛选条件
                if keyword:
                    query = query.where(
                        or_(
                            Contact.nickname.contains(keyword),
                            Contact.remark.contains(keyword),
                            Contact.alias.contains(keyword),
                            Contact.wxid.contains(keyword),
                        )
                    )

                if contact_type:
                    query = query.where(Contact.type == contact_type)

                # 添加排序和分页
                query = query.order_by(Contact.nickname).offset(offset).limit(limit)

                result = await session.execute(query)
                return result.scalars().all()
            except Exception as e:
                logger.error(f"搜索联系人失败: {e}")
                return []

    @classmethod
    async def get_all(
        cls, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> List["Contact"]:
        """获取所有联系人

        Args:
            offset: 分页偏移量
            limit: 每页数量

        Returns:
            List[Contact]: 联系人列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                query = select(Contact).order_by(Contact.nickname)

                if limit is not None:
                    query = query.limit(limit)
                    if offset is not None:
                        query = query.offset(offset)

                result = await session.execute(query)
                contacts = result.scalars().all()

                # 记录日志
                if offset is not None or limit is not None:
                    logger.info(
                        f"获取联系人列表 (offset={offset}, limit={limit}): 共{len(contacts)}条"
                    )
                else:
                    logger.info(f"获取全部联系人列表: 共{len(contacts)}条")

                return contacts
            except Exception as e:
                logger.error(f"获取联系人列表失败: {e}")
                return []

    @classmethod
    async def save(cls, contact_data: Dict[str, Any]) -> bool:
        """保存单个联系人

        Args:
            contact_data: 联系人数据字典

        Returns:
            bool: 是否保存成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 提取基本字段
                wxid = contact_data.get("wxid", "")
                if not wxid:
                    logger.error("保存联系人失败: 缺少wxid")
                    return False

                # 确定联系人类型
                contact_type = contact_data.get("type", "")
                if not contact_type:
                    contact_type = cls.determine_type(wxid)

                # 处理头像URL字段
                avatar = contact_data.get("avatar", "")
                big_head_img_url = contact_data.get(
                    "BigHeadImgUrl", ""
                ) or contact_data.get("big_head_img_url", "")
                small_head_img_url = contact_data.get(
                    "SmallHeadImgUrl", ""
                ) or contact_data.get("small_head_img_url", "")

                # 保持现有逻辑：如果avatar为空，则使用大头像或小头像
                if not avatar and big_head_img_url:
                    avatar = big_head_img_url
                elif not avatar and small_head_img_url:
                    avatar = small_head_img_url

                # 提取其他字段
                basic_fields = {
                    "nickname": contact_data.get("nickname", ""),
                    "remark": contact_data.get("remark", ""),
                    "avatar": avatar,
                    "big_head_img_url": big_head_img_url,
                    "small_head_img_url": small_head_img_url,
                    "alias": contact_data.get("alias", ""),
                    "type": contact_type,
                    "region": contact_data.get("region", ""),
                    "last_updated": int(time.time()),
                }

                # 提取额外字段
                extra_data = {}
                for key, value in contact_data.items():
                    if key not in [
                        "wxid",
                        "nickname",
                        "remark",
                        "avatar",
                        "big_head_img_url",
                        "small_head_img_url",
                        "BigHeadImgUrl",
                        "SmallHeadImgUrl",
                        "alias",
                        "type",
                        "region",
                        "last_updated",
                    ]:
                        extra_data[key] = value

                # 查询是否已存在
                result = await session.execute(
                    select(Contact).where(Contact.wxid == wxid)
                )
                contact = result.scalars().first()

                if contact:
                    # 更新现有联系人
                    for key, value in basic_fields.items():
                        setattr(contact, key, value)
                    contact.set_extra_data(extra_data)
                    logger.debug(f"更新联系人: {wxid}")
                else:
                    # 创建新联系人
                    contact = Contact(
                        wxid=wxid,
                        **basic_fields,
                        extra_data=json.dumps(extra_data, ensure_ascii=False),
                    )
                    session.add(contact)
                    logger.debug(f"创建联系人: {wxid}")

                await session.commit()
                return True
            except Exception as e:
                logger.error(f"保存联系人失败 ({wxid}): {e}")
                await session.rollback()
                return False

    @classmethod
    async def save_batch(cls, contacts: List[Dict[str, Any]]) -> bool:
        """批量保存联系人

        Args:
            contacts: 联系人数据列表

        Returns:
            bool: 是否全部保存成功
        """
        if not contacts:
            logger.warning("没有提供联系人数据")
            return True

        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                current_time = int(time.time())
                for contact_data in contacts:
                    # 提取wxid
                    wxid = contact_data.get("wxid", "")
                    if not wxid:
                        logger.warning(f"跳过缺少wxid的联系人: {contact_data}")
                        continue

                    # 确定联系人类型
                    contact_type = contact_data.get("type", "")
                    if not contact_type:
                        contact_type = cls.determine_type(wxid)

                    # 提取其他字段
                    avatar = contact_data.get("avatar", "")
                    big_head_img_url = contact_data.get(
                        "BigHeadImgUrl", ""
                    ) or contact_data.get("big_head_img_url", "")
                    small_head_img_url = contact_data.get(
                        "SmallHeadImgUrl", ""
                    ) or contact_data.get("small_head_img_url", "")

                    # 保持现有逻辑：如果avatar为空，则使用大头像或小头像
                    if not avatar and big_head_img_url:
                        avatar = big_head_img_url
                    elif not avatar and small_head_img_url:
                        avatar = small_head_img_url

                    # 提取其他字段
                    basic_fields = {
                        "nickname": contact_data.get("nickname", ""),
                        "remark": contact_data.get("remark", ""),
                        "avatar": avatar,
                        "big_head_img_url": big_head_img_url,
                        "small_head_img_url": small_head_img_url,
                        "alias": contact_data.get("alias", ""),
                        "type": contact_type,
                        "region": contact_data.get("region", ""),
                        "last_updated": current_time,
                    }

                    # 提取额外字段
                    extra_data = {}
                    for key, value in contact_data.items():
                        if key not in [
                            "wxid",
                            "nickname",
                            "remark",
                            "avatar",
                            "big_head_img_url",
                            "small_head_img_url",
                            "BigHeadImgUrl",
                            "SmallHeadImgUrl",
                            "alias",
                            "type",
                            "region",
                            "last_updated",
                        ]:
                            extra_data[key] = value

                    # 查询是否已存在
                    result = await session.execute(
                        select(Contact).where(Contact.wxid == wxid)
                    )
                    contact = result.scalars().first()

                    if contact:
                        # 更新现有联系人
                        for key, value in basic_fields.items():
                            setattr(contact, key, value)
                        contact.set_extra_data(extra_data)
                    else:
                        # 创建新联系人
                        contact = Contact(
                            wxid=wxid,
                            **basic_fields,
                            extra_data=json.dumps(extra_data, ensure_ascii=False),
                        )
                        session.add(contact)

                await session.commit()
                logger.success(f"成功保存{len(contacts)}个联系人")
                return True
            except Exception as e:
                logger.error(f"批量保存联系人失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def delete(cls, wxid: str) -> bool:
        """删除联系人

        Args:
            wxid: 联系人的wxid

        Returns:
            bool: 是否删除成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(
                    select(Contact).where(Contact.wxid == wxid)
                )
                contact = result.scalars().first()

                if contact:
                    await session.delete(contact)
                    await session.commit()
                    logger.info(f"删除联系人: {wxid}")
                    return True
                else:
                    logger.warning(f"要删除的联系人不存在: {wxid}")
                    return False
            except Exception as e:
                logger.error(f"删除联系人失败 ({wxid}): {e}")
                await session.rollback()
                return False

    @classmethod
    async def get_count(cls) -> int:
        """获取联系人总数

        Returns:
            int: 联系人总数
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                from sqlalchemy import func

                result = await session.execute(
                    select(func.count()).select_from(Contact)
                )
                return result.scalar() or 0
            except Exception as e:
                logger.error(f"获取联系人总数失败: {e}")
                return 0
