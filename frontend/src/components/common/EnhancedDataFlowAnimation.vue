<template>
  <div class="enhanced-data-flow-animation">
    <svg 
      ref="animationSvg"
      class="w-full h-full"
      :viewBox="`0 0 ${svgDimensions.width} ${svgDimensions.height}`"
      preserveAspectRatio="xMidYMid meet"
    >
      <!-- 定义渐变和滤镜 -->
      <defs>
        <!-- 数据传输渐变 -->
        <linearGradient id="dataFlowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0" />
          <stop offset="30%" :stop-color="primaryColor" stop-opacity="0.8" />
          <stop offset="70%" :stop-color="primaryColor" stop-opacity="1" />
          <stop offset="100%" :stop-color="primaryColor" stop-opacity="0" />
        </linearGradient>
        
        <!-- 脉冲光晕渐变 -->
        <radialGradient id="pulseGlow" cx="50%" cy="50%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0.8" />
          <stop offset="50%" :stop-color="primaryColor" stop-opacity="0.4" />
          <stop offset="100%" :stop-color="primaryColor" stop-opacity="0" />
        </radialGradient>
        
        <!-- 节点发光滤镜 -->
        <filter id="nodeGlow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        
        <!-- 连接线发光滤镜 -->
        <filter id="connectionGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="2" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        
        <!-- 粒子效果滤镜 -->
        <filter id="particleGlow" x="-100%" y="-100%" width="300%" height="300%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="1.5" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        
        <!-- 波浪效果渐变 -->
        <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :stop-color="primaryColor" stop-opacity="0" />
          <stop offset="25%" :stop-color="primaryColor" stop-opacity="0.6" />
          <stop offset="50%" :stop-color="primaryColor" stop-opacity="1" />
          <stop offset="75%" :stop-color="primaryColor" stop-opacity="0.6" />
          <stop offset="100%" :stop-color="primaryColor" stop-opacity="0" />
        </linearGradient>
      </defs>
      
      <!-- 连接线层 -->
      <g class="connections-layer">
        <g v-for="connection in activeConnections" :key="`${connection.from}-${connection.to}`">
          <!-- 基础连接线 -->
          <path
            :d="getConnectionPath(connection)"
            :stroke="connectionColor"
            stroke-width="2"
            stroke-linecap="round"
            fill="none"
            opacity="0.3"
            class="base-connection"
          />
          
          <!-- 脉冲光晕效果 -->
          <path
            :d="getConnectionPath(connection)"
            :stroke="primaryColor"
            stroke-width="8"
            stroke-linecap="round"
            fill="none"
            opacity="0.6"
            filter="url(#connectionGlow)"
            class="pulse-glow"
          >
            <animate
              attributeName="opacity"
              values="0.2;0.8;0.2"
              dur="2s"
              repeatCount="indefinite"
            />
          </path>
          
          <!-- 波浪传输效果 -->
          <path
            :d="getConnectionPath(connection)"
            stroke="url(#waveGradient)"
            stroke-width="4"
            stroke-linecap="round"
            fill="none"
            stroke-dasharray="20,40"
            class="wave-transmission"
          >
            <animate
              attributeName="stroke-dashoffset"
              values="0;-60;-120"
              dur="3s"
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
              filter="url(#particleGlow)"
              class="data-particle"
            >
              <animate
                attributeName="opacity"
                values="0;1;0"
                :dur="particle.duration"
                :begin="particle.delay"
                repeatCount="indefinite"
              />
            </circle>
          </g>
        </g>
      </g>
      
      <!-- 节点层 -->
      <g class="nodes-layer">
        <g v-for="node in activeNodes" :key="node.id" class="node-group">
          <!-- 节点脉冲光晕 -->
          <circle
            :cx="getNodePosition(node).x"
            :cy="getNodePosition(node).y"
            :r="node.radius + 15"
            fill="url(#pulseGlow)"
            class="node-pulse"
          >
            <animate
              attributeName="r"
              :values="`${node.radius + 10};${node.radius + 25};${node.radius + 10}`"
              dur="2s"
              repeatCount="indefinite"
            />
            <animate
              attributeName="opacity"
              values="0.8;0.2;0.8"
              dur="2s"
              repeatCount="indefinite"
            />
          </circle>
          
          <!-- 主节点 -->
          <circle
            :cx="getNodePosition(node).x"
            :cy="getNodePosition(node).y"
            :r="node.radius"
            :fill="node.color"
            :stroke="node.strokeColor"
            stroke-width="2"
            filter="url(#nodeGlow)"
            class="main-node"
          />
          
          <!-- 数据传输指示器 -->
          <g v-if="node.isTransmitting" class="transmission-indicator">
            <circle
              :cx="getNodePosition(node).x"
              :cy="getNodePosition(node).y"
              :r="node.radius + 8"
              fill="none"
              :stroke="primaryColor"
              stroke-width="2"
              stroke-dasharray="5,5"
              class="transmission-ring"
            >
              <animateTransform
                attributeName="transform"
                type="rotate"
                :values="`0 ${getNodePosition(node).x} ${getNodePosition(node).y};360 ${getNodePosition(node).x} ${getNodePosition(node).y}`"
                dur="1s"
                repeatCount="indefinite"
              />
            </circle>
          </g>
        </g>
      </g>
    </svg>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  connections: {
    type: Array,
    default: () => []
  },
  active: {
    type: Boolean,
    default: true
  },
  animationSpeed: {
    type: Number,
    default: 1.0
  },
  primaryColor: {
    type: String,
    default: '#3b82f6'
  },
  secondaryColor: {
    type: String,
    default: '#10b981'
  },
  connectionColor: {
    type: String,
    default: '#6b7280'
  }
})

