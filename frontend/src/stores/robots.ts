import { create } from 'zustand';
import { Robot, CreateRobotRequest, RobotService } from '../api/robots';

// 机器人状态接口
interface RobotState {
  // 状态
  robots: Robot[];
  selectedRobot: Robot | null;
  isLoading: boolean;
  error: string | null;

  // 操作
  fetchRobots: () => Promise<void>;
  selectRobot: (id: number) => void;
  createRobot: (data: CreateRobotRequest) => Promise<Robot | null>;
  deleteRobot: (id: number) => Promise<boolean>;
  loginRobot: (id: number) => Promise<boolean>;
  logoutRobot: (id: number) => Promise<boolean>;
  getQrcode: (id: number) => Promise<string | null>;
  checkLoginStatus: (id: number) => Promise<void>;
  setError: (error: string | null) => void;
}

// 创建机器人状态存储
export const useRobotStore = create<RobotState>((set, get) => ({
  // 初始状态
  robots: [],
  selectedRobot: null,
  isLoading: false,
  error: null,

  // 获取所有机器人
  fetchRobots: async () => {
    try {
      set({ isLoading: true, error: null });
      const response = await RobotService.getRobots();
      
      if (response.success && response.data) {
        set({ 
          robots: response.data, 
          isLoading: false 
        });
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '获取机器人列表失败' 
        });
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '获取机器人列表过程中发生错误' 
      });
    }
  },

  // 选择机器人
  selectRobot: (id: number) => {
    const { robots } = get();
    const robot = robots.find(r => r.id === id) || null;
    set({ selectedRobot: robot });
  },

  // 创建机器人
  createRobot: async (data: CreateRobotRequest) => {
    try {
      set({ isLoading: true, error: null });
      const response = await RobotService.createRobot(data);
      
      if (response.success && response.data) {
        const newRobot = response.data;
        set(state => ({ 
          robots: [...state.robots, newRobot], 
          isLoading: false 
        }));
        return newRobot;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '创建机器人失败' 
        });
        return null;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '创建机器人过程中发生错误' 
      });
      return null;
    }
  },

  // 删除机器人
  deleteRobot: async (id: number) => {
    try {
      set({ isLoading: true, error: null });
      const response = await RobotService.deleteRobot(id);
      
      if (response.success) {
        set(state => ({
          robots: state.robots.filter(r => r.id !== id),
          selectedRobot: state.selectedRobot?.id === id ? null : state.selectedRobot,
          isLoading: false
        }));
        return true;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '删除机器人失败' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '删除机器人过程中发生错误' 
      });
      return false;
    }
  },

  // 登录机器人
  loginRobot: async (id: number) => {
    try {
      set({ isLoading: true, error: null });
      const response = await RobotService.loginRobot(id);
      
      if (response.success) {
        // 更新机器人状态
        await get().fetchRobots();
        return true;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '登录机器人失败' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '登录机器人过程中发生错误' 
      });
      return false;
    }
  },

  // 登出机器人
  logoutRobot: async (id: number) => {
    try {
      set({ isLoading: true, error: null });
      const response = await RobotService.logoutRobot(id);
      
      if (response.success) {
        // 更新机器人状态
        await get().fetchRobots();
        return true;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '登出机器人失败' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '登出机器人过程中发生错误' 
      });
      return false;
    }
  },

  // 获取登录二维码
  getQrcode: async (id: number) => {
    try {
      set({ isLoading: true, error: null });
      const response = await RobotService.getLoginQrcode(id);
      
      if (response.success && response.data) {
        set({ isLoading: false });
        return response.data.qrcode;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '获取登录二维码失败' 
        });
        return null;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '获取登录二维码过程中发生错误' 
      });
      return null;
    }
  },

  // 检查登录状态
  checkLoginStatus: async (id: number) => {
    try {
      const response = await RobotService.checkLoginStatus(id);
      
      if (response.success && response.data) {
        // 更新机器人状态
        const { robots } = get();
        const updatedRobots = robots.map(robot => 
          robot.id === id 
            ? { ...robot, status: response.data.is_logged_in ? 'online' : 'offline' } 
            : robot
        );
        
        set({ robots: updatedRobots });
      }
    } catch (error) {
      console.error('检查登录状态失败:', error);
    }
  },

  // 设置错误
  setError: (error: string | null) => set({ error }),
})); 