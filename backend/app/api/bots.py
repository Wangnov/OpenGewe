"""
机器人管理相关API路由
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from ..core.session_manager import get_admin_session, bot_session, session_manager
from ..core.security import get_current_active_user, require_superadmin
from ..models.bot import BotInfo, Contact, ContactType
from ..schemas.bot import (
    BotCreateRequest,
    BotResponse,
    BotListResponse,
    BotUpdateRequest,
    BotStatusResponse,
    ContactResponse,
)
from ..services.bot_manager import BotClientManager
from ..services.bot_profile_manager import BotProfileManager
from opengewe.client import GeweClient
from opengewe.logger import init_default_logger, get_logger
from ..utils.timezone_utils import to_app_timezone
from datetime import datetime, timezone

init_default_logger()
logger = get_logger(__name__)


router = APIRouter()


@router.get("", response_model=BotListResponse, summary="获取机器人列表")
async def get_bots(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_online: Optional[bool] = Query(None, description="在线状态过滤"),
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
):
    """
    获取机器人列表

    - **page**: 页码（从1开始）
    - **page_size**: 每页大小（1-100）
    - **search**: 搜索关键词（匹配昵称或微信ID）
    - **is_online**: 在线状态过滤
    """
    # 构建查询条件
    conditions = []

    if search:
        search_pattern = f"%{search}%"
        conditions.append(
            or_(
                BotInfo.nickname.ilike(search_pattern),
                BotInfo.gewe_app_id.ilike(search_pattern),
            )
        )

    if is_online is not None:
        conditions.append(BotInfo.is_online == is_online)

    # 查询总数
    count_stmt = select(func.count(BotInfo.gewe_app_id))
    if conditions:
        count_stmt = count_stmt.where(and_(*conditions))

    count_result = await session.execute(count_stmt)
    total = count_result.scalar()

    # 查询数据
    stmt = select(BotInfo).order_by(BotInfo.created_at.desc())
    if conditions:
        stmt = stmt.where(and_(*conditions))

    # 分页
    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)

    result = await session.execute(stmt)
    bots = result.scalars().all()

    return BotListResponse(
        bots=[BotResponse.model_validate(bot) for bot in bots],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=BotResponse, summary="添加机器人")
async def create_bot(
    bot_data: BotCreateRequest,
    current_user: dict = Depends(require_superadmin),
    session: AsyncSession = Depends(get_admin_session),
):
    """
    添加新的机器人实例

    - **gewe_app_id**: GeWe应用ID
    - **gewe_token**: GeWe Token
    - **base_url**: client URL基础路径
    - **callback_url_override**: 回调URL覆盖（可选）
    """
    # 检查是否已存在相同的gewe_app_id
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == bot_data.gewe_app_id)
    result = await session.execute(stmt)
    existing_bot = result.scalar_one_or_none()

    if existing_bot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="该gewe_app_id已存在"
        )

    try:
        # 创建机器人记录（初始状态，个人信息将通过API获取）
        current_time = to_app_timezone(datetime.now(timezone.utc))

        bot = BotInfo(
            gewe_app_id=bot_data.gewe_app_id,
            gewe_token=bot_data.gewe_token,
            base_url=bot_data.base_url,
            nickname=None,  # 将通过API获取
            avatar_url=None,  # 将通过API获取
            callback_url_override=bot_data.callback_url_override,
            is_online=True,  # 初始状态为在线
            last_seen_at=current_time,  # 设置初始在线时间
        )

        session.add(bot)
        await session.commit()
        await session.refresh(bot)

        # 创建机器人专用数据库Schema
        try:
            schema_name = await session_manager.create_bot_schema(bot_data.gewe_app_id)
            logger.info(f"机器人Schema创建成功: {schema_name}")

        except Exception as e:
            logger.error(f"创建机器人Schema失败: {e}")
            # 如果Schema创建失败，删除机器人记录
            await session.delete(bot)
            await session.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="创建机器人数据库失败",
            )

        # 获取机器人客户端管理器实例并获取个人信息
        try:
            bot_manager = BotClientManager()

            # 获取唯一的客户端实例
            client = await bot_manager.get_client(bot_data.gewe_app_id, session)

            if not client:
                logger.warning(f"无法获取机器人客户端: {bot_data.gewe_app_id}")
            else:
                # 调用fetch_and_update_profile更新机器人信息
                profile_data = await BotProfileManager.fetch_and_update_profile(
                    client, bot_data.gewe_app_id, session
                )

                if profile_data:
                    # 重新查询更新后的机器人信息
                    await session.refresh(bot)
                    logger.info(f"机器人个人信息获取成功: {bot_data.gewe_app_id}")
                else:
                    logger.warning(f"机器人个人信息获取失败: {bot_data.gewe_app_id}")

        except Exception as e:
            logger.error(f"获取机器人个人信息失败: {e}")
            # 个人信息获取失败不影响机器人创建，只记录警告

        logger.info(
            f"机器人创建成功: {bot_data.gewe_app_id} by {current_user['username']}"
        )

        return BotResponse.model_validate(bot)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建机器人失败: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="创建机器人失败"
        )


@router.get("/{gewe_app_id}", response_model=BotResponse, summary="获取机器人详情")
async def get_bot(
    gewe_app_id: str,
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
):
    """获取指定机器人的详细信息"""
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    return BotResponse.model_validate(bot)


@router.put("/{gewe_app_id}", response_model=BotResponse, summary="更新机器人")
async def update_bot(
    gewe_app_id: str,
    bot_data: BotUpdateRequest,
    current_user: dict = Depends(require_superadmin),
    session: AsyncSession = Depends(get_admin_session),
):
    """更新机器人配置"""
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    # 更新字段
    update_data = bot_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bot, field, value)

    await session.commit()
    await session.refresh(bot)

    logger.info(f"机器人更新成功: {gewe_app_id} by {current_user['username']}")

    return BotResponse.model_validate(bot)


@router.delete("/{gewe_app_id}", summary="删除机器人")
async def delete_bot(
    gewe_app_id: str,
    current_user: dict = Depends(require_superadmin),
    session: AsyncSession = Depends(get_admin_session),
):
    """删除机器人实例"""
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    try:
        # 删除机器人记录
        await session.delete(bot)
        await session.commit()

        logger.info(f"机器人记录已从数据库删除: {gewe_app_id}")

        # 删除机器人专用的数据库Schema
        schema_deleted = await session_manager.drop_bot_schema(gewe_app_id)
        if not schema_deleted:
            # 即使schema删除失败，也认为机器人删除成功，但记录一个警告
            logger.warning(f"机器人 {gewe_app_id} 的数据库Schema删除失败，请手动清理")

        logger.info(f"机器人删除成功: {gewe_app_id} by {current_user['username']}")

        return {"message": "机器人删除成功"}

    except Exception as e:
        logger.error(f"删除机器人失败: {e}", exc_info=True)
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除机器人失败"
        )


@router.get(
    "/{gewe_app_id}/status", response_model=BotStatusResponse, summary="获取机器人状态"
)
async def get_bot_status(
    gewe_app_id: str,
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
):
    """获取机器人实时状态信息"""
    # 获取机器人基本信息
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    # 初始化统计信息
    message_count_24h = 0
    contact_count = 0
    group_count = 0

    # 使用机器人专用数据库连接
    try:
        async with bot_session(bot.gewe_app_id) as bot_session_obj:
            # 统计联系人数量
            contact_stmt = select(func.count(Contact.id)).where(
                and_(Contact.gewe_app_id == gewe_app_id, not Contact.is_deleted)
            )
            contact_result = await bot_session_obj.execute(contact_stmt)
            contact_count = contact_result.scalar() or 0

            # 统计群聊数量
            group_stmt = select(func.count(Contact.id)).where(
                and_(
                    Contact.gewe_app_id == gewe_app_id,
                    Contact.contact_type == ContactType.GROUP,
                    not Contact.is_deleted,
                )
            )
            group_result = await bot_session_obj.execute(group_stmt)
            group_count = group_result.scalar() or 0

    except Exception as e:
        logger.warning(f"获取机器人统计信息失败: {e}")
        # 如果机器人数据库不存在，使用默认值

    return BotStatusResponse(
        gewe_app_id=gewe_app_id,
        is_online=bot.is_online,
        last_seen_at=bot.last_seen_at,
        message_count_24h=message_count_24h,
        contact_count=contact_count,
        group_count=group_count,
    )


@router.get(
    "/{gewe_app_id}/contacts",
    response_model=List[ContactResponse],
    summary="获取机器人联系人",
)
async def get_bot_contacts(
    gewe_app_id: str,
    contact_type: Optional[ContactType] = Query(None, description="联系人类型过滤"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
):
    """获取机器人的联系人列表"""
    # 先验证机器人是否存在
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    try:
        async with bot_session(bot.gewe_app_id) as bot_session_obj:
            # 构建查询条件
            conditions = [
                Contact.gewe_app_id == gewe_app_id,
                Contact.is_deleted is False,
            ]

            if contact_type:
                conditions.append(Contact.contact_type == contact_type)

            if search:
                search_pattern = f"%{search}%"
                conditions.append(
                    or_(
                        Contact.nickname.ilike(search_pattern),
                        Contact.contact_wxid.ilike(search_pattern),
                        Contact.remark.ilike(search_pattern),
                    )
                )

            # 查询联系人
            stmt = (
                select(Contact)
                .where(and_(*conditions))
                .order_by(Contact.last_updated.desc())
            )

            # 分页
            offset = (page - 1) * page_size
            stmt = stmt.offset(offset).limit(page_size)

            result = await bot_session_obj.execute(stmt)
            contacts = result.scalars().all()

            return [ContactResponse.model_validate(contact) for contact in contacts]

    except Exception as e:
        logger.error(f"获取机器人联系人失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取联系人信息失败",
        )


@router.post("/check-online", summary="测试机器人连接")
async def check_bot_online(
    bot_data: BotCreateRequest,
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
):
    """
    测试机器人连接

    使用提供的凭据创建临时客户端并检查是否能够成功连接
    """
    try:
        # 创建临时客户端
        client = GeweClient(
            base_url=bot_data.base_url,
            app_id=bot_data.gewe_app_id,
            token=bot_data.gewe_token,
            debug=False,
        )

        # 调用account.check_online()方法检查连接
        result = await client.account.check_online()

        # 检查返回结果
        if result.get("ret") == 200 and result.get("data") is True:
            # 连接成功，更新机器人的last_seen_at时间（如果机器人已存在）
            try:
                stmt = select(BotInfo).where(
                    BotInfo.gewe_app_id == bot_data.gewe_app_id
                )
                db_result = await session.execute(stmt)
                bot = db_result.scalar_one_or_none()

                if bot:
                    bot.last_seen_at = to_app_timezone(
                        datetime.now(timezone.utc))
                    if not bot.is_online:
                        bot.is_online = True
                    await session.commit()
                    logger.info(
                        f"连接测试成功，已更新机器人在线状态: {bot_data.gewe_app_id}"
                    )
            except Exception as e:
                logger.warning(f"更新机器人在线状态失败: {e}")
                # 更新失败不影响连接测试结果

            return {"ret": 200, "msg": "操作成功", "data": True}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="连接测试失败: " + result.get("msg", "未知错误"),
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"机器人连接测试失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="连接测试失败: " + str(e),
        )


@router.put(
    "/{gewe_app_id}/update", response_model=BotResponse, summary="更新机器人个人信息"
)
async def update_bot_profile(
    gewe_app_id: str,
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
):
    """
    更新机器人个人信息

    从GeWe服务器获取机器人的个人信息并更新到数据库
    """
    # 先验证机器人是否存在
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()

    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="机器人不存在"
        )

    try:
        # 获取机器人客户端管理器实例
        bot_manager = BotClientManager()

        # 获取唯一的客户端实例
        client = await bot_manager.get_client(gewe_app_id, session)

        if not client:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="无法获取机器人客户端",
            )

        # 调用fetch_and_update_profile更新机器人信息
        profile_data = await BotProfileManager.fetch_and_update_profile(
            client, gewe_app_id, session
        )

        if not profile_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="获取机器人个人信息失败",
            )

        # 重新查询更新后的机器人信息
        await session.refresh(bot)

        logger.info(
            f"机器人个人信息更新成功: {gewe_app_id} by {current_user['username']}"
        )

        return BotResponse.model_validate(bot)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新机器人个人信息失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新机器人个人信息失败",
        )
