"""数据库迁移脚本

提供命令行接口运行数据库迁移操作。
支持创建迁移、应用迁移等操作。
"""

import argparse
import os
import subprocess
import sys

# 设置环境变量和路径
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
root_dir = os.path.dirname(backend_dir)
sys.path.insert(0, root_dir)


def run_alembic_command(command, *args):
    """运行Alembic命令

    Args:
        command: Alembic命令(如revision, upgrade等)
        args: 命令参数
    """
    full_command = ["alembic", "-c", f"{backend_dir}/alembic.ini", command]
    full_command.extend(args)
    print(f"运行命令: {' '.join(full_command)}")
    subprocess.run(full_command, cwd=backend_dir)


def create_migration(message):
    """创建新的迁移

    Args:
        message: 迁移描述信息
    """
    run_alembic_command("revision", "--autogenerate", "-m", message)


def upgrade_migration(revision="head"):
    """升级数据库到指定版本

    Args:
        revision: 目标版本
    """
    run_alembic_command("upgrade", revision)


def downgrade_migration(revision="-1"):
    """降级数据库到指定版本

    Args:
        revision: 目标版本
    """
    run_alembic_command("downgrade", revision)


def show_history():
    """显示迁移历史"""
    run_alembic_command("history")


def show_current():
    """显示当前版本"""
    run_alembic_command("current")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="数据库迁移工具")
    subparsers = parser.add_subparsers(dest="command")

    # 创建迁移
    create_parser = subparsers.add_parser("create", help="创建新的迁移")
    create_parser.add_argument("message", help="迁移描述信息")

    # 应用迁移
    upgrade_parser = subparsers.add_parser("upgrade", help="升级数据库")
    upgrade_parser.add_argument(
        "--revision", default="head", help="目标版本 (默认: head)"
    )

    # 回滚迁移
    downgrade_parser = subparsers.add_parser("downgrade", help="回滚迁移")
    downgrade_parser.add_argument(
        "--revision", default="-1", help="目标版本 (默认: -1)"
    )

    # 显示历史
    subparsers.add_parser("history", help="显示迁移历史")

    # 显示当前版本
    subparsers.add_parser("current", help="显示当前版本")

    # 解析参数
    args = parser.parse_args()

    if args.command == "create":
        create_migration(args.message)
    elif args.command == "upgrade":
        upgrade_migration(args.revision)
    elif args.command == "downgrade":
        downgrade_migration(args.revision)
    elif args.command == "history":
        show_history()
    elif args.command == "current":
        show_current()
    else:
        parser.print_help()
