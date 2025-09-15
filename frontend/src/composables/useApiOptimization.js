/**
 * API Optimization Composable
 * 提供API调用优化功能，包括缓存、防抖、批量请求等
 */

import { ref, reactive } from 'vue'

// 全局缓存存储
const apiCache = reactive(new Map())

// 正在进行的请求存储（防止重复请求）
const pendingRequests = reactive(new Map())

/**
 * API优化Hook
 */
export function useApiOptimization() {
  /**
   * 带缓存的API调用
   * @param {string} cacheKey - 缓存键
   * @param {Function} apiCall - API调用函数
   * @param {number} ttl - 缓存生存时间（毫秒）
   * @returns {Promise} API响应
   */
  async function cachedApiCall(cacheKey, apiCall, ttl = 5 * 60 * 1000) {
    // 检查缓存
    const cached = apiCache.get(cacheKey)
    if (cached && Date.now() - cached.timestamp < ttl) {
      console.log(`🎯 Cache hit for: ${cacheKey}`)
      return cached.data
    }

    // 检查是否有正在进行的相同请求
    if (pendingRequests.has(cacheKey)) {
      console.log(`⏳ Waiting for pending request: ${cacheKey}`)
      return await pendingRequests.get(cacheKey)
    }

    // 创建新的API调用
    const requestPromise = apiCall()
    pendingRequests.set(cacheKey, requestPromise)

    try {
      const data = await requestPromise
      
      // 缓存结果
      apiCache.set(cacheKey, {
        data,
        timestamp: Date.now()
      })
      
      console.log(`💾 Cached result for: ${cacheKey}`)
      return data
    } finally {
      // 清理pending request
      pendingRequests.delete(cacheKey)
    }
  }

  /**
   * 批量API调用
   * @param {Array} apiCalls - API调用数组 [{key, call}]
   * @param {number} concurrency - 并发数限制
   * @returns {Promise<Object>} 批量结果
   */
  async function batchApiCalls(apiCalls, concurrency = 3) {
    const results = {}
    const chunks = []
    
    // 分批处理
    for (let i = 0; i < apiCalls.length; i += concurrency) {
      chunks.push(apiCalls.slice(i, i + concurrency))
    }

    for (const chunk of chunks) {
      const promises = chunk.map(async ({ key, call, ttl }) => {
        try {
          const result = await cachedApiCall(key, call, ttl)
          results[key] = { success: true, data: result }
        } catch (error) {
          results[key] = { success: false, error: error.message }
        }
      })

      await Promise.all(promises)
    }

    return results
  }

  /**
   * 防抖API调用
   * @param {Function} apiCall - API调用函数
   * @param {number} delay - 防抖延迟
   * @returns {Function} 防抖函数
   */
  function debouncedApiCall(apiCall, delay = 300) {
    let timeoutId
    
    return (...args) => {
      clearTimeout(timeoutId)
      
      return new Promise((resolve, reject) => {
        timeoutId = setTimeout(async () => {
          try {
            const result = await apiCall(...args)
            resolve(result)
          } catch (error) {
            reject(error)
          }
        }, delay)
      })
    }
  }

  /**
   * 清除缓存
   * @param {string} pattern - 缓存键模式（可选）
   */
  function clearCache(pattern) {
    if (pattern) {
      // 清除匹配模式的缓存
      for (const key of apiCache.keys()) {
        if (key.includes(pattern)) {
          apiCache.delete(key)
        }
      }
    } else {
      // 清除所有缓存
      apiCache.clear()
    }
  }

  /**
   * 获取缓存统计
   */
  function getCacheStats() {
    return {
      totalCached: apiCache.size,
      pendingRequests: pendingRequests.size,
      cacheKeys: Array.from(apiCache.keys())
    }
  }

  return {
    cachedApiCall,
    batchApiCalls,
    debouncedApiCall,
    clearCache,
    getCacheStats
  }
}

/**
 * 页面加载优化Hook
 */
