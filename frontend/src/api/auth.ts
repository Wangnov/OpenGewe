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

// 缓存机制
interface CacheItem<T> {
  value: T;
  timestamp: number;
  expiresIn: number; // 毫秒
}

/**
 * 缓存管理器
 */
class Cache {
  private cache: Map<string, CacheItem<any>> = new Map();

  /**
   * 获取缓存项
   * @param key 缓存键
   * @returns 缓存值，如果不存在或已过期则返回null
   */
  get<T>(key: string): T | null {
    const item = this.cache.get(key);
    const now = Date.now();

    if (!item) return null;
    if (now - item.timestamp > item.expiresIn) {
      this.cache.delete(key);
      return null;
    }

    return item.value as T;
  }

  /**
   * 设置缓存项
   * @param key 缓存键
   * @param value 缓存值
   * @param expiresIn 过期时间（毫秒），默认5分钟
   */
  set<T>(key: string, value: T, expiresIn: number = 5 * 60 * 1000): void {
    this.cache.set(key, {
      value,
      timestamp: Date.now(),
      expiresIn
    });
  }

  /**
   * 清除缓存项
   * @param key 缓存键
   */
  clear(key?: string): void {
    if (key) {
      this.cache.delete(key);
    } else {
      this.cache.clear();
    }
  }
}

// 创建缓存实例
const cache = new Cache();

// 认证服务
export const AuthService = {
  /**
   * 检查管理员账户是否已初始化，没有则自动初始化
   * @param ignoreCache 是否忽略缓存
   * @returns 初始化状态
   */
  async checkAdminInit(ignoreCache: boolean = false): Promise<ApiResponse<{ initialized: boolean; admin_count: number; detail?: string }>> {
    const cacheKey = 'admin-init-status';
    
    // 如果不忽略缓存，尝试从缓存获取
    if (!ignoreCache) {
      const cachedResult = cache.get<ApiResponse<{ initialized: boolean; admin_count: number; detail?: string }>>(cacheKey);
      if (cachedResult) {
        console.log('[AUTH] 使用缓存的管理员初始化状态');
        return cachedResult;
      }
    }
    
    // 缓存未命中或忽略缓存，从服务器获取
    const response = await apiClient.get<{ initialized: boolean; admin_count: number; detail?: string }>('/admin/check-init');
    
    // 如果请求成功，缓存结果（缓存10秒，避免频繁请求）
    if (response.success) {
      cache.set(cacheKey, response, 10000); // 10秒缓存
    }
    
    return response;
  },

  /**
   * 用户登录
   * @param credentials 登录凭证
   * @returns 登录结果，包含认证token和用户信息
   */
  async login(credentials: LoginCredentials): Promise<ApiResponse<{ access_token: string; token_type: string; user: UserInfo }>> {
    // 登录成功后需要清除admin-init-status缓存
    const response = await apiClient.post<{ access_token: string; token_type: string; user: UserInfo }>('/admin/login', credentials);
    
    if (response.success) {
      cache.clear('admin-init-status');
    }
    
    return response;
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
    cache.clear(); // 清除所有缓存
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