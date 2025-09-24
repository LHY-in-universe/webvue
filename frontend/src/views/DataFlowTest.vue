<template>
  <div class="data-flow-test-page">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-center mb-8 text-gray-800 dark:text-white">
        数据传输动画测试
      </h1>
      
      <!-- 控制按钮 -->
      <div class="flex justify-center space-x-4 mb-8">
        <button 
          @click="startAnimations"
          class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          启动动画
        </button>
        <button 
          @click="stopAnimations"
          class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          停止动画
        </button>
        <button 
          @click="toggleAnimations"
          class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          {{ animationsEnabled ? '禁用' : '启用' }}动画
        </button>
      </div>
      
      <!-- 网络可视化测试 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
          联邦学习网络拓扑测试
        </h2>
        <div class="network-test-container bg-gray-50 dark:bg-gray-900 rounded-lg p-4" style="height: 500px;">
          <FederatedNetworkVisualization
            :nodes="testNodes"
            :connections="testConnections"
            :node-animation-states="nodeAnimationStates"
            @node-click="handleNodeClick"
          />
        </div>
      </div>
      
      <!-- 状态信息 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
          动画状态信息
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="status-item">
            <span class="font-medium">动画状态:</span>
            <span :class="animationsEnabled ? 'text-green-600' : 'text-red-600'">
              {{ animationsEnabled ? '已启用' : '已禁用' }}
            </span>
          </div>
          <div class="status-item">
            <span class="font-medium">连接数量:</span>
            <span class="text-blue-600">{{ testConnections.length }}</span>
          </div>
          <div class="status-item">
            <span class="font-medium">活跃连接:</span>
            <span class="text-green-600">{{ activeConnections }}</span>
          </div>
        </div>
        
        <div class="mt-4">
          <h3 class="font-medium mb-2">连接详情:</h3>
          <div class="space-y-2">
            <div 
              v-for="connection in testConnections" 
              :key="connection.id"
              class="flex items-center justify-between p-2 bg-gray-100 dark:bg-gray-700 rounded"
            >
              <span>{{ connection.from }} → {{ connection.to }}</span>
              <div class="flex items-center space-x-2">
                <span 
                  :class="connection.transmitting ? 'text-green-600' : 'text-gray-500'"
                  class="text-sm"
                >
                  {{ connection.transmitting ? '传输中' : '空闲' }}
                </span>
                <span class="text-sm text-gray-500">{{ connection.direction }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import FederatedNetworkVisualization from '@/components/edgeai/FederatedNetworkVisualization.vue'

// 响应式数据
const animationsEnabled = ref(true)
const nodeAnimationStates = ref(new Map())

// 测试节点数据
const testNodes = ref([
  {
    id: 'model-1',
    name: 'Model-1',
    ip: '192.168.1.10',
    type: 'model',
    role: 'MPC Model Node',
    x: 300,
    y: 200,
    status: 'online'
  },
  {
    id: 'model-2', 
    name: 'Model-2',
    ip: '192.168.1.11',
    type: 'model',
    role: 'MPC Model Node',
    x: 500,
    y: 200,
    status: 'online'
  },
  {
    id: 'control-1',
    name: 'Control-1',
    ip: '192.168.1.20',
    type: 'control',
    role: 'Model Manager Node',
    x: 400,
    y: 100,
    status: 'online'
  },
  {
    id: 'training-1',
    name: 'Training-1',
    ip: '192.168.1.30',
    type: 'training',
    role: 'Edge AI Training Node',
    x: 200,
    y: 350,
    status: 'training',
    trainingProgress: 75
  },
  {
    id: 'training-2',
    name: 'Training-2',
    ip: '192.168.1.31',
    type: 'training',
    role: 'Edge AI Training Node',
    x: 400,
    y: 350,
    status: 'training',
    trainingProgress: 60
  },
  {
    id: 'training-3',
    name: 'Training-3',
    ip: '192.168.1.32',
    type: 'training',
    role: 'Edge AI Training Node',
    x: 600,
    y: 350,
    status: 'training',
    trainingProgress: 85
  }
])

// 测试连接数据
const testConnections = ref([
  {
    id: 'control-model-1',
    from: 'control-1',
    to: 'model-1',
    type: 'control',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 1000
  },
  {
    id: 'control-model-2',
    from: 'control-1',
    to: 'model-2',
    type: 'control',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 1000
  },
  {
    id: 'model-training-1',
    from: 'model-1',
    to: 'training-1',
    type: 'data',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 500
  },
  {
    id: 'model-training-2',
    from: 'model-2',
    to: 'training-2',
    type: 'data',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 500
  },
  {
    id: 'training-model-1',
    from: 'training-1',
    to: 'model-1',
    type: 'data',
    direction: 'upstream',
    transmitting: true,
    bandwidth: 300
  },
  {
    id: 'training-model-2',
    from: 'training-2',
    to: 'model-2',
    type: 'data',
    direction: 'upstream',
    transmitting: true,
    bandwidth: 300
  },
  {
    id: 'training-model-3',
    from: 'training-3',
    to: 'model-1',
    type: 'data',
    direction: 'bidirectional',
    transmitting: true,
    bandwidth: 400
  }
])

// 计算属性
const activeConnections = computed(() => {
  return testConnections.value.filter(c => c.transmitting).length
})

// 事件处理
const handleNodeClick = (node) => {
  console.log('节点被点击:', node)
  
  // 添加点击动画效果
  if (nodeAnimationStates.value.has(node.id)) {
    const currentState = nodeAnimationStates.value.get(node.id)
    currentState.fading = true
    currentState.fadeStartTime = Date.now()
  } else {
    nodeAnimationStates.value.set(node.id, {
      fading: true,
      fadeStartTime: Date.now()
    })
  }
  
  // 3秒后重置动画状态
  setTimeout(() => {
    nodeAnimationStates.value.delete(node.id)
  }, 3000)
}

// 动画控制函数
const startAnimations = () => {
  testConnections.value.forEach(connection => {
    connection.transmitting = true
  })
  console.log('数据传输动画已启动')
}

const stopAnimations = () => {
  testConnections.value.forEach(connection => {
    connection.transmitting = false
  })
  console.log('数据传输动画已停止')
}

const toggleAnimations = () => {
  animationsEnabled.value = !animationsEnabled.value
  if (animationsEnabled.value) {
    startAnimations()
  } else {
    stopAnimations()
  }
}
</script>

<style scoped>
.data-flow-test-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.network-test-container {
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .network-test-container {
    height: 400px;
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .data-flow-test-page {
    background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
  }
}
</style>
