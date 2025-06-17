import React, { createContext, useReducer, useCallback, useEffect, useMemo, useRef } from 'react';
import { notificationService } from '../services/notificationService';
import { notificationQueue } from '../utils/notificationQueue';

// 通知类型
export const NotificationType = {
    SUCCESS: 'success',
    WARNING: 'warning',
    ERROR: 'error',
    INFO: 'info',
    SYSTEM: 'system'
};

// 通知优先级
export const NotificationPriority = {
    HIGH: 'high',
    MEDIUM: 'medium',
    LOW: 'low'
};

// Action 类型
const ActionTypes = {
    ADD_NOTIFICATION: 'ADD_NOTIFICATION',
    REMOVE_NOTIFICATION: 'REMOVE_NOTIFICATION',
    UPDATE_NOTIFICATION: 'UPDATE_NOTIFICATION',
    MARK_AS_READ: 'MARK_AS_READ',
    MARK_ALL_AS_READ: 'MARK_ALL_AS_READ',
    TOGGLE_PIN: 'TOGGLE_PIN',
    DELETE_FROM_HISTORY: 'DELETE_FROM_HISTORY',
    CLEAR_CURRENT: 'CLEAR_CURRENT',
    CLEAR_ALL: 'CLEAR_ALL',
    SET_HISTORY: 'SET_HISTORY',
    UPDATE_SETTINGS: 'UPDATE_SETTINGS',
    SET_UI_STATE: 'SET_UI_STATE'
};

// 初始状态
const initialState = {
    // 当前显示的通知
    activeNotifications: [],
    // 历史通知
    history: [],
    // 用户设置
    settings: {
        maxHistoryCount: 100,
        autoCleanupDays: 7,
        enableSound: false,
        enableDesktop: false,
        defaultDuration: 5000,
        position: 'top-right',
        animationDuration: 300
    },
    // UI 状态
    ui: {
        showHistory: false,
        filter: 'all',
        sortBy: 'newest',
        isLoading: false
    }
};

// Reducer
function notificationReducer(state, action) {
    switch (action.type) {
        case ActionTypes.ADD_NOTIFICATION: {
            const { notification } = action.payload;
            const newActive = notificationQueue.add(state.activeNotifications, notification);
            const newHistory = [notification, ...state.history].slice(0, state.settings.maxHistoryCount);

            return {
                ...state,
                activeNotifications: newActive,
                history: newHistory
            };
        }

        case ActionTypes.REMOVE_NOTIFICATION: {
            const { id } = action.payload;
            return {
                ...state,
                activeNotifications: state.activeNotifications.filter(n => n.id !== id)
            };
        }

        case ActionTypes.UPDATE_NOTIFICATION: {
            const { id, updates } = action.payload;
            return {
                ...state,
                activeNotifications: state.activeNotifications.map(n =>
                    n.id === id ? { ...n, ...updates } : n
                ),
                history: state.history.map(n =>
                    n.id === id ? { ...n, ...updates } : n
                )
            };
        }

        case ActionTypes.MARK_AS_READ: {
            const { id } = action.payload;
            return {
                ...state,
                history: state.history.map(n =>
                    n.id === id ? { ...n, isRead: true } : n
                )
            };
        }

        case ActionTypes.MARK_ALL_AS_READ: {
            return {
                ...state,
                history: state.history.map(n => ({ ...n, isRead: true }))
            };
        }

        case ActionTypes.TOGGLE_PIN: {
            const { id } = action.payload;
            return {
                ...state,
                history: state.history.map(n =>
                    n.id === id ? { ...n, isPinned: !n.isPinned } : n
                )
            };
        }

        case ActionTypes.DELETE_FROM_HISTORY: {
            const { id } = action.payload;
            return {
                ...state,
                history: state.history.filter(n => n.id !== id)
            };
        }

        case ActionTypes.CLEAR_CURRENT: {
            return {
                ...state,
                activeNotifications: []
            };
        }

        case ActionTypes.CLEAR_ALL: {
            return {
                ...state,
                activeNotifications: [],
                history: []
            };
        }

        case ActionTypes.SET_HISTORY: {
            const { history } = action.payload;
            return {
                ...state,
                history
            };
        }

        case ActionTypes.UPDATE_SETTINGS: {
            const { settings } = action.payload;
            return {
                ...state,
                settings: { ...state.settings, ...settings }
            };
        }

        case ActionTypes.SET_UI_STATE: {
            const { ui } = action.payload;
            return {
                ...state,
                ui: { ...state.ui, ...ui }
            };
        }

        default:
            return state;
    }
}

// Context
export const NotificationContext = createContext(null);

