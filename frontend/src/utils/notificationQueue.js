/**
 * 通知队列管理器
 * 处理通知的优先级、去重和排序
 */

class NotificationQueue {
    constructor() {
        this.maxActiveNotifications = 5;
        this.groupingWindow = 5000; // 5秒内的相似通知会被分组
    }

    /**
     * 添加通知到队列
     */
    add(currentNotifications, newNotification) {
        // 检查是否需要分组
        const groupedNotification = this.tryGroupNotification(currentNotifications, newNotification);
        if (groupedNotification) {
            return currentNotifications.map(n =>
                n.id === groupedNotification.id ? groupedNotification : n
            );
        }

        // 添加新通知
        let notifications = [...currentNotifications, newNotification];

        // 按优先级和时间排序
        notifications = this.sortNotifications(notifications);

        // 限制显示数量
        if (notifications.length > this.maxActiveNotifications) {
            // 保留高优先级和固定的通知
            const pinnedNotifications = notifications.filter(n => n.isPinned);
            const highPriorityNotifications = notifications
                .filter(n => !n.isPinned && n.priority === 'high')
                .slice(0, this.maxActiveNotifications - pinnedNotifications.length);

            const remainingSlots = this.maxActiveNotifications -
                pinnedNotifications.length -
                highPriorityNotifications.length;

            const otherNotifications = notifications
                .filter(n => !n.isPinned && n.priority !== 'high')
                .slice(0, Math.max(0, remainingSlots));

            notifications = [
                ...pinnedNotifications,
                ...highPriorityNotifications,
                ...otherNotifications
            ];
        }

        return notifications;
    }

    /**
     * 尝试将通知分组
     */
    tryGroupNotification(currentNotifications, newNotification) {
        const now = Date.now();
        const recentNotifications = currentNotifications.filter(n => {
            const notificationTime = new Date(n.timestamp).getTime();
            return now - notificationTime < this.groupingWindow;
        });

        // 查找可以分组的通知
        const similarNotification = recentNotifications.find(n =>
            n.type === newNotification.type &&
            n.title === newNotification.title &&
            !n.isPinned
        );

        if (similarNotification) {
            // 合并通知
            return {
                ...similarNotification,
                message: this.mergeMessages(similarNotification.message, newNotification.message),
                count: (similarNotification.count || 1) + 1,
                timestamp: newNotification.timestamp,
                metadata: {
                    ...similarNotification.metadata,
                    ...newNotification.metadata,
                    groupedIds: [
                        ...(similarNotification.metadata.groupedIds || [similarNotification.id]),
                        newNotification.id
                    ]
                }
            };
        }

        return null;
    }

    /**
     * 合并消息内容
     */
    mergeMessages(existingMessage, newMessage) {
        if (existingMessage === newMessage) {
            return existingMessage;
        }

        // 如果消息相似度很高，只显示一条加上计数
        const similarity = this.calculateSimilarity(existingMessage, newMessage);
        if (similarity > 0.8) {
            return existingMessage;
        }

        // 否则合并显示
        return `${existingMessage}\n${newMessage}`;
    }

    /**
     * 计算消息相似度
     */
    calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;

        if (longer.length === 0) {
            return 1.0;
        }

        const distance = this.levenshteinDistance(longer, shorter);
        return (longer.length - distance) / longer.length;
    }

    /**
     * 计算编辑距离
     */
    levenshteinDistance(str1, str2) {
        const matrix = [];

        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }

        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }

        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }

        return matrix[str2.length][str1.length];
    }

    /**
     * 排序通知
     */
    sortNotifications(notifications) {
        const priorityWeight = { high: 3, medium: 2, low: 1 };

        return notifications.sort((a, b) => {
            // 置顶的始终在前
            if (a.isPinned !== b.isPinned) {
                return a.isPinned ? -1 : 1;
            }

            // 按优先级排序
            const priorityDiff = priorityWeight[b.priority] - priorityWeight[a.priority];
            if (priorityDiff !== 0) {
                return priorityDiff;
            }

            // 按时间排序（新的在前）
            return new Date(b.timestamp) - new Date(a.timestamp);
        });
    }

    /**
     * 获取通知位置配置
     */
    getPositionClasses(position) {
        const positions = {
            'top-left': 'top-4 left-4',
            'top-center': 'top-4 left-1/2 -translate-x-1/2',
            'top-right': 'top-4 right-4',
            'bottom-left': 'bottom-4 left-4',
            'bottom-center': 'bottom-4 left-1/2 -translate-x-1/2',
            'bottom-right': 'bottom-4 right-4'
        };

        return positions[position] || positions['top-right'];
    }

    /**
     * 计算通知堆叠偏移
     */
    calculateStackOffset(index, _total) {
        const baseOffset = 8; // 基础偏移量（像素）
        const maxVisible = 3; // 最多显示的堆叠层数

        if (index >= maxVisible) {
            return {
                y: baseOffset * maxVisible,
                scale: 0.9,
                opacity: 0
            };
        }

        return {
            y: baseOffset * index,
            scale: 1 - (index * 0.02),
            opacity: 1 - (index * 0.1)
        };
    }
}

// 导出单例
export const notificationQueue = new NotificationQueue(); 