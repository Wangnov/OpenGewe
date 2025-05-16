"""微信机器人数据模型模块

定义微信机器人账号的数据结构和操作方法。
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any

from sqlalchemy import Column, String, Boolean, Text, DateTime, select, update, delete

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DatabaseManager

# 获取日志记录器
logger = get_logger("Robot")


class Robot(Base):
    """微信机器人模型

    存储微信机器人账号的信息和状态。
    """

    app_id = Column(
        String(100), unique=True, index=True, nullable=False, comment="机器人唯一ID"
    )
    token = Column(String(255), nullable=True, comment="微信登录token")
    name = Column(String(100), nullable=True, comment="机器人名称")
    wechat_id = Column(String(100), nullable=True, comment="微信ID")
    device_name = Column(String(100), nullable=True, comment="设备名称")
    status = Column(String(20), default="offline", comment="机器人状态")
    avatar_url = Column(String(255), nullable=True, comment="头像URL")
    login_time = Column(DateTime, nullable=True, comment="最后登录时间")
    is_active = Column(Boolean, default=True, comment="是否活跃")
    config = Column(Text, nullable=True, comment="机器人配置(JSON格式)")

    @property
    def config_dict(self) -> Dict[str, Any]:
        """获取配置字典

        Returns:
            Dict[str, Any]: 配置字典
        """
        if not self.config:
            return {}
        try:
            return json.loads(self.config)
        except json.JSONDecodeError:
            logger.error(f"机器人 {self.app_id} 的配置解析失败")
            return {}

    @config_dict.setter
    def config_dict(self, value: Dict[str, Any]) -> None:
        """设置配置字典

        Args:
            value: 配置字典
        """
        self.config = json.dumps(value, ensure_ascii=False)

    def to_dict(self) -> Dict[str, Any]:
        """将模型转换为字典

        Returns:
            Dict[str, Any]: 模型字典表示
        """
        result = super().to_dict()
        result["config"] = self.config_dict
        return result

    @classmethod
    async def get_all(cls) -> List["Robot"]:
        """获取所有机器人

        Returns:
            List[Robot]: 机器人列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(select(Robot))
                return result.scalars().all()
            except Exception as e:
                logger.error(f"获取所有机器人失败: {e}")
                return []

    @classmethod
    async def get_active(cls) -> List["Robot"]:
        """获取所有活跃的机器人

        Returns:
            List[Robot]: 活跃的机器人列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(
                    select(Robot).where(Robot.is_active == True)
                )
                return result.scalars().all()
            except Exception as e:
                logger.error(f"获取活跃机器人失败: {e}")
                return []

    @classmethod
    async def get_by_app_id(cls, app_id: str) -> Optional["Robot"]:
        """通过app_id获取机器人

        Args:
            app_id: 机器人唯一ID

        Returns:
            Optional[Robot]: 机器人对象，如果不存在则为None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(
                    select(Robot).where(Robot.app_id == app_id)
                )
                return result.scalars().first()
            except Exception as e:
                logger.error(f"通过app_id获取机器人失败: {e}")
                return None

    @classmethod
    async def create(
        cls,
        app_id: str,
        token: Optional[str] = None,
        name: Optional[str] = None,
        wechat_id: Optional[str] = None,
        device_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> Optional["Robot"]:
        """创建新机器人

        Args:
            app_id: 机器人唯一ID
            token: 微信登录token
            name: 机器人名称
            wechat_id: 微信ID
            device_name: 设备名称
            avatar_url: 头像URL
            config: 配置信息

        Returns:
            Optional[Robot]: 创建的机器人对象，失败则为None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 检查是否已存在
                existing = await cls.get_by_app_id(app_id)
                if existing:
                    logger.warning(f"机器人 {app_id} 已存在")
                    return existing

                # 创建新机器人
                robot = Robot(
                    app_id=app_id,
                    token=token,
                    name=name,
                    wechat_id=wechat_id,
                    device_name=device_name,
                    avatar_url=avatar_url,
                    status="offline",
                    is_active=True,
                )

                # 设置配置
                if config:
                    robot.config_dict = config

                session.add(robot)
                await session.commit()
                await session.refresh(robot)
                logger.info(f"机器人 {app_id} 创建成功")
                return robot
            except Exception as e:
                logger.error(f"创建机器人失败: {e}")
                await session.rollback()
                return None

    @classmethod
    async def update_token(cls, app_id: str, token: str) -> bool:
        """更新机器人token

        Args:
            app_id: 机器人唯一ID
            token: 新token

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                await session.execute(
                    update(Robot).where(Robot.app_id == app_id).values(token=token)
                )
                await session.commit()
                logger.debug(f"机器人 {app_id} token已更新")
                return True
            except Exception as e:
                logger.error(f"更新机器人token失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def update_status(cls, app_id: str, status: str) -> bool:
        """更新机器人状态

        Args:
            app_id: 机器人唯一ID
            status: 新状态

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 如果状态为online，同时更新登录时间
                values = {"status": status}
                if status == "online":
                    values["login_time"] = datetime.now()

                await session.execute(
                    update(Robot).where(Robot.app_id == app_id).values(**values)
                )
                await session.commit()
                logger.info(f"机器人 {app_id} 状态已更新为 {status}")
                return True
            except Exception as e:
                logger.error(f"更新机器人状态失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def update_profile(
        cls,
        app_id: str,
        name: Optional[str] = None,
        wechat_id: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> bool:
        """更新机器人资料

        Args:
            app_id: 机器人唯一ID
            name: 名称
            wechat_id: 微信ID
            avatar_url: 头像URL

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 构建更新值
                values = {}
                if name is not None:
                    values["name"] = name
                if wechat_id is not None:
                    values["wechat_id"] = wechat_id
                if avatar_url is not None:
                    values["avatar_url"] = avatar_url

                # 如果没有更新值，直接返回
                if not values:
                    return True

                await session.execute(
                    update(Robot).where(Robot.app_id == app_id).values(**values)
                )
                await session.commit()
                logger.debug(f"机器人 {app_id} 资料已更新")
                return True
            except Exception as e:
                logger.error(f"更新机器人资料失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def toggle_active(cls, app_id: str, is_active: bool) -> bool:
        """切换机器人活跃状态

        Args:
            app_id: 机器人唯一ID
            is_active: 是否活跃

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                await session.execute(
                    update(Robot)
                    .where(Robot.app_id == app_id)
                    .values(is_active=is_active)
                )
                await session.commit()

                status = "活跃" if is_active else "禁用"
                logger.info(f"机器人 {app_id} 已设置为{status}")
                return True
            except Exception as e:
                logger.error(f"切换机器人活跃状态失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def delete_by_app_id(cls, app_id: str) -> bool:
        """通过app_id删除机器人

        Args:
            app_id: 机器人唯一ID

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                await session.execute(delete(Robot).where(Robot.app_id == app_id))
                await session.commit()
                logger.info(f"机器人 {app_id} 已删除")
                return True
            except Exception as e:
                logger.error(f"删除机器人失败: {e}")
                await session.rollback()
                return False
