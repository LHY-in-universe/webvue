<template>
  <div class="enhanced-p2pai-demo p-6 space-y-6">
    <!-- Enhanced P2PAI Features Demo Header -->
    <div class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg p-6">
      <h2 class="text-2xl font-bold mb-2">🚀 Enhanced P2PAI Features Demo</h2>
      <p class="text-purple-100">Demonstrating all the new enhancements added to the P2PAI platform</p>
      
      <!-- Quick Status Indicators -->
      <div class="flex items-center space-x-4 mt-4">
        <div class="flex items-center space-x-2">
          <div :class="[
            'w-3 h-3 rounded-full',
            isOffline ? 'bg-red-400 animate-pulse' : 'bg-green-400'
          ]"></div>
          <span class="text-sm">{{ isOffline ? 'Offline' : 'Connected' }}</span>
        </div>
        
        <div v-if="queuedRequests > 0" class="flex items-center space-x-2">
          <span class="text-sm">📋 {{ queuedRequests }} queued requests</span>
        </div>
        
        <div class="flex items-center space-x-2">
          <span class="text-sm">⌨️ Press</span>
          <kbd class="px-2 py-1 bg-white/20 rounded text-xs">Alt+1</kbd>
          <span class="text-sm">for P2PAI dashboard</span>
        </div>
      </div>
    </div>

    <!-- P2PAI Performance Optimizations Demo -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center">
          <span class="text-purple-600 mr-2">⚡</span>
          P2PAI Performance Optimizations
        </h3>
        
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">Federated Learning</span>
            <span class="px-2 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded text-xs">
              Optimized
            </span>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">Privacy Protection</span>
            <span class="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded text-xs">
              Enhanced
            </span>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">Model Synchronization</span>
            <span class="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded text-xs">
              Real-time
            </span>
          </div>
          
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">MPC Training</span>
            <span class="px-2 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 rounded text-xs">
              Secure
            </span>
          </div>
        </div>
      </div>

      <!-- Training Session Demo -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold mb-4 flex items-center">
          <span class="text-indigo-600 mr-2">🧠</span>
          Live Training Session
        </h3>
        
        <div class="space-y-3">
          <div v-if="trainingActive" class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded p-3">
            <p class="text-sm text-green-600 dark:text-green-400 mb-2">Training in progress...</p>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div class="bg-green-600 h-2 rounded-full transition-all duration-1000" :style="{ width: trainingProgress + '%' }"></div>
            </div>
            <div class="flex justify-between text-xs text-green-600 dark:text-green-400 mt-1">
              <span>Round {{ currentRound }}/{{ totalRounds }}</span>
              <span>{{ trainingProgress.toFixed(1) }}%</span>
            </div>
          </div>
          
          <div v-else class="space-y-2">
            <Button @click="startTraining" size="sm" variant="outline" class="w-full">
              Start Federated Training
            </Button>
            
            <div class="text-xs text-gray-500 dark:text-gray-400">
              • Multi-party computation<br>
              • Privacy-preserving aggregation<br>
              • Secure model updates<br>
              • Distributed consensus
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced P2PAI Chart Demo -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center">
        <span class="text-purple-600 mr-2">📊</span>
        Enhanced P2PAI Data Visualization
      </h3>
      
      <EnhancedP2PAIChart
        title="Federated Training Metrics"
        subtitle="Real-time P2PAI training performance with enhanced features"
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
        @metric-change="onMetricChange"
      />
    </div>

    <!-- P2PAI Participant Network Demo -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center">
        <span class="text-green-600 mr-2">🌐</span>
        Participant Network Status
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {{ networkStats.totalNodes }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">Total Nodes</div>
        </div>
        
        <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div class="text-2xl font-bold text-green-600 dark:text-green-400">
            {{ networkStats.activeNodes }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">Active Nodes</div>
        </div>
        
        <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div class="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
            {{ networkStats.trainingNodes }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">Training Nodes</div>
        </div>
      </div>
      
      <div class="mt-4 space-x-2">
        <Button @click="simulateNodeJoin" size="sm" variant="outline">
          Simulate Node Join
        </Button>
        <Button @click="simulateNodeLeave" size="sm" variant="outline">
          Simulate Node Leave
        </Button>
        <Button @click="resetNetwork" size="sm" variant="ghost">
          Reset Network
        </Button>
      </div>
    </div>

    <!-- P2PAI Keyboard Shortcuts Demo -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 class="text-lg font-semibold mb-4 flex items-center">
        <span class="text-indigo-600 mr-2">⌨️</span>
        P2PAI Keyboard Shortcuts
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="shortcut in p2paiShortcuts" :key="shortcut.keys" class="flex justify-between items-center p-2 bg-gray-50 dark:bg-gray-700 rounded">
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
      <h4 class="font-semibold mb-3">P2PAI Demo Controls</h4>
      <div class="flex flex-wrap gap-2">
        <Button @click="refreshAllData" size="sm" :loading="refreshing">
          Refresh All Data
        </Button>
        <Button @click="simulateTrainingUpdate" size="sm" variant="outline">
          Simulate Training Update
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'
import { useErrorBoundary } from '@/composables/useErrorBoundary'
import { useOfflineMode } from '@/composables/useOfflineMode'
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts'
import Button from '@/components/ui/Button.vue'
import EnhancedP2PAIChart from './EnhancedP2PAIChart.vue'

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
const trainingActive = ref(false)
const trainingProgress = ref(0)
const currentRound = ref(0)
const totalRounds = ref(10)

// Network stats
const networkStats = ref({
  totalNodes: 5,
  activeNodes: 4,
  trainingNodes: 3
})

// Training interval
let trainingInterval = null

// Chart data for P2PAI
const chartData = ref({
  labels: ['Round 1', 'Round 2', 'Round 3', 'Round 4', 'Round 5'],
  datasets: [
    {
      label: 'Model Accuracy',
      data: [75, 82, 87, 91, 94],
      borderColor: '#9333ea',
      backgroundColor: '#9333ea20'
    },
    {
      label: 'Privacy Score',
      data: [85, 88, 90, 92, 95],
      borderColor: '#06b6d4',
      backgroundColor: '#06b6d420'
    },
    {
      label: 'Consensus Rate',
      data: [70, 78, 85, 89, 93],
      borderColor: '#10b981',
      backgroundColor: '#10b98120'
    }
  ]
})

// P2PAI specific shortcuts
const p2paiShortcuts = ref([
  { keys: 'Alt+1', description: 'P2PAI Dashboard' },
  { keys: 'Alt+2', description: 'Model Dashboard' },
  { keys: 'Alt+3', description: 'Training Monitor' },
  { keys: 'Alt+4', description: 'Participant Nodes' },
  { keys: 'Ctrl+F', description: 'Federated Training' },
  { keys: 'Ctrl+M', description: 'MPC Training' }
])

// Methods
const startTraining = () => {
  trainingActive.value = true
  trainingProgress.value = 0
  currentRound.value = 1
  
  trainingInterval = setInterval(() => {
    trainingProgress.value += Math.random() * 5
    currentRound.value = Math.min(Math.ceil((trainingProgress.value / 100) * totalRounds.value), totalRounds.value)
    
    if (trainingProgress.value >= 100) {
      trainingActive.value = false
      trainingProgress.value = 100
      currentRound.value = totalRounds.value
      clearInterval(trainingInterval)
      
      uiStore.addNotification({
        type: 'success',
        title: 'Training Completed',
        message: 'Federated training session completed successfully',
        duration: 3000
      })
    }
  }, 500)
  
  uiStore.addNotification({
    type: 'info',
    title: 'Training Started',
    message: 'Federated training session initiated',
    duration: 2000
  })
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
        data: dataset.data.map(() => Math.floor(Math.random() * 40) + 60)
      }))
    }
    
    // Update network stats
    networkStats.value = {
      totalNodes: Math.floor(Math.random() * 5) + 3,
      activeNodes: Math.floor(Math.random() * 4) + 2,
      trainingNodes: Math.floor(Math.random() * 3) + 1
    }
    
    uiStore.addNotification({
      type: 'success',
      title: 'P2PAI Data Refreshed',
      message: 'All P2PAI demo data has been updated',
      duration: 3000
    })
  } catch (error) {
    captureError(error, null, 'P2PAI Demo refresh')
  } finally {
    refreshing.value = false
  }
}

