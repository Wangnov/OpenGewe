# OpenGewe 前端开发规范

## 项目概述

OpenGewe前端使用现代React技术栈构建，采用Vite作为构建工具。主要技术包括：

- **React 19.1.0** - UI框架
- **React Router DOM 7.6.1** - 路由管理
- **Framer Motion 12.15.0** - 动画库
- **Axios 1.9.0** - HTTP客户端
- **Vite 6.3.5** - 构建工具
- **ESLint** - 代码质量检查

## 开发环境设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 代码检查
npm run lint
```

## 项目结构

```
frontend/
├── public/          # 静态资源
├── src/
│   ├── assets/      # 图片、字体等资源
│   │   ├── auth/    # 认证相关组件
│   │   ├── bots/    # 机器人管理组件
│   │   ├── common/  # 通用组件
│   │   └── notifications/ # 通知系统组件
│   ├── contexts/    # React Context
│   ├── hooks/       # 自定义Hook
│   ├── layouts/     # 布局组件
│   ├── pages/       # 页面组件
│   ├── services/    # API服务层
│   └── utils/       # 工具函数
├── index.css        # 全局样式
└── package.json
```

## 代码规范

### 1. 文件命名
- **组件文件**: PascalCase，如 `BotDetailModal.jsx`
- **Hook文件**: camelCase，以`use`开头，如 `useAuth.js`
- **工具文件**: camelCase，如 `imageProxy.js`
- **Context文件**: PascalCase + Context，如 `AuthContext.jsx`

### 2. 组件设计原则

**必须遵循的组件模板：**

```jsx
import React, { useState, useEffect, useCallback, useMemo } from 'react';
// 其他导入...

/**
 * 组件描述
 * @param {Object} props - 组件属性
 * @param {string} props.example - 属性说明
 * @returns {JSX.Element} 组件描述
 */
const ComponentName = ({ example, ...otherProps }) => {
    // 1. 状态声明
    const [state, setState] = useState(initialValue);
    
    // 2. Context和Hook使用
    const { contextValue } = useContext(SomeContext);
    const customHook = useCustomHook();
    
    // 3. 计算属性（使用useMemo优化）
    const computedValue = useMemo(() => {
        return expensiveCalculation(state);
    }, [state]);
    
    // 4. 副作用（useEffect）
    useEffect(() => {
        // 副作用逻辑
        return () => {
            // 清理逻辑
        };
    }, [dependencies]);
    
    // 5. 事件处理函数（使用useCallback优化）
    const handleClick = useCallback((event) => {
        // 事件处理逻辑
    }, [dependencies]);
    
    // 6. 渲染逻辑
    return (
        <div className="component-container">
            {/* JSX内容 */}
        </div>
    );
};

export default ComponentName;
```

### 3. Hook使用规范

**性能优化必须使用：**
- `useCallback` - 包装所有事件处理函数
- `useMemo` - 包装复杂计算和配置对象
- 合理使用依赖数组，避免无限重渲染

**示例：**
```jsx
// ✅ 正确的事件处理
const handleSubmit = useCallback(async (formData) => {
    await submitData(formData);
}, [submitData]);

// ✅ 正确的计算属性
const filteredData = useMemo(() => {
    return data.filter(item => item.status === 'active');
}, [data]);

// ✅ 正确的配置对象
const navItems = useMemo(() => [
    { to: '/dashboard', icon: 'fas fa-chart-pie', label: '仪表盘' },
    { to: '/bots', icon: 'fab fa-weixin', label: '机器人管理' }
], []);
```

## 样式规范

### 1. 颜色系统

**必须使用CSS变量，禁止硬编码颜色值：**

```css
/* ✅ 正确使用 */
.button {
    background-color: var(--color-primary);
    color: var(--color-gray-50);
}

/* ❌ 错误示例 */
.button {
    background-color: #2aae67;
    color: #F8FAFC;
}
```

**主要颜色变量：**
```css
--color-primary: #2aae67;        /* 主色调 */
--color-secondary: #9333ea;       /* 辅助色 */
--color-accent: #3b82f6;         /* 强调色 */
--color-gray-[50-900]: ...;      /* 灰度系列 */
--bg-glass: rgba(255, 255, 255, 0.7); /* 玻璃效果 */
```

### 2. 动画规范

**优先使用CSS动画，特殊情况使用framer-motion：**

**CSS动画（推荐）：**
```css
/* 模态框动画 */
@keyframes modal-backdrop-enter {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes modal-content-enter {
    from { 
        opacity: 0; 
        transform: scale(0.95) translateY(-10px); 
    }
    to { 
        opacity: 1; 
        transform: scale(1) translateY(0); 
    }
}

.modal-backdrop {
    animation: modal-backdrop-enter 0.3s ease-out;
}

.modal-content {
    animation: modal-content-enter 0.3s ease-out;
}
```

**Framer Motion（特殊场景）：**
```jsx
// 仅用于复杂的序列动画或手势交互
<motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -20 }}
    transition={{ duration: 0.3 }}
>
    内容
