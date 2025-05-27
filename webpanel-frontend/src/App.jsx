import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import AuthLayout from './layouts/AuthLayout';
import MainLayout from './layouts/MainLayout';
import Login from './pages/Login';
import ProtectedRoute from './components/auth/ProtectedRoute';

/**
 * 应用主组件
 * @returns {JSX.Element} 应用主组件
 */
function App() {
  return (
    <BrowserRouter>
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
              <Route path="/dashboard" element={<div>仪表盘页面（待实现）</div>} />

              {/* 机器人管理 */}
              <Route path="/bots" element={<div>机器人管理页面（待实现）</div>} />
              <Route path="/bots/:botId" element={<div>机器人详情页面（待实现）</div>} />

              {/* 插件管理 */}
              <Route path="/plugins" element={<div>插件管理页面（待实现）</div>} />

              {/* 系统设置 */}
              <Route path="/settings" element={<div>系统设置页面（待实现）</div>} />
            </Route>
          </Route>

          {/* 默认重定向 */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
