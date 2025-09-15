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
            <DocumentTextIcon class="h-8 w-8 text-indigo-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              系统日志
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <Button 
              @click="refreshLogs" 
              variant="outline" 
              size="sm" 
              :loading="loading"
            >
              刷新日志
            </Button>
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Log Controls -->
      <Card class="mb-6">
        <template #header>
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold">日志筛选</h2>
            <Button @click="exportLogs" variant="primary" size="sm" :loading="loading">
              <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
              导出日志
            </Button>
          </div>
        </template>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              日志级别
            </label>
            <select 
              v-model="selectedLevel"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600"
            >
              <option value="all">全部级别</option>
              <option value="info">信息</option>
              <option value="warning">警告</option>
              <option value="error">错误</option>
              <option value="debug">调试</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              时间范围
            </label>
            <select 
              v-model="selectedTimeRange"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600"
            >
              <option value="1h">最近 1 小时</option>
              <option value="6h">最近 6 小时</option>
              <option value="24h">最近 24 小时</option>
              <option value="7d">最近 7 天</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              日志来源
            </label>
            <select 
              v-model="selectedSource"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600"
            >
              <option value="all">全部来源</option>
              <option value="system">系统</option>
              <option value="application">应用</option>
              <option value="network">网络</option>
              <option value="storage">存储</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              搜索
            </label>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索日志内容..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600"
            />
          </div>
        </div>
      </Card>

      <!-- Log Statistics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="总日志条数"
          :value="totalLogs"
          :icon="DocumentTextIcon"
          variant="primary"
          description="当前筛选条件下的日志数量"
        />
        <StatCard
          title="错误日志"
          :value="errorLogs"
          :icon="ExclamationTriangleIcon"
          variant="danger"
          description="需要关注的错误日志"
        />
        <StatCard
          title="警告日志"
          :value="warningLogs"
          :icon="ExclamationCircleIcon"
          variant="warning"
          description="系统警告日志"
        />
        <StatCard
          title="信息日志"
          :value="infoLogs"
          :icon="InformationCircleIcon"
          variant="info"
          description="常规信息日志"
        />
      </div>

      <!-- Log List -->
      <Card>
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <DocumentTextIcon class="w-6 h-6 text-indigo-600 mr-3" />
              <h2 class="text-lg font-semibold">日志详情</h2>
            </div>
            <div class="flex items-center space-x-2">
              <Button @click="refreshLogs" variant="ghost" size="sm">
                <ArrowPathIcon class="w-4 h-4 mr-2" />
                刷新
              </Button>
              <Button @click="toggleAutoRefresh" :variant="autoRefresh ? 'primary' : 'ghost'" size="sm">
                {{ autoRefresh ? '停止' : '开启' }}自动刷新
              </Button>
            </div>
          </div>
        </template>

        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span class="ml-3 text-gray-600 dark:text-gray-400">加载日志中...</span>
        </div>
        
        <div v-else-if="error" class="text-center py-12">
          <ExclamationTriangleIcon class="w-12 h-12 text-red-400 mx-auto mb-4" />
          <p class="text-red-500 dark:text-red-400 mb-4">{{ error }}</p>
          <Button @click="refreshLogs" variant="ghost" size="sm">
            重试
          </Button>
        </div>
        
        <div v-else-if="filteredLogs.length === 0" class="text-center py-12">
          <DocumentTextIcon class="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p class="text-gray-500 dark:text-gray-400">暂无日志数据</p>
        </div>
        
        <div v-else class="space-y-2">
          <div 
            v-for="log in filteredLogs" 
            :key="log.id"
            :class="getLogColor(log.level)"
            class="p-4 rounded-lg border-l-4"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center space-x-3 mb-2">
                  <component :is="getLogIcon(log.level)" class="w-5 h-5 flex-shrink-0" />
                  <span class="text-xs font-medium uppercase tracking-wide">
                    {{ log.level }}
                  </span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">
                    {{ log.source }}
                  </span>
                  <span class="text-xs text-gray-500 dark:text-gray-400">
                    {{ log.timestamp }}
                  </span>
                </div>
                <div class="text-sm font-medium mb-1">
                  {{ log.message }}
                </div>
                <div v-if="log.details" class="text-xs text-gray-600 dark:text-gray-400 font-mono bg-gray-50 dark:bg-gray-800 p-2 rounded">
                  {{ log.details }}
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="lastUpdate" class="text-center py-4">
            <p class="text-xs text-gray-400">
              最后更新: {{ new Date(lastUpdate).toLocaleTimeString() }}
            </p>
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
          <div class="text-sm text-gray-700 dark:text-gray-300">
            显示 {{ (currentPage - 1) * pageSize + 1 }} 到 {{ Math.min(currentPage * pageSize, totalLogs) }} 条，共 {{ totalLogs }} 条
          </div>
          <div class="flex space-x-2">
            <Button 
              @click="previousPage" 
              :disabled="currentPage === 1" 
              variant="ghost" 
              size="sm"
            >
              上一页
            </Button>
            <Button 
              @click="nextPage" 
              :disabled="currentPage * pageSize >= totalLogs" 
              variant="ghost" 
              size="sm"
            >
              下一页
            </Button>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useApiOptimization } from '@/composables/useApiOptimization'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import {
  DocumentTextIcon,
  ArrowDownTrayIcon,
  ExclamationTriangleIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

// API setup
const { cachedApiCall } = useApiOptimization()

// Filter states
const selectedLevel = ref('all')
const selectedTimeRange = ref('24h')
const selectedSource = ref('all')
const searchQuery = ref('')
const autoRefresh = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)

