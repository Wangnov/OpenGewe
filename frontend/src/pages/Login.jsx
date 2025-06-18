import React, { useEffect, useState } from 'react';
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
    const [currentFeature, setCurrentFeature] = useState(0);
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    const [hoveredFeature, setHoveredFeature] = useState(null);

    // 如果已经登录，重定向到仪表盘
    useEffect(() => {
        if (isAuthenticated) {
            navigate('/dashboard');
        }
    }, [isAuthenticated, navigate]);

    // 鼠标跟踪效果
    useEffect(() => {
        const handleMouseMove = (e) => {
            setMousePosition({
                x: (e.clientX / window.innerWidth - 0.5) * 20,
                y: (e.clientY / window.innerHeight - 0.5) * 20
            });
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);

    // 特性轮播
    const features = [
        { icon: 'fas fa-robot', title: '多机器人管理', description: '集中管理多个微信机器人账号' },
        { icon: 'fas fa-plug', title: '插件系统', description: '灵活配置各种功能插件' },
        { icon: 'fas fa-chart-line', title: '数据统计', description: '实时监控机器人运行状态' },
        { icon: 'fas fa-comments', title: '联系人管理', description: '高效管理机器人联系人' }
    ];

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentFeature((prev) => (prev + 1) % features.length);
        }, 3000);
        return () => clearInterval(timer);
    }, [features.length]);

    return (
        <div className="min-h-screen flex">
            {/* 移动端顶部品牌区域 */}
            <div className="md:hidden fixed top-0 left-0 right-0 z-20 px-6 py-4 bg-white/70 backdrop-blur-md border-b border-gray-100">
                <div className="flex items-center justify-center">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-400/80 to-purple-400/80 flex items-center justify-center shadow-lg mr-3">
                        <i className="fas fa-robot text-white text-lg"></i>
                    </div>
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-500/90 to-purple-500/90 bg-clip-text text-transparent">
                        OpenGewe
                    </h1>
                </div>
            </div>

            {/* 左侧登录表单区域 */}
            <div className="w-full md:w-5/12 lg:w-2/5 flex items-center justify-center p-6 md:p-12 mt-20 md:mt-0 relative">
                {/* 浮动装饰元素 */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    <div
                        className="absolute top-10 left-10 w-32 h-32 bg-blue-300/30 rounded-full blur-3xl"
                        style={{
                            transform: `translate(${mousePosition.x}px, ${mousePosition.y}px)`
                        }}
                    />
                    <div
                        className="absolute bottom-10 right-10 w-40 h-40 bg-purple-300/30 rounded-full blur-3xl"
                        style={{
                            transform: `translate(${-mousePosition.x}px, ${-mousePosition.y}px)`
                        }}
                    />
                </div>

                <div className="w-full max-w-md relative z-10">
                    {/* 桌面端品牌信息 */}
                    <div className="hidden md:block mb-10 text-center">
                        <div className="inline-flex items-center justify-center mb-6 relative">
                            {/* 动态光环效果 */}
                            <div className="absolute inset-0 w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-400/30 to-purple-400/30 blur-xl animate-pulse"></div>
                            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center shadow-2xl transform hover:scale-110 transition-transform duration-300 relative">
                                <i className="fas fa-robot text-white text-2xl"></i>
                            </div>
                        </div>
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent mb-2">
                            OpenGewe
                        </h1>
                        <p className="text-gray-500 text-sm">微信机器人智能管理平台</p>
                    </div>

                    {/* 登录表单容器 */}
                    <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-lg p-8 md:p-10 border border-gray-100/50 hover:shadow-xl transition-shadow duration-300">
                        <LoginForm />
                    </div>

                    {/* 底部提示 - 更加简洁 */}
                    <div className="mt-8 text-center">
                        <p className="text-xs text-gray-400">
                            安全加密 · 隐私保护 · 专业服务
                        </p>
                    </div>
                </div>
            </div>

            {/* 右侧展示区域 - 仅桌面端显示 */}
            <div className="hidden md:flex md:w-7/12 lg:w-3/5 bg-gradient-to-br from-blue-100/70 via-purple-100/50 to-indigo-100/40 p-12 items-center justify-center relative overflow-hidden">
                {/* 装饰背景 - 更浓郁的蓝紫色 */}
                <div className="absolute inset-0 opacity-40">
                    <div className="absolute top-20 left-20 w-64 h-64 bg-blue-500/50 rounded-full mix-blend-multiply filter blur-3xl animate-float"></div>
                    <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/50 rounded-full mix-blend-multiply filter blur-3xl animate-float animation-delay-2000"></div>
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-indigo-500/40 rounded-full mix-blend-multiply filter blur-3xl animate-float animation-delay-4000"></div>
                </div>

                {/* 创意元素：几何图形装饰 */}
                <div className="absolute inset-0 opacity-10">
                    <div className="absolute top-1/4 left-1/4 w-32 h-32 border-4 border-gray-300 rounded-full animate-spin-slow"></div>
                    <div className="absolute bottom-1/4 right-1/4 w-24 h-24 border-4 border-gray-300 rounded-lg animate-spin-reverse"></div>
                    <div className="absolute top-1/2 right-1/3 w-16 h-16 border-4 border-gray-300 rounded-full animate-pulse"></div>
                </div>

                <div className="relative z-10 max-w-2xl">
                    <h2 className="text-4xl md:text-5xl font-bold text-gray-700 mb-6 leading-tight">
                        智能化管理您的
                        <br />
                        <span className="bg-gradient-to-r from-blue-500/80 to-purple-500/80 bg-clip-text text-transparent">微信机器人</span>
                    </h2>
                    <p className="text-xl text-gray-600 mb-12">
                        一站式解决方案，让机器人管理变得简单高效
                    </p>

                    {/* 特性展示 - 更柔和的设计 */}
                    <div className="grid grid-cols-2 gap-6">
                        {features.map((feature, index) => {
                            // 为每个卡片定义不同的渐变色
                            const gradients = [
                                'from-blue-500 to-indigo-500',
                                'from-indigo-500 to-purple-500',
                                'from-purple-500 to-pink-500',
                                'from-pink-500 to-blue-500'
                            ];

                            return (
                                <div
                                    key={index}
                                    className={`bg-white/60 backdrop-blur-md rounded-2xl p-6 border border-gray-200/50 transform transition-all duration-500 hover:shadow-lg relative ${index === currentFeature ? 'scale-105 bg-white/80 shadow-md' : 'hover:scale-105'
                                        }`}
                                    onMouseEnter={() => setHoveredFeature(index)}
                                    onMouseLeave={() => setHoveredFeature(null)}
                                >
                                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${gradients[index]} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                                        <i className={`${feature.icon} text-2xl text-white`}></i>
                                    </div>
                                    <h3 className="text-lg font-semibold text-gray-700 mb-2">{feature.title}</h3>
                                    <p className="text-sm text-gray-500">{feature.description}</p>

                                    {/* 创意元素：悬停指示器 */}
                                    <div className={`absolute -bottom-1 left-1/2 -translate-x-1/2 w-16 h-1 bg-gradient-to-r ${gradients[index]} rounded-full transition-all duration-300 ${hoveredFeature === index ? 'opacity-100' : 'opacity-0'
                                        }`}></div>
                                </div>
                            );
                        })}
                    </div>

                    {/* 创意元素：代码展示 */}
                    <div className="mt-12 p-4 bg-gray-900/5 backdrop-blur-sm rounded-xl border border-gray-200/50">
                        <div className="flex items-center justify-between mb-2">
                            <div className="flex space-x-2">
                                <div className="w-3 h-3 rounded-full bg-red-400/50"></div>
                                <div className="w-3 h-3 rounded-full bg-yellow-400/50"></div>
                                <div className="w-3 h-3 rounded-full bg-green-400/50"></div>
                            </div>
                            <span className="text-xs text-gray-400">message_example.py</span>
                        </div>
                        <pre className="text-xs text-gray-600 font-mono">
                            <code>{`# OpenGewe 发送消息示例
from opengewe import GeweClient

client = GeweClient(token="your_token")

# 发送文本消息
await client.send_text_message(
    wxid="friend@wechat",
    content="Hello, OpenGewe!"
)`}</code>
                        </pre>
                    </div>
                </div>
            </div>

            {/* 移动端底部特性展示 */}
            <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-xl border-t border-gray-100 p-4">
                <div className="flex items-center justify-center space-x-2 mb-3">
                    {features.map((_, index) => (
                        <div
                            key={index}
                            className={`h-1.5 rounded-full transition-all duration-300 ${index === currentFeature ? 'bg-purple-400 w-8' : 'bg-gray-300 w-1.5'
                                }`}
                        />
                    ))}
                </div>
                <div className="text-center">
                    <h3 className="text-sm font-semibold text-gray-700">{features[currentFeature].title}</h3>
                    <p className="text-xs text-gray-500 mt-1">{features[currentFeature].description}</p>
                </div>
            </div>
        </div>
    );
};

export default Login; 