import { apiClient, ApiResponse } from './client';

// 系统状态接口
export interface SystemStatus {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  uptime: number;
  robots_count: {
    total: number;
    online: number;
  };
  plugins_count: {
    total: number;
    enabled: number;
  };
}

// 系统配置接口
export interface SystemConfig {
  database: {
    url: string;
    debug: boolean;
  };
  redis: {
    url: string;
    prefix: string;
  };
  logging: {
    level: string;
    file: string;
  };
  server: {
    host: string;
    port: number;
    debug: boolean;
    cors_origins: string[];
  };
  [key: string]: any;
}

// 日志记录接口
export interface LogEntry {
  id: number;
  timestamp: string;
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
  module: string;
  message: string;
  details?: Record<string, any>;
}

// 系统API服务
export const SystemService = {
  /**
   * 获取系统状态
   */
  async getStatus(): Promise<ApiResponse<SystemStatus>> {
    return apiClient.get<SystemStatus>('/system/status');
  },

  /**
   * 获取系统配置
   */
  async getConfig(): Promise<ApiResponse<SystemConfig>> {
    return apiClient.get<SystemConfig>('/system/config');
  },

  /**
   * 更新系统配置
   * @param config 配置数据
   */
  async updateConfig(config: Partial<SystemConfig>): Promise<ApiResponse> {
    return apiClient.put('/system/config', config);
  },

  /**
   * 获取系统日志
   * @param params 过滤参数
   */
  async getLogs(params?: {
    level?: string;
    module?: string;
    start_time?: string;
    end_time?: string;
    limit?: number;
    offset?: number;
  }): Promise<ApiResponse<{ logs: LogEntry[]; total: number }>> {
    return apiClient.get<{ logs: LogEntry[]; total: number }>('/system/logs', { params });
  },

  /**
   * 重启系统服务
   */
  async restartSystem(): Promise<ApiResponse> {
    return apiClient.post('/system/restart');
  },
}; 