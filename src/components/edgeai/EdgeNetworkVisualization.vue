<template>
  <div class="edge-network-visualization w-full h-full relative">
    <svg 
      ref="networkSvg"
      class="w-full h-full cursor-grab"
      :class="{ 'cursor-grabbing': isDragging }"
      :viewBox="`${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`"
      preserveAspectRatio="xMidYMid meet"
      @mousedown="handlePanStart"
      @mousemove="handlePanMove"
      @mouseup="handlePanEnd"
      @mouseleave="handlePanEnd"
      @wheel="handleZoom"
    >
      <!-- Background -->
      <rect width="100%" height="100%" :fill="themeStore.isDark ? '#1f2937' : '#f8fafc'" />
      
      <!-- Grid Pattern and Gradients -->
      <defs>
        <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
          <path 
            d="M 50 0 L 0 0 0 50" 
            fill="none" 
            :stroke="themeStore.isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'" 
            stroke-width="0.5"
          />
          <circle cx="0" cy="0" r="0.8" :fill="themeStore.isDark ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.1)'" />
        </pattern>
        
        <!-- Node Gradients -->
        <radialGradient id="controlGradient" cx="30%" cy="30%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#fca5a5' : '#fee2e2'" />
          <stop offset="100%" :stop-color="props.theme.danger" />
        </radialGradient>
        
        <radialGradient id="edgeGradient" cx="30%" cy="30%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#6ee7b7' : '#d1fae5'" />
          <stop offset="100%" :stop-color="props.theme.primary" />
        </radialGradient>
        
        <radialGradient id="gatewayGradient" cx="30%" cy="30%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#fde68a' : '#fef3c7'" />
          <stop offset="100%" :stop-color="props.theme.warning" />
        </radialGradient>
        
        <radialGradient id="clientGradient" cx="30%" cy="30%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#93c5fd' : '#dbeafe'" />
          <stop offset="100%" :stop-color="props.theme.secondary" />
        </radialGradient>
        
        <!-- Connection Arrow Marker -->
        <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                refX="9" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" :fill="themeStore.isDark ? '#34d399' : props.theme.primary" />
        </marker>
        
        <!-- Drop Shadow Filter -->
        <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
          <feOffset dx="2" dy="4" result="offset" />
          <feComponentTransfer>
            <feFuncA type="linear" slope="0.3"/>
          </feComponentTransfer>
          <feMerge> 
            <feMergeNode/>
            <feMergeNode in="SourceGraphic"/> 
          </feMerge>
        </filter>
      </defs>
      
      <rect width="2000" height="2000" fill="url(#grid)" />
      
      <!-- Connections -->
      <g class="connections">
        <g v-for="connection in connections" :key="`${connection.from}-${connection.to}`">
          <!-- Connection Background (for glow effect) -->
          <path
            :d="getConnectionPath(connection)"
            :stroke="getConnectionColor(connection, true)"
            :stroke-width="getConnectionWidth(connection) + 4"
            stroke-linecap="round"
            :opacity="connection.active ? 0.3 : 0.1"
            fill="none"
          />
          
          <!-- Main Connection Line -->
          <path
            :d="getConnectionPath(connection)"
            :stroke="getConnectionColor(connection)"
            :stroke-width="getConnectionWidth(connection)"
            stroke-linecap="round"
            fill="none"
            marker-end="url(#arrowhead)"
            :opacity="connection.active ? 0.8 : 0.4"
            class="connection-line"
          >
            <!-- Connection pulse animation -->
            <animate
              v-if="connection.active"
              attributeName="stroke-dasharray"
              values="0,50;25,25;50,0"
              dur="2s"
              repeatCount="indefinite"
            />
          </path>
          
          <!-- Bandwidth indicator -->
          <text
            v-if="connection.bandwidth && connection.active"
            :x="getMidpoint(connection).x"
            :y="getMidpoint(connection).y - 8"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
            font-size="10"
            class="connection-label"
          >
            {{ formatBandwidth(connection.bandwidth) }}
          </text>
          
          <!-- Data flow particles -->
          <g v-if="connection.active && showDataFlow">
            <circle
              v-for="i in getParticleCount(connection)"
              :key="`particle-${i}`"
              r="3"
              :fill="getConnectionColor(connection)"
              :opacity="0.8"
            >
              <animateMotion
                :dur="getParticleSpeed(connection) + 's'"
                repeatCount="indefinite"
                :begin="`${i * 0.5}s`"
                :path="getConnectionPath(connection)"
              />
            </circle>
          </g>
        </g>
      </g>
      
      <!-- Nodes -->
      <g class="nodes">
        <g v-for="node in nodes" :key="node.id" class="node-group" :transform="`translate(${node.x}, ${node.y})`">
          <!-- Node Outer Ring (Selection indicator) -->
          <circle
            v-if="selectedNode?.id === node.id"
            r="35"
            fill="none"
            stroke="#fbbf24"
            stroke-width="2"
            :opacity="0.6"
          >
            <animate attributeName="r" values="35;40;35" dur="2s" repeatCount="indefinite" />
          </circle>
          
          <!-- Performance Ring -->
          <circle
            v-if="showPerformanceRings && node.performance"
            r="28"
            fill="none"
            :stroke="getPerformanceColor(node.performance)"
            stroke-width="3"
            :stroke-dasharray="`${(node.performance / 100) * 2 * Math.PI * 28} ${2 * Math.PI * 28}`"
            transform="rotate(-90)"
            :opacity="0.8"
          >
            <animate v-if="node.status === 'training'" attributeName="stroke-dashoffset" 
                     values="0;-175" dur="3s" repeatCount="indefinite" />
          </circle>
          
          <!-- Node Background Shadow -->
          <circle
            r="22"
            :fill="getNodeGradient(node)"
            filter="url(#dropShadow)"
            :opacity="0.1"
            transform="translate(1, 2)"
          />
          
          <!-- Main Node Circle -->
          <circle
            r="22"
            :fill="getNodeGradient(node)"
            :stroke="getNodeBorderColor(node)"
            :stroke-width="node.selected || selectedNode?.id === node.id ? 2 : 1"
            class="node-circle cursor-pointer transition-all duration-300"
            @click="handleNodeClick(node)"
            @mouseover="handleNodeHover(node, $event)"
            @mouseleave="handleNodeLeave(node)"
            @mousedown="handleNodeDragStart(node, $event)"
          >
            <!-- Node pulse animation for active nodes -->
            <animate
              v-if="node.status === 'training' || node.status === 'processing'"
              attributeName="r"
              values="22;24;22"
              dur="2s"
              repeatCount="indefinite"
            />
          </circle>
          
          <!-- Node Icon (SVG) -->
          <g class="node-icon" transform="translate(-8, -8)">
            <!-- Control Node Icon -->
            <g v-if="node.type === 'control'">
              <path d="M8 2L2 8l6 6 6-6-6-6z" :fill="themeStore.isDark ? '#fef3c7' : '#7c2d12'" stroke="none" />
              <circle cx="8" cy="8" r="2" :fill="themeStore.isDark ? '#fbbf24' : '#fed7aa'" />
            </g>
            
            <!-- Edge Node Icon -->
            <g v-else-if="node.type === 'edge'">
              <rect x="2" y="4" width="12" height="8" rx="2" :fill="themeStore.isDark ? '#d1fae5' : '#065f46'" />
              <rect x="4" y="6" width="8" height="1" :fill="themeStore.isDark ? '#10b981' : '#a7f3d0'" />
              <rect x="4" y="8" width="6" height="1" :fill="themeStore.isDark ? '#10b981' : '#a7f3d0'" />
              <rect x="4" y="10" width="4" height="1" :fill="themeStore.isDark ? '#10b981' : '#a7f3d0'" />
            </g>
            
            <!-- Gateway Node Icon -->
            <g v-else-if="node.type === 'gateway'">
              <circle cx="8" cy="8" r="6" fill="none" :stroke="themeStore.isDark ? '#fef3c7' : '#92400e'" stroke-width="2" />
              <circle cx="8" cy="8" r="2" :fill="themeStore.isDark ? '#fbbf24' : '#fcd34d'" />
              <circle cx="8" cy="4" r="1" :fill="themeStore.isDark ? '#fbbf24' : '#fcd34d'" />
              <circle cx="8" cy="12" r="1" :fill="themeStore.isDark ? '#fbbf24' : '#fcd34d'" />
              <circle cx="4" cy="8" r="1" :fill="themeStore.isDark ? '#fbbf24' : '#fcd34d'" />
              <circle cx="12" cy="8" r="1" :fill="themeStore.isDark ? '#fbbf24' : '#fcd34d'" />
            </g>
            
            <!-- Client Node Icon -->
            <g v-else-if="node.type === 'client'">
              <rect x="3" y="3" width="10" height="7" rx="1" :fill="themeStore.isDark ? '#dbeafe' : '#1e40af'" />
              <rect x="4" y="11" width="8" height="2" rx="1" :fill="themeStore.isDark ? '#93c5fd' : '#3b82f6'" />
              <rect x="7" y="10" width="2" height="1" :fill="themeStore.isDark ? '#93c5fd' : '#3b82f6'" />
            </g>
          </g>
          
          <!-- Node Label -->
          <text
            y="-35"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#f3f4f6' : '#111827'"
            font-size="12"
            font-weight="600"
            class="node-label"
          >{{ node.name || node.id }}</text>
          
          <!-- Status Indicator -->
          <circle
            cx="18"
            cy="-18"
            r="5"
            :fill="getStatusColor(node.status)"
            :stroke="themeStore.isDark ? '#1f2937' : '#ffffff'"
            stroke-width="2"
          >
            <!-- Status pulse animation -->
            <animate
              v-if="node.status === 'training'"
              attributeName="r"
              values="5;7;5"
              dur="1.5s"
              repeatCount="indefinite"
            />
          </circle>
          
          <!-- Resource Bars -->
          <g v-if="showResourceBars && node.resources" transform="translate(-20, 30)">
            <!-- CPU Bar Background -->
            <rect x="0" y="0" width="40" height="4" fill="rgba(0,0,0,0.1)" rx="2" />
            <!-- CPU Bar Fill -->
            <rect 
              x="0" y="0" 
              :width="(node.resources.cpu / 100) * 40" 
              height="4" 
              :fill="props.theme.warning" 
              rx="2"
            >
              <animate attributeName="width" 
                       :values="`0;${(node.resources.cpu / 100) * 40}`" 
                       dur="1s" begin="0s" fill="freeze" />
            </rect>
            
            <!-- Memory Bar Background -->
            <rect x="0" y="6" width="40" height="4" fill="rgba(0,0,0,0.1)" rx="2" />
            <!-- Memory Bar Fill -->
            <rect 
              x="0" y="6" 
              :width="(node.resources.memory / 100) * 40" 
              height="4" 
              :fill="props.theme.primary" 
              rx="2"
            >
              <animate attributeName="width" 
                       :values="`0;${(node.resources.memory / 100) * 40}`" 
                       dur="1s" begin="0.2s" fill="freeze" />
            </rect>
            
            <!-- Resource Labels -->
            <text x="42" y="3" font-size="8" :fill="themeStore.isDark ? '#9ca3af' : '#6b7280'">CPU</text>
            <text x="42" y="9" font-size="8" :fill="themeStore.isDark ? '#9ca3af' : '#6b7280'">MEM</text>
          </g>
        </g>
      </g>
    </svg>
    
    <!-- Node Info Panel -->
    <Transition name="slide-up">
      <div
        v-if="selectedNode"
        class="absolute bottom-4 right-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 w-64 z-10 border border-gray-200 dark:border-gray-700"
      >
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-semibold text-gray-900 dark:text-white">{{ selectedNode.name }}</h4>
          <button 
            @click="selectedNode = null"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="space-y-2 text-sm">
          <div class="flex justify-between">
            <span class="text-gray-500 dark:text-gray-400">Type:</span>
            <span class="font-medium">{{ getNodeTypeLabel(selectedNode.type) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500 dark:text-gray-400">Status:</span>
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 rounded-full" :class="getStatusColorClass(selectedNode.status)"></div>
              <span class="font-medium capitalize">{{ selectedNode.status }}</span>
            </div>
          </div>
          <div v-if="selectedNode.location" class="flex justify-between">
            <span class="text-gray-500 dark:text-gray-400">Location:</span>
            <span class="font-medium">{{ selectedNode.location }}</span>
          </div>
          <div v-if="selectedNode.performance" class="flex justify-between">
            <span class="text-gray-500 dark:text-gray-400">Performance:</span>
            <span class="font-medium">{{ selectedNode.performance }}%</span>
          </div>
          <div v-if="selectedNode.resources" class="mt-3">
            <div class="text-gray-500 dark:text-gray-400 text-xs mb-2">Resources:</div>
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs">CPU</span>
                <div class="flex items-center space-x-2">
                  <div class="w-16 h-1.5 bg-gray-200 dark:bg-gray-700 rounded">
                    <div 
                      class="h-1.5 bg-yellow-500 rounded" 
                      :style="{ width: `${selectedNode.resources.cpu}%` }"
                    ></div>
                  </div>
                  <span class="text-xs font-medium">{{ selectedNode.resources.cpu }}%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs">Memory</span>
                <div class="flex items-center space-x-2">
                  <div class="w-16 h-1.5 bg-gray-200 dark:bg-gray-700 rounded">
                    <div 
                      class="h-1.5 bg-blue-500 rounded" 
                      :style="{ width: `${selectedNode.resources.memory}%` }"
                    ></div>
                  </div>
                  <span class="text-xs font-medium">{{ selectedNode.resources.memory }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useThemeStore } from '@/stores/theme'

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
      primary: '#10b981',
      secondary: '#3b82f6',
      warning: '#f59e0b',
      danger: '#ef4444',
      success: '#22c55e'
    })
  },
  showDataFlow: {
    type: Boolean,
    default: true
  },
  showPerformanceRings: {
    type: Boolean,
    default: true
  },
  showResourceBars: {
    type: Boolean,
    default: true
  },
  layoutType: {
    type: String,
    default: 'force'
  }
})

