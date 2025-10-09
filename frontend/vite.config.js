import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          // Enable production optimizations
          hoistStatic: true,
          cacheHandlers: true,
        }
      }
    }),
    // Vue DevTools 已禁用 - 移除页面底部的Vue logo
    // vueDevTools({
    //   launchEditor: 'code',
    //   componentInspector: true,
    //   enableToast: false,
    //   ui: { port: 0 },
    // }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    // Build optimizations
    target: 'esnext',
    minify: 'terser',
    rollupOptions: {
      output: {
        // Manual chunk splitting for better caching
        manualChunks: {
          // Vendor chunks
          'vue-vendor': ['vue', 'vue-router'],
          'chart-vendor': ['chart.js'],
          'ui-components': [
            './src/components/ui/StatCard.vue',
            './src/components/ui/ProgressBar.vue',
            './src/components/ui/Modal.vue',
            './src/components/ui/LoadingSpinner.vue',
            './src/components/ui/Notification.vue',
            './src/components/ui/Chart.vue'
          ]
        }
      }
    },
    // Chunk size warnings
    chunkSizeWarningLimit: 1000,
    // Source maps for production debugging (optional)
    sourcemap: false,
    // Enable CSS code splitting
    cssCodeSplit: true,
    // Terser options for better compression
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      }
    }
  },
  server: {
    // Development server optimizations
    host: '0.0.0.0',
    port: 5173,
    hmr: {
      overlay: false, // Disable error overlay for better performance
      // 使用服务器IP地址，确保HMR在服务器环境下正常工作
      host: '175.178.24.56',
      clientPort: 5173,
      port: 5173,
      protocol: 'ws'
    },
    proxy: {
      // 将本地 /edge-train/* 转发到训练服务，避免浏览器CORS限制
      '/edge-train': {
        target: 'http://12.148.158.61:6677',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/edge-train/, '')
      },
      // 代理monitorRayCluster请求到监控服务
      '/monitorRayCluster': {
        target: 'http://12.148.158.61:6677',
        changeOrigin: true,
        secure: false
      },
      // 代理API请求到后端服务
      '/api': {
        target: 'http://175.178.24.56:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  optimizeDeps: {
    // Pre-bundle dependencies for faster dev startup
    include: [
      'vue',
      'vue-router',
      'chart.js',
      '@heroicons/vue/24/outline',
      '@heroicons/vue/24/solid'
    ]
  },
  // CSS preprocessing optimizations
  css: {
    devSourcemap: false,
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/assets/variables.scss";`
      }
    }
  }
})