export function usePageLoadOptimization() {
  const loading = ref(true)
  const loadingProgress = ref(0)
  const error = ref(null)

  /**
   * 优化的页面数据加载
   * @param {Array} dataLoaders - 数据加载器数组
   * @param {Object} options - 选项
   */
  async function optimizedPageLoad(dataLoaders, options = {}) {
    const { 
      showProgress = true, 
      essential = [], // 必需的数据加载器
      optional = [] // 可选的数据加载器
    } = options

    try {
      loading.value = true
      error.value = null
      
      if (showProgress) loadingProgress.value = 10

      // 首先加载必需数据
      if (essential.length > 0) {
        await Promise.all(essential.map(loader => loader()))
        if (showProgress) loadingProgress.value = 60
      }

      // 然后在后台加载可选数据
      if (optional.length > 0) {
        // 不等待可选数据加载完成
        Promise.all(optional.map(async loader => {
          try {
            await loader()
          } catch (error) {
            console.warn('Optional data loading failed:', error)
          }
        }))
      }

      if (showProgress) loadingProgress.value = 100
      
      // 延迟一点显示加载完成
      setTimeout(() => {
        loading.value = false
        loadingProgress.value = 0
      }, 200)

    } catch (err) {
      error.value = err.message
      loading.value = false
      loadingProgress.value = 0
      console.error('Page load optimization failed:', err)
    }
  }

  return {
    loading,
    loadingProgress,
    error,
    optimizedPageLoad
  }
}

/**
 * 实时数据优化Hook
 */
export function useRealtimeOptimization() {
  const connections = ref(new Map())

  /**
   * 优化的WebSocket连接管理
   * @param {string} endpoint - WebSocket端点
   * @param {Object} callbacks - 回调函数
   * @param {Object} options - 选项
   */
  function optimizedWebSocket(endpoint, callbacks = {}, options = {}) {
    const {
      reconnectDelay = 3000,
      maxReconnectAttempts = 5,
      heartbeatInterval = 30000
    } = options

    // 检查是否已存在连接
    if (connections.value.has(endpoint)) {
      console.log(`🔌 Reusing existing WebSocket connection: ${endpoint}`)
      return connections.value.get(endpoint)
    }

    const ws = new WebSocket(endpoint)
    let reconnectAttempts = 0
    let heartbeatTimer

    // 心跳机制
    const startHeartbeat = () => {
      heartbeatTimer = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'ping' }))
        }
      }, heartbeatInterval)
    }

    const stopHeartbeat = () => {
      if (heartbeatTimer) {
        clearInterval(heartbeatTimer)
        heartbeatTimer = null
      }
    }

    // 重连逻辑
    const reconnect = () => {
      if (reconnectAttempts < maxReconnectAttempts) {
        reconnectAttempts++
        console.log(`🔄 Reconnecting WebSocket (${reconnectAttempts}/${maxReconnectAttempts}): ${endpoint}`)
        
        setTimeout(() => {
          optimizedWebSocket(endpoint, callbacks, options)
        }, reconnectDelay)
      }
    }

    ws.onopen = (event) => {
      console.log(`✅ WebSocket connected: ${endpoint}`)
      reconnectAttempts = 0
      startHeartbeat()
      callbacks.onOpen?.(event)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        
        // 忽略心跳响应
        if (data.type === 'pong') return
        
        callbacks.onMessage?.(data)
      } catch (error) {
        console.error('WebSocket message parse error:', error)
        callbacks.onError?.(error)
      }
    }

    ws.onerror = (event) => {
      console.error(`❌ WebSocket error: ${endpoint}`, event)
      callbacks.onError?.(event)
    }

    ws.onclose = (event) => {
      console.log(`🔌 WebSocket closed: ${endpoint}`)
      stopHeartbeat()
      connections.value.delete(endpoint)
      callbacks.onClose?.(event)

      // 非正常关闭时尝试重连
      if (event.code !== 1000) {
        reconnect()
      }
    }

    connections.value.set(endpoint, ws)
    return ws
  }

  /**
   * 清理所有WebSocket连接
   */
  function cleanupConnections() {
    connections.value.forEach((ws, endpoint) => {
      console.log(`🧹 Cleaning up WebSocket: ${endpoint}`)
      ws.close(1000, 'Component unmounted')
    })
    connections.value.clear()
  }

  return {
    optimizedWebSocket,
    cleanupConnections,
    activeConnections: connections
  }
}

// 在开发环境暴露优化工具
if (import.meta.env.DEV) {
  window.apiOptimization = {
    clearCache: () => apiCache.clear(),
    getCacheStats: () => ({
      cached: apiCache.size,
      pending: pendingRequests.size,
      keys: Array.from(apiCache.keys())
    })
  }
}