const emit = defineEmits(['node-click', 'node-hover', 'node-leave', 'viewport-change'])

const themeStore = useThemeStore()
const networkSvg = ref(null)
const selectedNode = ref(null)

// Pan and zoom state
const viewBox = ref({ x: 0, y: 0, width: 800, height: 500 })
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const draggedNode = ref(null)

// Animation frame ID for smooth updates
const animationFrame = ref(null)

// Helper functions for nodes
const getNodePosition = (nodeId) => {
  const node = props.nodes.find(n => n.id === nodeId)
  return node ? { x: node.x || 400, y: node.y || 250 } : { x: 400, y: 250 }
}

const getNodeRadius = (node) => {
  return 22 // Fixed radius for modern design
}

const getNodeGradient = (node) => {
  const gradients = {
    control: 'url(#controlGradient)',
    edge: 'url(#edgeGradient)', 
    gateway: 'url(#gatewayGradient)',
    client: 'url(#clientGradient)'
  }
  return gradients[node.type] || 'url(#edgeGradient)'
}

const getNodeBorderColor = (node) => {
  if (selectedNode.value?.id === node.id) return '#fbbf24'
  return themeStore.isDark ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.2)'
}

// Connection helper functions
const getConnectionPath = (connection) => {
  const from = getNodePosition(connection.from)
  const to = getNodePosition(connection.to)
  
  // Create curved path for better visual appeal
  const midX = (from.x + to.x) / 2
  const midY = (from.y + to.y) / 2
  const offset = Math.min(50, Math.sqrt(Math.pow(to.x - from.x, 2) + Math.pow(to.y - from.y, 2)) / 4)
  
  return `M ${from.x} ${from.y} Q ${midX} ${midY - offset} ${to.x} ${to.y}`
}

