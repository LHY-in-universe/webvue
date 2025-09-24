<template>
  <div class="federated-network-visualization w-full h-full relative">
    <svg 
      ref="networkSvg"
      class="w-full h-full"
      :viewBox="`0 0 ${svgDimensions.width} ${svgDimensions.height}`"
      preserveAspectRatio="xMidYMid meet"
    >
      <!-- Clean white background -->
      <rect width="100%" height="100%" :fill="themeStore.isDark ? '#111827' : '#ffffff'" />
      
      <!-- Gradient and Pattern Definitions -->
      <defs>
        <!-- Simplified connection colors -->
        <linearGradient id="connectionGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#34d399' : '#10b981'" />
          <stop offset="100%" :stop-color="themeStore.isDark ? '#22c55e' : '#059669'" />
        </linearGradient>
        
        <!-- Simplified Node colors -->
        <radialGradient id="modelGradient" cx="50%" cy="50%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#93c5fd' : '#dbeafe'" />
          <stop offset="100%" :stop-color="themeStore.isDark ? '#3b82f6' : '#2563eb'" />
        </radialGradient>
        
        <radialGradient id="controlGradient" cx="50%" cy="50%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#fca5a5' : '#fecaca'" />
          <stop offset="100%" :stop-color="themeStore.isDark ? '#ef4444' : '#dc2626'" />
        </radialGradient>
        
        <radialGradient id="trainingGradient" cx="50%" cy="50%">
          <stop offset="0%" :stop-color="themeStore.isDark ? '#93c5fd' : '#dbeafe'" />
          <stop offset="100%" :stop-color="themeStore.isDark ? '#3b82f6' : '#2563eb'" />
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
          <!-- 移除静态连接线，只保留动态粒子效果 -->
          
          <!-- 纯数据粒子传输效果 - 始终显示 -->
          <g class="enhanced-data-flow">
            <!-- 数据包粒子效果 - 沿路径移动 -->
            <g v-for="(particle, index) in getDataParticles(connection)" :key="`particle-${index}`">
              <!-- 定义粒子移动路径 -->
              <path
                :d="`M ${particle.x} ${particle.y} Q ${particle.ctrlX} ${particle.ctrlY} ${particle.endX} ${particle.endY}`"
                stroke="transparent"
                fill="none"
                :id="`particle-path-${connection.id}-${index}`"
              />
              
              <!-- 粒子圆圈 -->
              <circle
                :r="particle.size"
                :fill="particle.color"
                class="data-particle"
                filter="url(#particleGlow)"
              >
                <!-- 沿路径移动动画 -->
                <animateMotion
                  :dur="particle.duration"
                  :begin="particle.delay"
                  repeatCount="indefinite"
                >
                  <mpath :href="`#particle-path-${connection.id}-${index}`" />
                </animateMotion>
                
                <!-- 透明度动画 - 平滑过渡，消除卡顿 -->
                <animate
                  attributeName="opacity"
                  :values="particle.direction === 'forward' ? '0;0.3;1;1;0.3;0' : '0;0.2;0.8;0.8;0.2;0'"
                  :dur="particle.duration"
                  :begin="particle.delay"
                  repeatCount="indefinite"
                  calcMode="spline"
                  keySplines="0.25 0.1 0.25 1; 0.25 0.1 0.25 1; 0.25 0.1 0.25 1; 0.25 0.1 0.25 1"
                />
                
                <!-- 大小动画 - 平滑过渡 -->
                <animate
                  attributeName="r"
                  :values="particle.direction === 'forward' ? '2;2.5;4;4;2.5;2' : '1.5;2;3;3;2;1.5'"
                  :dur="particle.duration"
                  :begin="particle.delay"
                  repeatCount="indefinite"
                  calcMode="spline"
                  keySplines="0.25 0.1 0.25 1; 0.25 0.1 0.25 1; 0.25 0.1 0.25 1; 0.25 0.1 0.25 1"
                />
                
                <!-- 发光效果动画 - 平滑颜色过渡 -->
                <animate
                  attributeName="fill"
                  :values="particle.direction === 'forward' 
                    ? `${particle.color};${particle.color};#ffffff;${particle.color};${particle.color}`
                    : `${particle.color};${particle.color};#fbbf24;${particle.color};${particle.color}`"
                  :dur="particle.duration"
                  :begin="particle.delay"
                  repeatCount="indefinite"
                  calcMode="spline"
                  keySplines="0.25 0.1 0.25 1; 0.25 0.1 0.25 1; 0.25 0.1 0.25 1; 0.25 0.1 0.25 1"
                />
              </circle>
            </g>
          </g>
        </g>
      </g>
      
      <!-- Nodes (Total: {{ validNodes.length }}) -->
      <g class="nodes">
        <g v-for="node in validNodes" :key="node.id"
           class="node-group static-node"
           :class="{ 'node-fading': nodeAnimationStates?.get(node.id)?.fading }"
           :style="{
             opacity: getNodeOpacity(node),
             transform: `scale(${getNodeScale(node)})`,
             transformOrigin: `${getNodePosition(node).x}px ${getNodePosition(node).y}px`,
             pointerEvents: 'all'
           }"
        >
          <!-- Larger Invisible Click Area -->
          <circle
            :cx="getNodePosition(node).x"
            :cy="getNodePosition(node).y"
            r="40"
            fill="transparent"
            class="node-click-area cursor-pointer"
            style="pointer-events: all; user-select: none;"
            @click.stop.prevent="handleNodeClick(node)"
          />

          <!-- Main Node Circle - 根据角色类型显示不同颜色 -->
          <circle
            :cx="getNodePosition(node).x"
            :cy="getNodePosition(node).y"
            r="25"
            :fill="getNodeColorByRole(node)"
            :stroke="themeStore.isDark ? '#ffffff' : '#000000'"
            stroke-width="2"
            class="node-circle select-none no-hover"
            style="pointer-events: none; user-select: none;"
          />
          
          <!-- Node Label -->
          <text
            :x="getNodePosition(node).x"
            :y="getNodePosition(node).y - 40"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#ffffff' : '#000000'"
            font-size="11"
            font-weight="600"
            class="node-label"
            style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; pointer-events: none; user-select: none;"
          >{{ getNodeDisplayName(node) }}</text>
          
          <!-- Training Progress Text (for training nodes) -->
          <text
            v-if="node.type === 'training' && typeof node.trainingProgress === 'number'"
            :x="getNodePosition(node).x"
            :y="getNodePosition(node).y + 5"
            text-anchor="middle"
            fill="#ffffff"
            font-size="14"
            font-weight="bold"
            class="progress-text"
            style="pointer-events: none; user-select: none;"
          >{{ Math.round(node.trainingProgress) }}%</text>
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

