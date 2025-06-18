import React, { useState, useCallback, useMemo } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

/**
 * 移动端底部导航栏组件
 * @returns {JSX.Element} 移动端底部导航栏
 */
const MobileBottomNav = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [showUserTooltip, setShowUserTooltip] = useState(false);

    // 处理登出 - 使用useCallback优化性能
    const handleLogout = useCallback(async () => {
        await logout();
        navigate('/login');
        setShowUserTooltip(false);
    }, [logout, navigate]);

    // 切换用户tooltip显示状态
    const toggleUserTooltip = useCallback(() => {
        setShowUserTooltip(prev => !prev);
    }, []);

    // 导航项配置 - 使用useMemo优化性能
    const navItems = useMemo(() => [
        { to: '/dashboard', icon: 'fas fa-chart-pie', label: '仪表盘', gradient: 'from-blue-400 to-blue-600' },
        { to: '/bots', icon: 'fab fa-weixin', label: '机器人', gradient: 'from-purple-400 to-purple-600' },
        { to: '/plugins', icon: 'fas fa-puzzle-piece', label: '插件', gradient: 'from-indigo-400 to-indigo-600' },
        { to: '/settings', icon: 'fas fa-sliders-h', label: '设置', gradient: 'from-violet-400 to-violet-600' }
    ], []);

    return (
        <>
            {/* 移动端底部导航栏 - 仅在移动端显示 */}
            <div className="md:hidden fixed bottom-0 left-0 right-0 z-50">
                {/* 用户tooltip */}
                {showUserTooltip && (
                    <>
                        {/* 遮罩层 */}
                        <div
                            className="fixed inset-0 bg-black/20 backdrop-blur-sm"
                            onClick={() => setShowUserTooltip(false)}
                        />
                        {/* tooltip内容 */}
                        <div className="absolute bottom-20 right-4 bg-white/60 backdrop-blur-xl rounded-xl shadow-xl border border-gray-200/50 p-4 min-w-[200px]">
                            <div className="flex items-center space-x-3 mb-3">
                                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold shadow-lg">
                                    {user?.username?.charAt(0).toUpperCase() || 'U'}
                                </div>
                                <div>
                                    <p className="text-sm font-semibold text-gray-800">{user?.username || '用户'}</p>
                                    <p className="text-xs text-gray-500">管理员</p>
                                </div>
                            </div>
                            <button
                                onClick={handleLogout}
                                className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white rounded-xl transition-all duration-200 text-sm font-medium shadow-lg hover:shadow-xl"
                            >
                                <i className="fas fa-sign-out-alt"></i>
                                <span>退出登录</span>
                            </button>
                            {/* 小三角箭头 */}
                            <div className="absolute bottom-[-6px] right-6 w-3 h-3 bg-white/60 border-r border-b border-gray-200/50 transform rotate-45"></div>
                        </div>
                    </>
                )}

                {/* 底部导航栏主体 */}
                <div className="bg-white/60 backdrop-blur-xl border-t border-gray-200/50 shadow-xl">
                    <div className="flex items-center">
                        {/* 可滚动的导航项容器 */}
                        <div className="flex-1 overflow-x-auto scrollbar-hide">
                            <div className="flex space-x-1 px-2">
                                {navItems.map((item) => (
                                    <NavLink
                                        key={item.to}
                                        to={item.to}
                                        className={({ isActive }) =>
                                            `flex flex-col items-center justify-center min-w-[70px] p-3 my-2 rounded-xl transition-all duration-300 relative ${isActive
                                                ? 'bg-white/80 shadow-lg backdrop-blur-sm border border-gray-200/50'
                                                : 'hover:bg-white/50'
                                            }`
                                        }
                                    >
                                        {({ isActive }) => (
                                            <>
                                                {/* 活跃状态的渐变背景 */}
                                                {isActive && (
                                                    <div className={`absolute inset-0 bg-gradient-to-r ${item.gradient} opacity-10 rounded-xl`} />
                                                )}

                                                {/* 图标 */}
                                                <div className={`w-6 h-6 rounded-lg flex items-center justify-center transition-all duration-300 relative z-10 mb-1 ${isActive
                                                    ? `bg-gradient-to-r ${item.gradient} text-white shadow-md`
                                                    : 'text-gray-500'
                                                    }`}>
                                                    <i className={`${item.icon} text-xs`}></i>
                                                </div>

                                                {/* 标签 */}
                                                <span className={`text-xs font-medium transition-all duration-300 relative z-10 ${isActive ? 'text-gray-800' : 'text-gray-600'
                                                    }`}>
                                                    {item.label}
                                                </span>

                                                {/* 活跃指示器 */}
                                                {isActive && (
                                                    <div className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 animate-pulse" />
                                                )}
                                            </>
                                        )}
                                    </NavLink>
                                ))}
                            </div>
                        </div>

                        {/* 固定的用户头像 */}
                        <div className="flex-shrink-0 ml-2 pl-2 border-l border-gray-200/50">
                            <button
                                onClick={toggleUserTooltip}
                                className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold shadow-lg transition-all duration-300 hover:scale-105 active:scale-95"
                            >
                                {user?.username?.charAt(0).toUpperCase() || 'U'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* 移动端底部占位空间，避免内容被导航栏遮挡 */}
            <div className="md:hidden h-20"></div>
        </>
    );
};

export default MobileBottomNav;