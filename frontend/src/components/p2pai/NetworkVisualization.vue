<template>
  <div class="network-visualization">
    <svg 
      ref="networkSvg"
      class="node-svg"
      :width="svgWidth"
      :height="svgHeight"
      viewBox="0 0 800 500"
      @mousedown="handleMouseDown"
      @mouseup="handleMouseUp"
      @mouseleave="handleMouseLeave"
      @wheel="handleWheel"
    >
      <!-- 背景网格 -->
      <defs>
        <pattern 
          id="grid" 
          width="50" 
          height="50" 
          patternUnits="userSpaceOnUse"
        >
          <path 
            d="M 50 0 L 0 0 0 50" 
            fill="none" 
            :stroke="gridColor" 
            stroke-width="0.5" 
            opacity="0.1"
          />
        </pattern>
        
        <!-- 数据流动画渐变 - 不同类型 -->
        <linearGradient id="dataFlowBlue" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:0" />
          <stop offset="50%" style="stop-color:#3b82f6;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:0" />
        </linearGradient>
        
        <linearGradient id="dataFlowGreen" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#10b981;stop-opacity:0" />
          <stop offset="50%" style="stop-color:#10b981;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#10b981;stop-opacity:0" />
        </linearGradient>
        
        <linearGradient id="dataFlowPurple" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#8b5cf6;stop-opacity:0" />
          <stop offset="50%" style="stop-color:#8b5cf6;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:0" />
        </linearGradient>
        
        <!-- 阴影滤镜 -->
        <filter id="dropshadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="2" dy="2" stdDeviation="4" flood-color="rgba(0,0,0,0.4)" />
        </filter>
        
        <!-- 发光滤镜 -->
        <filter id="glow">
          <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        
        <!-- 节点渐变效果 -->
        <radialGradient id="nodeGradient" cx="30%" cy="30%">
          <stop offset="0%" style="stop-color:rgba(255,255,255,0.3);stop-opacity:1" />
          <stop offset="100%" style="stop-color:rgba(0,0,0,0.1);stop-opacity:1" />
        </radialGradient>
        
        <!-- 控制节点特殊效果 -->
        <radialGradient id="controlNodeGradient" cx="25%" cy="25%">
          <stop offset="0%" style="stop-color:rgba(255,255,255,0.4);stop-opacity:1" />
          <stop offset="70%" style="stop-color:rgba(255,255,255,0.1);stop-opacity:1" />
          <stop offset="100%" style="stop-color:rgba(0,0,0,0.2);stop-opacity:1" />
        </radialGradient>
      </defs>
      
      <!-- 背景网格 -->
      <rect width="100%" height="100%" fill="url(#grid)" />
      
      <!-- 可缩放和平移的主内容组 -->
      <g :transform="svgTransform">
      
      <!-- 连接线层 -->
      <g id="connections">
        <g 
          v-for="connection in visibleConnections" 
          :key="`${connection.from}-${connection.to}`"
          class="connection-group"
        >
          <!-- 基础连接线 -->
          <line
            :x1="getNodePosition(connection.from).x"
            :y1="getNodePosition(connection.from).y"
            :x2="getNodePosition(connection.to).x"
            :y2="getNodePosition(connection.to).y"
            class="connection-line"
            :class="{ 'active': connection.active }"
            stroke="rgba(156, 163, 175, 0.1)"
            stroke-width="1"
            stroke-opacity="1"
          />
          
          <!-- 连接线悬停区域（增加悬停响应区域） -->
          <line
            :x1="getNodePosition(connection.from).x"
            :y1="getNodePosition(connection.from).y"
            :x2="getNodePosition(connection.to).x"
            :y2="getNodePosition(connection.to).y"
            stroke="transparent"
            stroke-width="8"
            style="cursor: pointer;"
            @mouseenter="handleConnectionHover(connection, $event)"
            @mouseleave="handleConnectionLeave"
          />
          
          <!-- 数据流动画线段 -->
          <line
            v-if="connection.active && trainingActive && shouldShowAnimation"
            :x1="getNodePosition(connection.from).x"
            :y1="getNodePosition(connection.from).y"
            :x2="getNodePosition(connection.to).x"
            :y2="getNodePosition(connection.to).y"
            :stroke="getDataFlowColor(connection)"
            stroke-width="2.5"
            stroke-linecap="round"
            class="data-flow-line"
          >
            <animate
              attributeName="stroke-dasharray"
              :values="isLargeNetwork ? '0,1000;20,980;0,1000' : '0,1000;40,960;0,1000'"
              :dur="isLargeNetwork ? '3s' : '1.8s'"
              repeatCount="indefinite"
            />
            <animate
              attributeName="stroke-dashoffset"
              values="1000;0;-1000"
              :dur="isLargeNetwork ? '3s' : '1.8s'"
              repeatCount="indefinite"
            />
          </line>
          
          <!-- 静态连接线（大型网络时显示） -->
          <line
            v-if="connection.active && trainingActive && !shouldShowAnimation"
            :x1="getNodePosition(connection.from).x"
            :y1="getNodePosition(connection.from).y"
            :x2="getNodePosition(connection.to).x"
            :y2="getNodePosition(connection.to).y"
            :stroke="getDataFlowColor(connection)"
            stroke-width="2"
            stroke-linecap="round"
            opacity="0.6"
          />
        </g>
      </g>
      
      <!-- MPC隐私保护：隐藏参与方占位符（仅显示虚影圆圈，不显示图标） -->
      <g v-if="projectType === 'mpc'" id="hiddenParties">
        <g 
          v-for="(position, index) in LAYOUT_CONFIGS.mpc.hidden" 
          :key="`hidden-${index}`"
          class="hidden-party-group"
        >
          <!-- 隐藏节点的虚影 -->
          <circle
            :cx="position.x"
            :cy="position.y"
            :r="18"
            fill="none"
            :stroke="themeStore.isDark ? '#374151' : '#d1d5db'"
            stroke-width="2"
            stroke-dasharray="5,5"
            opacity="0.5"
          >
            <!-- 虚化动画 -->
            <animate
              attributeName="opacity"
              values="0.3;0.6;0.3"
              dur="3s"
              repeatCount="indefinite"
            />
          </circle>
        </g>
      </g>

      <!-- 节点层 -->
      <g id="nodes">
        <g 
          v-for="node in visibleNodes" 
          :key="node.id"
          class="node-group"
          style="cursor: pointer;"
        >
          <!-- 主节点圆形 -->
          <circle
            :cx="getNodePosition(node.id).x"
            :cy="getNodePosition(node.id).y"
            :r="getNodeRadius(node)"
            :fill="getNodeFillColor(node)"
            :stroke="getNodeStrokeColor(node)"
            :stroke-width="getNodeStrokeWidth(node)"
            :class="getNodeClasses(node)"
            style="cursor: pointer; opacity: 1;"
            filter="url(#dropshadow)"
            @click="handleNodeClick(node)"
            @mouseenter="handleNodeHover(node)"
          />
          
          <!-- 节点渐变覆盖层 -->
          <circle
            :cx="getNodePosition(node.id).x"
            :cy="getNodePosition(node.id).y"
            :r="getNodeRadius(node)"
            :fill="node.type === 'control' ? 'url(#controlNodeGradient)' : 'url(#nodeGradient)'"
            style="pointer-events: none;"
          />
          
          <!-- 训练进度环（仅边缘节点） -->
          <circle
            v-if="node.type === 'edge' && node.status === 'training' && node.progress"
            :cx="getNodePosition(node.id).x"
            :cy="getNodePosition(node.id).y"
            :r="getNodeRadius(node) + 8"
            fill="none"
            :stroke="node.strokeColor"
            stroke-width="3"
            opacity="0.3"
            :stroke-dasharray="getProgressDashArray(node)"
            :stroke-dashoffset="getProgressDashOffset(node)"
            style="transition: all 0.5s ease;"
            transform="rotate(-90)"
          />
          
          <!-- 自己设备的脉搏外环 - 只有自己的设备才有 -->
          <circle
            v-if="node.isOwn"
            :cx="getNodePosition(node.id).x"
            :cy="getNodePosition(node.id).y"
            :r="getNodeRadius(node) + 5"
            fill="none"
            :stroke="getNodeStrokeColor(node)"
            stroke-width="2"
            opacity="0.6"
            class="own-device-pulse"
          >
            <animate
              attributeName="r"
              :values="`${getNodeRadius(node) + 3};${getNodeRadius(node) + 8};${getNodeRadius(node) + 3}`"
              dur="2s"
              repeatCount="indefinite"
            />
            <animate
              attributeName="opacity"
              values="0.6;0.2;0.6"
              dur="2s"
              repeatCount="indefinite"
            />
          </circle>

          <!-- 节点状态指示器 - 只有训练中的其他节点才显示 -->
          <circle
            v-if="node.status === 'training' && !node.isOwn"
            :r="4"
            :cx="getNodePosition(node.id).x + getNodeRadius(node) - 8"
            :cy="getNodePosition(node.id).y - getNodeRadius(node) + 8"
            fill="#10b981"
            class="status-indicator"
          >
            <animate
              attributeName="r"
              values="3;5;3"
              dur="1.5s"
              repeatCount="indefinite"
            />
          </circle>
          
          <!-- 离线状态指示器 - 只有其他节点离线时才显示 -->
          <circle
            v-if="node.status === 'offline' && !node.isOwn"
            :r="4"
            :cx="getNodePosition(node.id).x + getNodeRadius(node) - 8"
            :cy="getNodePosition(node.id).y - getNodeRadius(node) + 8"
            fill="#ef4444"
            opacity="0.7"
          />
          
          <!-- 节点内部图标 - 使用专业的HeroIcons -->
          <g :transform="`translate(${getNodePosition(node.id).x}, ${getNodePosition(node.id).y})`">
            <!-- 控制节点/服务器图标 -->
            <foreignObject
              v-if="node.type === 'control'"
              x="-12"
              y="-12"
              width="24"
              height="24"
              style="pointer-events: none;"
            >
              <ServerIcon 
                class="w-6 h-6 text-white drop-shadow-sm"
                :class="themeStore.isDark ? 'text-white' : 'text-white'"
              />
            </foreignObject>
            
            <!-- 边缘节点图标 -->
            <foreignObject
              v-if="node.type === 'edge'"
              x="-10"
              y="-10"
              width="20"
              height="20"
              style="pointer-events: none;"
            >
              <CpuChipIcon 
                v-if="node.isOwn"
                class="w-5 h-5 text-white drop-shadow-sm font-bold"
                stroke-width="2.5"
              />
              <ComputerDesktopIcon 
                v-else
                class="w-5 h-5 text-white drop-shadow-sm"
              />
            </foreignObject>
          </g>
        </g>
      </g>
      
      <!-- 标签层 -->
      <g id="labels">
        <g 
          v-for="node in visibleNodes" 
          :key="`label-${node.id}`"
          class="node-label-group"
        >
          <!-- 标签背景 -->
          <rect
            :x="getNodePosition(node.id).x - getTextWidth(node.name) / 2 - 8"
            :y="getNodePosition(node.id).y + getNodeRadius(node) + 15"
            :width="getTextWidth(node.name) + 16"
            height="24"
            rx="12"
            :fill="labelBackgroundColor"
            opacity="0.9"
          />
          
          <!-- 节点名称标签 -->
          <text
            :x="getNodePosition(node.id).x"
            :y="getNodePosition(node.id).y + getNodeRadius(node) + 30"
            text-anchor="middle"
            :class="labelTextClasses"
            font-size="12"
            font-weight="500"
          >
            {{ node.name }}
          </text>
          
          <!-- 训练进度文本（边缘节点） -->
          <text
            v-if="node.type === 'edge' && node.status === 'training' && node.progress"
            :x="getNodePosition(node.id).x"
            :y="getNodePosition(node.id).y + getNodeRadius(node) + 45"
            text-anchor="middle"
            :class="progressTextClasses"
            font-size="10"
          >
            {{ Math.round(node.progress) }}%
          </text>
        </g>
      </g>
      
      <!-- 训练完成状态覆盖层 -->
      <g 
        v-if="showTrainingComplete"
        id="trainingComplete"
        class="training-complete-overlay"
      >
        <!-- 背景遮罩 -->
        <rect 
          width="100%" 
          height="100%" 
          fill="rgba(16, 185, 129, 0.1)" 
          rx="10"
        />
        
        <!-- 完成状态文字 -->
        <text 
          x="50%" 
          y="40%" 
          text-anchor="middle" 
          class="training-complete-title"
          font-size="24"
          font-weight="bold"
          :fill="titleTextColor"
        >
          🎉 Training Complete 🎉
        </text>
        
        <text 
          x="50%" 
          y="50%" 
          text-anchor="middle" 
          class="training-complete-subtitle"
          font-size="16"
          :fill="subtitleTextColor"
        >
          All edge nodes have completed training tasks
        </text>
        
        <text 
          x="50%" 
          y="60%" 
          text-anchor="middle" 
          class="training-complete-details"
          font-size="14"
          :fill="detailTextColor"
        >
          Average Accuracy: {{ averageAccuracy.toFixed(1) }}% | Total Training Time: {{ formatTrainingTime() }}
        </text>
      </g>
      </g>
    </svg>
    
    
    <!-- 性能优化提示 -->
    <div 
      v-if="isLargeNetwork && hiddenNodesCount > 0"
      class="performance-notice"
    >
      <div class="flex items-center space-x-2 text-sm text-amber-600 dark:text-amber-400">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
        <span>
          Large network detected: Showing {{ visibleNodes.length }}/{{ nodes.length }} nodes 
          ({{ hiddenNodesCount }} hidden for performance)
        </span>
      </div>
    </div>
    
    <!-- 节点悬停工具提示 -->
    <div
      v-if="hoveredNode && showTooltip"
      ref="tooltip"
      class="node-tooltip"
      :style="tooltipStyle"
    >
      <div class="tooltip-content">
        <div class="font-semibold text-gray-900 dark:text-white flex items-center">
          <span class="mr-2">
            {{ hoveredNode.type === 'control' ? '🖥️' : (hoveredNode.isOwn ? '💻' : '📱') }}
          </span>
          {{ hoveredNode.name }}
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400">
          {{ getNodeTypeLabel(hoveredNode) }}
        </div>
        <div v-if="hoveredNode.isOwn" class="text-xs text-blue-600 dark:text-blue-400 mt-1 font-medium">
          🔒 Your Device
        </div>
        <div class="text-xs text-gray-500 dark:text-gray-500 mt-1">
          Status: {{ hoveredNode.status || 'Online' }}
        </div>
        <div v-if="hoveredNode.progress" class="text-xs text-gray-500 dark:text-gray-500">
          Training Progress: {{ Math.round(hoveredNode.progress) }}%
        </div>
      </div>
    </div>
    
    <!-- 连接线悬停工具提示 -->
    <div
      v-if="hoveredConnection && showConnectionTooltip"
      ref="connectionTooltip"
      class="connection-tooltip"
      :style="connectionTooltipStyle"
    >
      <div class="tooltip-content">
        <div class="font-semibold text-gray-900 dark:text-white mb-2">
          Connection Info
        </div>
        <div class="text-sm text-gray-600 dark:text-gray-400">
          <div class="flex justify-between items-center mb-1">
            <span>From:</span>
            <span class="font-medium">{{ getNodeName(hoveredConnection.from) }}</span>
          </div>
          <div class="flex justify-between items-center mb-1">
            <span>To:</span>
            <span class="font-medium">{{ getNodeName(hoveredConnection.to) }}</span>
          </div>
          <div class="flex justify-between items-center mb-1">
            <span>Status:</span>
            <span :class="hoveredConnection.active ? 'text-green-500' : 'text-gray-500'">
              {{ hoveredConnection.active ? 'Active' : 'Inactive' }}
            </span>
          </div>
          <div v-if="hoveredConnection.active" class="flex justify-between items-center mb-1">
            <span>Bandwidth:</span>
            <span class="font-medium text-blue-500">{{ getConnectionBandwidth(hoveredConnection) }}</span>
          </div>
          <div v-if="hoveredConnection.active" class="flex justify-between items-center">
            <span>Latency:</span>
            <span class="font-medium text-purple-500">{{ getConnectionLatency(hoveredConnection) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import {
  ServerIcon,
  ComputerDesktopIcon,
  CpuChipIcon
} from '@heroicons/vue/24/outline'

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
    default: 30 // 最大节点数量限制
  },
  enableVirtualization: {
    type: Boolean,
    default: false // 启用虚拟化渲染
  },
  projectType: {
    type: String,
    default: 'federated', // federated 或 mpc
    validator: value => ['federated', 'mpc'].includes(value)
  }
})

