import React, { useState, useCallback, useMemo } from 'react';
import { Outlet, NavLink, useNavigate, useLocation } from 'react-router-dom';
import useAuth from '../hooks/useAuth';
import useNotification from '../hooks/useNotification';
import MobileBottomNav from '../components/MobileBottomNav';
import NotificationBar from '../components/notifications/NotificationBar';
import NotificationBadge from '../components/notifications/NotificationBadge';
import NotificationHistory from '../components/notifications/NotificationHistory';

/**
 * 主布局组件 - 现代化Bento Grid风格设计
 * @returns {JSX.Element} 主布局
 */
const MainLayout = () => {
    const { user, logout } = useAuth();
    const { toggleHistory, unreadCount } = useNotification();
    const navigate = useNavigate();
    const location = useLocation();
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    // 处理登出 - 使用useCallback优化性能
    const handleLogout = useCallback(async () => {
        await logout();
        navigate('/login');
    }, [logout, navigate]);

    // 切换侧边栏 - 使用useCallback优化性能
    const toggleSidebar = useCallback(() => {
        setIsSidebarOpen(prev => !prev);
    }, []);

    // 导航项配置 - 使用useMemo优化性能
    const navItems = useMemo(() => [
        { to: '/dashboard', icon: 'fas fa-chart-pie', label: '仪表盘', gradient: 'from-blue-400 to-blue-600' },
        { to: '/bots', icon: 'fab fa-weixin', label: '机器人管理', gradient: 'from-purple-400 to-purple-600' },
        { to: '/plugins', icon: 'fas fa-puzzle-piece', label: '插件管理', gradient: 'from-indigo-400 to-indigo-600' },
        { to: '/settings', icon: 'fas fa-sliders-h', label: '系统设置', gradient: 'from-violet-400 to-violet-600' }
    ], []);

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-100/70 via-purple-100/50 to-indigo-100/40 flex relative overflow-hidden">
            {/* 动态背景装饰 - 与Login页面一致 */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-20 left-20 w-64 h-64 bg-blue-500/50 rounded-full mix-blend-multiply filter blur-3xl animate-float"></div>
                <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/50 rounded-full mix-blend-multiply filter blur-3xl animate-float animation-delay-2000"></div>
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-indigo-500/40 rounded-full mix-blend-multiply filter blur-3xl animate-float animation-delay-4000"></div>
            </div>

            {/* 侧边栏 - 桌面端显示，移动端隐藏 */}
            <aside
                className={`hidden md:flex backdrop-blur-xl bg-white/60 border-r border-gray-200/50 shadow-xl transition-all duration-500 ease-out ${isSidebarOpen ? 'w-60' : 'w-20'
                    } flex-col relative z-10`}
            >
                {/* 侧边栏头部 */}
                <div className={`p-6 flex items-center relative ${isSidebarOpen ? 'justify-between' : 'flex-col space-y-4'}`}>
                    {isSidebarOpen ? (
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center shadow-lg flex-shrink-0">
                                <i className="fas fa-robot text-white text-lg"></i>
                            </div>
                            <div>
                                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
                                    OpenGewe
                                </h1>
                                <p className="text-xs text-gray-500 font-medium">智能管理平台</p>
                            </div>
                        </div>
                    ) : (
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center shadow-lg flex-shrink-0">
                            <i className="fas fa-robot text-white text-lg"></i>
                        </div>
                    )}
                    <button
                        onClick={toggleSidebar}
                        className="p-2 rounded-xl hover:bg-white/70 backdrop-blur-sm transition-all duration-300 text-gray-600 hover:text-blue-600 hover:scale-110 flex-shrink-0"
                    >
                        <i className={`fas ${isSidebarOpen ? 'fa-chevron-left' : 'fa-chevron-right'} text-sm`}></i>
                    </button>
                </div>

                {/* 导航菜单 */}
                <nav className="flex-1 px-4 py-2 relative">
                    <ul className="space-y-2">
                        {navItems.map((item) => (
                            <li key={item.to}>
                                <NavLink
                                    to={item.to}
                                    className={({ isActive }) =>
                                        `group flex items-center ${isSidebarOpen ? 'px-4 py-3' : 'p-3 justify-center w-12 h-12'} rounded-xl transition-all duration-300 relative overflow-hidden ${isActive
                                            ? 'bg-white/80 shadow-lg backdrop-blur-sm border border-gray-200/50 text-gray-800'
                                            : 'text-gray-600 hover:bg-white/50 hover:text-gray-800 hover:shadow-md'
                                        }`
                                    }
                                >
                                    {({ isActive }) => (
                                        <>
                                            {/* 活跃状态的渐变背景 */}
                                            {isActive && (
                                                <div className={`absolute inset-0 bg-gradient-to-r ${item.gradient} opacity-10 rounded-xl`} />
                                            )}

                                            {/* 图标容器 - 修复收起时的尺寸问题 */}
                                            <div className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-300 relative z-10 flex-shrink-0 ${isActive
                                                ? `bg-gradient-to-r ${item.gradient} text-white shadow-lg`
                                                : 'text-gray-500 group-hover:text-gray-700'
                                                }`}>
                                                <i className={`${item.icon} text-sm`}></i>
                                            </div>

                                            {/* 标签 */}
                                            {isSidebarOpen && (
                                                <span className="ml-3 font-medium text-sm relative z-10 transition-all duration-300">
                                                    {item.label}
                                                </span>
                                            )}

                                            {/* 活跃指示器 - 仅在展开状态下显示 */}
                                            {isActive && isSidebarOpen && (
                                                <div className="absolute right-2 w-2 h-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 animate-pulse" />
                                            )}
                                        </>
                                    )}
                                </NavLink>
                            </li>
                        ))}
                    </ul>
                </nav>

                {/* 侧边栏底部 */}
                <div className="p-4 relative">
                    <div className={`flex items-center p-3 rounded-xl bg-white/60 backdrop-blur-sm border border-gray-200/50 transition-all duration-300 ${isSidebarOpen ? 'justify-start' : 'justify-center'
                        }`}>
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold shadow-lg flex-shrink-0">
                            {user?.username?.charAt(0).toUpperCase() || 'U'}
                        </div>
                        {isSidebarOpen && (
                            <div className="ml-3 flex-1">
                                <p className="text-sm font-semibold text-gray-800">{user?.username || '用户'}</p>
                                <button
                                    onClick={handleLogout}
                                    className="text-xs text-gray-500 hover:text-red-500 transition-colors duration-200 flex items-center mt-1"
                                >
                                    <i className="fas fa-sign-out-alt mr-1"></i>
                                    退出登录
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </aside>

            {/* 主内容区 */}
            <main className="flex-1 flex flex-col overflow-hidden relative z-10">
                {/* 顶部导航栏 */}
                <header className="backdrop-blur-xl bg-white/60 border-b border-gray-200/50 shadow-sm relative">
                    <div className="px-6 py-4 flex items-center justify-between">
                        <div>
                            <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
                                {location.pathname === '/dashboard' && '仪表盘'}
                                {location.pathname === '/bots' && '机器人管理'}
                                {location.pathname === '/plugins' && '插件管理'}
                                {location.pathname === '/settings' && '系统设置'}
                            </h2>
                            <p className="text-sm text-gray-500 mt-1">
                                {location.pathname === '/dashboard' && '查看系统概览和统计信息'}
                                {location.pathname === '/bots' && '管理您的微信机器人实例'}
                                {location.pathname === '/plugins' && '配置和管理机器人插件'}
                                {location.pathname === '/settings' && '系统配置和参数设置'}
                            </p>
                        </div>
                        <div className="flex items-center space-x-3">
                            <button
                                onClick={toggleHistory}
                                className="relative w-12 h-12 rounded-xl bg-white/60 backdrop-blur-sm border border-gray-200/50 text-gray-600 hover:text-blue-600 hover:bg-white/80 transition-all duration-300 hover:scale-105 shadow-sm flex items-center justify-center"
                            >
                                <i className="fas fa-bell text-lg"></i>
                                <NotificationBadge count={unreadCount} />
                            </button>
                            <button className="w-12 h-12 rounded-xl bg-white/60 backdrop-blur-sm border border-gray-200/50 text-gray-600 hover:text-purple-600 hover:bg-white/80 transition-all duration-300 hover:scale-105 shadow-sm flex items-center justify-center">
                                <i className="fas fa-question-circle text-lg"></i>
                            </button>
                        </div>
                    </div>
                </header>

                {/* 内容区 */}
                <div className="flex-1 overflow-auto p-6 md:p-6 pb-24 md:pb-6 relative">
                    <Outlet />
                </div>
            </main>

            {/* 移动端底部导航栏 */}
            <MobileBottomNav />

            {/* 浮动通知栏 */}
            <NotificationBar />

            {/* 通知历史弹窗 */}
            <NotificationHistory />
        </div>
    );
};

export default MainLayout;