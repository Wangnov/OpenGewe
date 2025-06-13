/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useState, useEffect, useCallback, useMemo } from 'react';
import notificationStorage from '../utils/notificationStorage';

// 通知类型常量
export const NotificationType = {
    SUCCESS: 'success',
    WARNING: 'warning',
    ERROR: 'error',
    INFO: 'info',
    SYSTEM: 'system'
};

// 通知优先级常量
export const NotificationPriority = {
    HIGH: 'high',
    MEDIUM: 'medium',
    LOW: 'low'
};

// 创建通知上下文
export const NotificationContext = createContext();

/**
 * 生成唯一ID
 * @returns {string} 唯一ID
 */
const generateId = () => {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

/**
 * 创建通知对象
 * @param {Object} notification - 通知配置
 * @returns {Object} 完整的通知对象
 */
const createNotification = (notification) => {
    const settings = notificationStorage.loadSettings();

    // 根据通知类型设置默认的已读状态
    const defaultIsRead = notification.type === NotificationType.SUCCESS ||
        notification.type === NotificationType.INFO ||
        notification.type === NotificationType.SYSTEM;

    return {
        id: generateId(),
        type: notification.type || NotificationType.INFO,
        title: notification.title || '通知',
        message: notification.message || '',
        duration: notification.duration !== undefined ? notification.duration : settings.defaultDuration,
        priority: notification.priority || NotificationPriority.MEDIUM,
        isRead: notification.isRead !== undefined ? notification.isRead : defaultIsRead,
        isPinned: notification.isPinned || false,
        timestamp: new Date().toISOString(),
        actions: notification.actions || [],
        metadata: notification.metadata || {},
        ...notification
    };
};

/**
 * 通知上下文提供者组件
 * @param {Object} props - 组件属性
 * @param {React.ReactNode} props.children - 子组件
 */
export const NotificationProvider = ({ children }) => {
    // 当前显示的通知列表
    const [notifications, setNotifications] = useState([]);
    // 历史通知列表
    const [history, setHistory] = useState([]);
    // 是否显示通知栏
    const [showBar, setShowBar] = useState(false);
    // 是否显示历史弹窗
    const [showHistory, setShowHistory] = useState(false);
    // 通知设置
    const [settings, setSettings] = useState(() => notificationStorage.loadSettings());

    // 计算未读数量
    const unreadCount = useMemo(() => {
        return history.filter(notification => !notification.isRead).length;
    }, [history]);

    // 初始化时加载历史通知
    useEffect(() => {
        const savedHistory = notificationStorage.loadNotifications();
        setHistory(savedHistory);
    }, []);

    // 保存历史通知到本地存储
    useEffect(() => {
        if (history.length > 0) {
            notificationStorage.saveNotifications(history);
        }
    }, [history]);

    // 自动隐藏通知栏
    useEffect(() => {
        if (notifications.length === 0) {
            setShowBar(false);
        } else if (notifications.length > 0 && !showBar) {
            setShowBar(true);
        }
    }, [notifications.length, showBar]);

    /**
     * 添加通知
     * @param {Object} notification - 通知配置
     * @returns {string} 通知ID
     */
    /**
     * 移除通知
     * @param {string} id - 通知ID
     */
    const removeNotification = useCallback((id) => {
        // 不立即移除，而是等待动画完成
        // 让组件自己处理移除逻辑
        setTimeout(() => {
            setNotifications(prev => prev.filter(notification => notification.id !== id));
        }, 600); // 给动画充足的时间（0.5s动画 + 0.1s缓冲）
    }, []);

    /**
     * 添加通知
     * @param {Object} notification - 通知配置
     * @returns {string} 通知ID
     */
    const addNotification = useCallback((notification) => {
        const newNotification = createNotification(notification);

        // 添加到当前通知列表
        setNotifications(prev => {
            // 检查是否已存在相同的通知（基于内容）
            const exists = prev.some(n =>
                n.title === newNotification.title &&
                n.message === newNotification.message &&
                n.type === newNotification.type
            );

            if (exists) {
                return prev; // 避免重复通知
            }

            // 根据优先级排序
            const updated = [...prev, newNotification];
            return updated.sort((a, b) => {
                const priorityOrder = { high: 3, medium: 2, low: 1 };
                return priorityOrder[b.priority] - priorityOrder[a.priority];
            });
        });

        // 添加到历史记录
        setHistory(prev => {
            const updated = [newNotification, ...prev];
            // 限制历史记录数量
            return updated.slice(0, settings.maxHistoryCount);
        });

        // 设置自动移除定时器
        if (newNotification.duration > 0) {
            setTimeout(() => {
                removeNotification(newNotification.id);
            }, newNotification.duration);
        }

        return newNotification.id;
    }, [removeNotification, settings.maxHistoryCount]);

    /**
     * 标记通知为已读
     * @param {string} id - 通知ID
     */
    const markAsRead = useCallback((id) => {
        setHistory(prev =>
            prev.map(notification =>
                notification.id === id
                    ? { ...notification, isRead: true }
                    : notification
            )
        );
    }, []);

    /**
     * 标记所有通知为已读
     */
    const markAllAsRead = useCallback(() => {
        setHistory(prev =>
            prev.map(notification => ({ ...notification, isRead: true }))
        );
    }, []);

    /**
     * 清空当前通知
     */
    const clearCurrent = useCallback(() => {
        setNotifications([]);
    }, []);

    /**
     * 清空所有通知
     */
    const clearAll = useCallback(() => {
        setNotifications([]);
        setHistory([]);
        notificationStorage.clearAll();
    }, []);

    /**
     * 切换历史弹窗显示状态
     */
    const toggleHistory = useCallback(() => {
        setShowHistory(prev => !prev);
    }, []);

    /**
     * 置顶/取消置顶通知
     * @param {string} id - 通知ID
     */
    const togglePin = useCallback((id) => {
        setHistory(prev =>
            prev.map(notification =>
                notification.id === id
                    ? { ...notification, isPinned: !notification.isPinned }
                    : notification
            )
        );
    }, []);

    /**
     * 删除历史通知
     * @param {string} id - 通知ID
     */
    const deleteFromHistory = useCallback((id) => {
        setHistory(prev => prev.filter(notification => notification.id !== id));
    }, []);

    /**
     * 更新设置
     * @param {Object} newSettings - 新设置
     */
    const updateSettings = useCallback((newSettings) => {
        const updatedSettings = { ...settings, ...newSettings };
        setSettings(updatedSettings);
        notificationStorage.saveSettings(updatedSettings);
    }, [settings]);

    /**
     * 快捷方法：添加成功通知
     */
    const success = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.SUCCESS,
            title,
            message,
            ...options
        });
    }, [addNotification]);

    /**
     * 快捷方法：添加警告通知
     */
    const warning = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.WARNING,
            title,
            message,
            duration: 0, // 警告默认不自动消失
            ...options
        });
    }, [addNotification]);

    /**
     * 快捷方法：添加错误通知
     */
    const error = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.ERROR,
            title,
            message,
            duration: 0, // 错误默认不自动消失
            priority: NotificationPriority.HIGH,
            ...options
        });
    }, [addNotification]);

    /**
     * 快捷方法：添加信息通知
     */
    const info = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.INFO,
            title,
            message,
            ...options
        });
    }, [addNotification]);

    /**
     * 快捷方法：添加系统通知
     */
    const system = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.SYSTEM,
            title,
            message,
            priority: NotificationPriority.HIGH,
            ...options
        });
    }, [addNotification]);

    // 上下文值
    const value = useMemo(() => ({
        // 状态
        notifications,
        history,
        unreadCount,
        showBar,
        showHistory,
        settings,

        // 方法
        addNotification,
        removeNotification,
        markAsRead,
        markAllAsRead,
        clearCurrent,
        clearAll,
        toggleHistory,
        togglePin,
        deleteFromHistory,
        updateSettings,

        // 快捷方法
        success,
        warning,
        error,
        info,
        system
    }), [
        notifications,
        history,
        unreadCount,
        showBar,
        showHistory,
        settings,
        addNotification,
        removeNotification,
        markAsRead,
        markAllAsRead,
        clearCurrent,
        clearAll,
        toggleHistory,
        togglePin,
        deleteFromHistory,
        updateSettings,
        success,
        warning,
        error,
        info,
        system
    ]);

    return (
        <NotificationContext.Provider value={value}>
            {children}
        </NotificationContext.Provider>
    );
}; 