import api from './api';

/**
 * 仪表盘服务
 */
const dashboardService = {
    /**
     * 获取仪表盘统计数据
     * @returns {Promise<Object>} 统计数据
     */
    async getStats() {
        try {
            const response = await api.get('/dashboard/stats');
            return response.data;
        } catch (error) {
            console.error('获取仪表盘统计数据失败:', error);
            throw error;
        }
    },

    /**
     * 获取系统状态信息
     * @returns {Promise<Object>} 系统状态数据
     */
    async getSystemStatus() {
        try {
            const response = await api.get('/dashboard/system-status');
            return response.data;
        } catch (error) {
            console.error('获取系统状态失败:', error);
            // 返回默认值，防止前端报错
            return {
                cpu_usage: 0.0,
                memory_usage: 0.0,
                memory_total: 0,
                memory_used: 0,
                memory_available: 0,
                uptime: 0
            };
        }
    }
};

export default dashboardService; 