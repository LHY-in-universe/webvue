<template>
  <div class="transaction-flow-visualization">
    <svg 
      ref="flowSvg"
      class="transaction-flow-svg w-full h-full"
      :width="width"
      :height="height"
      :viewBox="`0 0 ${width} ${height}`"
    >
      <!-- Definitions -->
      <defs>
        <!-- Transaction Flow Gradients -->
        <linearGradient id="txFlowHigh" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :style="`stop-color:${theme.danger};stop-opacity:0`" />
          <stop offset="50%" :style="`stop-color:${theme.danger};stop-opacity:1`" />
          <stop offset="100%" :style="`stop-color:${theme.danger};stop-opacity:0`" />
        </linearGradient>
        
        <linearGradient id="txFlowMedium" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :style="`stop-color:${theme.warning};stop-opacity:0`" />
          <stop offset="50%" :style="`stop-color:${theme.warning};stop-opacity:1`" />
          <stop offset="100%" :style="`stop-color:${theme.warning};stop-opacity:0`" />
        </linearGradient>
        
        <linearGradient id="txFlowLow" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :style="`stop-color:${theme.success};stop-opacity:0`" />
          <stop offset="50%" :style="`stop-color:${theme.success};stop-opacity:1`" />
          <stop offset="100%" :style="`stop-color:${theme.success};stop-opacity:0`" />
        </linearGradient>
        
        <!-- Arrow Markers -->
        <marker id="txArrow" viewBox="0 0 10 10" refX="8" refY="3" markerWidth="6" markerHeight="6" orient="auto">
          <path d="M0,0 L0,6 L9,3 z" :fill="theme.primary" />
        </marker>
        
        <!-- Filters for glow effect -->
        <filter id="txGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
      
      <!-- Background -->
      <rect width="100%" height="100%" :fill="themeStore.isDark ? '#1f2937' : '#ffffff'" />
      
      <!-- Transaction Pools -->
      <g class="transaction-pools">
        <g v-for="pool in transactionPools" :key="pool.id" class="tx-pool">
          <!-- Pool Container -->
          <rect
            :x="pool.x - pool.width/2"
            :y="pool.y - pool.height/2"
            :width="pool.width"
            :height="pool.height"
            :fill="getPoolBackgroundColor(pool)"
            :stroke="getPoolBorderColor(pool)"
            stroke-width="2"
            rx="8"
            class="pool-container"
          />
          
          <!-- Pool Label -->
          <text
            :x="pool.x"
            :y="pool.y - pool.height/2 - 10"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#ffffff' : '#000000'"
            font-size="14"
            font-weight="600"
          >{{ pool.name }}</text>
          
          <!-- Pool Stats -->
          <text
            :x="pool.x"
            :y="pool.y + pool.height/2 + 20"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
            font-size="12"
          >{{ pool.pendingCount }} pending</text>
          
          <!-- Transaction Items -->
          <g v-for="(tx, index) in getPoolTransactions(pool)" :key="tx.id">
            <rect
              :x="pool.x - pool.width/2 + 10 + (index % 6) * 25"
              :y="pool.y - pool.height/2 + 15 + Math.floor(index / 6) * 15"
              width="20"
              height="10"
              :fill="getTransactionColor(tx)"
              rx="2"
              opacity="0.8"
              class="tx-item"
              @click="selectTransaction(tx)"
            >
              <animateOpacity 
                v-if="tx.status === 'pending'"
                values="0.8;0.4;0.8" 
                dur="2s" 
                repeatCount="indefinite"
              />
            </rect>
          </g>
        </g>
      </g>
      
      <!-- Transaction Flows -->
      <g class="transaction-flows">
        <g v-for="flow in activeFlows" :key="flow.id" class="tx-flow">
          <!-- Flow Path -->
          <path
            :d="generateFlowPath(flow)"
            fill="none"
            :stroke="getFlowColor(flow)"
            :stroke-width="getFlowWidth(flow)"
            marker-end="url(#txArrow)"
            opacity="0.7"
            class="flow-path"
          />
          
          <!-- Animated Transaction -->
          <circle
            v-for="particle in flow.particles"
            :key="particle.id"
            :r="particle.size"
            :fill="getParticleColor(particle)"
            filter="url(#txGlow)"
            class="tx-particle"
          >
            <animateMotion
              :dur="getFlowDuration(flow)"
              repeatCount="indefinite"
              :begin="particle.delay"
            >
              <mpath :href="`#flow-path-${flow.id}`" />
            </animateMotion>
          </circle>
          
          <!-- Flow Label -->
          <text
            :x="getFlowMidpoint(flow).x"
            :y="getFlowMidpoint(flow).y - 10"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#ffffff' : '#000000'"
            font-size="10"
            opacity="0.8"
          >{{ flow.throughput }}/s</text>
        </g>
      </g>
      
      <!-- Block Creation Area -->
      <g class="block-creation">
        <rect
          :x="blockCreationArea.x"
          :y="blockCreationArea.y"
          :width="blockCreationArea.width"
          :height="blockCreationArea.height"
          :fill="getBlockAreaColor()"
          :stroke="theme.primary"
          stroke-width="3"
          stroke-dasharray="10,5"
          rx="12"
          opacity="0.3"
        >
          <animate
            v-if="isBlockBeingCreated"
            attributeName="opacity"
            values="0.3;0.7;0.3"
            dur="1s"
            repeatCount="indefinite"
          />
        </rect>
        
        <text
          :x="blockCreationArea.x + blockCreationArea.width/2"
          :y="blockCreationArea.y + 25"
          text-anchor="middle"
          :fill="theme.primary"
          font-size="16"
          font-weight="600"
        >Block Assembly</text>
        
        <!-- Current Block Preview -->
        <g v-if="currentBlock" class="current-block">
          <rect
            :x="blockCreationArea.x + 20"
            :y="blockCreationArea.y + 40"
            :width="blockCreationArea.width - 40"
            height="60"
            :fill="themeStore.isDark ? '#374151' : '#f9fafb'"
            :stroke="theme.primary"
            stroke-width="1"
            rx="4"
          />
          
          <text
            :x="blockCreationArea.x + blockCreationArea.width/2"
            :y="blockCreationArea.y + 60"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#ffffff' : '#000000'"
            font-size="12"
            font-weight="500"
          >Block #{{ currentBlock.number }}</text>
          
          <text
            :x="blockCreationArea.x + blockCreationArea.width/2"
            :y="blockCreationArea.y + 80"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
            font-size="10"
          >{{ currentBlock.transactionCount }} transactions</text>
        </g>
      </g>
      
      <!-- Statistics Overlay -->
      <g class="statistics-overlay">
        <rect
          x="10"
          y="10"
          width="200"
          height="120"
          :fill="themeStore.isDark ? 'rgba(0,0,0,0.8)' : 'rgba(255,255,255,0.9)'"
          stroke="none"
          rx="8"
        />
        
        <text x="20" y="30" :fill="themeStore.isDark ? '#ffffff' : '#000000'" font-size="14" font-weight="600">
          Network Activity
        </text>
        
        <text x="20" y="50" :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'" font-size="12">
          TPS: {{ currentTPS }}
        </text>
        
        <text x="20" y="70" :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'" font-size="12">
          Pool Size: {{ totalPoolSize }}
        </text>
        
        <text x="20" y="90" :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'" font-size="12">
          Avg Fee: {{ averageFee }} ETH
        </text>
        
        <text x="20" y="110" :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'" font-size="12">
          Next Block: {{ nextBlockTime }}s
        </text>
      </g>
    </svg>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useThemeStore } from '@/stores/theme'