const emit = defineEmits(['node-click', 'node-hover'])

const themeStore = useThemeStore()

// 响应式数据
const networkSvg = ref(null)
const tooltip = ref(null)
const hoveredNode = ref(null)
const hoveredConnection = ref(null)
const showTooltip = ref(false)
const showConnectionTooltip = ref(false)
const tooltipPosition = ref({ x: 0, y: 0 })
const connectionTooltipPosition = ref({ x: 0, y: 0 })

// 缩放和平移相关
const zoomLevel = ref(1)
const panOffset = ref({ x: 0, y: 0 })
const isDragging = ref(false)
const lastMousePosition = ref({ x: 0, y: 0 })
const minZoom = 0.3
const maxZoom = 3

// 智能布局配置 - 借鉴EdgeAI的布局系统
const LAYOUT_CONFIGS = {
  federated: {
    // 联邦学习：星形拓扑，中央服务器在上方，边缘设备围绕分布
    control: [
      { x: 400, y: 120 }  // 中央服务器位置
    ],
    edge: [
      { x: 200, y: 300 },  // 左侧边缘设备
      { x: 400, y: 380 },  // 中央边缘设备
      { x: 600, y: 300 },  // 右侧边缘设备
      { x: 150, y: 200 },  // 左上边缘设备
      { x: 650, y: 200 }   // 右上边缘设备
    ]
  },
  mpc: {
    // MPC：紧凑布局，体现隐私保护
    edge: [
      { x: 400, y: 250 }   // 本地设备居中
    ],
    hidden: [
      // 隐藏参与方的占位符位置
      { x: 300, y: 180 },
      { x: 500, y: 180 },
      { x: 350, y: 320 },
      { x: 450, y: 320 }
    ]
  }
}

