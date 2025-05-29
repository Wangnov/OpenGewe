import api from './api';

/**
 * 机器人相关API服务
 */
const botService = {
    /**
     * 获取机器人列表
     * @param {number} page - 页码
     * @param {number} pageSize - 每页大小
     * @param {string} search - 搜索关键词
     * @param {boolean} isOnline - 在线状态过滤
     * @returns {Promise} - 机器人列表响应
     */
    getBots: async (page = 1, pageSize = 20, search = null, isOnline = null) => {
        const params = { page, page_size: pageSize };
        if (search) params.search = search;
        if (isOnline !== null) params.is_online = isOnline;

        return api.get('/bots', { params });
    },

    /**
     * 获取机器人详情
     * @param {string} geweAppId - GeWe应用ID
     * @returns {Promise} - 机器人详情响应
     */
    getBotDetails: async (geweAppId) => {
        return api.get(`/bots/${geweAppId}`);
    },

    /**
     * 创建机器人
     * @param {Object} botData - 机器人数据
     * @param {string} botData.gewe_app_id - GeWe应用ID
     * @param {string} botData.gewe_token - GeWe Token
     * @param {string} botData.callback_url_override - 回调URL覆盖（可选）
     * @returns {Promise} - 创建机器人响应
     */
    createBot: async (botData) => {
        return api.post('/bots', botData);
    },

    /**
     * 更新机器人
     * @param {string} geweAppId - GeWe应用ID
     * @param {Object} botData - 机器人数据
     * @returns {Promise} - 更新机器人响应
     */
    updateBot: async (geweAppId, botData) => {
        return api.put(`/bots/${geweAppId}`, botData);
    },

    /**
     * 删除机器人
     * @param {string} geweAppId - GeWe应用ID
     * @returns {Promise} - 删除机器人响应
     */
    deleteBot: async (geweAppId) => {
        return api.delete(`/bots/${geweAppId}`);
    },

    /**
     * 获取机器人状态
     * @param {string} geweAppId - GeWe应用ID
     * @returns {Promise} - 机器人状态响应
     */
    getBotStatus: async (geweAppId) => {
        return api.get(`/bots/${geweAppId}/status`);
    },

    /**
     * 获取机器人联系人
     * @param {string} geweAppId - GeWe应用ID
     * @param {string} contactType - 联系人类型
     * @param {string} search - 搜索关键词
     * @param {number} page - 页码
     * @param {number} pageSize - 每页大小
     * @returns {Promise} - 机器人联系人响应
     */
    getBotContacts: async (geweAppId, contactType = null, search = null, page = 1, pageSize = 20) => {
        const params = { page, page_size: pageSize };
        if (contactType) params.contact_type = contactType;
        if (search) params.search = search;

        return api.get(`/bots/${geweAppId}/contacts`, { params });
    },

    /**
     * 获取机器人插件配置
     * @param {string} geweAppId - GeWe应用ID
     * @returns {Promise} - 机器人插件配置响应
     */
    getBotPlugins: async (geweAppId) => {
        return api.get(`/bots/${geweAppId}/plugins`);
    },

    /**
     * 更新机器人插件配置
     * @param {string} geweAppId - GeWe应用ID
     * @param {string} pluginName - 插件名称
     * @param {boolean} isEnabled - 是否启用
     * @param {Object} configJson - 插件配置
     * @returns {Promise} - 更新机器人插件配置响应
     */
    updateBotPlugin: async (geweAppId, pluginName, isEnabled, configJson = null) => {
        return api.put(`/bots/${geweAppId}/plugins/${pluginName}`, {
            is_enabled: isEnabled,
            config_json: configJson,
        });
    },

    /**
     * 测试机器人连接
     * @param {Object} botData - 机器人连接数据
     * @param {string} botData.gewe_app_id - GeWe应用ID
     * @param {string} botData.gewe_token - GeWe Token
     * @param {string} botData.base_url - 基础URL
     * @returns {Promise} - 测试连接响应
     */
    testBotConnection: async (botData) => {
        return api.post('/bots/test-connection', botData);
    },

    /**
     * 刷新机器人信息
     * @param {string} geweAppId - GeWe应用ID
     * @returns {Promise} - 刷新机器人信息响应
     */
    refreshBotInfo: async (geweAppId) => {
        return api.post(`/bots/${geweAppId}/refresh`);
    },
};

export default botService;