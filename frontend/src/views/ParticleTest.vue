<template>
  <div class="particle-test-page min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        数据粒子传输效果测试
      </h1>
      
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4">测试说明</h2>
        <div class="space-y-2 text-gray-600 dark:text-gray-400">
          <p>• 完全连接网络 - 每个节点都与所有其他节点传输数据</p>
          <p>• 每条连接使用单条弧线路径，粒子沿弧线双向流动</p>
          <p>• 正向粒子：绿色/蓝色，反向粒子：红色/橙色，双向：紫色</p>
          <p>• 粒子大小、透明度和发光效果根据传输方向动态调整</p>
          <p>• 没有任何静态连接线，只有动态粒子沿弧线传输</p>
          <p>• 4个节点 = 6条连接，每个节点都与3个其他节点连接</p>
        </div>
      </div>
      
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg h-[600px]">
        <div class="h-full relative">
          <FederatedNetworkVisualization
            :nodes="testNodes"
            :connections="testConnections"
            :node-animation-states="new Map()"
            @node-click="() => {}"
            @connection-click="() => {}"
          />
        </div>
      </div>
      
      <div class="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h3 class="text-lg font-semibold mb-4">连接信息</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="connection in testConnections" :key="connection.id" 
               class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <h4 class="font-medium text-gray-900 dark:text-white">{{ connection.from }} → {{ connection.to }}</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              方向: {{ connection.direction }} | 类型: {{ connection.type }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FederatedNetworkVisualization from '@/components/edgeai/FederatedNetworkVisualization.vue'

// 测试节点数据
const testNodes = ref([
  {
    id: 'node-1',
    name: '节点 1',
    type: 'model',
    status: 'online',
    role: 'Model Server',
    ipAddress: '192.168.1.1',
    resources: { cpu: 45, memory: '2.1', gpu: 78 },
    lastHeartbeat: '1 sec ago',
    priority: 1
  },
  {
    id: 'node-2', 
    name: '节点 2',
    type: 'training',
    status: 'training',
    role: 'Training Client',
    ipAddress: '192.168.1.2',
    resources: { cpu: 67, memory: '3.2', gpu: 89 },
    lastHeartbeat: '2 sec ago',
    priority: 1
  },
  {
    id: 'node-3',
    name: '节点 3', 
    type: 'training',
    status: 'training',
    role: 'Training Client',
    ipAddress: '192.168.1.3',
    resources: { cpu: 52, memory: '2.8', gpu: 76 },
    lastHeartbeat: '1 sec ago',
    priority: 1
  },
  {
    id: 'node-4',
    name: '节点 4',
    type: 'training', 
    status: 'training',
    role: 'Training Client',
    ipAddress: '192.168.1.4',
    resources: { cpu: 73, memory: '4.1', gpu: 82 },
    lastHeartbeat: '3 sec ago',
    priority: 1
  }
])

// 测试连接数据 - 完全连接网络（每个节点都与所有其他节点连接）
const testConnections = ref([
  // 节点1与所有其他节点的连接
  {
    id: 'conn-1-2',
    from: 'node-1',
    to: 'node-2',
    type: 'data',
    active: true,
    transmitting: true,
    direction: 'bidirectional',
    lastTransmission: Date.now(),
    bandwidth: 85
  },
  {
    id: 'conn-1-3',
    from: 'node-1', 
    to: 'node-3',
    type: 'data',
    active: true,
    transmitting: true,
    direction: 'downstream',
    lastTransmission: Date.now(),
    bandwidth: 92
  },
  {
    id: 'conn-1-4',
    from: 'node-1',
    to: 'node-4', 
    type: 'data',
    active: true,
    transmitting: true,
    direction: 'upstream',
    lastTransmission: Date.now(),
    bandwidth: 78
  },
  // 节点2与剩余节点的连接
  {
    id: 'conn-2-3',
    from: 'node-2',
    to: 'node-3',
    type: 'data',
    active: true,
    transmitting: true,
    direction: 'bidirectional',
    lastTransmission: Date.now(),
    bandwidth: 67
  },
  {
    id: 'conn-2-4',
    from: 'node-2',
    to: 'node-4',
    type: 'data', 
    active: true,
    transmitting: true,
    direction: 'downstream',
    lastTransmission: Date.now(),
    bandwidth: 73
  },
  // 节点3与节点4的连接
  {
    id: 'conn-3-4',
    from: 'node-3',
    to: 'node-4',
    type: 'data',
    active: true,
    transmitting: true,
    direction: 'upstream',
    lastTransmission: Date.now(),
    bandwidth: 89
  }
])
</script>

<style scoped>
/* 确保粒子效果可见 - 小粒子版本 */
:deep(.data-particle) {
  filter: drop-shadow(0 0 4px currentColor) !important;
}

:deep(.enhanced-data-flow) {
  pointer-events: none !important;
}
</style>
