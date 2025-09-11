<template>
  <Transition name="alert" appear>
    <div
      v-if="visible"
      :class="alertClasses"
      role="alert"
      :aria-live="ariaLive"
    >
      <!-- Icon -->
      <div v-if="showIcon" class="flex-shrink-0">
        <component
          :is="alertIcon"
          :class="iconClasses"
          class="h-5 w-5"
        />
      </div>

      <!-- Content -->
      <div class="flex-1 min-w-0">
        <!-- Title -->
        <div v-if="title || $slots.title" :class="titleClasses">
          <slot name="title">{{ title }}</slot>
        </div>

        <!-- Message -->
        <div v-if="message || $slots.default" :class="messageClasses">
          <slot>{{ message }}</slot>
        </div>

        <!-- Actions -->
        <div v-if="actions?.length || $slots.actions" class="mt-3 flex space-x-2">
          <slot name="actions">
            <Button
              v-for="action in actions"
              :key="action.key"
              :variant="action.variant || 'ghost'"
              :size="action.size || 'xs'"
              @click="handleActionClick(action)"
            >
              {{ action.label }}
            </Button>
          </slot>
        </div>
      </div>

      <!-- Close Button -->
      <div v-if="closable" class="flex-shrink-0 ml-4">
        <button
          @click="close"
          :class="closeButtonClasses"
          aria-label="Close alert"
        >
          <XMarkIcon class="h-4 w-4" />
        </button>
      </div>

      <!-- Progress Bar (for auto-dismiss) -->
      <div
        v-if="autoDismiss && showProgress && progress > 0"
        class="absolute bottom-0 left-0 h-1 bg-current opacity-30 transition-all duration-100 ease-linear"
        :style="{ width: `${progress}%` }"
      ></div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import Button from './Button.vue'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: value => ['success', 'error', 'warning', 'info'].includes(value)
  },
  variant: {
    type: String,
    default: 'filled',
    validator: value => ['filled', 'outlined', 'subtle'].includes(value)
  },
  title: String,
  message: String,
  showIcon: {
    type: Boolean,
    default: true
  },
  icon: [Object, Function],
  closable: {
    type: Boolean,
    default: false
  },
  autoDismiss: {
    type: [Boolean, Number],
    default: false
  },
  showProgress: {
    type: Boolean,
    default: false
  },
  actions: {
    type: Array,
    default: () => []
  },
  border: {
    type: Boolean,
    default: false
  },
  rounded: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  }
})

const emit = defineEmits(['close', 'action'])

const visible = ref(true)
const progress = ref(100)
let dismissTimer = null
let progressTimer = null

const alertIcon = computed(() => {
  if (props.icon) return props.icon
  
  const icons = {
    success: CheckCircleIcon,
    error: ExclamationCircleIcon,
    warning: ExclamationTriangleIcon,
    info: InformationCircleIcon
  }
  
  return icons[props.type] || icons.info
})

const ariaLive = computed(() => {
  return props.type === 'error' ? 'assertive' : 'polite'
})

const alertClasses = computed(() => {
  const base = 'relative flex items-start space-x-3 p-4 transition-all duration-200'
  
  // Size classes
  const sizes = {
    sm: 'text-sm p-3',
    md: 'text-sm p-4',
    lg: 'text-base p-5'
  }
  
  // Variant and type combinations
  const variantClasses = {
    filled: {
      success: 'bg-green-50 border-green-200 text-green-800 dark:bg-green-900/20 dark:border-green-800 dark:text-green-200',
      error: 'bg-red-50 border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-800 dark:text-red-200',
      warning: 'bg-yellow-50 border-yellow-200 text-yellow-800 dark:bg-yellow-900/20 dark:border-yellow-800 dark:text-yellow-200',
      info: 'bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-900/20 dark:border-blue-800 dark:text-blue-200'
    },
    outlined: {
      success: 'bg-white border-green-300 text-green-700 dark:bg-gray-800 dark:border-green-600 dark:text-green-300',
      error: 'bg-white border-red-300 text-red-700 dark:bg-gray-800 dark:border-red-600 dark:text-red-300',
      warning: 'bg-white border-yellow-300 text-yellow-700 dark:bg-gray-800 dark:border-yellow-600 dark:text-yellow-300',
      info: 'bg-white border-blue-300 text-blue-700 dark:bg-gray-800 dark:border-blue-600 dark:text-blue-300'
    },
    subtle: {
      success: 'bg-white border-gray-200 text-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-white',
      error: 'bg-white border-gray-200 text-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-white',
      warning: 'bg-white border-gray-200 text-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-white',
      info: 'bg-white border-gray-200 text-gray-900 dark:bg-gray-800 dark:border-gray-700 dark:text-white'
    }
  }
  
  const borderClass = props.border ? 'border' : 'border-0'
  const roundedClass = props.rounded ? 'rounded-lg' : ''
  
  return [
    base,
    sizes[props.size],
    variantClasses[props.variant][props.type],
    borderClass,
    roundedClass
  ].join(' ')
})