/* Very subtle hover effect to indicate clickability without visual changes */
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
</style>

<script setup>
import { ref, computed, reactive, onMounted, onUnmounted, nextTick, watch } from 'vue'
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
  trainingRound: {
    type: Number,
    default: 0
  },
  trainingStatus: {
    type: String,
    default: 'idle'
  },
  nodeAnimationStates: {
    type: Map,
    default: () => new Map()
  }
})

const emit = defineEmits(['node-click', 'connection-click'])

const themeStore = useThemeStore()
const networkSvg = ref(null)

// Removed all dragging functionality - nodes are now completely static

// Fixed layout dimensions
const svgDimensions = reactive({
  width: 1400,
  height: 600,
  padding: 80
})

// Computed property for valid nodes - filter out invalid/undefined nodes
// 修正：允许使用 ip 作为 id，并基于 role 推断 type，确保与 Node Details List 一一对应
const validNodes = computed(() => {
  if (!props.nodes || !Array.isArray(props.nodes)) {
    console.warn('validNodes: props.nodes is not a valid array:', props.nodes)
    return []
  }

  const normalized = props.nodes
    .map(original => {
      const node = { ...original }
      // 使用 ip 作为 id 的兜底
      if (!node.id && node.ip) node.id = node.ip

      // 基于 role 推断 type（与列表分类保持一致）
      if (!node.type && node.role) {
        const role = String(node.role).toLowerCase()
        if (role.includes('mpc model node')) node.type = 'model'
        else if (role.includes('model manager node')) node.type = 'control'
        else if (role.includes('edge ai training node')) node.type = 'training'
      }

      // 名称兜底
      if (!node.name) node.name = node.ip || node.id
      return node
    })
    .filter(node => {
      if (!node) return false
      if (!node.id) return false
      if (!node.type) node.type = 'training'
      return true
    })

  console.log(`validNodes: normalized ${normalized.length} nodes from ${props.nodes.length} total`)
  return normalized
})

