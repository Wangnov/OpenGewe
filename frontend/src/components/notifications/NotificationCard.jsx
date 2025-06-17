import React, { memo, useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { NotificationType } from '../../contexts/NotificationContext.new';

/**
 * 获取通知类型配置
 */
const getTypeConfig = (type) => {
    const configs = {
        [NotificationType.SUCCESS]: {
            icon: 'fas fa-check-circle',
            iconBg: 'bg-green-500',
            borderColor: 'border-green-200',
            textColor: 'text-green-800',
            progressBg: 'bg-green-500'
        },
        [NotificationType.WARNING]: {
            icon: 'fas fa-exclamation-triangle',
            iconBg: 'bg-amber-500',
            borderColor: 'border-amber-200',
            textColor: 'text-amber-800',
            progressBg: 'bg-amber-500'
        },
        [NotificationType.ERROR]: {
            icon: 'fas fa-times-circle',
            iconBg: 'bg-red-500',
            borderColor: 'border-red-200',
            textColor: 'text-red-800',
            progressBg: 'bg-red-500'
        },
        [NotificationType.INFO]: {
            icon: 'fas fa-info-circle',
            iconBg: 'bg-blue-500',
            borderColor: 'border-blue-200',
            textColor: 'text-blue-800',
            progressBg: 'bg-blue-500'
        },
        [NotificationType.SYSTEM]: {
            icon: 'fas fa-cog',
            iconBg: 'bg-purple-500',
            borderColor: 'border-purple-200',
            textColor: 'text-purple-800',
            progressBg: 'bg-purple-500'
        }
    };

    return configs[type] || configs[NotificationType.INFO];
};

/**
 * 通知卡片组件
 */
const NotificationCard = memo(({ notification, onClose, index }) => {
    const [isHovered, setIsHovered] = useState(false);
    const [progress, setProgress] = useState(100);
    const typeConfig = getTypeConfig(notification.type);

    // 自动关闭进度条
    useEffect(() => {
        if (notification.duration > 0 && !isHovered) {
            const interval = setInterval(() => {
                setProgress(prev => {
                    if (prev <= 0) {
                        clearInterval(interval);
                        return 0;
                    }
                    return prev - (100 / (notification.duration / 100));
                });
            }, 100);

            return () => clearInterval(interval);
        }
    }, [notification.duration, isHovered]);

    const handleAction = (action) => {
        if (action.onClick) {
            action.onClick(notification);
        }
        if (action.closeOnClick !== false) {
            onClose();
        }
    };

    return (
        <motion.div
            className={`relative bg-white rounded-xl shadow-lg border ${typeConfig.borderColor} 
                  overflow-hidden max-w-md w-full`}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
        >
            {/* 优先级指示器 */}
            {notification.priority === 'high' && (
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-red-500 to-orange-500" />
            )}

            <div className="p-4 flex items-start space-x-3">
                {/* 图标 */}
                <div className={`flex-shrink-0 w-10 h-10 ${typeConfig.iconBg} rounded-full 
                        flex items-center justify-center text-white shadow-md`}>
                    <i className={`${typeConfig.icon} text-lg`}></i>
                </div>

                {/* 内容 */}
                <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between">
                        <div className="flex-1">
                            <h4 className={`font-semibold ${typeConfig.textColor} mb-1`}>
                                {notification.title}
                                {notification.count && notification.count > 1 && (
                                    <span className="ml-2 text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                                        {notification.count}
                                    </span>
                                )}
                            </h4>
                            {notification.message && (
                                <p className="text-sm text-gray-600 line-clamp-2 whitespace-pre-line">
                                    {notification.message}
                                </p>
                            )}
                        </div>

                        {/* 关闭按钮 */}
                        <button
                            onClick={onClose}
                            className="ml-4 p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 
                        rounded-lg transition-colors duration-200"
                        >
                            <i className="fas fa-times text-sm"></i>
                        </button>
                    </div>

                    {/* 操作按钮 */}
                    {notification.actions && notification.actions.length > 0 && (
                        <div className="flex gap-2 mt-3">
                            {notification.actions.map((action, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => handleAction(action)}
                                    className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all duration-200
                            ${action.variant === 'primary'
                                            ? `${typeConfig.iconBg} text-white hover:opacity-90`
                                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                        }`}
                                >
                                    {action.icon && <i className={`${action.icon} mr-1.5`}></i>}
                                    {action.label}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* 自动关闭进度条 */}
            {notification.duration > 0 && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-100">
                    <motion.div
                        className={`h-full ${typeConfig.progressBg}`}
                        initial={{ width: '100%' }}
                        animate={{ width: `${progress}%` }}
                        transition={{ duration: 0.1, ease: 'linear' }}
                    />
                </div>
            )}

            {/* 堆叠阴影效果 */}
            {index > 0 && (
                <div className="absolute inset-0 bg-gradient-to-t from-black/5 to-transparent pointer-events-none" />
            )}
        </motion.div>
    );
});

NotificationCard.displayName = 'NotificationCard';

export default NotificationCard; 