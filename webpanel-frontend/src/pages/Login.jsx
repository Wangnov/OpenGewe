import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import LoginForm from '../components/auth/LoginForm';
import useAuth from '../hooks/useAuth';

/**
 * 登录页面
 * @returns {JSX.Element} 登录页面
 */
const Login = () => {
    const { isAuthenticated } = useAuth();
    const navigate = useNavigate();

    // 如果已经登录，重定向到仪表盘
    useEffect(() => {
        if (isAuthenticated) {
            navigate('/dashboard');
        }
    }, [isAuthenticated, navigate]);

    return (
        <div className="min-h-screen flex flex-col md:flex-row">
            {/* 左侧登录表单 */}
            <div className="w-full md:w-1/2 flex items-center justify-center p-8 md:p-16">
                <div className="animate-fade-in">
                    <LoginForm />
                </div>
            </div>

            {/* 右侧图片和说明 */}
            <div className="w-full md:w-1/2 bg-gradient-to-br from-primary/10 to-accent/10 flex flex-col items-center justify-center p-8 md:p-16">
                <div className="animate-slide-up max-w-lg">
                    <div className="mb-8 text-center">
                        <h2 className="text-3xl font-bold text-dark mb-4">微信机器人管理平台</h2>
                        <p className="text-gray-600 mb-6">
                            高效管理您的微信机器人，实现自动化运营，提升工作效率
                        </p>
                    </div>

                    <div className="grid grid-cols-2 gap-6">
                        <div className="card p-4 text-center">
                            <div className="text-primary mb-2">
                                <i className="fas fa-robot text-3xl"></i>
                            </div>
                            <h3 className="font-bold mb-1">多机器人管理</h3>
                            <p className="text-sm text-gray-500">集中管理多个微信机器人账号</p>
                        </div>

                        <div className="card p-4 text-center">
                            <div className="text-secondary mb-2">
                                <i className="fas fa-plug text-3xl"></i>
                            </div>
                            <h3 className="font-bold mb-1">插件系统</h3>
                            <p className="text-sm text-gray-500">灵活配置各种功能插件</p>
                        </div>

                        <div className="card p-4 text-center">
                            <div className="text-accent mb-2">
                                <i className="fas fa-chart-line text-3xl"></i>
                            </div>
                            <h3 className="font-bold mb-1">数据统计</h3>
                            <p className="text-sm text-gray-500">实时监控机器人运行状态</p>
                        </div>

                        <div className="card p-4 text-center">
                            <div className="text-orange-500 mb-2">
                                <i className="fas fa-comments text-3xl"></i>
                            </div>
                            <h3 className="font-bold mb-1">联系人管理</h3>
                            <p className="text-sm text-gray-500">高效管理机器人联系人</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login; 