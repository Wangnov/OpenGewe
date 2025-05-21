import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import viteCompression from 'vite-plugin-compression';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({
      // 确保与React 19兼容
      jsxRuntime: 'automatic',
      jsxImportSource: 'react',
      babel: {
        plugins: [
          // 添加转换指令
          ['@babel/plugin-transform-react-jsx', { runtime: 'automatic' }]
        ]
      }
    }),
    viteCompression({
      algorithm: 'gzip',
      threshold: 10240, // 大于10KB的文件才会被压缩
    }),
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5432,
    proxy: {
      '/api': {
        target: 'http://localhost:5433',
        changeOrigin: true,
      },
    },
  },
  optimizeDeps: {
    include: [
      'react', 
      'react-dom', 
      'react-router-dom', 
      'axios', 
      '@mantine/core', 
      '@mantine/hooks',
      'lodash',
      // Font Awesome相关包预构建
      '@fortawesome/fontawesome-svg-core',
      '@fortawesome/free-solid-svg-icons',
      '@fortawesome/free-regular-svg-icons',
      '@fortawesome/free-brands-svg-icons',
      '@fortawesome/react-fontawesome',
    ],
    force: true,
    esbuildOptions: {
      define: {
        'process.env.NODE_ENV': JSON.stringify('production'),
      },
    },
  },
  build: {
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'router-vendor': ['react-router', 'react-router-dom'],
          'ui-vendor': ['@mantine/core', '@mantine/hooks', '@mantine/form', '@mantine/notifications'],
          'fontawesome-vendor': [
            '@fortawesome/fontawesome-svg-core',
            '@fortawesome/free-solid-svg-icons',
            '@fortawesome/free-regular-svg-icons',
            '@fortawesome/free-brands-svg-icons',
            '@fortawesome/react-fontawesome',
          ],
        },
      },
    },
    minify: 'esbuild',
    sourcemap: false,
  },
  esbuild: {
    logOverride: { 'this-is-undefined-in-esm': 'silent' },
  },
});