const iconClasses = computed(() => {
  if (props.variant === 'subtle') {
    const colors = {
      success: 'text-green-600',
      error: 'text-red-600',
      warning: 'text-yellow-600',
      info: 'text-blue-600'
    }
    return colors[props.type] || colors.info
  }
  return '' // Use inherited color from parent
})

const titleClasses = computed(() => {
  const sizes = {
    sm: 'text-sm font-medium',
    md: 'text-sm font-medium',
    lg: 'text-base font-medium'
  }
  
  return `${sizes[props.size]} ${props.variant === 'filled' ? 'text-current' : 'text-gray-900 dark:text-white'}`
})

const messageClasses = computed(() => {
  const baseClass = props.title ? 'mt-1' : ''
  const sizeClass = props.size === 'lg' ? 'text-base' : 'text-sm'
  
  if (props.variant === 'subtle') {
    return `${baseClass} ${sizeClass} text-gray-600 dark:text-gray-400`
  }
  
  return `${baseClass} ${sizeClass} opacity-90`
})

const closeButtonClasses = computed(() => {
  const base = 'rounded-md p-1 focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors'
  
  if (props.variant === 'subtle') {
    return `${base} text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 focus:ring-gray-500`
  }
  
  const colors = {
    success: 'text-green-500 hover:text-green-700 focus:ring-green-500',
    error: 'text-red-500 hover:text-red-700 focus:ring-red-500',
    warning: 'text-yellow-500 hover:text-yellow-700 focus:ring-yellow-500',
    info: 'text-blue-500 hover:text-blue-700 focus:ring-blue-500'
  }
  
  return `${base} ${colors[props.type] || colors.info}`
})

const close = () => {
  visible.value = false
  clearTimers()
  emit('close')
}

const handleActionClick = (action) => {
  action.handler?.()
  emit('action', action)
  
  if (action.dismiss !== false) {
    close()
  }
}

const clearTimers = () => {
  if (dismissTimer) {
    clearTimeout(dismissTimer)
    dismissTimer = null
  }
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
}

const startAutoDismiss = () => {
  if (!props.autoDismiss) return
  
  const duration = typeof props.autoDismiss === 'number' ? props.autoDismiss : 5000
  
  if (props.showProgress) {
    const startTime = Date.now()
    progressTimer = setInterval(() => {
      const elapsed = Date.now() - startTime
      progress.value = Math.max(0, 100 - (elapsed / duration) * 100)
      
      if (progress.value <= 0) {
        clearInterval(progressTimer)
      }
    }, 50)
  }
  
  dismissTimer = setTimeout(() => {
    close()
  }, duration)
}

// Watch for changes in autoDismiss prop
watch(() => props.autoDismiss, (newValue) => {
  clearTimers()
  if (newValue) {
    startAutoDismiss()
  }
}, { immediate: true })

onMounted(() => {
  if (props.autoDismiss) {
    startAutoDismiss()
  }
})

onUnmounted(() => {
  clearTimers()
})
</script>

<style scoped>
/* Alert animations */
.alert-enter-active {
  transition: all 0.3s ease-out;
}

.alert-leave-active {
  transition: all 0.3s ease-in;
}

.alert-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.alert-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}
</style>