// 节点位置追踪
const nodePositions = ref(new Map())

// SVG 尺寸
const svgWidth = ref(800)
const svgHeight = ref(500)

// 计算属性
const gridColor = computed(() => 
  themeStore.isDark ? '#374151' : '#e5e7eb'
)

const labelBackgroundColor = computed(() => 
  themeStore.isDark ? 'rgba(31, 41, 55, 0.9)' : 'rgba(255, 255, 255, 0.9)'
)

const labelTextClasses = computed(() => 
  themeStore.isDark ? 'fill-gray-200' : 'fill-gray-800'
)

const progressTextClasses = computed(() => 
  themeStore.isDark ? 'fill-gray-400' : 'fill-gray-600'
)

const titleTextColor = computed(() => 
  themeStore.isDark ? '#10b981' : '#047857'
)

const subtitleTextColor = computed(() => 
  themeStore.isDark ? '#d1d5db' : '#374151'
)

const detailTextColor = computed(() => 
  themeStore.isDark ? '#9ca3af' : '#6b7280'
)

const averageAccuracy = computed(() => {
  const edgeNodes = props.nodes.filter(n => n.type === 'edge' && n.accuracy)
  if (edgeNodes.length === 0) return 0
  return edgeNodes.reduce((sum, n) => sum + n.accuracy, 0) / edgeNodes.length
})