// Fan-shaped node positions (训练节点大幅下移与模型节点区分)
const FIXED_NODE_POSITIONS = [
  // 第一层扇形 (内圈) - 错开Y坐标避免标签重叠
  { x: 500, y: 300 }, { x: 700, y: 320 }, { x: 900, y: 300 },
  // 第二层扇形 (中圈) - 错开Y坐标避免标签重叠
  { x: 340, y: 420 }, { x: 520, y: 450 }, { x: 700, y: 480 }, { x: 880, y: 450 }, { x: 1060, y: 420 },
  // 第三层扇形 (外圈) - 错开Y坐标避免标签重叠
  { x: 140, y: 540 }, { x: 380, y: 570 }, { x: 620, y: 590 }, { x: 780, y: 610 }, { x: 1020, y: 570 }, { x: 1260, y: 540 },
  // 最外层 - 底部中心下移
  { x: 700, y: 640 },
  // 扩展位置 - 支持更多节点
  { x: 200, y: 300 }, { x: 1200, y: 300 }, { x: 200, y: 500 }, { x: 1200, y: 500 },
  { x: 100, y: 400 }, { x: 1300, y: 400 }, { x: 100, y: 600 }, { x: 1300, y: 600 },
  { x: 300, y: 200 }, { x: 1100, y: 200 }, { x: 300, y: 700 }, { x: 1100, y: 700 },
  { x: 50, y: 300 }, { x: 1350, y: 300 }, { x: 50, y: 500 }, { x: 1350, y: 500 },
  { x: 150, y: 350 }, { x: 1250, y: 350 }, { x: 150, y: 650 }, { x: 1250, y: 650 }
]

// Control nodes at the center/top of the fan (优化控制节点位置)
const CONTROL_NODE_POSITIONS = [
  { x: 480, y: 130 },  // 左侧控制中心
  { x: 700, y: 100 },  // 中央控制中心
  { x: 920, y: 130 },  // 右侧控制中心
  // 扩展控制节点位置
  { x: 300, y: 150 },  // 左扩展
  { x: 1100, y: 150 }, // 右扩展
  { x: 600, y: 80 },   // 中左
  { x: 800, y: 80 },   // 中右
  { x: 200, y: 200 },  // 最左
  { x: 1200, y: 200 }  // 最右
]

// Node position tracking（逐层整齐排布）
const nodePositions = ref(new Map())

// 基于角色分三层并保持与列表一致的顺序
const layeredGroups = computed(() => {
  const groups = { mpc: [], manager: [], edge: [] }
  validNodes.value.forEach(n => {
    const role = String(n.role || '').toLowerCase()
    if (role.includes('mpc model node')) groups.mpc.push(n)
    else if (role.includes('model manager node')) groups.manager.push(n)
    else if (role.includes('edge ai training node')) groups.edge.push(n)
    else if (n.type === 'model') groups.mpc.push(n)
    else if (n.type === 'control') groups.manager.push(n)
    else groups.edge.push(n)
  })
  return groups
})

// 每层的Y坐标（上、中、下）
const LAYER_Y = computed(() => {
  const h = Math.max(600, svgDimensions.height)
  // 给出上中下三层在可视区域中的相对位置
  return {
    mpc: h * 0.18,
    manager: h * 0.38,
    edge: h * 0.60
  }
})

// 计算一层的X坐标分布
const getLayerX = (index, count) => {
  const padding = 120
  const width = Math.max(1400, svgDimensions.width) - padding * 2
  if (count <= 1) return padding + width / 2
  const step = width / (count - 1)
  return padding + step * index
}

// 根据节点ID稳定分配位置的函数
const getStablePositionIndex = (nodeId, nodeType) => {
  if (nodeType === 'training') {
    // 训练节点稳定分配 - 使用IP地址的哈希值
    const hash = nodeId.split('.').reduce((acc, part) => acc + parseInt(part), 0)
    return hash % FIXED_NODE_POSITIONS.length
  } else if (['model', 'control'].includes(nodeType)) {
    // 控制节点稳定分配 - 使用IP地址的哈希值
    const hash = nodeId.split('.').reduce((acc, part) => acc + parseInt(part), 0)
    return hash % CONTROL_NODE_POSITIONS.length
  }
  return 0
}

