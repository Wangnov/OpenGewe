#!/usr/bin/env python3
"""
OpenGewe 模块入口点
用于直接运行 python -m opengewe 命令
"""

import os
import sys
import argparse
import asyncio


def parse_args() -> argparse.Namespace:
    """解析命令行参数

    Returns:
        argparse.Namespace: 包含解析后参数的命名空间
    """
    parser = argparse.ArgumentParser(
        description="OpenGewe 微信机器人框架",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 客户端子命令
    client_parser = subparsers.add_parser("client", help="启动客户端")
    client_parser.add_argument(
        "--config", type=str, default="main_config.toml", help="配置文件路径"
    )
    client_parser.add_argument("--device", type=str, default="1", help="设备ID")

    return parser.parse_args()


async def start_client(config_path: str, device_id: str) -> None:
    """启动客户端

    Args:
        config_path: 配置文件路径
        device_id: 设备ID
    """
    # 根据Python版本导入不同的TOML解析库
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib
        
    from opengewe import GeweClient
    from opengewe.logger import get_logger

    logger = get_logger("GeweClient")
    logger.info(f"正在启动客户端，配置文件: {config_path}, 设备ID: {device_id}")

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        logger.error(f"配置文件不存在: {config_path}")
        sys.exit(1)
    except tomllib.TOMLDecodeError as e:
        logger.error(f"配置文件格式错误: {e}")
        sys.exit(1)

    device_config = config.get("gewe_apps", {}).get(device_id)
    if not device_config:
        logger.error(f"配置中没有找到设备: {device_id}")
        sys.exit(1)

    client = GeweClient(
        base_url=device_config.get("base_url"),
        download_url=device_config.get("download_url", ""),
        callback_url=device_config.get("callback_url", ""),
        app_id=device_config.get("app_id", ""),
        token=device_config.get("token", ""),
        is_gewe=device_config.get("is_gewe", True),
        debug=True,
    )

    try:
        logger.info("正在执行登录流程...")
        success = await client.start_login()
        if success:
            logger.info("登录成功，开始加载插件...")
            plugins_config = config.get("plugins", {})
            plugins_dir = plugins_config.get("plugins_dir", "plugins")
            loaded_plugins = await client.start_plugins(plugins_directory=plugins_dir)
            logger.info(
                f"已加载插件: {', '.join(loaded_plugins) if loaded_plugins else '无'}"
            )

            logger.info("客户端已成功启动，按 Ctrl+C 停止...")
            # 保持运行
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("正在关闭客户端...")
            finally:
                await client.close()
        else:
            logger.error("登录失败")
            sys.exit(1)
    except Exception as e:
        logger.error(f"运行客户端时出错: {e}")
        sys.exit(1)


def show_version() -> None:
    """显示版本信息"""
    from opengewe import __version__

    print(f"OpenGewe 版本: {__version__}")


def main() -> None:
    """主入口函数"""
    args = parse_args()

    # 设置环境变量
    if hasattr(args, "config"):
        os.environ["OPENGEWE_CONFIG"] = args.config

    # 根据子命令执行相应功能
    if args.command == "client":
        asyncio.run(start_client(args.config, args.device))
    elif args.command == "version":
        show_version()
    else:
        # 默认显示帮助信息
        print("请指定要执行的命令。使用 --help 查看帮助。")
        print("常用命令: client, version")
        sys.exit(1)


if __name__ == "__main__":
    main()
