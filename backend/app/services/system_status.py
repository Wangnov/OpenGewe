"""
系统状态服务
"""

import time
import psutil
from typing import Dict, Optional
from opengewe.logger import get_logger

logger = get_logger(__name__)


class SystemStatusService:
    """系统状态服务，提供系统资源信息获取和缓存"""
    
    _instance: Optional['SystemStatusService'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._cache: Dict = {}
            self._cache_timeout = 60  # 秒
            self._initialized = True
    
    async def get_system_status(self) -> Dict:
        """
        获取系统状态信息
        
        Returns:
            dict: 包含CPU、内存等系统资源信息
        """
        try:
            # 检查缓存是否有效
            if self._is_cache_valid():
                logger.debug("使用缓存的系统状态数据")
                return self._cache['data']
            
            # 获取新的系统状态数据
            logger.debug("获取新的系统状态数据")
            
            cpu_usage = self._get_cpu_usage()
            memory_info = self._get_memory_info()
            uptime = self._get_system_uptime()
            
            system_status = {
                "cpu_usage": round(cpu_usage, 1),
                "memory_usage": round(memory_info['usage_percent'], 1),
                "memory_total": memory_info['total_mb'],
                "memory_used": memory_info['used_mb'],
                "memory_available": memory_info['available_mb'],
                "uptime": uptime
            }
            
            # 更新缓存
            self._cache = {
                'data': system_status,
                'timestamp': time.time()
            }
            
            return system_status
            
        except Exception as e:
            logger.error(f"获取系统状态失败: {e}", exc_info=True)
            # 返回默认值，防止前端报错
            return {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "memory_total": 0,
                "memory_used": 0,
                "memory_available": 0,
                "uptime": 0
            }
    
    def _get_cpu_usage(self) -> float:
        """获取CPU使用率"""
        # 获取1秒内的平均CPU使用率
        return psutil.cpu_percent(interval=1)
    
    def _get_memory_info(self) -> Dict:
        """获取内存信息"""
        memory = psutil.virtual_memory()
        
        return {
            'total_mb': round(memory.total / (1024 * 1024)),
            'used_mb': round(memory.used / (1024 * 1024)),
            'available_mb': round(memory.available / (1024 * 1024)),
            'usage_percent': memory.percent
        }
    
    def _get_system_uptime(self) -> int:
        """获取系统运行时间（秒）"""
        boot_time = psutil.boot_time()
        current_time = time.time()
        return int(current_time - boot_time)
    
    def _is_cache_valid(self) -> bool:
        """检查缓存是否有效"""
        if not self._cache or 'timestamp' not in self._cache:
            return False
        
        return time.time() - self._cache['timestamp'] < self._cache_timeout


# 创建全局实例
system_status_service = SystemStatusService() 