import React, { useState, useEffect, memo, useRef } from 'react';
import { motion } from 'framer-motion';
import { NotificationType } from '../../contexts/NotificationContext';

/**
 * 获取通知类型配置
 * @param {string} type - 通知类型
 * @returns {Object} 类型配置
 */
const getTypeConfig = (type) => {
    const configs = {
        [NotificationType.SUCCESS]: {
            icon: 'fas fa-check-circle',
            bgColor: 'from-green-500 to-emerald-500',
            textColor: 'text-green-800',
            borderColor: 'border-green-200'
        },
        [NotificationType.WARNING]: {
            icon: 'fas fa-exclamation-triangle',
            bgColor: 'from-yellow-500 to-orange-500',
            textColor: 'text-yellow-800',
            borderColor: 'border-yellow-200'
        },
        [NotificationType.ERROR]: {
            icon: 'fas fa-times-circle',
            bgColor: 'from-red-500 to-rose-500',
            textColor: 'text-red-800',
            borderColor: 'border-red-200'
        },
        [NotificationType.INFO]: {
            icon: 'fas fa-info-circle',
            bgColor: 'from-blue-500 to-indigo-500',
            textColor: 'text-blue-800',
            borderColor: 'border-blue-200'
        },
        [NotificationType.SYSTEM]: {
            icon: 'fas fa-cog',
            bgColor: 'from-purple-500 to-violet-500',
            textColor: 'text-purple-800',
            borderColor: 'border-purple-200'
        }
    };

    return configs[type] || configs[NotificationType.INFO];
};

/**
 * 格式化时间显示
 * @param {string} timestamp - ISO时间字符串
 * @returns {string} 格式化后的时间
 */
const formatTime = (timestamp) => {
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

    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
};

/**
 * 单个通知项组件
 * @param {Object} props - 组件属性
 * @param {Object} props.notification - 通知对象
 * @param {Function} props.onClose - 关闭回调
 * @param {Function} props.onRead - 标记已读回调
 * @param {Function} props.onPin - 置顶回调
 * @param {Function} props.onDelete - 删除回调
 * @param {boolean} props.showActions - 是否显示操作按钮
 * @param {boolean} props.isInHistory - 是否在历史记录中
 * @param {boolean} props.isMobile - 是否为移动设备
 * @returns {JSX.Element} 通知项组件
 */
