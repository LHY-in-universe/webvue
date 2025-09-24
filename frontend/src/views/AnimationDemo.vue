<template>
  <div class="animation-demo-page">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-center mb-8 text-gray-800 dark:text-white">
        网络数据传输动画演示
      </h1>
      
      <!-- 控制面板 -->
      <div class="control-panel bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">动画控制</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="flex items-center space-x-2">
            <input
              id="enableAnimations"
              v-model="enableAnimations"
              type="checkbox"
              class="rounded"
            />
            <label for="enableAnimations" class="text-gray-700 dark:text-gray-300">
              启用动画效果
            </label>
          </div>
          
          <div class="flex items-center space-x-2">
            <label class="text-gray-700 dark:text-gray-300">动画速度:</label>
            <input
              v-model="animationSpeed"
              type="range"
              min="0.5"
              max="3.0"
              step="0.1"
              class="flex-1"
            />
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ animationSpeed }}x</span>
          </div>
          
          <div class="flex items-center space-x-2">
            <label class="text-gray-700 dark:text-gray-300">粒子数量:</label>
            <input
              v-model="particleCount"
              type="range"
              min="1"
              max="5"
              step="1"
              class="flex-1"
            />
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ particleCount }}</span>
          </div>
        </div>
      </div>
      
      <!-- 网络可视化演示 -->
      <div class="demo-section">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
          联邦学习网络拓扑
        </h2>
        <div class="network-demo-container bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-8">
          <FederatedNetworkVisualization
            :nodes="demoNodes"
            :connections="demoConnections"
            :node-animation-states="nodeAnimationStates"
            @node-click="handleNodeClick"
          />
        </div>
      </div>
      
      <!-- P2P网络演示 -->
      <div class="demo-section">
        <h2 class="text-2xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
          P2P网络拓扑
        </h2>
        <div class="network-demo-container bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-8">
          <NetworkVisualization
            :nodes="p2pNodes"
            :connections="p2pConnections"
            :training-active="enableAnimations"
            @node-click="handleNodeClick"
          />
        </div>
      </div>
      
      <!-- 动画效果说明 -->
      <div class="effects-description bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">动画效果说明</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="effect-item">
            <h3 class="text-lg font-medium text-blue-600 dark:text-blue-400 mb-2">
              🌊 波浪传输效果
            </h3>
            <p class="text-gray-600 dark:text-gray-400">
              连接线上显示波浪状的传输动画，模拟数据包的流动
            </p>
          </div>
          
          <div class="effect-item">
            <h3 class="text-lg font-medium text-green-600 dark:text-green-400 mb-2">
              ✨ 脉冲光晕效果
            </h3>
            <p class="text-gray-600 dark:text-gray-400">
              连接线和节点周围的光晕脉冲，增强视觉冲击力
            </p>
          </div>
          
          <div class="effect-item">
            <h3 class="text-lg font-medium text-purple-600 dark:text-purple-400 mb-2">
              🔮 数据粒子效果
            </h3>
            <p class="text-gray-600 dark:text-gray-400">
              在连接线上移动的粒子，模拟数据传输过程
            </p>
          </div>
          
          <div class="effect-item">
            <h3 class="text-lg font-medium text-orange-600 dark:text-orange-400 mb-2">
              💫 发光滤镜效果
            </h3>
            <p class="text-gray-600 dark:text-gray-400">
              使用SVG滤镜创建发光和阴影效果，提升视觉质量
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import FederatedNetworkVisualization from '@/components/edgeai/FederatedNetworkVisualization.vue'
import NetworkVisualization from '@/components/p2pai/NetworkVisualization.vue'

// 响应式数据
const enableAnimations = ref(true)
const animationSpeed = ref(1.0)
const particleCount = ref(3)

// 节点动画状态
const nodeAnimationStates = ref(new Map())

// 联邦学习演示数据
const demoNodes = ref([
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

const demoConnections = ref([
  {
    from: 'control-1',
    to: 'model-1',
    type: 'control',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 1000
  },
  {
    from: 'control-1',
    to: 'model-2',
    type: 'control',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 1000
  },
  {
    from: 'model-1',
    to: 'training-1',
    type: 'data',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 500
  },
  {
    from: 'model-2',
    to: 'training-2',
    type: 'data',
    direction: 'downstream',
    transmitting: true,
    bandwidth: 500
  },
  {
    from: 'training-1',
    to: 'model-1',
    type: 'data',
    direction: 'upstream',
    transmitting: true,
    bandwidth: 300
  },
  {
    from: 'training-2',
    to: 'model-2',
    type: 'data',
    direction: 'upstream',
    transmitting: true,
    bandwidth: 300
  },
  {
    from: 'training-3',
    to: 'model-1',
    type: 'data',
    direction: 'bidirectional',
    transmitting: true,
    bandwidth: 400
  }
])

// P2P网络演示数据
const p2pNodes = ref([
  {
    id: 'server-1',
    name: 'Server',
    type: 'control',
    x: 600,
    y: 100,
    status: 'online'
  },
  {
    id: 'device-1',
    name: 'Your Device',
    type: 'edge',
    isOwn: true,
    x: 600,
    y: 350,
    status: 'online'
  },
  {
    id: 'device-2',
    name: 'Device-2',
    type: 'edge',
    x: 400,
    y: 200,
    status: 'online'
  },
  {
    id: 'device-3',
    name: 'Device-3',
    type: 'edge',
    x: 800,
    y: 200,
    status: 'online'
  },
  {
    id: 'device-4',
    name: 'Device-4',
    type: 'edge',
    x: 400,
    y: 500,
    status: 'online'
  },
  {
    id: 'device-5',
    name: 'Device-5',
    type: 'edge',
    x: 800,
    y: 500,
    status: 'online'
  }
])

const p2pConnections = ref([
  {
    from: 'server-1',
    to: 'device-1',
    direction: 'downstream',
    active: true
  },
  {
    from: 'server-1',
    to: 'device-2',
    direction: 'downstream',
    active: true
  },
  {
    from: 'server-1',
    to: 'device-3',
    direction: 'downstream',
    active: true
  },
  {
    from: 'device-1',
    to: 'device-2',
    direction: 'bidirectional',
    active: true
  },
  {
    from: 'device-1',
    to: 'device-3',
    direction: 'bidirectional',
    active: true
  },
  {
    from: 'device-2',
    to: 'device-4',
    direction: 'bidirectional',
    active: true
  },
  {
    from: 'device-3',
    to: 'device-5',
    direction: 'bidirectional',
    active: true
  }
])

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

// 生命周期
onMounted(() => {
  console.log('动画演示页面已加载')
})
</script>

<style scoped>
.animation-demo-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.network-demo-container {
  height: 500px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.control-panel {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.9);
}

.effects-description {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.9);
}

.effect-item {
  padding: 1rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .network-demo-container {
    height: 400px;
  }
  
  .grid {
    grid-template-columns: 1fr;
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .animation-demo-page {
    background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
  }
  
  .control-panel,
  .effects-description {
    background: rgba(31, 41, 55, 0.9);
  }
  
  .effect-item {
    background: rgba(31, 41, 55, 0.5);
    border-color: rgba(255, 255, 255, 0.1);
  }
}
</style>
