"""
机器人个人资料管理器

负责获取和更新机器人的个人资料信息
"""

from typing import Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from opengewe.client import GeweClient
from ..models.bot import BotInfo
from .session_manager import admin_session
from .timezone_utils import utc_now, to_app_timezone


class BotProfileManager:
    """机器人个人资料管理器"""

    @staticmethod
    async def fetch_and_update_profile(
        client: GeweClient, gewe_app_id: str, session: Optional[AsyncSession] = None
    ) -> Optional[Dict[str, Any]]:
        """
        获取并更新机器人个人资料

        Args:
            client: GeweClient实例
            gewe_app_id: GeWe应用ID
            session: 可选的数据库session

        Returns:
            Optional[Dict[str, Any]]: 个人资料数据，如果失败则返回None
        """
        try:
            # 调用opengewe.personal.get_profile获取个人资料
            profile_response = await client.personal.get_profile()

            if profile_response.get("ret") != 200:
                logger.error(
                    f"获取机器人个人资料失败: gewe_app_id={gewe_app_id}, "
                    f"response={profile_response}"
                )
                return None

            profile_data = profile_response.get("data", {})

            # 更新数据库中的机器人信息
            await BotProfileManager._update_bot_profile_in_db(
                gewe_app_id, profile_data, session
            )

            logger.info(
                f"机器人个人资料更新成功: gewe_app_id={gewe_app_id}, "
                f"wxid={profile_data.get('wxid')}, "
                f"nickname={profile_data.get('nickName')}"
            )

            return profile_data

        except Exception as e:
            logger.error(
                f"获取机器人个人资料异常: gewe_app_id={gewe_app_id}, 错误: {e}",
                exc_info=True,
            )
            return None

    @staticmethod
    async def _update_bot_profile_in_db(
        gewe_app_id: str,
        profile_data: Dict[str, Any],
        session: Optional[AsyncSession] = None,
    ) -> None:
        """
        更新数据库中的机器人个人资料

        Args:
            gewe_app_id: GeWe应用ID
            profile_data: 个人资料数据
            session: 可选的数据库session
        """
        if session is not None:
            await BotProfileManager._update_profile_with_session(
                gewe_app_id, profile_data, session
            )
        else:
            async with admin_session() as new_session:
                await BotProfileManager._update_profile_with_session(
                    gewe_app_id, profile_data, new_session
                )

    @staticmethod
    async def _update_profile_with_session(
        gewe_app_id: str, profile_data: Dict[str, Any], session: AsyncSession
    ) -> None:
        """使用指定session更新机器人个人资料"""
        # 查询现有的机器人信息
        stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
        result = await session.execute(stmt)
        bot = result.scalar_one_or_none()

        if not bot:
            logger.warning(f"未找到机器人信息: gewe_app_id={gewe_app_id}")
            return

        # 更新个人资料字段
        bot.wxid = profile_data.get("wxid")
        bot.nickname = profile_data.get("nickName")
        bot.mobile = profile_data.get("mobile")
        bot.uin = profile_data.get("uin")
        bot.sex = profile_data.get("sex")
        bot.province = profile_data.get("province")
        bot.city = profile_data.get("city")
        bot.signature = profile_data.get("signature")
        bot.country = profile_data.get("country")
        bot.reg_country = profile_data.get("regCountry")
        bot.alias = profile_data.get("alias")

        # 更新头像URL
        bot.big_head_img_url = profile_data.get("bigHeadImgUrl")
        bot.small_head_img_url = profile_data.get("smallHeadImgUrl")
        bot.sns_bg_img = profile_data.get("snsBgImg")

        # 更新时间戳
        bot.profile_updated_at = to_app_timezone(utc_now())
        bot.updated_at = to_app_timezone(utc_now())

        await session.commit()

        logger.debug(f"数据库中的机器人个人资料已更新: gewe_app_id={gewe_app_id}")

    @staticmethod
    async def get_profile_from_db(gewe_app_id: str) -> Optional[Dict[str, Any]]:
        """
        从数据库获取机器人个人资料

        Args:
            gewe_app_id: GeWe应用ID

        Returns:
            Optional[Dict[str, Any]]: 个人资料数据，如果不存在则返回None
        """
        try:
            async with admin_session() as session:
                stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
                result = await session.execute(stmt)
                bot = result.scalar_one_or_none()

                if not bot:
                    return None

                return {
                    "wxid": bot.wxid,
                    "nickname": bot.nickname,
                    "mobile": bot.mobile,
                    "uin": bot.uin,
                    "sex": bot.sex,
                    "province": bot.province,
                    "city": bot.city,
                    "signature": bot.signature,
                    "country": bot.country,
                    "reg_country": bot.reg_country,
                    "alias": bot.alias,
                    "big_head_img_url": bot.big_head_img_url,
                    "small_head_img_url": bot.small_head_img_url,
                    "sns_bg_img": bot.sns_bg_img,
                    "profile_updated_at": bot.profile_updated_at.isoformat()
                    if bot.profile_updated_at
                    else None,
                }

        except Exception as e:
            logger.error(
                f"从数据库获取机器人个人资料失败: gewe_app_id={gewe_app_id}, 错误: {e}",
                exc_info=True,
            )
            return None

    @staticmethod
    async def should_update_profile(
        gewe_app_id: str,
        max_age_hours: int = 24,
        session: Optional[AsyncSession] = None,
    ) -> bool:
        """
        检查是否需要更新个人资料

        Args:
            gewe_app_id: GeWe应用ID
            max_age_hours: 个人资料最大有效期（小时）
            session: 可选的数据库session

        Returns:
            bool: 是否需要更新
        """
        try:
            if session is not None:
                return await BotProfileManager._check_profile_update_with_session(
                    gewe_app_id, max_age_hours, session
                )
            else:
                async with admin_session() as new_session:
                    return await BotProfileManager._check_profile_update_with_session(
                        gewe_app_id, max_age_hours, new_session
                    )

        except Exception as e:
            logger.error(
                f"检查个人资料更新状态失败: gewe_app_id={gewe_app_id}, 错误: {e}",
                exc_info=True,
            )
            return True  # 出错时默认需要更新

    @staticmethod
    async def _check_profile_update_with_session(
        gewe_app_id: str, max_age_hours: int, session: AsyncSession
    ) -> bool:
        """使用指定session检查是否需要更新个人资料"""
        stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
        result = await session.execute(stmt)
        bot = result.scalar_one_or_none()

        if not bot or not bot.profile_updated_at:
            return True

        # 检查个人资料是否过期
        now = to_app_timezone(utc_now())
        # 确保profile_updated_at有时区信息，避免时区相关的减法错误
        profile_updated_at_with_tz = to_app_timezone(bot.profile_updated_at)
        age = now - profile_updated_at_with_tz

        return age.total_seconds() > (max_age_hours * 3600)