const getConnectionColor = (connection, isGlow = false) => {
  const baseColors = {
    control: props.theme.danger,
    data: props.theme.primary,
    sync: props.theme.secondary
  }
  
  let color = baseColors[connection.type] || props.theme.primary
  
  if (!connection.active) {
    color = themeStore.isDark ? '#6b7280' : '#9ca3af'
  }
  
  return isGlow ? color : color
}

const getConnectionWidth = (connection) => {
  if (!connection.bandwidth) return connection.active ? 3 : 2
  
  // Scale width based on bandwidth (100-1000 range)
  const minWidth = 2
  const maxWidth = 6
  const bandwidth = Math.max(100, Math.min(1000, connection.bandwidth))
  return minWidth + ((bandwidth - 100) / 900) * (maxWidth - minWidth)
}

const getMidpoint = (connection) => {
  const from = getNodePosition(connection.from)
  const to = getNodePosition(connection.to)
  return {
    x: (from.x + to.x) / 2,
    y: (from.y + to.y) / 2 - 20
  }
}

const formatBandwidth = (bandwidth) => {
  if (bandwidth > 1000) return `${(bandwidth / 1000).toFixed(1)}Gb/s`
  return `${bandwidth}Mb/s`
}

const getParticleCount = (connection) => {
  return connection.active ? Math.max(2, Math.floor(connection.bandwidth / 300)) : 0
}

