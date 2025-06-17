import React, { memo } from 'react';
import { NotificationType } from '../../contexts/NotificationContext.new';

/**
 * 获取通知类型配置
 */
const getTypeConfig = (type) => {
    const configs = {
        [NotificationType.SUCCESS]: {
            icon: 'fas fa-check-circle',
            iconColor: 'text-green-500',
            bgColor: 'bg-green-50'
        },
        [NotificationType.WARNING]: {
            icon: 'fas fa-exclamation-triangle',
            iconColor: 'text-amber-500',
            bgColor: 'bg-amber-50'
        },
        [NotificationType.ERROR]: {
            icon: 'fas fa-times-circle',
            iconColor: 'text-red-500',
            bgColor: 'bg-red-50'
        },
        [NotificationType.INFO]: {
            icon: 'fas fa-info-circle',
            iconColor: 'text-blue-500',
            bgColor: 'bg-blue-50'
        },
        [NotificationType.SYSTEM]: {
            icon: 'fas fa-cog',
            iconColor: 'text-purple-500',
            bgColor: 'bg-purple-50'
        }
    };

    return configs[type] || configs[NotificationType.INFO];
};

/**
 * 格式化相对时间
 */
const formatRelativeTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffMins < 1) return '刚刚';
    if (diffMins < 60) return `${diffMins}分钟前`;
    if (diffHours < 24) return `${diffHours}小时前`;
    if (diffDays < 7) return `${diffDays}天前`;

    return date.toLocaleDateString('zh-CN');
};

/**
 * 通知历史项组件
 */
const NotificationHistoryItem = memo(({ notification, onRead, onPin, onDelete }) => {
    const typeConfig = getTypeConfig(notification.type);

    return (
        <div
            className={`group relative p-3 rounded-lg border transition-all duration-200
                ${notification.isRead
                    ? 'bg-white border-gray-200 hover:border-gray-300'
                    : `${typeConfig.bgColor} border-blue-200 hover:border-blue-300`}
                ${notification.isPinned ? 'ring-2 ring-purple-500/20' : ''}`}
        >
            {/* 置顶标记 */}
            {notification.isPinned && (
                <div className="absolute -top-2 -right-2 w-5 h-5 bg-purple-500 rounded-full flex items-center justify-center">
                    <i className="fas fa-thumbtack text-white text-xs"></i>
                </div>
            )}

            <div className="flex items-start space-x-3">
                {/* 图标 */}
                <div className={`flex-shrink-0 ${typeConfig.iconColor}`}>
                    <i className={`${typeConfig.icon} text-lg`}></i>
                </div>

                {/* 内容 */}
                <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between mb-1">
                        <h4 className={`font-medium ${notification.isRead ? 'text-gray-700' : 'text-gray-900'}`}>
                            {notification.title}
                            {notification.count && notification.count > 1 && (
                                <span className="ml-2 text-xs bg-gray-200 text-gray-600 px-1.5 py-0.5 rounded-full">
                                    {notification.count}
                                </span>
                            )}
                        </h4>
                        <span className="text-xs text-gray-500 ml-2 flex-shrink-0">
                            {formatRelativeTime(notification.timestamp)}
                        </span>
                    </div>

                    {notification.message && (
                        <p className="text-sm text-gray-600 line-clamp-2">
                            {notification.message}
                        </p>
                    )}

                    {/* 优先级标记 */}
                    {notification.priority === 'high' && (
                        <span className="inline-flex items-center mt-1 text-xs text-red-600">
                            <i className="fas fa-exclamation-circle mr-1"></i>
                            高优先级
                        </span>
                    )}
                </div>

                {/* 操作按钮 */}
                <div className="flex-shrink-0 flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    <button
                        onClick={() => onRead(notification.id)}
                        className={`p-1.5 rounded-md transition-colors duration-200
                      ${notification.isRead
                                ? 'text-gray-400 hover:text-blue-600 hover:bg-blue-50'
                                : 'text-blue-600 hover:bg-blue-100'}`}
                        title={notification.isRead ? '标记为未读' : '标记为已读'}
                    >
                        <i className={`fas ${notification.isRead ? 'fa-envelope' : 'fa-envelope-open'} text-xs`}></i>
                    </button>

                    <button
                        onClick={() => onPin(notification.id)}
                        className={`p-1.5 rounded-md transition-colors duration-200
                      ${notification.isPinned
                                ? 'text-purple-600 hover:bg-purple-100'
                                : 'text-gray-400 hover:text-purple-600 hover:bg-purple-50'}`}
                        title={notification.isPinned ? '取消置顶' : '置顶'}
                    >
                        <i className="fas fa-thumbtack text-xs"></i>
                    </button>

                    <button
                        onClick={() => onDelete(notification.id)}
                        className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors duration-200"
                        title="删除"
                    >
                        <i className="fas fa-trash text-xs"></i>
                    </button>
                </div>
            </div>
        </div>
    );
});

NotificationHistoryItem.displayName = 'NotificationHistoryItem';

export default NotificationHistoryItem; 