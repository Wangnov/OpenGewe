"""
FastAPI异步服务器简化版
"""

from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
import os
import tomllib
from typing import Optional
import uvicorn
import sys
import asyncio
from contextlib import asynccontextmanager

# 添加当前目录到模块搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from opengewe.client import GeweClient
from opengewe.logger import init_default_logger, get_logger

# 初始化日志系统（使用默认配置）
init_default_logger(level="INFO")

# 获取服务器主模块日志记录器
logger = get_logger("FastAPI")


# 配置读取函数
async def read_config():
    # 验证main_config.toml配置文件
    if not os.path.exists("main_config.toml"):
        logger.error("main_config.toml配置文件不存在，请检查文件是否存在")
        if os.path.exists("main_config_example.toml"):
            import shutil

            shutil.copy("main_config_example.toml", "main_config.toml")
            logger.info(
                "已复制main_config_example.toml文件到当前目录，请修改main_config.toml文件后重新启动"
            )
        exit(1)

    # 读取配置
    with open("main_config.toml", "rb") as f:
        return tomllib.load(f)


# 创建GeweClient的依赖注入
async def get_gewe_client():
    config = await read_config()

    client = GeweClient(
        base_url=config["gewe"]["base_url"],
        download_url=config["gewe"]["download_url"],
        callback_url=config["gewe"]["callback_url"],
        app_id=config["gewe"]["app_id"],
        token=config["gewe"]["token"],
        is_gewe=config["gewe"]["is_gewe"],
        debug=True,
    )

    return client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    try:
        logger.info("正在启动FastAPI服务...")

        # 读取配置
        config = await read_config()
        logger.debug(f"加载配置成功: {len(config)} 个配置项")

        # 初始化客户端
        client = await get_gewe_client()
        logger.info(f"初始化GeweClient成功，App ID: {client.app_id}")

        # 创建消息回调函数，转发消息给插件系统
        async def on_message(message):
            logger.debug(f"收到消息回调: {message.type.name}")
            # 由于plugin_manager.process_message已经在MessageFactory.process中调用，这里无需再次调用
            # 但是这里可以添加其他自定义处理逻辑

        # 注册消息回调函数
        client.message_factory.register_callback(on_message)
        logger.info("已注册消息回调函数")

        # 加载和启动插件
        logger.info("正在加载和启动插件...")
        loaded_plugins = await client.start_plugins()
        logger.info(f"已加载 {len(loaded_plugins)} 个插件: {', '.join(loaded_plugins)}")

        # 将client实例保存为应用状态
        app.state.client = client

        logger.info("应用初始化完成，使用简单队列模式")
    except Exception as e:
        logger.exception(f"启动事件发生异常: {e}")

    yield  # 应用运行期间

    # 关闭时执行的清理代码
    logger.info("应用正在关闭...")

    # 关闭客户端连接
    if hasattr(app.state, "client"):
        await app.state.client.close()
        logger.info("客户端连接已关闭")


# 创建FastAPI应用
app = FastAPI(title="OpenGewe API", description="微信自动化API接口", lifespan=lifespan)


@app.post("/callback")
async def webhook(request: Request):
    """微信回调接口"""
    try:
        # 获取JSON数据
        data = await request.json()

        if not data:
            logger.error("接收到无效的请求数据")
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "无效的请求数据"},
            )

        # 使用app.state中存储的client实例
        client = app.state.client
        if not client:
            logger.error("客户端未初始化")
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "客户端未初始化"},
            )

        # 使用client的message_factory处理消息
        logger.debug(f"接收到消息: {data}")
        task = client.message_factory.process_async(data)

        # 添加任务完成回调以记录异常
        def log_task_exception(task):
            try:
                # 获取任务异常（如果有）
                exc = task.exception()
                if exc:
                    logger.exception(f"消息处理任务异常: {exc}")
            except asyncio.CancelledError:
                logger.warning("消息处理任务被取消")

        task.add_done_callback(log_task_exception)

        # 直接返回成功，异步处理消息不会影响响应速度
        return JSONResponse(content={"status": "success"})

    except Exception as e:
        logger.exception(f"处理回调消息时出错: {e}")
        return JSONResponse(
            status_code=500, content={"status": "error", "message": str(e)}
        )


@app.get("/download/{filename:path}")
async def download_file(filename: str, custom_filename: Optional[str] = None):
    """
    文件下载接口
    支持通过URL路径下载：/download/文件名
    """
    # 安全检查：防止路径遍历攻击
    if ".." in filename or filename.startswith("/"):
        logger.warning(f"检测到非法文件路径尝试: {filename}")
        raise HTTPException(status_code=403, detail="非法的文件路径")

    download_dir = "./downloads"
    file_path = os.path.join(download_dir, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        logger.warning(f"请求的文件不存在: {file_path}")
        raise HTTPException(status_code=404, detail="文件不存在")

    logger.info(f"提供文件下载: {filename}")
    # 设置自定义文件名
    return FileResponse(
        path=file_path, filename=custom_filename if custom_filename else filename
    )


@app.get("/download")
async def download(file: str = Query(..., description="要下载的文件名")):
    """
    兼容原有的下载接口
    支持通过查询参数下载：/download?file=文件名
    """
    return await download_file(file)


@app.get("/status")
async def status():
    """健康检查接口"""
    logger.info("收到健康检查请求")  # 改为INFO级别，确保可以在控制台看到
    try:
        return {"status": "running", "queue_mode": "simple"}
    except Exception as e:
        logger.exception(f"处理状态请求时出错: {e}")
        return JSONResponse(
            status_code=500, content={"status": "error", "message": str(e)}
        )


@app.get("/logs/level/{level}")
async def set_log_level(level: str):
    """动态设置日志级别接口"""
    try:
        # 验证日志级别是否有效
        valid_levels = [
            "TRACE",
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ]
        if level.upper() not in valid_levels:
            logger.warning(f"尝试设置无效的日志级别: {level}")
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": f"无效的日志级别，有效值: {', '.join(valid_levels)}",
                },
            )

        # 设置新的日志级别
        from loguru import logger as _logger

        _logger.remove()

        # 重新配置日志系统，使用新的日志级别
        init_default_logger(level=level.upper())
        logger.info(f"日志级别已更改为: {level.upper()}")

        return {"status": "success", "level": level.upper()}
    except Exception as e:
        logger.exception(f"设置日志级别时出错: {e}")
        return JSONResponse(
            status_code=500, content={"status": "error", "message": str(e)}
        )


if __name__ == "__main__":
    logger.info("启动OpenGewe回调服务器...")
    uvicorn.run(app, host="0.0.0.0", port=5433)
