import React, { useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * 统一的弹窗组件
 * @param {Object} props - 组件属性
 * @param {boolean} props.isOpen - 是否打开弹窗
 * @param {Function} props.onClose - 关闭弹窗回调
 * @param {string} props.title - 弹窗标题
 * @param {React.ReactNode} props.children - 弹窗内容
 * @param {string} props.size - 弹窗大小 ('xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl', '6xl', '7xl', 'full')
 * @param {boolean} props.showCloseButton - 是否显示关闭按钮
 * @param {React.ReactNode} props.footer - 底部内容
 * @param {boolean} props.closeOnBackdropClick - 点击背景是否关闭
 * @param {string} props.className - 额外的CSS类名
 * @param {boolean} props.loading - 是否显示加载状态
 * @returns {JSX.Element|null} 弹窗组件
 */
const Modal = ({
    isOpen,
    onClose,
    title,
    children,
    size = 'md',
    showCloseButton = true,
    footer,
    closeOnBackdropClick = true,
    className = '',
    loading = false
}) => {
    const backdropRef = useRef(null);
    const contentRef = useRef(null);

    // 处理ESC键关闭
    useEffect(() => {
        const handleEscape = (e) => {
            if (e.key === 'Escape' && isOpen) {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener('keydown', handleEscape);
            // 防止背景滚动
            document.body.style.overflow = 'hidden';
        }

        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.body.style.overflow = 'unset';
        };
    }, [isOpen, onClose]);

    // 处理背景点击
    const handleBackdropClick = (e) => {
        if (closeOnBackdropClick && e.target === e.currentTarget) {
            onClose();
        }
    };

    // 获取弹窗尺寸类名
    const getSizeClass = () => {
        const sizeMap = {
            xs: 'sm:max-w-xs',
            sm: 'sm:max-w-sm',
            md: 'sm:max-w-md',
            lg: 'sm:max-w-lg',
            xl: 'sm:max-w-xl',
            '2xl': 'sm:max-w-2xl',
            '3xl': 'sm:max-w-3xl',
            '4xl': 'sm:max-w-4xl',
            '5xl': 'sm:max-w-5xl',
            '6xl': 'sm:max-w-6xl',
            '7xl': 'sm:max-w-7xl',
            'full': 'sm:max-w-full sm:mx-4'
        };
        return sizeMap[size] || sizeMap.md;
    };

    // 动画变体
    const backdropVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                duration: 0.3,
                ease: [0.25, 0.1, 0.25, 1]
            }
        },
        exit: {
            opacity: 0,
            transition: {
                duration: 0.2,
                ease: [0.25, 0.1, 0.25, 1]
            }
        }
    };

    const modalVariants = {
        hidden: {
            opacity: 0,
            scale: 0.95,
            y: 30,
            filter: "blur(4px)"
        },
        visible: {
            opacity: 1,
            scale: 1,
            y: 0,
            filter: "blur(0px)",
            transition: {
                duration: 0.3,
                ease: [0.25, 0.1, 0.25, 1],
                scale: {
                    type: "spring",
                    damping: 25,
                    stiffness: 300
                }
            }
        },
        exit: {
            opacity: 0,
            scale: 0.98,
            y: 20,
            filter: "blur(2px)",
            transition: {
                duration: 0.2,
                ease: [0.25, 0.1, 0.25, 1]
            }
        }
    };

    return createPortal(
        <AnimatePresence mode="wait">
            {isOpen && (
                <motion.div
                    key="modal"
                    className="fixed inset-0 z-50 overflow-y-auto"
                    initial="hidden"
                    animate="visible"
                    exit="exit"
                >
                    <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                        {/* 背景遮罩 - 增强视觉效果 */}
                        <motion.div
                            ref={backdropRef}
                            variants={backdropVariants}
                            className="fixed inset-0 bg-gray-900/75 backdrop-blur-sm transition-opacity"
                            onClick={handleBackdropClick}
                        />

                        {/* 弹窗内容 - 现代化设计 */}
                        <motion.div
                            ref={contentRef}
                            variants={modalVariants}
                            className={`inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all relative sm:my-8 sm:align-middle ${getSizeClass()} sm:w-full ring-1 ring-black/5 ${className}`}
                        >
                            {/* 弹窗头部 */}
                            {(title || showCloseButton) && (
                                <div className="relative bg-gradient-to-b from-gray-50 to-white px-6 pt-6 pb-5 border-b border-gray-100">
                                    <div className="flex items-center justify-between">
                                        {title && (
                                            <h3 className="text-xl font-semibold text-gray-900 tracking-tight">
                                                {title}
                                            </h3>
                                        )}
                                        {showCloseButton && (
                                            <button
                                                onClick={onClose}
                                                className="ml-4 p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
                                                aria-label="关闭弹窗"
                                            >
                                                <i className="fas fa-times h-5 w-5"></i>
                                            </button>
                                        )}
                                    </div>
                                </div>
                            )}

                            {/* 弹窗内容 */}
                            <div className="relative bg-white px-6 py-6 max-h-[calc(100vh-16rem)] overflow-y-auto custom-scrollbar">
                                {loading ? (
                                    <div className="flex items-center justify-center py-12">
                                        <div className="text-center">
                                            <div className="inline-flex items-center justify-center w-12 h-12 mb-4">
                                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
                                            </div>
                                            <p className="text-gray-500 text-sm">加载中...</p>
                                        </div>
                                    </div>
                                ) : (
                                    children
                                )}
                            </div>

                            {/* 弹窗底部 */}
                            {footer && (
                                <div className="bg-gradient-to-t from-gray-50 to-white px-6 py-4 border-t border-gray-100">
                                    {footer}
                                </div>
                            )}
                        </motion.div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>,
        document.body
    );
};

export default Modal;