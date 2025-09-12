<template>
  <div class="gauge-chart" :style="containerStyles">
    <div class="relative w-full h-full flex items-center justify-center">
      <!-- SVG Gauge -->
      <svg 
        :width="size" 
        :height="size * 0.6" 
        viewBox="0 0 200 120" 
        class="gauge-svg"
      >
        <!-- Background Arc -->
        <path
          :d="backgroundArcPath"
          :stroke="backgroundColor"
          :stroke-width="strokeWidth"
          fill="none"
          class="gauge-background"
        />
        
        <!-- Progress Arc -->
        <path
          :d="progressArcPath"
          :stroke="progressColor"
          :stroke-width="strokeWidth"
          fill="none"
          :stroke-dasharray="progressDashArray"
          :stroke-dashoffset="progressDashOffset"
          class="gauge-progress transition-all duration-1000 ease-out"
          :style="{ strokeLinecap: 'round' }"
        />
        
        <!-- Value Indicators -->
        <g v-if="showTicks">
          <g v-for="(tick, index) in ticks" :key="index">
            <line
              :x1="tick.x1"
              :y1="tick.y1"
              :x2="tick.x2"
              :y2="tick.y2"
              :stroke="tickColor"
              :stroke-width="tick.major ? 2 : 1"
              class="gauge-tick"
            />
            <text
              v-if="tick.major && showLabels"
              :x="tick.labelX"
              :y="tick.labelY"
              :fill="labelColor"
              text-anchor="middle"
              class="gauge-label text-xs"
            >
              {{ tick.value }}
            </text>
          </g>
        </g>
        
        <!-- Center Dot -->
        <circle
          cx="100"
          cy="100"
          :r="strokeWidth / 2"
          :fill="progressColor"
          class="gauge-center"
        />
      </svg>
      
      <!-- Value Display -->
      <div class="absolute inset-0 flex flex-col items-center justify-center pt-8">
        <div :class="valueClasses">
          {{ displayValue }}
        </div>
        <div v-if="label" class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          {{ label }}
        </div>
        <div v-if="subtitle" class="text-xs text-gray-500 dark:text-gray-500 mt-1">
          {{ subtitle }}
        </div>
      </div>
      
      <!-- Status Indicator -->
      <div 
        v-if="showStatus"
        :class="statusIndicatorClasses"
        class="absolute bottom-2 left-1/2 transform -translate-x-1/2"
      >
        <component :is="statusIcon" class="w-4 h-4 mr-1" />
        {{ statusText }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ExclamationCircleIcon,
  InformationCircleIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  value: {
    type: Number,
    required: true
  },
  min: {
    type: Number,
    default: 0
  },
  max: {
    type: Number,
    default: 100
  },
  size: {
    type: Number,
    default: 200
  },
  thickness: {
    type: Number,
    default: 10
  },
  label: String,
  subtitle: String,
  unit: {
    type: String,
    default: ''
  },
  precision: {
    type: Number,
    default: 0
  },
  
  // Styling
  color: {
    type: String,
    default: 'blue'
  },
  backgroundColor: {
    type: String,
    default: '#e5e7eb'
  },
  
  // Features
  showTicks: {
    type: Boolean,
    default: true
  },
  showLabels: {
    type: Boolean,
    default: true
  },
  showStatus: {
    type: Boolean,
    default: false
  },
  animated: {
    type: Boolean,
    default: true
  },
  
  // Thresholds for status
  thresholds: {
    type: Object,
    default: () => ({
      good: 80,
      warning: 60,
      critical: 30
    })
  }
})

