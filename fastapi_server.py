"""
FastAPI异步服务器示例
"""

from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.responses import JSONResponse, FileResponse
import os
import shutil
import tomllib
from typing import Optional, Dict, Any
from loguru import logger
import uvicorn
import sys
import asyncio

# 添加当前目录到模块搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from opengewe.client import GeweClient
from opengewe.message.factory import MessageFactory
from opengewe.message.types import MessageType

# 配置loguru
logger.remove()
# 添加文件日志，记录INFO级别以上的消息
logger.add(
    "logs/api_{time:YYYY-MM-DD}.log",
    level="INFO",
    rotation="00:00",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
# 添加DEBUG级别的日志文件，记录所有详细信息
logger.add(
    "logs/debug_{time:YYYY-MM-DD}.log",
    level="DEBUG",
    rotation="00:00",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
# 添加控制台输出
logger.add(lambda msg: print(msg), level="INFO")

# 创建FastAPI应用
app = FastAPI(title="OpenGewe API", description="微信自动化API接口")

# 配置读取函数
async def read_config():
    # 验证main_config.toml配置文件
    if not os.path.exists("main_config.toml"):
        logger.error("main_config.toml配置文件不存在，请检查文件是否存在")
        shutil.copy("main_config_example.toml", "main_config.toml")
        logger.info("已复制main_config_example.toml文件到当前目录，请修改main_config.toml文件后重新启动")
        exit(1)

    # 读取配置
    with open("main_config.toml", "rb") as f:
        return tomllib.load(f)

# 创建GeweClient和MessageFactory的依赖注入
async def get_gewe_client():
    config = await read_config()
    client = GeweClient(
        base_url=config["gewe"]["base_url"],
        download_url=config["gewe"]["download_url"],
        callback_url=config["gewe"]["callback_url"],
        app_id=config["gewe"]["app_id"],
        token=config["gewe"]["token"],
        is_gewe=config["gewe"]["is_gewe"],
        debug=True
    )
    return client

@app.on_event("startup")
async def startup_event():
    try:
        # 使用依赖注入获取factory实例
        client = await get_gewe_client()
        factory = MessageFactory(client)
        
        # 注册回调前先输出factory对象信息
        logger.debug(f"Factory对象初始化状态: client={factory.client is not None}, handlers={len(factory.handlers)}, callback={factory.on_message_callback}")
        
        # 注册回调函数
        factory.register_callback(on_message)
        
        # 将工厂实例保存为应用状态，确保使用同一个实例
        app.state.message_factory = factory
        
        # 注册后再次输出
        logger.debug(f"注册回调后Factory对象状态: callback={factory.on_message_callback.__name__ if factory.on_message_callback else None}")
        logger.info("已注册消息回调函数")
    except Exception as e:
        logger.exception(f"启动事件发生异常: {e}")

# 修改依赖注入获取消息工厂的方式，优先使用已保存的实例
async def get_message_factory(client: GeweClient = Depends(get_gewe_client)):
    # 如果应用状态中已有工厂实例，则使用它
    if hasattr(app.state, "message_factory"):
        return app.state.message_factory
        
    # 否则创建一个新实例
    factory = MessageFactory(client)
    return factory

# 消息回调函数
async def on_message(message):
    try:
        # 获取message对象的所有属性
        attrs = [
            attr
            for attr in dir(message)
            if not attr.startswith("_")
            and attr != "raw_data"
            and attr != "from_dict"
        ]
        
        # 构建属性信息字符串
        attr_info = []
        for attr in attrs:
            try:
                value = getattr(message, attr)
                attr_info.append(f"{attr}={value}")
            except Exception as e:
                attr_info.append(f"{attr}=<获取失败: {str(e)}>")
                
        # 打印所有属性信息
        logger.info(
            f"收到 {'群' if message.is_group_message else '好友'} {message.type.name} 消息: {', '.join(attr_info)}"
        )
        
        # 添加更详细的DEBUG日志
        logger.debug(f"消息详细信息: {message.__dict__}")

        if message.type == MessageType.TEXT:
            client = await get_gewe_client()
            if message.text == "测试":
                logger.info(f"接收到测试消息，准备回复")
                await client.message.post_text(message.from_wxid, "测试成功")
                logger.info(f"已回复测试消息")

            if message.text == "语音":
                result = await client.utils.convert_audio_to_silk(
                    "/root/opengewechat/downloads/test.wav",
                    "/root/opengewechat/downloads",
                )
                logger.info(f"语音转换结果: {result}")
                await client.message.send_voice(
                    message.from_wxid,
                    "http://ip:5432/download/test.silk",
                    result["duration"],
                )
    except Exception as e:
        logger.exception(f"处理消息时发生异常: {e}")

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
                content={"status": "error", "message": "无效的请求数据"}
            )

        # 使用应用状态中保存的工厂实例
        factory = app.state.message_factory
        if not factory:
            logger.error("消息工厂未初始化")
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "消息工厂未初始化"}
            )

        # 异步处理消息，立即返回响应，不阻塞HTTP请求
        logger.info(f"接收到消息: {data}")
        task = factory.process_async(data)
        
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
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/download/{filename:path}")
async def download_file(filename: str, custom_filename: Optional[str] = None):
    """
    文件下载接口
    支持通过URL路径下载：/download/文件名
    """
    # 安全检查：防止路径遍历攻击
    if ".." in filename or filename.startswith("/"):
        raise HTTPException(status_code=403, detail="非法的文件路径")

    download_dir = "./downloads"
    file_path = os.path.join(download_dir, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    # 设置自定义文件名
    return FileResponse(
        path=file_path, 
        filename=custom_filename if custom_filename else filename
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
    return {"status": "running"}

if __name__ == "__main__":
    logger.info("启动Gewe回调服务器...")
    uvicorn.run(app, host="0.0.0.0", port=5432) 