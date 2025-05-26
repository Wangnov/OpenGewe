"""
机器人客户端管理器

管理GeweClient实例，处理插件加载和消息分发
"""

import sys
import importlib.util
from typing import Dict, Optional, List, Any
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from loguru import logger

from opengewe.client import GeweClient
from opengewe.utils.plugin_base import PluginBase
from ..models.admin import GlobalPlugin
from ..models.bot import BotInfo, BotPlugin
from ..core.session_manager import admin_session
from ..core.bot_profile_manager import BotProfileManager
from ..core.session_manager import session_manager


class BotClientManager:
    """机器人客户端管理器单例"""

    _instance: Optional["BotClientManager"] = None
    _initialized: bool = False

    def __new__(cls) -> "BotClientManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._clients: Dict[str, GeweClient] = {}
            self._available_plugins: Dict[str, type] = {}
            self._plugins_loaded = False
            BotClientManager._initialized = True
            logger.info("机器人客户端管理器初始化完成")

    async def get_client(
        self, gewe_app_id: str, session: Optional[AsyncSession] = None
    ) -> Optional[GeweClient]:
        """获取或创建指定机器人的客户端实例"""
        if gewe_app_id in self._clients:
            return self._clients[gewe_app_id]

        # 从数据库获取机器人信息
        if session is not None:
            # 使用提供的session
            return await self._create_client_with_session(gewe_app_id, session)
        else:
            # 创建新的session
            async with admin_session() as new_session:
                return await self._create_client_with_session(gewe_app_id, new_session)

    async def _create_client_with_session(
        self, gewe_app_id: str, session: AsyncSession
    ) -> Optional[GeweClient]:
        """使用指定session创建客户端实例"""
        stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
        result = await session.execute(stmt)
        bot = result.scalar_one_or_none()

        if not bot:
            logger.warning(f"未找到机器人信息: gewe_app_id={gewe_app_id}")
            return None

        # 创建GeweClient实例
        client = GeweClient(
            base_url=bot.base_url,
            app_id=gewe_app_id,
            token=bot.gewe_token,
            debug=False,
        )

        # 加载插件
        await self._load_plugins_for_bot(client, bot, session)

        self._clients[gewe_app_id] = client
        logger.info(f"已创建机器人客户端: {gewe_app_id}")

        # 检查并更新机器人个人资料
        try:
            should_update = await BotProfileManager.should_update_profile(
                gewe_app_id, session=session
            )
            if should_update:
                logger.info(f"开始获取机器人个人资料: {gewe_app_id}")
                await BotProfileManager.fetch_and_update_profile(
                    client, gewe_app_id, session=session
                )
            else:
                logger.debug(f"机器人个人资料无需更新: {gewe_app_id}")
        except Exception as e:
            logger.error(
                f"更新机器人个人资料失败: gewe_app_id={gewe_app_id}, 错误: {e}",
                exc_info=True,
            )
            # 个人资料更新失败不影响客户端创建

        return client

    async def _load_available_plugins(self):
        """加载plugins目录中的所有可用插件"""
        if self._plugins_loaded:
            return

        # 获取项目根目录的plugins文件夹
        project_root = Path(__file__).parent.parent.parent.parent
        plugins_dir = project_root / "plugins"

        if not plugins_dir.exists():
            logger.warning(f"插件目录不存在: {plugins_dir}")
            return

        logger.info(f"开始加载插件目录: {plugins_dir}")

        # 遍历插件目录
        for plugin_folder in plugins_dir.iterdir():
            if not plugin_folder.is_dir() or plugin_folder.name.startswith("."):
                continue

            # 检查是否有main.py文件
            main_file = plugin_folder / "main.py"
            if not main_file.exists():
                logger.debug(f"插件目录缺少main.py: {plugin_folder.name}")
                continue

            try:
                # 动态导入插件模块
                spec = importlib.util.spec_from_file_location(
                    f"plugins.{plugin_folder.name}.main", main_file
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)

                    # 添加plugins目录到sys.path，确保插件能正确导入utils
                    if str(plugins_dir) not in sys.path:
                        sys.path.insert(0, str(plugins_dir))

                    spec.loader.exec_module(module)

                    # 查找PluginBase的子类
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, PluginBase)
                            and attr != PluginBase
                        ):
                            self._available_plugins[plugin_folder.name] = attr
                            logger.info(
                                f"加载插件: {plugin_folder.name} ({attr.__name__})"
                            )
                            break
                    else:
                        logger.warning(
                            f"插件目录中未找到PluginBase子类: {plugin_folder.name}"
                        )

            except Exception as e:
                logger.error(
                    f"加载插件失败: {plugin_folder.name}, 错误: {e}", exc_info=True
                )

        self._plugins_loaded = True
        logger.info(f"插件加载完成，可用插件数量: {len(self._available_plugins)}")

    async def _load_plugins_for_bot(
        self, client: GeweClient, bot: BotInfo, session: AsyncSession
    ):
        """为指定机器人加载插件"""
        # 确保插件已加载
        await self._load_available_plugins()

        # 查询全局启用的插件
        global_plugins_stmt = select(GlobalPlugin).where(
            GlobalPlugin.is_globally_enabled is True
        )
        global_result = await session.execute(global_plugins_stmt)
        global_plugins = {
            plugin.plugin_name: plugin for plugin in global_result.scalars().all()
        }

        # 查询机器人启用的插件 - 使用机器人专用会话
        async with session_manager.get_bot_session(bot.gewe_app_id) as bot_session:
            bot_plugins_stmt = select(BotPlugin).where(
                and_(
                    BotPlugin.gewe_app_id == bot.gewe_app_id,
                    BotPlugin.is_enabled is True,
                )
            )
            bot_result = await bot_session.execute(bot_plugins_stmt)
            bot_plugins = {
                plugin.plugin_name: plugin for plugin in bot_result.scalars().all()
            }

        loaded_count = 0

        # 为每个启用的插件创建实例
        for plugin_name in bot_plugins.keys():
            if plugin_name in self._available_plugins and plugin_name in global_plugins:
                try:
                    plugin_cls = self._available_plugins[plugin_name]

                    # 注册插件到客户端
                    await client.plugin_manager.register_plugin(plugin_cls)
                    loaded_count += 1

                    logger.info(f"为机器人 {bot.gewe_app_id} 加载插件: {plugin_name}")

                except Exception as e:
                    logger.error(
                        f"为机器人 {bot.gewe_app_id} 加载插件 {plugin_name} 失败: {e}",
                        exc_info=True,
                    )

        logger.info(
            f"机器人 {bot.gewe_app_id} 插件加载完成，已加载 {loaded_count} 个插件"
        )

    async def process_webhook_message(
        self,
        gewe_app_id: str,
        payload_data: Dict[str, Any],
        session: Optional[AsyncSession] = None,
    ) -> bool:
        """处理webhook消息，传递给对应机器人的插件"""
        try:
            client = await self.get_client(gewe_app_id, session)
            if not client:
                logger.error(f"无法获取机器人客户端: {gewe_app_id}")
                return False

            # 使用MessageFactory处理消息
            message = await client.message_factory.process(payload_data)

            if message:
                logger.debug(
                    f"消息处理成功: gewe_app_id={gewe_app_id}, "
                    f"message_type={message.type.name}, "
                    f"from_wxid={getattr(message, 'from_wxid', 'N/A')}"
                )
                return True
            else:
                logger.debug(f"消息未被处理: gewe_app_id={gewe_app_id}")
                return True  # 即使消息未被处理，也不算错误

        except Exception as e:
            logger.error(
                f"处理webhook消息失败: gewe_app_id={gewe_app_id}, 错误: {e}",
                exc_info=True,
            )
            return False

    async def reload_plugins(self, gewe_app_id: Optional[str] = None):
        """重新加载插件"""
        if gewe_app_id:
            # 重新加载指定机器人的插件
            if gewe_app_id in self._clients:
                client = self._clients[gewe_app_id]
                # 停止现有插件
                await client.plugin_manager.stop_all_plugins()

                # 重新加载
                async with admin_session() as session:
                    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
                    result = await session.execute(stmt)
                    bot = result.scalar_one_or_none()
                    if bot:
                        await self._load_plugins_for_bot(client, bot, session)
        else:
            # 重新加载所有插件
            self._plugins_loaded = False
            self._available_plugins.clear()

            # 重新初始化所有客户端的插件
            for gewe_app_id, client in self._clients.items():
                await client.plugin_manager.stop_all_plugins()
                async with admin_session() as session:
                    stmt = select(BotInfo).where(BotInfo.gewe_app_id == gewe_app_id)
                    result = await session.execute(stmt)
                    bot = result.scalar_one_or_none()
                    if bot:
                        await self._load_plugins_for_bot(client, bot, session)

    async def get_bot_plugin_status(self, gewe_app_id: str) -> Dict[str, Any]:
        """获取机器人的插件状态"""
        client = await self.get_client(gewe_app_id)
        if not client:
            return {"error": "机器人客户端不存在"}

        try:
            plugin_status = {
                "loaded_plugins": [],
                "available_plugins": list(self._available_plugins.keys()),
                "plugin_manager_info": {
                    "plugin_count": len(client.plugin_manager.plugins),
                    "enabled_plugins": [
                        name
                        for name, info in client.plugin_manager.plugin_info.items()
                        if info.get("enabled", False)
                    ],
                },
            }

            return plugin_status

        except Exception as e:
            logger.error(f"获取插件状态失败: {e}", exc_info=True)
            return {"error": str(e)}

    def get_available_plugins(self) -> List[str]:
        """获取所有可用插件列表"""
        return list(self._available_plugins.keys())

    async def close_client(self, gewe_app_id: str):
        """关闭指定机器人的客户端"""
        if gewe_app_id in self._clients:
            client = self._clients[gewe_app_id]
            try:
                await client.plugin_manager.stop_all_plugins()
                # 如果client有close方法的话
                if hasattr(client, "close"):
                    await client.close()
            except Exception as e:
                logger.error(f"关闭客户端失败: {e}")
            finally:
                del self._clients[gewe_app_id]
                logger.info(f"已关闭机器人客户端: {gewe_app_id}")


# 创建全局单例实例
bot_manager = BotClientManager()
