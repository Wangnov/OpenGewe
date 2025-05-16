"""插件服务模块

提供插件管理的业务逻辑，包括插件的获取、启用/禁用、配置更新等功能。
"""

import os
import sys
import importlib
import inspect
from typing import Dict, List, Optional, Any, Tuple

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

        # 扫描文件系统中的插件
        plugins = await PluginService.scan_plugins()

        # 获取数据库中的插件
        db_plugins = await Plugin.get_all()
        db_plugin_names = {p.name for p in db_plugins}

        added = 0
        updated = 0
        failed = 0

        # 同步插件
        for plugin_info in plugins:
            name = plugin_info["name"]

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
                else:
                    failed += 1
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
                    # 更新插件信息
                    plugin.display_name = plugin_info["display_name"]
                    plugin.description = plugin_info["description"]
                    plugin.version = plugin_info["version"]
                    plugin.author = plugin_info["author"]
                    plugin.path = plugin_info["path"]

                    # 保存更新
                    try:
                        from backend.app.db.session import DatabaseManager

                        db_manager = DatabaseManager()
                        async with db_manager.get_session() as session:
                            session.add(plugin)
                            await session.commit()
                            updated += 1
                    except Exception as e:
                        logger.error(f"更新插件 {name} 失败: {e}")
                        failed += 1

        return added, updated, failed

    @staticmethod
    async def get_loaded_plugins() -> List[Dict[str, Any]]:
        """获取当前加载的插件

        返回所有当前在GeweClient中加载的插件。

        Returns:
            List[Dict[str, Any]]: 已加载的插件列表
        """
        try:
            # 获取默认客户端
            client = await get_gewe_client()

            # 获取已加载的插件
            if hasattr(client, "plugin_manager"):
                # 获取插件信息
                loaded_plugins = client.plugin_manager.get_plugin_info()
                return (
                    loaded_plugins
                    if isinstance(loaded_plugins, list)
                    else [loaded_plugins]
                )

            return []
        except Exception as e:
            logger.error(f"获取已加载插件时出错: {e}")
            return []
