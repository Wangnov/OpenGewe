# 通知系统迁移指南

## 概述

通知系统已经完全重构，采用了更现代化的架构和更好的性能优化。本指南将帮助您从旧系统迁移到新系统。

## 主要改进

### 1. 性能优化
- ✅ 使用 IndexedDB 替代 localStorage，支持更大的数据存储
- ✅ 使用 useReducer 管理复杂状态，减少重渲染
- ✅ 实现批量更新和防抖优化
- ✅ 支持虚拟滚动（大量通知时）

### 2. UI/UX 提升
- ✅ 使用 Framer Motion 实现流畅动画
- ✅ 统一使用 Modal 组件
- ✅ 支持通知分组和智能合并
- ✅ 改进的移动端体验

### 3. 架构改进
- ✅ 模块化设计，关注点分离
- ✅ 更清晰的数据流
- ✅ 更好的错误处理

## 迁移步骤

### 1. 更新 Context Provider

旧代码：
```jsx
import { NotificationProvider } from './contexts/NotificationContext';

function App() {
  return (
    <NotificationProvider>
      {/* ... */}
    </NotificationProvider>
  );
}
```

新代码：
```jsx
import { NotificationProvider } from './contexts/NotificationContext.new';
import NotificationCenter from './components/notifications/NotificationCenter';

function App() {
  return (
    <NotificationProvider>
      {/* 添加通知中心 */}
      <NotificationCenter />
      {/* ... */}
    </NotificationProvider>
  );
}
```

### 2. 更新通知徽章

旧代码：
```jsx
import NotificationBadge from './components/notifications/NotificationBadge';
```

新代码：
```jsx
import NotificationBadge from './components/notifications/NotificationBadge.new';
```

### 3. 更新 Hook 使用

旧代码：
```jsx
import useNotification from './hooks/useNotification';
```

新代码：
```jsx
import useNotification from './hooks/useNotification.new';

// API 保持兼容，无需修改使用方式
const { success, error, warning, info } = useNotification();
```

### 4. 删除旧组件

以下组件已被替代，可以删除：
- `NotificationBar.jsx` -> 由 `NotificationContainer.jsx` 替代
- `NotificationHistory.jsx` -> 由 `NotificationDrawer.jsx` 替代
- `NotificationItem.jsx` -> 由 `NotificationCard.jsx` 和 `NotificationHistoryItem.jsx` 替代

### 5. 更新配置

新系统支持更多配置选项：

```jsx
const { updateSettings } = useNotification();

updateSettings({
  position: 'top-right', // 通知位置
  enableSound: true, // 启用声音
  enableDesktop: true, // 启用桌面通知
  maxHistoryCount: 200, // 增加历史记录数量
  animationDuration: 300 // 动画时长
});
```

## 新功能

### 1. 通知分组
相似的通知会自动分组，减少视觉干扰：

```jsx
// 连续发送相似通知会自动合并
notification.info('API 调用', '请求成功');
notification.info('API 调用', '请求成功'); // 会合并为一条，显示计数
```

### 2. 智能优先级
高优先级通知会始终显示在前面：

```jsx
notification.error('严重错误', '系统崩溃', { priority: 'high' });
```

### 3. 通知操作
支持自定义操作按钮：

```jsx
notification.warning('确认操作', '是否删除？', {
  actions: [
    {
      label: '确认',
      variant: 'primary',
      onClick: () => console.log('确认删除')
    },
    {
      label: '取消',
      onClick: () => console.log('取消操作')
    }
  ]
});
```

### 4. 搜索和过滤
通知历史支持搜索和多维度过滤。

## 注意事项

1. **数据迁移**：首次使用新系统时，旧的通知数据会自动迁移到 IndexedDB
2. **浏览器兼容性**：新系统需要支持 IndexedDB 的现代浏览器
3. **性能监控**：可以通过 `notificationService.getStats()` 获取性能统计

## 故障排除

### 问题：通知不显示
- 检查是否添加了 `<NotificationCenter />`
- 确认 Context Provider 已正确配置

### 问题：动画卡顿
- 检查是否有其他组件阻塞主线程
- 考虑减少同时显示的通知数量

### 问题：数据丢失
- IndexedDB 可能被浏览器清理，考虑实现云端备份

## 完整示例

```jsx
import React from 'react';
import { NotificationProvider } from './contexts/NotificationContext.new';
import NotificationCenter from './components/notifications/NotificationCenter';
import NotificationBadge from './components/notifications/NotificationBadge.new';
import useNotification from './hooks/useNotification.new';

function App() {
  return (
    <NotificationProvider>
      <NotificationCenter />
      <Header />
      <MainContent />
    </NotificationProvider>
  );
}

function Header() {
  return (
    <header>
      <NotificationBadge />
    </header>
  );
}

function MainContent() {
  const notification = useNotification();

  const handleAction = () => {
    notification.success('操作成功', '数据已保存');
  };

  return (
    <main>
      <button onClick={handleAction}>执行操作</button>
    </main>
  );
}
``` 