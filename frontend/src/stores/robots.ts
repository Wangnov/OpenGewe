import { create } from 'zustand';
import { apiClient } from '../api/client';

// 机器人状态
export type RobotStatus = 'online' | 'offline' | 'logging';

// 机器人类型定义
export interface Robot {
  id: number;
  name: string;
  app_id: string;
  status: RobotStatus;
  created_at: string;
  updated_at: string;
}

// 机器人状态接口
interface RobotState {
  robots: Robot[];
  isLoading: boolean;
  error: string | null;
  fetchRobots: () => Promise<void>;
  createRobot: (data: { name: string; app_id?: string }) => Promise<Robot | null>;
  deleteRobot: (id: number) => Promise<boolean>;
  loginRobot: (id: number) => Promise<boolean>;
  logoutRobot: (id: number) => Promise<boolean>;
}

// 创建机器人状态存储
export const useRobotStore = create<RobotState>((set, get) => ({
  robots: [],
  isLoading: false,
  error: null,

  // 获取机器人列表
  fetchRobots: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get('/robots');
      if (response.success && response.data) {
        set({ robots: response.data.robots || [] });
      } else {
        set({ error: response.message || '获取机器人列表失败' });
      }
    } catch (error) {
      set({ error: '获取机器人列表失败，请检查网络连接' });
      console.error('获取机器人列表错误:', error);
    } finally {
      set({ isLoading: false });
    }
  },

  // 创建机器人
  createRobot: async (data) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post('/robots/create', data);
      if (response.success && response.data) {
        const newRobot = response.data.robot;
        set((state) => ({
          robots: [...state.robots, newRobot],
        }));
        return newRobot;
      } else {
        set({ error: response.message || '创建机器人失败' });
        return null;
      }
    } catch (error) {
      set({ error: '创建机器人失败，请检查网络连接' });
      console.error('创建机器人错误:', error);
      return null;
    } finally {
      set({ isLoading: false });
    }
  },

  // 删除机器人
  deleteRobot: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.delete(`/robots/${id}`);
      if (response.success) {
        set((state) => ({
          robots: state.robots.filter(robot => robot.id !== id),
        }));
        return true;
      } else {
        set({ error: response.message || '删除机器人失败' });
        return false;
      }
    } catch (error) {
      set({ error: '删除机器人失败，请检查网络连接' });
      console.error('删除机器人错误:', error);
      return false;
    } finally {
      set({ isLoading: false });
    }
  },

  // 登录机器人
  loginRobot: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post(`/robots/${id}/login`);
      if (response.success) {
        set((state) => ({
          robots: state.robots.map(robot => 
            robot.id === id ? { ...robot, status: 'online' } : robot
          ),
        }));
        return true;
      } else {
        set({ error: response.message || '登录机器人失败' });
        return false;
      }
    } catch (error) {
      set({ error: '登录机器人失败，请检查网络连接' });
      console.error('登录机器人错误:', error);
      return false;
    } finally {
      set({ isLoading: false });
    }
  },

  // 登出机器人
  logoutRobot: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post(`/robots/${id}/logout`);
      if (response.success) {
        set((state) => ({
          robots: state.robots.map(robot => 
            robot.id === id ? { ...robot, status: 'offline' } : robot
          ),
        }));
        return true;
      } else {
        set({ error: response.message || '登出机器人失败' });
        return false;
      }
    } catch (error) {
      set({ error: '登出机器人失败，请检查网络连接' });
      console.error('登出机器人错误:', error);
      return false;
    } finally {
      set({ isLoading: false });
    }
  },
})); 