// Initialize positions for all nodes: 按层等间距排布，顺序与列表一致
const initializeNodePositions = () => {
  nodePositions.value.clear()
  const groups = layeredGroups.value

  // 逐层放置
  const placeGroup = (arr, y) => {
    arr.forEach((node, idx) => {
      const x = getLayerX(idx, arr.length)
      nodePositions.value.set(node.id, { x, y })
    })
  }

  placeGroup(groups.mpc, LAYER_Y.value.mpc)
  placeGroup(groups.manager, LAYER_Y.value.manager)
  placeGroup(groups.edge, LAYER_Y.value.edge)
}

// Get position for a specific node
const getNodePosition = (node) => {
  if (!node || !node.id) {
    console.error('getNodePosition called with invalid node:', node)
    return { x: 400, y: 250 }
  }

  // First check if we have a stored position
  const storedPosition = nodePositions.value.get(node.id)
  if (storedPosition) {
    // Validate stored position
    if (typeof storedPosition.x === 'number' && typeof storedPosition.y === 'number') {
      // Return a copy to prevent any modifications to the original position
      return { x: storedPosition.x, y: storedPosition.y }
    } else {
      console.error(`Invalid stored position for node ${node.id}:`, storedPosition)
      nodePositions.value.delete(node.id) // Remove invalid position
    }
  }

  // 如果没有缓存位置，按照分层规则即时计算
  const role = String(node.role || '').toLowerCase()
  let layer = 'edge'
  if (role.includes('mpc model node') || node.type === 'model') layer = 'mpc'
  else if (role.includes('model manager node') || node.type === 'control') layer = 'manager'
  else layer = 'edge'

  const groups = layeredGroups.value
  const arr = layer === 'mpc' ? groups.mpc : layer === 'manager' ? groups.manager : groups.edge
  const idx = arr.findIndex(n => n.id === node.id)
  const x = getLayerX(idx === -1 ? 0 : idx, arr.length || 1)
  const y = LAYER_Y.value[layer]
  const position = { x, y }
  nodePositions.value.set(node.id, position)
  return position

  // Fallback to node's original coordinates if available
  if (node.x && node.y && typeof node.x === 'number' && typeof node.y === 'number') {
    const fallbackPosition = { x: node.x, y: node.y }
    nodePositions.value.set(node.id, fallbackPosition)
    console.log(`Using fallback position for ${node.id}:`, fallbackPosition)
    return fallbackPosition
  }

  // Default position if nothing else works
  const defaultPosition = { x: 400, y: 250 }
  console.warn(`No position found for node ${node.id} (type: ${node.type}), using default:`, defaultPosition)
  nodePositions.value.set(node.id, defaultPosition)
  return defaultPosition
}

// Helper functions
const getConnectionPath = (connection) => {
  const fromNode = validNodes.value.find(n => n.id === connection.from)
  const toNode = validNodes.value.find(n => n.id === connection.to)

  if (!fromNode || !toNode) return ''
  
  // Use computed positions instead of static coordinates
  const fromPos = getNodePosition(fromNode)
  const toPos = getNodePosition(toNode)
  
  // Create enhanced curved path with adaptive curvature
  const dx = toPos.x - fromPos.x
  const dy = toPos.y - fromPos.y
  const distance = Math.sqrt(dx * dx + dy * dy)
  const midX = fromPos.x + dx * 0.5
  const midY = fromPos.y + dy * 0.5
  
  // Enhanced control point calculation for better curves
  let offset = Math.min(120, Math.max(30, distance / 4))
  
  // Different curve styles based on connection type
  if (connection.type === 'control') {
    offset *= 1.2 // Slightly more curved for control connections
  }
  
  const angle = Math.atan2(dy, dx) + Math.PI / 2
  const ctrlX = midX + Math.cos(angle) * offset
  const ctrlY = midY + Math.sin(angle) * offset
  
  return `M ${fromPos.x} ${fromPos.y} Q ${ctrlX} ${ctrlY} ${toPos.x} ${toPos.y}`
}

