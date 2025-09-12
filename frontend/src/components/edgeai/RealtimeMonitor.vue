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
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useEdgeAIStore } from '@/stores/edgeai'
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

// Component state
const isConnected = ref(true)
const autoRefresh = ref(true)
const refreshing = ref(false)
const lastUpdate = ref('Just now')
const eventFilter = ref('')

// Metrics data
const currentMetrics = ref({
  cpu: 45,
  memory: 62,
  networkIn: 1024 * 1024 * 2.5, // 2.5 MB/s
  networkOut: 1024 * 1024 * 1.2  // 1.2 MB/s
})

const metricsHistory = ref({
  cpu: [],
  memory: [],
  networkIn: [],
  networkOut: []
})

const events = ref([
  {
    id: 1,
    type: 'info',
    message: 'Training started on Factory Node A',
    timestamp: '2 minutes ago',
    source: 'Smart Manufacturing Monitor'
  },
  {
    id: 2,
    type: 'warning',
    message: 'High CPU usage detected on Traffic Hub Central',
    timestamp: '5 minutes ago',
    source: 'System Monitor'
  },
  {
    id: 3,
    type: 'error',
    message: 'Connection lost to Retail Analytics Hub',
    timestamp: '12 minutes ago',
    source: 'Network Monitor'
  },
  {
    id: 4,
    type: 'info',
    message: 'Model checkpoint saved successfully',
    timestamp: '15 minutes ago',
    source: 'Medical Image Diagnosis'
  }
])

// Auto-refresh interval
let refreshInterval = null
const REFRESH_INTERVAL = 2000 // 2 seconds

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
  refreshing.value = true
  
  try {
    // Simulate data refresh
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Update current metrics with some randomness
    currentMetrics.value = {
      cpu: Math.max(10, Math.min(95, currentMetrics.value.cpu + (Math.random() - 0.5) * 10)),
      memory: Math.max(15, Math.min(90, currentMetrics.value.memory + (Math.random() - 0.5) * 8)),
      networkIn: Math.max(1024 * 512, currentMetrics.value.networkIn + (Math.random() - 0.5) * 1024 * 1024),
      networkOut: Math.max(1024 * 256, currentMetrics.value.networkOut + (Math.random() - 0.5) * 1024 * 512)
    }
    
    // Update history (keep last 30 points)
    const maxPoints = 30
    
    metricsHistory.value.cpu.push(currentMetrics.value.cpu)
    metricsHistory.value.memory.push(currentMetrics.value.memory)
    metricsHistory.value.networkIn.push(currentMetrics.value.networkIn)
    metricsHistory.value.networkOut.push(currentMetrics.value.networkOut)
    
    if (metricsHistory.value.cpu.length > maxPoints) {
      metricsHistory.value.cpu.shift()
      metricsHistory.value.memory.shift()
      metricsHistory.value.networkIn.shift()
      metricsHistory.value.networkOut.shift()
    }
    
    lastUpdate.value = new Date().toLocaleTimeString()
    
    // Occasionally add new events
    if (Math.random() < 0.1) {
      addRandomEvent()
    }
    
  } finally {
    refreshing.value = false
  }
}

const startAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  
  refreshInterval = setInterval(refreshData, REFRESH_INTERVAL)
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

const addRandomEvent = () => {
  const eventTypes = ['info', 'warning', 'error']
  const messages = [
    'Training epoch completed',
    'Model accuracy improved',
    'Node reconnected successfully',
    'High resource usage detected',
    'Network latency increased',
    'Training paused due to error',
    'Backup created successfully',
    'Performance optimization applied'
  ]
  
  const newEvent = {
    id: Date.now(),
    type: eventTypes[Math.floor(Math.random() * eventTypes.length)],
    message: messages[Math.floor(Math.random() * messages.length)],
    timestamp: 'Just now',
    source: 'System Monitor'
  }
  
  events.value.unshift(newEvent)
  
  // Keep only last 50 events
  if (events.value.length > 50) {
    events.value = events.value.slice(0, 50)
  }
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

// Initialize data
const initializeData = () => {
  // Fill initial history
  for (let i = 0; i < 10; i++) {
    metricsHistory.value.cpu.push(Math.random() * 50 + 20)
    metricsHistory.value.memory.push(Math.random() * 40 + 30)
    metricsHistory.value.networkIn.push(Math.random() * 1024 * 1024 * 2)
    metricsHistory.value.networkOut.push(Math.random() * 1024 * 1024 * 1)
  }
}

// Lifecycle
onMounted(() => {
  initializeData()
  
  if (autoRefresh.value) {
    startAutoRefresh()
  }
  
  // Initial data refresh
  refreshData()
})

onUnmounted(() => {
  stopAutoRefresh()
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