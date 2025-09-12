<template>
  <div 
    :class="[
      'card-base p-6',
      {
        'card-interactive': interactive,
        'card-elevated': elevated
      }
    ]"
    @click="handleClick"
  >
    <!-- Header Section -->
    <div v-if="showHeader" class="flex items-start justify-between mb-4">
      <div class="flex items-center space-x-3">
        <!-- Icon -->
        <div 
          v-if="icon || status"
          :class="[
            'flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center',
            statusClasses.background
          ]"
        >
          <component 
            v-if="icon" 
            :is="icon" 
            :class="['w-5 h-5', statusClasses.text]" 
          />
          <div 
            v-else-if="status"
            :class="['w-2 h-2 rounded-full', statusClasses.indicator]"
          ></div>
        </div>
        
        <!-- Title & Subtitle -->
        <div class="min-w-0 flex-1">
          <h3 
            v-if="title" 
            class="text-heading-3 text-gray-900 dark:text-white truncate"
          >
            {{ title }}
          </h3>
          <p 
            v-if="subtitle" 
            class="text-body-sm text-gray-600 dark:text-gray-400 mt-1"
          >
            {{ subtitle }}
          </p>
        </div>
      </div>
      
      <!-- Badge -->
      <div v-if="badge" :class="['px-2 py-1 rounded-full text-xs font-medium', badgeClasses]">
        {{ badge }}
      </div>
    </div>

    <!-- Content Section -->
    <div class="space-y-4">
      <!-- Main Content -->
      <div v-if="$slots.default" class="text-body text-gray-700 dark:text-gray-300">
        <slot />
      </div>

      <!-- Stats/Metrics -->
      <div v-if="stats && stats.length" class="grid grid-cols-2 gap-4">
        <div 
          v-for="(stat, index) in stats" 
          :key="index" 
          class="text-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
        >
          <div class="text-heading-2 font-bold text-gray-900 dark:text-white">
            {{ stat.value }}
          </div>
          <div class="text-body-sm text-gray-600 dark:text-gray-400 mt-1">
            {{ stat.label }}
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div v-if="progress !== null" class="space-y-2">
        <div class="flex justify-between text-body-sm">
          <span class="text-gray-600 dark:text-gray-400">{{ progressLabel || 'Progress' }}</span>
          <span class="font-medium text-gray-900 dark:text-white">{{ progress }}%</span>
        </div>
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            :class="[
              'h-2 rounded-full transition-all duration-500',
              progressColorClass
            ]"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Footer Actions -->
    <div v-if="$slots.actions" class="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <slot name="actions" />
      </div>
    </div>

    <!-- Timestamp -->
    <div v-if="timestamp" class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
      <p class="text-caption text-gray-500 dark:text-gray-400">
        {{ formatTimestamp(timestamp) }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  subtitle: String,
  icon: [Object, Function, String],
  status: {
    type: String,
    validator: value => ['success', 'warning', 'danger', 'info'].includes(value)
  },
  badge: String,
  badgeVariant: {
    type: String,
    default: 'primary',
    validator: value => ['primary', 'success', 'warning', 'danger', 'info', 'gray'].includes(value)
  },
  interactive: {
    type: Boolean,
    default: false
  },
  elevated: {
    type: Boolean,
    default: true
  },
  stats: Array,
  progress: {
    type: Number,
    default: null
  },
  progressLabel: String,
  progressVariant: {
    type: String,
    default: 'primary',
    validator: value => ['primary', 'success', 'warning', 'danger'].includes(value)
  },
  timestamp: [String, Date, Number]
})

const emit = defineEmits(['click'])

const showHeader = computed(() => {
  return props.title || props.subtitle || props.icon || props.status || props.badge
})

const statusClasses = computed(() => {
  const variants = {
    success: {
      background: 'bg-success-100 dark:bg-success-900/20',
      text: 'text-success-600 dark:text-success-400',
      indicator: 'bg-success-500'
    },
    warning: {
      background: 'bg-warning-100 dark:bg-warning-900/20',
      text: 'text-warning-600 dark:text-warning-400',
      indicator: 'bg-warning-500'
    },
    danger: {
      background: 'bg-danger-100 dark:bg-danger-900/20',
      text: 'text-danger-600 dark:text-danger-400',
      indicator: 'bg-danger-500'
    },
    info: {
      background: 'bg-info-100 dark:bg-info-900/20',
      text: 'text-info-600 dark:text-info-400',
      indicator: 'bg-info-500'
    }
  }
  
  return variants[props.status] || variants.info
})

const badgeClasses = computed(() => {
  const variants = {
    primary: 'bg-primary-100 text-primary-800 dark:bg-primary-900/20 dark:text-primary-400',
    success: 'bg-success-100 text-success-800 dark:bg-success-900/20 dark:text-success-400',
    warning: 'bg-warning-100 text-warning-800 dark:bg-warning-900/20 dark:text-warning-400',
    danger: 'bg-danger-100 text-danger-800 dark:bg-danger-900/20 dark:text-danger-400',
    info: 'bg-info-100 text-info-800 dark:bg-info-900/20 dark:text-info-400',
    gray: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
  }
  
  return variants[props.badgeVariant] || variants.primary
})

const progressColorClass = computed(() => {
  const variants = {
    primary: 'bg-primary-600',
    success: 'bg-success-600',
    warning: 'bg-warning-600',
    danger: 'bg-danger-600'
  }
  
  return variants[props.progressVariant] || variants.primary
})

const handleClick = (event) => {
  if (props.interactive) {
    emit('click', event)
  }
}

const formatTimestamp = (timestamp) => {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (seconds < 60) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>