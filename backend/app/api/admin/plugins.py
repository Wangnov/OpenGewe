"""
插件管理API端点
"""
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.database import get_admin_session
from ...core.security import require_superadmin
from ...models.admin import GlobalPlugin
from ...schemas.plugin import GlobalPluginInfo, GlobalPluginInfoResponse, UpdateGlobalPluginRequest
from opengewe.logger import get_logger

import ast
try:
    import tomllib
except ImportError:
    import tomli as tomllib

logger = get_logger(__name__)
router = APIRouter()

# --- Helper Functions ---


def get_plugin_metadata(plugin_path: Path) -> Dict[str, Any]:
    """使用AST从插件的main.py文件中安全地提取元数据"""
    metadata = {
        "name": plugin_path.name,
        "description": None,
        "author": "佚名",
        "version": "未知",
    }
    main_py_path = plugin_path / "main.py"
    if not main_py_path.exists():
        return metadata

    try:
        with open(main_py_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and any(isinstance(b, ast.Name) and b.id == 'PluginBase' for b in node.bases):
                # 优先使用文档字符串作为描述
                docstring = ast.get_docstring(node)
                if docstring:
                    metadata['description'] = docstring.strip().split('\n')[0]

                # 遍历类成员进行赋值
                for class_node in node.body:
                    if isinstance(class_node, ast.Assign):
                        try:
                            target_name = class_node.targets[0].id
                            value_node = class_node.value

                            # 兼容 Python 3.8+ (ast.Constant) 和更早版本 (ast.Str)
                            str_value = None
                            if isinstance(value_node, ast.Constant):
                                str_value = value_node.value
                            elif isinstance(value_node, ast.Str):
                                str_value = value_node.s

                            if isinstance(str_value, str):
                                if target_name == 'name':
                                    metadata['name'] = str_value
                                # 如果已有文档字符串，则不再覆盖description
                                elif target_name == 'description' and not metadata.get('description'):
                                    metadata['description'] = str_value
                                elif target_name in ('author', '__author__'):
                                    metadata['author'] = str_value
                                elif target_name in ('version', '__version__'):
                                    metadata['version'] = str_value
                        except (AttributeError, IndexError):
                            continue
                # 找到第一个插件类后就停止
                break
    except Exception as e:
        logger.warning(f"使用AST解析插件元数据失败 {plugin_path.name}: {e}")

    return metadata


def get_plugin_readme(plugin_path: Path) -> Optional[str]:
    """获取插件的README.md内容"""
    readme_path = plugin_path / "README.md"
    if readme_path.exists():
        try:
            return readme_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"读取README失败 {plugin_path.name}: {e}")
    return None


def get_plugin_config_schema(plugin_path: Path) -> Optional[Dict[str, Any]]:
    """获取插件的默认配置（从config.toml）"""
    config_path = plugin_path / "config.toml"
    if config_path.exists():
        try:
            with open(config_path, "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            logger.warning(f"读取config.toml失败 {plugin_path.name}: {e}")
    return None

# --- API Endpoints ---


@router.get("", response_model=GlobalPluginInfoResponse, summary="获取所有可用插件列表")
async def get_available_plugins(
    current_user: dict = Depends(require_superadmin),
    session: AsyncSession = Depends(get_admin_session),
):
    """
    获取文件系统中所有可用的插件及其在数据库中的全局启用状态。
    """
    project_root = Path(__file__).parent.parent.parent.parent.parent
    plugins_dir = project_root / "plugins"

    if not plugins_dir.exists() or not plugins_dir.is_dir():
        return GlobalPluginInfoResponse(data=[])

    # 1. 从数据库获取所有全局插件的启用状态
    stmt = select(GlobalPlugin)
    result = await session.execute(stmt)
    db_plugins = {p.plugin_name: p for p in result.scalars().all()}

    # 2. 扫描插件目录并合并信息
    plugin_infos: List[GlobalPluginInfo] = []

    tasks = []
    for plugin_path in plugins_dir.iterdir():
        if plugin_path.is_dir() and not plugin_path.name.startswith(('.', '_')) and plugin_path.name != 'utils':
            tasks.append(process_plugin_dir(plugin_path, db_plugins))

    plugin_infos = await asyncio.gather(*tasks)

    # 过滤掉None的结果
    plugin_infos = [info for info in plugin_infos if info]

    return GlobalPluginInfoResponse(data=plugin_infos)


async def process_plugin_dir(plugin_path: Path, db_plugins: Dict[str, GlobalPlugin]) -> Optional[GlobalPluginInfo]:
    """异步处理单个插件目录"""
    try:
        plugin_id = plugin_path.name
        metadata = get_plugin_metadata(plugin_path)
        readme = get_plugin_readme(plugin_path)
        config_schema = get_plugin_config_schema(plugin_path)

        db_plugin = db_plugins.get(plugin_id)
        is_globally_enabled = db_plugin.is_globally_enabled if db_plugin else False

        return GlobalPluginInfo(
            plugin_id=plugin_id,
            is_globally_enabled=is_globally_enabled,
            **metadata,
            readme=readme,
            config_schema=config_schema,
        )
    except Exception as e:
        logger.error(f"处理插件目录失败 {plugin_path.name}: {e}")
        return None


@router.put("/{plugin_id}", summary="更新插件的全局启用状态")
async def update_global_plugin_status(
    plugin_id: str,
    request: UpdateGlobalPluginRequest,
    current_user: dict = Depends(require_superadmin),
    session: AsyncSession = Depends(get_admin_session),
):
    """
    更新指定插件的全局启用/禁用状态。
    如果插件在数据库中不存在，会自动创建记录。
    """
    stmt = select(GlobalPlugin).where(GlobalPlugin.plugin_name == plugin_id)
    result = await session.execute(stmt)
    db_plugin = result.scalar_one_or_none()

    if db_plugin:
        db_plugin.is_globally_enabled = request.is_globally_enabled
    else:
        db_plugin = GlobalPlugin(
            plugin_name=plugin_id,
            is_globally_enabled=request.is_globally_enabled
        )
        session.add(db_plugin)

    await session.commit()

    return {"status": "success", "message": f"插件 '{plugin_id}' 的全局状态已更新。"}