const tooltipStyle = computed(() => ({
  left: `${tooltipPosition.value.x}px`,
  top: `${tooltipPosition.value.y}px`,
  transform: 'translate(-50%, -100%)',
  pointerEvents: 'none'
}))

const connectionTooltipStyle = computed(() => ({
  left: `${connectionTooltipPosition.value.x}px`,
  top: `${connectionTooltipPosition.value.y}px`,
  transform: 'translate(-50%, -100%)',
  pointerEvents: 'none'
}))

// 性能优化相关计算属性
const isLargeNetwork = computed(() => props.nodes.length > props.maxNodes)

// 进行节点过滤和虚拟化的节点列表
const visibleNodes = computed(() => {
  if (!isLargeNetwork.value) {
    return props.nodes
  }
  
  // 大型网络优先级策略：
  // 1. 显示所有控制节点
  // 2. 显示自己的节点
  // 3. 显示部分活跃的边缘节点
  const controlNodes = props.nodes.filter(n => n.type === 'control')
  const ownNodes = props.nodes.filter(n => n.isOwn && n.type !== 'control')
  const otherActiveNodes = props.nodes
    .filter(n => !n.isOwn && n.type !== 'control' && n.status !== 'offline')
    .sort((a, b) => (b.progress || 0) - (a.progress || 0))
    .slice(0, Math.max(0, props.maxNodes - controlNodes.length - ownNodes.length))
    
  return [...controlNodes, ...ownNodes, ...otherActiveNodes]
})

