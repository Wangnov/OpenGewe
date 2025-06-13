import api from './api';

/**
 * 认证相关API服务
 */
const authService = {
    /**
     * 用户登录
     * @param {string} username - 用户名
     * @param {string} password - 密码
     * @param {boolean} remember - 是否记住登录状态
     * @returns {Promise} - 登录响应
     */
    login: async (username, password, remember = false) => {
        console.log('尝试登录:', { username, remember });
        try {
            const response = await api.post('/auth/login', {
                username,
                password,
                remember,
            });

            console.log('登录响应:', response.data);

            // 保存认证信息到本地存储
            const { access_token, refresh_token, user } = response.data;
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);
            localStorage.setItem('user', JSON.stringify(user));

            return response.data;
        } catch (error) {
            console.error('登录错误详情:', error.response || error);
            throw error;
        }
    },

    /**
     * 用户登出
     * @returns {Promise} - 登出响应
     */
    logout: async () => {
        try {
            // 只调用登出API，不清除本地存储
            await api.post('/auth/logout');
        } catch (error) {
            // 即使失败也继续，让上层处理
            console.error('登出API调用失败', error);
        }
    },

    /**
     * 刷新访问令牌
     * @param {string} refreshToken - 刷新令牌
     * @returns {Promise} - 刷新令牌响应
     */
    refreshToken: async (refreshToken) => {
        const response = await api.post('/auth/refresh', {
            refresh_token: refreshToken,
        });

        // 保存新的令牌
        const { access_token, refresh_token } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);

        return response.data;
    },

    /**
     * 获取当前用户信息
     * @returns {Promise} - 用户信息响应
     */
    getCurrentUser: async () => {
        return api.get('/auth/me');
    },

    /**
     * 修改密码
     * @param {string} oldPassword - 原密码
     * @param {string} newPassword - 新密码
     * @param {string} confirmPassword - 确认新密码
     * @returns {Promise} - 修改密码响应
     */
    changePassword: async (oldPassword, newPassword, confirmPassword) => {
        return api.post('/auth/change-password', {
            old_password: oldPassword,
            new_password: newPassword,
            confirm_password: confirmPassword,
        });
    },

    /**
     * 检查用户是否已登录
     * @returns {boolean} - 是否已登录
     */
    isAuthenticated: () => {
        return !!localStorage.getItem('access_token');
    },

    /**
     * 获取本地存储的用户信息
     * @returns {Object|null} - 用户信息
     */
    getUser: () => {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                return JSON.parse(userStr);
            } catch (error) {
                console.error('解析用户信息失败', error);
                return null;
            }
        }
        return null;
    },
};

export default authService; 