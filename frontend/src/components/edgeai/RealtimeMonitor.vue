<template>
  <div class="realtime-monitor">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">
        <div class="flex items-center mr-4">
          <div 
            :class="[
              'w-3 h-3 rounded-full mr-2 transition-colors',
              isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'
            ]"
          ></div>
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ isConnected ? 'Connected' : 'Disconnected' }}
          </span>
        </div>
        <div class="text-xs text-gray-500 dark:text-gray-400">
          Last update: {{ lastUpdate }}
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <Button 
          @click="toggleAutoRefresh"
          :variant="autoRefresh ? 'primary' : 'outline'"
          size="sm"
        >
          <PlayIcon v-if="!autoRefresh" class="w-4 h-4 mr-1" />
          <PauseIcon v-else class="w-4 h-4 mr-1" />
          Auto Refresh
        </Button>
        <Button @click="refreshData" variant="outline" size="sm" :loading="refreshing">
          <ArrowPathIcon class="w-4 h-4" />
        </Button>
      </div>
    </div>

    <!-- System Overview -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <!-- CPU Usage Chart -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-semibold text-gray-900 dark:text-white">CPU Usage</h3>
          <div class="flex items-center">
            <div class="text-2xl font-bold text-blue-600">{{ currentMetrics.cpu }}%</div>
          </div>
        </div>
        <MetricsChart
          type="area"
          :data="cpuChartData"
          :height="120"
          :theme="themeStore.isDark ? 'dark' : 'light'"
          :animated="true"
        />
      </div>

      <!-- Memory Usage Chart -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-semibold text-gray-900 dark:text-white">Memory Usage</h3>
          <div class="flex items-center">
            <div class="text-2xl font-bold text-green-600">{{ currentMetrics.memory }}%</div>
          </div>
        </div>
        <MetricsChart
          type="area"
          :data="memoryChartData"
          :height="120"
          :theme="themeStore.isDark ? 'dark' : 'light'"
          :animated="true"
        />
      </div>

      <!-- Network I/O Chart -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-semibold text-gray-900 dark:text-white">Network I/O</h3>
          <div class="flex items-center space-x-4">
            <div class="text-xs text-green-600">↑ {{ formatBytes(currentMetrics.networkIn) }}/s</div>
            <div class="text-xs text-red-600">↓ {{ formatBytes(currentMetrics.networkOut) }}/s</div>
          </div>
        </div>
        <MetricsChart
          type="line"
          :data="networkChartData"
          :height="120"
          :theme="themeStore.isDark ? 'dark' : 'light'"
          :animated="true"
        />
      </div>
    </div>

    <!-- Node Performance Grid -->
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-8">
      <!-- Training Progress -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Training Progress</h3>
        <div class="space-y-4">
          <div
            v-for="project in trainingProjects"
            :key="project.id"
            class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center">
              <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center mr-3">
                <CpuChipIcon class="w-6 h-6 text-white" />
              </div>
              <div>
                <div class="font-medium text-gray-900 dark:text-white">{{ project.name }}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">
                  Epoch {{ project.currentEpoch }}/{{ project.totalEpochs }}
                </div>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <div class="w-32">
                <ProgressBar :value="project.progress" variant="primary" size="sm" />
              </div>
              <div class="text-sm font-medium text-gray-900 dark:text-white min-w-12">
                {{ project.progress }}%
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Node Status -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Node Status</h3>
        <div class="space-y-3">
          <div
            v-for="node in monitoredNodes"
            :key="node.id"
            class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center">
              <div
                :class="[
                  'w-3 h-3 rounded-full mr-3',
                  getNodeStatusColor(node.status)
                ]"
              ></div>
              <div>
                <div class="font-medium text-gray-900 dark:text-white">{{ node.name }}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">{{ node.type }}</div>
              </div>
            </div>
            <div class="flex items-center space-x-3 text-xs">
              <div class="flex items-center">
                <span class="text-gray-500 mr-1">CPU:</span>
                <span class="font-medium">{{ Math.round(node.cpuUsage) }}%</span>
              </div>
              <div class="flex items-center">
                <span class="text-gray-500 mr-1">MEM:</span>
                <span class="font-medium">{{ Math.round(node.memoryUsage) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Alerts and Events -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Recent Events</h3>
        <div class="flex items-center space-x-2">
          <select 
            v-model="eventFilter"
            class="text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            <option value="">All Events</option>
            <option value="info">Info</option>
            <option value="warning">Warning</option>
            <option value="error">Error</option>
          </select>
          <Button @click="clearEvents" variant="outline" size="xs">
            Clear
          </Button>
        </div>
      </div>
      
      <div class="space-y-2 max-h-64 overflow-y-auto">
        <div
          v-for="event in filteredEvents"
          :key="event.id"
          :class="[
            'flex items-start p-3 rounded-lg border-l-4',
            getEventStyle(event.type)
          ]"
        >
          <div class="flex-shrink-0 mr-3 mt-0.5">
            <component :is="getEventIcon(event.type)" class="w-4 h-4" />
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-sm font-medium text-gray-900 dark:text-white">
              {{ event.message }}
            </div>
            <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {{ event.timestamp }} • {{ event.source }}
            </div>
          </div>
        </div>
        
        <div v-if="filteredEvents.length === 0" class="text-center py-8">
          <ClockIcon class="w-12 h-12 mx-auto text-gray-400 mb-4" />
          <p class="text-gray-500 dark:text-gray-400">No events to display</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick, shallowRef } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useEdgeAIStore } from '@/stores/edgeai'
