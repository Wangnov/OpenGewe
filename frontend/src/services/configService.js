import api from './api';

/**
 * 系统配置相关的API服务
 */
const configService = {
    /**
     * 获取所有可管理的配置段
     * @returns {Promise} - 包含所有配置段数据的响应
     */
    getAllConfigs: async () => {
        return api.get('/admin/config');
    },

    /**
     * 获取指定的配置段
     * @param {string} sectionName - 配置段名称
     * @returns {Promise} - 指定配置段的数据响应
     */
    getConfigSection: async (sectionName) => {
        return api.get(`/admin/config/${sectionName}`);
    },

    /**
     * 更新指定的配置段
     * @param {string} sectionName - 配置段名称
     * @param {Object} configData - 新的配置数据
     * @returns {Promise} - 更新操作的响应
     */
    updateConfigSection: async (sectionName, configData) => {
        return api.put(`/admin/config/${sectionName}`, { config: configData });
    },
};

export default configService;