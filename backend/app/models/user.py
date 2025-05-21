"""用户数据模型模块

定义用户的数据结构和操作方法。
"""

import secrets
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict, Any

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    select,
    update,
    delete,
    Integer,
)
from sqlalchemy.exc import SQLAlchemyError, TimeoutError as SQLATimeoutError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from opengewe.logger import get_logger
from backend.app.db.base import Base
from backend.app.db.session import (
    DatabaseManager,
    DB_OPERATION_TIMEOUT,
    DB_SEMAPHORE,
    async_db_session,
)

# 获取日志记录器
logger = get_logger("User")

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """用户模型

    存储系统用户信息，主要用于管理员账户。
    """

    __tablename__ = "users"  # 显式指定表名
    __table_args__ = {
        "extend_existing": True,  # 允许表已存在
    }  # 确保表定义正确

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(
        String(50), unique=True, index=True, nullable=False, comment="用户名"
    )
    email = Column(String(120), unique=True, index=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(128), nullable=False, comment="密码哈希")
    full_name = Column(String(100), nullable=True, comment="全名")
    is_active = Column(Boolean(), default=True, comment="是否激活")
    is_admin = Column(Boolean(), default=False, comment="是否管理员")
    is_superuser = Column(Boolean(), default=False, comment="是否超级用户")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间",
    )
    api_key = Column(String(128), nullable=True, comment="API密钥")
    api_key_expires = Column(DateTime, nullable=True, comment="API密钥过期时间")
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")

    def verify_password(self, plain_password: str) -> bool:
        """验证密码

        Args:
            plain_password: 明文密码

        Returns:
            bool: 密码是否匹配
        """
        # 输出调试信息
        try:
            result = pwd_context.verify(plain_password, self.hashed_password)
            print(
                f"密码验证: 输入={plain_password}, 哈希={self.hashed_password}, 结果={result}"
            )
            return result
        except Exception as e:
            print(f"密码验证失败: {e}")
            return False

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
    async def get_all(cls) -> Tuple[List["User"], Optional[str]]:
        """获取所有用户

        Returns:
            Tuple[List[User], Optional[str]]: (用户列表, 错误信息)
        """
        db_manager = DatabaseManager()
        try:
            logger.info("开始获取所有用户")
            async with DB_SEMAPHORE:
                logger.debug("获取到数据库信号量")
                async with asyncio.timeout(DB_OPERATION_TIMEOUT):
                    logger.debug("设置超时保护")
                    async with db_manager.get_session(is_admin=True) as session:
                        logger.debug("获取到管理员数据库会话")
                        try:
                            # 使用简单查询，不加锁 - 移除可能导致超时的FOR UPDATE
                            stmt = select(cls)
                            logger.debug(f"执行查询: {stmt}")
                            result = await session.execute(stmt)
                            users = result.scalars().all()
                            logger.info(f"成功获取到 {len(users)} 个用户")
                            return users, None
                        except SQLATimeoutError as e:
                            error_msg = "数据库查询超时"
                            logger.error(f"{error_msg}: {str(e)}")
                            return [], error_msg
                        except SQLAlchemyError as e:
                            error_msg = f"数据库查询错误: {str(e)}"
                            logger.error(error_msg)
                            return [], error_msg
        except asyncio.TimeoutError as e:
            error_msg = "获取用户列表超时"
            logger.error(f"{error_msg}: {str(e)}")
            return [], error_msg
        except Exception as e:
            error_msg = f"未知错误: {str(e)}"
            logger.error(error_msg)
            return [], error_msg

    @classmethod
    async def get_by_username(cls, username: str) -> Optional["User"]:
        """通过用户名获取用户

        Args:
            username: 用户名

        Returns:
            Optional[User]: 用户对象，如果不存在则为None
        """
        try:
            async with DB_SEMAPHORE:
                async with asyncio.timeout(DB_OPERATION_TIMEOUT):
                    async with async_db_session(is_admin=True) as session:
                        try:
                            # 使用简单查询，不加锁
                            result = await session.execute(
                                select(User).where(User.username == username)
                            )
                            return result.scalars().first()
                        except Exception as e:
                            logger.error(f"通过用户名获取用户失败: {e}")
                            return None
        except asyncio.TimeoutError:
            logger.error(f"通过用户名获取用户超时: {username}")
            return None
        except Exception as e:
            logger.error(f"通过用户名获取用户时发生未知错误: {e}")
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
        async with db_manager.get_session(is_admin=True) as session:
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
        async with db_manager.get_session(is_admin=True) as session:
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
        try:
            logger.info(f"开始创建用户: {username}")
            async with DB_SEMAPHORE:
                logger.debug("获取到数据库信号量")
                async with asyncio.timeout(DB_OPERATION_TIMEOUT):
                    logger.debug("设置超时保护")
                    async with db_manager.get_session(is_admin=True) as session:
                        logger.debug("获取到管理员数据库会话")
                        async with session.begin():
                            try:
                                # 检查用户名是否已存在
                                stmt = select(cls).where(cls.username == username)
                                result = await session.execute(stmt)
                                if result.scalar_one_or_none():
                                    logger.warning(f"用户名 {username} 已存在")
                                    return None

                                # 检查邮箱是否已存在
                                stmt = select(cls).where(cls.email == email)
                                result = await session.execute(stmt)
                                if result.scalar_one_or_none():
                                    logger.warning(f"邮箱 {email} 已被使用")
                                    return None

                                # 创建新用户
                                user = cls(
                                    username=username,
                                    email=email,
                                    full_name=full_name,
                                    is_active=True,
                                    is_superuser=is_superuser,
                                    is_admin=is_admin,
                                    created_at=datetime.utcnow(),
                                    updated_at=datetime.utcnow(),
                                )

                                # 设置密码
                                user.set_password(password)

                                session.add(user)
                                await session.flush()  # 立即获取自增ID
                                logger.info(f"用户 {username} 创建成功")
                                return user

                            except SQLATimeoutError as e:
                                logger.error(f"创建用户时数据库超时: {e}")
                                return None
                            except SQLAlchemyError as e:
                                logger.error(f"创建用户时数据库错误: {e}")
                                return None

        except asyncio.TimeoutError as e:
            logger.error(f"创建用户超时: {e}")
            return None
        except Exception as e:
            logger.error(f"创建用户时发生未知错误: {e}")
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
        async with db_manager.get_session(is_admin=True) as session:
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
        async with db_manager.get_session(is_admin=True) as session:
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
        async with db_manager.get_session(is_admin=True) as session:
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
        async with db_manager.get_session(is_admin=True) as session:
            try:
                await session.execute(delete(User).where(User.username == username))
                await session.commit()
                logger.info(f"用户 {username} 已删除")
                return True
            except Exception as e:
                logger.error(f"删除用户失败: {e}")
                await session.rollback()
                return False

    def to_dict(self) -> Dict[str, Any]:
        """将用户对象转换为字典

        Returns:
            Dict[str, Any]: 用户数据字典
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "is_superuser": self.is_superuser,
            "last_login": self.last_login,
            "api_key": self.api_key,
            "api_key_expires": self.api_key_expires,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    async def get_by_id(cls, db: AsyncSession, user_id: int) -> Optional["User"]:
        """通过ID获取用户

        Args:
            db: 数据库会话
            user_id: 用户ID

        Returns:
            Optional[User]: 用户对象，如果不存在则为None
        """
        try:
            # 使用最基本的字段查询，避免依赖可能不存在的字段
            query = select(
                User.id,
                User.username,
                User.email,
                User.hashed_password,
                User.is_active,
                User.is_admin,
                User.created_at,
                User.updated_at,
            ).where(User.id == user_id)

            result = await db.execute(query)
            row = result.first()

            if not row:
                return None

            # 手动构建用户对象，设置默认值
            user = User()
            user.id = row[0]
            user.username = row[1]
            user.email = row[2]
            user.hashed_password = row[3]
            user.is_active = row[4]
            user.is_admin = row[5]
            user.created_at = row[6]
            user.updated_at = row[7]

            # 设置默认值
            user.is_superuser = user.is_admin  # 默认超级用户与管理员相同
            user.api_key = None
            user.api_key_expires = None
            user.last_login = None
            user.full_name = "System Administrator"  # 默认管理员名称

            return user
        except Exception as e:
            logger.error(f"通过ID获取用户失败: {e}")
            return None
