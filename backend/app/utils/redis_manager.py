"""Redis管理器模块

提供Redis连接和操作的管理，支持设备级别的键空间隔离。
"""

import asyncio
from typing import Any, Dict, List, Optional, Set, Union, TypeVar

from redis import asyncio as aioredis

from opengewe.logger import get_logger
from backend.app.core.config import get_settings
from backend.app.core.device import get_current_device_id

# 获取日志记录器
logger = get_logger("RedisManager")

# 定义通用返回类型
T = TypeVar("T")


class RedisManager:
    """Redis连接和操作管理器

    提供Redis连接池和常用操作接口，支持设备级别的键空间隔离。
    使用单例模式确保每个进程只有一个连接池实例。
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """创建单例实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化Redis管理器"""
        if not self._initialized:
            self._redis: Optional[aioredis.Redis] = None
            self._lock = asyncio.Lock()
            self._initialized = True

    async def _ensure_connection(self) -> aioredis.Redis:
        """确保Redis连接可用

        Returns:
            Redis: Redis客户端
        """
        if self._redis is None or not await self._ping():
            async with self._lock:
                if self._redis is None or not await self._ping():
                    await self._connect()
        return self._redis

    async def _connect(self) -> None:
        """创建Redis连接"""
        settings = get_settings()
        redis_config = settings.redis

        try:
            # 创建连接
            self._redis = await aioredis.from_url(
                f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}",
                password=redis_config.password if redis_config.password else None,
                decode_responses=True,
            )
            logger.info(
                f"Redis连接已建立: {redis_config.host}:{redis_config.port}/{redis_config.db}"
            )
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            self._redis = None
            raise

    async def _ping(self) -> bool:
        """检查Redis连接是否正常

        Returns:
            bool: 连接是否正常
        """
        if self._redis is None:
            return False

        try:
            result = await self._redis.ping()
            return result
        except Exception as e:
            logger.warning(f"Redis ping失败: {e}")
            return False

    async def close(self) -> None:
        """关闭Redis连接"""
        if self._redis is not None:
            await self._redis.close()
            self._redis = None
            logger.debug("Redis连接已关闭")

    def _get_key(self, key: str, device_specific: bool = True) -> str:
        """获取带前缀的Redis键

        Args:
            key: 原始键名
            device_specific: 是否添加设备ID前缀

        Returns:
            str: 带前缀的键名
        """
        settings = get_settings()
        prefix = settings.redis.prefix

        # 添加设备特定前缀
        if device_specific:
            device_id = (
                get_current_device_id() or settings.devices.get_default_device_id()
            )
            return f"{prefix}{device_id}:{key}"

        return f"{prefix}{key}"

    async def get(self, key: str, device_specific: bool = True) -> Optional[str]:
        """获取字符串值

        Args:
            key: 键名
            device_specific: 是否使用设备特定前缀

        Returns:
            Optional[str]: 值，不存在时返回None
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return await redis.get(full_key)
        except Exception as e:
            logger.error(f"Redis GET失败 ({full_key}): {e}")
            return None

    async def set(
        self,
        key: str,
        value: str,
        expire: Optional[int] = None,
        device_specific: bool = True,
    ) -> bool:
        """设置字符串值

        Args:
            key: 键名
            value: 值
            expire: 过期时间(秒)
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            await redis.set(full_key, value, ex=expire)
            return True
        except Exception as e:
            logger.error(f"Redis SET失败 ({full_key}): {e}")
            return False

    async def delete(self, key: str, device_specific: bool = True) -> bool:
        """删除键

        Args:
            key: 键名
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            await redis.delete(full_key)
            return True
        except Exception as e:
            logger.error(f"Redis DEL失败 ({full_key}): {e}")
            return False

    async def exists(self, key: str, device_specific: bool = True) -> bool:
        """检查键是否存在

        Args:
            key: 键名
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 键是否存在
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return bool(await redis.exists(full_key))
        except Exception as e:
            logger.error(f"Redis EXISTS失败 ({full_key}): {e}")
            return False

    async def expire(
        self, key: str, seconds: int, device_specific: bool = True
    ) -> bool:
        """设置键的过期时间

        Args:
            key: 键名
            seconds: 过期时间(秒)
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return bool(await redis.expire(full_key, seconds))
        except Exception as e:
            logger.error(f"Redis EXPIRE失败 ({full_key}): {e}")
            return False

    async def ttl(self, key: str, device_specific: bool = True) -> int:
        """获取键的剩余生存时间

        Args:
            key: 键名
            device_specific: 是否使用设备特定前缀

        Returns:
            int: 剩余秒数，-1表示永久，-2表示不存在
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return await redis.ttl(full_key)
        except Exception as e:
            logger.error(f"Redis TTL失败 ({full_key}): {e}")
            return -2

    # 哈希表操作

    async def hget(
        self, key: str, field: str, device_specific: bool = True
    ) -> Optional[str]:
        """获取哈希表字段值

        Args:
            key: 键名
            field: 字段名
            device_specific: 是否使用设备特定前缀

        Returns:
            Optional[str]: 值，不存在时返回None
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return await redis.hget(full_key, field)
        except Exception as e:
            logger.error(f"Redis HGET失败 ({full_key}): {e}")
            return None

    async def hset(
        self, key: str, field: str, value: str, device_specific: bool = True
    ) -> bool:
        """设置哈希表字段值

        Args:
            key: 键名
            field: 字段名
            value: 值
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            await redis.hset(full_key, field, value)
            return True
        except Exception as e:
            logger.error(f"Redis HSET失败 ({full_key}): {e}")
            return False

    async def hdel(self, key: str, field: str, device_specific: bool = True) -> bool:
        """删除哈希表字段

        Args:
            key: 键名
            field: 字段名
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            await redis.hdel(full_key, field)
            return True
        except Exception as e:
            logger.error(f"Redis HDEL失败 ({full_key}): {e}")
            return False

    async def hgetall(self, key: str, device_specific: bool = True) -> Dict[str, str]:
        """获取哈希表所有字段和值

        Args:
            key: 键名
            device_specific: 是否使用设备特定前缀

        Returns:
            Dict[str, str]: 字段和值的字典
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return await redis.hgetall(full_key)
        except Exception as e:
            logger.error(f"Redis HGETALL失败 ({full_key}): {e}")
            return {}

    # 列表操作

    async def lpush(self, key: str, *values: str, device_specific: bool = True) -> bool:
        """向列表左侧添加元素

        Args:
            key: 键名
            values: 要添加的值
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            await redis.lpush(full_key, *values)
            return True
        except Exception as e:
            logger.error(f"Redis LPUSH失败 ({full_key}): {e}")
            return False

    async def rpush(self, key: str, *values: str, device_specific: bool = True) -> bool:
        """向列表右侧添加元素

        Args:
            key: 键名
            values: 要添加的值
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            await redis.rpush(full_key, *values)
            return True
        except Exception as e:
            logger.error(f"Redis RPUSH失败 ({full_key}): {e}")
            return False

    async def lpop(self, key: str, device_specific: bool = True) -> Optional[str]:
        """从列表左侧弹出元素

        Args:
            key: 键名
            device_specific: 是否使用设备特定前缀

        Returns:
            Optional[str]: 弹出的值，不存在时返回None
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return await redis.lpop(full_key)
        except Exception as e:
            logger.error(f"Redis LPOP失败 ({full_key}): {e}")
            return None

    async def rpop(self, key: str, device_specific: bool = True) -> Optional[str]:
        """从列表右侧弹出元素

        Args:
            key: 键名
            device_specific: 是否使用设备特定前缀

        Returns:
            Optional[str]: 弹出的值，不存在时返回None
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return await redis.rpop(full_key)
        except Exception as e:
            logger.error(f"Redis RPOP失败 ({full_key}): {e}")
            return None

    async def lrange(
        self, key: str, start: int, end: int, device_specific: bool = True
    ) -> List[str]:
        """获取列表指定范围的元素

        Args:
            key: 键名
            start: 起始索引
            end: 结束索引
            device_specific: 是否使用设备特定前缀

        Returns:
            List[str]: 元素列表
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return await redis.lrange(full_key, start, end)
        except Exception as e:
            logger.error(f"Redis LRANGE失败 ({full_key}): {e}")
            return []

    # 集合操作

    async def sadd(self, key: str, *members: str, device_specific: bool = True) -> bool:
        """向集合添加成员

        Args:
            key: 键名
            members: 要添加的成员
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            await redis.sadd(full_key, *members)
            return True
        except Exception as e:
            logger.error(f"Redis SADD失败 ({full_key}): {e}")
            return False

    async def srem(self, key: str, *members: str, device_specific: bool = True) -> bool:
        """从集合移除成员

        Args:
            key: 键名
            members: 要移除的成员
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            await redis.srem(full_key, *members)
            return True
        except Exception as e:
            logger.error(f"Redis SREM失败 ({full_key}): {e}")
            return False

    async def smembers(self, key: str, device_specific: bool = True) -> Set[str]:
        """获取集合所有成员

        Args:
            key: 键名
            device_specific: 是否使用设备特定前缀

        Returns:
            Set[str]: 成员集合
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return await redis.smembers(full_key)
        except Exception as e:
            logger.error(f"Redis SMEMBERS失败 ({full_key}): {e}")
            return set()

    # 有序集合操作

    async def zadd(
        self,
        key: str,
        mapping: Dict[str, Union[int, float]],
        device_specific: bool = True,
    ) -> bool:
        """向有序集合添加成员

        Args:
            key: 键名
            mapping: 成员和分数的映射
            device_specific: 是否使用设备特定前缀

        Returns:
            bool: 操作是否成功
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            await redis.zadd(full_key, mapping)
            return True
        except Exception as e:
            logger.error(f"Redis ZADD失败 ({full_key}): {e}")
            return False

    async def zrange(
        self,
        key: str,
        start: int,
        end: int,
        withscores: bool = False,
        device_specific: bool = True,
    ) -> Union[List[str], List[Dict[str, Union[str, float]]]]:
        """获取有序集合指定范围的成员

        Args:
            key: 键名
            start: 起始索引
            end: 结束索引
            withscores: 是否包含分数
            device_specific: 是否使用设备特定前缀

        Returns:
            Union[List[str], List[Dict[str, Union[str, float]]]]: 成员列表
        """
        redis = await self._ensure_connection()
        full_key = self._get_key(key, device_specific)

        try:
            return await redis.zrange(full_key, start, end, withscores=withscores)
        except Exception as e:
            logger.error(f"Redis ZRANGE失败 ({full_key}): {e}")
            return []
