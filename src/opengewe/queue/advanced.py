import asyncio
import os
import base64
import tempfile
from asyncio import Future
from typing import Any, Awaitable, Callable, Dict, Optional

from celery import Celery
from celery.result import AsyncResult
from loguru import logger
import joblib

from .base import BaseMessageQueue, QueueError, WorkerNotFoundError

# 默认配置，可通过环境变量覆盖
DEFAULT_BROKER = "redis://localhost:6379/0"
DEFAULT_BACKEND = "redis://localhost:6379/0"
DEFAULT_QUEUE_NAME = "opengewe_messages"


# 创建Celery应用工厂函数
def create_celery_app(
    broker: Optional[str] = None,
    backend: Optional[str] = None,
    queue_name: Optional[str] = None,
) -> Celery:
    """创建Celery应用实例

    Args:
        broker: 消息代理的URI，例如 'redis://localhost:6379/0' 或 'amqp://guest:guest@localhost:5672//'
        backend: 结果存储的URI，例如 'redis://localhost:6379/0'
        queue_name: 队列名称

    Returns:
        Celery: Celery应用实例
    """
    # 从环境变量或参数中获取配置
    broker = broker or os.environ.get("OPENGEWE_BROKER_URL", DEFAULT_BROKER)
    backend = backend or os.environ.get("OPENGEWE_RESULT_BACKEND", DEFAULT_BACKEND)
    queue_name = queue_name or os.environ.get("OPENGEWE_QUEUE_NAME", DEFAULT_QUEUE_NAME)

    # 创建Celery应用
    app = Celery(
        "opengewe_message_queue",
        broker=broker,
        backend=backend,
    )

    # 配置Celery
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="Asia/Shanghai",
        enable_utc=True,
        task_routes={"opengewe.queue.advanced.process_message": {"queue": queue_name}},
        # 添加更多Celery配置
        worker_prefetch_multiplier=1,
        task_acks_late=True,
        task_reject_on_worker_lost=True,
    )

    return app


# 创建模块级别的Celery实例
celery = create_celery_app()


# 定义处理消息的Celery任务
@celery.task(name="opengewe.queue.advanced.process_message", bind=True)
def process_message(
    self,
    task_id: str,
    serialized_func_data: str,
    func_args: list,
    func_kwargs: dict,
) -> Any:
    """处理消息的Celery任务

    Args:
        self: Celery任务实例（bind=True时自动传入）
        task_id: 任务ID
        serialized_func_data: 使用joblib序列化的函数数据
        func_args: 函数的位置参数
        func_kwargs: 函数的关键字参数

    Returns:
        Any: 函数执行的结果
    """
    try:
        logger.info(f"开始处理消息任务: {task_id}")

        # 使用joblib反序列化函数
        try:
            func_bytes = base64.b64decode(serialized_func_data)

            # 创建临时文件来存储序列化数据
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(func_bytes)
                temp_file_path = temp_file.name

            try:
                # 使用joblib加载函数
                func = joblib.load(temp_file_path)
            finally:
                # 清理临时文件
                os.unlink(temp_file_path)

        except Exception as e:
            raise ValueError(f"无法反序列化函数: {str(e)}")

        # 检查函数是否为异步函数
        if asyncio.iscoroutinefunction(func):
            # 异步函数使用asyncio.run执行
            result = asyncio.run(func(*func_args, **func_kwargs))
        else:
            # 同步函数直接调用
            result = func(*func_args, **func_kwargs)

        logger.info(f"任务 {task_id} 执行成功")
        return {"status": "success", "data": result}

    except Exception as e:
        logger.error(f"消息处理异常: {str(e)}")
        # 记录更详细的错误信息
        import traceback

        logger.error(f"错误堆栈: {traceback.format_exc()}")
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}


