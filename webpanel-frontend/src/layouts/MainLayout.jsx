import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

/**
 * 主布局组件
 * @returns {JSX.Element} 主布局
 */
const MainLayout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    // 处理登出
    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    // 切换侧边栏
    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    return (
        <div className="min-h-screen bg-light flex">
            {/* 侧边栏 */}
            <aside
                className={`bg-dark text-white transition-all duration-300 ${isSidebarOpen ? 'w-64' : 'w-20'
                    } flex flex-col`}
            >
                {/* 侧边栏头部 */}
                <div className="p-4 flex items-center justify-between border-b border-gray-700">
                    {isSidebarOpen ? (
                        <h1 className="text-xl font-bold text-white">OpenGewe</h1>
                    ) : (
                        <h1 className="text-xl font-bold text-white">OG</h1>
                    )}
                    <button
                        onClick={toggleSidebar}
                        className="text-gray-400 hover:text-white"
                    >
                        <i className={`fas ${isSidebarOpen ? 'fa-chevron-left' : 'fa-chevron-right'}`}></i>
                    </button>
                </div>

                {/* 导航菜单 */}
                <nav className="flex-1 py-4 overflow-y-auto">
                    <ul>
                        <li>
                            <NavLink
                                to="/dashboard"
                                className={({ isActive }) =>
                                    `flex items-center px-4 py-3 ${isActive ? 'bg-primary text-white' : 'text-gray-300 hover:bg-gray-800'}`
                                }
                            >
                                <i className="fas fa-tachometer-alt w-6"></i>
                                {isSidebarOpen && <span className="ml-2">仪表盘</span>}
                            </NavLink>
                        </li>
                        <li>
                            <NavLink
                                to="/bots"
                                className={({ isActive }) =>
                                    `flex items-center px-4 py-3 ${isActive ? 'bg-primary text-white' : 'text-gray-300 hover:bg-gray-800'}`
                                }
                            >
                                <i className="fas fa-robot w-6"></i>
                                {isSidebarOpen && <span className="ml-2">机器人管理</span>}
                            </NavLink>
                        </li>
                        <li>
                            <NavLink
                                to="/plugins"
                                className={({ isActive }) =>
                                    `flex items-center px-4 py-3 ${isActive ? 'bg-primary text-white' : 'text-gray-300 hover:bg-gray-800'}`
                                }
                            >
                                <i className="fas fa-plug w-6"></i>
                                {isSidebarOpen && <span className="ml-2">插件管理</span>}
                            </NavLink>
                        </li>
                        <li>
                            <NavLink
                                to="/settings"
                                className={({ isActive }) =>
                                    `flex items-center px-4 py-3 ${isActive ? 'bg-primary text-white' : 'text-gray-300 hover:bg-gray-800'}`
                                }
                            >
                                <i className="fas fa-cog w-6"></i>
                                {isSidebarOpen && <span className="ml-2">系统设置</span>}
                            </NavLink>
                        </li>
                    </ul>
                </nav>

                {/* 侧边栏底部 */}
                <div className="p-4 border-t border-gray-700">
                    <div className="flex items-center">
                        <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white">
                            {user?.username?.charAt(0).toUpperCase() || 'U'}
                        </div>
                        {isSidebarOpen && (
                            <div className="ml-3">
                                <p className="text-sm font-medium text-white">{user?.username || '用户'}</p>
                                <button
                                    onClick={handleLogout}
                                    className="text-xs text-gray-400 hover:text-white"
                                >
                                    退出登录
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </aside>

            {/* 主内容区 */}
            <main className="flex-1 flex flex-col overflow-hidden">
                {/* 顶部导航栏 */}
                <header className="bg-white shadow-sm z-10">
                    <div className="px-6 py-4 flex items-center justify-between">
                        <h2 className="text-xl font-semibold text-gray-800">微信机器人管理后台</h2>
                        <div className="flex items-center space-x-4">
                            <button className="text-gray-600 hover:text-primary">
                                <i className="fas fa-bell"></i>
                            </button>
                            <button className="text-gray-600 hover:text-primary">
                                <i className="fas fa-question-circle"></i>
                            </button>
                        </div>
                    </div>
                </header>

                {/* 内容区 */}
                <div className="flex-1 overflow-auto p-6">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default MainLayout; 