// 可见连接（只显示与可见节点相关的连接）
const visibleConnections = computed(() => {
  const visibleNodeIds = new Set(visibleNodes.value.map(n => n.id))
  return props.connections.filter(conn => 
    visibleNodeIds.has(conn.from) && visibleNodeIds.has(conn.to)
  )
})

// 隐藏节点数量统计
const hiddenNodesCount = computed(() => 
  Math.max(0, props.nodes.length - visibleNodes.value.length)
)

// 动画性能优化：大型网络时减少动画
const shouldShowAnimation = computed(() => {
  return !isLargeNetwork.value || props.enableVirtualization
})

// SVG 变换属性
const svgTransform = computed(() => {
  return `translate(${panOffset.value.x}, ${panOffset.value.y}) scale(${zoomLevel.value})`
})

// 缩放控制
const zoomIn = () => {
  zoomLevel.value = Math.min(maxZoom, zoomLevel.value * 1.2)
}

const zoomOut = () => {
  zoomLevel.value = Math.max(minZoom, zoomLevel.value / 1.2)
}

const resetView = () => {
  zoomLevel.value = 1
  panOffset.value = { x: 0, y: 0 }
}

// 鼠标事件处理
const handleMouseDown = (event) => {
  if (event.button === 0) { // 左键
    isDragging.value = true
    lastMousePosition.value = { x: event.clientX, y: event.clientY }
    event.preventDefault()
  }
}

const handleMouseMove = (event) => {
  if (isDragging.value) {
    const deltaX = event.clientX - lastMousePosition.value.x
    const deltaY = event.clientY - lastMousePosition.value.y
    
    panOffset.value.x += deltaX
    panOffset.value.y += deltaY
    
    lastMousePosition.value = { x: event.clientX, y: event.clientY }
    event.preventDefault()
  }
}

const handleMouseUp = () => {
  isDragging.value = false
}

