<template>
  <div class="progress-container">
    <!-- Label and Value -->
    <div v-if="label || showPercentage || showValue" class="flex justify-between items-center mb-2">
      <span v-if="label" class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ label }}</span>
      <div class="flex items-center space-x-2">
        <span v-if="showValue" class="text-sm text-gray-500 dark:text-gray-400 font-mono">
          {{ formatValue(value) }}{{ unit }}
        </span>
        <span v-else-if="showPercentage" class="text-sm text-gray-500 dark:text-gray-400">
          {{ Math.round(percentage) }}%
        </span>
      </div>
    </div>
    
    <!-- Progress Bar -->
    <div class="progress-track" :class="sizeClasses" :title="tooltip">
      <!-- Background Track -->
      <div class="progress-background"></div>
      
      <!-- Buffer/Loading progress (for streaming) -->
      <div 
        v-if="bufferValue !== null"
        class="progress-buffer"
        :style="{ width: `${Math.min(100, Math.max(0, bufferPercentage))}%` }"
      ></div>
      
      <!-- Main Progress Fill -->
      <div 
        class="progress-fill transition-all duration-500 ease-out"
        :class="[colorClasses, animatedClasses]"
        :style="progressStyle"
        role="progressbar"
        :aria-valuenow="value || percentage"
        :aria-valuemin="min"
        :aria-valuemax="max || 100"
        :aria-valuetext="ariaText"
      >
        <!-- Optional gradient overlay -->
        <div v-if="gradient" class="absolute inset-0 bg-gradient-to-r from-transparent to-white/20 rounded-full"></div>
        
        <!-- Striped pattern -->
        <div v-if="striped" class="progress-stripes"></div>
        
        <!-- Optional pulse animation -->
        <div v-if="animated && (percentage > 0 || value > 0)" class="progress-pulse" :class="colorClasses"></div>
        
        <!-- Inner label -->
        <span v-if="showInnerLabel && (percentage > 15 || value > 15)" class="progress-inner-label">
          {{ showValue ? `${formatValue(value)}${unit}` : `${Math.round(percentage)}%` }}
        </span>
      </div>
      
      <!-- Multiple segments (for segmented progress) -->
      <div v-if="segments > 1" class="absolute inset-0 flex">
        <div
          v-for="segment in segments"
          :key="segment"
          class="flex-1 border-r border-white dark:border-gray-800 last:border-r-0"
          :class="segment <= currentSegment ? 'opacity-100' : 'opacity-30'"
        ></div>
      </div>
      
      <!-- Steps indicators -->
      <div v-if="steps && steps.length > 0" class="absolute inset-0 flex items-center">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="absolute transform -translate-x-1/2"
          :style="{ left: `${(step.value / (max || 100)) * 100}%` }"
        >
          <div :class="getStepClasses(step)" :title="step.label">
            <component v-if="step.icon" :is="step.icon" class="w-2 h-2" />
            <div v-else class="w-1.5 h-1.5 bg-current rounded-full"></div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Status message -->
    <div v-if="status" class="mt-1 text-xs" :class="statusClasses">
      {{ status }}
    </div>
    
    <!-- Additional Info -->
    <div v-if="$slots.info || info" class="mt-2">
      <slot name="info">
        <p class="text-xs text-gray-500 dark:text-gray-400">{{ info }}</p>
      </slot>
    </div>
    
    <!-- Multiple progress bars (stacked) -->
    <div v-if="multipleValues && multipleValues.length > 0" class="mt-3 space-y-2">
      <div
        v-for="(item, index) in multipleValues"
        :key="index"
        class="flex items-center space-x-2"
      >
        <div class="flex-1">
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs text-gray-600 dark:text-gray-400">{{ item.label }}</span>
            <span class="text-xs text-gray-500 dark:text-gray-500 font-mono">
              {{ formatValue(item.value) }}{{ unit }}
            </span>
          </div>
          <div class="h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              :class="[
                'h-full rounded-full transition-all duration-300',
                getMultipleBarColor(item.color || variant)
              ]"
              :style="{ width: `${Math.min(100, Math.max(0, (item.value / (max || 100)) * 100))}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // Value-based props
  value: {
    type: Number,
    default: null
  },
  max: {
    type: Number,
    default: 100
  },
  min: {
    type: Number,
    default: 0
  },
  unit: {
    type: String,
    default: ''
  },
  
  // Legacy percentage prop (for backward compatibility)
  percentage: {
    type: Number,
    default: null,
    validator: (value) => value === null || (value >= 0 && value <= 100)
  },
  
  // Display props
  label: {
    type: String,
    default: ''
  },
  info: {
    type: String,
    default: ''
  },
  showPercentage: {
    type: Boolean,
    default: true
  },
  showValue: {
    type: Boolean,
    default: false
  },
  showInnerLabel: {
    type: Boolean,
    default: false
  },
  
  // Styling props
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  
  // Animation and effects
  animated: {
    type: Boolean,
    default: false
  },
  gradient: {
    type: Boolean,
    default: false
  },
  striped: {
    type: Boolean,
    default: false
  },
  
  // Advanced features
  bufferValue: {
    type: Number,
    default: null
  },
  segments: {
    type: Number,
    default: 1,
    validator: (value) => value >= 1
  },
  steps: {
    type: Array,
    default: () => []
  },
  multipleValues: {
    type: Array,
    default: () => []
  },
  status: {
    type: String,
    default: ''
  },
  tooltip: {
    type: String,
    default: ''
  }
})

