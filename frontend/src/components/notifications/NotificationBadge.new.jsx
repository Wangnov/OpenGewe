import React, { useContext } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { NotificationContext } from '../../contexts/NotificationContext.new';

/**
 * 通知徽章组件
 * 显示未读通知数量
 */
const NotificationBadge = ({ onClick, className = '' }) => {
    const { unreadCount, setUIState } = useContext(NotificationContext);

    const handleClick = () => {
        if (onClick) {
            onClick();
        } else {
            setUIState({ showHistory: true });
        }
    };

    return (
        <button
            onClick={handleClick}
            className={`relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 
                 rounded-lg transition-all duration-200 ${className}`}
            title={unreadCount > 0 ? `${unreadCount} 条未读通知` : '通知中心'}
        >
            <i className="fas fa-bell text-xl"></i>

            <AnimatePresence>
                {unreadCount > 0 && (
                    <motion.div
                        initial={{ scale: 0, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0, opacity: 0 }}
                        transition={{
                            type: 'spring',
                            stiffness: 500,
                            damping: 20
                        }}
                        className="absolute -top-1 -right-1"
                    >
                        <span className="relative flex h-5 w-5">
                            {/* 脉冲动画 */}
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                            <span className="relative inline-flex items-center justify-center rounded-full h-5 w-5 bg-red-500 text-white text-xs font-bold">
                                {unreadCount > 99 ? '99+' : unreadCount}
                            </span>
                        </span>
                    </motion.div>
                )}
            </AnimatePresence>
        </button>
    );
};

export default NotificationBadge; 