// Data states
const loading = ref(false)
const error = ref(null)
const systemLogs = ref([])
const totalCount = ref(0)
const lastUpdate = ref(null)

// Auto-refresh interval
let refreshInterval = null

// Load system logs from API
const loadSystemLogs = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('SystemLogs')
  loading.value = true
  error.value = null
  
  try {
    const params = {
      level: selectedLevel.value === 'all' ? undefined : selectedLevel.value,
      time_range: selectedTimeRange.value,
      source: selectedSource.value === 'all' ? undefined : selectedSource.value,
      query: searchQuery.value || undefined,
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    const cacheKey = `edgeai-logs-${JSON.stringify(params)}`
    const result = await cachedApiCall(cacheKey, 
      () => edgeaiService.logs.getLogs(params), 
      30 * 1000 // Cache for 30 seconds
    )
    
    if (result && result.data) {
      systemLogs.value = result.data.map(log => ({
        id: log.id,
        level: log.level,
        source: log.source || 'system',
        message: log.message,
        timestamp: formatTimestamp(log.timestamp),
        details: log.details || log.context
      }))
      totalCount.value = result.total || result.data.length
    }
    
    lastUpdate.value = new Date().toISOString()
    pageMonitor.end()
    
  } catch (err) {
    console.error('Failed to load system logs:', err)
    error.value = err.message || 'Failed to load system logs'
    pageMonitor.end()
  } finally {
    loading.value = false
  }
}

// Format timestamp
const formatTimestamp = (timestamp) => {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// Computed properties
const filteredLogs = computed(() => systemLogs.value)

const totalLogs = computed(() => totalCount.value)
const errorLogs = computed(() => {
  return systemLogs.value.filter(log => log.level === 'error').length
})
const warningLogs = computed(() => {
  return systemLogs.value.filter(log => log.level === 'warning').length
})
const infoLogs = computed(() => {
  return systemLogs.value.filter(log => log.level === 'info').length
})

const getLogColor = (level) => {
  const colors = {
    info: 'bg-blue-50 dark:bg-blue-900/20 border-blue-500',
    warning: 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-500',
    error: 'bg-red-50 dark:bg-red-900/20 border-red-500',
    debug: 'bg-gray-50 dark:bg-gray-800 border-gray-400'
  }
  return colors[level] || 'bg-gray-50 dark:bg-gray-800 border-gray-400'
}

const getLogIcon = (level) => {
  const icons = {
    info: InformationCircleIcon,
    warning: ExclamationCircleIcon,
    error: ExclamationTriangleIcon,
    debug: DocumentTextIcon
  }
  return icons[level] || DocumentTextIcon
}

const refreshLogs = async () => {
  await loadSystemLogs()
}

const toggleAutoRefresh = () => {
  autoRefresh.value = !autoRefresh.value
  
  if (autoRefresh.value) {
    refreshInterval = setInterval(() => {
      refreshLogs()
    }, 10000) // 10秒刷新一次
  } else {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
  }
}

const exportLogs = async () => {
  try {
    loading.value = true
    
    const params = {
      level: selectedLevel.value === 'all' ? undefined : selectedLevel.value,
      time_range: selectedTimeRange.value,
      source: selectedSource.value === 'all' ? undefined : selectedSource.value,
      query: searchQuery.value || undefined,
      format: 'txt'
    }
    
    await edgeaiService.logs.exportLogs(params, `system_logs_${new Date().toISOString().split('T')[0]}.txt`)
    
  } catch (err) {
    console.error('Failed to export logs:', err)
    error.value = err.message || 'Failed to export logs'
  } finally {
    loading.value = false
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value * pageSize.value < totalLogs.value) {
    currentPage.value++
  }
}

// Watch for filter changes
watch([selectedLevel, selectedTimeRange, selectedSource], () => {
  currentPage.value = 1 // Reset to first page when filters change
  loadSystemLogs()
}, { deep: true })

watch(currentPage, () => {
  loadSystemLogs()
})

// Debounced search
let searchTimeout = null
watch(searchQuery, (newQuery) => {
  if (searchTimeout) clearTimeout(searchTimeout)
  
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadSystemLogs()
  }, 500)
})

// Lifecycle
onMounted(async () => {
  await loadSystemLogs()
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>