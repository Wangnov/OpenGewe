"""GeweClient管理器模块

提供GeweClient实例的管理功能，包括创建、获取、缓存和关闭客户端实例。
"""

import asyncio
from typing import Dict, Optional, Set, List
import time

from opengewe.client import GeweClient
from opengewe.logger import get_logger

from backend.app.core.config import get_settings
from backend.app.core.device import get_current_device_id
from backend.app.gewe.client_factory import create_client

# 获取日志记录器
logger = get_logger("GeweClientManager")


class GeweClientManager:
    """GeweClient管理器

    管理多个设备的GeweClient实例，提供按设备ID获取和缓存客户端的功能。
    使用单例模式确保每个进程只有一个管理器实例。
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """创建单例实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化客户端管理器"""
        if not self._initialized:
            # 客户端缓存，按设备ID索引
            self._clients: Dict[str, GeweClient] = {}
            # 客户端最后使用时间记录
            self._last_used: Dict[str, float] = {}
            # 最大空闲时间（秒），超过此时间未使用的客户端将被关闭
            self._max_idle_time = 3600  # 1小时
            # 客户端创建锁，按设备ID索引
            self._locks: Dict[str, asyncio.Lock] = {}
            # 创建后台清理任务
            self._cleanup_task = None
            # 管理器锁
            self._manager_lock = asyncio.Lock()
            # 已加载插件的设备ID集合
            self._plugins_loaded: Set[str] = set()
            # 管理器是否已启动
            self._started = False

            self._initialized = True
            logger.debug("GeweClient管理器已初始化")

    async def start(self):
        """启动管理器，创建后台清理任务"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_idle_clients())
            self._started = True
            logger.info("GeweClient管理器后台清理任务已启动")

    async def stop(self):
        """停止管理器，关闭所有客户端和后台任务"""
        async with self._manager_lock:
            # 取消后台清理任务
            if self._cleanup_task is not None:
                self._cleanup_task.cancel()
                try:
                    await self._cleanup_task
                except asyncio.CancelledError:
                    pass
                self._cleanup_task = None
                logger.debug("后台清理任务已取消")

            # 关闭所有客户端
            for device_id, client in list(self._clients.items()):
                try:
                    await client.close()
                    logger.info(f"关闭设备 {device_id} 的客户端")
                except Exception as e:
                    logger.error(f"关闭设备 {device_id} 的客户端时出错: {e}")

            self._clients.clear()
            self._last_used.clear()
            self._started = False
            logger.info("所有GeweClient实例已关闭")

    def is_ready(self) -> bool:
        """检查GeweClient管理器是否已准备好服务请求

        返回管理器的启动状态，表示是否可以提供GeweClient服务

        Returns:
            bool: 如果管理器已启动则返回True，否则返回False
        """
        return self._initialized and self._started

    async def _cleanup_idle_clients(self):
        """后台任务：清理空闲客户端"""
        try:
            while True:
                await asyncio.sleep(300)  # 每5分钟检查一次
                await self._do_cleanup()
        except asyncio.CancelledError:
            logger.debug("清理空闲客户端的后台任务已取消")
        except Exception as e:
            logger.error(f"清理空闲客户端时出错: {e}")

    async def _do_cleanup(self):
        """执行一次空闲客户端清理"""
        now = time.time()
        to_close = []

        async with self._manager_lock:
            # 收集超过空闲时间的客户端
            for device_id, last_used in self._last_used.items():
                if now - last_used > self._max_idle_time:
                    to_close.append(device_id)

            # 关闭空闲客户端
            for device_id in to_close:
                if device_id in self._clients:
                    client = self._clients.pop(device_id)
                    self._last_used.pop(device_id)
                    if device_id in self._plugins_loaded:
                        self._plugins_loaded.remove(device_id)

                    try:
                        await client.close()
                        logger.info(
                            f"关闭空闲客户端: {device_id} (空闲时间: {now - last_used:.1f}秒)"
                        )
                    except Exception as e:
                        logger.error(f"关闭空闲客户端 {device_id} 时出错: {e}")

    async def get_client(
        self, device_id: Optional[str] = None, load_plugins: bool = True
    ) -> GeweClient:
        """获取设备的GeweClient实例

        如果实例已存在于缓存中，则返回缓存的实例，否则创建新实例。
        可以通过load_plugins参数控制是否加载插件。

        Args:
            device_id: 设备ID，如果为None则使用当前上下文的设备ID
            load_plugins: 是否加载插件

        Returns:
            GeweClient: 客户端实例

        Raises:
            ValueError: 如果未提供设备ID且无法获取当前上下文的设备ID
        """
        # 如果未提供设备ID，使用当前上下文的设备ID
        if device_id is None:
            device_id = get_current_device_id()
            if device_id is None:
                settings = get_settings()
                try:
                    device_id = settings.devices.get_default_device_id()
                    logger.debug(f"使用默认设备ID: {device_id}")
                except ValueError:
                    raise ValueError("未提供设备ID，且无法获取当前上下文或默认的设备ID")

        # 更新最后使用时间
        self._last_used[device_id] = time.time()

        # 如果客户端已存在，直接返回
        if device_id in self._clients:
            logger.debug(f"使用缓存的客户端: {device_id}")
            return self._clients[device_id]

        # 创建锁（如果不存在）
        if device_id not in self._locks:
            async with self._manager_lock:  # 使用管理器锁保护锁字典的修改
                if device_id not in self._locks:  # 再次检查，避免竞态条件
                    self._locks[device_id] = asyncio.Lock()

        # 获取锁以确保一次只有一个协程创建客户端
        async with self._locks[device_id]:
            # 再次检查，以防在等待锁的过程中已经创建了客户端
            if device_id in self._clients:
                return self._clients[device_id]

            # 创建新客户端
            client = await create_client(device_id=device_id)

            # 使用管理器锁保护客户端字典的修改
            async with self._manager_lock:
                self._clients[device_id] = client
                logger.info(f"创建新客户端: {device_id}")

            # 如果需要，加载插件
            if load_plugins and device_id not in self._plugins_loaded:
                try:
                    settings = get_settings()
                    plugins_dir = settings.plugins.plugins_dir
                    loaded_plugins = await client.start_plugins(plugins_dir)
                    if loaded_plugins:
                        logger.info(
                            f"设备 {device_id} 加载了 {len(loaded_plugins)} 个插件: {', '.join(loaded_plugins)}"
                        )
                        # 使用管理器锁保护插件加载状态的修改
                        async with self._manager_lock:
                            self._plugins_loaded.add(device_id)
                    else:
                        logger.warning(f"设备 {device_id} 未加载任何插件")
                except Exception as e:
                    logger.error(f"设备 {device_id} 加载插件时出错: {e}")

            return client

    async def close_client(self, device_id: str) -> bool:
        """关闭指定设备的客户端

        Args:
            device_id: 设备ID

        Returns:
            bool: 是否成功关闭
        """
        async with self._manager_lock:
            if device_id in self._clients:
                client = self._clients.pop(device_id)
                if device_id in self._last_used:
                    self._last_used.pop(device_id)
                if device_id in self._plugins_loaded:
                    self._plugins_loaded.remove(device_id)

                try:
                    await client.close()
                    logger.info(f"关闭设备 {device_id} 的客户端")
                    return True
                except Exception as e:
                    logger.error(f"关闭设备 {device_id} 的客户端时出错: {e}")
                    return False
            return False

    async def refresh_client(
        self, device_id: str, load_plugins: bool = True
    ) -> GeweClient:
        """刷新设备的客户端

        关闭现有客户端（如果存在），并创建新客户端。

        Args:
            device_id: 设备ID
            load_plugins: 是否加载插件

        Returns:
            GeweClient: 新的客户端实例
        """
        # 先关闭现有客户端
        await self.close_client(device_id)
        # 创建新客户端
        return await self.get_client(device_id, load_plugins)

    def get_active_clients(self) -> List[str]:
        """获取所有活动的客户端设备ID列表

        Returns:
            List[str]: 设备ID列表
        """
        return list(self._clients.keys())

    def get_plugins_loaded_clients(self) -> List[str]:
        """获取已加载插件的客户端设备ID列表

        Returns:
            List[str]: 设备ID列表
        """
        return list(self._plugins_loaded)


# 创建全局单例实例
client_manager = GeweClientManager()