import { useApiOptimization } from '@/composables/useApiOptimization'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import MetricsChart from './MetricsChart.vue'
import {
  PlayIcon,
  PauseIcon,
  ArrowPathIcon,
  CpuChipIcon,
  ClockIcon,
  InformationCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon
} from '@heroicons/vue/24/outline'

const themeStore = useThemeStore()
const edgeaiStore = useEdgeAIStore()
const { cachedApiCall } = useApiOptimization()

// Component state
const isConnected = ref(true)
const autoRefresh = ref(true)
const refreshing = ref(false)
const lastUpdate = ref('Just now')
const eventFilter = ref('')

// Metrics data - using shallowRef for better performance with large arrays
const currentMetrics = ref({
  cpu: 0,
  memory: 0,
  networkIn: 0,
  networkOut: 0
})

const metricsHistory = shallowRef({
  cpu: [],
  memory: [],
  networkIn: [],
  networkOut: []
})

// Performance optimization: throttle updates
const updateThrottle = ref(false)
const THROTTLE_DELAY = 100 // ms

const events = ref([])

// Auto-refresh interval with adaptive timing
let refreshInterval = null
const REFRESH_INTERVAL = 2000 // 2 seconds
const BACKGROUND_REFRESH_INTERVAL = 10000 // 10 seconds when tab is hidden
let isPageVisible = ref(true)

// Computed properties
const trainingProjects = computed(() => {
  return edgeaiStore.projects.filter(p => p.status === 'training')
})

const monitoredNodes = computed(() => {
  return edgeaiStore.nodes.slice(0, 6) // Show top 6 nodes
})

const filteredEvents = computed(() => {
  if (!eventFilter.value) return events.value
  return events.value.filter(event => event.type === eventFilter.value)
})

// Chart data
const cpuChartData = computed(() => ({
  labels: Array.from({ length: metricsHistory.value.cpu.length }, (_, i) => `${i * 2}s`),
  datasets: [{
    label: 'CPU Usage',
    data: metricsHistory.value.cpu,
    backgroundColor: '#3b82f680',
    borderColor: '#3b82f6',
    tension: 0.4
  }]
}))

const memoryChartData = computed(() => ({
  labels: Array.from({ length: metricsHistory.value.memory.length }, (_, i) => `${i * 2}s`),
  datasets: [{
    label: 'Memory Usage',
    data: metricsHistory.value.memory,
    backgroundColor: '#10b98180',
    borderColor: '#10b981',
    tension: 0.4
  }]
}))

const networkChartData = computed(() => ({
  labels: Array.from({ length: metricsHistory.value.networkIn.length }, (_, i) => `${i * 2}s`),
  datasets: [
    {
      label: 'Network In',
      data: metricsHistory.value.networkIn.map(v => v / (1024 * 1024)), // Convert to MB/s
      backgroundColor: '#10b98140',
      borderColor: '#10b981',
      tension: 0.4
    },
    {
      label: 'Network Out',
      data: metricsHistory.value.networkOut.map(v => v / (1024 * 1024)), // Convert to MB/s
      backgroundColor: '#ef444440',
      borderColor: '#ef4444',
      tension: 0.4
    }
  ]
}))

// Methods
const toggleAutoRefresh = () => {
  autoRefresh.value = !autoRefresh.value
  
  if (autoRefresh.value) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}

const refreshData = async () => {
  // Throttle rapid successive calls
  if (updateThrottle.value) return
  
  updateThrottle.value = true
  setTimeout(() => {
    updateThrottle.value = false
  }, THROTTLE_DELAY)
  
  const pageMonitor = performanceMonitor.monitorPageLoad('RealtimeMonitor')
  refreshing.value = true
  
  try {
    const [metricsResult, eventsResult] = await Promise.all([
      cachedApiCall('edgeai-realtime-metrics', 
        () => edgeaiService.monitoring.getRealTimeMetrics(), 
        5 * 1000 // Cache for 5 seconds
      ),
      cachedApiCall('edgeai-recent-events', 
        () => edgeaiService.monitoring.getRecentEvents(), 
        10 * 1000 // Cache for 10 seconds
      )
    ])
    
    if (metricsResult) {
      // Batch updates for better performance
      await nextTick(() => {
        currentMetrics.value = {
          cpu: Math.round(metricsResult.cpu_usage || 0),
          memory: Math.round(metricsResult.memory_usage || 0),
          networkIn: metricsResult.network_in || 0,
          networkOut: metricsResult.network_out || 0
        }
        
        // Update history (keep last 30 points) - efficient array operations
        const maxPoints = 30
        const newHistory = { ...metricsHistory.value }
        
        newHistory.cpu = [...newHistory.cpu, currentMetrics.value.cpu].slice(-maxPoints)
        newHistory.memory = [...newHistory.memory, currentMetrics.value.memory].slice(-maxPoints)
        newHistory.networkIn = [...newHistory.networkIn, currentMetrics.value.networkIn].slice(-maxPoints)
        newHistory.networkOut = [...newHistory.networkOut, currentMetrics.value.networkOut].slice(-maxPoints)
        
        metricsHistory.value = newHistory
      })
    }
    
    if (eventsResult && eventsResult.data) {
      // Only update events if there are changes
      const newEvents = eventsResult.data.map(event => ({
        id: event.id,
        type: event.severity || 'info',
        message: event.message,
        timestamp: formatRelativeTime(event.created_at),
        source: event.source || 'System Monitor'
      }))
      
      // Check if events actually changed before updating
      if (JSON.stringify(newEvents) !== JSON.stringify(events.value)) {
        events.value = newEvents
      }
    }
    
    lastUpdate.value = new Date().toLocaleTimeString()
    pageMonitor.end()
    
  } catch (err) {
    console.error('Failed to refresh realtime data:', err)
    pageMonitor.end()
  } finally {
    refreshing.value = false
  }
}

