<template>
  <Teleport to="body">
    <div class="toast-container fixed top-4 right-4 z-50 flex flex-col gap-3 max-w-sm w-full pointer-events-none">
      <TransitionGroup name="toast" tag="div">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="[
            'toast-base pointer-events-auto',
            toastClasses[notification.type]
          ]"
          @click="handleToastClick(notification)"
        >
          <!-- Progress Bar -->
          <div
            v-if="notification.autoClose && notification.progress !== undefined"
            :class="[
              'toast-progress absolute top-0 left-0 h-1 transition-all duration-100 ease-linear',
              progressClasses[notification.type]
            ]"
            :style="{ width: `${notification.progress}%` }"
          ></div>

          <div class="flex items-start space-x-3">
            <!-- Icon -->
            <div :class="['flex-shrink-0 mt-0.5', iconClasses[notification.type]]">
              <component :is="getIcon(notification.type)" class="w-5 h-5" />
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div v-if="notification.title" class="font-medium text-gray-900 dark:text-white text-sm">
                {{ notification.title }}
              </div>
              <div class="text-gray-700 dark:text-gray-300 text-sm mt-1">
                {{ notification.message }}
              </div>
              
              <!-- Actions -->
              <div v-if="notification.actions && notification.actions.length" class="flex gap-2 mt-3">
                <button
                  v-for="(action, index) in notification.actions"
                  :key="index"
                  :class="[
                    'text-xs font-medium px-2 py-1 rounded transition-colors duration-200',
                    actionClasses[notification.type]
                  ]"
                  @click.stop="handleActionClick(notification, action)"
                >
                  {{ action.label }}
                </button>
              </div>
            </div>

            <!-- Close Button -->
            <button
              v-if="notification.closable !== false"
              @click.stop="removeNotification(notification.id)"
              class="flex-shrink-0 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
            >
              <XMarkIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { onMounted, onUnmounted, computed } from 'vue'
import { useUIStore } from '@/stores/ui'
import { 
  CheckCircleIcon, 
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const uiStore = useUIStore()

const notifications = computed(() => uiStore.getNotifications)

const toastClasses = {
  success: 'bg-white dark:bg-gray-800 border-l-4 border-l-success-500 shadow-large',
  error: 'bg-white dark:bg-gray-800 border-l-4 border-l-danger-500 shadow-large',
  warning: 'bg-white dark:bg-gray-800 border-l-4 border-l-warning-500 shadow-large',
  info: 'bg-white dark:bg-gray-800 border-l-4 border-l-info-500 shadow-large'
}

const iconClasses = {
  success: 'text-success-500',
  error: 'text-danger-500',
  warning: 'text-warning-500',
  info: 'text-info-500'
}

const progressClasses = {
  success: 'bg-success-500',
  error: 'bg-danger-500',
  warning: 'bg-warning-500',
  info: 'bg-info-500'
}

const actionClasses = {
  success: 'text-success-700 hover:bg-success-50 dark:text-success-400 dark:hover:bg-success-900/20',
  error: 'text-danger-700 hover:bg-danger-50 dark:text-danger-400 dark:hover:bg-danger-900/20',
  warning: 'text-warning-700 hover:bg-warning-50 dark:text-warning-400 dark:hover:bg-warning-900/20',
  info: 'text-info-700 hover:bg-info-50 dark:text-info-400 dark:hover:bg-info-900/20'
}

const getIcon = (type) => {
  const icons = {
    success: CheckCircleIcon,
    error: ExclamationCircleIcon,
    warning: ExclamationTriangleIcon,
    info: InformationCircleIcon
  }
  return icons[type] || icons.info
}

const removeNotification = (id) => {
  uiStore.removeNotification(id)
}

const handleToastClick = (notification) => {
  if (notification.onClick) {
    notification.onClick(notification)
  }
}

const handleActionClick = (notification, action) => {
  if (action.handler) {
    action.handler(notification)
  }
  
  if (action.closeOnClick !== false) {
    removeNotification(notification.id)
  }
}

// Progress tracking for auto-close notifications
let progressIntervals = new Map()

const startProgressTracking = (notification) => {
  if (!notification.autoClose || !notification.duration) return
  
  const startTime = notification.timestamp || Date.now()
  const duration = notification.duration
  
  const interval = setInterval(() => {
    const elapsed = Date.now() - startTime
    const progress = Math.max(0, Math.min(100, 100 - (elapsed / duration) * 100))
    
    // Update progress in the notification object
    notification.progress = progress
    
    if (progress <= 0) {
      clearInterval(interval)
      progressIntervals.delete(notification.id)
    }
  }, 50) // Update every 50ms for smooth animation
  
  progressIntervals.set(notification.id, interval)
}

const stopProgressTracking = (id) => {
  const interval = progressIntervals.get(id)
  if (interval) {
    clearInterval(interval)
    progressIntervals.delete(id)
  }
}

// Watch for new notifications
let lastNotificationCount = 0
const checkForNewNotifications = () => {
  const currentNotifications = notifications.value
  
  if (currentNotifications.length > lastNotificationCount) {
    // New notifications added
    const newNotifications = currentNotifications.slice(lastNotificationCount)
    newNotifications.forEach(notification => {
      if (notification.autoClose) {
        startProgressTracking(notification)
      }
    })
  } else if (currentNotifications.length < lastNotificationCount) {
    // Notifications removed - clean up progress tracking
    progressIntervals.forEach((interval, id) => {
      const exists = currentNotifications.find(n => n.id === id)
      if (!exists) {
        stopProgressTracking(id)
      }
    })
  }
  
  lastNotificationCount = currentNotifications.length
}

onMounted(() => {
  // Check for existing notifications
  lastNotificationCount = notifications.value.length
  notifications.value.forEach(notification => {
    if (notification.autoClose) {
      startProgressTracking(notification)
    }
  })
  
  // Watch for changes (simple polling approach)
  const watcher = setInterval(checkForNewNotifications, 100)
  
  onUnmounted(() => {
    clearInterval(watcher)
    // Clean up all progress intervals
    progressIntervals.forEach(interval => clearInterval(interval))
    progressIntervals.clear()
  })
})
</script>

<style scoped>
.toast-base {
  @apply relative overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 p-4 backdrop-blur-sm;
  @apply transform transition-all duration-300 ease-out;
}

.toast-progress {
  border-radius: 0 0 4px 0;
}

/* Toast Transitions */
.toast-enter-active,
.toast-leave-active {
  @apply transition-all duration-300 ease-out;
}

.toast-enter-from {
  @apply opacity-0 transform translate-x-full scale-95;
}

.toast-leave-to {
  @apply opacity-0 transform translate-x-full scale-95;
}

.toast-move {
  @apply transition-transform duration-300 ease-out;
}

/* Container positioning */
.toast-container {
  /* Ensure it's above most elements but below modals */
  z-index: 40;
}

/* Mobile adjustments */
@media (max-width: 639px) {
  .toast-container {
    @apply left-4 right-4 max-w-none;
  }
}
</style>