// Computed properties
const containerStyles = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size * 0.6}px`
}))

const strokeWidth = computed(() => props.thickness)

const percentage = computed(() => {
  return Math.max(0, Math.min(100, ((props.value - props.min) / (props.max - props.min)) * 100))
})

const displayValue = computed(() => {
  return props.value.toFixed(props.precision) + props.unit
})

const valueClasses = computed(() => {
  const baseClass = 'font-bold text-center'
  const sizeClass = props.size >= 200 ? 'text-2xl' : props.size >= 150 ? 'text-xl' : 'text-lg'
  return `${baseClass} ${sizeClass} ${progressColor.value.replace('stroke-', 'text-').replace('#', '')}`
})

// Color mapping
const colorMap = {
  blue: '#3B82F6',
  green: '#10B981',
  yellow: '#F59E0B',
  red: '#EF4444',
  purple: '#8B5CF6',
  indigo: '#6366F1',
  pink: '#EC4899',
  gray: '#6B7280'
}

const progressColor = computed(() => {
  if (props.showStatus) {
    if (props.value >= props.thresholds.good) return colorMap.green
    if (props.value >= props.thresholds.warning) return colorMap.yellow
    if (props.value >= props.thresholds.critical) return colorMap.red
    return colorMap.gray
  }
  
  return colorMap[props.color] || props.color
})

const tickColor = computed(() => '#9CA3AF')
const labelColor = computed(() => '#6B7280')

// Arc calculations
const radius = computed(() => 80)
const circumference = computed(() => Math.PI * radius.value)
const startAngle = computed(() => Math.PI) // Start from left (180 degrees)
const endAngle = computed(() => 0) // End at right (0 degrees)

const backgroundArcPath = computed(() => {
  const startX = 100 - radius.value
  const startY = 100
  const endX = 100 + radius.value
  const endY = 100
  
  return `M ${startX} ${startY} A ${radius.value} ${radius.value} 0 0 1 ${endX} ${endY}`
})

const progressArcPath = computed(() => {
  return backgroundArcPath.value
})

const progressDashArray = computed(() => {
  return circumference.value
})

const progressDashOffset = computed(() => {
  return circumference.value - (percentage.value / 100) * circumference.value
})

// Tick marks
const ticks = computed(() => {
  const tickCount = 11 // 0, 10, 20, ..., 100
  const ticks = []
  
  for (let i = 0; i < tickCount; i++) {
    const angle = startAngle.value - (i / (tickCount - 1)) * Math.PI
    const isMajor = i % 2 === 0 // Major ticks every 20%
    const tickRadius = radius.value
    const innerRadius = tickRadius - (isMajor ? 8 : 4)
    
    const x1 = 100 + Math.cos(angle) * innerRadius
    const y1 = 100 + Math.sin(angle) * innerRadius
    const x2 = 100 + Math.cos(angle) * tickRadius
    const y2 = 100 + Math.sin(angle) * tickRadius
    
    const labelRadius = tickRadius - 15
    const labelX = 100 + Math.cos(angle) * labelRadius
    const labelY = 100 + Math.sin(angle) * labelRadius + 4 // Offset for text baseline
    
    const value = Math.round(props.min + (i / (tickCount - 1)) * (props.max - props.min))
    
    ticks.push({
      x1,
      y1,
      x2,
      y2,
      labelX,
      labelY,
      value,
      major: isMajor
    })
  }
  
  return ticks
})

// Status
const status = computed(() => {
  if (!props.showStatus) return null
  
  if (props.value >= props.thresholds.good) return 'good'
  if (props.value >= props.thresholds.warning) return 'warning'
  if (props.value >= props.thresholds.critical) return 'critical'
  return 'danger'
})

const statusIcon = computed(() => {
  const icons = {
    good: CheckCircleIcon,
    warning: ExclamationTriangleIcon,
    critical: ExclamationCircleIcon,
    danger: ExclamationCircleIcon
  }
  return icons[status.value] || InformationCircleIcon
})

const statusText = computed(() => {
  const texts = {
    good: 'Good',
    warning: 'Warning',
    critical: 'Critical',
    danger: 'Danger'
  }
  return texts[status.value] || 'Unknown'
})

const statusIndicatorClasses = computed(() => {
  const baseClass = 'flex items-center text-xs font-medium px-2 py-1 rounded-full'
  
  const statusClasses = {
    good: 'text-green-700 bg-green-100 dark:text-green-300 dark:bg-green-900/20',
    warning: 'text-yellow-700 bg-yellow-100 dark:text-yellow-300 dark:bg-yellow-900/20',
    critical: 'text-red-700 bg-red-100 dark:text-red-300 dark:bg-red-900/20',
    danger: 'text-red-700 bg-red-100 dark:text-red-300 dark:bg-red-900/20'
  }
  
  return `${baseClass} ${statusClasses[status.value] || statusClasses.danger}`
})
</script>

<style scoped>
.gauge-chart {
  @apply flex items-center justify-center;
}

.gauge-svg {
  @apply drop-shadow-sm;
}

.gauge-progress {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.gauge-background {
  @apply opacity-30;
}

.gauge-tick {
  @apply opacity-70;
}

.gauge-label {
  @apply font-medium;
}

.gauge-center {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

/* Animation for value changes */
@keyframes gauge-fill {
  from {
    stroke-dashoffset: var(--circumference);
  }
  to {
    stroke-dashoffset: var(--progress-offset);
  }
}

.gauge-progress.animated {
  animation: gauge-fill 1.5s ease-out;
}
</style>