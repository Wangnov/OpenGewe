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
    }
};

export default dashboardService; 