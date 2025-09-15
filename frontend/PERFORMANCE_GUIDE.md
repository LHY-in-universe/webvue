# 🚀 性能优化指南

## 网站变慢的常见原因及解决方案

### 1. **API调用阻塞问题**

#### 问题表现
- 页面加载时白屏时间长
- 用户交互响应延迟
- 数据更新卡顿

#### 解决方案
```javascript
// ❌ 同步阻塞方式
const data = await apiCall()
setData(data)

// ✅ 异步优化方式
import { useApiOptimization } from '@/composables/useApiOptimization.js'

const { cachedApiCall } = useApiOptimization()
const data = await cachedApiCall('projects-list', () => apiCall(), 5 * 60 * 1000) // 5分钟缓存
```

### 2. **重复API请求**

#### 问题表现
- 同一接口被多次调用
- 网络资源浪费
- 后端压力增大

#### 解决方案
```javascript
// ✅ 使用缓存和防重复请求
const { cachedApiCall } = useApiOptimization()

// 自动防止重复请求，使用缓存
const result = await cachedApiCall('user-profile', getUserProfile)
```

### 3. **页面加载策略问题**

#### 问题表现
- 所有数据一次性加载
- 必需数据和可选数据混在一起
- 加载进度不明确

#### 解决方案
```javascript
// ✅ 分层加载策略
import { usePageLoadOptimization } from '@/composables/useApiOptimization.js'

const { optimizedPageLoad } = usePageLoadOptimization()

await optimizedPageLoad([], {
  essential: [
    () => loadUserProfile(),
    () => loadBasicData()
  ],
  optional: [
    () => loadAnalytics(),
    () => loadRecommendations()
  ]
})
```

### 4. **WebSocket连接管理**

#### 问题表现
- 多个重复连接
- 连接不稳定
- 内存泄漏

#### 解决方案
```javascript
// ✅ 优化的WebSocket管理
import { useRealtimeOptimization } from '@/composables/useApiOptimization.js'

const { optimizedWebSocket, cleanupConnections } = useRealtimeOptimization()

const ws = optimizedWebSocket('/ws/training', {
  onMessage: handleMessage,
  onError: handleError
}, {
  reconnectDelay: 3000,
  heartbeatInterval: 30000
})

// 组件卸载时清理
onUnmounted(() => {
  cleanupConnections()
})
```

## 🔧 性能监控工具

### 1. **API性能监控**

```javascript
// 在浏览器控制台中使用
window.performance.report() // 查看详细性能报告
window.performance.monitor.getApiStats() // 查看API统计
```

### 2. **缓存管理**

```javascript
// 查看缓存状态
window.apiOptimization.getCacheStats()

// 清理缓存
window.apiOptimization.clearCache() // 清理所有
window.apiOptimization.clearCache('projects') // 清理特定模式
```

### 3. **API测试工具**

```javascript
// 测试API性能
window.apiTest.runFullAPITest()
window.apiTest.testBackendConnection()
```

## ⚡ 最佳实践

### 1. **组件级优化**

```vue
<template>
  <div>
    <!-- 使用loading状态 -->
    <LoadingSpinner v-if="loading" />
    <ProjectList v-else :projects="projects" />
  </div>
</template>

<script setup>
import { useApiOptimization, usePageLoadOptimization } from '@/composables/useApiOptimization.js'

const { cachedApiCall } = useApiOptimization()
const { loading, optimizedPageLoad } = usePageLoadOptimization()

// 优化的数据加载
onMounted(async () => {
  const loadMonitor = performanceMonitor.monitorPageLoad('ProjectList')
  
  await optimizedPageLoad([], {
    essential: [
      () => cachedApiCall('projects', getProjects, 5 * 60 * 1000)
    ],
    optional: [
      () => cachedApiCall('stats', getStats, 10 * 60 * 1000)
    ]
  })
  
  loadMonitor.end()
})
</script>
```

### 2. **状态管理优化**

```javascript
// stores/projects.js
import { defineStore } from 'pinia'
import { useApiOptimization } from '@/composables/useApiOptimization.js'

export const useProjectsStore = defineStore('projects', () => {
  const { cachedApiCall, batchApiCalls } = useApiOptimization()
  
  const fetchProjects = async () => {
    // 使用缓存避免重复请求
    return await cachedApiCall('projects-list', getProjects, 5 * 60 * 1000)
  }
  
  const fetchProjectsBatch = async (projectIds) => {
    // 批量请求优化
    const calls = projectIds.map(id => ({
      key: `project-${id}`,
      call: () => getProject(id),
      ttl: 5 * 60 * 1000
    }))
    
    return await batchApiCalls(calls, 3) // 限制并发数
  }
})
```

### 3. **环境配置优化**

```javascript
// .env 文件
VITE_DEBUG_API=true  # 开发环境启用API调试
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
```

## 📊 性能指标

### 良好的性能指标
- **API响应时间**: < 500ms
- **页面加载时间**: < 2s
- **首次内容绘制**: < 1s
- **API成功率**: > 99%

### 监控命令
```javascript
// 获取当前性能数据
const stats = window.performance.monitor.getApiStats()
console.table(stats)

// 监控页面加载
const monitor = window.performance.monitor.monitorPageLoad('HomePage')
// ... 页面加载完成后
monitor.end()
```

## 🐛 常见问题排查

### 1. **API调用过慢**
- 检查网络连接
- 查看控制台的API响应时间
- 使用 `window.performance.report()` 分析

### 2. **页面卡顿**
- 检查是否有同步API调用阻塞UI
- 使用浏览器Performance工具分析
- 检查WebSocket连接是否正常

### 3. **内存泄漏**
- 确保WebSocket连接在组件卸载时清理
- 检查API缓存大小
- 使用 `cleanupConnections()` 清理连接

## 🎯 优化检查清单

- [ ] 使用API缓存减少重复请求
- [ ] 实施分层数据加载策略
- [ ] 添加loading状态提升用户体验
- [ ] 优化WebSocket连接管理
- [ ] 启用性能监控
- [ ] 设置合理的超时时间
- [ ] 实施错误重试机制
- [ ] 使用防抖优化频繁操作