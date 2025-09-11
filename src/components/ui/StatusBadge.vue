<template>
  <span :class="badgeClasses">
    <component v-if="icon" :is="icon" class="w-3 h-3 mr-1" />
    <slot>{{ label }}</slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  status: {
    type: String,
    required: true,
    validator: value => [
      'success', 'error', 'warning', 'info', 'pending', 
      'active', 'inactive', 'completed', 'failed', 'running'
    ].includes(value)
  },
  variant: {
    type: String,
    default: 'filled',
    validator: value => ['filled', 'outlined', 'subtle'].includes(value)
  },
  size: {
    type: String,
    default: 'sm',
    validator: value => ['xs', 'sm', 'md'].includes(value)
  },
  icon: [Object, Function],
  rounded: {
    type: Boolean,
    default: true
  }
})

const badgeClasses = computed(() => {
  const base = 'inline-flex items-center font-medium'
  
  // Size classes
  const sizes = {
    xs: 'px-2 py-0.5 text-xs',
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm'
  }
  
  // Status color mappings
  const statusColors = {
    success: {
      filled: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      outlined: 'border border-green-300 text-green-600 dark:border-green-600 dark:text-green-400',
      subtle: 'bg-green-50 text-green-600 dark:bg-green-900/20 dark:text-green-400'
    },
    error: {
      filled: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
      outlined: 'border border-red-300 text-red-600 dark:border-red-600 dark:text-red-400',
      subtle: 'bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400'
    },
    warning: {
      filled: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      outlined: 'border border-yellow-300 text-yellow-600 dark:border-yellow-600 dark:text-yellow-400',
      subtle: 'bg-yellow-50 text-yellow-600 dark:bg-yellow-900/20 dark:text-yellow-400'
    },
    info: {
      filled: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
      outlined: 'border border-blue-300 text-blue-600 dark:border-blue-600 dark:text-blue-400',
      subtle: 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400'
    },
    pending: {
      filled: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200',
      outlined: 'border border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400',
      subtle: 'bg-gray-50 text-gray-600 dark:bg-gray-900/20 dark:text-gray-400'
    },
    active: {
      filled: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      outlined: 'border border-green-300 text-green-600 dark:border-green-600 dark:text-green-400',
      subtle: 'bg-green-50 text-green-600 dark:bg-green-900/20 dark:text-green-400'
    },
    inactive: {
      filled: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200',
      outlined: 'border border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400',
      subtle: 'bg-gray-50 text-gray-600 dark:bg-gray-900/20 dark:text-gray-400'
    },
    completed: {
      filled: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      outlined: 'border border-green-300 text-green-600 dark:border-green-600 dark:text-green-400',
      subtle: 'bg-green-50 text-green-600 dark:bg-green-900/20 dark:text-green-400'
    },
    failed: {
      filled: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
      outlined: 'border border-red-300 text-red-600 dark:border-red-600 dark:text-red-400',
      subtle: 'bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400'
    },
    running: {
      filled: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
      outlined: 'border border-blue-300 text-blue-600 dark:border-blue-600 dark:text-blue-400',
      subtle: 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400'
    }
  }

  const roundedClass = props.rounded ? 'rounded-full' : 'rounded-md'
  
  return [
    base,
    sizes[props.size],
    statusColors[props.status]?.[props.variant] || statusColors.info[props.variant],
    roundedClass
  ].join(' ')
})
</script>