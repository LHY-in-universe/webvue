<template>
  <div class="p2p-network-visualization w-full h-full relative">
    <svg 
      ref="networkSvg"
      class="w-full h-full"
      :viewBox="`0 0 ${svgDimensions.width} ${svgDimensions.height}`"
      preserveAspectRatio="xMidYMid meet"
    >
      <!-- Clean background -->
      <rect width="100%" height="100%" :fill="themeStore.isDark ? '#111827' : '#ffffff'" />
      
      <!-- Gradient and Pattern Definitions -->
      <defs>
        <!-- Connection colors -->
        <linearGradient id="connectionGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#34d399' : '#10b981'" />
          <stop offset="100%" :stop-color="themeStore.isDark ? '#22c55e' : '#059669'" />
        </linearGradient>
        
        <!-- Edge node gradient (blue) -->
        <radialGradient id="edgeGradient" cx="50%" cy="50%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#93c5fd' : '#dbeafe'" />
          <stop offset="100%" :stop-color="themeStore.isDark ? '#3b82f6' : '#2563eb'" />
        </radialGradient>
        
        <!-- Control node gradient (red) -->
        <radialGradient id="controlGradient" cx="50%" cy="50%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#fca5a5' : '#fecaca'" />
          <stop offset="100%" :stop-color="themeStore.isDark ? '#ef4444' : '#dc2626'" />
        </radialGradient>
        
        <!-- Connection Arrow Marker -->
        <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                refX="9" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" fill="url(#connectionGradient)" />
        </marker>
        
        <!-- Drop Shadow Filter -->
        <filter id="dropShadow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="4"/>
          <feOffset dx="2" dy="4" result="offset" />
          <feComponentTransfer>
            <feFuncA type="linear" slope="0.2"/>
          </feComponentTransfer>
          <feMerge> 
            <feMergeNode/>
            <feMergeNode in="SourceGraphic"/> 
          </feMerge>
        </filter>
      </defs>
      
      <!-- Connections -->
      <g class="connections">
        <g v-for="connection in connections" :key="`${connection.from}-${connection.to}`">
          <!-- Transparent Background Connection Line -->
          <path
            :d="getConnectionPath(connection)"
            stroke="transparent"
            stroke-width="2"
            stroke-linecap="round"
            fill="none"
            class="background-connection-line"
          />
          
          <!-- Enhanced Data Flow Animation -->
          <g v-if="connection.active && trainingActive" class="enhanced-data-flow">
            <!-- 脉冲光晕效果 -->
            <path
              :d="getConnectionPath(connection)"
              :stroke="getTransmissionColor(connection.direction)"
              stroke-width="8"
              stroke-linecap="round"
              fill="none"
              opacity="0.6"
              class="pulse-glow"
            >
              <animate
                attributeName="opacity"
                values="0.2;0.8;0.2"
                dur="2s"
                repeatCount="indefinite"
              />
              <animate
                attributeName="stroke-width"
                values="6;12;6"
                dur="2s"
                repeatCount="indefinite"
              />
            </path>
            
            <!-- 波浪传输效果 -->
            <path
              :d="getConnectionPath(connection)"
              :stroke="getTransmissionColor(connection.direction)"
              stroke-width="4"
              stroke-linecap="round"
              stroke-dasharray="15,30"
              fill="none"
              class="wave-transmission"
            >
              <animate
                attributeName="stroke-dashoffset"
                :values="getAnimationValues(connection.direction)"
                dur="2s"
                repeatCount="indefinite"
              />
            </path>
            
            <!-- 数据包粒子效果 -->
            <g v-for="(particle, index) in getDataParticles(connection)" :key="`particle-${index}`">
              <circle
                :cx="particle.x"
                :cy="particle.y"
                :r="particle.size"
                :fill="particle.color"
                class="data-particle"
              >
                <animate
                  attributeName="opacity"
                  values="0;1;0"
                  :dur="particle.duration"
                  :begin="particle.delay"
                  repeatCount="indefinite"
                />
                <animate
                  attributeName="r"
                  values="2;4;2"
                  :dur="particle.duration"
                  :begin="particle.delay"
                  repeatCount="indefinite"
                />
              </circle>
            </g>
          </g>
        </g>
      </g>
      
      <!-- Nodes -->
      <g class="nodes">
        <g v-for="node in visibleNodes" :key="node.id" 
           class="node-group static-node"
           :style="{ 
             opacity: 1,
             transform: `scale(1)`,
             transformOrigin: `${getNodePosition(node).x}px ${getNodePosition(node).y}px`,
             pointerEvents: 'all'
           }"
        >
          <!-- Main Node Circle -->
          <circle
            :cx="getNodePosition(node).x"
            :cy="getNodePosition(node).y"
            :r="getNodeRadius(node)"
            :fill="getNodeFillColor(node)"
            :stroke="themeStore.isDark ? '#ffffff' : '#000000'"
            stroke-width="2"
            class="node-circle cursor-pointer select-none no-hover clickable-node"
            style="pointer-events: all; user-select: none;"
            @click.stop.prevent="handleNodeClick(node)"
          />
          
          <!-- Node Label -->
          <text
            :x="getNodePosition(node).x"
            :y="getNodePosition(node).y - getNodeRadius(node) - 10"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#ffffff' : '#000000'"
            font-size="12"
            font-weight="600"
            class="node-label"
          >{{ node.name || node.id }}</text>
          
        </g>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.static-node {
  cursor: pointer;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  pointer-events: all;
}

