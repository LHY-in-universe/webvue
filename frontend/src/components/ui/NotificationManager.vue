<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 pointer-events-none">
      <div :class="containerClasses">
        <TransitionGroup
          name="notification"
          tag="div"
          class="space-y-3"
        >
          <div
            v-for="notification in visibleNotifications"
            :key="notification.id"
            :class="notificationClasses(notification)"
            @click="handleNotificationClick(notification)"
            @mouseenter="pauseAutoClose(notification.id)"
            @mouseleave="resumeAutoClose(notification.id)"
          >
            <!-- Icon -->
            <div v-if="notification.icon || getDefaultIcon(notification.type)" class="flex-shrink-0">
              <component
                :is="notification.icon || getDefaultIcon(notification.type)"
                :class="iconClasses(notification.type)"
              />
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div v-if="notification.title" class="text-sm font-medium text-gray-900 dark:text-white">
                {{ notification.title }}
              </div>
              <div :class="messageClasses(notification.title)">
                {{ notification.message }}
              </div>
              <div v-if="notification.actions?.length" class="mt-3 flex space-x-2">
                <Button
                  v-for="action in notification.actions"
                  :key="action.key"
                  :variant="action.variant || 'ghost'"
                  size="xs"
                  @click.stop="handleActionClick(notification, action)"
                >
                  {{ action.label }}
                </Button>
              </div>
            </div>

            <!-- Close Button -->
            <div v-if="notification.dismissible !== false" class="flex-shrink-0">
              <button
                @click.stop="dismiss(notification.id)"
                class="rounded-md text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <XMarkIcon class="h-4 w-4" />
              </button>
            </div>

            <!-- Progress Bar -->
            <div
              v-if="notification.duration && notification.showProgress"
              class="absolute bottom-0 left-0 h-1 bg-current opacity-20 transition-all duration-100 ease-linear"
              :style="{ width: `${getProgress(notification)}%` }"
            ></div>
          </div>
        </TransitionGroup>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Button from './Button.vue'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  position: {
    type: String,
    default: 'top-right',
    validator: value => [
      'top-left', 'top-center', 'top-right',
      'bottom-left', 'bottom-center', 'bottom-right',
      'center'
    ].includes(value)
  },
  maxNotifications: {
    type: Number,
    default: 5
  },
  defaultDuration: {
    type: Number,
    default: 5000
  }
})

const notifications = ref([])
const timers = ref(new Map())
const pausedTimers = ref(new Set())

const visibleNotifications = computed(() => {
  return notifications.value.slice(0, props.maxNotifications)
})

const containerClasses = computed(() => {
  const positions = {
    'top-left': 'top-4 left-4',
    'top-center': 'top-4 left-1/2 transform -translate-x-1/2',
    'top-right': 'top-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'bottom-center': 'bottom-4 left-1/2 transform -translate-x-1/2',
    'bottom-right': 'bottom-4 right-4',
    'center': 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2'
  }

  return `fixed ${positions[props.position]} max-w-sm w-full z-50`
})

const notificationClasses = (notification) => {
  const base = 'relative pointer-events-auto flex items-start p-4 rounded-lg shadow-lg backdrop-blur-sm border transition-all duration-200 hover:scale-105 cursor-pointer overflow-hidden'

  const variants = {
    success: 'bg-green-50/90 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-800 dark:text-green-200',
    error: 'bg-red-50/90 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-800 dark:text-red-200',
    warning: 'bg-yellow-50/90 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800 text-yellow-800 dark:text-yellow-200',
    info: 'bg-blue-50/90 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200',
    default: 'bg-white/90 dark:bg-gray-800/90 border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white'
  }

  return `${base} ${variants[notification.type] || variants.default}`
}

const iconClasses = (type) => {
  const base = 'h-5 w-5'
  const colors = {
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500',
    default: 'text-gray-500'
  }

  return `${base} ${colors[type] || colors.default}`
}

