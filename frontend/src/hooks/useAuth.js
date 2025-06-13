import { createContext, useContext } from 'react';

// 创建认证上下文
export const AuthContext = createContext(null);

/**
 * 认证钩子，用于在组件中访问认证上下文
 * @returns {Object} 认证上下文
 */
const useAuth = () => {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error('useAuth必须在AuthProvider内部使用');
    }

    return context;
};

export default useAuth; 