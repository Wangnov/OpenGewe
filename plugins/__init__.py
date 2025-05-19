"""自定义插件包

此包包含自定义插件，可以被opengewe加载。
"""

import sys
import os
import importlib.util


# 导入钩子
class ImportHook:
    """导入钩子，用于解决utils模块的导入问题"""

    @staticmethod
    def install():
        """安装导入钩子"""
        # 在插件目录中添加utils目录的导入支持
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 确保utils模块可以被直接导入
        if "utils" not in sys.modules:
            # 创建utils模块并添加到sys.modules
            utils_path = os.path.join(current_dir, "utils")
            if os.path.exists(utils_path):
                # 添加utils到系统路径
                if current_dir not in sys.path:
                    sys.path.insert(0, current_dir)

                # 提前创建各种常用的utils子模块，以确保它们可被正确导入
                utils_submodules = [
                    "plugin_base",
                    "decorators",
                    "event_manager",
                    "singleton",
                ]

                for submodule in utils_submodules:
                    module_name = f"utils.{submodule}"
                    if module_name not in sys.modules:
                        module_path = os.path.join(utils_path, f"{submodule}.py")
                        if os.path.exists(module_path):
                            try:
                                spec = importlib.util.spec_from_file_location(
                                    module_name, module_path
                                )
                                module = importlib.util.module_from_spec(spec)
                                sys.modules[module_name] = module
                                spec.loader.exec_module(module)
                            except Exception as e:
                                print(f"警告: 预加载模块 {module_name} 失败: {e}")

        # 确保opengewe目录在系统路径中
        root_dir = os.path.abspath(os.path.join(current_dir, ".."))
        src_dir = os.path.join(root_dir, "src")
        if src_dir not in sys.path and os.path.exists(src_dir):
            sys.path.insert(0, src_dir)


# 安装导入钩子
ImportHook.install()
