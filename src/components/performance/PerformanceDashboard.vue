<template>
  <div class="performance-dashboard p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          Performance Dashboard
        </h1>
        <p class="text-gray-600 dark:text-gray-400 mt-1">
          Monitor and analyze your application's performance metrics
        </p>
      </div>
      
      <div class="flex items-center space-x-3">
        <!-- Auto-refresh toggle -->
        <div class="flex items-center space-x-2">
          <label class="text-sm text-gray-600 dark:text-gray-400">Auto-refresh:</label>
          <SwitchToggle v-model="autoRefresh" size="sm" />
        </div>
        
        <!-- Export button -->
        <Button
          variant="ghost"
          size="sm"
          :leftIcon="ArrowDownTrayIcon"
          @click="exportData"
        >
          Export
        </Button>
        
        <!-- Settings -->
        <Button
          variant="ghost"
          size="sm"
          :leftIcon="CogIcon"
          @click="showSettings = true"
        >
          Settings
        </Button>
        
        <!-- Clear data -->
        <Button
          variant="ghost"
          size="sm"
          :leftIcon="TrashIcon"
          @click="confirmClearData"
        >
          Clear
        </Button>
      </div>
    </div>

    <!-- Status indicators -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <StatCard
        title="Monitoring Status"
        :value="isMonitoringEnabled ? 'Active' : 'Disabled'"
        :icon="isMonitoringEnabled ? CheckCircleIcon : XCircleIcon"
        :variant="isMonitoringEnabled ? 'success' : 'warning'"
      />
      
      <StatCard
        title="Tracked Components"
        :value="performanceData.components.size"
        :icon="CubeIcon"
        variant="info"
      />
      
      <StatCard
        title="Total Renders"
        :value="totalRenders"
        :icon="ArrowPathIcon"
        variant="primary"
      />
      
      <StatCard
        title="Error Count"
        :value="performanceData.errors.length"
        :icon="ExclamationTriangleIcon"
        :variant="performanceData.errors.length > 0 ? 'danger' : 'success'"
      />
    </div>

    <!-- Performance Analysis -->
    <Card class="p-6">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Performance Analysis
      </h2>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Summary metrics -->
        <div>
          <h3 class="text-md font-medium text-gray-900 dark:text-white mb-3">Summary</h3>
          <div class="space-y-3">
            <div class="flex justify-between">
              <span class="text-gray-600 dark:text-gray-400">Average Render Time:</span>
              <span class="font-medium" :class="averageRenderTime > 16 ? 'text-red-600' : 'text-green-600'">
                {{ averageRenderTime.toFixed(2) }}ms
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600 dark:text-gray-400">Memory Usage:</span>
              <span class="font-medium">{{ formatBytes(currentMemoryUsage) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600 dark:text-gray-400">Memory Trend:</span>
              <span class="font-medium" :class="getMemoryTrendColor(analysis.summary.memoryTrend)">
                {{ analysis.summary.memoryTrend }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- Recommendations -->
        <div>
          <h3 class="text-md font-medium text-gray-900 dark:text-white mb-3">Recommendations</h3>
          <div v-if="analysis.recommendations.length > 0" class="space-y-2">
            <Alert
              v-for="(recommendation, index) in analysis.recommendations"
              :key="index"
              :type="recommendation.severity === 'high' ? 'error' : 'warning'"
              :message="recommendation.message"
              size="sm"
              :closable="false"
            />
          </div>
          <div v-else class="text-gray-500 dark:text-gray-400 text-sm">
            No performance issues detected
          </div>
        </div>
      </div>
    </Card>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Render time chart -->
      <Card class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Render Performance
        </h3>
        <MetricChart
          :chart-data="renderChartData"
          :options="{ maintainAspectRatio: false }"
          height="300px"
          chart-type="line"
        />
      </Card>

      <!-- Memory usage chart -->
      <Card class="p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Memory Usage
        </h3>
        <MetricChart
          :chart-data="memoryChartData"
          :options="{ maintainAspectRatio: false }"
          height="300px"
          chart-type="area"
        />
      </Card>
    </div>

    <!-- Component performance table -->
    <Card class="p-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Component Performance
      </h3>
      <DataTable
        :data="componentTableData"
        :columns="componentTableColumns"
        :show-pagination="componentTableData.length > 10"
        :page-size="10"
        :sortable="true"
        :default-sort="{ key: 'averageRenderTime', order: 'desc' }"
        size="sm"
      />
    </Card>

    <!-- Error log -->
    <Card v-if="performanceData.errors.length > 0" class="p-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Error Log
      </h3>
      <div class="space-y-2 max-h-64 overflow-y-auto">
        <Alert
          v-for="(error, index) in recentErrors"
          :key="index"
          type="error"
          :title="`${error.componentName}: ${error.message}`"
          :message="`${formatDate(error.timestamp)} - ${error.url}`"
          size="sm"
          :closable="false"
        />
      </div>
    </Card>

    <!-- Settings Modal -->
    <Modal
      v-model:is-open="showSettings"
      title="Performance Monitoring Settings"
      size="md"
    >
      <PerformanceSettings
        :config="monitoringConfig"
        @update-config="updateConfig"
        @close="showSettings = false"
      />
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { usePerformanceMonitor } from '@/composables/usePerformanceMonitor'
import { $notify } from '@/composables/useNotifications'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import DataTable from '@/components/ui/DataTable.vue'
import MetricChart from '@/components/charts/MetricChart.vue'
import Alert from '@/components/ui/Alert.vue'
import Modal from '@/components/ui/Modal.vue'
import SwitchToggle from '@/components/ui/SwitchToggle.vue'
import PerformanceSettings from './PerformanceSettings.vue'
import {
  CheckCircleIcon,
  XCircleIcon,
  CubeIcon,
  ArrowPathIcon,
  ExclamationTriangleIcon,
  ArrowDownTrayIcon,
  CogIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

const {
  performanceData,
  isMonitoringEnabled,
  monitoringConfig,
  analyzePerformance,
  exportPerformanceData,
  clearPerformanceData,
  updateConfig
} = usePerformanceMonitor()

// State
const autoRefresh = ref(true)
const showSettings = ref(false)
let refreshInterval = null

// Computed properties
const analysis = computed(() => analyzePerformance())

const totalRenders = computed(() => {
  return Array.from(performanceData.components.values())
    .reduce((sum, comp) => sum + comp.totalRenders, 0)
})

const averageRenderTime = computed(() => {
  const components = Array.from(performanceData.components.values())
  if (components.length === 0) return 0
  
  return components
    .reduce((sum, comp) => sum + comp.averageRenderTime, 0) / components.length
})

const currentMemoryUsage = computed(() => {
  const recent = performanceData.memory.slice(-1)[0]
  return recent?.usedJSHeapSize || 0
})

const renderChartData = computed(() => {
  const recentRenders = performanceData.renders.slice(-50)
  
  return {
    labels: recentRenders.map(render => 
      new Date(render.timestamp).toLocaleTimeString()
    ),
    datasets: [{
      label: 'Render Time (ms)',
      data: recentRenders.map(render => render.renderTime),
      borderColor: '#3B82F6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4
    }]
  }
})

const memoryChartData = computed(() => {
  const recentMemory = performanceData.memory.slice(-50)
  
  return {
    labels: recentMemory.map(mem => 
      new Date(mem.timestamp).toLocaleTimeString()
    ),
    datasets: [{
      label: 'Used Memory (MB)',
      data: recentMemory.map(mem => mem.usedJSHeapSize / 1024 / 1024),
      borderColor: '#10B981',
      backgroundColor: 'rgba(16, 185, 129, 0.2)',
      fill: true,
      tension: 0.4
    }]
  }
})

const componentTableData = computed(() => {
  return Array.from(performanceData.components.values())
    .map(component => ({
      ...component,
      renderRate: component.totalRenders / (Date.now() - component.renderHistory[0]?.timestamp || 1) * 1000
    }))
})

const componentTableColumns = ref([
  {
    key: 'name',
    title: 'Component',
    sortable: true
  },
  {
    key: 'totalRenders',
    title: 'Renders',
    sortable: true,
    align: 'center'
  },
  {
    key: 'averageRenderTime',
    title: 'Avg Time (ms)',
    sortable: true,
    align: 'center',
    format: 'number'
  },
  {
    key: 'maxRenderTime',
    title: 'Max Time (ms)', 
    sortable: true,
    align: 'center',
    format: 'number'
  },
  {
    key: 'errorCount',
    title: 'Errors',
    sortable: true,
    align: 'center'
  }
])

const recentErrors = computed(() => {
  return performanceData.errors.slice(-10).reverse()
})

// Methods
const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`
}

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

const getMemoryTrendColor = (trend) => {
  switch (trend) {
    case 'increasing': return 'text-red-600'
    case 'decreasing': return 'text-green-600'
    case 'stable': return 'text-blue-600'
    default: return 'text-gray-600'
  }
}

const exportData = () => {
  const data = exportPerformanceData('json')
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `performance-data-${new Date().toISOString()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  $notify.success('Performance data exported successfully')
}

const confirmClearData = async () => {
  const result = await $notify.confirmWarning(
    'This will clear all performance monitoring data. Are you sure?'
  )
  
  if (result.confirmed) {
    clearPerformanceData()
    $notify.success('Performance data cleared')
  }
}

const startAutoRefresh = () => {
  if (refreshInterval) return
  
  refreshInterval = setInterval(() => {
    // Trigger reactivity update
    performanceData.components = new Map(performanceData.components)
  }, 2000)
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

// Watch auto-refresh toggle
watch(autoRefresh, (enabled) => {
  if (enabled) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
})

// Lifecycle
onMounted(() => {
  if (autoRefresh.value) {
    startAutoRefresh()
  }
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.performance-dashboard {
  @apply min-h-screen bg-gray-50 dark:bg-gray-900;
}
</style>