import { useEffect } from 'react';
import { redirect, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/auth';

interface AuthGuardProps {
  children: React.ReactNode;
}

/**
 * 权限守卫组件
 * 用于保护需要登录才能访问的路由
 */
export const AuthGuard = ({ children }: AuthGuardProps) => {
  const { isAuthenticated, user, fetchUserInfo } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    // 如果未登录，则尝试获取用户信息
    if (!isAuthenticated || !user) {
      // 检查是否有token
      const token = localStorage.getItem('auth_token');
      
      if (token) {
        // 有token，尝试获取用户信息
        fetchUserInfo().catch(() => {
          // 获取失败，重定向到登录页
          navigate('/login');
        });
      } else {
        // 没有token，直接重定向到登录页
        navigate('/login');
      }
    }
  }, [isAuthenticated, user, fetchUserInfo, navigate]);

  // 如果未登录且没有用户信息，显示空内容（等待重定向）
  if (!isAuthenticated || !user) {
    return null;
  }

  // 已登录，显示子组件
  return <>{children}</>;
};

/**
 * 登录路由守卫
 * 用于在服务端判断是否需要重定向到登录页
 */
export const authGuard = () => {
  // 检查是否有token
  const token = localStorage.getItem('auth_token');
  
  if (!token) {
    return redirect('/login');
  }
  
  return null;
}; 