.static-node * {
  cursor: pointer !important;
  user-select: none !important;
  -webkit-user-select: none !important;
  -moz-user-select: none !important;
  -ms-user-select: none !important;
  pointer-events: all !important;
}

.node-circle {
  cursor: pointer !important;
  user-select: none !important;
  -webkit-user-select: none !important;
  -webkit-user-drag: none !important;
  -webkit-touch-callout: none !important;
}

.clickable-node {
  cursor: pointer !important;
}

.clickable-node:hover {
  cursor: pointer !important;
}

.node-group {
  cursor: pointer;
}

svg {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

.p2p-network-visualization {
  background: transparent;
  overflow: hidden;
}

.node-circle {
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Static nodes with no hover effects */
.no-hover,
.no-hover:hover,
.node-group:hover .no-hover,
.static-node:hover,
.static-node:hover * {
  transform: none !important;
  filter: none !important;
  transition: none !important;
  stroke-width: 2 !important;
  font-weight: inherit !important;
  font-size: inherit !important;
}

.node-label,
.progress-text {
  pointer-events: none;
  user-select: none;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.connection-line {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 增强的数据流动画样式 */
.enhanced-data-flow {
  pointer-events: none;
}

.pulse-glow {
  filter: drop-shadow(0 0 8px currentColor);
  animation: pulse-glow 2s ease-in-out infinite;
}

.wave-transmission {
  filter: drop-shadow(0 0 4px currentColor);
  animation: wave-flow 2s linear infinite;
}

.data-particle {
  filter: drop-shadow(0 0 3px currentColor);
  animation: particle-float 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    opacity: 0.2;
    stroke-width: 6;
  }
  50% {
    opacity: 0.8;
    stroke-width: 12;
  }
}

@keyframes wave-flow {
  0% {
    stroke-dashoffset: 0;
  }
  100% {
    stroke-dashoffset: -45;
  }
}

@keyframes particle-float {
  0%, 100% {
    opacity: 0;
    transform: scale(0.5);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

/* 原有数据流动画样式保持兼容 */
.data-flow-animation {
  filter: drop-shadow(0 0 4px currentColor);
  opacity: 0.9;
}

.data-flow-upstream {
  filter: drop-shadow(0 0 6px #3b82f6);
}

.data-flow-downstream {
  filter: drop-shadow(0 0 6px #10b981);
}

.data-flow-bidirectional {
  filter: drop-shadow(0 0 6px #8b5cf6);
}

.background-connection-line {
  pointer-events: none;
}

@media (max-width: 768px) {
  .node-label,
  .progress-text {
    font-size: 10px;
  }
}
</style>

<script setup>
import { ref, computed, reactive, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useThemeStore } from '@/stores/theme'

const props = defineProps({
  nodes: {
    type: Array,
    required: true
  },
  connections: {
    type: Array,
    required: true
  },
  trainingActive: {
    type: Boolean,
    default: false
  },
  showTrainingComplete: {
    type: Boolean,
    default: false
  },
  maxNodes: {
    type: Number,
    default: 30
  },
  projectType: {
    type: String,
    default: 'federated',
    validator: value => ['federated', 'mpc'].includes(value)
  }
})

const emit = defineEmits(['node-click', 'connection-click'])

const themeStore = useThemeStore()
const networkSvg = ref(null)

// Fixed layout dimensions - Updated for 700px container
const svgDimensions = reactive({
  width: 1200,
  height: 700,
  padding: 80
})

// P2P Regular topology - Fixed positions for predictable layout
const CONTROL_NODE_POSITIONS = [
  { x: 600, y: 70 }  // Central server at top with better spacing
]

// Fixed regular circular positions - Your device in center, others in two circles
// Updated for 700px container with better scaling and centering
const EDGE_NODE_POSITIONS = [
  { x: 600, y: 350 },  // Index 0: Your device in center (true center of 700px)
  
  // Inner circle - 6 positions around center (radius 150, increased from 130)
  { x: 600, y: 200 },  // Index 1: Top
  { x: 730, y: 275 },  // Index 2: Top-right (60° from top)
  { x: 730, y: 425 },  // Index 3: Bottom-right (120° from top)
  { x: 600, y: 500 },  // Index 4: Bottom (180° from top)
  { x: 470, y: 425 },  // Index 5: Bottom-left (240° from top)
  { x: 470, y: 275 },  // Index 6: Top-left (300° from top)
  
  // Outer circle - 8 positions around center (radius 250, increased from 200)
  { x: 777, y: 173 },  // Index 7: Top-right (45° from top)
  { x: 850, y: 350 },  // Index 8: Right (90° from top)
  { x: 777, y: 527 },  // Index 9: Bottom-right (135° from top)
  { x: 600, y: 600 },  // Index 10: Bottom (180° from top)
  { x: 423, y: 527 },  // Index 11: Bottom-left (225° from top)
  { x: 350, y: 350 },  // Index 12: Left (270° from top)
  { x: 423, y: 173 },  // Index 13: Top-left (315° from top)
  { x: 716, y: 134 }   // Index 14: Top-right diagonal (30° from top)
]

// Performance optimization - visible nodes
const visibleNodes = computed(() => {
  if (props.nodes.length <= props.maxNodes) {
    return props.nodes
  }
  
  // Priority: control nodes first, then own nodes, then active nodes
  const controlNodes = props.nodes.filter(n => n.type === 'control')
  const ownNodes = props.nodes.filter(n => n.isOwn && n.type !== 'control')
  const otherActiveNodes = props.nodes
    .filter(n => !n.isOwn && n.type !== 'control' && n.status !== 'offline')
    .sort((a, b) => (b.progress || 0) - (a.progress || 0))
    .slice(0, Math.max(0, props.maxNodes - controlNodes.length - ownNodes.length))
    
  return [...controlNodes, ...ownNodes, ...otherActiveNodes]
})

// Node position tracking
const nodePositions = ref(new Map())

// Stable position assignment function
const getStablePositionIndex = (nodeId, nodeType, isOwn = false) => {
  if (nodeType === 'control') {
    // Control node stable assignment
    if (nodeId.includes('server')) return 0
    if (nodeId.includes('control')) return 0
    return 0
  } else if (nodeType === 'edge') {
    // Your device always gets center position (index 0)
    if (isOwn) return 0
    
    // Other edge nodes based on ID stable assignment (starting from index 1)
    const match = nodeId.match(/(\d+)/)
    if (match) {
      const nodeNumber = parseInt(match[1])
      return ((nodeNumber - 1) % (EDGE_NODE_POSITIONS.length - 1)) + 1
    }
    return 1 // Default to index 1 if no number found
  }
  return 0
}

// Initialize fixed positions for all nodes
const initializeNodePositions = () => {
  console.log('Initializing P2P positions for', props.nodes.length, 'nodes')
  
  props.nodes.forEach((node, index) => {
    // Skip nodes that already have positions
    if (nodePositions.value.has(node.id)) {
      return
    }
    
    if (node.type === 'control') {
      // Use stable control node position assignment
      const positionIndex = getStablePositionIndex(node.id, node.type, node.isOwn)
      if (positionIndex < CONTROL_NODE_POSITIONS.length) {
        nodePositions.value.set(node.id, CONTROL_NODE_POSITIONS[positionIndex])
        console.log(`Positioned control node ${node.id} at`, CONTROL_NODE_POSITIONS[positionIndex])
      }
    } else if (node.type === 'edge') {
      // Use stable edge node position assignment
      const positionIndex = getStablePositionIndex(node.id, node.type, node.isOwn)
      if (positionIndex < EDGE_NODE_POSITIONS.length) {
        nodePositions.value.set(node.id, EDGE_NODE_POSITIONS[positionIndex])
        console.log(`Positioned ${node.isOwn ? 'YOUR' : 'edge'} node ${node.id} at`, EDGE_NODE_POSITIONS[positionIndex])
      }
    }
  })
  
  console.log('Total positioned nodes:', nodePositions.value.size)
}

// Get position for a specific node
const getNodePosition = (node) => {
  // First check if we have a stored position
  const storedPosition = nodePositions.value.get(node.id)
  if (storedPosition) {
    // Return a copy to prevent any modifications to the original position
    return { x: storedPosition.x, y: storedPosition.y }
  }
  
  // If no stored position, assign one immediately using stable index
  if (node.type === 'control') {
    const positionIndex = getStablePositionIndex(node.id, node.type, node.isOwn)
    if (positionIndex < CONTROL_NODE_POSITIONS.length) {
      const position = CONTROL_NODE_POSITIONS[positionIndex]
      nodePositions.value.set(node.id, position)
      return position
    }
  } else if (node.type === 'edge') {
    const positionIndex = getStablePositionIndex(node.id, node.type, node.isOwn)
    if (positionIndex < EDGE_NODE_POSITIONS.length) {
      const position = EDGE_NODE_POSITIONS[positionIndex]
      nodePositions.value.set(node.id, position)
      return position
    }
  }
  
  // Fallback to node's original coordinates if available
  if (node.x && node.y) {
    return { x: node.x, y: node.y }
  }
  
  // Default position if nothing else works
  console.warn(`No position found for node ${node.id}, using default`)
  return { x: 400, y: 250 }
}

// Node styling functions
const getNodeRadius = (node) => {
  if (node.type === 'control') {
    return 30 // Control nodes larger
  }
  return node.isOwn ? 25 : 22 // Own device slightly larger
}

const getNodeFillColor = (node) => {
  if (node.type === 'control') {
    // Control node - red
    return themeStore.isDark ? '#ef4444' : '#dc2626'
  } else if (node.type === 'edge') {
    if (node.isOwn) {
      // Own device - blue
      return themeStore.isDark ? '#3b82f6' : '#2563eb'
    } else {
      // Other edge devices - green
      return themeStore.isDark ? '#10b981' : '#059669'
    }
  }
  return '#6b7280' // Default gray
}

// Helper functions
const getConnectionPath = (connection) => {
  const fromNode = props.nodes.find(n => n.id === connection.from)
  const toNode = props.nodes.find(n => n.id === connection.to)
  
  if (!fromNode || !toNode) return ''
  
  // Use computed positions
  const fromPos = getNodePosition(fromNode)
  const toPos = getNodePosition(toNode)
  
  // Create curved path
  const dx = toPos.x - fromPos.x
  const dy = toPos.y - fromPos.y
  const distance = Math.sqrt(dx * dx + dy * dy)
  const midX = fromPos.x + dx * 0.5
  const midY = fromPos.y + dy * 0.5
  
  let offset = Math.min(60, Math.max(20, distance / 6))
  
  const angle = Math.atan2(dy, dx) + Math.PI / 2
  const ctrlX = midX + Math.cos(angle) * offset
  const ctrlY = midY + Math.sin(angle) * offset
  
  return `M ${fromPos.x} ${fromPos.y} Q ${ctrlX} ${ctrlY} ${toPos.x} ${toPos.y}`
}

// Data flow animation functions
const getTransmissionColor = (direction) => {
  const colors = {
    upstream: '#3b82f6',      // Blue: edge → control (data upload)
    downstream: '#10b981',    // Green: control → edge (model download)
    bidirectional: '#8b5cf6'  // Purple: bidirectional
  }
  return colors[direction] || '#10b981'
}

const getAnimationValues = (direction) => {
  switch (direction) {
    case 'downstream': // Control → edge
      return "0;-120;-240"
    case 'upstream':   // Edge → control
      return "0;120;240"
    case 'bidirectional': // Bidirectional
      return "0;-120;0;120;0"
    default:
      return "0;-120;-240"
  }
}

// 生成数据粒子效果
const getDataParticles = (connection) => {
  const particles = []
  const particleCount = 3
  
  for (let i = 0; i < particleCount; i++) {
    const progress = (Date.now() / 1000 + i * 0.33) % 1
    const fromNode = props.nodes.find(n => n.id === connection.from)
    const toNode = props.nodes.find(n => n.id === connection.to)
    
    if (fromNode && toNode) {
      const fromPos = getNodePosition(fromNode)
      const toPos = getNodePosition(toNode)
      
      // 计算粒子在路径上的位置
      const x = fromPos.x + (toPos.x - fromPos.x) * progress
      const y = fromPos.y + (toPos.y - fromPos.y) * progress
      
      particles.push({
        x,
        y,
        size: 3 + Math.sin(Date.now() / 200 + i) * 1,
        color: getTransmissionColor(connection.direction),
        duration: '2s',
        delay: `${i * 0.5}s`
      })
    }
  }
  
  return particles
}

// Node interaction handlers
const handleNodeClick = (node) => {
  emit('node-click', node)
}

// Responsive layout support
const updateDimensions = () => {
  if (!networkSvg.value) return
  
  const container = networkSvg.value.parentElement
  if (container) {
    const rect = container.getBoundingClientRect()
    svgDimensions.width = Math.max(1200, rect.width)
    svgDimensions.height = Math.max(700, rect.height)
  }
}

// Initialize node positions
const autoArrange = () => {
  nextTick(() => {
    initializeNodePositions()
  })
}

// Lifecycle management
onMounted(() => {
  updateDimensions()
  initializeNodePositions()
  window.addEventListener('resize', updateDimensions)
  
  // Force position initialization after delay
  setTimeout(() => {
    console.log('Force initializing P2P positions for', props.nodes.length, 'nodes')
    initializeNodePositions()
  }, 100)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateDimensions)
})

// Watch for node changes and reinitialize positions
watch(() => props.nodes.length, () => {
  autoArrange()
}, { immediate: true })

watch(() => props.nodes, () => {
  autoArrange()
}, { deep: true, immediate: true })

defineExpose({
  autoArrange,
  updateDimensions
})
</script>