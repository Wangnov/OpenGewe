import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';

/**
 * 受保护的路由组件，用于保护需要认证的路由
 * @returns {JSX.Element} 受保护的路由
 */
const ProtectedRoute = () => {
    const { isAuthenticated, loading } = useAuth();

    // 如果正在加载认证状态，显示加载中
    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <i className="fas fa-circle-notch fa-spin text-4xl text-primary mb-4"></i>
                    <p className="text-gray-600">正在加载...</p>
                </div>
            </div>
        );
    }

    // 如果未认证，重定向到登录页
    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }

    // 已认证，渲染子路由
    return <Outlet />;
};

export default ProtectedRoute; 