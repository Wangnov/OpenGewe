#!/usr/bin/env python3
"""
OpenGewe 模块入口点
用于直接运行 python -m opengewe 命令
"""

import os
import sys
import argparse
import asyncio

# 根据Python版本导入不同的TOML解析库
try:
    import tomllib
except ImportError:
    import tomli as tomllib # type: ignore

from opengewe.client import GeweClient
from opengewe.logger import init_default_logger, get_logger


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


async def client_command(config_path: str, device_id: str) -> None:
    """客户端启动命令"""
    # 初始化默认日志系统
    init_default_logger()
    
    # 获取logger实例
    logger = get_logger("OpenGewe.Main")
    
    logger.info(f"正在启动客户端，配置文件: {config_path}, 设备ID: {device_id}")

    try:
        # 检查配置文件是否存在
        if not os.path.exists(config_path):
            logger.error(f"配置文件不存在: {config_path}")
            return
        
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
    except Exception as e:
        logger.error(f"配置文件格式错误: {e}")
        return

    # 查找指定的设备配置
    device_config = None
    for device in config.get("devices", []):
        if device.get("device_id") == device_id:
            device_config = device
            break

    if not device_config:
        logger.error(f"配置中没有找到设备: {device_id}")
        return

    # 创建客户端实例
    client = GeweClient(
        base_url=device_config["base_url"],
        download_url=device_config.get("download_url", ""),
        callback_url=device_config.get("callback_url", ""),
        app_id=device_config.get("app_id", ""),
        token=device_config.get("token", ""),
        debug=device_config.get("debug", False),
        is_gewe=device_config.get("is_gewe", False),
        queue_type=device_config.get("queue_type", "simple"),
        **device_config.get("queue_options", {}),
    )

    try:
        # 执行登录流程
        logger.info("正在执行登录流程...")
        login_success = await client.start_login()
        
        if login_success:
            logger.info("登录成功，开始加载插件...")
            # 启动插件系统
            loaded_plugins = await client.start_plugins(
                config.get("plugins", {}).get("directory", "plugins")
            )
            logger.info(
                f"已加载 {len(loaded_plugins)} 个插件: {', '.join(loaded_plugins) if loaded_plugins else '无'}"
            )
            
            logger.info("客户端已成功启动，按 Ctrl+C 停止...")
            
            # 保持运行，直到收到中断信号
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("正在关闭客户端...")
                await client.close()
        else:
            logger.error("登录失败")
    except Exception as e:
        logger.error(f"运行客户端时出错: {e}", exc_info=True)
        await client.close()


def version_command() -> None:
    """版本信息命令"""
    from opengewe import __version__
    
    # 这里保留print因为这是用户界面需要的输出
    print(f"OpenGewe 版本: {__version__}")


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="OpenGewe - 微信机器人框架",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  opengewe client config.toml device1    # 启动客户端
  opengewe version                       # 显示版本信息
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 客户端命令
    client_parser = subparsers.add_parser("client", help="启动客户端")
    client_parser.add_argument("config", help="配置文件路径")
    client_parser.add_argument("device", help="设备ID")

    # 版本命令
    subparsers.add_parser("version", help="显示版本信息")

    args = parser.parse_args()

    if args.command == "client":
        asyncio.run(client_command(args.config, args.device))
    elif args.command == "version":
        version_command()
    else:
        # 这里保留print因为这是用户界面需要的输出
        print("请指定要执行的命令。使用 --help 查看帮助。")
        print("常用命令: client, version")


if __name__ == "__main__":
    main()