const getConnectionWidth = (connection) => {
  if (!connection.bandwidth) {
    return connection.type === 'control' ? 4 : 3
  }
  
  const minWidth = connection.type === 'control' ? 3 : 2
  const maxWidth = connection.type === 'control' ? 7 : 5
  const bandwidth = Math.max(100, Math.min(1000, connection.bandwidth))
  return minWidth + ((bandwidth - 100) / 900) * (maxWidth - minWidth)
}

const getMidpoint = (connection) => {
  const from = validNodes.value.find(n => n.id === connection.from)
  const to = validNodes.value.find(n => n.id === connection.to)

  if (!from || !to) return { x: 0, y: 0 }
  
  return {
    x: (from.x + to.x) / 2,
    y: (from.y + to.y) / 2 - 15
  }
}

const formatBandwidth = (bandwidth) => {
  if (bandwidth > 1000) return `${(bandwidth / 1000).toFixed(1)}Gb/s`
  return `${bandwidth}Mb/s`
}

const getNodeGradient = (node) => {
  const gradients = {
    model: 'url(#modelGradient)',
    control: 'url(#controlGradient)',
    training: 'url(#trainingGradient)'
  }
  return gradients[node.type] || 'url(#trainingGradient)'
}

const getProgressColor = (progress) => {
  if (progress >= 95) return themeStore.isDark ? '#22c55e' : '#15803d'  // Excellent
  if (progress >= 80) return themeStore.isDark ? '#3b82f6' : '#1e40af'  // Good
  if (progress >= 60) return themeStore.isDark ? '#06b6d4' : '#0c4a6e'  // Fair
  if (progress >= 40) return themeStore.isDark ? '#f59e0b' : '#d97706'  // Poor
  if (progress >= 20) return themeStore.isDark ? '#f97316' : '#ea580c'  // Very Poor
  return themeStore.isDark ? '#ef4444' : '#dc2626'  // Critical
}

const getStatusColor = (status) => {
  const colors = {
    online: '#22c55e',
    training: '#3b82f6',
    completed: '#10b981',
    offline: '#ef4444'
  }
  return colors[status] || '#6b7280'
}

const getConnectionGradient = (connection) => {
  const gradients = {
    control: 'url(#controlGradient)',
    data: 'url(#dataGradient)',
    sync: 'url(#connectionGradient)'
  }
  return gradients[connection.type] || 'url(#connectionGradient)'
}

// 数据流动画相关函数
const getTransmissionColor = (direction) => {
  const colors = {
    upstream: '#3b82f6',      // 蓝色：训练节点 → 模型节点 (梯度上传)
    downstream: '#10b981',    // 绿色：模型节点 → 训练节点 (参数下发)
    bidirectional: '#8b5cf6'  // 紫色：双向传输
  }
  return colors[direction] || '#10b981'
}

const getAnimationValues = (direction) => {
  switch (direction) {
    case 'downstream': // 模型节点 → 训练节点
      return "0;-120;-240"
    case 'upstream':   // 训练节点 → 模型节点  
      return "0;120;240"
    case 'bidirectional': // 双向传输
      return "0;-120;0;120;0"
    default:
      return "0;-120;-240"
  }
}

