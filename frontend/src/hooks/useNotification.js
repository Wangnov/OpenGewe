import { useContext } from 'react';
import { NotificationContext } from '../contexts/NotificationContext';

/**
 * 通知管理Hook
 * 提供简洁的通知操作接口
 * @returns {Object} 通知操作方法和状态
 */
const useNotification = () => {
    const context = useContext(NotificationContext);

    if (!context) {
        throw new Error('useNotification must be used within a NotificationProvider');
    }

    return context;
};

export default useNotification;