// Core computed properties
const percentage = computed(() => {
  if (props.percentage !== null) {
    return props.percentage
  }
  if (props.value !== null) {
    return Math.min(100, Math.max(0, ((props.value - props.min) / (props.max - props.min)) * 100))
  }
  return 0
})

const bufferPercentage = computed(() => {
  if (props.bufferValue === null) return 0
  return Math.min(100, Math.max(0, ((props.bufferValue - props.min) / (props.max - props.min)) * 100))
})

const currentSegment = computed(() => {
  return Math.ceil((percentage.value / 100) * props.segments)
})

const progressStyle = computed(() => ({
  width: `${Math.min(100, Math.max(0, percentage.value))}%`
}))

const ariaText = computed(() => {
  if (props.showValue && props.value !== null) {
    return `${formatValue(props.value)}${props.unit} of ${formatValue(props.max)}${props.unit}`
  }
  return `${Math.round(percentage.value)}% complete`
})

// Size classes
const sizeClasses = computed(() => {
  const sizes = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4'
  }
  return `${sizes[props.size]} bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden relative`
})

// Color classes
const colorClasses = computed(() => {
  const colors = {
    primary: 'bg-blue-600 dark:bg-blue-500',
    success: 'bg-green-600 dark:bg-green-500',
    warning: 'bg-yellow-600 dark:bg-yellow-500',
    danger: 'bg-red-600 dark:bg-red-500',
    info: 'bg-cyan-600 dark:bg-cyan-500'
  }
  return colors[props.variant]
})

// Animation classes
const animatedClasses = computed(() => {
  return props.animated ? 'relative overflow-hidden' : ''
})

// Status classes
const statusClasses = computed(() => {
  const baseClasses = 'text-xs'
  if (props.status.toLowerCase().includes('error') || props.status.toLowerCase().includes('failed')) {
    return `${baseClasses} text-red-600 dark:text-red-400`
  }
  if (props.status.toLowerCase().includes('success') || props.status.toLowerCase().includes('complete')) {
    return `${baseClasses} text-green-600 dark:text-green-400`
  }
  if (props.status.toLowerCase().includes('warning')) {
    return `${baseClasses} text-yellow-600 dark:text-yellow-400`
  }
  return `${baseClasses} text-gray-600 dark:text-gray-400`
})

// Methods
const formatValue = (value) => {
  if (value === null || value === undefined) return '0'
  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`
  if (value >= 1000) return `${(value / 1000).toFixed(1)}K`
  return value.toString()
}

const getStepClasses = (step) => {
  const baseClasses = 'flex items-center justify-center w-4 h-4 rounded-full text-xs border-2'
  const isActive = props.value >= step.value
  const isCompleted = props.value > step.value
  
  if (isCompleted) {
    return `${baseClasses} bg-green-600 border-green-600 text-white dark:bg-green-500 dark:border-green-500`
  }
  if (isActive) {
    return `${baseClasses} bg-blue-600 border-blue-600 text-white dark:bg-blue-500 dark:border-blue-500`
  }
  return `${baseClasses} bg-gray-200 border-gray-300 text-gray-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-400`
}

const getMultipleBarColor = (color) => {
  const colors = {
    primary: 'bg-blue-600 dark:bg-blue-500',
    success: 'bg-green-600 dark:bg-green-500',
    warning: 'bg-yellow-600 dark:bg-yellow-500',
    danger: 'bg-red-600 dark:bg-red-500',
    info: 'bg-cyan-600 dark:bg-cyan-500',
    secondary: 'bg-gray-600 dark:bg-gray-500',
    purple: 'bg-purple-600 dark:bg-purple-500',
    pink: 'bg-pink-600 dark:bg-pink-500',
    indigo: 'bg-indigo-600 dark:bg-indigo-500'
  }
  return colors[color] || colors.primary
}
</script>

<style scoped>
.progress-container {
  @apply w-full;
}

.progress-track {
  @apply relative;
}

.progress-background {
  @apply absolute inset-0 bg-gray-200 dark:bg-gray-700 rounded-full;
}

.progress-buffer {
  @apply absolute top-0 left-0 h-full bg-gray-300 dark:bg-gray-600 rounded-full opacity-50;
}

.progress-fill {
  @apply h-full rounded-full relative z-10;
}

.progress-stripes {
  @apply absolute inset-0 bg-gradient-to-r;
  background-image: repeating-linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.1) 0,
    rgba(255, 255, 255, 0.1) 10px,
    transparent 10px,
    transparent 20px
  );
  animation: stripes-move 1s linear infinite;
}

@keyframes stripes-move {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 40px 0;
  }
}

.progress-pulse {
  @apply absolute top-0 right-0 h-full w-8 opacity-50 rounded-full;
  animation: pulse-right 2s ease-in-out infinite;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
}

@keyframes pulse-right {
  0%, 100% {
    transform: translateX(-100%);
    opacity: 0;
  }
  50% {
    transform: translateX(0);
    opacity: 1;
  }
}

.progress-inner-label {
  @apply absolute inset-0 flex items-center justify-center text-xs font-medium text-white drop-shadow-sm;
}

/* Enhanced hover effects */
.progress-fill:hover {
  @apply brightness-110;
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .progress-stripes,
  .progress-pulse {
    animation: none;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .progress-background {
    @apply border border-gray-400 dark:border-gray-500;
  }
  
  .progress-fill {
    @apply border border-current;
  }
}

/* Focus styles for interactive elements */
.progress-track:focus-within {
  @apply ring-2 ring-blue-500 ring-offset-2 rounded-full;
}

/* Print styles */
@media print {
  .progress-stripes,
  .progress-pulse {
    display: none;
  }
}
</style>