// 生成数据粒子效果 - 单条弧线双向传输
const getDataParticles = (connection) => {
  const particles = []
  const fromNode = validNodes.value.find(n => n.id === connection.from)
  const toNode = validNodes.value.find(n => n.id === connection.to)
  
  if (!fromNode || !toNode) return particles
  
  const fromPos = getNodePosition(fromNode)
  const toPos = getNodePosition(toNode)
  
  // 计算弧线路径的控制点
  const dx = toPos.x - fromPos.x
  const dy = toPos.y - fromPos.y
  const distance = Math.sqrt(dx * dx + dy * dy)
  const midX = fromPos.x + dx * 0.5
  const midY = fromPos.y + dy * 0.5
  
  // 创建单条弧线路径
  // 为了避免多条近似共线的连接在视觉上堆叠为一条带，我们给每条连接引入稳定的抖动（基于连接ID的种子），
  // 并对粒子相位/持续时间做轻微错峰，从而在时间轴和空间上都拉开。
  const hashCode = (str) => {
    let h = 0
    for (let k = 0; k < str.length; k++) {
      h = ((h << 5) - h) + str.charCodeAt(k)
      h |= 0
    }
    return Math.abs(h)
  }
  const seededRandom = (seed, a = 9301, c = 49297, m = 233280) => {
    seed = (seed * a + c) % m
    return seed / m
  }
  const seed = hashCode(connection.id)
  const r1 = seededRandom(seed)
  const r2 = seededRandom(seed + 1)
  const r3 = seededRandom(seed + 2)

  // 基础弧度
  let offset = Math.min(80, Math.max(30, distance / 4))
  // 如果近似水平连接，适当增大弧度，避免在画布下方重叠
  const isNearlyHorizontal = Math.abs(dy) < Math.max(20, Math.abs(dx) * 0.2)
  if (isNearlyHorizontal) offset *= 1.35

  // 对弧度加入稳定抖动（±20%）
  offset *= (0.8 + r1 * 0.4)
  const angle = Math.atan2(dy, dx) + Math.PI / 2
  // 控制点加入少量横向/纵向抖动（相对于offset的±15%）
  const jitterFactor = 0.15 * offset
  const ctrlX = midX + Math.cos(angle) * offset + (r2 - 0.5) * 2 * jitterFactor
  const ctrlY = midY + Math.sin(angle) * offset + (r3 - 0.5) * 2 * jitterFactor

  // 双向粒子流 - 正向和反向，优化时序消除卡顿，并加入稳定相位偏移
  const directions = ['forward', 'reverse']
  // 距离越长粒子越多，但限制范围，避免过密
  const particleCount = Math.max(6, Math.min(12, Math.floor(distance / 120) + 6))
  // 每条连接的基础持续时间加入±10%的偏移
  const baseDuration = 2.4 * (0.9 + seededRandom(seed + 3) * 0.2)
  // 交错延迟更短，更连续
  const staggerDelay = 0.12
  // 稳定的相位偏移（0-1.5s），使不同连接不同步
  const phaseOffset = seededRandom(seed + 4) * 1.5

  directions.forEach((direction, dirIndex) => {
    for (let i = 0; i < particleCount; i++) {
      const isForward = direction === 'forward'
      const startPos = isForward ? fromPos : toPos
      const endPos = isForward ? toPos : fromPos

      // 根据方向选择颜色
      let particleColor
      if (isForward) {
        particleColor = getTransmissionColor(connection.direction || 'downstream')
      } else {
        // 反向传输使用不同的颜色
        const reverseColors = {
          downstream: '#ef4444', // 红色
          upstream: '#f59e0b',   // 橙色
          bidirectional: '#8b5cf6' // 紫色
        }
        particleColor = reverseColors[connection.direction || 'downstream'] || '#ef4444'
      }

      // 平滑且稳定的延迟时间（加入相位偏移），确保不同连接不同步
      const delay = phaseOffset + (i + dirIndex * particleCount) * staggerDelay

      particles.push({
        x: startPos.x,
        y: startPos.y,
        ctrlX: ctrlX,
        ctrlY: ctrlY,
        endX: endPos.x,
        endY: endPos.y,
        size: 2.5 + Math.sin(Date.now() / 300 + i) * 1,
        color: particleColor,
        duration: `${baseDuration}s`,
        delay: `${delay}s`,
        direction: direction
      })
    }
  })
  
  console.log(`为连接 ${connection.from} <-> ${connection.to} 生成了 ${particles.length} 个弧线粒子`)
  return particles
}

// 生成所有节点间的完全连接 - 每个节点都与所有其他节点传输数据
const generateFullMeshConnections = (nodes) => {
  const connections = []
  
  // 为每对节点创建双向连接
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const fromNode = nodes[i]
      const toNode = nodes[j]
      const connectionId = `${fromNode.id}-${toNode.id}`
      
      const directions = ['upstream', 'downstream', 'bidirectional']
      const randomDirection = directions[Math.floor(Math.random() * directions.length)]
      
      connections.push({
        id: connectionId,
        from: fromNode.id,
        to: toNode.id,
        type: 'data',
        active: true,
        transmitting: true,
        direction: randomDirection,
        lastTransmission: Date.now(),
        bandwidth: Math.random() * 100
      })
    }
  }
  
  console.log(`生成了 ${connections.length} 个完全连接（所有节点互相传输）`)
  return connections
}