const handleWheel = (event) => {
  event.preventDefault()
  const delta = event.deltaY > 0 ? 0.9 : 1.1
  const newZoom = Math.max(minZoom, Math.min(maxZoom, zoomLevel.value * delta))
  
  if (newZoom !== zoomLevel.value) {
    // 以鼠标位置为中心缩放
    const rect = networkSvg.value.getBoundingClientRect()
    const mouseX = event.clientX - rect.left
    const mouseY = event.clientY - rect.top
    
    const scaleDiff = newZoom / zoomLevel.value
    panOffset.value.x = mouseX - (mouseX - panOffset.value.x) * scaleDiff
    panOffset.value.y = mouseY - (mouseY - panOffset.value.y) * scaleDiff
    
    zoomLevel.value = newZoom
  }
}

// 智能位置分配函数 - 借鉴EdgeAI系统
const getStablePositionIndex = (nodeId, nodeType) => {
  if (nodeType === 'control') {
    // 控制节点稳定分配
    if (nodeId.includes('server')) return 0
    if (nodeId.includes('control')) return 1
    return 0
  } else if (nodeType === 'edge') {
    // 边缘节点基于ID稳定分配位置
    const match = nodeId.match(/(\d+)/)
    if (match) {
      const nodeNumber = parseInt(match[1])
      const layoutConfig = LAYOUT_CONFIGS[props.projectType]
      const edgePositions = layoutConfig?.edge || []
      return (nodeNumber - 1) % edgePositions.length
    }
  }
  return 0
}

// 初始化节点位置
const initializeNodePositions = () => {
  const layoutConfig = LAYOUT_CONFIGS[props.projectType]
  if (!layoutConfig) return
  
  props.nodes.forEach((node, index) => {
    // 跳过已有位置的节点
    if (nodePositions.value.has(node.id)) return
    
    let position = null
    
    if (node.type === 'control' && layoutConfig.control) {
      const positionIndex = getStablePositionIndex(node.id, node.type)
      position = layoutConfig.control[positionIndex] || layoutConfig.control[0]
    } else if (node.type === 'edge' && layoutConfig.edge) {
      const positionIndex = getStablePositionIndex(node.id, node.type)
      position = layoutConfig.edge[positionIndex] || layoutConfig.edge[0]
    }
    
    if (position) {
      nodePositions.value.set(node.id, { ...position })
    }
  })
}

// 获取节点位置 - 优先使用智能布局，回退到原坐标
const getNodePosition = (nodeId) => {
  const node = props.nodes.find(n => n.id === nodeId)
  if (!node) return { x: 0, y: 0 }
  
  // 优先从位置缓存获取
  const cachedPosition = nodePositions.value.get(nodeId)
  if (cachedPosition) {
    return { ...cachedPosition }
  }
  
  // 如果节点有原始坐标，使用原始坐标
  if (node.x !== undefined && node.y !== undefined) {
    return { x: node.x, y: node.y }
  }
  
  // 否则使用布局系统分配位置
  const layoutConfig = LAYOUT_CONFIGS[props.projectType]
  if (layoutConfig) {
    let position = null
    
    if (node.type === 'control' && layoutConfig.control) {
      const positionIndex = getStablePositionIndex(nodeId, node.type)
      position = layoutConfig.control[positionIndex] || layoutConfig.control[0]
    } else if (node.type === 'edge' && layoutConfig.edge) {
      const positionIndex = getStablePositionIndex(nodeId, node.type)
      position = layoutConfig.edge[positionIndex] || layoutConfig.edge[0]
    }
    
    if (position) {
      // 缓存位置
      nodePositions.value.set(nodeId, { ...position })
      return { ...position }
    }
  }
  
  // 最后回退到默认位置
  return { x: 400, y: 250 }
}

const getNodeRadius = (node) => {
  if (node.type === 'control') {
    return 30 // 服务器节点更大
  }
  return node.isOwn ? 22 : 20 // 自己的设备稍大
}

const getNodeFillColor = (node) => {
  if (node.type === 'control') {
    // 控制节点/服务器 - 红色系
    return themeStore.isDark ? '#ef4444' : '#dc2626'
  } else if (node.type === 'edge') {
    if (node.isOwn) {
      // 自己的设备 - 蓝色系，更鲜艳
      return themeStore.isDark ? '#3b82f6' : '#2563eb'
    } else {
      // 其他边缘设备 - 绿色系
      return themeStore.isDark ? '#10b981' : '#059669'
    }
  }
  return '#6b7280' // 默认灰色
}

const getNodeStrokeColor = (node) => {
  if (node.type === 'control') {
    return themeStore.isDark ? '#fca5a5' : '#b91c1c'
  } else if (node.type === 'edge') {
    if (node.isOwn) {
      // 自己的设备有特殊边框
      return themeStore.isDark ? '#60a5fa' : '#1d4ed8'
    } else {
      return themeStore.isDark ? '#34d399' : '#047857'
    }
  }
  return '#4b5563'
}

