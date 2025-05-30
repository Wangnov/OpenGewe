import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import NotificationItem from './NotificationItem';
import useNotification from '../../hooks/useNotification';

/**
 * 检测是否为移动设备
 * @returns {boolean} 是否为移动设备
 */
const isMobileDevice = () => {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
        window.innerWidth <= 768;
};

/**
 * 顶部浮动通知栏组件
 * @returns {JSX.Element} 通知栏组件
 */
const NotificationBar = () => {
    const { notifications, removeNotification } = useNotification();
    const [isMobile, setIsMobile] = useState(isMobileDevice());

    // 监听窗口大小变化
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(isMobileDevice());
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    /**
     * 处理通知关闭
     * @param {string} id - 通知ID
     */
    const handleNotificationClose = (id) => {
        removeNotification(id);
    };

    // 如果没有通知，不渲染任何内容
    if (notifications.length === 0) {
        return null;
    }

    const NotificationBarContent = (
        <div
            className="fixed top-0 left-0 right-0 z-[1000] pointer-events-none animate-notification-enter"
            style={{
                paddingTop: isMobile ? 'env(safe-area-inset-top, 12px)' : '16px'
            }}
        >
            <div className={`${isMobile ? 'px-3' : 'max-w-md mx-auto px-4'} space-y-3 pointer-events-auto`}>
                {notifications.map((notification) => (
                    <NotificationItem
                        key={notification.id}
                        notification={notification}
                        onClose={handleNotificationClose}
                        showActions={true}
                        isInHistory={false}
                        isMobile={isMobile}
                    />
                ))}
            </div>
        </div>
    );

    // 使用 Portal 渲染到 body
    return createPortal(NotificationBarContent, document.body);
};

export default NotificationBar; 