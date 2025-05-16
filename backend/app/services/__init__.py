"""服务包

提供业务逻辑服务，包括插件管理、机器人管理、系统管理和文件管理等服务。
"""

from backend.app.services.plugin_service import PluginService
from backend.app.services.robot_service import RobotService
from backend.app.services.admin_service import AdminService
from backend.app.services.file_service import FileService

__all__ = [
    "PluginService",
    "RobotService",
    "AdminService",
    "FileService",
]
