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
    return response;
  }

  // 错误响应处理
  private handleError = (error: AxiosError): Promise<never> => {
    const status = error.response?.status;

    // 处理认证错误（401）
    if (status === 401) {
      localStorage.removeItem('auth_token');
      // 重定向到登录页
      window.location.href = '/login';
    }

    // 处理403错误
    if (status === 403) {
      console.error('无权访问资源');
    }

    // 处理500服务器错误
    if (status === 500) {
      console.error('服务器错误，请稍后重试');
    }

    return Promise.reject(error);
  };

  // GET请求
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.get<ApiResponse<T>>(url, config);
      return response.data;
    } catch (error) {
      return this.formatError(error);
    }
  }

  // POST请求
  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.post<ApiResponse<T>>(url, data, config);
      return response.data;
    } catch (error) {
      return this.formatError(error);
    }
  }

  // PUT请求
  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.put<ApiResponse<T>>(url, data, config);
      return response.data;
    } catch (error) {
      return this.formatError(error);
    }
  }

  // DELETE请求
  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.delete<ApiResponse<T>>(url, config);
      return response.data;
    } catch (error) {
      return this.formatError(error);
    }
  }

  // 格式化错误响应
  private formatError(error: any): ApiResponse {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<ApiResponse>;
      if (axiosError.response?.data) {
        return {
          success: false,
          ...axiosError.response.data,
        };
      }
      
      return {
        success: false,
        message: axiosError.message,
        error: `${axiosError.code || 'UNKNOWN'}: ${axiosError.message}`,
      };
    }
    
    return {
      success: false,
      message: '未知错误',
      error: error?.toString() || 'Unknown error',
    };
  }
}

// 导出单例实例
export const apiClient = new ApiClient(); 