const simulateTrainingUpdate = () => {
  const updates = [
    'New participant joined training',
    'Model aggregation completed',
    'Privacy validation passed',
    'Consensus reached',
    'Training round completed'
  ]
  
  const randomUpdate = updates[Math.floor(Math.random() * updates.length)]
  
  uiStore.addNotification({
    type: 'info',
    title: 'Training Update',
    message: randomUpdate,
    duration: 2000
  })
}

const simulateNodeJoin = () => {
  networkStats.value.totalNodes++
  networkStats.value.activeNodes++
  
  uiStore.addNotification({
    type: 'success',
    title: 'Node Joined',
    message: 'New participant node joined the network',
    duration: 2000
  })
}

const simulateNodeLeave = () => {
  if (networkStats.value.totalNodes > 1) {
    networkStats.value.totalNodes--
    if (networkStats.value.activeNodes > 0) {
      networkStats.value.activeNodes--
    }
    
    uiStore.addNotification({
      type: 'warning',
      title: 'Node Left',
      message: 'A participant node left the network',
      duration: 2000
    })
  }
}

const resetNetwork = () => {
  networkStats.value = {
    totalNodes: 5,
    activeNodes: 4,
    trainingNodes: 3
  }
  
  uiStore.addNotification({
    type: 'info',
    title: 'Network Reset',
    message: 'Network statistics reset to default values',
    duration: 2000
  })
}

