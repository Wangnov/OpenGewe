import { apiClient, ApiResponse } from './client';

// 登录凭证接口
export interface LoginCredentials {
  username: string;
  password: string;
}

// 用户信息接口
export interface UserInfo {
  id: number;
  username: string;
  email?: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

// 认证服务
export const AuthService = {
  /**
   * 用户登录
   * @param credentials 登录凭证
   * @returns 登录结果，包含认证token
   */
  async login(credentials: LoginCredentials): Promise<ApiResponse<{ access_token: string }>> {
    return apiClient.post<{ access_token: string }>('/admin/login', credentials);
  },

  /**
   * 获取当前用户信息
   * @returns 用户信息
   */
  async getCurrentUser(): Promise<ApiResponse<UserInfo>> {
    return apiClient.get<UserInfo>('/admin/me');
  },

  /**
   * 修改密码
   * @param data 包含旧密码和新密码的对象
   * @returns 操作结果
   */
  async changePassword(data: { old_password: string; new_password: string }): Promise<ApiResponse> {
    return apiClient.put('/admin/me/password', data);
  },

  /**
   * 退出登录
   * @returns 操作结果
   */
  async logout(): Promise<void> {
    localStorage.removeItem('auth_token');
  },

  /**
   * 检查用户是否已登录
   * @returns 是否已登录
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  },
}; 