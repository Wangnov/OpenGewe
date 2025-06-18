import React, { useState } from 'react';
import useAuth from '../../hooks/useAuth';
import useNotification from '../../hooks/useNotification';

/**
 * 登录表单组件
 * @returns {JSX.Element} 登录表单
 */
const LoginForm = () => {
    // 表单状态
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [remember, setRemember] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [formError, setFormError] = useState('');
    const [focusedField, setFocusedField] = useState('');

    // 使用认证钩子
    const { login, error: authError } = useAuth();
    // 使用通知钩子
    const { info, warning } = useNotification();

    /**
     * 处理表单提交
     * @param {React.FormEvent} e - 表单事件
     */
    const handleSubmit = async (e) => {
        e.preventDefault();

        // 表单验证
        if (!username.trim()) {
            setFormError('请输入用户名');
            warning('输入验证', '请输入用户名后继续', { duration: 3000 });
            return;
        }

        if (!password) {
            setFormError('请输入密码');
            warning('输入验证', '请输入密码后继续', { duration: 3000 });
            return;
        }

        setFormError('');
        setIsSubmitting(true);

        // 显示登录处理中的信息
        info('登录中', '正在验证您的身份...', { duration: 2000 });

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

    /**
     * 处理输入变化，清除错误
     */
    const handleInputChange = (setter) => (e) => {
        setter(e.target.value);
        if (formError) {
            setFormError('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="w-full">
            <div className="mb-8 text-center">
                <h2 className="text-2xl font-bold text-gray-800 mb-2">欢迎回来</h2>
                <p className="text-gray-600">请登录您的账户</p>
            </div>

            {/* 错误提示 */}
            {(formError || authError) && (
                <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-xl border border-red-200 flex items-center">
                    <i className="fas fa-exclamation-circle mr-3"></i>
                    <span className="text-sm">{formError || authError}</span>
                </div>
            )}

            {/* 用户名输入 */}
            <div className="mb-6 relative">
                <label
                    htmlFor="username"
                    className={`absolute left-4 transition-all duration-200 pointer-events-none z-10 ${focusedField === 'username' || username
                        ? 'top-2 text-xs text-blue-600'
                        : 'top-4 text-gray-500'
                        }`}
                >
                    用户名
                </label>
                <div className="relative">
                    <input
                        id="username"
                        type="text"
                        className={`w-full px-4 pt-6 pb-2 bg-white border-2 rounded-xl transition-all duration-200 focus:outline-none ${focusedField === 'username'
                            ? 'border-blue-500 shadow-lg shadow-blue-100/50'
                            : 'border-gray-200 hover:border-gray-300'
                            }`}
                        value={username}
                        onChange={handleInputChange(setUsername)}
                        onFocus={() => setFocusedField('username')}
                        onBlur={() => setFocusedField('')}
                        disabled={isSubmitting}
                        autoComplete="username"
                    />
                    <div className={`absolute right-4 top-1/2 -translate-y-1/2 transition-all duration-200 ${focusedField === 'username' ? 'opacity-100' : 'opacity-0'
                        }`}>
                        <i className="fas fa-user text-blue-500"></i>
                    </div>
                </div>
            </div>

            {/* 密码输入 */}
            <div className="mb-6 relative">
                <label
                    htmlFor="password"
                    className={`absolute left-4 transition-all duration-200 pointer-events-none z-10 ${focusedField === 'password' || password
                        ? 'top-2 text-xs text-blue-600'
                        : 'top-4 text-gray-500'
                        }`}
                >
                    密码
                </label>
                <div className="relative">
                    <input
                        id="password"
                        type={showPassword ? 'text' : 'password'}
                        className={`w-full px-4 pt-6 pb-2 pr-12 bg-white border-2 rounded-xl transition-all duration-200 focus:outline-none ${focusedField === 'password'
                            ? 'border-blue-500 shadow-lg shadow-blue-100/50'
                            : 'border-gray-200 hover:border-gray-300'
                            }`}
                        value={password}
                        onChange={handleInputChange(setPassword)}
                        onFocus={() => setFocusedField('password')}
                        onBlur={() => setFocusedField('')}
                        disabled={isSubmitting}
                        autoComplete="current-password"
                    />
                    <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-blue-500 transition-colors duration-200 z-10"
                    >
                        <i className={`fas ${showPassword ? 'fa-eye-slash' : 'fa-eye'}`}></i>
                    </button>
                </div>
            </div>

            {/* 记住登录和忘记密码 */}
            <div className="flex items-center justify-between mb-8">
                <label className="flex items-center cursor-pointer group">
                    <div className="relative">
                        <input
                            id="remember"
                            type="checkbox"
                            className="sr-only"
                            checked={remember}
                            onChange={(e) => setRemember(e.target.checked)}
                            disabled={isSubmitting}
                        />
                        <div className={`w-5 h-5 rounded border-2 transition-all duration-200 flex items-center justify-center ${remember
                            ? 'bg-blue-500 border-blue-500'
                            : 'bg-white border-gray-300 group-hover:border-gray-400'
                            }`}>
                            {remember && (
                                <i className="fas fa-check text-white text-xs"></i>
                            )}
                        </div>
                    </div>
                    <span className="ml-2 text-sm text-gray-700 select-none">记住登录状态</span>
                </label>

                <a href="#" className="text-sm text-blue-600 hover:text-blue-700 font-medium transition-colors duration-200">
                    忘记密码？
                </a>
            </div>

            {/* 提交按钮 */}
            <button
                type="submit"
                className="w-full py-4 bg-gradient-to-r from-blue-500 to-purple-500 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-blue-300/50 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none hover:from-blue-600 hover:to-purple-600"
                disabled={isSubmitting}
            >
                {isSubmitting ? (
                    <span className="flex items-center justify-center">
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-3"></div>
                        登录中...
                    </span>
                ) : (
                    <span className="flex items-center justify-center">
                        <i className="fas fa-sign-in-alt mr-2"></i>
                        立即登录
                    </span>
                )}
            </button>
        </form>
    );
};

export default LoginForm; 