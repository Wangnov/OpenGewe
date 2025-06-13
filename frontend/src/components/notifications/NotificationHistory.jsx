import React, { useState, useMemo, useRef, useEffect } from 'react';
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
 * 通知历史弹窗组件
 * @returns {JSX.Element} 历史弹窗组件
 */
const NotificationHistory = () => {
    const {
        history,
        showHistory,
        toggleHistory,
        markAsRead,
        markAllAsRead,
        togglePin,
        deleteFromHistory,
        clearAll
    } = useNotification();

    const [filter, setFilter] = useState('all'); // all, unread, pinned
    const [sortBy, setSortBy] = useState('newest'); // newest, oldest, priority
    const [isMobile] = useState(isMobileDevice());
    const [isClosing, setIsClosing] = useState(false);
    const backdropRef = useRef(null);
    const contentRef = useRef(null);

    // 过滤和排序历史记录
    const filteredHistory = useMemo(() => {
        let filtered = [...history];

        // 应用过滤器
        switch (filter) {
            case 'unread':
                filtered = filtered.filter(notification => !notification.isRead);
                break;
            case 'pinned':
                filtered = filtered.filter(notification => notification.isPinned);
                break;
            default:
                // 显示所有
                break;
        }

        // 应用排序
        switch (sortBy) {
            case 'oldest':
                filtered.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
                break;
            case 'priority':
                const priorityOrder = { high: 3, medium: 2, low: 1 };
                filtered.sort((a, b) => priorityOrder[b.priority] - priorityOrder[a.priority]);
                break;
            default: // newest
                filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
                break;
        }

        return filtered;
    }, [history, filter, sortBy]);

    const unreadCount = history.filter(n => !n.isRead).length;
    const pinnedCount = history.filter(n => n.isPinned).length;

    /**
     * 处理关闭弹窗
     */
    const handleClose = () => {
        if (isClosing) return; // 防止重复触发

        setIsClosing(true);

        // 添加退出动画类
        if (backdropRef.current && contentRef.current) {
            backdropRef.current.classList.add('animate-modal-backdrop-exit');
            backdropRef.current.classList.remove('animate-modal-backdrop-enter');

            contentRef.current.classList.add('animate-modal-content-exit');
            contentRef.current.classList.remove('animate-modal-content-enter');

            // 监听动画结束事件
            const handleAnimationEnd = () => {
                contentRef.current?.removeEventListener('animationend', handleAnimationEnd);
                setIsClosing(false);
                toggleHistory(); // 真正关闭弹窗
            };

            contentRef.current.addEventListener('animationend', handleAnimationEnd);

            // 备用：如果动画事件没有触发，使用定时器
            setTimeout(() => {
                if (contentRef.current) {
                    contentRef.current.removeEventListener('animationend', handleAnimationEnd);
                    setIsClosing(false);
                    toggleHistory();
                }
            }, 300);
        } else {
            // 如果DOM元素不存在，直接关闭
            setIsClosing(false);
            toggleHistory();
        }
    };

    /**
     * 处理蒙版点击
     */
    const handleBackdropClick = (e) => {
        // 确保点击的是蒙版本身，而不是内容区域
        if (e.target === e.currentTarget) {
            handleClose();
        }
    };

    // 重置关闭状态
    useEffect(() => {
        if (showHistory) {
            setIsClosing(false);
        }
    }, [showHistory]);

    if (!showHistory) return null;

    const HistoryContent = (
        <>
            {/* 背景遮罩 */}
            <div
                ref={backdropRef}
                className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[2000] animate-modal-backdrop-enter"
                onClick={handleBackdropClick}
            />

            {/* 弹窗内容 */}
            <div
                className="fixed inset-0 z-[2001] flex items-center justify-center p-4"
                onClick={handleBackdropClick}
            >
                <div
                    ref={contentRef}
                    className="bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl w-full max-w-2xl max-h-[80vh] flex flex-col overflow-hidden animate-modal-content-enter"
                    style={{
                        filter: 'drop-shadow(0 25px 50px rgb(0 0 0 / 0.25))',
                        boxShadow: '0 0 0 1px rgba(255, 255, 255, 0.2) inset'
                    }}
                    onClick={(e) => e.stopPropagation()}
                >

                    {/* 头部 */}
                    <div className="p-6 border-b border-gray-200/50">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-xl font-bold text-gray-800 flex items-center">
                                <i className="fas fa-history mr-2 text-blue-500"></i>
                                通知历史
                                <span className="ml-2 text-sm font-normal text-gray-500">
                                    ({filteredHistory.length})
                                </span>
                            </h2>
                            <button
                                onClick={handleClose}
                                disabled={isClosing}
                                className="w-8 h-8 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-500 hover:text-gray-700 flex items-center justify-center transition-all duration-200 disabled:opacity-50"
                            >
                                <i className="fas fa-times text-sm"></i>
                            </button>
                        </div>

                        {/* 过滤器和操作 */}
                        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                            {/* 过滤器 */}
                            <div className="flex items-center space-x-2">
                                <select
                                    value={filter}
                                    onChange={(e) => setFilter(e.target.value)}
                                    className="px-3 py-1 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                                >
                                    <option value="all">全部 ({history.length})</option>
                                    <option value="unread">未读 ({unreadCount})</option>
                                    <option value="pinned">置顶 ({pinnedCount})</option>
                                </select>

                                <select
                                    value={sortBy}
                                    onChange={(e) => setSortBy(e.target.value)}
                                    className="px-3 py-1 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                                >
                                    <option value="newest">最新优先</option>
                                    <option value="oldest">最旧优先</option>
                                    <option value="priority">按优先级</option>
                                </select>
                            </div>

                            {/* 操作按钮 */}
                            <div className="flex items-center space-x-2">
                                {unreadCount > 0 && (
                                    <button
                                        onClick={markAllAsRead}
                                        className="px-3 py-1 text-xs font-medium bg-blue-100 text-blue-600 hover:bg-blue-200 rounded-lg transition-all duration-200"
                                    >
                                        全部已读
                                    </button>
                                )}
                                {history.length > 0 && (
                                    <button
                                        onClick={() => {
                                            clearAll();
                                        }}
                                        className="px-3 py-1 text-xs font-medium bg-red-100 text-red-600 hover:bg-red-200 rounded-lg transition-all duration-200"
                                    >
                                        清空所有
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* 通知列表 */}
                    <div className="flex-1 overflow-y-auto p-6">
                        {filteredHistory.length === 0 ? (
                            <div className="text-center py-12">
                                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <i className="fas fa-bell-slash text-2xl text-gray-400"></i>
                                </div>
                                <h3 className="text-lg font-medium text-gray-800 mb-2">
                                    {filter === 'unread' ? '没有未读通知' :
                                        filter === 'pinned' ? '没有置顶通知' : '暂无通知历史'}
                                </h3>
                                <p className="text-gray-500">
                                    {filter === 'all' ? '您的通知历史将会显示在这里' : '尝试调整过滤条件'}
                                </p>
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {filteredHistory.map((notification) => (
                                    <NotificationItem
                                        key={notification.id}
                                        notification={notification}
                                        onRead={markAsRead}
                                        onPin={togglePin}
                                        onDelete={deleteFromHistory}
                                        showActions={true}
                                        isInHistory={true}
                                        isMobile={isMobile}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    );

    return createPortal(HistoryContent, document.body);
};

export default NotificationHistory; 