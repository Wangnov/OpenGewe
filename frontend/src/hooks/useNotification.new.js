import { useContext } from 'react';
import { NotificationContext } from '../contexts/NotificationContext.new';

/**
 * 通知钩子
 * 提供便捷的通知系统访问接口
 */
const useNotification = () => {
    const context = useContext(NotificationContext);

    if (!context) {
        throw new Error('useNotification must be used within NotificationProvider');
    }

    return context;
};

export default useNotification; 