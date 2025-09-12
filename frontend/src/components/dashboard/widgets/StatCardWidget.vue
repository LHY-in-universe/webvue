<template>
  <div class="stat-card-widget h-full p-4 flex flex-col justify-center">
    <div class="text-center">
      <!-- Value Display -->
      <div class="mb-2">
        <div :class="valueClasses">
          {{ formattedValue }}
        </div>
        <div v-if="config.subtitle" class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          {{ config.subtitle }}
        </div>
      </div>

      <!-- Trend Indicator -->
      <div v-if="config.showTrend && trend !== null && trend !== undefined" class="flex items-center justify-center">
        <component 
          :is="trendIcon" 
          :class="trendClasses"
          class="w-4 h-4 mr-1"
        />
        <span :class="trendClasses" class="text-sm font-medium">
          {{ Math.abs(trend).toFixed(1) }}%
        </span>
        <span class="text-xs text-gray-500 dark:text-gray-400 ml-1">
          {{ trendLabel }}
        </span>
      </div>

      <!-- Progress Bar -->
      <div v-if="config.showProgress && config.max" class="mt-4">
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            class="bg-blue-500 h-2 rounded-full transition-all duration-500"
            :style="{ width: `${progressPercentage}%` }"
          ></div>
        </div>
        <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
          <span>0</span>
          <span>{{ formatValue(config.max) }}</span>
        </div>
      </div>

      <!-- Comparison -->
      <div v-if="config.comparison && config.comparisonValue" class="mt-3 text-xs text-gray-500 dark:text-gray-400">
        vs {{ config.comparison }}: {{ formatValue(config.comparisonValue) }}
        <span v-if="comparisonDiff" :class="comparisonClasses">
          ({{ comparisonDiff > 0 ? '+' : '' }}{{ comparisonDiff.toFixed(1) }}%)
        </span>
      </div>

      <!-- Status Indicator -->
      <div v-if="config.status" class="mt-2">
        <span :class="statusClasses" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium">
          <div :class="statusDotClasses" class="w-2 h-2 rounded-full mr-1"></div>
          {{ config.status }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  ArrowUpIcon,
  ArrowDownIcon,
  MinusIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  widget: {
    type: Object,
    required: true
  },
  config: {
    type: Object,
    required: true
  },
  value: {
    type: [Number, String],
    default: 0
  },
  trend: {
    type: Number,
    default: null
  },
  unit: {
    type: String,
    default: ''
  },
  format: {
    type: String,
    default: 'number',
    validator: value => ['number', 'currency', 'percentage', 'bytes', 'duration'].includes(value)
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: String
})

// Computed properties
const valueClasses = computed(() => {
  const size = props.config.size || 'large'
  const color = props.config.color || 'default'
  
  const sizeClasses = {
    small: 'text-xl',
    medium: 'text-2xl', 
    large: 'text-3xl',
    xlarge: 'text-4xl'
  }
  
  const colorClasses = {
    default: 'text-gray-900 dark:text-white',
    primary: 'text-blue-600 dark:text-blue-400',
    success: 'text-green-600 dark:text-green-400',
    warning: 'text-yellow-600 dark:text-yellow-400',
    danger: 'text-red-600 dark:text-red-400'
  }
  
  return `font-bold ${sizeClasses[size]} ${colorClasses[color]}`
})

const trendIcon = computed(() => {
  if (props.trend > 0) return ArrowUpIcon
  if (props.trend < 0) return ArrowDownIcon
  return MinusIcon
})

const trendClasses = computed(() => {
  if (props.trend > 0) return 'text-green-600 dark:text-green-400'
  if (props.trend < 0) return 'text-red-600 dark:text-red-400'
  return 'text-gray-500 dark:text-gray-400'
})

const trendLabel = computed(() => {
  return props.config.trendLabel || 'vs last period'
})

const progressPercentage = computed(() => {
  if (!props.config.max || !props.value) return 0
  return Math.min(100, (Number(props.value) / props.config.max) * 100)
})

const comparisonDiff = computed(() => {
  if (!props.config.comparisonValue || !props.value) return null
  const current = Number(props.value)
  const comparison = Number(props.config.comparisonValue)
  if (comparison === 0) return null
  return ((current - comparison) / comparison) * 100
})

const comparisonClasses = computed(() => {
  if (!comparisonDiff.value) return ''
  if (comparisonDiff.value > 0) return 'text-green-600 dark:text-green-400'
  if (comparisonDiff.value < 0) return 'text-red-600 dark:text-red-400'
  return ''
})

const statusClasses = computed(() => {
  const status = props.config.status?.toLowerCase()
  const statusVariants = {
    success: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    info: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    default: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
  }
  
  return statusVariants[status] || statusVariants.default
})

const statusDotClasses = computed(() => {
  const status = props.config.status?.toLowerCase()
  const dotVariants = {
    success: 'bg-green-400',
    warning: 'bg-yellow-400',
    error: 'bg-red-400',
    info: 'bg-blue-400',
    default: 'bg-gray-400'
  }
  
  return dotVariants[status] || dotVariants.default
})

const formattedValue = computed(() => {
  return formatValue(props.value)
})

// Methods
const formatValue = (value) => {
  if (value === null || value === undefined) return '-'
  
  const numValue = Number(value)
  if (isNaN(numValue)) return value
  
  switch (props.format) {
    case 'currency':
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: props.config.currency || 'USD'
      }).format(numValue)
    
    case 'percentage':
      return `${numValue.toFixed(props.config.precision || 1)}%`
    
    case 'bytes':
      return formatBytes(numValue)
    
    case 'duration':
      return formatDuration(numValue)
    
    case 'number':
    default:
      // Handle large numbers with K/M/B suffixes
      if (numValue >= 1000000000) {
        return `${(numValue / 1000000000).toFixed(1)}B${props.unit}`
      } else if (numValue >= 1000000) {
        return `${(numValue / 1000000).toFixed(1)}M${props.unit}`
      } else if (numValue >= 1000) {
        return `${(numValue / 1000).toFixed(1)}K${props.unit}`
      } else {
        const precision = props.config.precision ?? (numValue % 1 === 0 ? 0 : 1)
        return `${numValue.toFixed(precision)}${props.unit}`
      }
  }
}

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`
}

const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`
  } else if (minutes > 0) {
    return `${minutes}m ${secs}s`
  } else {
    return `${secs}s`
  }
}
</script>

<style scoped>
.stat-card-widget {
  @apply select-none;
}

/* Animations for value changes */
.stat-card-widget .font-bold {
  @apply transition-all duration-300 ease-in-out;
}
</style>