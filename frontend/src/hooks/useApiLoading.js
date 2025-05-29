import { useState, useCallback } from 'react';

/**
 * API加载状态管理Hook
 * 确保加载动画最少显示0.5秒
 * @returns {Object} { loading, executeWithLoading }
 */
const useApiLoading = () => {
  const [loading, setLoading] = useState(false);

  const executeWithLoading = useCallback(async (apiFunction, minLoadingTime = 500) => {
    setLoading(true);
    const startTime = Date.now();

    try {
      // 执行API调用
      const result = await apiFunction();
      
      // 计算已经过去的时间
      const elapsedTime = Date.now() - startTime;
      
      // 如果执行时间少于最小加载时间，等待剩余时间
      if (elapsedTime < minLoadingTime) {
        await new Promise(resolve => 
          setTimeout(resolve, minLoadingTime - elapsedTime)
        );
      }
      
      return result;
    } catch (error) {
      // 即使出错也要确保最小加载时间
      const elapsedTime = Date.now() - startTime;
      if (elapsedTime < minLoadingTime) {
        await new Promise(resolve => 
          setTimeout(resolve, minLoadingTime - elapsedTime)
        );
      }
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return { loading, executeWithLoading };
};

export default useApiLoading; 