const getParticleSpeed = (connection) => {
  return connection.bandwidth > 500 ? 2 : 3
}

// Status and performance helpers  
const getStatusColor = (status) => {
  const colors = {
    online: '#22c55e',
    offline: '#ef4444', 
    training: '#3b82f6',
    processing: '#8b5cf6',
    error: '#ef4444',
    warning: '#f59e0b'
  }
  return colors[status] || '#6b7280'
}

const getStatusColorClass = (status) => {
  const classes = {
    online: 'bg-green-500',
    offline: 'bg-red-500',
    training: 'bg-blue-500',
    processing: 'bg-purple-500',
    error: 'bg-red-500', 
    warning: 'bg-yellow-500'
  }
  return classes[status] || 'bg-gray-500'
}

const getPerformanceColor = (performance) => {
  if (performance >= 80) return props.theme.success
  if (performance >= 60) return props.theme.warning
  return props.theme.danger
}

const getNodeTypeLabel = (type) => {
  const labels = {
    control: 'Control Node',
    edge: 'Edge Node', 
    gateway: 'Gateway',
    client: 'Client Device'
  }
  return labels[type] || type
}

// Pan and zoom handlers
const handlePanStart = (event) => {
  if (draggedNode.value) return // Don't pan if dragging a node
  
  isDragging.value = true
  dragStart.value = {
    x: event.clientX,
    y: event.clientY,
    viewBoxX: viewBox.value.x,
    viewBoxY: viewBox.value.y
  }
  event.preventDefault()
}

