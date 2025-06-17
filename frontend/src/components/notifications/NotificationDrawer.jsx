import React, { useContext, useMemo, useState } from 'react';
import Modal from '../common/Modal';
import { NotificationContext } from '../../contexts/NotificationContext.new';
import NotificationHistoryItem from './NotificationHistoryItem';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * 通知抽屉组件
 */
const NotificationDrawer = () => {
    const {
        history,
        ui,
        unreadCount,
        pinnedCount,
        setUIState,
        markAsRead,
        markAllAsRead,
        togglePin,
        deleteFromHistory,
        clearAll
    } = useContext(NotificationContext);

    const [searchQuery, setSearchQuery] = useState('');

    // 过滤和排序通知
    const filteredNotifications = useMemo(() => {
        let filtered = [...history];

        // 搜索过滤
        if (searchQuery) {
            const query = searchQuery.toLowerCase();
            filtered = filtered.filter(n =>
                n.title.toLowerCase().includes(query) ||
                n.message.toLowerCase().includes(query)
            );
        }

        // 分类过滤
        switch (ui.filter) {
            case 'unread':
                filtered = filtered.filter(n => !n.isRead);
                break;
            case 'pinned':
                filtered = filtered.filter(n => n.isPinned);
                break;
            default:
                break;
        }

        // 排序
        const priorityWeight = { high: 3, medium: 2, low: 1 };
        switch (ui.sortBy) {
            case 'oldest':
                filtered.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
                break;
            case 'priority':
                filtered.sort((a, b) => priorityWeight[b.priority] - priorityWeight[a.priority]);
                break;
            default: // newest
                filtered.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
                break;
        }

        return filtered;
    }, [history, searchQuery, ui.filter, ui.sortBy]);

    const handleClose = () => {
        setUIState({ showHistory: false });
    };

    const filterTabs = [
        { key: 'all', label: '全部', count: history.length },
        { key: 'unread', label: '未读', count: unreadCount },
        { key: 'pinned', label: '置顶', count: pinnedCount }
    ];

    const sortOptions = [
        { value: 'newest', label: '最新优先' },
        { value: 'oldest', label: '最旧优先' },
        { value: 'priority', label: '按优先级' }
    ];

    const modalContent = (
        <div className="flex flex-col h-full max-h-[600px]">
            {/* 搜索和筛选 */}
            <div className="space-y-4 mb-4">
                {/* 搜索框 */}
                <div className="relative">
                    <i className="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
                    <input
                        type="text"
                        placeholder="搜索通知..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                    {searchQuery && (
                        <button
                            onClick={() => setSearchQuery('')}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                            <i className="fas fa-times"></i>
                        </button>
                    )}
                </div>

                {/* 筛选标签 */}
                <div className="flex items-center justify-between">
                    <div className="flex space-x-2">
                        {filterTabs.map(tab => (
                            <button
                                key={tab.key}
                                onClick={() => setUIState({ filter: tab.key })}
                                className={`px-3 py-1.5 text-sm font-medium rounded-lg transition-all duration-200
                          ${ui.filter === tab.key
                                        ? 'bg-purple-100 text-purple-700'
                                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                    }`}
                            >
                                {tab.label}
                                <span className="ml-1.5 text-xs">({tab.count})</span>
                            </button>
                        ))}
                    </div>

                    {/* 排序选择 */}
                    <select
                        value={ui.sortBy}
                        onChange={(e) => setUIState({ sortBy: e.target.value })}
                        className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                    >
                        {sortOptions.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            {/* 通知列表 */}
            <div className="flex-1 overflow-y-auto -mx-6 px-6">
                {filteredNotifications.length === 0 ? (
                    <div className="text-center py-12">
                        <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                            <i className="fas fa-bell-slash text-2xl text-gray-400"></i>
                        </div>
                        <h3 className="text-lg font-medium text-gray-800 mb-2">
                            {searchQuery ? '没有找到匹配的通知' :
                                ui.filter === 'unread' ? '没有未读通知' :
                                    ui.filter === 'pinned' ? '没有置顶通知' : '暂无通知记录'}
                        </h3>
                        <p className="text-gray-500 text-sm">
                            {searchQuery ? '尝试使用其他关键词搜索' : '新的通知将会显示在这里'}
                        </p>
                    </div>
                ) : (
                    <div className="space-y-2">
                        <AnimatePresence mode="popLayout">
                            {filteredNotifications.map((notification) => (
                                <motion.div
                                    key={notification.id}
                                    layout
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, x: -100 }}
                                    transition={{ duration: 0.2 }}
                                >
                                    <NotificationHistoryItem
                                        notification={notification}
                                        onRead={() => markAsRead(notification.id)}
                                        onPin={() => togglePin(notification.id)}
                                        onDelete={() => deleteFromHistory(notification.id)}
                                    />
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>
                )}
            </div>
        </div>
    );

    const modalFooter = (
        <div className="flex items-center justify-between">
            <div className="text-sm text-gray-500">
                共 {history.length} 条通知
            </div>
            <div className="flex space-x-2">
                {unreadCount > 0 && (
                    <button
                        onClick={markAllAsRead}
                        className="px-3 py-1.5 text-sm font-medium bg-blue-100 text-blue-700 hover:bg-blue-200 rounded-lg transition-colors duration-200"
                    >
                        全部标为已读
                    </button>
                )}
                {history.length > 0 && (
                    <button
                        onClick={() => {
                            if (window.confirm('确定要清空所有通知记录吗？')) {
                                clearAll();
                            }
                        }}
                        className="px-3 py-1.5 text-sm font-medium bg-red-100 text-red-700 hover:bg-red-200 rounded-lg transition-colors duration-200"
                    >
                        清空所有
                    </button>
                )}
            </div>
        </div>
    );

    return (
        <Modal
            isOpen={ui.showHistory}
            onClose={handleClose}
            title="通知中心"
            size="xl"
            footer={modalFooter}
            loading={ui.isLoading}
        >
            {modalContent}
        </Modal>
    );
};

export default NotificationDrawer; 