"""事件管理器模块

提供异步事件绑定和触发功能。
"""

import copy
from typing import Callable, Dict, List, Tuple

from opengewe.callback.types import MessageType


class EventManager:
    """事件管理器

    用于管理和触发异步事件。事件处理函数通过MessageType类型进行索引。
    """

    # {MessageType: [(handler, instance, priority)]}
    _handlers: Dict[MessageType, List[Tuple[Callable, object, int]]] = {}

    @classmethod
    def bind_instance(cls, instance: object) -> None:
        """将实例的事件处理方法绑定到事件管理器

        Args:
            instance: 包含事件处理方法的实例
        """
        for method_name in dir(instance):
            method = getattr(instance, method_name)
            if hasattr(method, "_message_type"):
                message_type = getattr(method, "_message_type")
                priority = getattr(method, "_priority", 50)

                if message_type not in cls._handlers:
                    cls._handlers[message_type] = []
                cls._handlers[message_type].append((method, instance, priority))
                # 按优先级排序，优先级高的在前（数字小的优先级高）
                cls._handlers[message_type].sort(key=lambda x: x[2])

    @classmethod
    async def emit(cls, message_type: MessageType, *args, **kwargs) -> None:
        """触发指定类型的事件

        Args:
            message_type: 消息类型
            *args: 传递给事件处理函数的位置参数
            **kwargs: 传递给事件处理函数的关键字参数
        """
        # 首先处理普通的消息类型处理器
        if message_type in cls._handlers:
            # 通常第一个参数是client，第二个参数是message
            if len(args) >= 2:
                client, message = args[0], args[1]
                remaining_args = args[2:]
                
                for handler, instance, priority in cls._handlers[message_type]:
                    # 检查是否为@消息处理器，如果是则跳过（会在下面专门处理）
                    if hasattr(handler, "_is_at_message"):
                        continue
                        
                    # 只对message进行深拷贝，client保持不变
                    handler_args = (client, copy.deepcopy(message)) + tuple(
                        copy.deepcopy(arg) for arg in remaining_args
                    )
                    new_kwargs = {k: copy.deepcopy(v) for k, v in kwargs.items()}
                    
                    result = await handler(*handler_args, **new_kwargs)
                    
                    if isinstance(result, bool) and not result:
                        # 处理函数返回False时，停止后续处理
                        break
            else:
                # 处理参数不足的情况
                for handler, instance, priority in cls._handlers[message_type]:
                    if hasattr(handler, "_is_at_message"):
                        continue
                        
                    handler_args = tuple(copy.deepcopy(arg) for arg in args)
                    new_kwargs = {k: copy.deepcopy(v) for k, v in kwargs.items()}
                    
                    result = await handler(*handler_args, **new_kwargs)
                    
                    if isinstance(result, bool) and not result:
                        break
        
        # 处理@消息
        if message_type == MessageType.TEXT and len(args) >= 2:
            client, message = args[0], args[1]
            remaining_args = args[2:]
            
            # 检查消息是否为@消息
            is_at = getattr(message, "is_at", False)
            
            if is_at and MessageType.TEXT in cls._handlers:
                for handler, instance, priority in cls._handlers[MessageType.TEXT]:
                    # 只处理被标记为@消息处理器的处理器
                    if not hasattr(handler, "_is_at_message"):
                        continue
                        
                    # 只对message进行深拷贝，client保持不变
                    handler_args = (client, copy.deepcopy(message)) + tuple(
                        copy.deepcopy(arg) for arg in remaining_args
                    )
                    new_kwargs = {k: copy.deepcopy(v) for k, v in kwargs.items()}
                    
                    result = await handler(*handler_args, **new_kwargs)
                    
                    if isinstance(result, bool) and not result:
                        # 处理函数返回False时，停止后续处理
                        break

    @classmethod
    def unbind_instance(cls, instance: object) -> None:
        """解绑实例的所有事件处理函数

        Args:
            instance: 要解绑的实例
        """
        for message_type in list(cls._handlers.keys()):
            cls._handlers[message_type] = [
                (handler, inst, priority)
                for handler, inst, priority in cls._handlers[message_type]
                if inst is not instance
            ]
            # 如果没有处理函数了，删除该类型的条目
            if not cls._handlers[message_type]:
                del cls._handlers[message_type]