</motion.div>
```

**动画使用原则：**
- 模态框开启：CSS动画
- 模态框关闭：CSS动画 + DOM操作控制
- 列表项动画：framer-motion
- 页面转换：React Router + CSS
- 加载动画：CSS + LoadingSpinner组件

### 3. 响应式设计

**使用断点变量：**
```css
/* 移动端优先设计 */
.component {
    /* 默认移动端样式 */
}

@media (min-width: 768px) {
    .component {
        /* 平板样式 */
    }
}

@media (min-width: 1024px) {
    .component {
        /* 桌面样式 */
    }
}
```

## 组件开发指南

### 1. 弹窗/模态框开发规范

**必须遵循的弹窗模板：**

```jsx
import React, { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';

const ModalComponent = ({ isOpen, onClose, children }) => {
    const [isClosing, setIsClosing] = useState(false);
    const backdropRef = useRef(null);
    const contentRef = useRef(null);

    // 关闭处理
    const handleClose = useCallback(() => {
        setIsClosing(true);
        
        // 添加退出动画class
        const backdrop = backdropRef.current;
        const content = contentRef.current;
        
        if (backdrop) backdrop.classList.add('modal-backdrop-exit');
        if (content) content.classList.add('modal-content-exit');
        
        // 等待动画完成后执行回调
        const cleanup = () => {
            setIsClosing(false);
            onClose();
        };
        
        if (content) {
            content.addEventListener('animationend', cleanup, { once: true });
            setTimeout(cleanup, 350); // 动画超时保护
        } else {
            setTimeout(cleanup, 300);
        }
    }, [onClose]);

    // 背景点击关闭
    const handleBackdropClick = useCallback((e) => {
        if (e.target === e.currentTarget) {
            handleClose();
        }
    }, [handleClose]);

    // ESC键关闭
    useEffect(() => {
        const handleEscape = (e) => {
            if (e.key === 'Escape' && isOpen) {
                handleClose();
            }
        };

        if (isOpen) {
            document.addEventListener('keydown', handleEscape);
            document.body.style.overflow = 'hidden';
        }

        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.body.style.overflow = '';
        };
    }, [isOpen, handleClose]);

    if (!isOpen) return null;

    return createPortal(
        <div
            ref={backdropRef}
            className="modal-backdrop fixed inset-0 z-50 overflow-y-auto"
            onClick={handleBackdropClick}
        >
            <div className="flex items-center justify-center min-h-screen px-4">
                <div
                    ref={contentRef}
                    className="modal-content bg-white rounded-xl shadow-xl max-w-md w-full"
                    onClick={(e) => e.stopPropagation()}
                >
                    {children}
                </div>
            </div>
        </div>,
        document.body
    );
};
```

**关键点：**
- 必须使用`createPortal`渲染到body
- 必须处理背景点击、ESC键关闭
- 必须添加关闭动画
- 必须防止body滚动

### 2. 表单组件规范

**统一的表单验证：**
```jsx
const useFormValidation = (initialValues, validationRules) => {
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({});
    
    const validate = useCallback((fieldName, value) => {
        const rule = validationRules[fieldName];
        if (!rule) return '';
        
        return rule(value) || '';
    }, [validationRules]);
    
    const setValue = useCallback((name, value) => {
        setValues(prev => ({ ...prev, [name]: value }));
        const error = validate(name, value);
        setErrors(prev => ({ ...prev, [name]: error }));
    }, [validate]);
    
    return { values, errors, setValue, setValues, setErrors };
};
```

## 状态管理规范

### 1. Context使用原则

**单一职责原则：**
- AuthContext - 仅处理用户认证
- NotificationContext - 仅处理通知系统
- 避免巨大的全局Context

**Context结构模板：**
```jsx
import React, { createContext, useContext, useMemo } from 'react';

const SomeContext = createContext();

export const SomeProvider = ({ children }) => {
    // 状态和逻辑
    
    const value = useMemo(() => ({
        // 所有需要传递的值
    }), [/* 依赖项 */]);
    
    return (
        <SomeContext.Provider value={value}>
            {children}
        </SomeContext.Provider>
    );
};

// 自定义Hook
export const useSome = () => {
    const context = useContext(SomeContext);
    if (!context) {
        throw new Error('useSome must be used within SomeProvider');
    }
    return context;
};
```

### 2. 数据流设计

**单向数据流：**
```
Context/Service → Hook → Component → User Action → Service → Context
```

## API集成规范

### 1. 服务层设计

**必须使用统一的API客户端：**

```javascript
// services/api.js
import axios from 'axios';

const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// 响应拦截器
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;
```

**服务层模板：**
```javascript
// services/someService.js
import api from './api';

const someService = {
    async getData(params) {
        try {
            const response = await api.get('/endpoint', { params });
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.message || '获取数据失败');
        }
    },
    
    async createData(data) {
        try {
            const response = await api.post('/endpoint', data);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.message || '创建失败');
        }
    }
};

