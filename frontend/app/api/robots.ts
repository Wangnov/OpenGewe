import { apiClient, ApiResponse } from './client';

// 机器人信息接口
export interface Robot {
  id: number;
  name: string;
  app_id: string;
  wxid?: string;
  status: 'online' | 'offline' | 'logging' | 'error';
  last_login_time?: string;
  created_at: string;
  qrcode?: string;
  uuid?: string;
  login_url?: string;
}

// 创建机器人请求
export interface CreateRobotRequest {
  name: string;
  app_id?: string;
}

// 消息发送请求
export interface SendMessageRequest {
  robot_id: number;
  to_wxid: string;
  message_type: 'text' | 'image' | 'file' | 'voice' | 'video' | 'link';
  content: string;
  extra?: Record<string, any>; // 不同消息类型的额外参数
}

// 机器人API服务
export const RobotService = {
  /**
   * 获取机器人列表
   */
  async getRobots(): Promise<ApiResponse<Robot[]>> {
    return apiClient.get<Robot[]>('/robots');
  },

  /**
   * 获取单个机器人详情
   * @param id 机器人ID
   */
  async getRobot(id: number): Promise<ApiResponse<Robot>> {
    return apiClient.get<Robot>(`/robots/${id}`);
  },

  /**
   * 创建新机器人
   * @param data 机器人信息
   */
  async createRobot(data: CreateRobotRequest): Promise<ApiResponse<Robot>> {
    return apiClient.post<Robot>('/robots/create', data);
  },

  /**
   * 删除机器人
   * @param id 机器人ID
   */
  async deleteRobot(id: number): Promise<ApiResponse> {
    return apiClient.delete(`/robots/${id}`);
  },

  /**
   * 获取机器人登录二维码
   * @param id 机器人ID
   */
  async getLoginQrcode(id: number): Promise<ApiResponse<{ qrcode: string, uuid: string }>> {
    return apiClient.get<{ qrcode: string, uuid: string }>(`/robots/${id}/qrcode`);
  },

  /**
   * 检查机器人登录状态
   * @param id 机器人ID
   */
  async checkLoginStatus(id: number): Promise<ApiResponse<{ status: string, is_logged_in: boolean }>> {
    return apiClient.get<{ status: string, is_logged_in: boolean }>(`/robots/${id}/status`);
  },

  /**
   * 登录机器人
   * @param id 机器人ID
   */
  async loginRobot(id: number): Promise<ApiResponse> {
    return apiClient.post(`/robots/${id}/login`);
  },

  /**
   * 登出机器人
   * @param id 机器人ID
   */
  async logoutRobot(id: number): Promise<ApiResponse> {
    return apiClient.post(`/robots/${id}/logout`);
  },

  /**
   * 发送消息
   * @param data 消息数据
   */
  async sendMessage(data: SendMessageRequest): Promise<ApiResponse> {
    return apiClient.post('/robots/send', data);
  },
}; 