const toggleTheme = () => {
  themeStore.toggleTheme()
}

const showAllShortcuts = () => {
  showShortcutsHelp()
}

const resetDemo = () => {
  // Stop training if active
  if (trainingInterval) {
    clearInterval(trainingInterval)
  }
  trainingActive.value = false
  trainingProgress.value = 0
  currentRound.value = 0
  
  // Reset chart data
  chartData.value = {
    labels: ['Round 1', 'Round 2', 'Round 3', 'Round 4', 'Round 5'],
    datasets: [
      {
        label: 'Model Accuracy',
        data: [75, 82, 87, 91, 94],
        borderColor: '#9333ea',
        backgroundColor: '#9333ea20'
      },
      {
        label: 'Privacy Score',
        data: [85, 88, 90, 92, 95],
        borderColor: '#06b6d4',
        backgroundColor: '#06b6d420'
      },
      {
        label: 'Consensus Rate',
        data: [70, 78, 85, 89, 93],
        borderColor: '#10b981',
        backgroundColor: '#10b98120'
      }
    ]
  }
  
  // Reset network stats
  resetNetwork()
  
  uiStore.addNotification({
    type: 'info',
    title: 'Demo Reset',
    message: 'All P2PAI demo data has been reset to initial values',
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
      data: dataset.data.map(() => Math.floor(Math.random() * 40) + 60)
    }))
  }
}

const onExportChart = () => {
  uiStore.addNotification({
    type: 'success',
    title: 'Chart Exported',
    message: 'P2PAI chart has been exported as PNG',
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

const onMetricChange = (metric) => {
  uiStore.addNotification({
    type: 'info',
    title: 'Metric Changed',
    message: `Switched to ${metric} metric`,
    duration: 2000
  })
}

onMounted(() => {
  uiStore.addNotification({
    type: 'info',
    title: 'Enhanced P2PAI Features Demo',
    message: 'Welcome to the P2PAI enhancements showcase!',
    duration: 5000
  })
})

onUnmounted(() => {
  if (trainingInterval) {
    clearInterval(trainingInterval)
  }
})
</script>

<style scoped>
.enhanced-p2pai-demo {
  max-width: 1200px;
  margin: 0 auto;
}

kbd {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.75rem;
}
</style>