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
          
          <div class="h-64 flex items-center justify-center border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
            <div class="text-center">
              <ChartBarIcon class="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p class="text-gray-500 dark:text-gray-400">性能图表占位符</p>
              <p class="text-sm text-gray-400">实际部署中将显示实时性能图表</p>
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
import { ref } from 'vue'
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

const avgResponseTime = ref(245)
const cpuUsage = ref(68)
const memoryUsage = ref(54)
const storageUsage = ref(72)
const networkUsage = ref(35)
const networkThroughput = ref(125.3)

const nodePerformance = ref([
  {
    id: 1,
    name: 'edge-node-01',
    status: 'online',
    cpu: 65,
    memory: 48,
    load: 1.2
  },
  {
    id: 2,
    name: 'edge-node-02',
    status: 'online',
    cpu: 72,
    memory: 61,
    load: 1.8
  },
  {
    id: 3,
    name: 'edge-node-03',
    status: 'warning',
    cpu: 89,
    memory: 84,
    load: 2.3
  },
  {
    id: 4,
    name: 'edge-node-04',
    status: 'offline',
    cpu: 0,
    memory: 0,
    load: 0
  }
])

const performanceAlerts = ref([
  {
    id: 1,
    level: 'warning',
    message: 'CPU 使用率过高',
    node: 'edge-node-03',
    time: '5 分钟前'
  },
  {
    id: 2,
    level: 'info',
    message: '内存使用率正常',
    node: '系统整体',
    time: '10 分钟前'
  },
  {
    id: 3,
    level: 'error',
    message: '节点连接丢失',
    node: 'edge-node-04',
    time: '15 分钟前'
  }
])

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