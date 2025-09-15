<!--
  性能优化示例组件
  展示如何在实际组件中使用API优化工具
-->

<template>
  <div class="optimized-component">
    <!-- Loading状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中... {{ Math.round(loadingProgress) }}%</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-container">
      <p>❌ 加载失败: {{ error }}</p>
      <button @click="retryLoad" class="retry-btn">重试</button>
    </div>

    <!-- 正常内容 -->
    <div v-else class="content">
      <h2>优化后的组件示例</h2>
      
      <!-- 必需数据 -->
      <div v-if="essentialData" class="essential-data">
        <h3>核心数据</h3>
        <pre>{{ essentialData }}</pre>
      </div>

      <!-- 可选数据（懒加载） -->
      <div v-if="optionalData" class="optional-data">
        <h3>扩展数据</h3>
        <pre>{{ optionalData }}</pre>
      </div>
      
      <!-- 缓存状态显示 -->
      <div v-if="showDebugInfo" class="debug-info">
        <h4>调试信息</h4>
        <p>缓存命中: {{ cacheStats.totalCached }} 项</p>
        <p>进行中请求: {{ cacheStats.pendingRequests }} 个</p>
        <button @click="clearCache">清除缓存</button>
      </div>

      <!-- 实时数据连接状态 -->
      <div v-if="wsConnected" class="ws-status">
        🟢 实时连接已建立
      </div>
      <div v-else class="ws-status">
        🔴 实时连接断开
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useApiOptimization, usePageLoadOptimization, useRealtimeOptimization } from '@/composables/useApiOptimization.js'
import { p2paiService } from '@/services/index.js'
import performanceMonitor from '@/utils/performanceMonitor.js'

// 优化工具
const { cachedApiCall, getCacheStats, clearCache: clearApiCache } = useApiOptimization()
const { loading, loadingProgress, error, optimizedPageLoad } = usePageLoadOptimization()
const { optimizedWebSocket, cleanupConnections } = useRealtimeOptimization()

// 数据状态
const essentialData = ref(null)
const optionalData = ref(null)
const wsConnected = ref(false)
const showDebugInfo = ref(import.meta.env.DEV)

// 缓存统计
const cacheStats = computed(() => getCacheStats())

// WebSocket连接
let ws = null

/**
 * 加载必需数据
 */
async function loadEssentialData() {
  console.log('📊 Loading essential data...')
  
  // 使用缓存的API调用，5分钟有效期
  essentialData.value = await cachedApiCall(
    'projects-essential', 
    () => p2paiService.projects.getProjects({ limit: 5 }), 
    5 * 60 * 1000
  )
}

/**
 * 加载可选数据
 */
async function loadOptionalData() {
  console.log('🔄 Loading optional data...')
  
  // 延迟加载可选数据，不阻塞UI
  setTimeout(async () => {
    try {
      optionalData.value = await cachedApiCall(
        'projects-stats',
        () => p2paiService.projects.getProjectStats(),
        10 * 60 * 1000
      )
    } catch (err) {
      console.warn('Optional data loading failed:', err)
      // 可选数据加载失败不影响主要功能
    }
  }, 500)
}

/**
 * 建立WebSocket连接
 */
function establishWebSocketConnection() {
  ws = optimizedWebSocket('ws://localhost:8000/api/p2pai/training/ws/demo', {
    onOpen: () => {
      wsConnected.value = true
      console.log('✅ WebSocket connected')
    },
    onMessage: (data) => {
      console.log('📨 Received:', data)
      // 处理实时数据更新
    },
    onError: (error) => {
      console.error('❌ WebSocket error:', error)
      wsConnected.value = false
    },
    onClose: () => {
      console.log('🔌 WebSocket closed')
      wsConnected.value = false
    }
  }, {
    reconnectDelay: 3000,
    maxReconnectAttempts: 5,
    heartbeatInterval: 30000
  })
}

/**
 * 重试加载
 */
async function retryLoad() {
  await loadData()
}

/**
 * 清除缓存
 */
function clearCache() {
  clearApiCache()
  console.log('🧹 Cache cleared')
}

/**
 * 优化的数据加载
 */
async function loadData() {
  const pageMonitor = performanceMonitor.monitorPageLoad('OptimizedComponent')
  
  try {
    await optimizedPageLoad([], {
      essential: [
        loadEssentialData
      ],
      optional: [
        loadOptionalData,
        establishWebSocketConnection
      ]
    })
  } finally {
    pageMonitor.end()
  }
}

// 生命周期
onMounted(async () => {
  console.group('🚀 OptimizedComponent mounted')
  console.log('Starting optimized data loading...')
  
  await loadData()
  
  console.log('Component fully loaded with optimizations')
  console.groupEnd()
})

onUnmounted(() => {
  console.log('🧹 Cleaning up OptimizedComponent')
  
  // 清理WebSocket连接
  cleanupConnections()
})
</script>

<style scoped>
.optimized-component {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.loading-container {
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 40px;
  color: #e74c3c;
}

.retry-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.retry-btn:hover {
  background: #2980b9;
}

.content {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.essential-data, .optional-data {
  background: #f8f9fa;
  padding: 15px;
  margin: 15px 0;
  border-radius: 4px;
  border-left: 4px solid #3498db;
}

.debug-info {
  background: #fff3cd;
  padding: 15px;
  margin: 15px 0;
  border-radius: 4px;
  border-left: 4px solid #ffc107;
  font-size: 14px;
}

.debug-info button {
  background: #ffc107;
  color: #212529;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 12px;
  margin-top: 10px;
}

.ws-status {
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
  font-size: 14px;
  text-align: center;
}

pre {
  background: #f4f4f4;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}
</style>