const handlePanMove = (event) => {
  if (!isDragging.value && !draggedNode.value) return
  
  if (isDragging.value) {
    const deltaX = (event.clientX - dragStart.value.x) * (viewBox.value.width / 800)
    const deltaY = (event.clientY - dragStart.value.y) * (viewBox.value.height / 500)
    
    viewBox.value.x = dragStart.value.viewBoxX - deltaX
    viewBox.value.y = dragStart.value.viewBoxY - deltaY
    
    emit('viewport-change', { ...viewBox.value })
  }
  
  if (draggedNode.value) {
    const rect = networkSvg.value.getBoundingClientRect()
    const x = ((event.clientX - rect.left) / rect.width) * viewBox.value.width + viewBox.value.x
    const y = ((event.clientY - rect.top) / rect.height) * viewBox.value.height + viewBox.value.y
    
    draggedNode.value.x = x
    draggedNode.value.y = y
  }
}

const handlePanEnd = () => {
  isDragging.value = false
  draggedNode.value = null
}

const handleZoom = (event) => {
  event.preventDefault()
  
  const scaleFactor = event.deltaY > 0 ? 1.1 : 0.9
  const rect = networkSvg.value.getBoundingClientRect()
  
  // Get mouse position in SVG coordinates
  const mouseX = ((event.clientX - rect.left) / rect.width) * viewBox.value.width + viewBox.value.x
  const mouseY = ((event.clientY - rect.top) / rect.height) * viewBox.value.height + viewBox.value.y
  
  // Calculate new viewBox
  const newWidth = viewBox.value.width * scaleFactor
  const newHeight = viewBox.value.height * scaleFactor
  
  viewBox.value = {
    x: mouseX - (mouseX - viewBox.value.x) * scaleFactor,
    y: mouseY - (mouseY - viewBox.value.y) * scaleFactor,
    width: Math.max(200, Math.min(2000, newWidth)),
    height: Math.max(125, Math.min(1250, newHeight))
  }
  
  emit('viewport-change', { ...viewBox.value })
}

