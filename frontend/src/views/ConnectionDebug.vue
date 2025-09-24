<template>
  <div class="connection-debug-page">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-center mb-8 text-gray-800 dark:text-white">
        连接数据调试页面
      </h1>
      
      <!-- 调试信息 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
          调试信息
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <span class="font-medium">节点数量:</span>
            <span class="text-blue-600">{{ nodes.length }}</span>
          </div>
          <div>
            <span class="font-medium">连接数量:</span>
            <span class="text-green-600">{{ connections.length }}</span>
          </div>
          <div>
            <span class="font-medium">传输中连接:</span>
            <span class="text-orange-600">{{ transmittingConnections }}</span>
          </div>
          <div>
            <span class="font-medium">活跃连接:</span>
            <span class="text-purple-600">{{ activeConnections }}</span>
          </div>
        </div>
      </div>
      
      <!-- 节点列表 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
          节点列表
        </h2>
        <div class="space-y-2">
          <div 
            v-for="node in nodes" 
            :key="node.id"
            class="flex items-center justify-between p-3 bg-gray-100 dark:bg-gray-700 rounded"
          >
            <div class="flex items-center space-x-3">
              <div 
                :class="getNodeColorClass(node.type)"
                class="w-4 h-4 rounded-full"
              ></div>
              <span class="font-medium">{{ node.name || node.id }}</span>
              <span class="text-sm text-gray-500">{{ node.ip }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <span class="text-sm">{{ node.type }}</span>
              <span 
                :class="getStatusColorClass(node.status)"
                class="px-2 py-1 rounded text-xs"
              >
                {{ node.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 连接列表 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
          连接列表
        </h2>
        <div class="space-y-2">
          <div 
            v-for="connection in connections" 
            :key="connection.id"
            class="flex items-center justify-between p-3 bg-gray-100 dark:bg-gray-700 rounded"
          >
            <div class="flex items-center space-x-3">
              <span class="font-medium">{{ connection.from }}</span>
              <span class="text-gray-500">→</span>
              <span class="font-medium">{{ connection.to }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <span 
                :class="connection.transmitting ? 'text-green-600' : 'text-gray-500'"
                class="text-sm"
              >
                {{ connection.transmitting ? '传输中' : '空闲' }}
              </span>
              <span class="text-sm text-gray-500">{{ connection.direction }}</span>
              <span class="text-sm text-gray-500">{{ connection.type }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 网络可视化 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
          纯数据粒子传输效果
        </h2>
        <div class="mb-4 text-sm text-gray-600 dark:text-gray-400">
          <p>✨ 现在只显示动态数据粒子，没有静态连接线</p>
          <p>🚀 粒子沿着曲线路径在节点之间移动</p>
          <p>💫 每个粒子都有发光效果和颜色变化</p>
        </div>
        <div class="network-debug-container bg-gray-50 dark:bg-gray-900 rounded-lg p-4" style="height: 500px;">
          <FederatedNetworkVisualization
            :nodes="nodes"
            :connections="connections"
            :node-animation-states="nodeAnimationStates"
            @node-click="handleNodeClick"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import FederatedNetworkVisualization from '@/components/edgeai/FederatedNetworkVisualization.vue'

// 响应式数据
const nodeAnimationStates = ref(new Map())

// 测试节点数据
const nodes = ref([
  {
    id: '175.178.24.56',
    name: 'Model-1',
    ip: '175.178.24.56',
    type: 'model',
    role: 'MPC Model Node',
    x: 200,
    y: 150,
    status: 'online'
  },
  {
    id: '43.135.30.207',
    name: 'Model-2',
    ip: '43.135.30.207',
    type: 'model',
    role: 'MPC Model Node',
    x: 400,
    y: 150,
    status: 'online'
  },
  {
    id: '106.52.36.202',
    name: 'Model-3',
    ip: '106.52.36.202',
    type: 'model',
    role: 'MPC Model Node',
    x: 600,
    y: 150,
    status: 'online'
  },
  {
    id: '10.0.4.31',
    name: 'Control-1',
    ip: '10.0.4.31',
    type: 'control',
    role: 'Model Manager Node',
    x: 400,
    y: 300,
    status: 'online'
  },
  {
    id: '42.194.177.24',
    name: 'Training-1',
    ip: '42.194.177.24',
    type: 'training',
    role: 'Edge AI Training Node',
    x: 200,
    y: 450,
    status: 'training',
    trainingProgress: 75
  },
  {
    id: '114.132.200.147',
    name: 'Training-2',
    ip: '114.132.200.147',
    type: 'training',
    role: 'Edge AI Training Node',
    x: 600,
    y: 450,
    status: 'training',
    trainingProgress: 60
  }
])

// 测试连接数据
const connections = ref([
  {
    id: 'control-model-1',
    from: '10.0.4.31',
    to: '175.178.24.56',
    type: 'control',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 1000
  },
  {
    id: 'control-model-2',
    from: '10.0.4.31',
    to: '43.135.30.207',
    type: 'control',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 1000
  },
  {
    id: 'control-model-3',
    from: '10.0.4.31',
    to: '106.52.36.202',
    type: 'control',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 1000
  },
  {
    id: 'model-training-1',
    from: '175.178.24.56',
    to: '42.194.177.24',
    type: 'data',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 500
  },
  {
    id: 'model-training-2',
    from: '43.135.30.207',
    to: '114.132.200.147',
    type: 'data',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 500
  },
  {
    id: 'training-model-1',
    from: '42.194.177.24',
    to: '175.178.24.56',
    type: 'data',
    direction: 'upstream',
    transmitting: true,
    bandwidth: 300
  },
  {
    id: 'training-model-2',
    from: '114.132.200.147',
    to: '43.135.30.207',
    type: 'data',
    direction: 'upstream',
    transmitting: true,
    bandwidth: 300
  }
])

// 计算属性
const transmittingConnections = computed(() => {
  return connections.value.filter(c => c.transmitting).length
})

const activeConnections = computed(() => {
  return connections.value.filter(c => c.active !== false).length
})

// 辅助函数
const getNodeColorClass = (type) => {
  const classes = {
    model: 'bg-blue-500',
    control: 'bg-green-500',
    training: 'bg-purple-500'
  }
  return classes[type] || 'bg-gray-500'
}

const getStatusColorClass = (status) => {
  const classes = {
    online: 'bg-green-100 text-green-800',
    training: 'bg-blue-100 text-blue-800',
    offline: 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

// 事件处理
const handleNodeClick = (node) => {
  console.log('节点被点击:', node)
}
</script>

<style scoped>
.connection-debug-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.network-debug-container {
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .network-debug-container {
    height: 400px;
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .connection-debug-page {
    background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
  }
}
</style>
