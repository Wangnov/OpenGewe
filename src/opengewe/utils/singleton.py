"""单例模式的实现

提供线程安全的单例模式实现，用于确保特定类在整个应用程序中只有一个实例。
"""

import threading
from typing import Any, Dict, Type, TypeVar, Optional, cast

T = TypeVar("T")


class Singleton(type):
    """线程安全的单例元类

    使用方法:
    ```python
    class MyClass(metaclass=Singleton):
        pass

    # 获取的总是同一个实例
    a = MyClass()
    b = MyClass()
    assert a is b
    ```
    """

    _instances: Dict[Type[Any], Any] = {}
    _lock = threading.RLock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """创建或获取类的单例实例

        首次调用时创建实例，后续调用返回已创建的实例。
        使用线程锁确保在多线程环境下安全。

        Returns:
            实例: 类的唯一实例
        """
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def reset_instance(mcs, cls: Type[T]) -> None:
        """重置指定类的单例实例

        Args:
            cls: 要重置实例的类
        """
        with mcs._lock:
            if cls in mcs._instances:
                del mcs._instances[cls]

    @classmethod
    def reset_all(mcs) -> None:
        """重置所有单例实例

        Args:
            mcs: 单例元类实例
        """
        with mcs._lock:
            mcs._instances.clear()

    @classmethod
    def get_instance(mcs, cls: Type[T]) -> Optional[T]:
        """获取指定类的现有实例，不创建新实例

        Args:
            cls: 要获取实例的类

        Returns:
            Optional[T]: 类的实例，如果不存在则返回None
        """
        with mcs._lock:
            return cast(Optional[T], mcs._instances.get(cls))

    @classmethod
    def has_instance(mcs, cls: Type[Any]) -> bool:
        """检查指定类是否已创建实例

        Args:
            cls: 要检查的类

        Returns:
            bool: 如果类已有实例则为True，否则为False
        """
        with mcs._lock:
            return cls in mcs._instances
