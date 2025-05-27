import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5432', // 假设后端API运行在8000端口
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
