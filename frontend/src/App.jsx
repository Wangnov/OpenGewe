import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { NotificationProvider } from './contexts/NotificationContext';
import AuthLayout from './layouts/AuthLayout';
import MainLayout from './layouts/MainLayout';
import Login from './pages/Login';
import Bots from './pages/Bots';
import Settings from './pages/Settings';
import Plugins from './pages/Plugins';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Dashboard from './pages/Dashboard';

/**
 * 应用主组件
 * @returns {JSX.Element} 应用主组件
 */
function App() {
  return (
    <BrowserRouter>
      <NotificationProvider>
        <AuthProvider>
          <Routes>
            {/* 认证页面路由 */}
            <Route element={<AuthLayout />}>
              <Route path="/login" element={<Login />} />
            </Route>

            {/* 受保护的主应用路由 */}
            <Route element={<ProtectedRoute />}>
              <Route element={<MainLayout />}>
                {/* 仪表盘 */}
                <Route path="/dashboard" element={<Dashboard />} />

                {/* 机器人管理 */}
                <Route path="/bots" element={<Bots />} />
                <Route path="/bots/:botId" element={<div>机器人详情页面（待实现）</div>} />

                {/* 插件管理 */}
                <Route path="/plugins" element={<Plugins />} />

                {/* 系统设置 */}
                <Route path="/settings" element={<Settings />} />
              </Route>
            </Route>

            {/* 默认重定向 */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </AuthProvider>
      </NotificationProvider>
    </BrowserRouter>
  );
}

export default App;
