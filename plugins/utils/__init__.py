"""OpenGewe插件桥接层

此包为插件提供与opengewe包兼容的导入路径，
允许使用形如"from utils.xxx import Yyy"的导入语句，
而实际导入的是opengewe包中的相应模块。
"""

import sys
import importlib
import os
from types import ModuleType
import importlib.util
import inspect

# 尝试导入opengewe的logger，如果失败则使用print fallback
_logger = None
try:
    from opengewe.logger import get_logger
    _logger = get_logger("Plugins.Utils.Proxy")
except ImportError:
    pass

def _log_debug(message: str) -> None:
    """调试日志记录"""
    if _logger:
        _logger.debug(message)
    # 在DEBUG模式下才打印到控制台
    elif os.environ.get("OPENGEWE_DEBUG", "").lower() in ("true", "1", "yes"):
        print(f"[DEBUG] Plugins.Utils.Proxy: {message}")

def _log_warning(message: str) -> None:
    """警告日志记录"""
    if _logger:
        _logger.warning(message)
    else:
        print(f"[WARNING] Plugins.Utils.Proxy: {message}")

# 启用更详细的调试
DEBUG = os.environ.get("OPENGEWE_DEBUG", "").lower() in ("true", "1", "yes")

# 存储已导入的模块缓存
_module_cache = {}


class UtilsModuleProxy(ModuleType):
    """utils模块的代理，重定向导入到plugins.utils或opengewe.utils"""

    def __init__(self, name):
        super().__init__(name)
        # 获取当前目录路径
        self.__path__ = [os.path.dirname(os.path.abspath(__file__))]
        # 存储已导入的子模块
        self._loaded_submodules = {}

        _log_debug(f"初始化utils模块代理，路径={self.__path__}")
        _log_debug(f"当前sys.path={sys.path[:3]}...")  # 只显示前3个路径避免日志过长

    def __getattr__(self, name):
        # 已加载的子模块直接返回
        if name in self._loaded_submodules:
            return self._loaded_submodules[name]

        # 特殊属性处理
        if name == "__path__":
            return self.__path__

        # 尝试不同的导入策略
        module = None

        # 策略1: 直接从plugins.utils导入
        try:
            _log_debug(f"尝试从plugins.utils导入{name}")
            module = importlib.import_module(f"plugins.utils.{name}")
            _log_debug(f"成功从plugins.utils导入{name}")
            self._loaded_submodules[name] = module
            return module
        except ImportError as e:
            _log_debug(f"从plugins.utils导入{name}失败: {e}")
            pass

        # 策略2: 从opengewe.utils导入
        try:
            _log_debug(f"尝试从opengewe.utils导入{name}")
            module = importlib.import_module(f"opengewe.utils.{name}")
            _log_debug(f"成功从opengewe.utils导入{name}")
            self._loaded_submodules[name] = module
            return module
        except ImportError as e:
            _log_debug(f"从opengewe.utils导入{name}失败: {e}")
            pass

        # 策略3: 直接加载插件目录下的模块文件
        try:
            module_path = os.path.join(self.__path__[0], f"{name}.py")
            if os.path.exists(module_path):
                _log_debug(f"尝试从文件{module_path}加载模块")

                spec = importlib.util.spec_from_file_location(
                    f"utils.{name}", module_path
                )
                module = importlib.util.module_from_spec(spec)

                # 将模块添加到sys.modules中，以便其他模块可以导入它
                sys.modules[f"utils.{name}"] = module

                # 执行模块
                spec.loader.exec_module(module)

                _log_debug(f"成功从文件{module_path}加载模块")

                self._loaded_submodules[name] = module
                return module
        except Exception as e:
            _log_debug(f"从文件加载模块{name}失败: {e}")
            pass

        # 如果所有策略都失败，抛出AttributeError
        raise AttributeError(f"模块 'utils' 没有属性 '{name}'")


# 从opengewe.utils导入所有模块并添加到utils模块代理中
def _import_all_from_opengewe():
    try:
        import opengewe.utils

        loaded_count = 0
        for name in dir(opengewe.utils):
            # 排除特殊属性和方法
            if not name.startswith("_"):
                # 获取属性
                attr = getattr(opengewe.utils, name)
                # 如果是模块，添加到utils模块代理
                if inspect.ismodule(attr):
                    module_name = f"utils.{name}"
                    if module_name not in sys.modules:
                        sys.modules[module_name] = attr
                        loaded_count += 1
        
        if loaded_count > 0:
            _log_debug(f"成功从opengewe.utils预加载了{loaded_count}个模块")
    except ImportError:
        _log_warning("无法导入opengewe.utils，插件工具代理功能受限")
    except Exception as e:
        _log_warning(f"预加载opengewe.utils模块时出错: {e}")


# 只创建一次utils模块代理
if "utils" not in sys.modules:
    # 创建utils模块代理
    utils_module = UtilsModuleProxy("utils")
    # 将模块添加到sys.modules
    sys.modules["utils"] = utils_module
    # 从opengewe.utils导入所有模块
    _import_all_from_opengewe()

# 导出所有桥接层模块
__all__ = ["plugin_base", "plugin_manager", "decorators", "event_manager", "singleton"]
