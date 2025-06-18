import React from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * 仪表盘页面
 * @returns {JSX.Element} 仪表盘页面
 */
const Dashboard = () => {
    const navigate = useNavigate();

    // 统计卡片数据
    const stats = [
        {
            icon: 'fab fa-weixin',
            title: '在线机器人',
            value: '3',
            total: '5',
            gradient: 'from-blue-500 to-indigo-500',
            bgGradient: 'from-blue-100 to-indigo-100'
        },
        {
            icon: 'fas fa-puzzle-piece',
            title: '已启用插件',
            value: '12',
            total: '20',
            gradient: 'from-indigo-500 to-purple-500',
            bgGradient: 'from-indigo-100 to-purple-100'
        },
        {
            icon: 'fas fa-comments',
            title: '今日消息',
            value: '1,258',
            trend: '+12%',
            gradient: 'from-purple-500 to-pink-500',
            bgGradient: 'from-purple-100 to-pink-100'
        },
        {
            icon: 'fas fa-users',
            title: '活跃用户',
            value: '356',
            trend: '+5%',
            gradient: 'from-pink-500 to-blue-500',
            bgGradient: 'from-pink-100 to-blue-100'
        }
    ];

    // 快捷操作
    const quickActions = [
        { icon: 'fas fa-plus', label: '添加机器人', path: '/bots', color: 'blue' },
        { icon: 'fas fa-plug', label: '管理插件', path: '/plugins', color: 'purple' },
        { icon: 'fas fa-cog', label: '系统设置', path: '/settings', color: 'indigo' }
    ];

    return (
        <div className="space-y-6">
            {/* 欢迎区域 */}
            <div className="bg-white/60 backdrop-blur-md rounded-3xl p-8 border border-gray-200/50 shadow-lg">
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent mb-2">
                    欢迎回来
                </h1>
                <p className="text-gray-600">系统运行正常，一切准备就绪</p>
            </div>

            {/* 统计卡片 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, index) => (
                    <div
                        key={index}
                        className="bg-white/60 backdrop-blur-md rounded-2xl p-6 border border-gray-200/50 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 relative overflow-hidden"
                    >
                        {/* 背景装饰 */}
                        <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${stat.bgGradient} opacity-20 rounded-full blur-3xl`}></div>

                        <div className="relative z-10">
                            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.gradient} flex items-center justify-center mb-4 shadow-lg`}>
                                <i className={`${stat.icon} text-xl text-white`}></i>
                            </div>
                            <h3 className="text-sm text-gray-600 font-medium mb-1">{stat.title}</h3>
                            <div className="flex items-baseline space-x-2">
                                <span className="text-2xl font-bold text-gray-800">{stat.value}</span>
                                {stat.total && (
                                    <span className="text-sm text-gray-500">/ {stat.total}</span>
                                )}
                                {stat.trend && (
                                    <span className={`text-sm font-medium ${stat.trend.startsWith('+') ? 'text-green-500' : 'text-red-500'}`}>
                                        {stat.trend}
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* 快捷操作区域 */}
            <div className="bg-white/60 backdrop-blur-md rounded-2xl p-6 border border-gray-200/50 shadow-lg">
                <h2 className="text-xl font-bold text-gray-800 mb-4">快捷操作</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {quickActions.map((action, index) => (
                        <button
                            key={index}
                            onClick={() => navigate(action.path)}
                            className="flex items-center space-x-3 p-4 rounded-xl bg-white/50 hover:bg-white/80 border border-gray-200/50 transition-all duration-300 hover:shadow-md hover:scale-105 group"
                        >
                            <div className={`w-10 h-10 rounded-lg bg-gradient-to-br from-${action.color}-500 to-${action.color}-600 flex items-center justify-center shadow-md group-hover:shadow-lg transition-all duration-300`}>
                                <i className={`${action.icon} text-white`}></i>
                            </div>
                            <span className="text-gray-700 font-medium">{action.label}</span>
                            <i className="fas fa-arrow-right text-gray-400 ml-auto group-hover:translate-x-1 transition-transform duration-300"></i>
                        </button>
                    ))}
                </div>
            </div>

            {/* 最近活动 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 系统状态 */}
                <div className="bg-white/60 backdrop-blur-md rounded-2xl p-6 border border-gray-200/50 shadow-lg">
                    <h2 className="text-xl font-bold text-gray-800 mb-4">系统状态</h2>
                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                                <span className="text-gray-700">服务运行状态</span>
                            </div>
                            <span className="text-green-600 font-medium">正常</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                                <span className="text-gray-700">CPU 使用率</span>
                            </div>
                            <span className="text-gray-600 font-medium">23%</span>
                        </div>
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                                <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                                <span className="text-gray-700">内存使用率</span>
                            </div>
                            <span className="text-gray-600 font-medium">45%</span>
                        </div>
                    </div>
                </div>

                {/* 最近日志 */}
                <div className="bg-white/60 backdrop-blur-md rounded-2xl p-6 border border-gray-200/50 shadow-lg">
                    <h2 className="text-xl font-bold text-gray-800 mb-4">最近日志</h2>
                    <div className="space-y-3">
                        <div className="flex items-start space-x-3">
                            <span className="text-xs text-gray-500 font-mono">10:23</span>
                            <div className="flex-1">
                                <p className="text-sm text-gray-700">机器人 Bot-001 上线成功</p>
                            </div>
                        </div>
                        <div className="flex items-start space-x-3">
                            <span className="text-xs text-gray-500 font-mono">10:15</span>
                            <div className="flex-1">
                                <p className="text-sm text-gray-700">插件 ChatGPT 已启用</p>
                            </div>
                        </div>
                        <div className="flex items-start space-x-3">
                            <span className="text-xs text-gray-500 font-mono">09:45</span>
                            <div className="flex-1">
                                <p className="text-sm text-gray-700">系统备份完成</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard; 