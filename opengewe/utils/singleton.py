class Singleton(type):
    """单例元类

    使用方法:
    class MyClass(metaclass=Singleton):
        pass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def reset_instance(mcs, cls):
        """重置指定类的单例实例"""
        if cls in mcs._instances:
            del mcs._instances[cls]

    @classmethod
    def reset_all(mcs):
        """重置所有单例实例"""
        mcs._instances.clear()