// 获取节点的透明度（基于动画状态）
const getNodeOpacity = (node) => {
  if (!node || !node.id) {
    console.warn('getNodeOpacity called with invalid node:', node)
    return 1
  }

  const animationState = props.nodeAnimationStates?.get(node.id)
  if (!animationState) return 1

  if (animationState.fading) {
    // 计算淡出进度（3秒内从1到0）
    const elapsed = Date.now() - animationState.fadeStartTime
    const fadeProgress = Math.min(elapsed / 3000, 1) // 3秒淡出
    const opacity = 1 - fadeProgress
    // 确保最小透明度为0.3，避免节点完全不可见
    return Math.max(0.3, opacity)
  }

  return 1
}

// 获取节点的缩放（基于动画状态）
const getNodeScale = (node) => {
  if (!node || !node.id) {
    console.warn('getNodeScale called with invalid node:', node)
    return 1
  }

  const animationState = props.nodeAnimationStates?.get(node.id)
  if (!animationState) return 1

  if (animationState.fading) {
    // 计算缩放进度（3秒内从1到0.5）
    const elapsed = Date.now() - animationState.fadeStartTime
    const fadeProgress = Math.min(elapsed / 3000, 1)
    const scale = 1 - (fadeProgress * 0.5) // 缩放到50%而不是30%
    // 确保最小缩放为0.5，保持节点可点击
    return Math.max(0.5, scale)
  }

  return 1
}

// Validate node data structure
const validateNode = (node) => {
  if (!node) {
    console.error('Node is null or undefined')
    return false
  }

  // 使用 ip 作为 id（如果 id 不存在）
  if (!node.id && node.ip) {
    node.id = node.ip
  }

  if (!node.id) {
    console.error('Node missing required id/ip field:', node)
    return false
  }

  // 根据角色设置类型
  if (!node.type && node.role) {
    const role = String(node.role).toLowerCase()
    if (role.includes('mpc model node')) {
      node.type = 'model'
    } else if (role.includes('model manager node')) {
      node.type = 'control'
    } else if (role.includes('edge ai training node')) {
      node.type = 'training'
    } else {
      node.type = 'training' // 默认类型
    }
  }

  if (!node.type) {
    console.warn(`Node ${node.id} missing type field, assuming 'training'`)
    node.type = 'training'
  }

  // 使用 ip 作为 name（如果 name 不存在）
  if (!node.name) {
    node.name = node.ip || node.id
  }

  return true
}

// Get display name for node (truncate if too long to prevent overlap)
const getNodeDisplayName = (node) => {
  if (!validateNode(node)) {
    return 'Invalid'
  }

  const name = node.name || node.id
  // Truncate long names to prevent overlap - use 12 chars max
  if (name.length > 12) {
    return name.substring(0, 9) + '...'
  }
  return name
}

// 根据节点角色返回对应颜色
const getNodeColorByRole = (node) => {
  if (!node || !node.role) {
    // 根据 type 兜底
    if (node?.type === 'model') return '#3b82f6'
    if (node?.type === 'control') return '#10b981'
    if (node?.type === 'training') return '#8b5cf6'
    return '#6b7280'
  }
  
  const role = String(node.role).toLowerCase()
  
  // MPC Model Node - 蓝色
  if (role.includes('mpc model node')) {
    return '#3b82f6' // 蓝色
  }
  // Model Manager Node - 绿色  
  else if (role.includes('model manager node')) {
    return '#10b981' // 绿色
  }
  // Edge AI Training Node - 紫色
  else if (role.includes('edge ai training node')) {
    return '#8b5cf6' // 紫色
  }
  // 兜底逻辑：根据关键词判断
  else if (role.includes('model')) {
    return '#3b82f6' // 蓝色
  }
  else if (role.includes('manager') || node?.type === 'control') {
    return '#10b981' // 绿色
  }
  else if (role.includes('training')) {
    return '#8b5cf6' // 紫色
  }
  
  // 默认颜色
  return '#6b7280' // 灰色
}

// All dragging functionality removed - nodes are completely static