const formatRelativeTime = (timestamp) => {
  if (!timestamp) return 'Unknown time'
  
  const now = new Date()
  const eventTime = new Date(timestamp)
  const diffMs = now - eventTime
  const diffMinutes = Math.floor(diffMs / 60000)
  
  if (diffMinutes < 1) return 'Just now'
  if (diffMinutes < 60) return `${diffMinutes} minutes ago`
  
  const diffHours = Math.floor(diffMinutes / 60)
  if (diffHours < 24) return `${diffHours} hours ago`
  
  const diffDays = Math.floor(diffHours / 24)
  return `${diffDays} days ago`
}

const startAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  
  // Use different intervals based on page visibility
  const interval = isPageVisible.value ? REFRESH_INTERVAL : BACKGROUND_REFRESH_INTERVAL
  refreshInterval = setInterval(refreshData, interval)
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

const loadInitialData = async () => {
  try {
    const metricsHistoryResult = await cachedApiCall('edgeai-metrics-history', 
      () => edgeaiService.monitoring.getMetricsHistory(), 
      60 * 1000 // Cache for 1 minute
    )
    
    if (metricsHistoryResult && metricsHistoryResult.data) {
      const history = metricsHistoryResult.data
      metricsHistory.value.cpu = history.cpu || []
      metricsHistory.value.memory = history.memory || []
      metricsHistory.value.networkIn = history.network_in || []
      metricsHistory.value.networkOut = history.network_out || []
    }
  } catch (err) {
    console.error('Failed to load initial metrics history:', err)
    // Fall back to empty arrays
    initializeEmptyData()
  }
}

const initializeEmptyData = () => {
  // Initialize with empty arrays if API fails
  metricsHistory.value.cpu = []
  metricsHistory.value.memory = []
  metricsHistory.value.networkIn = []
  metricsHistory.value.networkOut = []
}

const clearEvents = () => {
  events.value = []
}

const getNodeStatusColor = (status) => {
  const colors = {
    online: 'bg-green-500',
    training: 'bg-blue-500',
    idle: 'bg-yellow-500',
    error: 'bg-red-500'
  }
  return colors[status] || 'bg-gray-500'
}

const getEventStyle = (type) => {
  const styles = {
    info: 'bg-blue-50 dark:bg-blue-900/20 border-blue-400 dark:border-blue-500',
    warning: 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-400 dark:border-yellow-500',
    error: 'bg-red-50 dark:bg-red-900/20 border-red-400 dark:border-red-500'
  }
  return styles[type] || styles.info
}

const getEventIcon = (type) => {
  const icons = {
    info: InformationCircleIcon,
    warning: ExclamationTriangleIcon,
    error: XCircleIcon
  }
  return icons[type] || InformationCircleIcon
}

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

// Check connection status
const checkConnectionStatus = async () => {
  try {
    const result = await edgeaiService.monitoring.getConnectionStatus()
    isConnected.value = result.connected || false
  } catch (err) {
    console.error('Failed to check connection status:', err)
    isConnected.value = false
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadInitialData(),
    checkConnectionStatus()
  ])
  
  // Add visibility change listener for performance optimization
  document.addEventListener('visibilitychange', handleVisibilityChange)
  
  if (autoRefresh.value) {
    startAutoRefresh()
  }
  
  // Initial data refresh
  await refreshData()
})

// Handle page visibility for performance optimization
const handleVisibilityChange = () => {
  isPageVisible.value = !document.hidden
  
  if (autoRefresh.value) {
    stopAutoRefresh()
    startAutoRefresh()
  }
}

onUnmounted(() => {
  stopAutoRefresh()
  document.removeEventListener('visibilitychange', handleVisibilityChange)
})

// Watch for connection status
watch(() => edgeaiStore.isConnected, (connected) => {
  isConnected.value = connected
})
</script>

<style scoped>
.realtime-monitor {
  @apply space-y-6;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>