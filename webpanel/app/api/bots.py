"""
机器人管理相关API路由
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from loguru import logger

from ..core.database import get_admin_session, get_bot_session, db_manager
from ..core.security import get_current_active_user, require_superadmin
from ..models.bot import BotInfo, Contact, ContactType
from ..schemas.bot import (
    BotCreateRequest, 
    BotResponse, 
    BotListResponse, 
    BotUpdateRequest,
    BotStatusResponse,
    ContactResponse
)


router = APIRouter()


@router.get("", response_model=BotListResponse, summary="获取机器人列表")
async def get_bots(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_online: Optional[bool] = Query(None, description="在线状态过滤"),
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session)
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
                BotInfo.bot_wxid.ilike(search_pattern),
                BotInfo.gewe_app_id.ilike(search_pattern)
            )
        )
    
    if is_online is not None:
        conditions.append(BotInfo.is_online == is_online)
    
    # 查询总数
    count_stmt = select(func.count(BotInfo.bot_wxid))
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
        page_size=page_size
    )


@router.post("", response_model=BotResponse, summary="添加机器人")
async def create_bot(
    bot_data: BotCreateRequest,
    current_user: dict = Depends(require_superadmin),
    session: AsyncSession = Depends(get_admin_session)
):
    """
    添加新的机器人实例
    
    - **gewe_app_id**: GeWe应用ID
    - **gewe_token**: GeWe Token
    - **callback_url_override**: 回调URL覆盖（可选）
    """
    # TODO: 这里需要集成OpenGewe客户端来验证连接和获取机器人信息
    # 目前先创建基础记录
    
    # 检查是否已存在相同的gewe_app_id
    stmt = select(BotInfo).where(BotInfo.gewe_app_id == bot_data.gewe_app_id)
    result = await session.execute(stmt)
    existing_bot = result.scalar_one_or_none()
    
    if existing_bot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该GeWe应用ID已存在"
        )
    
    try:
        # TODO: 验证GeweClient连接
        # client = GeweClient(
        #     base_url="http://www.geweapi.com/gewe/v2/api",
        #     app_id=bot_data.gewe_app_id,
        #     token=bot_data.gewe_token,
        #     is_gewe=True
        # )
        # 
        # # 检查在线状态
        # online_status = await client.account.check_online()
        # if not online_status.get("data"):
        #     raise HTTPException(400, "机器人离线或配置错误")
        # 
        # # 获取机器人信息
        # profile = await client.personal.get_profile()
        # bot_wxid = profile["data"]["wxid"]
        # nickname = profile["data"]["nickname"]
        # avatar_url = profile["data"]["big_head_img_url"]
        
        # 临时使用虚拟数据，等集成OpenGewe后替换
        bot_wxid = f"bot_{bot_data.gewe_app_id}"
        nickname = f"机器人_{bot_data.gewe_app_id}"
        avatar_url = None
        
        # 创建机器人记录
        bot = BotInfo(
            bot_wxid=bot_wxid,
            gewe_app_id=bot_data.gewe_app_id,
            gewe_token=bot_data.gewe_token,
            nickname=nickname,
            avatar_url=avatar_url,
            callback_url_override=bot_data.callback_url_override,
            is_online=False  # 初始状态为离线
        )
        
        session.add(bot)
        await session.commit()
        await session.refresh(bot)
        
        # 创建机器人专用数据库Schema
        try:
            schema_name = await db_manager.create_bot_schema(bot_wxid)
            logger.info(f"机器人Schema创建成功: {schema_name}")
            
            # TODO: 启动后台同步任务
            # sync_contacts_task.delay(bot_wxid)
            
        except Exception as e:
            logger.error(f"创建机器人Schema失败: {e}")
            # 如果Schema创建失败，删除机器人记录
            await session.delete(bot)
            await session.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="创建机器人数据库失败"
            )
        
        logger.info(f"机器人创建成功: {bot_wxid} by {current_user['username']}")
        
        return BotResponse.model_validate(bot)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建机器人失败: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建机器人失败"
        )


@router.get("/{bot_wxid}", response_model=BotResponse, summary="获取机器人详情")
async def get_bot(
    bot_wxid: str,
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session)
):
    """获取指定机器人的详细信息"""
    stmt = select(BotInfo).where(BotInfo.bot_wxid == bot_wxid)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机器人不存在"
        )
    
    return BotResponse.model_validate(bot)


@router.put("/{bot_wxid}", response_model=BotResponse, summary="更新机器人")
async def update_bot(
    bot_wxid: str,
    bot_data: BotUpdateRequest,
    current_user: dict = Depends(require_superadmin),
    session: AsyncSession = Depends(get_admin_session)
):
    """更新机器人配置"""
    stmt = select(BotInfo).where(BotInfo.bot_wxid == bot_wxid)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机器人不存在"
        )
    
    # 更新字段
    update_data = bot_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bot, field, value)
    
    await session.commit()
    await session.refresh(bot)
    
    logger.info(f"机器人更新成功: {bot_wxid} by {current_user['username']}")
    
    return BotResponse.model_validate(bot)


@router.delete("/{bot_wxid}", summary="删除机器人")
async def delete_bot(
    bot_wxid: str,
    current_user: dict = Depends(require_superadmin),
    session: AsyncSession = Depends(get_admin_session)
):
    """删除机器人实例"""
    stmt = select(BotInfo).where(BotInfo.bot_wxid == bot_wxid)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机器人不存在"
        )
    
    try:
        # 删除机器人记录
        await session.delete(bot)
        await session.commit()
        
        # TODO: 清理机器人相关资源
        # 1. 停止GeweClient实例
        # 2. 删除数据库Schema（可选，也可以保留数据）
        # 3. 清理缓存等
        
        logger.info(f"机器人删除成功: {bot_wxid} by {current_user['username']}")
        
        return {"message": "机器人删除成功"}
        
    except Exception as e:
        logger.error(f"删除机器人失败: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除机器人失败"
        )


@router.get("/{bot_wxid}/status", response_model=BotStatusResponse, summary="获取机器人状态")
async def get_bot_status(
    bot_wxid: str,
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session)
):
    """获取机器人实时状态信息"""
    # 获取机器人基本信息
    stmt = select(BotInfo).where(BotInfo.bot_wxid == bot_wxid)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机器人不存在"
        )
    
    # TODO: 获取统计信息
    # 这里需要查询机器人专用数据库
    message_count_24h = 0
    contact_count = 0
    group_count = 0
    
    # 使用机器人专用数据库连接
    try:
        async with get_bot_session(bot_wxid) as bot_session:
            # 统计联系人数量
            contact_stmt = select(func.count(Contact.id)).where(
                and_(
                    Contact.bot_wxid == bot_wxid,
                    Contact.is_deleted == False
                )
            )
            contact_result = await bot_session.execute(contact_stmt)
            contact_count = contact_result.scalar() or 0
            
            # 统计群聊数量
            group_stmt = select(func.count(Contact.id)).where(
                and_(
                    Contact.bot_wxid == bot_wxid,
                    Contact.contact_type == ContactType.GROUP,
                    Contact.is_deleted == False
                )
            )
            group_result = await bot_session.execute(group_stmt)
            group_count = group_result.scalar() or 0
            
    except Exception as e:
        logger.warning(f"获取机器人统计信息失败: {e}")
        # 如果机器人数据库不存在，使用默认值
    
    return BotStatusResponse(
        bot_wxid=bot_wxid,
        is_online=bot.is_online,
        last_seen_at=bot.last_seen_at,
        message_count_24h=message_count_24h,
        contact_count=contact_count,
        group_count=group_count
    )


@router.get("/{bot_wxid}/contacts", response_model=List[ContactResponse], summary="获取机器人联系人")
async def get_bot_contacts(
    bot_wxid: str,
    contact_type: Optional[ContactType] = Query(None, description="联系人类型过滤"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session)
):
    """获取机器人的联系人列表"""
    # 先验证机器人是否存在
    stmt = select(BotInfo).where(BotInfo.bot_wxid == bot_wxid)
    result = await session.execute(stmt)
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="机器人不存在"
        )
    
    try:
        async with get_bot_session(bot_wxid) as bot_session:
            # 构建查询条件
            conditions = [
                Contact.bot_wxid == bot_wxid,
                Contact.is_deleted == False
            ]
            
            if contact_type:
                conditions.append(Contact.contact_type == contact_type)
            
            if search:
                search_pattern = f"%{search}%"
                conditions.append(
                    or_(
                        Contact.nickname.ilike(search_pattern),
                        Contact.contact_wxid.ilike(search_pattern),
                        Contact.remark.ilike(search_pattern)
                    )
                )
            
            # 查询联系人
            stmt = select(Contact).where(and_(*conditions)).order_by(Contact.last_updated.desc())
            
            # 分页
            offset = (page - 1) * page_size
            stmt = stmt.offset(offset).limit(page_size)
            
            result = await bot_session.execute(stmt)
            contacts = result.scalars().all()
            
            return [ContactResponse.model_validate(contact) for contact in contacts]
            
    except Exception as e:
        logger.error(f"获取机器人联系人失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取联系人信息失败"
        ) 