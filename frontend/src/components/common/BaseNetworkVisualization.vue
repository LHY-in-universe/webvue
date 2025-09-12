<template>
  <div class="base-network-visualization">
    <svg 
      ref="networkSvg"
      class="network-svg w-full h-full"
      :width="svgWidth"
      :height="svgHeight"
      :viewBox="`0 0 ${viewBoxWidth} ${viewBoxHeight}`"
      @mousedown="handleMouseDown"
      @mousemove="handleMouseMove"
      @mouseup="handleMouseUp"
      @mouseleave="handleMouseLeave"
      @wheel="handleWheel"
    >
      <!-- Base Definitions -->
      <defs>
        <!-- Grid Pattern -->
        <pattern 
          id="networkGrid" 
          width="50" 
          height="50" 
          patternUnits="userSpaceOnUse"
        >
          <path 
            d="M 50 0 L 0 0 0 50" 
            fill="none" 
            :stroke="themeStore.isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)'" 
            stroke-width="0.5"
          />
        </pattern>
        
        <!-- Data Flow Gradients -->
        <linearGradient id="dataFlowPrimary" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :style="`stop-color:${theme.primary};stop-opacity:0`" />
          <stop offset="50%" :style="`stop-color:${theme.primary};stop-opacity:1`" />
          <stop offset="100%" :style="`stop-color:${theme.primary};stop-opacity:0`" />
        </linearGradient>
        
        <linearGradient id="dataFlowSecondary" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :style="`stop-color:${theme.secondary};stop-opacity:0`" />
          <stop offset="50%" :style="`stop-color:${theme.secondary};stop-opacity:1`" />
          <stop offset="100%" :style="`stop-color:${theme.secondary};stop-opacity:0`" />
        </linearGradient>
        
        <!-- Filters -->
        <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="2" dy="2" stdDeviation="4" :flood-color="themeStore.isDark ? 'rgba(0,0,0,0.6)' : 'rgba(0,0,0,0.2)'" />
        </filter>
        
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        
        <!-- Node Gradients -->
        <radialGradient id="nodeGradient" cx="30%" cy="30%">
          <stop offset="0%" :style="`stop-color:${themeStore.isDark ? 'rgba(255,255,255,0.2)' : 'rgba(255,255,255,0.8)'};stop-opacity:1`" />
          <stop offset="100%" :style="`stop-color:${themeStore.isDark ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.1)'};stop-opacity:1`" />
        </radialGradient>
      </defs>
      
      <!-- Background Grid -->
      <rect width="100%" height="100%" fill="url(#networkGrid)" />
      
      <!-- Main Content Group with Transform -->
      <g :transform="svgTransform">
        <!-- Connections Layer -->
        <g class="connections-layer">
          <slot name="connections" :connections="visibleConnections" :theme="theme" />
        </g>
        
        <!-- Nodes Layer -->
        <g class="nodes-layer">
          <slot name="nodes" :nodes="visibleNodes" :theme="theme" />
        </g>
        
        <!-- Overlays Layer -->
        <g class="overlays-layer">
          <slot name="overlays" />
        </g>
      </g>
      
      <!-- UI Controls Overlay -->
      <g class="controls-overlay">
        <slot name="controls" />
      </g>
    </svg>
    
    <!-- Info Panel -->
    <Transition name="slide-up">
      <div
        v-if="showInfoPanel && selectedNode"
        class="absolute bottom-4 right-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-4 min-w-72 max-w-sm"
        :class="{ 'z-50': showInfoPanel }"
      >
        <slot name="info-panel" :node="selectedNode" :close="closeInfoPanel" />
      </div>
    </Transition>
    
    <!-- Mini Map -->
    <div
      v-if="showMiniMap"
      class="absolute top-4 right-4 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-lg border border-gray-200 dark:border-gray-700 p-2"
      :class="{ 'z-40': showMiniMap }"
    >
      <svg class="w-32 h-20" :viewBox="`0 0 ${viewBoxWidth} ${viewBoxHeight}`">
        <rect width="100%" height="100%" fill="url(#networkGrid)" opacity="0.3" />
        <g>
          <slot name="mini-map" :scale="miniMapScale" :nodes="visibleNodes" />
        </g>
        <!-- Viewport Indicator -->
        <rect
          :x="viewportIndicator.x"
          :y="viewportIndicator.y"
          :width="viewportIndicator.width"
          :height="viewportIndicator.height"
          fill="none"
          stroke="#3b82f6"
          stroke-width="2"
          opacity="0.6"
        />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
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
      accent: '#8b5cf6',
      warning: '#f59e0b',
      danger: '#ef4444'
    })
  },
  enableZoom: {
    type: Boolean,
    default: true
  },
  enablePan: {
    type: Boolean,
    default: true
  },
  enableMiniMap: {
    type: Boolean,
    default: true
  },
  autoLayout: {
    type: Boolean,
    default: false
  },
  layoutType: {
    type: String,
    default: 'force',
    validator: value => ['force', 'circular', 'hierarchical', 'grid'].includes(value)
  }
})

