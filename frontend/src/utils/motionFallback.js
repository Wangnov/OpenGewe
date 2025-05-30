/**
 * Framer Motion 替代方案 - 使用CSS动画
 * 当framer-motion出现兼容性问题时的备用方案
 */

import React from 'react';

// 简化的motion div组件，使用CSS动画
export const motion = {
    div: ({
        initial,
        animate,
        exit,
        transition,
        variants,
        className,
        children,
        onAnimationComplete,
        ...props
    }) => {
        const [animationState, setAnimationState] = React.useState('initial');

        React.useEffect(() => {
            if (animate) {
                setAnimationState('animate');
            }
        }, [animate]);

        const getAnimationClass = () => {
            if (variants && animate) {
                return `motion-${animate}`;
            }
            return 'motion-default';
        };

        return (
            <div
                className={`${className || ''} ${getAnimationClass()}`}
                onAnimationEnd={onAnimationComplete}
                {...props}
            >
                {children}
            </div>
        );
    }
};

// AnimatePresence 替代
export const AnimatePresence = ({ children, mode = "wait" }) => {
    return <>{children}</>;
};

// 检测framer-motion是否可用
export const checkFramerMotionCompatibility = () => {
    try {
        // 尝试导入framer-motion
        require('framer-motion');
        return true;
    } catch (error) {
        console.warn('Framer Motion compatibility issue detected, falling back to CSS animations');
        return false;
    }
};

// 导出配置
export const motionConfig = {
    fallback: true,
    debug: process.env.NODE_ENV === 'development'
}; 