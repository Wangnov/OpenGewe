import React from 'react';
import { Outlet } from 'react-router-dom';

/**
 * 认证页面布局组件
 * @returns {JSX.Element} 认证页面布局
 */
const AuthLayout = () => {
    return (
        <div className="min-h-screen bg-light">
            <Outlet />
        </div>
    );
};

export default AuthLayout; 