import { create } from 'zustand';
import { SystemStatus, SystemConfig, LogEntry, SystemService } from '../api/system';

// 系统状态接口
interface SystemState {
  // 状态
  status: SystemStatus | null;
  config: SystemConfig | null;
  logs: LogEntry[];
  totalLogs: number;
  isLoading: boolean;
  error: string | null;

  // 操作
  fetchStatus: () => Promise<void>;
  fetchConfig: () => Promise<void>;
  updateConfig: (config: Partial<SystemConfig>) => Promise<boolean>;
  fetchLogs: (params?: {
    level?: string;
    module?: string;
    start_time?: string;
    end_time?: string;
    limit?: number;
    offset?: number;
  }) => Promise<void>;
  restartSystem: () => Promise<boolean>;
  setError: (error: string | null) => void;
}

// 创建系统状态存储
export const useSystemStore = create<SystemState>((set) => ({
  // 初始状态
  status: null,
  config: null,
  logs: [],
  totalLogs: 0,
  isLoading: false,
  error: null,

  // 获取系统状态
  fetchStatus: async () => {
    try {
      set({ isLoading: true, error: null });
      const response = await SystemService.getStatus();
      
      if (response.success && response.data) {
        set({ 
          status: response.data, 
          isLoading: false 
        });
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '获取系统状态失败' 
        });
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '获取系统状态过程中发生错误' 
      });
    }
  },

  // 获取系统配置
  fetchConfig: async () => {
    try {
      set({ isLoading: true, error: null });
      const response = await SystemService.getConfig();
      
      if (response.success && response.data) {
        set({ 
          config: response.data, 
          isLoading: false 
        });
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '获取系统配置失败' 
        });
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '获取系统配置过程中发生错误' 
      });
    }
  },

  // 更新系统配置
  updateConfig: async (config: Partial<SystemConfig>) => {
    try {
      set({ isLoading: true, error: null });
      const response = await SystemService.updateConfig(config);
      
      if (response.success) {
        // 更新配置后刷新数据
        const configResponse = await SystemService.getConfig();
        if (configResponse.success && configResponse.data) {
          set({ 
            config: configResponse.data,
            isLoading: false 
          });
        } else {
          set({ isLoading: false });
        }
        return true;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '更新系统配置失败' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '更新系统配置过程中发生错误' 
      });
      return false;
    }
  },

  // 获取系统日志
  fetchLogs: async (params) => {
    try {
      set({ isLoading: true, error: null });
      const response = await SystemService.getLogs(params);
      
      if (response.success && response.data) {
        set({ 
          logs: response.data.logs, 
          totalLogs: response.data.total,
          isLoading: false 
        });
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '获取系统日志失败' 
        });
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '获取系统日志过程中发生错误' 
      });
    }
  },

  // 重启系统
  restartSystem: async () => {
    try {
      set({ isLoading: true, error: null });
      const response = await SystemService.restartSystem();
      
      if (response.success) {
        set({ isLoading: false });
        return true;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '重启系统失败' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '重启系统过程中发生错误' 
      });
      return false;
    }
  },

  // 设置错误
  setError: (error: string | null) => set({ error }),
})); 