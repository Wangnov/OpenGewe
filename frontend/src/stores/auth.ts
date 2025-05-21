import { create } from 'zustand';
import { LoginCredentials, UserInfo, AuthService } from '../api/auth';

// 认证状态接口
interface AuthState {
  // 状态
  isAuthenticated: boolean;
  isLoading: boolean;
  user: UserInfo | null;
  error: string | null;

  // 操作
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => Promise<void>;
  fetchUserInfo: () => Promise<UserInfo | null>;
  changePassword: (oldPassword: string, newPassword: string) => Promise<boolean>;
  setError: (error: string | null) => void;
}

// 创建认证状态存储
export const useAuthStore = create<AuthState>((set, get) => ({
  // 初始状态
  isAuthenticated: AuthService.isAuthenticated(),
  isLoading: false,
  user: null,
  error: null,

  // 登录操作
  login: async (credentials: LoginCredentials) => {
    try {
      set({ isLoading: true, error: null });
      console.log('[Auth Store] 尝试登录:', credentials.username);
      
      const response = await AuthService.login(credentials);
      console.log('[Auth Store] 登录响应:', response);
      
      if (response.success && response.data) {
        // 保存令牌
        localStorage.setItem('auth_token', response.data.access_token);
        
        // 检查用户信息是否存在
        if (response.data.user) {
          console.log('[Auth Store] 登录成功，用户信息:', response.data.user);
          set({ 
            isAuthenticated: true, 
            isLoading: false,
            user: response.data.user
          });
          return true;
        } else {
          // 如果没有用户信息，尝试获取
          console.log('[Auth Store] 登录成功但缺少用户信息，尝试获取用户信息');
          const userInfo = await get().fetchUserInfo();
          
          if (userInfo) {
            return true;
          } else {
            set({ 
              isLoading: false, 
              error: '登录成功但无法获取用户信息'
            });
            return false;
          }
        }
      } else {
        set({ 
          isLoading: false, 
          error: response.message || response.error || '登录失败，请检查用户名和密码' 
        });
        return false;
      }
    } catch (error) {
      console.error('[Auth Store] 登录错误:', error);
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '登录过程中发生错误' 
      });
      return false;
    }
  },

  // 登出操作
  logout: async () => {
    try {
      set({ isLoading: true });
      await AuthService.logout();
      set({ 
        isAuthenticated: false, 
        user: null, 
        isLoading: false 
      });
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '登出过程中发生错误' 
      });
    }
  },

  // 获取用户信息
  fetchUserInfo: async () => {
    try {
      set({ isLoading: true, error: null });
      const response = await AuthService.getCurrentUser();
      
      if (response.success && response.data) {
        set({ 
          isLoading: false, 
          user: response.data,
          isAuthenticated: true
        });
        return response.data;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '获取用户信息失败',
          isAuthenticated: false,
          user: null
        });
        return null;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '获取用户信息过程中发生错误',
        isAuthenticated: false,
        user: null
      });
      return null;
    }
  },

  // 修改密码
  changePassword: async (oldPassword: string, newPassword: string) => {
    try {
      set({ isLoading: true, error: null });
      const response = await AuthService.changePassword({
        old_password: oldPassword,
        new_password: newPassword
      });
      
      set({ isLoading: false });
      
      if (response.success) {
        return true;
      } else {
        set({ error: response.message || '修改密码失败' });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '修改密码过程中发生错误' 
      });
      return false;
    }
  },

  // 设置错误
  setError: (error: string | null) => set({ error }),
})); 