const getNodeStrokeWidth = (node) => {
  if (node.isOwn) return 3 // 自己的设备边框更粗
  if (node.type === 'control') return 2.5 // 控制节点稍粗
  if (node.status === 'offline') return 2
  return 2
}

const getNodeClasses = (node) => {
  const classes = ['node-element']
  
  if (node.type === 'control') {
    classes.push('control-node')
  } else {
    classes.push('edge-node')
    
    if (node.isOwn) {
      classes.push('own-node')
    } else if (node.status === 'offline') {
      classes.push('other-offline')
    } else {
      classes.push('other-online')
    }
  }
  
  return classes.join(' ')
}

const getProgressDashArray = (node) => {
  const radius = getNodeRadius(node) + 8
  const circumference = 2 * Math.PI * radius
  return `${circumference * (node.progress / 100)}, ${circumference}`
}

const getProgressDashOffset = (node) => {
  const radius = getNodeRadius(node) + 8
  const circumference = 2 * Math.PI * radius
  return circumference - (circumference * (node.progress / 100))
}

const getTextWidth = (text) => {
  // 简单的文本宽度估算
  return text.length * 7
}

const getNodeTypeLabel = (node) => {
  if (node.type === 'control') {
    return 'Central Server'
  } else if (node.type === 'edge') {
    if (node.isOwn) {
      return 'Your Training Device'
    } else {
      return 'Remote Edge Device'
    }
  }
  return 'Network Node'
}

const handleNodeClick = (node) => {
  emit('node-click', node)
}

const handleNodeHover = async (node) => {
  hoveredNode.value = node
  showTooltip.value = true
  
  // 等待DOM更新后计算工具提示位置
  await nextTick()
  
  if (networkSvg.value) {
    const rect = networkSvg.value.getBoundingClientRect()
    const nodePos = getNodePosition(node.id)
    tooltipPosition.value = {
      x: rect.left + nodePos.x,
      y: rect.top + nodePos.y - getNodeRadius(node) - 10
    }
  }
  
  emit('node-hover', node)
}

const handleMouseLeave = () => {
  isDragging.value = false // 停止拖拽
  showTooltip.value = false
  hoveredNode.value = null
  showConnectionTooltip.value = false
  hoveredConnection.value = null
  emit('node-hover', null)
}

// 连接线悬停处理
const handleConnectionHover = async (connection, event) => {
  hoveredConnection.value = connection
  showConnectionTooltip.value = true
  
  // 计算连接线的中点位置
  const fromPos = getNodePosition(connection.from)
  const toPos = getNodePosition(connection.to)
  const midX = (fromPos.x + toPos.x) / 2
  const midY = (fromPos.y + toPos.y) / 2
  
  // 等待DOM更新后计算工具提示位置
  await nextTick()
  
  if (networkSvg.value) {
    const rect = networkSvg.value.getBoundingClientRect()
    connectionTooltipPosition.value = {
      x: rect.left + (midX * zoomLevel.value) + panOffset.value.x,
      y: rect.top + (midY * zoomLevel.value) + panOffset.value.y - 10
    }
  }
}

const handleConnectionLeave = () => {
  showConnectionTooltip.value = false
  hoveredConnection.value = null
}

// 获取节点名称
const getNodeName = (nodeId) => {
  const node = props.nodes.find(n => n.id === nodeId)
  return node ? node.name : nodeId
}

// 获取连接带宽（模拟数据）
const getConnectionBandwidth = (connection) => {
  const fromNode = props.nodes.find(n => n.id === connection.from)
  const toNode = props.nodes.find(n => n.id === connection.to)
  
  // 控制节点间的连接带宽更高
  if (fromNode?.type === 'control' && toNode?.type === 'control') {
    return `${(Math.random() * 500 + 800).toFixed(0)} Mbps`
  }
  // 控制节点到边缘节点的连接
  if (fromNode?.type === 'control' || toNode?.type === 'control') {
    return `${(Math.random() * 200 + 300).toFixed(0)} Mbps`
  }
  // 边缘节点间的连接
  return `${(Math.random() * 100 + 100).toFixed(0)} Mbps`
}

// 获取连接延迟（模拟数据）
const getConnectionLatency = (connection) => {
  const fromNode = props.nodes.find(n => n.id === connection.from)
  const toNode = props.nodes.find(n => n.id === connection.to)
  
  // 控制节点间的延迟更低
  if (fromNode?.type === 'control' && toNode?.type === 'control') {
    return `${(Math.random() * 5 + 1).toFixed(1)} ms`
  }
  // 控制节点到边缘节点的延迟
  if (fromNode?.type === 'control' || toNode?.type === 'control') {
    return `${(Math.random() * 20 + 10).toFixed(1)} ms`
  }
  // 边缘节点间的延迟
  return `${(Math.random() * 50 + 20).toFixed(1)} ms`
}

