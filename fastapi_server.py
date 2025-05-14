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
import subprocess
import signal
import time
from contextlib import asynccontextmanager

# 添加当前目录到模块搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from opengewe.client import GeweClient
from opengewe.callback.factory import MessageFactory
from opengewe.callback.types import MessageType

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

# 全局变量保存worker进程
worker_process = None

def start_celery_worker(config: Dict[str, Any]) -> bool:
    """启动Celery worker子进程
    
    Args:
        config: 包含队列配置的字典
        
    Returns:
        bool: 是否成功启动worker
    """
    global worker_process
    
    # 检查队列类型
    queue_config = config.get("queue", {})
    queue_type = queue_config.get("queue_type", "simple")
    
    # 如果不是高级队列模式，不启动worker
    if queue_type != "advanced":
        logger.info(f"当前队列类型为 {queue_type}，不需要启动Celery worker")
        return False
    
    logger.info("正在启动Celery worker...")
    
    # 从配置中获取队列参数
    broker = queue_config.get("broker", "redis://localhost:6379/0")
    backend = queue_config.get("backend", "redis://localhost:6379/0")
    queue_name = queue_config.get("name", "opengewe_messages")
    concurrency = str(queue_config.get("concurrency", 4))
    
    # 设置环境变量
    env = os.environ.copy()
    env.update({
        "OPENGEWE_BROKER_URL": broker,
        "OPENGEWE_RESULT_BACKEND": backend,
        "OPENGEWE_QUEUE_NAME": queue_name,
        "OPENGEWE_CONCURRENCY": concurrency
    })
    
    # 启动worker进程
    worker_process = subprocess.Popen(
        [sys.executable, "-m", "opengewe.queue.celery_worker"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # 等待worker启动
    logger.info("等待Celery worker启动...")
    for _ in range(10):  # 最多等待10秒
        if worker_process.poll() is not None:
            # worker已退出
            stdout, _ = worker_process.communicate()
            logger.error(f"Celery worker启动失败:\n{stdout}")
            return False
        
        # 检查输出是否包含表示成功启动的消息
        output = worker_process.stdout.readline()
        logger.debug(f"Worker输出: {output.strip()}")
        if "ready" in output.lower() or "working" in output.lower():
            logger.info("Celery worker已成功启动!")
            break
            
        time.sleep(1)
    
    # 创建一个后台任务来收集输出
    asyncio.create_task(collect_worker_output())
    return True


async def collect_worker_output():
    """收集并打印worker的输出"""
    global worker_process
    while worker_process and worker_process.poll() is None:
        line = worker_process.stdout.readline()
        if line:
            logger.debug(f"Worker > {line.strip()}")
        else:
            await asyncio.sleep(0.1)


def stop_celery_worker():
    """停止Celery worker子进程"""
    global worker_process
    if worker_process and worker_process.poll() is None:
        logger.info("正在关闭Celery worker...")
        # 首先尝试使用SIGTERM信号优雅关闭
        worker_process.terminate()
        
        # 等待进程结束
        try:
            worker_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # 如果超时，强制关闭
            logger.warning("Celery worker未响应，强制关闭...")
            worker_process.kill()
            worker_process.wait()
        
        logger.info("Celery worker已关闭")

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
    
    # 从配置中获取高级队列的配置
    queue_config = config.get("queue", {})
    queue_type = queue_config.get("queue_type", "simple")
    broker = queue_config.get("broker", "redis://localhost:6379/0")
    backend = queue_config.get("backend", "redis://localhost:6379/0")
    queue_name = queue_config.get("name", "opengewe_messages")
    
    client = GeweClient(
        base_url=config["gewe"]["base_url"],
        download_url=config["gewe"]["download_url"],
        callback_url=config["gewe"]["callback_url"],
        app_id=config["gewe"]["app_id"],
        token=config["gewe"]["token"],
        is_gewe=config["gewe"]["is_gewe"],
        debug=True,
        # 使用配置的队列类型
        queue_type=queue_type,
        broker=broker,
        backend=backend,
        queue_name=queue_name
    )
    
    return client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    try:
        # 读取配置
        config = await read_config()
        
        # 启动Celery worker（如果是高级队列模式）
        worker_started = start_celery_worker(config)
        app.state.worker_running = worker_started
        app.state.queue_mode = config.get("queue", {}).get("queue_type", "simple")
        
        # 使用依赖注入获取factory实例
        client = await get_gewe_client()
        factory = MessageFactory(client)
        # 注册回调函数
        factory.register_callback(on_message)
        
        # 将工厂实例保存为应用状态，确保使用同一个实例
        app.state.message_factory = factory
        
        logger.info(f"应用初始化完成，队列模式: {app.state.queue_mode}")
    except Exception as e:
        logger.exception(f"启动事件发生异常: {e}")
        # 如果初始化失败，确保关闭worker
        stop_celery_worker()
    
    yield  # 应用运行期间
    
    # 关闭时执行的清理代码
    logger.info("应用正在关闭...")
    stop_celery_worker()

# 创建FastAPI应用
app = FastAPI(
    title="OpenGewe API", 
    description="微信自动化API接口",
    lifespan=lifespan
)

# 注册信号处理函数，确保程序被中断时能优雅退出
def signal_handler(sig, frame):
    logger.info("收到中断信号，开始优雅关闭...")
    # 此处不需要特别处理，因为uvicorn会在收到信号时自动关闭FastAPI应用
    # 而在lifespan的退出逻辑中我们已经处理了worker的关闭

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

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
                await client.send_text_message(message.from_wxid, "测试成功")
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
    return {
        "status": "running", 
        "queue_mode": getattr(app.state, "queue_mode", "unknown"), 
        "worker_running": getattr(app.state, "worker_running", False)
    }

if __name__ == "__main__":
    logger.info("启动Gewe回调服务器...")
    uvicorn.run(app, host="0.0.0.0", port=5432) 