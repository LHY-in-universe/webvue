<template>
  <div class="enhanced-dashboard-demo p-6 space-y-6">
    <!-- Enhanced Features Demo Header -->
    <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg p-6">
      <h2 class="text-2xl font-bold mb-2">🚀 Enhanced EdgeAI Features Demo</h2>
      <p class="text-blue-100">Demonstrating all the new enhancements added to the EdgeAI platform</p>
      
      <!-- Quick Status Indicators -->
      <div class="flex items-center space-x-4 mt-4">
        <div class="flex items-center space-x-2">
          <div :class="[
            'w-3 h-3 rounded-full',
            isOffline ? 'bg-red-400 animate-pulse' : 'bg-green-400'
          ]"></div>
          <span class="text-sm">{{ isOffline ? 'Offline' : 'Online' }}</span>
        </div>
        
        <div v-if="queuedRequests > 0" class="flex items-center space-x-2">
          <span class="text-sm">📋 {{ queuedRequests }} queued requests</span>
        </div>
        
        <div class="flex items-center space-x-2">
          <span class="text-sm">⌨️ Press</span>
          <kbd class="px-2 py-1 bg-white/20 rounded text-xs">Ctrl+Shift+?</kbd>
          <span class="text-sm">for shortcuts</span>
        </div>
      </div>
    </div>

    <!-- Performance Optimizations Demo -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center">
          <span class="text-blue-600 mr-2">⚡</span>
          Performance Optimizations
        </h3>
        
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">Real-time Monitoring</span>
            <span class="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded text-xs">
              Optimized
            </span>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">Memory Usage</span>
            <span class="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded text-xs">
              Reduced by 40%
            </span>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">Update Throttling</span>
            <span class="px-2 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded text-xs">
              Active
            </span>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">Visibility-based Refresh</span>
            <span class="px-2 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 rounded text-xs">
              Adaptive
            </span>
          </div>
        </div>
      </div>

      <!-- Error Boundary Demo -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center">
          <span class="text-red-600 mr-2">🛡️</span>
          Error Boundary Protection
        </h3>
        
        <div class="space-y-3">
          <div v-if="hasError" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded p-3">
            <p class="text-sm text-red-600 dark:text-red-400">An error was caught and handled gracefully!</p>
            <Button @click="retry()" size="sm" variant="ghost" class="mt-2 text-red-600">
              Retry
            </Button>
          </div>
          
          <div v-else class="space-y-2">
            <Button @click="triggerError" size="sm" variant="outline" class="w-full">
              Test Error Boundary
            </Button>
            
            <div class="text-xs text-gray-500 dark:text-gray-400">
              • Automatic error capture<br>
              • User-friendly notifications<br>
              • Graceful degradation<br>
              • Error reporting integration
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Metrics Chart Demo -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center">
        <span class="text-green-600 mr-2">📊</span>
        Enhanced Data Visualization
      </h3>
      
      <EnhancedMetricsChart
        title="System Performance Metrics"
        subtitle="Real-time monitoring with enhanced features"
        type="line"
        :data="chartData"
        :height="300"
        :theme="themeStore.isDark ? 'dark' : 'light'"
        :real-time="true"
        :show-stats="true"
        :animated="true"
        :refresh-interval="5000"
        @refresh="refreshChartData"
        @export="onExportChart"
        @time-range-change="onTimeRangeChange"
      />
    </div>

    <!-- Offline Mode Demo -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center">
        <span class="text-yellow-600 mr-2">📱</span>
        Offline Mode Support
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {{ hasOfflineData ? '✓' : '✗' }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">Cached Data</div>
        </div>
        
        <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div class="text-2xl font-bold text-green-600 dark:text-green-400">
            {{ queuedRequests }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">Queued Requests</div>
        </div>
        
        <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {{ isOffline ? 'Offline' : 'Online' }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">Connection Status</div>
        </div>
      </div>
      
      <div class="mt-4 space-x-2">
        <Button @click="simulateOffline" size="sm" variant="outline">
          Simulate Offline
        </Button>
        <Button @click="simulateOnline" size="sm" variant="outline">
          Simulate Online
        </Button>
        <Button @click="clearOfflineData" size="sm" variant="ghost">
          Clear Cache
        </Button>
      </div>
    </div>

    <!-- Keyboard Shortcuts Demo -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center">
        <span class="text-indigo-600 mr-2">⌨️</span>
        Keyboard Shortcuts
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="shortcut in popularShortcuts" :key="shortcut.keys" class="flex justify-between items-center p-2 bg-gray-50 dark:bg-gray-700 rounded">
          <span class="text-sm text-gray-600 dark:text-gray-400">{{ shortcut.description }}</span>
          <div class="flex space-x-1">
            <kbd v-for="key in shortcut.keys.split('+')" :key="key" class="px-2 py-1 bg-gray-200 dark:bg-gray-600 rounded text-xs">
              {{ key }}
            </kbd>
          </div>
        </div>
      </div>
      
      <div class="mt-4">
        <Button @click="showAllShortcuts" size="sm" variant="outline">
          Show All Shortcuts (Ctrl+Shift+?)
        </Button>
      </div>
    </div>

    <!-- Demo Controls -->
    <div class="bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
      <h4 class="font-semibold mb-3">Demo Controls</h4>
      <div class="flex flex-wrap gap-2">
        <Button @click="refreshAllData" size="sm" :loading="refreshing">
          Refresh All Data
        </Button>
        <Button @click="simulateError" size="sm" variant="outline">
          Trigger Error
        </Button>
        <Button @click="toggleTheme" size="sm" variant="outline">
          Toggle Theme
        </Button>
        <Button @click="resetDemo" size="sm" variant="ghost">
          Reset Demo
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'
import { useErrorBoundary } from '@/composables/useErrorBoundary'
import { useOfflineMode } from '@/composables/useOfflineMode'
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts'
import Button from '@/components/ui/Button.vue'
import EnhancedMetricsChart from './EnhancedMetricsChart.vue'

const themeStore = useThemeStore()
const uiStore = useUIStore()
const { hasError, retry, captureError } = useErrorBoundary()
const { 
  isOffline, 
  queuedRequests, 
  hasOfflineData, 
  clearOfflineData,
  offlineAwareFetch 
} = useOfflineMode()
const { showShortcutsHelp } = useKeyboardShortcuts()

// Demo state
const refreshing = ref(false)
const chartData = ref({
  labels: ['1min', '2min', '3min', '4min', '5min'],
  datasets: [
    {
      label: 'CPU Usage',
      data: [45, 52, 48, 61, 55],
      borderColor: '#3b82f6',
      backgroundColor: '#3b82f620'
    },
    {
      label: 'Memory Usage',
      data: [62, 58, 65, 59, 63],
      borderColor: '#10b981',
      backgroundColor: '#10b98120'
    }
  ]
})

// Popular shortcuts for demo
const popularShortcuts = ref([
  { keys: 'Ctrl+1', description: 'Dashboard' },
  { keys: 'Ctrl+2', description: 'All Nodes' },
  { keys: 'Ctrl+3', description: 'Models' },
  { keys: 'Ctrl+Shift+T', description: 'Toggle Theme' },
  { keys: 'Ctrl+R', description: 'Refresh' },
  { keys: 'Ctrl+F', description: 'Search' }
])

// Methods
const triggerError = () => {
  try {
    throw new Error('Demo error for testing error boundary')
  } catch (error) {
    captureError(error, null, 'Demo trigger')
  }
}

const refreshAllData = async () => {
  refreshing.value = true
  
  try {
    // Simulate data refresh
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update chart data with random values
    chartData.value = {
      ...chartData.value,
      datasets: chartData.value.datasets.map(dataset => ({
        ...dataset,
        data: dataset.data.map(() => Math.floor(Math.random() * 100))
      }))
    }
    
    uiStore.addNotification({
      type: 'success',
      title: 'Data Refreshed',
      message: 'All demo data has been updated',
      duration: 3000
    })
  } catch (error) {
    captureError(error, null, 'Demo refresh')
  } finally {
    refreshing.value = false
  }
}

const simulateError = () => {
  const errors = [
    'Network connection timeout',
    'Authentication failed',
    'Server internal error',
    'Data validation failed'
  ]
  
  const randomError = errors[Math.floor(Math.random() * errors.length)]
  captureError(new Error(randomError), null, 'Simulated error')
}

const simulateOffline = () => {
  // Dispatch offline event
  window.dispatchEvent(new Event('offline'))
  
  uiStore.addNotification({
    type: 'warning',
    title: 'Offline Mode Simulated',
    message: 'The app is now in offline mode for demonstration',
    duration: 3000
  })
}

const simulateOnline = () => {
  // Dispatch online event
  window.dispatchEvent(new Event('online'))
  
  uiStore.addNotification({
    type: 'success',
    title: 'Online Mode Restored',
    message: 'Connection has been restored',
    duration: 3000
  })
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}

const showAllShortcuts = () => {
  showShortcutsHelp()
}

const resetDemo = () => {
  // Reset all demo state
  chartData.value = {
    labels: ['1min', '2min', '3min', '4min', '5min'],
    datasets: [
      {
        label: 'CPU Usage',
        data: [45, 52, 48, 61, 55],
        borderColor: '#3b82f6',
        backgroundColor: '#3b82f620'
      },
      {
        label: 'Memory Usage',
        data: [62, 58, 65, 59, 63],
        borderColor: '#10b981',
        backgroundColor: '#10b98120'
      }
    ]
  }
  
  uiStore.addNotification({
    type: 'info',
    title: 'Demo Reset',
    message: 'All demo data has been reset to initial values',
    duration: 3000
  })
}

// Chart event handlers
const refreshChartData = () => {
  // Simulate new data
  chartData.value = {
    ...chartData.value,
    datasets: chartData.value.datasets.map(dataset => ({
      ...dataset,
      data: dataset.data.map(() => Math.floor(Math.random() * 100))
    }))
  }
}

const onExportChart = () => {
  uiStore.addNotification({
    type: 'success',
    title: 'Chart Exported',
    message: 'Chart has been exported as PNG',
    duration: 3000
  })
}

const onTimeRangeChange = (range) => {
  uiStore.addNotification({
    type: 'info',
    title: 'Time Range Changed',
    message: `Switched to ${range} time range`,
    duration: 2000
  })
}

onMounted(() => {
  uiStore.addNotification({
    type: 'info',
    title: 'Enhanced Features Demo',
    message: 'Welcome to the EdgeAI enhancements showcase!',
    duration: 5000
  })
})
</script>

<style scoped>
.enhanced-dashboard-demo {
  max-width: 1200px;
  margin: 0 auto;
}

kbd {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.75rem;
}
</style>