const messageClasses = (hasTitle) => {
  return hasTitle
    ? 'text-sm text-gray-700 dark:text-gray-300'
    : 'text-sm font-medium text-gray-900 dark:text-white'
}

const getDefaultIcon = (type) => {
  const icons = {
    success: CheckCircleIcon,
    error: ExclamationCircleIcon,
    warning: ExclamationTriangleIcon,
    info: InformationCircleIcon,
    default: InformationCircleIcon
  }

  return icons[type] || icons.default
}

const getProgress = (notification) => {
  if (!notification.startTime || !notification.duration) return 0
  
  const elapsed = Date.now() - notification.startTime
  const progress = Math.max(0, Math.min(100, (elapsed / notification.duration) * 100))
  
  return 100 - progress
}

// Notification management methods
const show = (options) => {
  const notification = {
    id: Date.now() + Math.random(),
    type: options.type || 'default',
    title: options.title,
    message: options.message || '',
    icon: options.icon,
    duration: options.duration ?? props.defaultDuration,
    dismissible: options.dismissible !== false,
    showProgress: options.showProgress !== false,
    actions: options.actions || [],
    startTime: Date.now(),
    onClick: options.onClick,
    onDismiss: options.onDismiss,
    ...options
  }

  notifications.value.unshift(notification)

  // Auto-dismiss if duration is set
  if (notification.duration > 0) {
    scheduleAutoClose(notification.id, notification.duration)
  }

  return notification.id
}

const dismiss = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    const notification = notifications.value[index]
    notifications.value.splice(index, 1)
    clearTimer(id)
    notification.onDismiss?.(notification)
  }
}

const dismissAll = () => {
  notifications.value.forEach(n => n.onDismiss?.(n))
  notifications.value.splice(0)
  timers.value.clear()
  pausedTimers.value.clear()
}

const scheduleAutoClose = (id, duration) => {
  const timer = setTimeout(() => {
    if (!pausedTimers.value.has(id)) {
      dismiss(id)
    }
  }, duration)
  
  timers.value.set(id, timer)
}

const clearTimer = (id) => {
  const timer = timers.value.get(id)
  if (timer) {
    clearTimeout(timer)
    timers.value.delete(id)
  }
  pausedTimers.value.delete(id)
}

const pauseAutoClose = (id) => {
  pausedTimers.value.add(id)
}

const resumeAutoClose = (id) => {
  if (pausedTimers.value.has(id)) {
    pausedTimers.value.delete(id)
    const notification = notifications.value.find(n => n.id === id)
    if (notification && notification.duration > 0) {
      clearTimer(id)
      const elapsed = Date.now() - notification.startTime
      const remaining = Math.max(0, notification.duration - elapsed)
      if (remaining > 0) {
        scheduleAutoClose(id, remaining)
      } else {
        dismiss(id)
      }
    }
  }
}

const handleNotificationClick = (notification) => {
  if (notification.onClick) {
    notification.onClick(notification)
  }
}

const handleActionClick = (notification, action) => {
  action.handler?.(notification, action)
  if (action.dismiss !== false) {
    dismiss(notification.id)
  }
}

// Convenience methods
const success = (message, options = {}) => show({ ...options, type: 'success', message })
const error = (message, options = {}) => show({ ...options, type: 'error', message })
const warning = (message, options = {}) => show({ ...options, type: 'warning', message })
const info = (message, options = {}) => show({ ...options, type: 'info', message })

// Lifecycle
onUnmounted(() => {
  timers.value.forEach(timer => clearTimeout(timer))
})

// Expose methods for programmatic usage
defineExpose({
  show,
  success,
  error,
  warning,
  info,
  dismiss,
  dismissAll
})
</script>

<style scoped>
/* Notification animations */
.notification-enter-active {
  transition: all 0.3s ease-out;
}

.notification-leave-active {
  transition: all 0.3s ease-in;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>