class AdvancedMessageQueue(BaseMessageQueue):
    """基于Celery的高级消息队列实现"""

    def __init__(
        self,
        broker: str = DEFAULT_BROKER,
        backend: str = DEFAULT_BACKEND,
        queue_name: str = DEFAULT_QUEUE_NAME,
        celery_app: Optional[Celery] = None,
    ):
        """初始化高级消息队列

        Args:
            broker: 消息代理的URI，例如 'redis://localhost:6379/0' 或 'amqp://guest:guest@localhost:5672//'
            backend: 结果存储的URI，例如 'redis://localhost:6379/0'
            queue_name: 队列名称
            celery_app: 可选的Celery应用实例，如果提供则使用该实例，否则使用默认实例
        """
        self._futures: Dict[str, Future] = {}
        self._queue_name = queue_name
        self._processed_messages = 0
        self._is_processing = False

        # 使用提供的Celery实例或模块级别的实例
        if celery_app:
            self.celery = celery_app
        else:
            # 如果broker或backend与默认值不同，创建新的Celery实例
            if (
                broker != DEFAULT_BROKER
                or backend != DEFAULT_BACKEND
                or queue_name != DEFAULT_QUEUE_NAME
            ):
                self.celery = create_celery_app(broker, backend, queue_name)
            else:
                self.celery = celery

    def _serialize_function(self, func: Callable) -> str:
        """序列化函数为base64字符串

        Args:
            func: 要序列化的函数

        Returns:
            str: base64编码的序列化函数数据
        """
        try:
            # 创建临时文件来存储序列化数据
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file_path = temp_file.name

            try:
                # 使用joblib序列化函数，使用默认压缩提高性能
                joblib.dump(func, temp_file_path, compress="lz4")

                # 读取序列化数据并编码为base64
                with open(temp_file_path, "rb") as f:
                    func_bytes = f.read()

                return base64.b64encode(func_bytes).decode("utf-8")

            finally:
                # 清理临时文件
                os.unlink(temp_file_path)

        except Exception as e:
            raise ValueError(f"无法序列化函数 {func.__name__}: {str(e)}")

    async def _check_workers_available(self, timeout: float = 1.0) -> tuple[bool, int]:
        """检查是否有可用的Celery worker

        Args:
            timeout: 检测超时时间，默认1秒

        Returns:
            tuple[bool, int]: (是否有可用worker, worker数量)
        """
        try:
            # 使用ping检测worker
            ping_result = self.celery.control.ping(timeout=timeout)
            if ping_result:
                worker_count = len(ping_result)
                logger.debug(f"检测到 {worker_count} 个活跃的Celery worker")
                return True, worker_count
            else:
                logger.warning("未检测到活跃的Celery worker")
                return False, 0
        except Exception as e:
            logger.error(f"检测Celery worker失败: {e}")
            return False, 0

    @property
    def is_processing(self) -> bool:
        """返回当前是否正在处理消息

        Returns:
            bool: 如果处理器正在运行则返回True，否则返回False
        """
        return self._is_processing or len(self._futures) > 0

    async def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态信息

        Returns:
            Dict[str, Any]: 包含队列当前状态的字典
        """
        try:
            # 获取Celery inspect对象
            inspect_obj = self.celery.control.inspect()

            # 获取活跃任务
            active_tasks = inspect_obj.active() or {}

            # 获取预约任务
            scheduled_tasks = inspect_obj.scheduled() or {}

            # 获取保留任务
            reserved_tasks = inspect_obj.reserved() or {}

            # 计算总任务数
            total_active = sum(len(tasks) for tasks in active_tasks.values())
            total_scheduled = sum(len(tasks) for tasks in scheduled_tasks.values())
            total_reserved = sum(len(tasks) for tasks in reserved_tasks.values())

            # 获取worker状态
            worker_stats = inspect_obj.stats() or {}
            worker_count = len(worker_stats)

            return {
                "queue_size": total_scheduled + total_reserved,
                "processing": self.is_processing,
                "worker_count": worker_count,
                "processed_messages": self._processed_messages,
                "active_tasks": total_active,
                "scheduled_tasks": total_scheduled,
                "reserved_tasks": total_reserved,
                "pending_futures": len(self._futures),
                "queue_name": self._queue_name,
                "workers": list(worker_stats.keys()),
            }
        except Exception as e:
            logger.warning(f"获取队列状态失败: {e}")
            return {
                "queue_size": 0,
                "processing": self.is_processing,
                "worker_count": 0,
                "processed_messages": self._processed_messages,
                "active_tasks": 0,
                "scheduled_tasks": 0,
                "reserved_tasks": 0,
                "pending_futures": len(self._futures),
                "queue_name": self._queue_name,
                "workers": [],
                "error": str(e),
            }

    async def clear_queue(self) -> int:
        """清空当前队列中的所有待处理消息

        Returns:
            int: 被清除的消息数量

        Raises:
            QueueError: 清空队列失败时
        """
        try:
            # 获取Celery inspect对象
            inspect_obj = self.celery.control.inspect()

            # 获取预约和保留的任务
            scheduled_tasks = inspect_obj.scheduled() or {}
            reserved_tasks = inspect_obj.reserved() or {}

            # 计算待清除的任务数
            scheduled_count = sum(len(tasks) for tasks in scheduled_tasks.values())
            reserved_count = sum(len(tasks) for tasks in reserved_tasks.values())
            total_count = scheduled_count + reserved_count

            # 清空队列
            self.celery.control.purge()

            # 取消所有待处理的Future
            cancelled_futures = 0
            for future in list(self._futures.values()):
                if not future.done():
                    future.cancel()
                    cancelled_futures += 1

            # 清空Future字典
            self._futures.clear()

            logger.info(
                f"已清空队列，删除 {total_count} 个排队任务，取消 {cancelled_futures} 个Future"
            )
            return total_count + cancelled_futures

        except Exception as e:
            error_msg = f"清空队列失败: {str(e)}"
            logger.error(error_msg)
            raise QueueError(error_msg) from e

    async def enqueue(
        self, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any
    ) -> Any:
        """将消息添加到队列

        Args:
            func: 要执行的异步函数
            *args: 函数的位置参数
            **kwargs: 函数的关键字参数

        Returns:
            Any: 函数执行的结果
        """
        # 检查worker可用性
        workers_available, worker_count = await self._check_workers_available()
        if not workers_available:
            error_msg = (
                "没有检测到活跃的Celery worker！\n"
                "请启动Celery worker：\n"
                f"  celery -A opengewe.queue.advanced worker --loglevel=info\n"
                "\n"
                "或者检查worker状态：\n"
                f"  celery -A opengewe.queue.advanced inspect ping\n"
                "\n"
                "确保Redis服务正在运行：\n"
                f"  {self.celery.conf.broker_url}\n"
                "\n"
                "如果您想使用简单队列，请将queue_type设置为'simple'"
            )
            raise WorkerNotFoundError(error_msg)

        logger.debug(f"检测到 {worker_count} 个可用worker，提交任务: {func.__name__}")

        # 序列化函数
        try:
            serialized_func_data = self._serialize_function(func)
        except Exception as e:
            raise QueueError(f"序列化函数失败: {str(e)}") from e

        # 创建一个Future对象用于异步等待结果
        future = Future()

        # 生成唯一的任务ID
        task_id = f"{func.__name__}_{id(future)}"

        # 存储Future以便后续设置结果
        self._futures[task_id] = future

        try:
            # 提交任务到Celery
            async_result = process_message.apply_async(
                args=(task_id, serialized_func_data, list(args), kwargs),
                task_id=task_id,
                queue=self._queue_name,  # 明确指定队列
            )

            # 创建一个监听任务结果的异步任务
            asyncio.create_task(self._wait_for_result(task_id, async_result))

            # 标记开始处理
            self._is_processing = True

            # 返回Future，等待结果
            return await future

        except Exception as e:
            # 清理Future
            self._futures.pop(task_id, None)
            raise QueueError(f"提交任务到队列失败: {str(e)}") from e

    async def _wait_for_result(
        self, task_id: str, async_result: AsyncResult, timeout: float = 30.0
    ) -> None:
        """等待Celery任务结果并设置到Future

        Args:
            task_id: 任务ID
            async_result: Celery的AsyncResult对象
            timeout: 等待超时时间，默认30秒
        """
        try:
            # 使用超时机制等待任务完成
            await asyncio.wait_for(
                self._wait_for_task_completion(async_result), timeout=timeout
            )

            # 获取任务结果
            result = async_result.result

            # 获取对应的Future
            future = self._futures.get(task_id)
            if future and not future.done():
                if isinstance(result, dict) and result.get("status") == "error":
                    # 如果任务失败，设置异常
                    error_msg = result.get("error", "Unknown error")
                    future.set_exception(Exception(error_msg))
                else:
                    # 设置结果
                    if isinstance(result, dict) and "data" in result:
                        future.set_result(result["data"])
                    else:
                        future.set_result(result)

                # 增加处理计数
                self._processed_messages += 1

        except asyncio.TimeoutError:
            # 处理超时情况
            logger.error(f"任务 {task_id} 等待超时({timeout}秒)")

            # 获取对应的Future并设置超时异常
            future = self._futures.get(task_id)
            if future and not future.done():
                timeout_msg = (
                    f"任务等待超时({timeout}秒)！可能原因：\n"
                    "1. Celery worker处理任务太慢\n"
                    "2. Worker突然停止工作\n"
                    "3. 网络连接问题\n"
                    "\n"
                    "请检查worker状态：\n"
                    f"  celery -A opengewe.queue.advanced inspect active\n"
                    f"  celery -A opengewe.queue.advanced inspect ping\n"
                    "\n"
                    f"任务ID: {task_id}"
                )
                future.set_exception(QueueError(timeout_msg))

        except Exception as e:
            logger.error(f"等待任务结果异常: {str(e)}")
            # 设置异常到Future
            future = self._futures.get(task_id)
            if future and not future.done():
                future.set_exception(e)
        finally:
            # 移除Future
            self._futures.pop(task_id, None)

            # 如果没有待处理的Future，更新处理状态
            if not self._futures:
                self._is_processing = False

    async def _wait_for_task_completion(self, async_result: AsyncResult) -> None:
        """等待任务完成的内部方法

        Args:
            async_result: Celery的AsyncResult对象
        """
        # 使用非阻塞方式等待任务完成
        while not async_result.ready():
            await asyncio.sleep(0.1)  # 短暂休眠，避免CPU占用过高

    async def start_processing(self) -> None:
        """开始处理队列中的消息

        注意：在使用Celery的情况下，消息处理是由Celery worker负责的
        此方法仅用于保持接口一致性
        """
        logger.info("Celery消息队列不需要手动启动处理，请确保Celery worker已运行")
        logger.info(f"队列名称: {self._queue_name}")

        # 检查worker状态
        try:
            inspect_obj = self.celery.control.inspect()
            worker_stats = inspect_obj.stats() or {}
            if worker_stats:
                logger.info(
                    f"发现 {len(worker_stats)} 个活跃的Celery worker: {list(worker_stats.keys())}"
                )
            else:
                logger.warning(
                    "未发现活跃的Celery worker，请启动worker: celery -A opengewe.queue.advanced worker --loglevel=info"
                )
        except Exception as e:
            logger.warning(f"无法检查Celery worker状态: {e}")

    async def stop_processing(self) -> None:
        """停止处理队列中的消息

        注意：在使用Celery的情况下，消息处理是由Celery worker负责的
        此方法仅用于保持接口一致性
        """
        logger.info("Celery消息队列不需要手动停止处理")

        # 取消所有待处理的Future
        cancelled_count = 0
        for future in list(self._futures.values()):
            if not future.done():
                future.cancel()
                cancelled_count += 1

        if cancelled_count > 0:
            logger.info(f"已取消 {cancelled_count} 个待处理的Future")

        # 清空Future字典
        self._futures.clear()
        self._is_processing = False
