import { apiClient, ApiResponse } from './client';

// 插件信息接口
export interface Plugin {
  id: number;
  name: string;
  description?: string;
  path: string;
  is_enabled: boolean;
  version?: string;
  author?: string;
  created_at: string;
  updated_at: string;
  config?: Record<string, any>;
}

// 插件配置接口
export interface PluginConfig {
  id: number;
  plugin_id: number;
  key: string;
  value: any;
  description?: string;
  type: 'string' | 'number' | 'boolean' | 'json';
}

// 插件API服务
export const PluginService = {
  /**
   * 获取插件列表
   */
  async getPlugins(): Promise<ApiResponse<Plugin[]>> {
    return apiClient.get<Plugin[]>('/plugins');
  },

  /**
   * 获取单个插件详情
   * @param id 插件ID
   */
  async getPlugin(id: number): Promise<ApiResponse<Plugin>> {
    return apiClient.get<Plugin>(`/plugins/${id}`);
  },

  /**
   * 启用插件
   * @param id 插件ID
   */
  async enablePlugin(id: number): Promise<ApiResponse> {
    return apiClient.post(`/plugins/${id}/enable`);
  },

  /**
   * 禁用插件
   * @param id 插件ID
   */
  async disablePlugin(id: number): Promise<ApiResponse> {
    return apiClient.post(`/plugins/${id}/disable`);
  },

  /**
   * 获取插件配置
   * @param id 插件ID
   */
  async getPluginConfig(id: number): Promise<ApiResponse<Record<string, any>>> {
    return apiClient.get<Record<string, any>>(`/plugins/${id}/config`);
  },

  /**
   * 更新插件配置
   * @param id 插件ID
   * @param config 配置数据
   */
  async updatePluginConfig(id: number, config: Record<string, any>): Promise<ApiResponse> {
    return apiClient.put(`/plugins/${id}/config`, config);
  },

  /**
   * 扫描插件目录，查找新插件
   */
  async scanPlugins(): Promise<ApiResponse<Plugin[]>> {
    return apiClient.post<Plugin[]>('/plugins/scan');
  },

  /**
   * 重新加载所有插件
   */
  async reloadPlugins(): Promise<ApiResponse> {
    return apiClient.post('/plugins/reload');
  },
}; 