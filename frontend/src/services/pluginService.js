import api from './api';

/**
 * 插件管理相关的API服务
 */
const pluginService = {
    /**
     * 获取所有全局插件的信息
     * @returns {Promise} - 包含所有插件信息的响应
     */
    getGlobalPlugins: async () => {
        return api.get('/admin/plugins');
    },

    /**
     * 更新插件的全局启用状态
     * @param {string} pluginId - 插件的唯一标识符
     * @param {boolean} isEnabled - 是否全局启用
     * @returns {Promise} - 更新操作的响应
     */
    updateGlobalPluginStatus: async (pluginId, isEnabled) => {
        return api.put(`/admin/plugins/${pluginId}`, { is_globally_enabled: isEnabled });
    },

    /**
     * 获取指定机器人合并后的插件配置
     * @param {string} botId - 机器人的gewe_app_id
     * @param {string} pluginId - 插件的唯一标识符
     * @returns {Promise} - 包含合并后配置的响应
     */
    getBotPluginConfig: async (botId, pluginId) => {
        return api.get(`/bots/${botId}/plugins/${pluginId}`);
    },

    /**
     * 更新指定机器人的插件配置
     * @param {string} botId - 机器人的gewe_app_id
     * @param {string} pluginId - 插件的唯一标识符
     * @param {Object} configData - 包含 is_enabled 和 config_json 的对象
     * @returns {Promise} - 更新操作的响应
     */
    updateBotPluginConfig: async (botId, pluginId, configData) => {
        return api.put(`/bots/${botId}/plugins/${pluginId}`, configData);
    },

    /**
     * 触发后端热重载所有插件配置
     * @returns {Promise} - 热重载操作的响应
     */
    reloadPluginConfig: async () => {
        return api.post('/admin/plugins/reload');
    },

    /**
     * 更新插件的全局配置
     * @param {string} pluginId - 插件的唯一标识符
     * @param {Object} config - 新的配置对象
     * @returns {Promise} - 更新操作的响应
     */
    updateGlobalPluginConfig: async (pluginId, config) => {
        return api.put(`/admin/plugins/${pluginId}/config`, config);
    },
};

export default pluginService;