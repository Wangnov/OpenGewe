import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react({
    // 确保JSX运行时正确配置
    jsxRuntime: 'automatic'
  })],
  optimizeDeps: {
    // 预构建framer-motion以避免运行时问题
    include: ['framer-motion', 'react', 'react-dom']
  },
  define: {
    // 确保React全局可用
    global: 'globalThis'
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5432', // 后端API运行在5432端口
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
