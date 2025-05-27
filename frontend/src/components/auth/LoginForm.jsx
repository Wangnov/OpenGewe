import React, { useState } from 'react';
import useAuth from '../../hooks/useAuth';

/**
 * 登录表单组件
 * @returns {JSX.Element} 登录表单
 */
const LoginForm = () => {
    // 表单状态
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [remember, setRemember] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [formError, setFormError] = useState('');

    // 使用认证钩子
    const { login, error: authError } = useAuth();

    /**
     * 处理表单提交
     * @param {React.FormEvent} e - 表单事件
     */
    const handleSubmit = async (e) => {
        e.preventDefault();

        // 表单验证
        if (!username.trim()) {
            setFormError('请输入用户名');
            return;
        }

        if (!password) {
            setFormError('请输入密码');
            return;
        }

        setFormError('');
        setIsSubmitting(true);

        try {
            // 调用登录
            await login(username, password, remember);
            // 登录成功后会自动重定向
        } catch (error) {
            // 错误已在useAuth中处理
            console.error('登录失败', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="w-full max-w-md">
            <div className="mb-8">
                <h1 className="hero-text mb-2">OpenGewe</h1>
                <p className="text-xl text-gray-600">微信机器人管理后台</p>
            </div>

            {/* 错误提示 */}
            {(formError || authError) && (
                <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
                    {formError || authError}
                </div>
            )}

            {/* 用户名输入 */}
            <div className="mb-6">
                <label htmlFor="username" className="block text-gray-700 text-sm font-medium mb-2">
                    用户名
                </label>
                <input
                    id="username"
                    type="text"
                    className="input"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    disabled={isSubmitting}
                    placeholder="请输入用户名"
                    autoComplete="username"
                />
            </div>

            {/* 密码输入 */}
            <div className="mb-6">
                <label htmlFor="password" className="block text-gray-700 text-sm font-medium mb-2">
                    密码
                </label>
                <input
                    id="password"
                    type="password"
                    className="input"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={isSubmitting}
                    placeholder="请输入密码"
                    autoComplete="current-password"
                />
            </div>

            {/* 记住登录 */}
            <div className="flex items-center mb-6">
                <input
                    id="remember"
                    type="checkbox"
                    className="h-4 w-4 text-primary border-gray-300 rounded"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                    disabled={isSubmitting}
                />
                <label htmlFor="remember" className="ml-2 block text-gray-700 text-sm">
                    记住登录状态
                </label>
            </div>

            {/* 提交按钮 */}
            <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={isSubmitting}
            >
                {isSubmitting ? (
                    <>
                        <i className="fas fa-circle-notch fa-spin"></i>
                        <span>登录中...</span>
                    </>
                ) : (
                    <>
                        <i className="fas fa-sign-in-alt"></i>
                        <span>登录</span>
                    </>
                )}
            </button>
        </form>
    );
};

export default LoginForm; 