const emit = defineEmits(['node-click', 'node-hover', 'node-leave', 'connection-click', 'viewport-change'])

const themeStore = useThemeStore()
const networkSvg = ref(null)

// SVG Dimensions
const svgWidth = ref(props.width)
const svgHeight = ref(props.height)
const viewBoxWidth = ref(800)
const viewBoxHeight = ref(500)

// Transform State
const transform = ref({ x: 0, y: 0, scale: 1 })
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const lastMousePos = ref({ x: 0, y: 0 })

// Selection State
const selectedNode = ref(null)
const hoveredNode = ref(null)
const showInfoPanel = ref(false)

// UI State
const showMiniMap = computed(() => props.enableMiniMap)
const miniMapScale = ref(0.15)

// Computed Properties
const svgTransform = computed(() => {
  const { x, y, scale } = transform.value
  return `translate(${x}, ${y}) scale(${scale})`
})

const visibleNodes = computed(() => {
  return props.nodes.filter(node => node.visible !== false)
})

const visibleConnections = computed(() => {
  return props.connections.filter(connection => {
    const fromNode = visibleNodes.value.find(n => n.id === connection.from)
    const toNode = visibleNodes.value.find(n => n.id === connection.to)
    return fromNode && toNode
  })
})

const viewportIndicator = computed(() => {
  const scale = transform.value.scale
  const x = -transform.value.x / scale
  const y = -transform.value.y / scale
  const width = viewBoxWidth.value / scale
  const height = viewBoxHeight.value / scale
  
  return {
    x: Math.max(0, Math.min(x, viewBoxWidth.value - width)),
    y: Math.max(0, Math.min(y, viewBoxHeight.value - height)),
    width: Math.min(width, viewBoxWidth.value),
    height: Math.min(height, viewBoxHeight.value)
  }
})

// Event Handlers
const handleMouseDown = (event) => {
  if (!props.enablePan) return
  
  isDragging.value = true
  dragStart.value = { x: event.clientX, y: event.clientY }
  lastMousePos.value = { x: event.clientX, y: event.clientY }
  
  event.preventDefault()
}

const handleMouseMove = (event) => {
  if (!props.enablePan) return
  
  if (isDragging.value) {
    const deltaX = event.clientX - lastMousePos.value.x
    const deltaY = event.clientY - lastMousePos.value.y
    
    transform.value.x += deltaX
    transform.value.y += deltaY
    
    lastMousePos.value = { x: event.clientX, y: event.clientY }
    
    emit('viewport-change', { ...transform.value })
  }
}

const handleMouseUp = () => {
  isDragging.value = false
}

const handleMouseLeave = () => {
  isDragging.value = false
}

