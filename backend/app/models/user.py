"""用户数据模型模块

定义用户的数据结构和操作方法。
"""

import secrets
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import Column, String, Boolean, DateTime, select, update, delete
from passlib.context import CryptContext

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import DatabaseManager

# 获取日志记录器
logger = get_logger("User")

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """用户模型

    存储系统用户信息，主要用于管理员账户。
    """

    username = Column(
        String(50), unique=True, index=True, nullable=False, comment="用户名"
    )
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(100), nullable=False, comment="密码哈希")
    full_name = Column(String(100), nullable=True, comment="全名")
    is_active = Column(Boolean, default=True, comment="是否活跃")
    is_superuser = Column(Boolean, default=False, comment="是否超级用户")
    is_admin = Column(Boolean, default=False, comment="是否管理员")
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")
    api_key = Column(String(64), unique=True, nullable=True, comment="API密钥")
    api_key_expires = Column(DateTime, nullable=True, comment="API密钥过期时间")

    def verify_password(self, plain_password: str) -> bool:
        """验证密码

        Args:
            plain_password: 明文密码

        Returns:
            bool: 密码是否匹配
        """
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, password: str) -> None:
        """设置密码

        Args:
            password: 明文密码
        """
        self.hashed_password = pwd_context.hash(password)

    def generate_api_key(self, expires_days: int = 30) -> str:
        """生成API密钥

        Args:
            expires_days: 过期天数

        Returns:
            str: 生成的API密钥
        """
        self.api_key = secrets.token_hex(32)
        self.api_key_expires = datetime.now() + timedelta(days=expires_days)
        return self.api_key

    def is_api_key_valid(self) -> bool:
        """检查API密钥是否有效

        Returns:
            bool: 密钥是否有效
        """
        if not self.api_key or not self.api_key_expires:
            return False
        return datetime.now() < self.api_key_expires

    @classmethod
    async def get_all(cls) -> List["User"]:
        """获取所有用户

        Returns:
            List[User]: 用户列表
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(select(User))
                return result.scalars().all()
            except Exception as e:
                logger.error(f"获取所有用户失败: {e}")
                return []

    @classmethod
    async def get_by_username(cls, username: str) -> Optional["User"]:
        """通过用户名获取用户

        Args:
            username: 用户名

        Returns:
            Optional[User]: 用户对象，如果不存在则为None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(
                    select(User).where(User.username == username)
                )
                return result.scalars().first()
            except Exception as e:
                logger.error(f"通过用户名获取用户失败: {e}")
                return None

    @classmethod
    async def get_by_email(cls, email: str) -> Optional["User"]:
        """通过邮箱获取用户

        Args:
            email: 邮箱

        Returns:
            Optional[User]: 用户对象，如果不存在则为None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(select(User).where(User.email == email))
                return result.scalars().first()
            except Exception as e:
                logger.error(f"通过邮箱获取用户失败: {e}")
                return None

    @classmethod
    async def get_by_api_key(cls, api_key: str) -> Optional["User"]:
        """通过API密钥获取用户

        Args:
            api_key: API密钥

        Returns:
            Optional[User]: 用户对象，如果不存在或密钥无效则为None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                result = await session.execute(
                    select(User).where(User.api_key == api_key)
                )
                user = result.scalars().first()

                if not user or not user.is_api_key_valid():
                    return None

                return user
            except Exception as e:
                logger.error(f"通过API密钥获取用户失败: {e}")
                return None

    @classmethod
    async def create(
        cls,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        is_superuser: bool = False,
        is_admin: bool = False,
    ) -> Optional["User"]:
        """创建新用户

        Args:
            username: 用户名
            email: 邮箱
            password: 明文密码
            full_name: 全名
            is_superuser: 是否超级用户
            is_admin: 是否管理员

        Returns:
            Optional[User]: 创建的用户对象，失败则为None
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 检查用户名是否已存在
                existing_user = await cls.get_by_username(username)
                if existing_user:
                    logger.warning(f"用户名 {username} 已存在")
                    return None

                # 检查邮箱是否已存在
                existing_email = await cls.get_by_email(email)
                if existing_email:
                    logger.warning(f"邮箱 {email} 已被使用")
                    return None

                # 创建新用户
                user = User(
                    username=username,
                    email=email,
                    full_name=full_name,
                    is_active=True,
                    is_superuser=is_superuser,
                    is_admin=is_admin,
                )

                # 设置密码
                user.set_password(password)

                session.add(user)
                await session.commit()
                await session.refresh(user)
                logger.info(f"用户 {username} 创建成功")
                return user
            except Exception as e:
                logger.error(f"创建用户失败: {e}")
                await session.rollback()
                return None

    @classmethod
    async def update_last_login(cls, username: str) -> bool:
        """更新用户最后登录时间

        Args:
            username: 用户名

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                await session.execute(
                    update(User)
                    .where(User.username == username)
                    .values(last_login=datetime.now())
                )
                await session.commit()
                logger.debug(f"用户 {username} 最后登录时间已更新")
                return True
            except Exception as e:
                logger.error(f"更新用户最后登录时间失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def update_password(cls, username: str, new_password: str) -> bool:
        """更新用户密码

        Args:
            username: 用户名
            new_password: 新密码

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                # 哈希密码
                hashed_password = pwd_context.hash(new_password)

                await session.execute(
                    update(User)
                    .where(User.username == username)
                    .values(hashed_password=hashed_password)
                )
                await session.commit()
                logger.info(f"用户 {username} 密码已更新")
                return True
            except Exception as e:
                logger.error(f"更新用户密码失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def toggle_active(cls, username: str, is_active: bool) -> bool:
        """切换用户活跃状态

        Args:
            username: 用户名
            is_active: 是否活跃

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                await session.execute(
                    update(User)
                    .where(User.username == username)
                    .values(is_active=is_active)
                )
                await session.commit()

                status = "活跃" if is_active else "禁用"
                logger.info(f"用户 {username} 已设置为{status}")
                return True
            except Exception as e:
                logger.error(f"切换用户活跃状态失败: {e}")
                await session.rollback()
                return False

    @classmethod
    async def delete_by_username(cls, username: str) -> bool:
        """通过用户名删除用户

        Args:
            username: 用户名

        Returns:
            bool: 操作是否成功
        """
        db_manager = DatabaseManager()
        async with db_manager.get_session() as session:
            try:
                await session.execute(delete(User).where(User.username == username))
                await session.commit()
                logger.info(f"用户 {username} 已删除")
                return True
            except Exception as e:
                logger.error(f"删除用户失败: {e}")
                await session.rollback()
                return False
