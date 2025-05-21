import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// 定义API响应类型
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// 创建API客户端类
class ApiClient {
  private client: AxiosInstance;
  private baseURL: string;

  constructor() {
    // 获取API基础URL，如果不存在则使用相对路径
    this.baseURL = '/api';
    
    console.log(`[API Client] Using base URL: ${this.baseURL}`);
    
    // 创建axios实例
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000, // 30秒超时
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器 - 添加认证Token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        
        // 移除URL中可能存在的v1前缀，保证一致性
        if (config.url && config.url.startsWith('/v1/')) {
          config.url = config.url.replace('/v1/', '/');
          console.warn(`[API Client] Removed v1 prefix from URL: ${config.url}`);
        }
        
        // 添加调试日志
        console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
        
        return config;
      },
      (error) => Promise.reject(error)
    );

    // 响应拦截器 - 错误处理
    this.client.interceptors.response.use(
      this.handleSuccess,
      this.handleError
    );
  }

  // 成功响应处理
  private handleSuccess(response: AxiosResponse): AxiosResponse {
    console.log(`[API Response] Status: ${response.status} for ${response.config.url}`);
    return response;
  }

  // 错误响应处理
  private handleError = (error: AxiosError): Promise<never> => {
    console.error(`[API Error] ${error.message} for ${error.config?.url}`);
    
    const status = error.response?.status;

    // 处理认证错误（401）
    if (status === 401) {
      console.warn('[API] 未授权访问，正在重定向到登录页');
      localStorage.removeItem('auth_token');
      // 重定向到登录页
      window.location.href = '/login';
    }

    // 处理403错误
    if (status === 403) {
      console.error('[API] 无权访问资源');
    }

    // 处理500服务器错误
    if (status === 500) {
      console.error('[API] 服务器错误，请稍后重试');
    }
    
    // 处理404错误 - 特别标记API路径问题
    if (status === 404) {
      console.error(`[API] 未找到资源: ${error.config?.url}`);
      console.warn('[API] 请检查API路径格式是否正确，确保不要使用v1前缀');
    }
    
    // 处理连接错误
    if (error.code === 'ECONNREFUSED' || error.code === 'ECONNABORTED') {
      console.error('[API] 无法连接到服务器，请确保后端服务已启动');
    }

    return Promise.reject(error);
  };

  // GET请求
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      // 确保URL中没有v1前缀
      const cleanUrl = this.ensureNoV1Prefix(url);
      const response = await this.client.get<ApiResponse<T>>(cleanUrl, config);
      return response.data;
    } catch (error) {
      return this.formatError(error);
    }
  }

  // POST请求
  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      // 确保URL中没有v1前缀
      const cleanUrl = this.ensureNoV1Prefix(url);
      
      // 对于登录请求，使用 form-data 格式
      if (cleanUrl === '/admin/login') {
        console.log('[API Client] 使用表单数据格式发送登录请求');
        
        const formData = new URLSearchParams();
        for (const key in data) {
          formData.append(key, data[key]);
        }
        
        const loginConfig = {
          ...config,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        };
        
        const response = await this.client.post<any>(cleanUrl, formData, loginConfig);
        
        // 调试输出
        console.log('[API Client] 登录响应:', response.data);
        
        // 格式化响应
        if (response.data && typeof response.data === 'object') {
          // 判断是否已经是标准响应格式
          if ('code' in response.data && !('success' in response.data)) {
            // 转换为标准响应格式
            const standardResponse: ApiResponse<T> = {
              success: response.data.code === 0,
              data: response.data.data,
              message: response.data.msg || '',
              error: response.data.code !== 0 ? response.data.msg : undefined
            };
            return standardResponse;
          }
        }
        
        return response.data;
      }
      
      const response = await this.client.post<ApiResponse<T>>(cleanUrl, data, config);
      return response.data;
    } catch (error) {
      return this.formatError(error);
    }
  }

  // PUT请求
  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      // 确保URL中没有v1前缀
      const cleanUrl = this.ensureNoV1Prefix(url);
      const response = await this.client.put<ApiResponse<T>>(cleanUrl, data, config);
      return response.data;
    } catch (error) {
      return this.formatError(error);
    }
  }

  // DELETE请求
  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      // 确保URL中没有v1前缀
      const cleanUrl = this.ensureNoV1Prefix(url);
      const response = await this.client.delete<ApiResponse<T>>(cleanUrl, config);
      return response.data;
    } catch (error) {
      return this.formatError(error);
    }
  }

  // 确保URL中没有v1前缀
  private ensureNoV1Prefix(url: string): string {
    if (url.startsWith('/v1/')) {
      const cleanUrl = url.replace('/v1/', '/');
      console.warn(`[API Client] Removed v1 prefix from URL: ${url} -> ${cleanUrl}`);
      return cleanUrl;
    }
    return url;
  }

  // 格式化错误响应
  private formatError(error: unknown): ApiResponse {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<any>;
      if (axiosError.response?.data) {
        const responseData = axiosError.response.data;
        // 确保不会覆盖success字段
        if (typeof responseData === 'object' && responseData !== null && 'success' in responseData) {
          return responseData as ApiResponse;
        } else if (typeof responseData === 'object' && responseData !== null) {
          return {
            success: false,
            ...responseData
          };
        }
      }
      
      return {
        success: false,
        message: axiosError.message,
        error: `${axiosError.code || 'UNKNOWN'}: ${axiosError.message}`,
      };
    }
    
    let errorMessage = 'Unknown error';
    if (error !== null && error !== undefined) {
      errorMessage = String(error);
    }
    
    return {
      success: false,
      message: '未知错误',
      error: errorMessage
    };
  }
}

// 导出单例实例
export const apiClient = new ApiClient(); 