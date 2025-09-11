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
      <!-- Task Statistics -->
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import {
  CpuChipIcon,
  PlayIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  PlusIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()

const tasks = ref([
  {
    id: 1,
    name: '图像分类训练',
    type: '深度学习',
    status: 'running',
    node: 'edge-node-01',
    progress: 65,
    createdAt: '2024-01-10 09:30'
  },
  {
    id: 2,
    name: '数据预处理',
    type: '数据处理',
    status: 'queued',
    node: '-',
    progress: 0,
    createdAt: '2024-01-10 10:15'
  },
  {
    id: 3,
    name: '模型推理',
    type: '推理',
    status: 'completed',
    node: 'edge-node-02',
    progress: 100,
    createdAt: '2024-01-10 08:45'
  },
  {
    id: 4,
    name: '联邦学习聚合',
    type: '联邦学习',
    status: 'failed',
    node: 'edge-node-03',
    progress: 25,
    createdAt: '2024-01-10 07:20'
  }
])

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
}

const retryTask = (task) => {
  console.log('重试任务:', task.name)
  task.status = 'queued'
  task.progress = 0
}
</script>