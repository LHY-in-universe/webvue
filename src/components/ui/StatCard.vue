<template>
  <Card 
    :class="[
      'stat-card interactive-element micro-lift',
      clickable && 'cursor-pointer hover-glow-primary',
      animated && 'animate-fade-in-up',
      colorClasses
    ]"
    @click="handleClick"
  >
    <div class="p-6">
      <!-- Icon and Header -->
      <div class="flex items-start justify-between mb-4">
        <div class="flex items-center space-x-3">
          <!-- Icon -->
          <div 
            :class="[
              'flex items-center justify-center rounded-xl glass-effect micro-bounce',
              iconSizeClasses,
              iconColorClasses
            ]"
          >
            <component :is="icon" :class="iconClasses" v-if="icon" />
            <slot name="icon" v-else />
          </div>
          
          <!-- Title -->
          <div>
            <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400 text-shadow-soft">
              {{ title }}
            </h3>
            <p class="text-xs text-gray-500 dark:text-gray-500" v-if="subtitle">
              {{ subtitle }}
            </p>
          </div>
        </div>
        
        <!-- Badge -->
        <div v-if="badge" :class="badgeClasses">
          {{ badge }}
        </div>
      </div>
      
      <!-- Value -->
      <div class="mb-3">
        <div v-if="loading" class="flex items-center space-x-2">
          <div class="animate-pulse bg-gray-300 dark:bg-gray-600 h-8 w-16 rounded"></div>
          <span v-if="unit" class="text-lg font-medium text-gray-400 dark:text-gray-500">
            {{ unit }}
          </span>
        </div>
        <div v-else class="flex items-baseline space-x-2">
          <span 
            :class="[valueClasses, variant === 'primary' && 'text-gradient']"
            :title="tooltip"
          >
            {{ formattedValue || placeholder }}
          </span>
          <span v-if="unit" class="text-lg font-medium text-gray-600 dark:text-gray-400">
            {{ unit }}
          </span>
          <!-- Status Indicator -->
          <div 
            v-if="status" 
            :class="[
              'w-2 h-2 rounded-full ml-2',
              statusIndicatorClasses
            ]"
            :title="`Status: ${status}`"
          ></div>
        </div>
      </div>
      
      <!-- Progress/Trend -->
      <div v-if="progress !== null || trend" class="mb-4">
        <!-- Progress Bar -->
        <ProgressBar 
          v-if="progress !== null"
          :percentage="progress"
          :variant="variant"
          size="sm"
          :show-percentage="false"
          :animated="animated"
        />
        
        <!-- Trend Indicator -->
        <div v-if="trend" class="flex items-center space-x-1 mt-2">
          <component :is="trendIcon" :class="trendIconClasses" class="w-4 h-4" />
          <span :class="trendTextClasses" class="text-sm font-medium">
            {{ Math.abs(trend).toFixed(2) }}%
          </span>
          <span class="text-xs text-gray-500 dark:text-gray-400">
            {{ trendLabel }}
          </span>
        </div>
        
        <!-- Comparison Indicator -->
        <div v-if="comparison" class="flex items-center space-x-1 mt-2">
          <component :is="comparisonIcon" :class="comparisonIconClasses" class="w-4 h-4" />
          <span :class="comparisonTextClasses" class="text-sm font-medium">
            {{ comparison.value }}
          </span>
          <span class="text-xs text-gray-500 dark:text-gray-400">
            {{ comparison.label }}
          </span>
        </div>
      </div>
      
      <!-- Description -->
      <div v-if="description || $slots.description">
        <slot name="description">
          <p class="text-xs text-gray-600 dark:text-gray-400">
            {{ description }}
          </p>
        </slot>
      </div>
      
      <!-- Action -->
      <div v-if="$slots.action" class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <slot name="action" />
      </div>
    </div>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import Card from './Card.vue'
import ProgressBar from './ProgressBar.vue'
import { 
  ArrowUpIcon, 
  ArrowDownIcon,
  MinusIcon 
} from '@heroicons/vue/24/outline'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  value: {
    type: [Number, String],
    required: true
  },
  unit: {
    type: String,
    default: ''
  },
  precision: {
    type: Number,
    default: 2
  },
  icon: {
    type: [Object, String, Function],
    default: null
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  progress: {
    type: Number,
    default: null
  },
  trend: {
    type: Number,
    default: null
  },
  trendLabel: {
    type: String,
    default: 'vs last period'
  },
  badge: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  clickable: {
    type: Boolean,
    default: false
  },
  animated: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: '--'
  },
  comparison: {
    type: Object,
    default: null
    // { value: number, label: string, type: 'increase' | 'decrease' | 'neutral' }
  },
  status: {
    type: String,
    default: null,
    validator: (value) => value === null || ['healthy', 'warning', 'critical'].includes(value)
  },
  tooltip: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click'])

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value.toFixed(props.precision)
  }
  return props.value
})

