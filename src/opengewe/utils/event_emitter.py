"""
事件发射器 - 用于消息发送事件的异步通知
"""

import asyncio
from typing import Dict, List, Callable, Any, Optional
from opengewe.logger import get_logger

logger = get_logger(__name__)


class EventEmitter:
    """简单的异步事件发射器"""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._loop: Optional[asyncio.AbstractEventLoop] = None
    
    def on(self, event_name: str, callback: Callable):
        """注册事件监听器"""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)
        logger.debug(f"注册事件监听器: {event_name} -> {callback.__name__}")
    
    def off(self, event_name: str, callback: Callable):
        """移除事件监听器"""
        if event_name in self._listeners:
            try:
                self._listeners[event_name].remove(callback)
                logger.debug(f"移除事件监听器: {event_name} -> {callback.__name__}")
            except ValueError:
                pass
    
    async def emit(self, event_name: str, *args, **kwargs):
        """异步发射事件"""
        if event_name not in self._listeners:
            return
        
        # 为每个监听器创建异步任务
        tasks = []
        for listener in self._listeners[event_name]:
            try:
                if asyncio.iscoroutinefunction(listener):
                    task = asyncio.create_task(listener(*args, **kwargs))
                else:
                    # 如果是同步函数，在事件循环中运行
                    loop = asyncio.get_event_loop()
                    task = loop.run_in_executor(None, listener, *args, **kwargs)
                tasks.append(task)
            except Exception as e:
                logger.error(f"创建事件任务失败: {event_name} -> {listener.__name__}: {e}")
        
        # 等待所有任务完成，但不阻塞主流程
        if tasks:
            # 使用 asyncio.gather 并设置 return_exceptions=True 来避免异常传播
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def emit_nowait(self, event_name: str, *args, **kwargs):
        """非阻塞发射事件（创建任务但不等待）"""
        try:
            loop = asyncio.get_event_loop()
            task = asyncio.create_task(self.emit(event_name, *args, **kwargs))
            # 添加异常处理器避免未处理的异常警告
            task.add_done_callback(self._handle_task_exception)
        except RuntimeError:
            # 如果没有运行的事件循环，记录警告
            logger.warning(f"无法发射事件 {event_name}: 没有运行的事件循环")
    
    def _handle_task_exception(self, task: asyncio.Task):
        """处理任务异常"""
        try:
            task.result()
        except Exception as e:
            logger.error(f"事件处理器异常: {e}", exc_info=True)


# 全局事件发射器实例
message_event_emitter = EventEmitter() 