export default someService;
```

### 2. 错误处理统一化

**必须使用useApiLoading Hook：**
```jsx
import useApiLoading from '../hooks/useApiLoading';
import useNotification from '../hooks/useNotification';

const Component = () => {
    const { loading, executeWithLoading } = useApiLoading();
    const { success, error } = useNotification();
    
    const handleSubmit = useCallback(async (data) => {
        try {
            const result = await executeWithLoading(() => 
                someService.createData(data)
            );
            success('操作成功', '数据已保存');
            return result;
        } catch (err) {
            error('操作失败', err.message);
        }
    }, [executeWithLoading, success, error]);
    
    return (
        <div>
            {loading && <LoadingSpinner />}
            {/* 其他内容 */}
        </div>
    );
};
```

## 图片和资源处理

### 1. CachedImage使用规范

**必须使用CachedImage替代img标签：**

```jsx
import CachedImage from '../components/common/CachedImage';

// ✅ 正确使用
<CachedImage
    src={imageUrl}
    alt="描述"
    className="w-10 h-10 rounded-full"
    onLoad={() => console.log('图片加载完成')}
    onError={() => console.log('图片加载失败')}
/>

// ❌ 错误示例
<img src={imageUrl} alt="描述" className="w-10 h-10 rounded-full" />
```

### 2. 图片代理规范

**微信图片必须使用代理：**
```jsx
import { useProxiedImage } from '../utils/imageProxy';

const Component = ({ wechatImageUrl }) => {
    const { imageUrl, loading, error } = useProxiedImage(wechatImageUrl, true);
    
    if (loading) return <LoadingSpinner size="sm" />;
    if (error) return <div>图片加载失败</div>;
    
    return <CachedImage src={imageUrl} alt="微信图片" />;
};
```

## 通知系统使用

### 1. 通知类型和优先级

**必须使用正确的通知类型：**
```jsx
import useNotification from '../hooks/useNotification';

const Component = () => {
    const { success, warning, error, info, system } = useNotification();
    
    const handleSuccess = () => {
        success('操作成功', '数据已保存'); // 自动消失
    };
    
    const handleWarning = () => {
        warning('注意', '请检查输入数据', { duration: 0 }); // 不自动消失
    };
    
    const handleError = () => {
        error('错误', '网络连接失败', { 
            duration: 0,
            priority: 'high' 
        });
    };
    
    const handleInfo = () => {
        info('提示', '这是一条信息');
    };
    
    const handleSystem = () => {
        system('系统通知', '服务器维护中', {
            priority: 'high',
            isPinned: true
        });
    };
};
```

### 2. 用户反馈设计

**操作反馈模式：**
- 成功操作：绿色通知，3秒自动消失
- 警告信息：黄色通知，手动关闭
- 错误信息：红色通知，手动关闭，高优先级
- 系统通知：蓝色通知，可固定显示

## 测试和部署

### 1. 代码检查规范

**ESLint规则：**
- 必须修复所有errors
- 建议修复warnings
- 禁用`no-unused-vars`对React、motion等的检查

### 2. 构建优化

**Vite配置优化：**
```javascript
// vite.config.js
export default defineConfig({
    plugins: [react()],
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ['react', 'react-dom'],
                    router: ['react-router-dom'],
                    motion: ['framer-motion']
                }
            }
        }
    }
});
```

## 避免的反模式

### 1. 组件修改注意事项

**严禁破坏性修改：**
- 不得随意删除已有的DOM结构
- 不得移除组件的核心功能
- 修改动画时必须保持原有的视觉设计
- 不得改变组件的API接口

**正确的修改方式：**
```jsx
// ✅ 正确：仅添加功能，保持原有结构
const Component = ({ ...originalProps }) => {
    // 新增状态和逻辑
    const [newFeature, setNewFeature] = useState(false);
    
    return (
        <OriginalStructure>
            {/* 保持原有内容 */}
            {newFeature && <AdditionalFeature />}
        </OriginalStructure>
    );
};

// ❌ 错误：删除原有结构
const Component = () => {
    return <CompletelyNewStructure />; // 破坏性修改
};
```

### 2. 性能陷阱

**避免的性能问题：**
```jsx
// ❌ 避免：内联对象导致重渲染
<Component style={{ marginTop: 10 }} />

// ✅ 正确：使用CSS类或useMemo
const styles = useMemo(() => ({ marginTop: 10 }), []);
<Component style={styles} />

// ❌ 避免：未使用依赖数组
useEffect(() => {
    fetchData();
}); // 每次渲染都执行

// ✅ 正确：正确的依赖数组
useEffect(() => {
    fetchData();
}, [dependency]);
```


## 总结

这些规范确保了代码质量、一致性和可维护性。在开发新组件时，请严格遵循这些指导原则，并参考现有组件的实现方式。特别注意：

1. **性能优化**：必须使用useCallback和useMemo
2. **动画处理**：优先CSS动画，合理使用framer-motion
3. **图片处理**：必须使用CachedImage和代理系统
4. **通知系统**：正确使用类型和优先级
5. **避免破坏性修改**：保持原有结构和功能完整性
