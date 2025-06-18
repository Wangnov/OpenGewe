import React from 'react';
import { Outlet } from 'react-router-dom';

/**
 * 认证页面布局组件
 * @returns {JSX.Element} 认证页面布局
 */
const AuthLayout = () => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-100/70 via-purple-100/50 to-indigo-100/40 relative overflow-hidden">
            {/* 动态背景装饰 */}
            <div className="absolute inset-0 overflow-hidden">
                {/* 渐变背景叠加 */}
                <div className="absolute inset-0 bg-gradient-to-tr from-blue-200/30 via-transparent to-purple-200/30"></div>

                {/* 动态圆形装饰 */}
                <div className="blob blob-1 bg-blue-400/30"></div>
                <div className="blob blob-2 bg-purple-400/30"></div>
                <div className="blob blob-3 bg-indigo-400/25"></div>
            </div>

            {/* 内容区域 */}
            <div className="relative z-10">
                <Outlet />
            </div>
        </div >
    );
};

export default AuthLayout; 