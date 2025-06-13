import axios from 'axios';

// API基础URL，使用环境变量或默认值
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

// 创建axios实例
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 请求拦截器 - 添加认证令牌
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器 - 处理错误和令牌刷新
api.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        // 如果是401错误且未尝试过刷新令牌
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // 尝试使用刷新令牌获取新的访问令牌
                const refreshToken = localStorage.getItem('refresh_token');
                if (!refreshToken) {
                    // 如果没有刷新令牌，清除认证状态并跳转到登录页
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    localStorage.removeItem('user');
                    window.location.href = '/login';
                    return Promise.reject(error);
                }

                // 调用刷新令牌API
                const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
                    refresh_token: refreshToken
                });

                // 保存新的令牌
                const { access_token, refresh_token } = response.data;
                localStorage.setItem('access_token', access_token);
                localStorage.setItem('refresh_token', refresh_token);

                // 使用新令牌重试原始请求
                originalRequest.headers.Authorization = `Bearer ${access_token}`;
                return axios(originalRequest);
            } catch (refreshError) {
                // 刷新令牌失败，清除认证状态并跳转到登录页
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api; 