const props = defineProps({
  width: {
    type: Number,
    default: 800
  },
  height: {
    type: Number,
    default: 500
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
  },
  transactions: {
    type: Array,
    default: () => []
  },
  isRealTime: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['transaction-select', 'block-created'])

const themeStore = useThemeStore()
const flowSvg = ref(null)

// Reactive data
const transactionPools = ref([
  {
    id: 'mempool',
    name: 'Memory Pool',
    x: 150,
    y: 150,
    width: 200,
    height: 120,
    pendingCount: 1250,
    priority: 'mixed'
  },
  {
    id: 'priority',
    name: 'Priority Pool',
    x: 150,
    y: 350,
    width: 200,
    height: 80,
    pendingCount: 85,
    priority: 'high'
  }
])

const activeFlows = ref([
  {
    id: 'mempool-to-block',
    from: { x: 250, y: 150 },
    to: { x: 550, y: 250 },
    throughput: 15.5,
    priority: 'mixed',
    particles: [
      { id: 1, size: 3, delay: '0s' },
      { id: 2, size: 2, delay: '0.5s' },
      { id: 3, size: 4, delay: '1s' }
    ]
  },
  {
    id: 'priority-to-block',
    from: { x: 250, y: 350 },
    to: { x: 550, y: 250 },
    throughput: 8.2,
    priority: 'high',
    particles: [
      { id: 4, size: 4, delay: '0s' },
      { id: 5, size: 3, delay: '0.3s' }
    ]
  }
])

const blockCreationArea = ref({
  x: 450,
  y: 180,
  width: 200,
  height: 140
})

const currentBlock = ref({
  number: 18425679,
  transactionCount: 234,
  timestamp: Date.now()
})

const isBlockBeingCreated = ref(false)
const currentTPS = ref(23.7)
const totalPoolSize = ref(1335)
const averageFee = ref(0.0034)
const nextBlockTime = ref(12)

// Computed properties
const getPoolTransactions = (pool) => {
  const maxDisplay = 24 // 6x4 grid
  const count = Math.min(pool.pendingCount, maxDisplay)
  return Array.from({ length: count }, (_, i) => ({
    id: `tx-${pool.id}-${i}`,
    status: i < count * 0.8 ? 'pending' : 'processing',
    priority: pool.priority === 'high' ? 'high' : (Math.random() > 0.7 ? 'high' : 'normal'),
    fee: Math.random() * 0.01
  }))
}

// Styling functions
const getPoolBackgroundColor = (pool) => {
  const alpha = themeStore.isDark ? 0.2 : 0.1
  if (pool.priority === 'high') return `rgba(239, 68, 68, ${alpha})`
  return `rgba(59, 130, 246, ${alpha})`
}

const getPoolBorderColor = (pool) => {
  if (pool.priority === 'high') return props.theme.danger
  return props.theme.primary
}

const getTransactionColor = (tx) => {
  if (tx.priority === 'high') return props.theme.danger
  if (tx.status === 'processing') return props.theme.warning
  return props.theme.secondary
}

const getFlowColor = (flow) => {
  if (flow.priority === 'high') return `url(#txFlowHigh)`
  if (flow.priority === 'medium') return `url(#txFlowMedium)`
  return `url(#txFlowLow)`
}

const getFlowWidth = (flow) => {
  const baseWidth = 2
  const throughputMultiplier = Math.log10(flow.throughput + 1) * 2
  return baseWidth + throughputMultiplier
}

const getFlowDuration = (flow) => {
  const baseSpeed = 3 // seconds
  const speedMultiplier = Math.max(0.5, 2 - (flow.throughput / 20))
  return `${baseSpeed * speedMultiplier}s`
}

const getParticleColor = (particle) => {
  const colors = [props.theme.primary, props.theme.secondary, props.theme.warning]
  return colors[particle.id % colors.length]
}

const getBlockAreaColor = () => {
  const alpha = themeStore.isDark ? 0.1 : 0.05
  return `rgba(59, 130, 246, ${alpha})`
}

// Path generation
const generateFlowPath = (flow) => {
  const { from, to } = flow
  const controlX1 = from.x + (to.x - from.x) * 0.3
  const controlY1 = from.y - 30
  const controlX2 = from.x + (to.x - from.x) * 0.7
  const controlY2 = to.y - 30
  
  return `M ${from.x} ${from.y} C ${controlX1} ${controlY1}, ${controlX2} ${controlY2}, ${to.x} ${to.y}`
}

const getFlowMidpoint = (flow) => {
  return {
    x: (flow.from.x + flow.to.x) / 2,
    y: (flow.from.y + flow.to.y) / 2 - 20
  }
}

// Event handlers
const selectTransaction = (tx) => {
  emit('transaction-select', tx)
}

// Animation and updates
let animationInterval = null

const updateStats = () => {
  if (props.isRealTime) {
    currentTPS.value = +(Math.random() * 30 + 10).toFixed(1)
    totalPoolSize.value = Math.floor(Math.random() * 2000 + 1000)
    averageFee.value = +(Math.random() * 0.01 + 0.001).toFixed(4)
    nextBlockTime.value = Math.floor(Math.random() * 15 + 8)
  }
}

const simulateBlockCreation = () => {
  if (props.isRealTime && Math.random() > 0.85) {
    isBlockBeingCreated.value = true
    setTimeout(() => {
      currentBlock.value.number++
      currentBlock.value.transactionCount = Math.floor(Math.random() * 300 + 100)
      currentBlock.value.timestamp = Date.now()
      isBlockBeingCreated.value = false
      emit('block-created', currentBlock.value)
    }, 2000)
  }
}

// Lifecycle
onMounted(() => {
  if (props.isRealTime) {
    animationInterval = setInterval(() => {
      updateStats()
      simulateBlockCreation()
    }, 3000)
  }
})

onUnmounted(() => {
  if (animationInterval) {
    clearInterval(animationInterval)
  }
})

// Watchers
watch(() => props.isRealTime, (newValue) => {
  if (newValue && !animationInterval) {
    animationInterval = setInterval(() => {
      updateStats()
      simulateBlockCreation()
    }, 3000)
  } else if (!newValue && animationInterval) {
    clearInterval(animationInterval)
    animationInterval = null
  }
})
</script>

<style scoped>
.transaction-flow-visualization {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--color-background);
  border-radius: 0.5rem;
}

.pool-container {
  transition: all 0.3s ease;
}

.pool-container:hover {
  filter: brightness(1.1);
}

.tx-item {
  cursor: pointer;
  transition: all 0.2s ease;
}

.tx-item:hover {
  transform: scale(1.2);
  opacity: 1 !important;
}

.flow-path {
  transition: stroke-width 0.3s ease;
}

.tx-particle {
  filter: drop-shadow(0 0 4px currentColor);
}

.current-block {
  animation: blockPulse 2s ease-in-out infinite;
}

@keyframes blockPulse {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}
</style>