const colorClasses = computed(() => {
  const variants = {
    default: 'bg-white dark:bg-slate-800 border-gray-200 dark:border-slate-700',
    primary: 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800',
    success: 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800',
    warning: 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800',
    danger: 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800',
    info: 'bg-cyan-50 dark:bg-cyan-900/20 border-cyan-200 dark:border-cyan-800'
  }
  return variants[props.variant]
})

const iconSizeClasses = computed(() => {
  const sizes = {
    sm: 'w-10 h-10',
    md: 'w-12 h-12',
    lg: 'w-14 h-14'
  }
  return sizes[props.size]
})

const iconColorClasses = computed(() => {
  const variants = {
    default: 'bg-gray-100 dark:bg-gray-700',
    primary: 'bg-blue-100 dark:bg-blue-800',
    success: 'bg-green-100 dark:bg-green-800',
    warning: 'bg-yellow-100 dark:bg-yellow-800',
    danger: 'bg-red-100 dark:bg-red-800',
    info: 'bg-cyan-100 dark:bg-cyan-800'
  }
  return variants[props.variant]
})

const iconClasses = computed(() => {
  const sizes = {
    sm: 'w-5 h-5',
    md: 'w-6 h-6',
    lg: 'w-7 h-7'
  }
  
  const variants = {
    default: 'text-gray-600 dark:text-gray-300',
    primary: 'text-blue-600 dark:text-blue-300',
    success: 'text-green-600 dark:text-green-300',
    warning: 'text-yellow-600 dark:text-yellow-300',
    danger: 'text-red-600 dark:text-red-300',
    info: 'text-cyan-600 dark:text-cyan-300'
  }
  
  return `${sizes[props.size]} ${variants[props.variant]}`
})

const valueClasses = computed(() => {
  const sizes = {
    sm: 'text-2xl',
    md: 'text-3xl',
    lg: 'text-4xl'
  }
  return `${sizes[props.size]} font-bold text-gray-900 dark:text-white`
})

const badgeClasses = computed(() => {
  return `px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-xs font-medium rounded-md`
})

const trendIcon = computed(() => {
  if (props.trend > 0) return ArrowUpIcon
  if (props.trend < 0) return ArrowDownIcon
  return MinusIcon
})

const trendIconClasses = computed(() => {
  if (props.trend > 0) return 'text-green-500'
  if (props.trend < 0) return 'text-red-500'
  return 'text-gray-400'
})

const trendTextClasses = computed(() => {
  if (props.trend > 0) return 'text-green-600 dark:text-green-400'
  if (props.trend < 0) return 'text-red-600 dark:text-red-400'
  return 'text-gray-500'
})

const statusIndicatorClasses = computed(() => {
  const indicators = {
    healthy: 'bg-green-500',
    warning: 'bg-yellow-500',
    critical: 'bg-red-500'
  }
  return indicators[props.status] || 'bg-gray-400'
})

const comparisonIcon = computed(() => {
  if (!props.comparison) return null
  
  const type = props.comparison.type
  if (type === 'increase') return ArrowUpIcon
  if (type === 'decrease') return ArrowDownIcon
  return MinusIcon
})

const comparisonIconClasses = computed(() => {
  if (!props.comparison) return ''
  
  const type = props.comparison.type
  if (type === 'increase') return 'text-green-500'
  if (type === 'decrease') return 'text-red-500'
  return 'text-gray-400'
})

const comparisonTextClasses = computed(() => {
  if (!props.comparison) return ''
  
  const type = props.comparison.type
  if (type === 'increase') return 'text-green-600 dark:text-green-400'
  if (type === 'decrease') return 'text-red-600 dark:text-red-400'
  return 'text-gray-500'
})

const handleClick = () => {
  if (props.clickable) {
    emit('click')
  }
}
</script>

<style scoped>
.stat-card {
  @apply border;
}

.stat-card:hover {
  @apply shadow-lg;
}
</style>