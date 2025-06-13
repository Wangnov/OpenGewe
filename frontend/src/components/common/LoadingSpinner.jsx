import React from 'react';
import { motion } from 'framer-motion';

/**
 * 加载动画组件
 * @param {Object} props - 组件属性
 * @param {string} props.size - 尺寸大小 'sm' | 'md' | 'lg'
 * @param {string} props.text - 加载文本
 * @param {boolean} props.overlay - 是否显示遮罩层
 * @returns {JSX.Element} 加载动画组件
 */
const LoadingSpinner = ({ 
  size = 'md', 
  text = '加载中...', 
  overlay = false 
}) => {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  };

  const spinnerVariants = {
    animate: {
      rotate: 360,
      transition: {
        duration: 1,
        repeat: Infinity,
        ease: "linear"
      }
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { duration: 0.2 }
    }
  };

  const dotVariants = {
    animate: {
      scale: [1, 1.2, 1],
      opacity: [0.6, 1, 0.6],
      transition: {
        duration: 1.2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  const LoadingContent = (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="flex flex-col items-center justify-center space-y-4"
    >
      {/* 主要加载动画 */}
      <div className="relative">
        {/* 外圈渐变圆环 */}
        <motion.div
          variants={spinnerVariants}
          animate="animate"
          className={`${sizeClasses[size]} rounded-full border-2 border-transparent bg-gradient-to-r from-purple-500 via-blue-500 to-cyan-500 bg-clip-border`}
          style={{
            background: 'conic-gradient(from 0deg, var(--color-secondary), var(--color-accent), var(--color-primary), var(--color-secondary))',
            padding: '2px'
          }}
        >
          <div className="w-full h-full rounded-full bg-white"></div>
        </motion.div>
        
        {/* 内部脉动点 */}
        <motion.div
          variants={dotVariants}
          animate="animate"
          className="absolute inset-0 flex items-center justify-center"
        >
          <div 
            className="w-2 h-2 rounded-full"
            style={{
              background: 'linear-gradient(135deg, var(--color-secondary), var(--color-accent))'
            }}
          ></div>
        </motion.div>
      </div>

      {/* 加载文本 */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.3 }}
        className={`${textSizeClasses[size]} font-medium text-gray-600 text-center`}
      >
        {text}
        <motion.span
          animate={{ opacity: [0, 1, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
        >
          ...
        </motion.span>
      </motion.div>
    </motion.div>
  );

  if (overlay) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-white bg-opacity-80 backdrop-blur-sm flex items-center justify-center z-50"
        style={{ backdropFilter: 'blur(4px)' }}
      >
        {LoadingContent}
      </motion.div>
    );
  }

  return LoadingContent;
};

export default LoadingSpinner; 