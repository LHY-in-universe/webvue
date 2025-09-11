<template>
  <Teleport to="body">
    <div 
      class="notification-container fixed top-4 right-4 z-50 space-y-2 max-w-sm w-full"
      role="region"
      aria-live="polite"
      aria-label="Notifications"
    >
      <TransitionGroup name="notification" tag="div">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="[
            'notification-item relative overflow-hidden rounded-lg shadow-lg border p-4',
            'transform transition-all duration-300',
            getNotificationClasses(notification.type)
          ]"
        >
          <!-- Progress Bar -->
          <div 
            v-if="notification.showProgress && notification.duration"
            class="absolute top-0 left-0 h-1 bg-current opacity-30 transition-all ease-linear"
            :style="{ 
              width: `${getProgressWidth(notification)}%`,
              transitionDuration: `${notification.duration}ms`
            }"
          ></div>

          <div class="flex items-start space-x-3">
            <!-- Icon -->
            <div class="flex-shrink-0 mt-0.5">
              <component 
                :is="getIcon(notification.type)"
                :class="getIconClasses(notification.type)"
                class="w-5 h-5"
              />
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <!-- Title -->
              <h4 
                v-if="notification.title"
                class="text-sm font-semibold"
                :class="getTitleClasses(notification.type)"
              >
                {{ notification.title }}
              </h4>

              <!-- Message -->
              <p 
                :class="[
                  'text-sm',
                  getMessageClasses(notification.type),
                  notification.title ? 'mt-1' : ''
                ]"
              >
                {{ notification.message }}
              </p>

              <!-- Actions -->
              <div v-if="notification.actions?.length" class="mt-3 flex space-x-2">
                <button
                  v-for="action in notification.actions"
                  :key="action.label"
                  @click="handleAction(notification, action)"
                  class="text-xs font-medium underline hover:no-underline focus:outline-none"
                  :class="getActionClasses(notification.type)"
                >
                  {{ action.label }}
                </button>
              </div>
            </div>

            <!-- Close Button -->
            <div class="flex-shrink-0">
              <button
                @click="removeNotification(notification.id)"
                class="rounded-md p-1.5 hover:bg-black/5 focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors"
                :class="getCloseButtonClasses(notification.type)"
              >
                <XMarkIcon class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

// Notification store
const notifications = ref([])

// Auto-removal timers
const timers = new Map()

const getIcon = (type) => {
  const icons = {
    success: CheckCircleIcon,
    warning: ExclamationTriangleIcon,
    error: XCircleIcon,
    info: InformationCircleIcon
  }
  return icons[type] || InformationCircleIcon
}

const getNotificationClasses = (type) => {
  const classes = {
    success: 'bg-green-50 border-green-200 text-green-800 dark:bg-green-900/20 dark:border-green-800 dark:text-green-300',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800 dark:bg-yellow-900/20 dark:border-yellow-800 dark:text-yellow-300',
    error: 'bg-red-50 border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-800 dark:text-red-300',
    info: 'bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-900/20 dark:border-blue-800 dark:text-blue-300'
  }
  return classes[type] || classes.info
}

const getIconClasses = (type) => {
  const classes = {
    success: 'text-green-500 dark:text-green-400',
    warning: 'text-yellow-500 dark:text-yellow-400',
    error: 'text-red-500 dark:text-red-400',
    info: 'text-blue-500 dark:text-blue-400'
  }
  return classes[type] || classes.info
}

const getTitleClasses = (type) => {
  const classes = {
    success: 'text-green-900 dark:text-green-200',
    warning: 'text-yellow-900 dark:text-yellow-200',
    error: 'text-red-900 dark:text-red-200',
    info: 'text-blue-900 dark:text-blue-200'
  }
  return classes[type] || classes.info
}

const getMessageClasses = (type) => {
  const classes = {
    success: 'text-green-700 dark:text-green-300',
    warning: 'text-yellow-700 dark:text-yellow-300',
    error: 'text-red-700 dark:text-red-300',
    info: 'text-blue-700 dark:text-blue-300'
  }
  return classes[type] || classes.info
}

const getActionClasses = (type) => {
  const classes = {
    success: 'text-green-800 hover:text-green-900 dark:text-green-300 dark:hover:text-green-200',
    warning: 'text-yellow-800 hover:text-yellow-900 dark:text-yellow-300 dark:hover:text-yellow-200',
    error: 'text-red-800 hover:text-red-900 dark:text-red-300 dark:hover:text-red-200',
    info: 'text-blue-800 hover:text-blue-900 dark:text-blue-300 dark:hover:text-blue-200'
  }
  return classes[type] || classes.info
}

const getCloseButtonClasses = (type) => {
  const classes = {
    success: 'text-green-500 hover:text-green-600 focus:ring-green-600 dark:text-green-400 dark:hover:text-green-300',
    warning: 'text-yellow-500 hover:text-yellow-600 focus:ring-yellow-600 dark:text-yellow-400 dark:hover:text-yellow-300',
    error: 'text-red-500 hover:text-red-600 focus:ring-red-600 dark:text-red-400 dark:hover:text-red-300',
    info: 'text-blue-500 hover:text-blue-600 focus:ring-blue-600 dark:text-blue-400 dark:hover:text-blue-300'
  }
  return classes[type] || classes.info
}

const getProgressWidth = (notification) => {
  if (!notification.duration || !notification.createdAt) return 100
  
  const elapsed = Date.now() - notification.createdAt
  const remaining = Math.max(0, notification.duration - elapsed)
  return (remaining / notification.duration) * 100
}

const addNotification = (notification) => {
  const id = Date.now() + Math.random()
  const newNotification = {
    id,
    type: 'info',
    duration: 5000,
    showProgress: true,
    createdAt: Date.now(),
    ...notification
  }
  
  notifications.value.push(newNotification)
  
  // Auto-remove after duration
  if (newNotification.duration > 0) {
    const timer = setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
    
    timers.set(id, timer)
  }
  
  return id
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
  
  // Clear timer
  if (timers.has(id)) {
    clearTimeout(timers.get(id))
    timers.delete(id)
  }
}

const clearAll = () => {
  notifications.value = []
  timers.forEach(timer => clearTimeout(timer))
  timers.clear()
}

const handleAction = (notification, action) => {
  if (typeof action.handler === 'function') {
    action.handler(notification)
  }
  
  if (action.closeOnClick !== false) {
    removeNotification(notification.id)
  }
}

// Cleanup timers on unmount
onUnmounted(() => {
  timers.forEach(timer => clearTimeout(timer))
  timers.clear()
})

// Expose methods for external use
defineExpose({
  addNotification,
  removeNotification,
  clearAll
})
</script>

<style scoped>
/* Notification transitions */
.notification-enter-active {
  transition: all 0.3s ease-out;
}

.notification-leave-active {
  transition: all 0.3s ease-in;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.notification-move {
  transition: transform 0.3s ease;
}

/* Enhanced shadows */
.notification-item {
  backdrop-filter: blur(8px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
</style>