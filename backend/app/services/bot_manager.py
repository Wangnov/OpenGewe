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
from opengewe.client import GeweClient
from opengewe.utils.plugin_base import PluginBase
from ..models.admin import GlobalPlugin
from ..models.bot import BotInfo, BotPlugin
from ..core.session_manager import admin_session
from .bot_profile_manager import BotProfileManager
from ..core.session_manager import session_manager
from ..services.config_manager import config_manager
from opengewe.logger import init_default_logger, get_logger

init_default_logger()
logger = get_logger(__name__)


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

        # 从配置中获取队列设置
        queue_config = await config_manager.get_config("queue") or {}
        queue_type = queue_config.get("queue_type", "simple")
        queue_options = {
            "broker": queue_config.get("broker"),
            "backend": queue_config.get("backend"),
            "queue_name": queue_config.get("name"),
            "concurrency": queue_config.get("concurrency"),
        }

        # 从配置中获取插件目录
        plugins_config = await config_manager.get_config("plugins") or {}
        plugins_dir = plugins_config.get("plugins_dir", "plugins")

        # 创建GeweClient实例
        client = GeweClient(
            base_url=bot.base_url,
            app_id=gewe_app_id,
            token=bot.gewe_token,
            debug=False,
            queue_type=queue_type,
            plugins_dir=plugins_dir,
            **queue_options,
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

        # 需要排除的目录名称
        excluded_dirs = {
            "utils",
            "__pycache__",
            ".git",
            ".vscode",
            ".idea",
            "node_modules",
            "venv",
            ".venv",
        }

        # 遍历插件目录
        for plugin_folder in plugins_dir.iterdir():
            if not plugin_folder.is_dir() or plugin_folder.name.startswith("."):
                continue

            # 排除非插件目录
            if plugin_folder.name in excluded_dirs:
                logger.debug(f"跳过非插件目录: {plugin_folder.name}")
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

        logger.info(f"开始为机器人 {bot.gewe_app_id} 加载插件...")
        logger.debug(f"可用插件: {list(self._available_plugins.keys())}")

        # 查询全局启用的插件
        global_plugins_stmt = select(GlobalPlugin).where(
            GlobalPlugin.is_globally_enabled
        )
        global_result = await session.execute(global_plugins_stmt)
        global_plugins = {
            plugin.plugin_name: plugin for plugin in global_result.scalars().all()
        }
        logger.debug(f"全局启用的插件: {list(global_plugins.keys())}")

        # 查询机器人启用的插件 - 使用机器人专用会话
        async with session_manager.get_bot_session(bot.gewe_app_id) as bot_session:
            bot_plugins_stmt = select(BotPlugin).where(
                and_(
                    BotPlugin.gewe_app_id == bot.gewe_app_id,
                    BotPlugin.is_enabled,
                )
            )
            bot_result = await bot_session.execute(bot_plugins_stmt)
            bot_plugins = {
                plugin.plugin_name: plugin for plugin in bot_result.scalars().all()
            }
        logger.debug(
            f"机器人 {bot.gewe_app_id} 启用的插件: {list(bot_plugins.keys())}")

        loaded_count = 0

        # 为每个启用的插件创建实例
        for plugin_name, bot_plugin in bot_plugins.items():
            if (
                plugin_name in self._available_plugins
                and plugin_name in global_plugins
            ):
                try:
                    plugin_cls = self._available_plugins[plugin_name]
                    global_plugin = global_plugins[plugin_name]

                    # 合并配置：机器人配置 > 全局配置
                    override_config = {}
                    if global_plugin.global_config:
                        override_config.update(global_plugin.global_config)
                    if bot_plugin.config_json:
                        override_config.update(bot_plugin.config_json)

                    logger.info(
                        f"正在为机器人 {bot.gewe_app_id} 注册插件: {plugin_name}"
                    )

                    # 注册插件到客户端，并传入覆盖配置
                    await client.plugin_manager.register_plugin(
                        plugin_cls, override_config=override_config
                    )
                    loaded_count += 1

                    logger.info(
                        f"为机器人 {bot.gewe_app_id} 成功加载插件: {plugin_name}"
                    )

                except Exception as e:
                    logger.error(
                        f"为机器人 {bot.gewe_app_id} 加载插件 {plugin_name} 失败: {e}",
                        exc_info=True,
                    )
            else:
                missing_conditions = []
                if plugin_name not in self._available_plugins:
                    missing_conditions.append("插件类不可用")
                if plugin_name not in global_plugins:
                    missing_conditions.append("全局未启用")

                logger.warning(
                    f"跳过插件 {plugin_name} for 机器人 {bot.gewe_app_id}: {', '.join(missing_conditions)}"
                )

        logger.info(
            f"机器人 {bot.gewe_app_id} 插件加载完成，已加载 {loaded_count} 个插件"
        )

        # 启动插件管理器
        try:
            plugin_manager = client.plugin_manager

            # 方式1: 尝试start_all_plugins方法
            if hasattr(plugin_manager, "start_all_plugins"):
                await plugin_manager.start_all_plugins()
                logger.debug(
                    f"机器人 {bot.gewe_app_id} 的插件管理器已启动 (start_all_plugins)"
                )

            # 方式2: 尝试start方法
            elif hasattr(plugin_manager, "start"):
                await plugin_manager.start()
                logger.debug(f"机器人 {bot.gewe_app_id} 的插件管理器已启动 (start)")

            # 检查插件管理器的event_manager是否正确初始化
            if not hasattr(plugin_manager, "event_manager"):
                logger.error("插件管理器缺少event_manager，这不应该发生")

            # 检查事件管理器的handlers属性
            event_manager = plugin_manager.event_manager
            if not hasattr(event_manager.__class__, "_handlers"):
                logger.error("事件管理器缺少_handlers类属性，这不应该发生")

                # 方式6: 尝试重新注册插件的事件处理器
                try:
                    for plugin_name, plugin_instance in plugin_manager.plugins.items():
                        logger.debug(f"尝试为插件 {plugin_name} 重新注册事件处理器")

                        # 检查插件是否有消息处理方法
                        for method_name in dir(plugin_instance):
                            if method_name.startswith("handle_"):
                                method = getattr(plugin_instance, method_name)
                                if callable(method):
                                    logger.debug(
                                        f"发现插件方法: {plugin_name}.{method_name}"
                                    )

                                    # 尝试手动注册到事件管理器
                                    if method_name == "handle_text":
                                        try:
                                            from opengewe.callback.types import (
                                                MessageType,
                                            )

                                            if hasattr(event_manager, "handlers"):
                                                event_manager.handlers[
                                                    MessageType.TEXT
                                                ].append(method)
                                                logger.debug(
                                                    f"已手动注册文本消息处理器: {plugin_name}.{method_name}"
                                                )
                                        except Exception as e:
                                            logger.error(
                                                f"手动注册文本消息处理器失败: {e}"
                                            )

                except Exception as e:
                    logger.error(f"重新注册插件事件处理器失败: {e}")

            # 检查插件是否正确注册了事件处理器
            if hasattr(plugin_manager, "event_manager") and hasattr(
                plugin_manager.event_manager, "handlers"
            ):
                handlers = plugin_manager.event_manager.handlers
                total_handlers = sum(
                    len(handler_list) for handler_list in handlers.values()
                )
                logger.debug(
                    f"机器人 {bot.gewe_app_id} 的事件处理器数量: {total_handlers}"
                )

                if total_handlers == 0:
                    logger.warning(f"机器人 {bot.gewe_app_id} 没有注册任何事件处理器")

        except Exception as e:
            logger.error(f"启动插件管理器失败: {e}", exc_info=True)

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
                    stmt = select(BotInfo).where(
                        BotInfo.gewe_app_id == gewe_app_id)
                    result = await session.execute(stmt)
                    bot = result.scalar_one_or_none()
                    if bot:
                        await self._load_plugins_for_bot(client, bot, session)
        else:
            # 重新加载所有插件
            self._plugins_loaded = False
            self._available_plugins.clear()
            await self._load_available_plugins()  # 重新扫描插件目录

            # 重新初始化所有客户端的插件
            for gewe_app_id, client in self._clients.items():
                # 先卸载所有旧插件
                await client.plugin_manager.unload_plugins()

                # 然后像首次加载一样，重新加载所有插件并注入配置
                async with admin_session() as session:
                    stmt = select(BotInfo).where(
                        BotInfo.gewe_app_id == gewe_app_id)
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
            # 获取插件管理器信息
            plugin_manager_info = {
                "plugin_count": len(client.plugin_manager.plugins),
                "registered_plugins": list(client.plugin_manager.plugins.keys()),
            }

            # 尝试获取更多插件信息
            if hasattr(client.plugin_manager, "plugin_info"):
                plugin_manager_info["plugin_info"] = client.plugin_manager.plugin_info
                plugin_manager_info["enabled_plugins"] = [
                    name
                    for name, info in client.plugin_manager.plugin_info.items()
                    if info.get("enabled", False)
                ]

            # 获取事件处理器信息
            event_handlers_info = {}
            if hasattr(client.plugin_manager, "event_manager"):
                event_manager = client.plugin_manager.event_manager
                if hasattr(event_manager, "handlers"):
                    for event_type, handlers in event_manager.handlers.items():
                        event_handlers_info[event_type] = len(handlers)

            plugin_status = {
                "available_plugins": list(self._available_plugins.keys()),
                "plugin_manager_info": plugin_manager_info,
                "event_handlers_info": event_handlers_info,
                "client_info": {
                    "has_plugin_manager": hasattr(client, "plugin_manager"),
                    "has_message_factory": hasattr(client, "message_factory"),
                    "plugin_manager_type": type(client.plugin_manager).__name__
                    if hasattr(client, "plugin_manager")
                    else None,
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

    async def reload_all_clients_plugins_config(self) -> Dict[str, Any]:
        """
        热重载所有机器人客户端的插件配置。
        这将重新从数据库加载配置并应用到每个客户端。
        """
        logger.info("开始热重载所有客户端的插件配置...")

        # 1. 强制重新扫描插件目录，刷新可用的插件类定义
        self._plugins_loaded = False
        self._available_plugins.clear()
        await self._load_available_plugins()

        results = {}
        # 2. 遍历所有客户端，重新加载它们的插件
        for gewe_app_id, client in self._clients.items():
            try:
                logger.info(f"正在为客户端 {gewe_app_id} 重载插件...")

                # a. 卸载当前客户端的所有插件
                unloaded, failed_unloads = await client.plugin_manager.unload_plugins()
                logger.info(
                    f"客户端 {gewe_app_id}: 已卸载 {len(unloaded)} 个插件, "
                    f"失败 {len(failed_unloads)} 个。"
                )
                if failed_unloads:
                    logger.warning(f"卸载失败的插件: {failed_unloads}")

                # b. 像首次加载一样，重新从数据库加载配置并加载插件
                async with admin_session() as session:
                    stmt = select(BotInfo).where(
                        BotInfo.gewe_app_id == gewe_app_id)
                    result = await session.execute(stmt)
                    bot = result.scalar_one_or_none()

                    if bot:
                        await self._load_plugins_for_bot(client, bot, session)
                        loaded_plugins = list(
                            client.plugin_manager.plugins.keys())
                        results[gewe_app_id] = {
                            "status": "success",
                            "loaded": len(loaded_plugins),
                            "loaded_plugins": loaded_plugins,
                        }
                        logger.info(f"客户端 {gewe_app_id} 插件配置重载成功。")
                    else:
                        results[gewe_app_id] = {
                            "status": "error",
                            "message": f"未在数据库中找到机器人信息: {gewe_app_id}",
                        }
                        logger.error(
                            f"无法重载客户端 {gewe_app_id} 的插件，因为在数据库中找不到它。"
                        )

            except Exception as e:
                logger.error(f"客户端 {gewe_app_id} 插件配置重载失败: {e}", exc_info=True)
                results[gewe_app_id] = {"status": "error", "message": str(e)}

        logger.info("所有客户端插件配置热重载完成。")
        return results


# 创建全局单例实例
bot_manager = BotClientManager()