// Node interaction handlers
const handleNodeClick = (node) => {
  selectedNode.value = selectedNode.value?.id === node.id ? null : node
  emit('node-click', node)
}

const handleNodeHover = (node, event) => {
  emit('node-hover', node, event)
}

const handleNodeLeave = (node) => {
  emit('node-leave', node)
}

const handleNodeDragStart = (node, event) => {
  draggedNode.value = node
  event.stopPropagation() // Prevent pan from starting
}

// Public methods for external control
const zoomToFit = () => {
  if (props.nodes.length === 0) return
  
  const padding = 50
  const minX = Math.min(...props.nodes.map(n => n.x)) - padding
  const maxX = Math.max(...props.nodes.map(n => n.x)) + padding  
  const minY = Math.min(...props.nodes.map(n => n.y)) - padding
  const maxY = Math.max(...props.nodes.map(n => n.y)) + padding
  
  viewBox.value = {
    x: minX,
    y: minY,
    width: maxX - minX,
    height: maxY - minY
  }
}

const resetZoom = () => {
  viewBox.value = { x: 0, y: 0, width: 800, height: 500 }
}

// Expose public methods
defineExpose({
  zoomToFit,
  resetZoom,
  selectedNode
})
</script>

<style scoped>
.edge-network-visualization {
  background: var(--color-background);
  overflow: hidden;
}

/* Node styling */
.node-circle {
  filter: drop-shadow(0 3px 6px rgba(0, 0, 0, 0.15));
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.node-circle:hover {
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.25));
  transform: scale(1.08);
}

.node-icon,
.node-label {
  pointer-events: none;
  user-select: none;
}

.node-label {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

/* Connection styling */
.connection-line {
  transition: all 0.3s ease;
}

.connection-line:hover {
  filter: drop-shadow(0 0 6px currentColor);
}

.connection-label {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

/* Cursor states */
.cursor-grab {
  cursor: grab;
}

.cursor-grabbing {
  cursor: grabbing;
}

/* Animations */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Smooth transitions */
.node-group {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Info panel transitions */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.95);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .node-label {
    font-size: 10px;
  }
  
  .connection-label {
    font-size: 8px;
  }
}
</style>