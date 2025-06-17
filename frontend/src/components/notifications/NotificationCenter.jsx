import React from 'react';
import NotificationContainer from './NotificationContainer';
import NotificationDrawer from './NotificationDrawer';

/**
 * 通知中心组件
 * 统一管理所有通知相关的 UI
 */
const NotificationCenter = () => {
    return (
        <>
            {/* 浮动通知容器 */}
            <NotificationContainer />

            {/* 通知历史抽屉 */}
            <NotificationDrawer />
        </>
    );
};

export default NotificationCenter; 