const emit = defineEmits(['node-click', 'connection-click'])

const animationSvg = ref(null)
const animationId = ref(null)

// SVG 尺寸
const svgDimensions = reactive({
  width: 1200,
  height: 700
})

// 动画状态
const animationState = reactive({
  time: 0,
  particles: []
})

// 计算属性
const activeNodes = computed(() => {
  return props.nodes.filter(node => node.visible !== false)
})

const activeConnections = computed(() => {
  return props.connections.filter(connection => {
    const fromNode = activeNodes.value.find(n => n.id === connection.from)
    const toNode = activeNodes.value.find(n => n.id === connection.to)
    return fromNode && toNode && connection.active
  })
})

// 获取节点位置
const getNodePosition = (node) => {
  return {
    x: node.x || 0,
    y: node.y || 0
  }
}

// 获取连接路径
const getConnectionPath = (connection) => {
  const fromNode = activeNodes.value.find(n => n.id === connection.from)
  const toNode = activeNodes.value.find(n => n.id === connection.to)
  
  if (!fromNode || !toNode) return ''
  
  const fromPos = getNodePosition(fromNode)
  const toPos = getNodePosition(toNode)
  
  // 创建曲线路径
  const dx = toPos.x - fromPos.x
  const dy = toPos.y - fromPos.y
  const distance = Math.sqrt(dx * dx + dy * dy)
  const midX = fromPos.x + dx * 0.5
  const midY = fromPos.y + dy * 0.5
  
  const offset = Math.min(60, Math.max(20, distance / 6))
  const angle = Math.atan2(dy, dx) + Math.PI / 2
  const ctrlX = midX + Math.cos(angle) * offset
  const ctrlY = midY + Math.sin(angle) * offset
  
  return `M ${fromPos.x} ${fromPos.y} Q ${ctrlX} ${ctrlY} ${toPos.x} ${toPos.y}`
}

// 生成数据粒子
const getDataParticles = (connection) => {
  const particles = []
  const particleCount = 3
  
  for (let i = 0; i < particleCount; i++) {
    const progress = (animationState.time + i * 0.33) % 1
    const path = getConnectionPath(connection)
    
    // 简化的路径点计算
    const fromNode = activeNodes.value.find(n => n.id === connection.from)
    const toNode = activeNodes.value.find(n => n.id === connection.to)
    
    if (fromNode && toNode) {
      const fromPos = getNodePosition(fromNode)
      const toPos = getNodePosition(toNode)
      
      const x = fromPos.x + (toPos.x - fromPos.x) * progress
      const y = fromPos.y + (toPos.y - fromPos.y) * progress
      
      particles.push({
        x,
        y,
        size: 3 + Math.sin(animationState.time * 10 + i) * 1,
        color: props.primaryColor,
        duration: `${2 / props.animationSpeed}s`,
        delay: `${i * 0.5}s`
      })
    }
  }
  
  return particles
}

// 动画循环
const animate = () => {
  if (!props.active) return
  
  animationState.time += 0.016 * props.animationSpeed
  
  // 更新粒子位置
  animationState.particles = []
  activeConnections.value.forEach(connection => {
    const particles = getDataParticles(connection)
    animationState.particles.push(...particles)
  })
  
  animationId.value = requestAnimationFrame(animate)
}

// 生命周期
onMounted(() => {
  if (props.active) {
    animate()
  }
  
  // 监听窗口大小变化
  const handleResize = () => {
    if (animationSvg.value) {
      const rect = animationSvg.value.parentElement.getBoundingClientRect()
      svgDimensions.width = rect.width
      svgDimensions.height = rect.height
    }
  }
  
  window.addEventListener('resize', handleResize)
  handleResize()
})

onUnmounted(() => {
  if (animationId.value) {
    cancelAnimationFrame(animationId.value)
  }
  window.removeEventListener('resize', handleResize)
})

// 监听 active 属性变化
watch(() => props.active, (newActive) => {
  if (newActive) {
    animate()
  } else {
    if (animationId.value) {
      cancelAnimationFrame(animationId.value)
    }
  }
})
</script>

<style scoped>
.enhanced-data-flow-animation {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.base-connection {
  transition: all 0.3s ease;
}

.pulse-glow {
  animation: pulse-glow 2s ease-in-out infinite;
}

.wave-transmission {
  animation: wave-flow 3s linear infinite;
}

.data-particle {
  animation: particle-float 2s ease-in-out infinite;
}

.node-pulse {
  animation: node-pulse 2s ease-in-out infinite;
}

.main-node {
  transition: all 0.3s ease;
}

.transmission-ring {
  animation: transmission-rotate 1s linear infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    opacity: 0.2;
    stroke-width: 8;
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
    stroke-dashoffset: -60;
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

@keyframes node-pulse {
  0%, 100% {
    r: 25;
    opacity: 0.8;
  }
  50% {
    r: 40;
    opacity: 0.2;
  }
}

@keyframes transmission-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .enhanced-data-flow-animation {
    font-size: 12px;
  }
}
</style>