const NotificationItem = ({
    notification,
    onClose,
    onRead,
    onPin,
    onDelete,
    showActions = true,
    isInHistory = false,
    isMobile = false
}) => {
    const [isHovered, setIsHovered] = useState(false);
    const [isDragging, setIsDragging] = useState(false);
    const [isRemoving, setIsRemoving] = useState(false);
    const autoCloseTimerRef = useRef(null);
    const elementRef = useRef(null);

    const typeConfig = getTypeConfig(notification.type);

    // 自动关闭定时器
    useEffect(() => {
        if (!isInHistory && notification.duration > 0 && !isHovered && !isDragging) {
            autoCloseTimerRef.current = setTimeout(() => {
                handleClose();
            }, notification.duration);
        } else {
            if (autoCloseTimerRef.current) {
                clearTimeout(autoCloseTimerRef.current);
                autoCloseTimerRef.current = null;
            }
        }

        return () => {
            if (autoCloseTimerRef.current) {
                clearTimeout(autoCloseTimerRef.current);
                autoCloseTimerRef.current = null;
            }
        };
    }, [notification.duration, isHovered, isDragging, isInHistory, notification.id]);

    // 监听isRemoving状态，用于触发移除动画
    useEffect(() => {
        if (notification.isRemoving) {
            setIsRemoving(true);
        }
    }, [notification.isRemoving]);

    /**
     * 处理关闭 - 使用DOM操作确保动画完成
     */
    const handleClose = () => {
        if (isRemoving) return; // 防止重复触发

        setIsRemoving(true);

        // 添加退出动画类
        if (elementRef.current) {
            elementRef.current.classList.add('animate-notification-exit');
            elementRef.current.classList.remove('animate-notification-enter');

            // 监听动画结束事件
            const handleAnimationEnd = () => {
                elementRef.current?.removeEventListener('animationend', handleAnimationEnd);
                onClose?.(notification.id);
            };

            elementRef.current.addEventListener('animationend', handleAnimationEnd);

            // 备用：如果动画事件没有触发，使用定时器
            setTimeout(() => {
                if (elementRef.current) {
                    elementRef.current.removeEventListener('animationend', handleAnimationEnd);
                    onClose?.(notification.id);
                }
            }, 600);
        }
    };

    /**
     * 处理标记已读
     */
    const handleRead = () => {
        onRead?.(notification.id);
    };

    /**
     * 处理置顶
     */
    const handlePin = () => {
        onPin?.(notification.id);
    };

    /**
     * 处理删除
     */
    const handleDelete = () => {
        onDelete?.(notification.id);
    };

    /**
     * 处理操作按钮点击
     * @param {Object} action - 操作配置
     */
    const handleActionClick = (action) => {
        if (action.onClick) {
            action.onClick(notification);
        }
    };

    /**
     * 处理拖拽开始
     */
    const handleDragStart = () => {
        setIsDragging(true);
    };

    /**
     * 处理拖拽结束
     * @param {Event} event - 事件对象
     * @param {Object} info - 拖拽信息
     */
    const handleDragEnd = (event, info) => {
        setIsDragging(false);

        // 移动端上划消失逻辑
        if (isMobile && !isInHistory) {
            const { offset, velocity } = info;
            const shouldDismiss = offset.y < -50 || velocity.y < -500;

            if (shouldDismiss) {
                handleClose();
            }
        }
    };

    // 拖拽约束
    const dragConstraints = isMobile && !isInHistory ? {
        top: -100,
        bottom: 10,
        left: 0,
        right: 0
    } : false;

    return (
        <div
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            className={`relative bg-white/95 backdrop-blur-xl rounded-xl shadow-lg border ${typeConfig.borderColor} 
                       overflow-hidden hover:shadow-xl hover:scale-[1.02] transition-all duration-200
                       ${isInHistory ? 'mb-2' : 'mb-3'} ${notification.isPinned ? 'ring-2 ring-purple-500/30' : ''}
                       ${!notification.isRead && isInHistory ? 'border-l-4 border-l-blue-500' : ''}
                       ${isDragging ? 'cursor-grabbing' : (dragConstraints ? 'cursor-grab' : '')}
                       ${isRemoving ? 'animate-notification-exit' : 'animate-notification-enter'}`}
            style={{
                filter: 'drop-shadow(0 4px 8px rgb(0 0 0 / 0.1))',
                boxShadow: 'rgba(0, 0, 0, 0.1) 0px 4px 12px, rgba(255, 255, 255, 0.4) 0px 0px 0px 1px inset'
            }}
            ref={elementRef}
        >
            {/* 渐变背景装饰 */}
            <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${typeConfig.bgColor}`} />

            {/* 置顶标识 */}
            {notification.isPinned && (
                <div className="absolute top-3 right-3 w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center z-10">
                    <i className="fas fa-thumbtack text-white text-xs"></i>
                </div>
            )}

            {/* 移动端上划提示 */}
            {isMobile && !isInHistory && isDragging && (
                <div className="absolute top-1 left-1/2 transform -translate-x-1/2 text-xs text-gray-500 bg-white/80 px-2 py-1 rounded-full">
                    上划关闭
                </div>
            )}

            <div className="p-4 flex items-center space-x-3 min-h-[80px]">
                {/* 图标 */}
                <div className={`flex-shrink-0 w-10 h-10 rounded-lg bg-gradient-to-br ${typeConfig.bgColor} 
                               flex items-center justify-center shadow-lg`}>
                    <i className={`${typeConfig.icon} text-white text-lg`}></i>
                </div>

                {/* 内容区域 */}
                <div className="flex-1 min-w-0 py-2">
                    {/* 标题和时间 */}
                    <div className="flex items-center justify-between mb-1">
                        <h4 className={`font-semibold text-gray-800 text-sm leading-tight ${notification.title.length > 20 ? 'line-clamp-1' : ''
                            }`}>
                            {notification.title}
                        </h4>
                        <span className="text-xs text-gray-500 ml-2 flex-shrink-0">
                            {formatTime(notification.timestamp)}
                        </span>
                    </div>

                    {/* 消息内容 */}
                    {notification.message && (
                        <p className="text-gray-600 text-sm leading-relaxed line-clamp-2">
                            {notification.message}
                        </p>
                    )}

                    {/* 自定义操作按钮 */}
                    {notification.actions && notification.actions.length > 0 && (
                        <div className="flex space-x-2 mt-2">
                            {notification.actions.map((action, index) => (
                                <button
                                    key={index}
                                    onClick={() => handleActionClick(action)}
                                    className={`px-3 py-1 text-xs font-medium rounded-lg transition-all duration-200
                                               ${action.variant === 'primary'
                                            ? `bg-gradient-to-r ${typeConfig.bgColor} text-white hover:scale-105 shadow-sm`
                                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                        }`}
                                >
                                    {action.icon && <i className={`${action.icon} mr-1`}></i>}
                                    {action.label}
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                {/* 操作按钮 - 移动端始终显示关闭按钮 */}
                {showActions && (
                    <div className={`flex-shrink-0 flex items-center space-x-1 transition-opacity duration-200
                                   ${isMobile || isHovered || isInHistory ? 'opacity-100' : 'opacity-0'}`}>

                        {isInHistory && (
                            <>
                                {/* 标记已读/未读 */}
                                <button
                                    onClick={handleRead}
                                    className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-200
                                               ${notification.isRead
                                            ? 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                                            : 'bg-blue-100 text-blue-600 hover:bg-blue-200'
                                        }`}
                                    title={notification.isRead ? '标记为未读' : '标记为已读'}
                                >
                                    <i className={`fas ${notification.isRead ? 'fa-envelope' : 'fa-envelope-open'} text-xs`}></i>
                                </button>

                                {/* 置顶/取消置顶 */}
                                <button
                                    onClick={handlePin}
                                    className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-200
                                               ${notification.isPinned
                                            ? 'bg-purple-100 text-purple-600 hover:bg-purple-200'
                                            : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                                        }`}
                                    title={notification.isPinned ? '取消置顶' : '置顶'}
                                >
                                    <i className="fas fa-thumbtack text-xs"></i>
                                </button>

                                {/* 删除 */}
                                <button
                                    onClick={handleDelete}
                                    className="w-8 h-8 rounded-lg bg-gray-100 text-gray-500 hover:bg-red-100 hover:text-red-600 
                                             flex items-center justify-center transition-all duration-200"
                                    title="删除"
                                >
                                    <i className="fas fa-trash text-xs"></i>
                                </button>
                            </>
                        )}

                        {!isInHistory && (
                            /* 关闭按钮 - 移动端始终显示 */
                            <button
                                onClick={handleClose}
                                className={`w-8 h-8 rounded-lg bg-gray-100 text-gray-500 hover:bg-gray-200 hover:text-red-600
                                         flex items-center justify-center transition-all duration-200 
                                         ${isMobile ? 'opacity-80' : ''}`}
                                title="关闭"
                            >
                                <i className="fas fa-times text-xs"></i>
                            </button>
                        )}
                    </div>
                )}
            </div>

            {/* 优先级指示器 */}
            {notification.priority === 'high' && (
                <div className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-red-500 to-orange-500" />
            )}
        </div>
    );
};

export default memo(NotificationItem);