/**
 * 通知服务
 * 使用 IndexedDB 进行高性能存储
 */

const DB_NAME = 'OpenGeweNotifications';
const DB_VERSION = 1;
const STORE_NAMES = {
    NOTIFICATIONS: 'notifications',
    SETTINGS: 'settings'
};

class NotificationService {
    constructor() {
        this.db = null;
        this.initPromise = this.initDB();
        this.audioCache = new Map();
    }

    /**
     * 初始化 IndexedDB
     */
    async initDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(DB_NAME, DB_VERSION);

            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;

                // 创建通知存储
                if (!db.objectStoreNames.contains(STORE_NAMES.NOTIFICATIONS)) {
                    const notificationStore = db.createObjectStore(STORE_NAMES.NOTIFICATIONS, {
                        keyPath: 'id'
                    });
                    notificationStore.createIndex('timestamp', 'timestamp');
                    notificationStore.createIndex('type', 'type');
                    notificationStore.createIndex('isRead', 'isRead');
                    notificationStore.createIndex('isPinned', 'isPinned');
                }

                // 创建设置存储
                if (!db.objectStoreNames.contains(STORE_NAMES.SETTINGS)) {
                    db.createObjectStore(STORE_NAMES.SETTINGS, { keyPath: 'key' });
                }
            };
        });
    }

    /**
     * 确保数据库已初始化
     */
    async ensureDB() {
        if (!this.db) {
            await this.initPromise;
        }
    }

    /**
     * 保存通知列表
     */
    async saveNotifications(notifications) {
        await this.ensureDB();

        const transaction = this.db.transaction([STORE_NAMES.NOTIFICATIONS], 'readwrite');
        const store = transaction.objectStore(STORE_NAMES.NOTIFICATIONS);

        // 清空现有数据
        await new Promise((resolve, reject) => {
            const clearRequest = store.clear();
            clearRequest.onsuccess = resolve;
            clearRequest.onerror = () => reject(clearRequest.error);
        });

        // 批量添加新数据
        const promises = notifications.map(notification => {
            return new Promise((resolve, reject) => {
                const request = store.add(notification);
                request.onsuccess = resolve;
                request.onerror = () => reject(request.error);
            });
        });

        await Promise.all(promises);
    }

    /**
     * 加载通知列表
     */
    async loadNotifications() {
        await this.ensureDB();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([STORE_NAMES.NOTIFICATIONS], 'readonly');
            const store = transaction.objectStore(STORE_NAMES.NOTIFICATIONS);
            const index = store.index('timestamp');
            const request = index.openCursor(null, 'prev'); // 按时间倒序

            const notifications = [];

            request.onsuccess = (event) => {
                const cursor = event.target.result;
                if (cursor) {
                    notifications.push(cursor.value);
                    cursor.continue();
                } else {
                    resolve(notifications);
                }
            };

            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 保存设置
     */
    async saveSettings(settings) {
        await this.ensureDB();

        const transaction = this.db.transaction([STORE_NAMES.SETTINGS], 'readwrite');
        const store = transaction.objectStore(STORE_NAMES.SETTINGS);

        return new Promise((resolve, reject) => {
            const request = store.put({ key: 'userSettings', ...settings });
            request.onsuccess = resolve;
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 加载设置
     */
    async loadSettings() {
        await this.ensureDB();

        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([STORE_NAMES.SETTINGS], 'readonly');
            const store = transaction.objectStore(STORE_NAMES.SETTINGS);
            const request = store.get('userSettings');

            request.onsuccess = () => {
                if (request.result) {
                    const { key: _key, ...settings } = request.result;
                    resolve(settings);
                } else {
                    resolve({}); // 返回空对象，让 Context 使用默认值
                }
            };

            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 清空所有数据
     */
    async clearAll() {
        await this.ensureDB();

        const transaction = this.db.transaction(
            [STORE_NAMES.NOTIFICATIONS, STORE_NAMES.SETTINGS],
            'readwrite'
        );

        await Promise.all([
            new Promise((resolve, reject) => {
                const request = transaction.objectStore(STORE_NAMES.NOTIFICATIONS).clear();
                request.onsuccess = resolve;
                request.onerror = () => reject(request.error);
            }),
            new Promise((resolve, reject) => {
                const request = transaction.objectStore(STORE_NAMES.SETTINGS).clear();
                request.onsuccess = resolve;
                request.onerror = () => reject(request.error);
            })
        ]);
    }

    /**
     * 清理过期通知
     */
    async cleanupExpired(days = 7) {
        await this.ensureDB();

        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - days);
        const cutoffTimestamp = cutoffDate.toISOString();

        const transaction = this.db.transaction([STORE_NAMES.NOTIFICATIONS], 'readwrite');
        const store = transaction.objectStore(STORE_NAMES.NOTIFICATIONS);
        const index = store.index('timestamp');
        const range = IDBKeyRange.upperBound(cutoffTimestamp);

        return new Promise((resolve, reject) => {
            const request = index.openCursor(range);
            let deletedCount = 0;

            request.onsuccess = (event) => {
                const cursor = event.target.result;
                if (cursor) {
                    if (!cursor.value.isPinned) { // 不删除置顶的通知
                        cursor.delete();
                        deletedCount++;
                    }
                    cursor.continue();
                } else {
                    resolve(deletedCount);
                }
            };

            request.onerror = () => reject(request.error);
        });
    }

    /**
     * 获取通知统计
     */
    async getStats() {
        await this.ensureDB();

        const transaction = this.db.transaction([STORE_NAMES.NOTIFICATIONS], 'readonly');
        const store = transaction.objectStore(STORE_NAMES.NOTIFICATIONS);

        const [total, unread, pinned] = await Promise.all([
            new Promise((resolve, reject) => {
                const request = store.count();
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            }),
            new Promise((resolve, reject) => {
                const request = store.index('isRead').count(false);
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            }),
            new Promise((resolve, reject) => {
                const request = store.index('isPinned').count(true);
                request.onsuccess = () => resolve(request.result);
                request.onerror = () => reject(request.error);
            })
        ]);

        return { total, unread, pinned };
    }

    /**
     * 播放通知声音
     */
    async playSound(type) {
        try {
            const soundMap = {
                success: '/sounds/success.mp3',
                warning: '/sounds/warning.mp3',
                error: '/sounds/error.mp3',
                info: '/sounds/info.mp3',
                system: '/sounds/system.mp3'
            };

            const soundUrl = soundMap[type] || soundMap.info;

            if (!this.audioCache.has(soundUrl)) {
                const audio = new Audio(soundUrl);
                audio.volume = 0.5;
                this.audioCache.set(soundUrl, audio);
            }

            const audio = this.audioCache.get(soundUrl);
            audio.currentTime = 0;
            await audio.play();
        } catch (error) {
            console.warn('Failed to play notification sound:', error);
        }
    }

    /**
     * 显示桌面通知
     */
    async showDesktopNotification(notification) {
        if (!('Notification' in window)) {
            return;
        }

        if (Notification.permission === 'default') {
            await Notification.requestPermission();
        }

        if (Notification.permission === 'granted') {
            const iconMap = {
                success: '✅',
                warning: '⚠️',
                error: '❌',
                info: 'ℹ️',
                system: '⚙️'
            };

            new Notification(notification.title, {
                body: notification.message,
                icon: `/icons/${notification.type}.png`,
                badge: iconMap[notification.type],
                tag: notification.id,
                requireInteraction: notification.priority === 'high'
            });
        }
    }

    /**
     * 导出数据
     */
    async exportData() {
        const [notifications, settings] = await Promise.all([
            this.loadNotifications(),
            this.loadSettings()
        ]);

        return {
            notifications,
            settings,
            exportTime: new Date().toISOString(),
            version: DB_VERSION
        };
    }

    /**
     * 导入数据
     */
    async importData(data) {
        if (data.notifications) {
            await this.saveNotifications(data.notifications);
        }
        if (data.settings) {
            await this.saveSettings(data.settings);
        }
    }
}

// 导出单例
export const notificationService = new NotificationService(); 