// Provider
export function NotificationProvider({ children }) {
    const [state, dispatch] = useReducer(notificationReducer, initialState);
    const saveTimeoutRef = useRef(null);

    // 计算派生状态
    const unreadCount = useMemo(() =>
        state.history.filter(n => !n.isRead).length,
        [state.history]
    );

    const pinnedCount = useMemo(() =>
        state.history.filter(n => n.isPinned).length,
        [state.history]
    );

    // 初始化：加载历史记录
    useEffect(() => {
        const loadData = async () => {
            dispatch({ type: ActionTypes.SET_UI_STATE, payload: { ui: { isLoading: true } } });

            try {
                const [history, settings] = await Promise.all([
                    notificationService.loadNotifications(),
                    notificationService.loadSettings()
                ]);

                dispatch({ type: ActionTypes.SET_HISTORY, payload: { history } });
                dispatch({ type: ActionTypes.UPDATE_SETTINGS, payload: { settings } });
            } catch (error) {
                console.error('Failed to load notification data:', error);
            } finally {
                dispatch({ type: ActionTypes.SET_UI_STATE, payload: { ui: { isLoading: false } } });
            }
        };

        loadData();
    }, []);

    // 防抖保存到存储
    useEffect(() => {
        if (saveTimeoutRef.current) {
            clearTimeout(saveTimeoutRef.current);
        }

        saveTimeoutRef.current = setTimeout(() => {
            notificationService.saveNotifications(state.history);
            notificationService.saveSettings(state.settings);
        }, 1000);

        return () => {
            if (saveTimeoutRef.current) {
                clearTimeout(saveTimeoutRef.current);
            }
        };
    }, [state.history, state.settings]);

    // 创建通知
    const createNotification = useCallback((config) => {
        const notification = {
            id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            type: config.type || NotificationType.INFO,
            title: config.title || '通知',
            message: config.message || '',
            duration: config.duration !== undefined ? config.duration : state.settings.defaultDuration,
            priority: config.priority || NotificationPriority.MEDIUM,
            isRead: config.isRead ?? (config.type === NotificationType.SUCCESS || config.type === NotificationType.INFO),
            isPinned: config.isPinned || false,
            timestamp: new Date().toISOString(),
            actions: config.actions || [],
            metadata: config.metadata || {},
            ...config
        };

        return notification;
    }, [state.settings.defaultDuration]);

    // Actions
    const addNotification = useCallback((config) => {
        const notification = createNotification(config);
        dispatch({ type: ActionTypes.ADD_NOTIFICATION, payload: { notification } });

        // 自动移除
        if (notification.duration > 0) {
            setTimeout(() => {
                dispatch({ type: ActionTypes.REMOVE_NOTIFICATION, payload: { id: notification.id } });
            }, notification.duration);
        }

        // 播放声音
        if (state.settings.enableSound && notification.type !== NotificationType.SUCCESS) {
            notificationService.playSound(notification.type);
        }

        // 桌面通知
        if (state.settings.enableDesktop && document.hidden) {
            notificationService.showDesktopNotification(notification);
        }

        return notification.id;
    }, [createNotification, state.settings]);

    const removeNotification = useCallback((id) => {
        dispatch({ type: ActionTypes.REMOVE_NOTIFICATION, payload: { id } });
    }, []);

    const updateNotification = useCallback((id, updates) => {
        dispatch({ type: ActionTypes.UPDATE_NOTIFICATION, payload: { id, updates } });
    }, []);

    const markAsRead = useCallback((id) => {
        dispatch({ type: ActionTypes.MARK_AS_READ, payload: { id } });
    }, []);

    const markAllAsRead = useCallback(() => {
        dispatch({ type: ActionTypes.MARK_ALL_AS_READ });
    }, []);

    const togglePin = useCallback((id) => {
        dispatch({ type: ActionTypes.TOGGLE_PIN, payload: { id } });
    }, []);

    const deleteFromHistory = useCallback((id) => {
        dispatch({ type: ActionTypes.DELETE_FROM_HISTORY, payload: { id } });
    }, []);

    const clearCurrent = useCallback(() => {
        dispatch({ type: ActionTypes.CLEAR_CURRENT });
    }, []);

    const clearAll = useCallback(() => {
        dispatch({ type: ActionTypes.CLEAR_ALL });
        notificationService.clearAll();
    }, []);

    const updateSettings = useCallback((settings) => {
        dispatch({ type: ActionTypes.UPDATE_SETTINGS, payload: { settings } });
    }, []);

    const setUIState = useCallback((ui) => {
        dispatch({ type: ActionTypes.SET_UI_STATE, payload: { ui } });
    }, []);

    // 快捷方法
    const success = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.SUCCESS,
            title,
            message,
            ...options
        });
    }, [addNotification]);

    const warning = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.WARNING,
            title,
            message,
            duration: 0,
            ...options
        });
    }, [addNotification]);

    const error = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.ERROR,
            title,
            message,
            duration: 0,
            priority: NotificationPriority.HIGH,
            ...options
        });
    }, [addNotification]);

    const info = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.INFO,
            title,
            message,
            ...options
        });
    }, [addNotification]);

    const system = useCallback((title, message, options = {}) => {
        return addNotification({
            type: NotificationType.SYSTEM,
            title,
            message,
            priority: NotificationPriority.HIGH,
            ...options
        });
    }, [addNotification]);

    // Context value
    const value = useMemo(() => ({
        // State
        ...state,
        notifications: state.activeNotifications,
        unreadCount,
        pinnedCount,

        // Actions
        addNotification,
        removeNotification,
        updateNotification,
        markAsRead,
        markAllAsRead,
        togglePin,
        deleteFromHistory,
        clearCurrent,
        clearAll,
        updateSettings,
        setUIState,

        // Shortcuts
        success,
        warning,
        error,
        info,
        system
    }), [
        state,
        unreadCount,
        pinnedCount,
        addNotification,
        removeNotification,
        updateNotification,
        markAsRead,
        markAllAsRead,
        togglePin,
        deleteFromHistory,
        clearCurrent,
        clearAll,
        updateSettings,
        setUIState,
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
} 