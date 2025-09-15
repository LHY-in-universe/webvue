<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <Button 
              @click="$router.back()" 
              variant="ghost" 
              size="sm" 
              class="mr-4"
            >
              ← 返回
            </Button>
            <ChartBarIcon class="h-8 w-8 text-orange-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              性能指标监控
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <Button 
              @click="refreshData" 
              variant="outline" 
              size="sm" 
              :loading="loading"
            >
              刷新数据
            </Button>
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Performance Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="平均响应时间"
          :value="avgResponseTime"
          unit="ms"
          :icon="ClockIcon"
          variant="primary"
          :trend="-5.2"
          trend-label="改进"
          description="系统平均响应时间"
        />
        <StatCard
          title="CPU 使用率"
          :value="cpuUsage"
          unit="%"
          :icon="CpuChipIcon"
          variant="warning"
          :trend="2.1"
          trend-label="vs 昨天"
          description="集群平均 CPU 使用率"
        />
        <StatCard
          title="内存使用率"
          :value="memoryUsage"
          unit="%"
          :icon="ServerIcon"
          variant="info"
          :trend="-1.8"
          trend-label="vs 昨天"
          description="集群平均内存使用率"
        />
        <StatCard
          title="网络吞吐量"
          :value="networkThroughput"
          unit="MB/s"
          :icon="SignalIcon"
          variant="success"
          :trend="15.3"
          trend-label="vs 昨天"
          description="网络数据传输速率"
        />
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- System Performance Chart -->
        <Card>
          <template #header>
            <div class="flex items-center">
              <ChartBarIcon class="w-6 h-6 text-blue-600 mr-3" />
              <h2 class="text-lg font-semibold">系统性能趋势</h2>
            </div>
          </template>
          
          <div v-if="loading" class="h-64 flex items-center justify-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
          
          <div v-else-if="error" class="h-64 flex items-center justify-center">
            <div class="text-center">
              <ExclamationTriangleIcon class="w-12 h-12 text-red-400 mx-auto mb-4" />
              <p class="text-red-500 dark:text-red-400 mb-2">{{ error }}</p>
              <Button @click="refreshData" variant="ghost" size="sm">
                重试
              </Button>
            </div>
          </div>
          
          <div v-else class="h-64 flex items-center justify-center border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
            <div class="text-center">
              <ChartBarIcon class="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p class="text-gray-500 dark:text-gray-400">性能图表占位符</p>
              <p class="text-sm text-gray-400">实际部署中将显示实时性能图表</p>
              <p v-if="lastUpdate" class="text-xs text-gray-400 mt-2">
                最后更新: {{ new Date(lastUpdate).toLocaleTimeString() }}
              </p>
            </div>
          </div>
        </Card>

        <!-- Node Performance -->
        <Card>
          <template #header>
            <div class="flex items-center">
              <ServerIcon class="w-6 h-6 text-green-600 mr-3" />
              <h2 class="text-lg font-semibold">节点性能详情</h2>
            </div>
          </template>
          
          <div class="space-y-4">
            <div 
              v-for="node in nodePerformance" 
              :key="node.id"
              class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="font-medium text-gray-900 dark:text-white">
                  {{ node.name }}
                </div>
                <div class="flex items-center space-x-2">
                  <span :class="getStatusColor(node.status)" class="w-2 h-2 rounded-full"></span>
                  <span class="text-sm text-gray-500 dark:text-gray-400">{{ node.status }}</span>
                </div>
              </div>
              
              <div class="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <div class="text-gray-500 dark:text-gray-400">CPU</div>
                  <div class="font-medium">{{ node.cpu }}%</div>
                </div>
                <div>
                  <div class="text-gray-500 dark:text-gray-400">内存</div>
                  <div class="font-medium">{{ node.memory }}%</div>
                </div>
                <div>
                  <div class="text-gray-500 dark:text-gray-400">负载</div>
                  <div class="font-medium">{{ node.load }}</div>
                </div>
              </div>
            </div>
          </div>
        </Card>

        <!-- Resource Utilization -->
        <Card>
          <template #header>
            <div class="flex items-center">
              <CpuChipIcon class="w-6 h-6 text-purple-600 mr-3" />
              <h2 class="text-lg font-semibold">资源利用率</h2>
            </div>
          </template>
          
          <div class="space-y-6">
            <div>
              <div class="flex justify-between mb-2">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">CPU 集群利用率</span>
                <span class="text-sm text-gray-500 dark:text-gray-400">{{ cpuUsage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: cpuUsage + '%' }"
                ></div>
              </div>
            </div>
            
            <div>
              <div class="flex justify-between mb-2">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">内存集群利用率</span>
                <span class="text-sm text-gray-500 dark:text-gray-400">{{ memoryUsage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-green-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: memoryUsage + '%' }"
                ></div>
              </div>
            </div>
            
            <div>
              <div class="flex justify-between mb-2">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">存储利用率</span>
                <span class="text-sm text-gray-500 dark:text-gray-400">{{ storageUsage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-yellow-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: storageUsage + '%' }"
                ></div>
              </div>
            </div>
            
            <div>
              <div class="flex justify-between mb-2">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">网络带宽利用率</span>
                <span class="text-sm text-gray-500 dark:text-gray-400">{{ networkUsage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-purple-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: networkUsage + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </Card>

        <!-- Performance Alerts -->
        <Card>
          <template #header>
            <div class="flex items-center">
              <ExclamationTriangleIcon class="w-6 h-6 text-red-600 mr-3" />
              <h2 class="text-lg font-semibold">性能警报</h2>
            </div>
          </template>
          
          <div class="space-y-3">
            <div 
              v-for="alert in performanceAlerts" 
              :key="alert.id"
              :class="getAlertColor(alert.level)"
              class="p-3 rounded-lg"
            >
              <div class="flex items-start">
                <ExclamationTriangleIcon class="w-5 h-5 mt-0.5 mr-3 flex-shrink-0" />
                <div class="flex-1">
                  <div class="font-medium">{{ alert.message }}</div>
                  <div class="text-sm mt-1">{{ alert.node }}</div>
                  <div class="text-xs mt-1 opacity-75">{{ alert.time }}</div>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useEdgeAIStore } from '@/stores/edgeai'
import { useApiOptimization } from '@/composables/useApiOptimization'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import {
  ChartBarIcon,
  ClockIcon,
  CpuChipIcon,
  ServerIcon,
  SignalIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

// Store and API setup
const edgeaiStore = useEdgeAIStore()
const { cachedApiCall } = useApiOptimization()

// State
const loading = ref(false)
const error = ref(null)
const performanceData = ref(null)
const nodePerformance = ref([])
const performanceAlerts = ref([])
const lastUpdate = ref(null)

// Computed performance metrics
const avgResponseTime = computed(() => {
  if (!performanceData.value) return 0
  return Math.round(performanceData.value.response_time || 0)
})

const cpuUsage = computed(() => {
  if (!performanceData.value) return 0
  return Math.round(performanceData.value.cpu_usage || 0)
})

const memoryUsage = computed(() => {
  if (!performanceData.value) return 0
  return Math.round(performanceData.value.memory_usage || 0)
})

const storageUsage = computed(() => {
  if (!performanceData.value) return 0
  return Math.round(performanceData.value.storage_usage || 0)
})

const networkUsage = computed(() => {
  if (!performanceData.value) return 0
  return Math.round(performanceData.value.network_usage || 0)
})

const networkThroughput = computed(() => {
  if (!performanceData.value) return 0
  return Number((performanceData.value.network_throughput || 0).toFixed(1))
})

// Auto-refresh
let refreshInterval = null

// Load performance data
const loadPerformanceData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('PerformanceMetrics')
  loading.value = true
  error.value = null
  
  try {
    const [metricsResult, nodesResult, alertsResult] = await Promise.all([
      cachedApiCall('edgeai-performance-metrics', 
        () => edgeaiService.performance.getMetrics(), 
        30 * 1000
      ),
      cachedApiCall('edgeai-node-performance', 
        () => edgeaiService.nodes.getNodes(), 
        30 * 1000
      ),
      cachedApiCall('edgeai-performance-alerts', 
        () => edgeaiService.performance.getAlerts(), 
        60 * 1000
      )
    ])
    
    if (metricsResult) {
      performanceData.value = metricsResult
    }
    
    if (nodesResult && nodesResult.data) {
      nodePerformance.value = nodesResult.data.map(node => ({
        id: node.id,
        name: node.name,
        status: node.status,
        cpu: Math.round(node.cpuUsage || 0),
        memory: Math.round(node.memoryUsage || 0),
        load: Number((node.loadAverage || 0).toFixed(1))
      }))
    }
    
    if (alertsResult && alertsResult.data) {
      performanceAlerts.value = alertsResult.data.map(alert => ({
        id: alert.id,
        level: alert.severity || 'info',
        message: alert.message,
        node: alert.node_name || '系统整体',
        time: formatRelativeTime(alert.created_at)
      }))
    }
    
    lastUpdate.value = new Date().toISOString()
    pageMonitor.end()
    
  } catch (err) {
    console.error('Failed to load performance data:', err)
    error.value = err.message || 'Failed to load performance data'
    pageMonitor.end()
  } finally {
    loading.value = false
  }
}

// Format relative time
const formatRelativeTime = (timestamp) => {
  if (!timestamp) return '未知时间'
  
  const now = new Date()
  const alertTime = new Date(timestamp)
  const diffMs = now - alertTime
  const diffMinutes = Math.floor(diffMs / 60000)
  
  if (diffMinutes < 1) return '刚刚'
  if (diffMinutes < 60) return `${diffMinutes} 分钟前`
  
  const diffHours = Math.floor(diffMinutes / 60)
  if (diffHours < 24) return `${diffHours} 小时前`
  
  const diffDays = Math.floor(diffHours / 24)
  return `${diffDays} 天前`
}

// Setup auto-refresh
const setupAutoRefresh = () => {
  if (refreshInterval) clearInterval(refreshInterval)
  
  refreshInterval = setInterval(async () => {
    await loadPerformanceData()
  }, 30000) // Refresh every 30 seconds
}

// Manual refresh
const refreshData = async () => {
  await loadPerformanceData()
}

const getStatusColor = (status) => {
  const colors = {
    online: 'bg-green-500',
    warning: 'bg-yellow-500',
    offline: 'bg-red-500'
  }
  return colors[status] || 'bg-gray-500'
}

const getAlertColor = (level) => {
  const colors = {
    info: 'bg-blue-50 text-blue-800 dark:bg-blue-900/50 dark:text-blue-200',
    warning: 'bg-yellow-50 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-200',
    error: 'bg-red-50 text-red-800 dark:bg-red-900/50 dark:text-red-200'
  }
  return colors[level] || 'bg-gray-50 text-gray-800'
}
</script>