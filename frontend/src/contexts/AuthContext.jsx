import React, { createContext, useState, useEffect } from 'react';
import authService from '../services/authService';
import useNotification from '../hooks/useNotification';

// 创建认证上下文
export const AuthContext = createContext();

/**
 * 认证上下文提供者组件
 * @param {Object} props - 组件属性
 * @param {React.ReactNode} props.children - 子组件
 */
export const AuthProvider = ({ children }) => {
    // 用户状态
    const [user, setUser] = useState(null);
    // 加载状态
    const [loading, setLoading] = useState(true);
    // 错误状态
    const [error, setError] = useState(null);

    // 通知系统
    const { success, error: notifyError, info } = useNotification();

    // 初始化时检查用户是否已登录
    useEffect(() => {
        const initAuth = async () => {
            try {
                // 检查是否有访问令牌
                if (authService.isAuthenticated()) {
                    // 获取本地存储的用户信息
                    const storedUser = authService.getUser();
                    if (storedUser) {
                        setUser(storedUser);
                    } else {
                        // 如果没有用户信息，尝试从API获取
                        try {
                            const response = await authService.getCurrentUser();
                            setUser(response.data);
                        } catch (err) {
                            console.error('获取用户信息失败', err);
                            // 认证失败，清除令牌
                            await logout();
                        }
                    }
                }
            } catch (err) {
                console.error('初始化认证失败', err);
                setError('初始化认证失败');
            } finally {
                setLoading(false);
            }
        };

        initAuth();
    }, []);

    /**
     * 用户登录
     * @param {string} username - 用户名
     * @param {string} password - 密码
     * @param {boolean} remember - 是否记住登录状态
     * @returns {Promise} - 登录结果
     */
    const login = async (username, password, remember = false) => {
        setLoading(true);
        setError(null);
        try {
            const data = await authService.login(username, password, remember);
            setUser(data.user);

            // 显示登录成功通知
            success('登录成功', `欢迎回来，${data.user?.username || '用户'}！`, {
                duration: 3000,
                actions: [{
                    label: '查看仪表盘',
                    onClick: () => window.location.href = '/dashboard',
                    variant: 'primary'
                }]
            });

            return data;
        } catch (err) {
            console.error('登录失败', err);
            const errorMessage = err.response?.data?.detail || '登录失败，请检查用户名和密码';
            setError(errorMessage);

            // 显示登录失败通知
            notifyError('登录失败', errorMessage, {
                duration: 0, // 错误通知不自动消失
                actions: [{
                    label: '重试',
                    onClick: () => window.location.reload(),
                    variant: 'primary'
                }]
            });

            throw err;
        } finally {
            setLoading(false);
        }
    };

    /**
     * 用户登出
     * @returns {Promise} - 登出结果
     */
    const logout = async () => {
        setLoading(true);
        try {
            await authService.logout();
            setUser(null);

            // 显示登出成功通知
            info('已退出登录', '您已安全退出系统，感谢使用！', {
                duration: 2000
            });

        } catch (err) {
            console.error('登出失败', err);
            setError('登出失败');

            // 显示登出失败通知
            notifyError('登出失败', '登出过程中出现错误，请刷新页面重试', {
                duration: 5000
            });
        } finally {
            setLoading(false);
        }
    };

    /**
     * 修改密码
     * @param {string} oldPassword - 原密码
     * @param {string} newPassword - 新密码
     * @param {string} confirmPassword - 确认新密码
     * @returns {Promise} - 修改密码结果
     */
    const changePassword = async (oldPassword, newPassword, confirmPassword) => {
        setLoading(true);
        setError(null);
        try {
            const result = await authService.changePassword(
                oldPassword,
                newPassword,
                confirmPassword
            );

            // 显示修改密码成功通知
            success('密码修改成功', '您的密码已成功更新，请妥善保管新密码', {
                duration: 5000,
                actions: [{
                    label: '重新登录',
                    onClick: () => logout(),
                    variant: 'primary'
                }]
            });

            return result;
        } catch (err) {
            console.error('修改密码失败', err);
            const errorMessage = err.response?.data?.detail || '修改密码失败';
            setError(errorMessage);

            // 显示修改密码失败通知
            notifyError('密码修改失败', errorMessage, {
                duration: 0,
                actions: [{
                    label: '重试',
                    onClick: () => window.location.reload(),
                    variant: 'primary'
                }]
            });

            throw err;
        } finally {
            setLoading(false);
        }
    };

    // 上下文值
    const value = {
        user,
        loading,
        error,
        login,
        logout,
        changePassword,
        isAuthenticated: !!user,
        isSuperAdmin: user?.is_superadmin || false,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 