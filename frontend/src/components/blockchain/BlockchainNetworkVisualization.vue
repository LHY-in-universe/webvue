<template>
  <BaseNetworkVisualization
    :nodes="nodes"
    :connections="connections"
    :theme="theme"
    :enable-zoom="true"
    :enable-pan="true"
    :enable-mini-map="true"
    :auto-layout="false"
    layout-type="hierarchical"
    @node-click="handleNodeClick"
    @node-hover="handleNodeHover"
    @viewport-change="$emit('viewport-change', $event)"
  >
    <!-- Node Rendering -->
    <template #nodes="{ nodes: visibleNodes, theme }">
      <g v-for="node in visibleNodes" :key="node.id" class="blockchain-node">
        <!-- Node Background Circle -->
        <circle
          :cx="node.x"
          :cy="node.y"
          :r="getNodeRadius(node)"
          :fill="getNodeColor(node)"
          :stroke="getNodeBorderColor(node)"
          :stroke-width="getStrokeWidth(node)"
          :class="getNodeClasses(node)"
          @click="handleNodeClick(node)"
          @mouseover="handleNodeHover(node, $event)"
          @mouseleave="handleNodeLeave(node)"
        />
        
        <!-- Validator Ring (for validator nodes) -->
        <circle
          v-if="node.type === 'validator'"
          :cx="node.x"
          :cy="node.y"
          :r="getNodeRadius(node) + 8"
          fill="none"
          :stroke="theme.warning"
          stroke-width="2"
          stroke-dasharray="5,5"
          :class="{ 'animate-spin-slow': node.status === 'validating' }"
        />
        
        <!-- Consensus Indicator -->
        <g v-if="node.type === 'validator' && node.isLeader">
          <circle
            :cx="node.x - 15"
            :cy="node.y - 15"
            r="6"
            :fill="theme.warning"
            class="animate-pulse"
          />
          <text
            :x="node.x - 15"
            :y="node.y - 11"
            text-anchor="middle"
            fill="white"
            font-size="8"
            font-weight="bold"
          >L</text>
        </g>
        
        <!-- Block Height Indicator -->
        <rect
          v-if="node.blockHeight"
          :x="node.x - 20"
          :y="node.y + getNodeRadius(node) + 5"
          width="40"
          height="16"
          rx="8"
          :fill="themeStore.isDark ? 'rgba(0,0,0,0.8)' : 'rgba(255,255,255,0.9)'"
          stroke="none"
        />
        <text
          v-if="node.blockHeight"
          :x="node.x"
          :y="node.y + getNodeRadius(node) + 16"
          text-anchor="middle"
          :fill="themeStore.isDark ? '#ffffff' : '#000000'"
          font-size="10"
          font-weight="500"
        >{{ formatBlockHeight(node.blockHeight) }}</text>
        
        <!-- Node Icon -->
        <g :transform="`translate(${node.x - 12}, ${node.y - 12})`">
          <component 
            :is="getNodeIcon(node)" 
            class="w-6 h-6"
            :class="getIconColor(node)"
          />
        </g>
        
        <!-- Node Label -->
        <text
          :x="node.x"
          :y="node.y - getNodeRadius(node) - 10"
          text-anchor="middle"
          :fill="themeStore.isDark ? '#ffffff' : '#000000'"
          font-size="12"
          font-weight="500"
        >{{ node.name || node.id }}</text>
        
        <!-- Status Indicator -->
        <circle
          :cx="node.x + getNodeRadius(node) - 5"
          :cy="node.y - getNodeRadius(node) + 5"
          r="4"
          :fill="getStatusColor(node.status)"
          stroke="white"
          stroke-width="1"
        />
        
        <!-- Transaction Pool Indicator -->
        <g v-if="node.transactionPool && node.transactionPool > 0">
          <circle
            :cx="node.x + 20"
            :cy="node.y"
            r="8"
            :fill="getPoolColor(node.transactionPool)"
            opacity="0.8"
          />
          <text
            :x="node.x + 20"
            :y="node.y + 3"
            text-anchor="middle"
            fill="white"
            font-size="8"
            font-weight="bold"
          >{{ formatPoolSize(node.transactionPool) }}</text>
        </g>
      </g>
    </template>
    
    <!-- Connection Rendering -->
    <template #connections="{ connections: visibleConnections, theme }">
      <g v-for="connection in visibleConnections" :key="`${connection.from}-${connection.to}`" class="blockchain-connection">
        <!-- Connection Line -->
        <line
          :x1="getNodePosition(connection.from).x"
          :y1="getNodePosition(connection.from).y"
          :x2="getNodePosition(connection.to).x"
          :y2="getNodePosition(connection.to).y"
          :stroke="getConnectionColor(connection)"
          :stroke-width="getConnectionWidth(connection)"
          :stroke-dasharray="getConnectionDashArray(connection)"
          opacity="0.6"
          :class="getConnectionClasses(connection)"
        />
        
        <!-- Data Flow Animation -->
        <circle
          v-if="connection.hasDataFlow"
          :r="3"
          :fill="theme.primary"
          opacity="0.8"
        >
          <animateMotion
            :dur="getAnimationDuration(connection)"
            repeatCount="indefinite"
          >
            <mpath :href="`#connection-${connection.from}-${connection.to}`" />
          </animateMotion>
        </circle>
        
        <!-- Connection Label -->
        <text
          v-if="connection.label"
          :x="(getNodePosition(connection.from).x + getNodePosition(connection.to).x) / 2"
          :y="(getNodePosition(connection.from).y + getNodePosition(connection.to).y) / 2 - 5"
          text-anchor="middle"
          :fill="themeStore.isDark ? '#ffffff' : '#000000'"
          font-size="10"
          opacity="0.7"
        >{{ connection.label }}</text>
      </g>
    </template>
    
    <!-- Mini Map -->
    <template #mini-map="{ scale, nodes }">
      <g v-for="node in nodes" :key="`mini-${node.id}`">
        <circle
          :cx="node.x * scale"
          :cy="node.y * scale"
          :r="Math.max(2, getNodeRadius(node) * scale)"
          :fill="getNodeColor(node)"
          opacity="0.8"
        />
      </g>
    </template>
    
    <!-- Info Panel -->
    <template #info-panel="{ node, close }">
      <div class="blockchain-node-info">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ node.name || node.id }}
          </h3>
          <Button @click="close" variant="ghost" size="sm">
            <XMarkIcon class="w-4 h-4" />
          </Button>
        </div>
        
        <div class="space-y-3">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Type</p>
              <p class="font-medium capitalize">{{ node.type }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Status</p>
              <div class="flex items-center space-x-2">
                <div class="w-2 h-2 rounded-full" :class="getStatusColor(node.status)"></div>
                <p class="font-medium capitalize">{{ node.status }}</p>
              </div>
            </div>
          </div>
          
          <div v-if="node.blockHeight">
            <p class="text-xs text-gray-500 dark:text-gray-400">Block Height</p>
            <p class="font-medium">{{ node.blockHeight.toLocaleString() }}</p>
          </div>
          
          <div v-if="node.transactionPool">
            <p class="text-xs text-gray-500 dark:text-gray-400">Transaction Pool</p>
            <p class="font-medium">{{ node.transactionPool.toLocaleString() }} pending</p>
          </div>
          
          <div v-if="node.type === 'validator'">
            <p class="text-xs text-gray-500 dark:text-gray-400">Validation Power</p>
            <div class="mt-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                class="bg-yellow-500 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${(node.validationPower || 0)}%` }"
              ></div>
            </div>
            <p class="text-xs text-gray-600 dark:text-gray-300 mt-1">
              {{ node.validationPower || 0 }}%
            </p>
          </div>
          
          <div v-if="node.lastBlockTime">
            <p class="text-xs text-gray-500 dark:text-gray-400">Last Block</p>
            <p class="font-medium">{{ formatTime(node.lastBlockTime) }}</p>
          </div>
        </div>
      </div>
    </template>
  </BaseNetworkVisualization>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useThemeStore } from '@/stores/theme'
import BaseNetworkVisualization from '@/components/common/BaseNetworkVisualization.vue'
import Button from '@/components/ui/Button.vue'
import { 
  CubeIcon, 
  ServerIcon, 
  ShieldCheckIcon, 
  UserIcon, 
  XMarkIcon 
} from '@heroicons/vue/24/outline'

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  connections: {
    type: Array,
    default: () => []
  },
  theme: {
    type: Object,
    default: () => ({
      primary: '#3b82f6',
      secondary: '#10b981',
      warning: '#f59e0b',
      danger: '#ef4444',
      success: '#22c55e'
    })
  }
})

const emit = defineEmits(['node-click', 'node-hover', 'node-leave', 'viewport-change'])

const themeStore = useThemeStore()

// Node styling functions
const getNodeRadius = (node) => {
  const baseRadius = 20
  const typeMultipliers = {
    validator: 1.3,
    full: 1.1,
    light: 0.9,
    miner: 1.2
  }
  return baseRadius * (typeMultipliers[node.type] || 1)
}

const getNodeColor = (node) => {
  const colors = {
    validator: props.theme.warning,
    full: props.theme.primary,
    light: props.theme.secondary,
    miner: props.theme.danger
  }
  return colors[node.type] || props.theme.primary
}

const getNodeBorderColor = (node) => {
  if (node.isSelected) return props.theme.warning
  if (node.isLeader) return '#ffd700'
  return themeStore.isDark ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.2)'
}

const getStrokeWidth = (node) => {
  if (node.isSelected) return 3
  if (node.isLeader) return 2
  return 1
}

const getNodeClasses = (node) => {
  const classes = ['blockchain-node-circle', 'transition-all', 'duration-300', 'cursor-pointer']
  if (node.status === 'syncing') classes.push('animate-pulse')
  if (node.isHovered) classes.push('shadow-lg', 'transform', 'scale-110')
  return classes.join(' ')
}

const getNodeIcon = (node) => {
  const icons = {
    validator: ShieldCheckIcon,
    full: ServerIcon,
    light: UserIcon,
    miner: CubeIcon
  }
  return icons[node.type] || ServerIcon
}

const getIconColor = (node) => {
  return 'text-white drop-shadow-sm'
}

const getStatusColor = (status) => {
  const colors = {
    online: 'bg-green-500',
    offline: 'bg-red-500',
    syncing: 'bg-yellow-500',
    validating: 'bg-blue-500',
    error: 'bg-red-600'
  }
  return colors[status] || 'bg-gray-400'
}

const getPoolColor = (poolSize) => {
  if (poolSize > 1000) return '#ef4444'
  if (poolSize > 500) return '#f59e0b'
  if (poolSize > 100) return '#eab308'
  return '#22c55e'
}

// Connection styling functions
const getConnectionColor = (connection) => {
  const typeColors = {
    consensus: props.theme.warning,
    sync: props.theme.primary,
    transaction: props.theme.secondary,
    gossip: props.theme.accent || '#8b5cf6'
  }
  return typeColors[connection.type] || props.theme.primary
}

const getConnectionWidth = (connection) => {
  const widths = {
    consensus: 3,
    sync: 2,
    transaction: 1.5,
    gossip: 1
  }
  return widths[connection.type] || 1
}

const getConnectionDashArray = (connection) => {
  if (connection.type === 'gossip') return '2,2'
  if (connection.status === 'unstable') return '5,5'
  return 'none'
}

const getConnectionClasses = (connection) => {
  const classes = ['blockchain-connection-line']
  if (connection.hasDataFlow) classes.push('animate-pulse')
  return classes.join(' ')
}

const getAnimationDuration = (connection) => {
  const speeds = {
    consensus: '2s',
    sync: '3s',
    transaction: '1s',
    gossip: '4s'
  }
  return speeds[connection.type] || '2s'
}

// Helper functions
const getNodePosition = (nodeId) => {
  const node = props.nodes.find(n => n.id === nodeId)
  return node ? { x: node.x, y: node.y } : { x: 0, y: 0 }
}

const formatBlockHeight = (height) => {
  if (height > 1000000) return `${(height / 1000000).toFixed(1)}M`
  if (height > 1000) return `${(height / 1000).toFixed(1)}K`
  return height.toString()
}

const formatPoolSize = (size) => {
  if (size > 1000) return `${Math.floor(size / 1000)}K`
  return size.toString()
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString()
}

// Event handlers
const handleNodeClick = (node) => {
  emit('node-click', node)
}

const handleNodeHover = (node, event) => {
  emit('node-hover', node, event)
}

const handleNodeLeave = (node) => {
  emit('node-leave', node)
}
</script>

<style scoped>
.blockchain-node-circle {
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.blockchain-node-circle:hover {
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.2));
}

.animate-spin-slow {
  animation: spin 3s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.blockchain-connection-line {
  transition: stroke-width 0.2s ease, opacity 0.2s ease;
}

.blockchain-connection-line:hover {
  stroke-width: 4px !important;
  opacity: 0.8 !important;
}
</style>