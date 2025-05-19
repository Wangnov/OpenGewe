"""插件服务模块

提供插件管理的业务逻辑，包括插件的获取、启用/禁用、配置更新等功能。
"""

import os
import sys
import importlib
import inspect
from typing import Dict, List, Optional, Any, Tuple

from sqlalchemy import select

from opengewe.client import GeweClient
from opengewe.logger import get_logger
from opengewe.utils.plugin_base import PluginBase

from backend.app.models.plugin import Plugin
from backend.app.core.config import get_settings
from backend.app.gewe import get_gewe_client

# 获取日志记录器
logger = get_logger("PluginService")


class PluginService:
    """插件服务类

    提供插件管理的业务逻辑。
    """

    @staticmethod
    async def get_all_plugins(include_disabled: bool = True) -> List[Dict[str, Any]]:
        """获取所有插件

        Args:
            include_disabled: 是否包含已禁用的插件

        Returns:
            List[Dict[str, Any]]: 插件列表
        """
        if include_disabled:
            plugins = await Plugin.get_all()
        else:
            plugins = await Plugin.get_enabled()

        return [plugin.to_dict() for plugin in plugins]

    @staticmethod
    async def get_plugin_by_name(name: str) -> Optional[Dict[str, Any]]:
        """获取指定名称的插件

        Args:
            name: 插件名称

        Returns:
            Optional[Dict[str, Any]]: 插件信息，如果不存在则为None
        """
        plugin = await Plugin.get_by_name(name)
        return plugin.to_dict() if plugin else None

    @staticmethod
    async def enable_plugin(
        name: str, client: Optional[GeweClient] = None
    ) -> Tuple[bool, str]:
        """启用插件

        Args:
            name: 插件名称
            client: 可选的GeweClient实例，如果不提供则使用默认实例

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 在数据库中启用插件
        result = await Plugin.toggle_enabled(name, True)
        if not result:
            return False, f"插件 {name} 不存在或启用失败"

        # 如果提供了客户端，尝试加载插件
        if client:
            try:
                # 获取插件对象
                plugin = await Plugin.get_by_name(name)
                if not plugin:
                    return False, f"插件 {name} 不存在"

                # 查找插件类并加载
                plugin_loaded = await client.plugin_manager.load_plugin(name)
                if not plugin_loaded:
                    await Plugin.toggle_enabled(name, False)  # 回滚数据库状态
                    return False, f"插件 {name} 加载失败"

                return True, f"插件 {name} 已启用并加载"
            except Exception as e:
                logger.error(f"启用插件 {name} 时出错: {e}")
                await Plugin.toggle_enabled(name, False)  # 回滚数据库状态
                return False, f"启用插件出错: {str(e)}"

        return True, f"插件 {name} 已启用"

    @staticmethod
    async def disable_plugin(
        name: str, client: Optional[GeweClient] = None
    ) -> Tuple[bool, str]:
        """禁用插件

        Args:
            name: 插件名称
            client: 可选的GeweClient实例，如果不提供则使用默认实例

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 在数据库中禁用插件
        result = await Plugin.toggle_enabled(name, False)
        if not result:
            return False, f"插件 {name} 不存在或禁用失败"

        # 如果提供了客户端，尝试卸载插件
        if client and hasattr(client, "plugin_manager"):
            try:
                # 卸载插件
                unloaded, failed = await client.plugin_manager.unload_plugins([name])
                if name not in unloaded:
                    logger.warning(f"插件 {name} 卸载失败，但在数据库中已禁用")
                    if name in failed:
                        return (
                            True,
                            f"插件 {name} 已在数据库中禁用，但卸载失败: {failed[name]}",
                        )
                    return True, f"插件 {name} 已在数据库中禁用，但卸载失败"

                return True, f"插件 {name} 已禁用并卸载"
            except Exception as e:
                logger.error(f"禁用插件 {name} 时出错: {e}")
                return True, f"插件已在数据库中禁用，但卸载出错: {str(e)}"

        return True, f"插件 {name} 已禁用"

    @staticmethod
    async def update_plugin_config(
        name: str, config: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """更新插件配置

        Args:
            name: 插件名称
            config: 新配置

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await Plugin.update_config(name, config)
        if result:
            return True, f"插件 {name} 配置已更新"
        else:
            return False, f"插件 {name} 不存在或配置更新失败"

    @staticmethod
    async def scan_plugins() -> List[Dict[str, Any]]:
        """扫描文件系统中的插件

        扫描插件目录，查找所有可用的插件，并返回插件信息。

        Returns:
            List[Dict[str, Any]]: 插件信息列表
        """
        settings = get_settings()
        plugins_dir = settings.plugins.plugins_dir
        found_plugins = []

        if not os.path.isdir(plugins_dir):
            logger.warning(f"插件目录 {plugins_dir} 不存在")
            return []

        # 扫描插件目录
        for dirname in os.listdir(plugins_dir):
            plugin_path = os.path.join(plugins_dir, dirname)
            main_file = os.path.join(plugin_path, "main.py")

            if os.path.isdir(plugin_path) and os.path.exists(main_file):
                try:
                    # 导入插件模块
                    module_name = f"plugins.{dirname}.main"
                    if module_name not in [
                        m.__name__
                        for m in list(sys.modules.values())
                        if hasattr(m, "__name__")
                    ]:
                        module = importlib.import_module(module_name)
                    else:
                        module = importlib.reload(sys.modules[module_name])

                    # 查找插件类
                    for name, obj in inspect.getmembers(module):
                        if (
                            inspect.isclass(obj)
                            and issubclass(obj, PluginBase)
                            and obj != PluginBase
                        ):
                            # 获取插件信息
                            plugin_info = {
                                "name": obj.__name__,
                                "display_name": getattr(
                                    obj, "display_name", obj.__name__
                                ),
                                "description": getattr(obj, "description", ""),
                                "version": getattr(obj, "version", "0.1.0"),
                                "author": getattr(obj, "author", "Unknown"),
                                "path": dirname,
                            }
                            found_plugins.append(plugin_info)
                except Exception as e:
                    logger.error(f"扫描插件 {dirname} 时出错: {e}")
                    continue

        return found_plugins

    @staticmethod
    async def sync_plugins() -> Tuple[int, int, int]:
        """同步文件系统中的插件和数据库记录

        扫描文件系统中的插件，将新插件添加到数据库中，并更新现有插件的信息。

        Returns:
            Tuple[int, int, int]: (添加的插件数, 更新的插件数, 失败的插件数)
        """
        logger.debug("开始同步插件信息")

        # 扫描文件系统中的插件
        plugins = await PluginService.scan_plugins()
        logger.debug(f"从文件系统中扫描到 {len(plugins)} 个插件")

        # 获取数据库中的插件
        db_plugins = await Plugin.get_all()
        db_plugin_names = {p.name for p in db_plugins}
        logger.debug(f"数据库中已有 {len(db_plugins)} 个插件记录")

        added = 0
        updated = 0
        failed = 0

        # 同步插件
        for plugin_info in plugins:
            name = plugin_info["name"]

            try:
                if name not in db_plugin_names:
                    # 添加新插件
                    result = await Plugin.create(
                        name=name,
                        display_name=plugin_info["display_name"],
                        description=plugin_info["description"],
                        version=plugin_info["version"],
                        path=plugin_info["path"],
                        author=plugin_info["author"],
                    )
                    if result:
                        added += 1
                        logger.debug(f"添加新插件: {name}")
                    else:
                        failed += 1
                        logger.error(f"添加插件 {name} 失败")
                else:
                    # 更新现有插件信息
                    plugin = next(p for p in db_plugins if p.name == name)

                    # 检查是否需要更新
                    if (
                        plugin.display_name != plugin_info["display_name"]
                        or plugin.description != plugin_info["description"]
                        or plugin.version != plugin_info["version"]
                        or plugin.author != plugin_info["author"]
                        or plugin.path != plugin_info["path"]
                    ):
                        # 使用更安全的异步上下文管理器模式保存更新
                        try:
                            from backend.app.db import async_db_session

                            # 在单独的会话中更新插件信息
                            async with async_db_session() as session:
                                # 再次查询以防并发更改
                                refresh_query = await session.execute(
                                    select(Plugin).where(Plugin.name == name)
                                )
                                db_plugin = refresh_query.scalars().first()

                                if db_plugin:
                                    db_plugin.display_name = plugin_info["display_name"]
                                    db_plugin.description = plugin_info["description"]
                                    db_plugin.version = plugin_info["version"]
                                    db_plugin.author = plugin_info["author"]
                                    db_plugin.path = plugin_info["path"]

                                    await session.commit()
                                    updated += 1
                                    logger.debug(f"更新插件: {name}")
                                else:
                                    logger.warning(f"尝试更新插件 {name} 时找不到记录")
                        except Exception as e:
                            logger.error(f"更新插件 {name} 失败: {e}")
                            failed += 1
            except Exception as e:
                logger.error(f"处理插件 {name} 时出错: {e}")
                failed += 1

        logger.info(
            f"插件同步完成: 添加 {added} 个, 更新 {updated} 个, 失败 {failed} 个"
        )
        return added, updated, failed

    @staticmethod
    async def get_loaded_plugins() -> List[Dict[str, Any]]:
        """获取当前已加载的插件

        Returns:
            List[Dict[str, Any]]: 已加载的插件列表
        """
        client = await get_gewe_client()
        if not client:
            return []

        loaded_plugins = []
        for plugin_name in client.plugin_manager.get_active_plugins():
            plugin = await Plugin.get_by_name(plugin_name)
            if plugin:
                plugin_data = plugin.to_dict()
                plugin_data["loaded"] = True
                loaded_plugins.append(plugin_data)

        return loaded_plugins

    @staticmethod
    async def load_enabled_plugins() -> Tuple[bool, str, Dict[str, Any]]:
        """加载所有已启用的插件

        在应用启动时调用此方法，为所有设备加载已启用的插件。

        Returns:
            Tuple[bool, str, Dict[str, Any]]:
                (成功标志, 消息, 包含已加载和失败插件列表的字典)
        """
        try:
            # 获取已启用的插件列表
            logger.debug("正在获取已启用的插件列表...")
            enabled_plugins = await Plugin.get_enabled()
            plugin_names = [plugin.name for plugin in enabled_plugins]

            # 如果数据库中没有启用的插件，尝试从配置文件读取
            if not plugin_names:
                settings = get_settings()
                config_enabled_plugins = settings.plugins.enabled_plugins

                if config_enabled_plugins:
                    logger.info(
                        f"数据库中没有启用的插件，从配置文件读取: {config_enabled_plugins}"
                    )
                    plugin_names = config_enabled_plugins
                else:
                    logger.info("没有已启用的插件需要加载")
                    return (
                        True,
                        "没有已启用的插件需要加载",
                        {"loaded": [], "failed": []},
                    )

            # 如果应用启动时没有请求上下文，使用默认设备
            try:
                # 获取GeweClient
                client = await get_gewe_client()
            except Exception as e:
                # 如果获取失败（可能是因为没有请求上下文），尝试使用默认设备创建客户端
                logger.warning(f"无法通过依赖获取客户端: {e}")
                settings = get_settings()
                try:
                    default_device_id = settings.devices.get_default_device_id()
                    logger.info(f"使用默认设备 {default_device_id} 创建客户端")

                    from backend.app.gewe.client_manager import client_manager

                    client = await client_manager.get_client(
                        default_device_id, load_plugins=False
                    )
                except Exception as e2:
                    logger.error(f"无法获取默认设备或创建客户端: {e2}")
                    return (
                        False,
                        f"无法获取客户端: {str(e2)}",
                        {"loaded": [], "failed": plugin_names},
                    )

            if not client:
                logger.error("无法获取GeweClient，插件加载失败")
                return (
                    False,
                    "无法获取GeweClient",
                    {"loaded": [], "failed": plugin_names},
                )

            # 在单个事务中同步插件表
            logger.debug("同步插件信息...")
            try:
                await PluginService.sync_plugins()
            except Exception as e:
                logger.warning(f"同步插件信息时出错: {e}")
                # 继续加载，不中断流程

            # 加载插件
            loaded_plugins = []
            failed_plugins = []

            for plugin_name in plugin_names:
                try:
                    logger.info(f"正在加载插件: {plugin_name}")
                    plugin_loaded = await client.plugin_manager.load_plugin(plugin_name)

                    if plugin_loaded:
                        loaded_plugins.append(plugin_name)
                        logger.success(f"插件 {plugin_name} 加载成功")

                        # 如果插件加载成功但数据库中未启用，则在数据库中启用它
                        try:
                            plugin = await Plugin.get_by_name(plugin_name)
                            if plugin is None:
                                # 可能是新插件，但在加载前未同步到数据库
                                logger.debug(
                                    f"插件 {plugin_name} 不在数据库中，将为其创建记录"
                                )
                                continue

                            if not plugin.enabled:
                                logger.info(
                                    f"插件 {plugin_name} 已加载但数据库未启用，更新数据库"
                                )
                                await Plugin.toggle_enabled(plugin_name, True)
                        except Exception as db_error:
                            # 数据库操作失败不应影响插件加载流程
                            logger.warning(f"更新插件状态时出现数据库错误: {db_error}")
                    else:
                        failed_plugins.append(plugin_name)
                        logger.warning(f"插件 {plugin_name} 加载失败")
                except Exception as e:
                    failed_plugins.append(plugin_name)
                    logger.error(f"加载插件 {plugin_name} 出错: {e}")

            # 返回结果
            if not failed_plugins:
                return (
                    True,
                    f"成功加载 {len(loaded_plugins)} 个插件",
                    {"loaded": loaded_plugins, "failed": failed_plugins},
                )
            elif loaded_plugins:
                return (
                    True,
                    f"部分加载成功: 成功 {len(loaded_plugins)} 个, 失败 {len(failed_plugins)} 个",
                    {"loaded": loaded_plugins, "failed": failed_plugins},
                )
            else:
                return (
                    False,
                    "所有插件加载失败",
                    {"loaded": [], "failed": failed_plugins},
                )

        except Exception as e:
            logger.error(f"加载插件时发生错误: {e}")
            return False, f"加载插件出错: {str(e)}", {"loaded": [], "failed": []}
