# OpenGewe 前端开发指南

## 开发环境设置

### 依赖安装

```bash
npm install
```

### 开发服务器启动

```bash
npm run dev
```

开发服务器将在 http://localhost:5432 上运行

## 性能优化指南

### 解决页面加载慢的问题

如果在开发过程中遇到页面加载慢、大量请求 chunk 文件的问题，可以：

1. **预构建依赖**

   在启动开发服务器前，先运行依赖预构建：

   ```bash
   npx vite optimize
   ```
   
   或使用我们提供的快捷命令：
   
   ```bash
   npm run optimize
   ```

2. **优化 NPM 依赖缓存**

   清理和重建 NPM 缓存：

   ```bash
   npm cache clean --force
   npm cache verify
   ```

3. **开发模式优化**

   启动时添加 `--force` 参数，强制重新优化依赖：

   ```bash
   npm run dev -- --force
   ```

4. **使用我们的 Font Awesome 图标组件**

   项目使用 Font Awesome 图标库，并提供了专门的图标加载优化组件：
   
   ```typescript
   import { Icons } from '@/utils/fa-icon-loader';
   
   // 使用预定义图标
   <Icons.User size={24} color="#3498db" />
   
   // 使用不同类型的图标：solid(默认), regular, brand
   {Icons.icon("github", "brand", { size: 32 })}
   {Icons.icon("heart", "regular", { size: 24, color: "red" })}
   ```

### 解决后端连接问题

如果前端无法连接到后端 API，请检查：

1. 确保后端服务在正确的端口运行（5433）
2. 确保前端开发服务器在正确的端口运行（5432）
3. 检查 vite.config.ts 中的代理配置指向正确的后端地址
4. 使用浏览器开发工具检查网络请求，查看具体错误信息

```typescript
// vite.config.ts 代理配置示例
server: {
  port: 5432,
  proxy: {
    '/api': {
      target: 'http://localhost:5433',
      changeOrigin: true,
    },
  },
}
```

## 构建生产版本

```bash
npm run build
```

## 常见问题

### Q: 页面加载非常慢，请求了大量的 chunk 文件

解决方法：
- 使用我们提供的 Font Awesome 图标组件 `@/utils/fa-icon-loader`
- 执行 `npm run optimize` 预构建依赖
- 检查项目依赖是否过多，考虑移除不必要的依赖

### Q: API 请求没有响应

解决方法：
- 确保后端服务正在运行，端口为 5433
- 确保前端开发服务器正在运行，端口为 5432
- 使用 `npm run check-backend` 检查后端服务状态
- 检查控制台中的API请求日志，特别注意URL格式是否正确（不要使用 /v1 前缀） 