// Node interaction handlers
const handleNodeClick = (node) => {
  // Enhanced click logging for debugging
  console.log('🖱️ Node click event triggered:', {
    timestamp: new Date().toISOString(),
    nodeId: node?.id,
    nodeName: node?.name,
    nodeType: node?.type,
    nodeStatus: node?.status,
    hasValidId: !!node?.id,
    eventType: 'click',
    position: node ? getNodePosition(node) : null
  })

  // Validate node data
  if (!validateNode(node)) {
    console.error('❌ Node click rejected - validation failed:', {
      node,
      reason: 'Invalid node data'
    })
    return
  }

  // Additional safety check
  if (!node.id) {
    console.error('❌ Node click rejected - missing ID:', node)
    return
  }

  console.log('✅ Node click successful, emitting event for:', {
    nodeId: node.id,
    nodeName: node.name,
    nodeType: node.type
  })

  // Emit the node click event
  try {
    emit('node-click', node)
    console.log('📤 Node click event emitted successfully')
  } catch (error) {
    console.error('❌ Failed to emit node click event:', error)
  }
}

// All hover handlers removed for completely static nodes

// Removed all dragging mouse handlers - nodes are now completely static

// Public methods (removed zoom functionality)
const resetView = () => {
  // Reset nodes to their original positions if needed
  console.log('View reset (no zoom functionality)')
}

// Responsive layout support
const updateDimensions = () => {
  if (!networkSvg.value) return
  
  const container = networkSvg.value.parentElement
  if (container) {
    const rect = container.getBoundingClientRect()
    svgDimensions.width = Math.max(1400, rect.width)
    svgDimensions.height = Math.max(600, rect.height)
  }
}

// Initialize node positions to fixed coordinates
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
  
  // Force position initialization after a short delay
  setTimeout(() => {
    console.log('Force initializing positions for', validNodes.value.length, 'valid nodes')
    initializeNodePositions()
  }, 100)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateDimensions)
})

// Watch for valid node changes and reinitialize positions
watch(() => validNodes.value.length, () => {
  autoArrange()
}, { immediate: true })

// Watch for valid nodes array changes to reinitialize positions
watch(validNodes, () => {
  autoArrange()
}, { deep: true, immediate: true })

defineExpose({
  resetView,
  autoArrange,
  updateDimensions
})
</script>

<style scoped>
.federated-network-visualization {
  background: transparent;
  overflow: hidden;
}

.node-circle {
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* All hover effects removed for completely static nodes */
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
  pointer-events: none !important;
  user-select: none !important;
  -webkit-user-select: none !important;
  -moz-user-select: none !important;
  -ms-user-select: none !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.node-click-area {
  cursor: pointer !important;
  pointer-events: all !important;
  fill: transparent;
}

.node-circle {
  pointer-events: none !important;
  user-select: none !important;
}

/* Ensure proper layering */
.nodes {
  pointer-events: all;
}

.node-group {
  pointer-events: all !important;
}

.connection-line {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Connection hover effects also removed */

.control-connection {
  filter: drop-shadow(0 2px 4px rgba(245, 158, 11, 0.3));
}

.data-connection {
  filter: drop-shadow(0 2px 4px rgba(16, 185, 129, 0.3));
}

.training-active {
  filter: drop-shadow(0 0 8px currentColor) brightness(1.1);
}

.connection-label {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}


.node-group {
  transition: transform 0.2s ease, opacity 0.5s ease;
}

.node-fading {
  transition: opacity 3s ease-out, transform 3s ease-out !important;
}

/* 纯数据粒子传输效果样式 */
.enhanced-data-flow {
  pointer-events: none;
}

.data-particle {
  filter: drop-shadow(0 0 4px currentColor);
  animation: particle-glow 2.5s cubic-bezier(0.25, 0.1, 0.25, 1) infinite;
}

@keyframes particle-glow {
  0%, 100% {
    filter: drop-shadow(0 0 2px currentColor);
  }
  25% {
    filter: drop-shadow(0 0 4px currentColor);
  }
  50% {
    filter: drop-shadow(0 0 8px currentColor);
  }
  75% {
    filter: drop-shadow(0 0 4px currentColor);
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

/* 移除不需要的连接线样式 */

@media (max-width: 768px) {
  .node-label,
  .progress-text {
    font-size: 10px;
  }
  
  .connection-label {
    font-size: 9px;
  }
}
</style>