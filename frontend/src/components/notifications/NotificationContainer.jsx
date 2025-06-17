import React, { useContext } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { NotificationContext } from '../../contexts/NotificationContext.new';
import NotificationCard from './NotificationCard';
import { notificationQueue } from '../../utils/notificationQueue';

/**
 * 通知容器组件
 * 管理通知的显示位置和动画
 */
const NotificationContainer = () => {
    const { notifications, settings, removeNotification } = useContext(NotificationContext);
    const positionClasses = notificationQueue.getPositionClasses(settings.position);

    // 动画配置
    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: {
            opacity: 0,
            y: settings.position.includes('top') ? -50 : 50,
            scale: 0.9
        },
        visible: (custom) => {
            const offset = notificationQueue.calculateStackOffset(custom.index, notifications.length);
            return {
                opacity: offset.opacity,
                y: offset.y,
                scale: offset.scale,
                transition: {
                    type: 'spring',
                    stiffness: 300,
                    damping: 25
                }
            };
        },
        exit: {
            opacity: 0,
            scale: 0.8,
            x: settings.position.includes('right') ? 100 :
                settings.position.includes('left') ? -100 : 0,
            transition: {
                duration: 0.2,
                ease: 'easeInOut'
            }
        }
    };

    if (notifications.length === 0) {
        return null;
    }

    const content = (
        <div className={`fixed z-[1000] ${positionClasses} pointer-events-none`}>
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="space-y-3 pointer-events-auto"
            >
                <AnimatePresence mode="popLayout">
                    {notifications.map((notification, index) => (
                        <motion.div
                            key={notification.id}
                            custom={{ index }}
                            variants={itemVariants}
                            initial="hidden"
                            animate="visible"
                            exit="exit"
                            layout
                            layoutId={notification.id}
                        >
                            <NotificationCard
                                notification={notification}
                                onClose={() => removeNotification(notification.id)}
                                index={index}
                            />
                        </motion.div>
                    ))}
                </AnimatePresence>
            </motion.div>
        </div>
    );

    return createPortal(content, document.body);
};

export default NotificationContainer; 