const formatTrainingTime = () => {
  // 模拟训练时间
  const minutes = 45
  const seconds = 32
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

// 根据连接类型获取数据流颜色
const getDataFlowColor = (connection) => {
  const fromNode = props.nodes.find(n => n.id === connection.from)
  const toNode = props.nodes.find(n => n.id === connection.to)
  
  // 控制节点之间的连接使用紫色
  if (fromNode?.type === 'control' && toNode?.type === 'control') {
    return 'url(#dataFlowPurple)'
  }
  // 控制节点到边缘节点使用蓝色
  if (fromNode?.type === 'control' || toNode?.type === 'control') {
    return 'url(#dataFlowBlue)'
  }
  // 边缘节点之间使用绿色
  return 'url(#dataFlowGreen)'
}

// 监听主题变化
watch(
  () => themeStore.isDark,
  () => {
    // 主题变化时的处理逻辑
  }
)

// 监听节点变化，重新初始化位置
watch(
  () => props.nodes.length,
  () => {
    initializeNodePositions()
  },
  { immediate: true }
)

// 监听项目类型变化，清除缓存并重新布局
watch(
  () => props.projectType,
  () => {
    nodePositions.value.clear()
    initializeNodePositions()
  }
)

// 添加全局鼠标事件监听器
onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
  
  // 初始化节点位置
  initializeNodePositions()
  
  // 添加快捷键事件监听器
  const container = networkSvg.value?.closest('.network-visualization-container')
  if (container) {
    container.addEventListener('resetView', resetView)
    container.addEventListener('zoomIn', zoomIn)
    container.addEventListener('zoomOut', zoomOut)
  }
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
  
  // 清理快捷键事件监听器
  const container = networkSvg.value?.closest('.network-visualization-container')
  if (container) {
    container.removeEventListener('resetView', resetView)
    container.removeEventListener('zoomIn', zoomIn)
    container.removeEventListener('zoomOut', zoomOut)
  }
})
</script>

<style scoped>
.network-visualization {
  width: 100%;
  height: 100%;
  position: relative;
}

.node-svg {
  width: 100%;
  height: 500px;
  max-height: 500px;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  overflow: hidden;
  border: 1px solid rgba(156, 163, 175, 0.2);
  cursor: grab;
}

.node-svg:active {
  cursor: grabbing;
}

/* 节点样式 */
.control-node {
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-node:hover {
  /* Removed movement effects - keeping only subtle visual feedback */
}

.edge-node {
  cursor: pointer;
  transition: all 0.3s ease;
}

.edge-node:hover {
  /* Removed movement effects - keeping only subtle visual feedback */
}

.edge-node.own-node {
  filter: brightness(1.1);
}

.edge-node.other-offline {
  opacity: 0.6;
}

/* 连接线动画 */
.connection-line {
  transition: stroke-opacity 0.3s ease;
}

.data-flow-line {
  stroke-linecap: round;
  opacity: 0.8;
}

/* 状态指示器动画 */
.status-indicator {
  filter: drop-shadow(0 0 3px rgba(16, 185, 129, 0.6));
}

/* 训练完成覆盖层 */
.training-complete-overlay {
  animation: fadeIn 0.8s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 工具提示样式 */
.node-tooltip {
  position: fixed;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 8px;
  padding: 8px 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(8px);
  max-width: 200px;
  transition: opacity 0.2s ease;
}

:root.dark .node-tooltip {
  background: rgba(31, 41, 55, 0.95);
  border-color: rgba(75, 85, 99, 0.8);
}

.connection-tooltip {
  position: fixed;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: 8px;
  padding: 10px 14px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(8px);
  max-width: 240px;
  transition: opacity 0.2s ease;
  min-width: 200px;
}

:root.dark .connection-tooltip {
  background: rgba(31, 41, 55, 0.95);
  border-color: rgba(75, 85, 99, 0.8);
}

.tooltip-content {
  font-size: 12px;
  line-height: 1.4;
}

/* 性能优化提示样式 */
.performance-notice {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 6px;
  padding: 8px 12px;
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
  max-width: 300px;
  font-size: 12px;
}

:root.dark .performance-notice {
  background: rgba(31, 41, 55, 0.95);
  border-color: rgba(245, 158, 11, 0.4);
}


/* 响应式设计 */
@media (max-width: 768px) {
  .node-svg {
    height: 400px;
  }
  
  .node-tooltip {
    font-size: 11px;
    padding: 6px 10px;
  }
}
</style>