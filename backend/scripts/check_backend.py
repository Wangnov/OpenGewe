#!/usr/bin/env python
"""
检查后端服务状态

此脚本用于检查后端服务是否正常运行，并验证API端点是否可访问。
"""

import asyncio
import sys
import os
import tomllib
import httpx
import socket
import json
import subprocess
from pathlib import Path

# 添加项目根目录到模块搜索路径
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from opengewe.logger import init_default_logger, get_logger

# 初始化日志
init_default_logger(level="INFO")
logger = get_logger("Backend-Check")

# 前端服务端口
FRONTEND_PORT = 5432

# 默认后端服务端口
DEFAULT_BACKEND_PORT = 5433


async def check_port_open(host, port):
    """检查指定端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        logger.error(f"检查端口时出错: {e}")
        return False


async def check_backend_api(url, endpoint):
    """检查后端API端点是否可访问"""
    try:
        # 确保endpoint不包含/v1前缀
        if endpoint.startswith("/api/v1/"):
            endpoint = endpoint.replace("/api/v1/", "/api/")
            logger.info(f"已将API路径中的v1前缀移除: {endpoint}")

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}{endpoint}", timeout=5.0)
            logger.info(f"API响应状态码: {response.status_code}")
            logger.debug(f"API响应内容: {response.text}")
            return response.status_code < 500  # 任何非500错误都算API可访问
    except Exception as e:
        logger.error(f"访问API时出错: {e}")
        return False


async def read_config():
    """读取配置文件"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "main_config.toml",
    )
    if not os.path.exists(config_path):
        logger.error(f"配置文件不存在: {config_path}")
        return None

    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        logger.error(f"读取配置文件时出错: {e}")
        return None


async def check_process_running(port):
    """检查是否有进程正在使用指定端口"""
    if sys.platform == "win32":
        # Windows
        try:
            output = subprocess.check_output(
                f"netstat -aon | findstr :{port}", shell=True
            ).decode()
            if output:
                lines = output.strip().split("\n")
                for line in lines:
                    if f":{port}" in line and "LISTENING" in line:
                        parts = line.strip().split()
                        pid = parts[-1]
                        return True, pid
            return False, None
        except subprocess.CalledProcessError:
            return False, None
    else:
        # macOS/Linux
        try:
            output = subprocess.check_output(
                f"lsof -i :{port} -P -n", shell=True
            ).decode()
            if output:
                lines = output.strip().split("\n")
                if len(lines) > 1:  # 第一行是列名
                    pid = lines[1].split()[1]
                    return True, pid
            return False, None
        except subprocess.CalledProcessError:
            return False, None


async def start_backend_service():
    """尝试启动后端服务"""
    logger.info("尝试启动后端服务...")
    project_root = Path(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
    start_script = project_root / "start_backend.sh"

    if start_script.exists():
        try:
            # 使用nohup在后台启动服务
            logger.info(f"执行启动脚本: {start_script}")
            subprocess.Popen(
                ["nohup", "bash", str(start_script), "&"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            logger.success("后端服务启动命令已执行，请等待几秒钟...")
            return True
        except Exception as e:
            logger.error(f"启动后端服务时出错: {e}")
            return False
    else:
        logger.error(f"启动脚本不存在: {start_script}")
        return False


async def main():
    """主函数"""
    config = await read_config()
    if not config:
        logger.error("无法读取配置文件")
        return

    # 获取后端服务配置
    host = config["backend"]["host"]
    port = config["backend"]["port"]

    logger.info(f"前端服务端口: {FRONTEND_PORT}")
    logger.info(f"后端服务端口: {port}")

    # 如果host是0.0.0.0，则使用localhost进行测试
    test_host = "localhost" if host == "0.0.0.0" else host

    # 检查是否有进程在使用该端口
    process_running, pid = await check_process_running(port)
    if process_running:
        logger.info(f"检测到进程(PID: {pid})正在使用端口 {port}")
    else:
        logger.warning(f"未检测到进程使用端口 {port}，后端服务可能未启动")

        # 询问是否要启动后端服务
        user_input = input("是否要尝试启动后端服务? (y/n): ")
        if user_input.lower() == "y":
            if await start_backend_service():
                logger.info("等待服务启动...")
                # 等待服务启动
                for _ in range(10):  # 最多等待10秒
                    await asyncio.sleep(1)
                    port_open = await check_port_open(test_host, port)
                    if port_open:
                        logger.success(f"端口 {port} 已开放，服务可能已启动")
                        break
            else:
                logger.error("无法启动后端服务")
                return

    # 检查端口是否开放
    logger.info(f"检查后端服务端口 {test_host}:{port} 是否开放...")
    port_open = await check_port_open(test_host, port)
    if port_open:
        logger.success(f"端口 {port} 已开放")
    else:
        logger.error(f"端口 {port} 未开放")
        logger.info("请确保后端服务已启动")
        logger.info("可以手动执行以下命令启动后端服务：")
        logger.info("bash /path/to/your/project/start_backend.sh")
        return

    # 检查API端点
    logger.info("检查后端API端点...")
    base_url = f"http://{test_host}:{port}"

    # 检查健康检查端点
    health_check = await check_backend_api(base_url, "/health")
    if health_check:
        logger.success("/health 端点可访问")
    else:
        logger.error("/health 端点不可访问")

    # 检查admin/check-init端点 - 使用正确的路径（不带v1前缀）
    admin_check = await check_backend_api(base_url, "/api/admin/check-init")
    if admin_check:
        logger.success("/api/admin/check-init 端点可访问")
    else:
        logger.error("/api/admin/check-init 端点不可访问")
        logger.info("请检查后端路由配置是否正确")

        # 检查是否有v1前缀的路由 - 现在不鼓励使用v1前缀
        v1_check = await check_backend_api(base_url, "/api/v1/admin/check-init")
        if v1_check:
            logger.warning("注意: 端点 /api/v1/admin/check-init 可访问 (使用了v1前缀)")
            logger.info("但前端已配置为不使用v1前缀，请确保后端路由配置正确")

    # 输出总结
    if health_check and admin_check:
        logger.success("后端服务运行正常，所有检查都通过")
        logger.info(f"前端: http://localhost:{FRONTEND_PORT}")
        logger.info(f"后端: http://{test_host}:{port}")
    else:
        logger.warning("后端服务可能存在问题，请查看上述日志")

    # 检查前端端口是否被占用
    frontend_port_open = await check_port_open("localhost", FRONTEND_PORT)
    if not frontend_port_open:
        logger.warning(f"前端端口 {FRONTEND_PORT} 可能未开放，请确保前端服务已启动")
    else:
        logger.info(f"前端端口 {FRONTEND_PORT} 已开放")


if __name__ == "__main__":
    asyncio.run(main())
