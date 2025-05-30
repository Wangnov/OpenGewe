/**
 * 通知本地存储工具
 * 提供通知数据的持久化存储功能
 */

// 存储键名常量
const STORAGE_KEYS = {
    NOTIFICATIONS: 'opengewe_notifications',
    SETTINGS: 'opengewe_notification_settings',
    LAST_CLEANUP: 'opengewe_notification_last_cleanup'
};

// 默认设置
const DEFAULT_SETTINGS = {
    maxHistoryCount: 100,          // 最大历史记录数量
    autoCleanupDays: 7,           // 自动清理天数
    enableSound: false,           // 启用声音提醒
    enableDesktop: false,         // 启用桌面通知
    defaultDuration: 5000,        // 默认显示时长(ms)
    position: 'top-center'        // 显示位置
};

/**
 * 通知存储API
 */
const notificationStorage = {
    /**
     * 保存通知列表到本地存储
     * @param {Array} notifications - 通知列表
     */
    saveNotifications: (notifications) => {
        try {
            const data = {
                notifications: notifications,
                timestamp: Date.now()
            };
            localStorage.setItem(STORAGE_KEYS.NOTIFICATIONS, JSON.stringify(data));
        } catch (error) {
            console.error('保存通知失败:', error);
        }
    },

    /**
     * 从本地存储加载通知列表
     * @returns {Array} 通知列表
     */
    loadNotifications: () => {
        try {
            const stored = localStorage.getItem(STORAGE_KEYS.NOTIFICATIONS);
            if (!stored) return [];

            const data = JSON.parse(stored);
            return Array.isArray(data.notifications) ? data.notifications : [];
        } catch (error) {
            console.error('加载通知失败:', error);
            return [];
        }
    },

    /**
     * 保存通知设置
     * @param {Object} settings - 设置对象
     */
    saveSettings: (settings) => {
        try {
            const mergedSettings = { ...DEFAULT_SETTINGS, ...settings };
            localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(mergedSettings));
        } catch (error) {
            console.error('保存设置失败:', error);
        }
    },

    /**
     * 加载通知设置
     * @returns {Object} 设置对象
     */
    loadSettings: () => {
        try {
            const stored = localStorage.getItem(STORAGE_KEYS.SETTINGS);
            if (!stored) return DEFAULT_SETTINGS;

            return { ...DEFAULT_SETTINGS, ...JSON.parse(stored) };
        } catch (error) {
            console.error('加载设置失败:', error);
            return DEFAULT_SETTINGS;
        }
    },

    /**
     * 清理过期通知
     * @param {number} days - 保留天数
     */
    clearExpired: (days = 7) => {
        try {
            const notifications = notificationStorage.loadNotifications();
            const cutoffTime = Date.now() - (days * 24 * 60 * 60 * 1000);

            const validNotifications = notifications.filter(notification => {
                const notificationTime = new Date(notification.timestamp).getTime();
                return notificationTime > cutoffTime;
            });

            notificationStorage.saveNotifications(validNotifications);
            localStorage.setItem(STORAGE_KEYS.LAST_CLEANUP, Date.now().toString());

            return notifications.length - validNotifications.length; // 返回清理数量
        } catch (error) {
            console.error('清理过期通知失败:', error);
            return 0;
        }
    },

    /**
     * 检查是否需要自动清理
     * @returns {boolean} 是否需要清理
     */
    shouldAutoCleanup: () => {
        try {
            const lastCleanup = parseInt(localStorage.getItem(STORAGE_KEYS.LAST_CLEANUP) || '0');
            const daysSinceCleanup = (Date.now() - lastCleanup) / (24 * 60 * 60 * 1000);
            return daysSinceCleanup >= 1; // 每天检查一次
        } catch (error) {
            return true;
        }
    },

    /**
     * 获取存储使用情况
     * @returns {Object} 存储信息
     */
    getStorageInfo: () => {
        try {
            const notifications = notificationStorage.loadNotifications();
            const settings = notificationStorage.loadSettings();

            return {
                notificationCount: notifications.length,
                storageSize: new Blob([JSON.stringify(notifications)]).size,
                settings: settings,
                lastCleanup: parseInt(localStorage.getItem(STORAGE_KEYS.LAST_CLEANUP) || '0')
            };
        } catch (error) {
            console.error('获取存储信息失败:', error);
            return {
                notificationCount: 0,
                storageSize: 0,
                settings: DEFAULT_SETTINGS,
                lastCleanup: 0
            };
        }
    },

    /**
     * 清空所有通知数据
     */
    clearAll: () => {
        try {
            localStorage.removeItem(STORAGE_KEYS.NOTIFICATIONS);
            localStorage.removeItem(STORAGE_KEYS.LAST_CLEANUP);
        } catch (error) {
            console.error('清空通知数据失败:', error);
        }
    },

    /**
     * 导出通知数据
     * @returns {Object} 导出的数据
     */
    exportData: () => {
        try {
            return {
                notifications: notificationStorage.loadNotifications(),
                settings: notificationStorage.loadSettings(),
                exportTime: Date.now()
            };
        } catch (error) {
            console.error('导出数据失败:', error);
            return null;
        }
    },

    /**
     * 导入通知数据
     * @param {Object} data - 导入的数据
     * @returns {boolean} 导入是否成功
     */
    importData: (data) => {
        try {
            if (data.notifications && Array.isArray(data.notifications)) {
                notificationStorage.saveNotifications(data.notifications);
            }
            if (data.settings && typeof data.settings === 'object') {
                notificationStorage.saveSettings(data.settings);
            }
            return true;
        } catch (error) {
            console.error('导入数据失败:', error);
            return false;
        }
    }
};

// 初始化时自动清理过期数据
if (notificationStorage.shouldAutoCleanup()) {
    notificationStorage.clearExpired();
}

export default notificationStorage; 