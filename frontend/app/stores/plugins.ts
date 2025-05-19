import { create } from 'zustand';
import { Plugin, PluginService } from '../api/plugins';

// 插件状态接口
interface PluginState {
  // 状态
  plugins: Plugin[];
  selectedPlugin: Plugin | null;
  isLoading: boolean;
  error: string | null;

  // 操作
  fetchPlugins: () => Promise<void>;
  selectPlugin: (id: number) => void;
  enablePlugin: (id: number) => Promise<boolean>;
  disablePlugin: (id: number) => Promise<boolean>;
  getPluginConfig: (id: number) => Promise<Record<string, any> | null>;
  updatePluginConfig: (id: number, config: Record<string, any>) => Promise<boolean>;
  scanPlugins: () => Promise<void>;
  reloadPlugins: () => Promise<boolean>;
  setError: (error: string | null) => void;
}

// 创建插件状态存储
export const usePluginStore = create<PluginState>((set, get) => ({
  // 初始状态
  plugins: [],
  selectedPlugin: null,
  isLoading: false,
  error: null,

  // 获取所有插件
  fetchPlugins: async () => {
    try {
      set({ isLoading: true, error: null });
      const response = await PluginService.getPlugins();
      
      if (response.success && response.data) {
        set({ 
          plugins: response.data, 
          isLoading: false 
        });
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '获取插件列表失败' 
        });
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '获取插件列表过程中发生错误' 
      });
    }
  },

  // 选择插件
  selectPlugin: (id: number) => {
    const { plugins } = get();
    const plugin = plugins.find(p => p.id === id) || null;
    set({ selectedPlugin: plugin });
  },

  // 启用插件
  enablePlugin: async (id: number) => {
    try {
      set({ isLoading: true, error: null });
      const response = await PluginService.enablePlugin(id);
      
      if (response.success) {
        // 更新插件状态
        set(state => ({
          plugins: state.plugins.map(plugin => 
            plugin.id === id 
              ? { ...plugin, is_enabled: true } 
              : plugin
          ),
          isLoading: false
        }));
        return true;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '启用插件失败' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '启用插件过程中发生错误' 
      });
      return false;
    }
  },

  // 禁用插件
  disablePlugin: async (id: number) => {
    try {
      set({ isLoading: true, error: null });
      const response = await PluginService.disablePlugin(id);
      
      if (response.success) {
        // 更新插件状态
        set(state => ({
          plugins: state.plugins.map(plugin => 
            plugin.id === id 
              ? { ...plugin, is_enabled: false } 
              : plugin
          ),
          isLoading: false
        }));
        return true;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '禁用插件失败' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '禁用插件过程中发生错误' 
      });
      return false;
    }
  },

  // 获取插件配置
  getPluginConfig: async (id: number) => {
    try {
      set({ isLoading: true, error: null });
      const response = await PluginService.getPluginConfig(id);
      
      if (response.success && response.data) {
        set({ isLoading: false });
        return response.data;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '获取插件配置失败' 
        });
        return null;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '获取插件配置过程中发生错误' 
      });
      return null;
    }
  },

  // 更新插件配置
  updatePluginConfig: async (id: number, config: Record<string, any>) => {
    try {
      set({ isLoading: true, error: null });
      const response = await PluginService.updatePluginConfig(id, config);
      
      if (response.success) {
        set({ isLoading: false });
        return true;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '更新插件配置失败' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '更新插件配置过程中发生错误' 
      });
      return false;
    }
  },

  // 扫描插件
  scanPlugins: async () => {
    try {
      set({ isLoading: true, error: null });
      const response = await PluginService.scanPlugins();
      
      if (response.success && response.data) {
        set({ 
          plugins: response.data, 
          isLoading: false 
        });
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '扫描插件失败' 
        });
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '扫描插件过程中发生错误' 
      });
    }
  },

  // 重新加载插件
  reloadPlugins: async () => {
    try {
      set({ isLoading: true, error: null });
      const response = await PluginService.reloadPlugins();
      
      if (response.success) {
        // 重新获取插件列表
        await get().fetchPlugins();
        return true;
      } else {
        set({ 
          isLoading: false, 
          error: response.message || '重新加载插件失败' 
        });
        return false;
      }
    } catch (error) {
      set({ 
        isLoading: false, 
        error: error instanceof Error ? error.message : '重新加载插件过程中发生错误' 
      });
      return false;
    }
  },

  // 设置错误
  setError: (error: string | null) => set({ error }),
})); 