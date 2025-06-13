import React, { useState, useEffect, useCallback, createContext } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../services/authService';
import useNotification from '../hooks/useNotification';

// 创建认证上下文
// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext(null);

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
    const navigate = useNavigate();

    // 通知系统
    const { success, error: notifyError, info } = useNotification();

    /**
     * 用户登出
     * @returns {Promise} - 登出结果
     */
    const logout = useCallback(async () => {
        setLoading(true);
        try {
            await authService.logout();
            // 仅在成功时显示成功通知
            info('已退出登录', '您已安全退出系统，感谢使用！', {
                duration: 2000
            });
        } catch (err) {
            console.error('登出失败', err);
            setError('登出失败');
            notifyError('登出失败', '登出过程中出现错误，请刷新页面重试', {
                duration: 5000
            });
        } finally {
            // 无论成功与否，都清除本地认证信息
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            setUser(null);
            setLoading(false);
        }
    }, [info, notifyError]);

    // 登出并重定向
    const logoutAndRedirect = useCallback(async () => {
        await logout();
        navigate('/login');
    }, [logout, navigate]);

    // 初始化和事件监听
    useEffect(() => {
        const initAuth = async () => {
            try {
                if (authService.isAuthenticated()) {
                    const storedUser = authService.getUser();
                    if (storedUser) {
                        setUser(storedUser);
                    } else {
                        try {
                            const response = await authService.getCurrentUser();
                            setUser(response.data);
                        } catch (err) {
                            console.error('获取用户信息失败', err);
                            await logoutAndRedirect();
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

        // 监听认证错误事件
        window.addEventListener('auth-error', logoutAndRedirect);

        // 清理事件监听器
        return () => {
            window.removeEventListener('auth-error', logoutAndRedirect);
        };
    }, [logoutAndRedirect]);

    /**
     * 用户登录
     * @param {string} username - 用户名
     * @param {string} password - 密码
     * @param {boolean} remember - 是否记住登录状态
     * @returns {Promise} - 登录结果
     */
    const login = useCallback(async (username, password, remember = false) => {
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
                duration: 5000,
            });

            throw err;
        } finally {
            setLoading(false);
        }
    }, [success, notifyError]);


    /**
     * 修改密码
     * @param {string} oldPassword - 原密码
     * @param {string} newPassword - 新密码
     * @param {string} confirmPassword - 确认新密码
     * @returns {Promise} - 修改密码结果
     */
    const changePassword = useCallback(async (oldPassword, newPassword, confirmPassword) => {
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
    }, [success, notifyError, logout]);

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