const handleWheel = (event) => {
  if (!props.enableZoom) return
  
  event.preventDefault()
  
  const rect = networkSvg.value.getBoundingClientRect()
  const mouseX = event.clientX - rect.left
  const mouseY = event.clientY - rect.top
  
  const scaleFactor = event.deltaY > 0 ? 0.9 : 1.1
  const newScale = Math.max(0.1, Math.min(5, transform.value.scale * scaleFactor))
  
  if (newScale !== transform.value.scale) {
    const scaleRatio = newScale / transform.value.scale
    
    transform.value.x = mouseX - (mouseX - transform.value.x) * scaleRatio
    transform.value.y = mouseY - (mouseY - transform.value.y) * scaleRatio
    transform.value.scale = newScale
    
    emit('viewport-change', { ...transform.value })
  }
}

// Public Methods
const zoomToFit = () => {
  if (visibleNodes.value.length === 0) return
  
  const bounds = getNodesBounds()
  const padding = 50
  
  const scaleX = (svgWidth.value - padding * 2) / bounds.width
  const scaleY = (svgHeight.value - padding * 2) / bounds.height
  const scale = Math.min(scaleX, scaleY, 1)
  
  transform.value = {
    x: (svgWidth.value - bounds.width * scale) / 2 - bounds.left * scale,
    y: (svgHeight.value - bounds.height * scale) / 2 - bounds.top * scale,
    scale
  }
  
  emit('viewport-change', { ...transform.value })
}

const zoomToNode = (nodeId) => {
  const node = visibleNodes.value.find(n => n.id === nodeId)
  if (!node) return
  
  const targetScale = 1.5
  const centerX = svgWidth.value / 2
  const centerY = svgHeight.value / 2
  
  transform.value = {
    x: centerX - node.x * targetScale,
    y: centerY - node.y * targetScale,
    scale: targetScale
  }
  
  emit('viewport-change', { ...transform.value })
}

const resetZoom = () => {
  transform.value = { x: 0, y: 0, scale: 1 }
  emit('viewport-change', { ...transform.value })
}

const selectNode = (node) => {
  selectedNode.value = node
  showInfoPanel.value = true
  emit('node-click', node)
}

const closeInfoPanel = () => {
  showInfoPanel.value = false
  selectedNode.value = null
}

// Helper Functions
const getNodesBounds = () => {
  if (visibleNodes.value.length === 0) {
    return { left: 0, top: 0, width: viewBoxWidth.value, height: viewBoxHeight.value }
  }
  
  let minX = Infinity, maxX = -Infinity
  let minY = Infinity, maxY = -Infinity
  
  visibleNodes.value.forEach(node => {
    minX = Math.min(minX, node.x || 0)
    maxX = Math.max(maxX, node.x || 0)
    minY = Math.min(minY, node.y || 0)
    maxY = Math.max(maxY, node.y || 0)
  })
  
  return {
    left: minX,
    top: minY,
    width: maxX - minX,
    height: maxY - minY
  }
}

// Resize Handler
const handleResize = () => {
  if (networkSvg.value) {
    const rect = networkSvg.value.parentElement.getBoundingClientRect()
    svgWidth.value = rect.width
    svgHeight.value = rect.height
  }
}

// Lifecycle
onMounted(() => {
  nextTick(() => {
    handleResize()
    if (props.autoLayout) {
      zoomToFit()
    }
  })
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// Watchers
watch(() => props.nodes, () => {
  if (props.autoLayout) {
    nextTick(() => {
      zoomToFit()
    })
  }
}, { deep: true })

// Expose public methods
defineExpose({
  zoomToFit,
  zoomToNode,
  resetZoom,
  selectNode,
  closeInfoPanel
})
</script>

<style scoped>
.base-network-visualization {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--color-background);
  border-radius: 0.5rem;
}

.network-svg {
  cursor: grab;
  user-select: none;
}

.network-svg:active {
  cursor: grabbing;
}

/* Transition Styles */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Layer Styles */
.connections-layer {
  pointer-events: none;
}

.nodes-layer {
  pointer-events: all;
}

.overlays-layer {
  pointer-events: none;
}

.controls-overlay {
  pointer-events: all;
}
</style>