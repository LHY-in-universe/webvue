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
            <CpuChipIcon class="h-8 w-8 text-blue-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              任务管理
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600 dark:text-gray-400">Loading tasks data...</span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-8">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
              Failed to load tasks data
            </h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </div>
            <div class="mt-3">
              <Button @click="loadTasksData" variant="ghost" size="sm" class="text-red-800 dark:text-red-200 hover:bg-red-100 dark:hover:bg-red-800/30">
                Try again
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Task Statistics -->
      <template v-else>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="运行中任务"
          :value="runningTasks"
          :icon="PlayIcon"
          variant="primary"
          description="当前正在执行的任务"
        />
        <StatCard
          title="队列中任务"
          :value="queuedTasks"
          :icon="ClockIcon"
          variant="warning"
          description="等待执行的任务"
        />
        <StatCard
          title="已完成任务"
          :value="completedTasks"
          :icon="CheckCircleIcon"
          variant="success"
          description="今日完成的任务"
        />
        <StatCard
          title="失败任务"
          :value="failedTasks"
          :icon="XCircleIcon"
          variant="danger"
          description="需要重试的任务"
        />
      </div>

      <!-- Task List -->
      <Card class="mb-8">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <CpuChipIcon class="w-6 h-6 text-blue-600 mr-3" />
              <h2 class="text-lg font-semibold">任务列表</h2>
            </div>
            <Button @click="createNewTask" variant="primary" size="sm">
              <PlusIcon class="w-4 h-4 mr-2" />
              新建任务
            </Button>
          </div>
        </template>

        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  任务名称
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  状态
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  节点
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  进度
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  创建时间
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  操作
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="task in tasks" :key="task.id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ task.name }}
                  </div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">
                    {{ task.type }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusColor(task.status)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ task.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ task.node }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      class="bg-blue-600 h-2 rounded-full" 
                      :style="{ width: task.progress + '%' }"
                    ></div>
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {{ task.progress }}%
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ task.createdAt }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <Button 
                    @click="viewTask(task)" 
                    variant="ghost" 
                    size="sm"
                  >
                    查看
                  </Button>
                  <Button 
                    v-if="task.status === 'failed'" 
                    @click="retryTask(task)" 
                    variant="primary" 
                    size="sm"
                  >
                    重试
                  </Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import { useApiOptimization } from '@/composables/useApiOptimization'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import {
  CpuChipIcon,
  PlayIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  PlusIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const { error: showError } = useNotifications()
const { cachedApiCall, clearCache } = useApiOptimization()

// Loading and error states
const loading = ref(false)
const error = ref(null)
const refreshInterval = ref(null)

// Tasks data (will be loaded from API)
const tasks = ref([])

const runningTasks = computed(() => 
  tasks.value.filter(task => task.status === 'running').length
)

const queuedTasks = computed(() => 
  tasks.value.filter(task => task.status === 'queued').length
)

const completedTasks = computed(() => 
  tasks.value.filter(task => task.status === 'completed').length
)

const failedTasks = computed(() => 
  tasks.value.filter(task => task.status === 'failed').length
)

// Load tasks data from API
const loadTasksData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('EdgeAITaskManager')
  loading.value = true
  error.value = null
  
  try {
    const result = await cachedApiCall('edgeai-tasks', 
      () => edgeaiService.tasks.getTasks(), 
      30 * 1000 // Cache for 30 seconds for real-time data
    )

    if (result && Array.isArray(result)) {
      tasks.value = result.map(task => ({
        id: task.id,
        name: task.name || 'Unnamed Task',
        type: task.type || '深度学习',
        status: task.status || 'queued',
        node: task.node_id || '-',
        progress: task.progress || 0,
        createdAt: task.created_at || new Date().toISOString()
      }))
    }

    pageMonitor.end({ success: true, taskCount: tasks.value.length })
  } catch (err) {
    console.error('Failed to load tasks data:', err)
    error.value = err.message || 'Failed to load tasks data'
    pageMonitor.end({ success: false, error: err.message })
  } finally {
    loading.value = false
  }
}

// Setup auto-refresh for real-time task updates
const setupAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  
  refreshInterval.value = setInterval(() => {
    if (!loading.value) {
      loadTasksData()
    }
  }, 15 * 1000) // Refresh every 15 seconds for tasks
}

const getStatusColor = (status) => {
  const colors = {
    running: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    queued: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    completed: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    failed: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const createNewTask = () => {
  router.push('/edgeai/create-project')
}

const viewTask = (task) => {
  console.log('查看任务:', task.name)
  router.push(`/edgeai/task-details/${task.id}`)
}

const retryTask = async (task) => {
  const monitor = performanceMonitor.startTimer('EdgeAITaskRetry')
  
  try {
    const result = await edgeaiService.tasks.retryTask(task.id)
    
    if (result && result.success) {
      // Update local task state
      task.status = 'queued'
      task.progress = 0
      
      console.log('重试任务:', task.name)
      monitor.end({ success: true, taskId: task.id })
    } else {
      throw new Error(result?.error || 'Failed to retry task')
    }
  } catch (error) {
    console.error('Failed to retry task:', error)
    showError(`Failed to retry task "${task.name}": ${error.message}`)
    monitor.end({ success: false, error: error.message })
  }
}

// Add task lifecycle management functions
const startTask = async (task) => {
  if (task.status === 'running') {
    return
  }

  const monitor = performanceMonitor.startTimer('EdgeAITaskStart')
  
  try {
    const result = await edgeaiService.tasks.startTask(task.id)
    
    if (result && result.success) {
      task.status = 'running'
      console.log('Started task:', task.name)
      monitor.end({ success: true, taskId: task.id })
    } else {
      throw new Error(result?.error || 'Failed to start task')
    }
  } catch (error) {
    console.error('Failed to start task:', error)
    showError(`Failed to start task "${task.name}": ${error.message}`)
    monitor.end({ success: false, error: error.message })
  }
}

const stopTask = async (task) => {
  if (task.status !== 'running') {
    return
  }

  const monitor = performanceMonitor.startTimer('EdgeAITaskStop')
  
  try {
    const result = await edgeaiService.tasks.stopTask(task.id)
    
    if (result && result.success) {
      task.status = 'paused'
      console.log('Stopped task:', task.name)
      monitor.end({ success: true, taskId: task.id })
    } else {
      throw new Error(result?.error || 'Failed to stop task')
    }
  } catch (error) {
    console.error('Failed to stop task:', error)
    showError(`Failed to stop task "${task.name}": ${error.message}`)
    monitor.end({ success: false, error: error.message })
  }
}

const deleteTask = async (task) => {
  if (!confirm(`Are you sure you want to delete task "${task.name}"? This action cannot be undone.`)) {
    return
  }

  const monitor = performanceMonitor.startTimer('EdgeAITaskDelete')
  
  try {
    const result = await edgeaiService.tasks.deleteTask(task.id)
    
    if (result && result.success) {
      // Remove task from local state
      const index = tasks.value.findIndex(t => t.id === task.id)
      if (index !== -1) {
        tasks.value.splice(index, 1)
      }
      
      console.log('Deleted task:', task.name)
      monitor.end({ success: true, taskId: task.id })
    } else {
      throw new Error(result?.error || 'Failed to delete task')
    }
  } catch (error) {
    console.error('Failed to delete task:', error)
    showError(`Failed to delete task "${task.name}": ${error.message}`)
    monitor.end({ success: false, error: error.message })
  }
}

// Component lifecycle
onMounted(async () => {
  await loadTasksData()
  setupAutoRefresh()
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  clearCache()
})
</script>