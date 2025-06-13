import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * 通知数量徽章组件
 * @param {Object} props - 组件属性
 * @param {number} props.count - 通知数量
 * @param {boolean} props.show - 是否显示徽章
 * @param {string} props.size - 徽章大小 ('sm' | 'md' | 'lg')
 * @param {string} props.color - 徽章颜色主题
 * @param {string} props.position - 徽章位置 ('top-right' | 'top-left' | 'bottom-right' | 'bottom-left')
 * @returns {JSX.Element} 徽章组件
 */
const NotificationBadge = ({
    count = 0,
    show = false,
    size = 'md',
    color = 'red',
    position = 'top-right'
}) => {
    // 如果数量为0且不强制显示，则不渲染
    if (count === 0 && !show) {
        return null;
    }

    // 尺寸配置
    const sizeConfig = {
        sm: {
            container: 'w-4 h-4 text-xs',
            text: 'text-xs leading-none',
            offset: '-top-1 -right-1'
        },
        md: {
            container: 'w-5 h-5',
            text: 'text-xs leading-none',
            offset: '-top-2 -right-2'
        },
        lg: {
            container: 'w-6 h-6',
            text: 'text-sm leading-none',
            offset: '-top-2 -right-2'
        }
    };

    // 颜色配置
    const colorConfig = {
        red: 'bg-red-500 text-white',
        blue: 'bg-blue-500 text-white',
        green: 'bg-green-500 text-white',
        yellow: 'bg-yellow-500 text-white',
        purple: 'bg-purple-500 text-white',
        indigo: 'bg-indigo-500 text-white',
        pink: 'bg-pink-500 text-white',
        gray: 'bg-gray-500 text-white'
    };

    // 位置配置
    const positionConfig = {
        'top-right': '-top-2 -right-2',
        'top-left': '-top-2 -left-2',
        'bottom-right': '-bottom-2 -right-2',
        'bottom-left': '-bottom-2 -left-2'
    };

    const currentSize = sizeConfig[size] || sizeConfig.md;
    const currentColor = colorConfig[color] || colorConfig.red;
    const currentPosition = positionConfig[position] || positionConfig['top-right'];

    // 显示的数量文本
    const displayCount = count > 99 ? '99+' : count.toString();

    // 动画配置
    const badgeVariants = {
        hidden: {
            scale: 0,
            opacity: 0,
            rotate: -180
        },
        visible: {
            scale: 1,
            opacity: 1,
            rotate: 0,
            transition: {
                type: "spring",
                stiffness: 500,
                damping: 25,
                duration: 0.6
            }
        },
        exit: {
            scale: 0,
            opacity: 0,
            rotate: 180,
            transition: {
                duration: 0.3,
                ease: "easeInOut"
            }
        },
        pulse: {
            scale: [1, 1.2, 1],
            transition: {
                duration: 0.6,
                ease: "easeInOut",
                times: [0, 0.5, 1]
            }
        }
    };

    return (
        <AnimatePresence>
            {(count > 0 || show) && (
                <motion.div
                    variants={badgeVariants}
                    initial="hidden"
                    animate="visible"
                    exit="exit"
                    whileHover="pulse"
                    className={`absolute ${currentPosition} ${currentSize.container} ${currentColor} 
                               rounded-full flex items-center justify-center font-bold shadow-lg 
                               border-2 border-white z-10`}
                    style={{
                        minWidth: currentSize.container.includes('w-4') ? '16px' :
                            currentSize.container.includes('w-5') ? '20px' : '24px'
                    }}
                >
                    <span className={currentSize.text}>
                        {displayCount}
                    </span>

                    {/* 脉冲动画效果 - 仅在有新通知时显示 */}
                    {count > 0 && (
                        <motion.div
                            className={`absolute inset-0 ${currentColor} rounded-full opacity-30`}
                            animate={{
                                scale: [1, 1.5, 1],
                                opacity: [0.3, 0, 0.3]
                            }}
                            transition={{
                                duration: 2,
                                repeat: Infinity,
                                ease: "easeInOut"
                            }}
                        />
                    )}
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default NotificationBadge; 