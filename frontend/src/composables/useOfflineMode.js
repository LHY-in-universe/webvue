import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useUIStore } from '@/stores/ui'
import { logger } from '@/utils/logger'

export function useOfflineMode() {
  const uiStore = useUIStore()
  
  const isOnline = ref(navigator.onLine)
  const offlineQueue = ref([])
  const offlineData = ref({})
  const lastSync = ref(null)
  
  // Computed
  const isOffline = computed(() => !isOnline.value)
  const queuedRequests = computed(() => offlineQueue.value.length)
  const hasOfflineData = computed(() => Object.keys(offlineData.value).length > 0)

  // Event handlers
  const handleOnline = () => {
    isOnline.value = true
    uiStore.addNotification({
      type: 'success',
      title: 'Connection Restored',
      message: 'You are back online. Syncing data...',
      duration: 3000
    })
    syncOfflineData()
  }

  const handleOffline = () => {
    isOnline.value = false
    uiStore.addNotification({
      type: 'warning',
      title: 'Connection Lost',
      message: 'You are now offline. Data will be cached locally.',
      duration: 5000
    })
  }

  // Offline data management
  const cacheData = (key, data) => {
    try {
      offlineData.value[key] = {
        data,
        timestamp: Date.now(),
        expires: Date.now() + (24 * 60 * 60 * 1000) // 24 hours
      }
      
      // Also store in localStorage for persistence
      localStorage.setItem('edgeai_offline_data', JSON.stringify(offlineData.value))
    } catch (error) {
      logger.error('Failed to cache offline data:', error)
    }
  }

  const getCachedData = (key) => {
    try {
      const cached = offlineData.value[key]
      if (!cached) return null
      
      // Check if data has expired
      if (Date.now() > cached.expires) {
        delete offlineData.value[key]
        return null
      }
      
      return cached.data
    } catch (error) {
      logger.error('Failed to retrieve cached data:', error)
      return null
    }
  }

  const queueRequest = (request) => {
    try {
      const queueItem = {
        id: Date.now() + Math.random(),
        url: request.url,
        method: request.method || 'GET',
        data: request.data,
        headers: request.headers,
        timestamp: Date.now(),
        retries: 0,
        maxRetries: 3
      }
      
      offlineQueue.value.push(queueItem)
      
      // Store in localStorage for persistence
      localStorage.setItem('edgeai_offline_queue', JSON.stringify(offlineQueue.value))
      
      uiStore.addNotification({
        type: 'info',
        title: 'Request Queued',
        message: 'Your request will be processed when connection is restored.',
        duration: 3000
      })
    } catch (error) {
      logger.error('Failed to queue request:', error)
    }
  }

  const syncOfflineData = async () => {
    if (!isOnline.value || offlineQueue.value.length === 0) return
    
    const queue = [...offlineQueue.value]
    const successfulRequests = []
    const failedRequests = []
    
    for (const request of queue) {
      try {
        const response = await fetch(request.url, {
          method: request.method,
          headers: {
            'Content-Type': 'application/json',
            ...request.headers
          },
          body: request.data ? JSON.stringify(request.data) : undefined
        })
        
        if (response.ok) {
          successfulRequests.push(request.id)
        } else {
          throw new Error(`HTTP ${response.status}`)
        }
      } catch (error) {
        logger.error('Failed to sync request:', error)
        request.retries++
        
        if (request.retries >= request.maxRetries) {
          failedRequests.push(request.id)
        }
      }
    }
    
    // Remove successful and permanently failed requests from queue
    offlineQueue.value = offlineQueue.value.filter(request => 
      !successfulRequests.includes(request.id) && !failedRequests.includes(request.id)
    )
    
    // Update localStorage
    localStorage.setItem('edgeai_offline_queue', JSON.stringify(offlineQueue.value))
    lastSync.value = new Date().toISOString()
    
    // Notify user of sync results
    if (successfulRequests.length > 0) {
      uiStore.addNotification({
        type: 'success',
        title: 'Data Synced',
        message: `${successfulRequests.length} requests synced successfully.`,
        duration: 3000
      })
    }
    
    if (failedRequests.length > 0) {
      uiStore.addNotification({
        type: 'error',
        title: 'Sync Failed',
        message: `${failedRequests.length} requests failed to sync.`,
        duration: 5000
      })
    }
  }

  const clearOfflineData = () => {
    offlineData.value = {}
    offlineQueue.value = []
    localStorage.removeItem('edgeai_offline_data')
    localStorage.removeItem('edgeai_offline_queue')
    
    uiStore.addNotification({
      type: 'info',
      title: 'Offline Data Cleared',
      message: 'All cached offline data has been cleared.',
      duration: 3000
    })
  }

  const loadPersistedData = () => {
    try {
      // Load cached data
      const cachedDataString = localStorage.getItem('edgeai_offline_data')
      if (cachedDataString) {
        const cachedData = JSON.parse(cachedDataString)
        // Filter out expired data
        const now = Date.now()
        Object.keys(cachedData).forEach(key => {
          if (cachedData[key].expires > now) {
            offlineData.value[key] = cachedData[key]
          }
        })
      }
      
      // Load queued requests
      const queueString = localStorage.getItem('edgeai_offline_queue')
      if (queueString) {
        offlineQueue.value = JSON.parse(queueString)
      }
    } catch (error) {
      logger.error('Failed to load persisted offline data:', error)
    }
  }

  // Enhanced fetch function with offline support
  const offlineAwareFetch = async (url, options = {}) => {
    const cacheKey = `${url}_${JSON.stringify(options)}`
    
    if (isOffline.value) {
      // Try to get cached data for GET requests
      if (!options.method || options.method === 'GET') {
        const cachedData = getCachedData(cacheKey)
        if (cachedData) {
          return Promise.resolve({
            ok: true,
            json: () => Promise.resolve(cachedData),
            fromCache: true
          })
        }
      }
      
      // Queue non-GET requests or failed cache lookups
      queueRequest({ url, ...options })
      throw new Error('Offline: Request queued for later')
    }
    
    try {
      const response = await fetch(url, options)
      
      // Cache successful GET responses
      if (response.ok && (!options.method || options.method === 'GET')) {
        const data = await response.clone().json()
        cacheData(cacheKey, data)
      }
      
      return response
    } catch (error) {
      // If fetch fails but we have cached data, return it
      if (!options.method || options.method === 'GET') {
        const cachedData = getCachedData(cacheKey)
        if (cachedData) {
          uiStore.addNotification({
            type: 'warning',
            title: 'Using Cached Data',
            message: 'Network request failed, showing cached data.',
            duration: 3000
          })
          
          return Promise.resolve({
            ok: true,
            json: () => Promise.resolve(cachedData),
            fromCache: true
          })
        }
      }
      
      throw error
    }
  }

  // Lifecycle
  onMounted(() => {
    loadPersistedData()
    
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    
    // Try to sync on mount if online
    if (isOnline.value && offlineQueue.value.length > 0) {
      setTimeout(syncOfflineData, 1000)
    }
  })

  onUnmounted(() => {
    window.removeEventListener('online', handleOnline)
    window.removeEventListener('offline', handleOffline)
  })

  return {
    isOnline,
    isOffline,
    queuedRequests,
    hasOfflineData,
    lastSync,
    offlineQueue,
    cacheData,
    getCachedData,
    queueRequest,
    syncOfflineData,
    clearOfflineData,
    offlineAwareFetch
  }
}