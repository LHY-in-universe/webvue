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
            <Button @click="exportLogs" variant="primary" size="sm">
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

        <div class="space-y-2">
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
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

const selectedLevel = ref('all')
const selectedTimeRange = ref('24h')
const selectedSource = ref('all')
const searchQuery = ref('')
const autoRefresh = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)

let refreshInterval = null

const systemLogs = ref([
  {
    id: 1,
    level: 'info',
    source: 'system',
    message: 'Edge node edge-01 connected successfully',
    timestamp: '2024-01-10 10:30:15',
    details: 'Connection established from IP: 192.168.1.100'
  },
  {
    id: 2,
    level: 'warning',
    source: 'application',
    message: 'High CPU usage detected on node edge-02',
    timestamp: '2024-01-10 10:28:42',
    details: 'CPU usage: 87%, Memory usage: 65%'
  },
  {
    id: 3,
    level: 'error',
    source: 'network',
    message: 'Failed to connect to edge-03',
    timestamp: '2024-01-10 10:25:18',
    details: 'Connection timeout after 30 seconds, retrying...'
  },
  {
    id: 4,
    level: 'info',
    source: 'application',
    message: 'Training task completed successfully',
    timestamp: '2024-01-10 10:22:03',
    details: 'Task ID: task-12345, Duration: 2h 15m'
  },
  {
    id: 5,
    level: 'debug',
    source: 'storage',
    message: 'Cache cleanup completed',
    timestamp: '2024-01-10 10:20:30',
    details: 'Freed 1.2GB of cache space'
  },
  {
    id: 6,
    level: 'error',
    source: 'system',
    message: 'Disk space running low',
    timestamp: '2024-01-10 10:15:45',
    details: 'Available space: 2.1GB, Usage: 89%'
  }
])

const filteredLogs = computed(() => {
  let logs = systemLogs.value

  // Filter by level
  if (selectedLevel.value !== 'all') {
    logs = logs.filter(log => log.level === selectedLevel.value)
  }

  // Filter by source
  if (selectedSource.value !== 'all') {
    logs = logs.filter(log => log.source === selectedSource.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    logs = logs.filter(log => 
      log.message.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      log.details?.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Pagination
  const startIndex = (currentPage.value - 1) * pageSize.value
  return logs.slice(startIndex, startIndex + pageSize.value)
})

const totalLogs = computed(() => systemLogs.value.length)
const errorLogs = computed(() => systemLogs.value.filter(log => log.level === 'error').length)
const warningLogs = computed(() => systemLogs.value.filter(log => log.level === 'warning').length)
const infoLogs = computed(() => systemLogs.value.filter(log => log.level === 'info').length)

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

const refreshLogs = () => {
  console.log('刷新日志...')
  // 实际实现中会从服务器获取最新日志
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

const exportLogs = () => {
  console.log('导出日志...')
  // 实际实现中会导出筛选后的日志
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

onMounted(() => {
  refreshLogs()
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>