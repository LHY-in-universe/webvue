import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

const app = createApp(App)

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err)
  console.error('Component instance:', instance)
  console.error('Error info:', info)
  
  // 尝试使用通知系统显示错误（如果已初始化）
  if (window.$notify) {
    const errorMessage = err.message || 'An unexpected error occurred'
    window.$notify.error(errorMessage)
  }
}

// Global warning handler (development only)
if (import.meta.env.DEV) {
  app.config.warnHandler = (msg, instance, trace) => {
    console.warn('Vue warning:', msg)
    console.warn('Trace:', trace)
  }
}

// Install plugins
app.use(createPinia())
app.use(router)

// 开发环境下加载调试工具
if (import.meta.env.DEV && import.meta.env.VITE_DEBUG_API) {
  Promise.all([
    import('./utils/apiTest.js'),
    import('./utils/performanceMonitor.js'),
    import('./composables/useApiOptimization.js')
  ]).then(() => {
    console.log('🔧 Development tools loaded:')
    console.log('   • API testing: window.apiTest')
    console.log('   • Performance monitoring: window.performance')
    console.log('   • Cache management: window.apiOptimization')
    console.log('   • Run window.performance.report() for performance analysis')
  })
}

app.mount('#app')
