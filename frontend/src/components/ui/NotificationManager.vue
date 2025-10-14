<template>
  <div class="fixed top-4 right-4 z-50 space-y-3 max-w-sm">
    <TransitionGroup
      name="notification"
      tag="div"
      class="space-y-3"
    >
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="[
          'w-full relative overflow-hidden',
          'bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl',
          'shadow-2xl shadow-black/10 dark:shadow-black/30',
          'border border-white/20 dark:border-slate-700/50',
          'rounded-2xl',
          'transform transition-all duration-500 ease-out',
          'hover:scale-[1.02] hover:shadow-3xl',
          // Success styling
          notification.type === 'success' && [
            'border-l-4 border-l-emerald-500',
            'bg-gradient-to-r from-emerald-50/80 to-white/80',
            'dark:from-emerald-900/20 dark:to-slate-800/80',
            'shadow-emerald-500/10'
          ],
          // Error styling  
          notification.type === 'error' && [
            'border-l-4 border-l-red-500',
            'bg-gradient-to-r from-red-50/80 to-white/80',
            'dark:from-red-900/20 dark:to-slate-800/80',
            'shadow-red-500/10'
          ],
          // Warning styling
          notification.type === 'warning' && [
            'border-l-4 border-l-amber-500',
            'bg-gradient-to-r from-amber-50/80 to-white/80',
            'dark:from-amber-900/20 dark:to-slate-800/80',
            'shadow-amber-500/10'
          ],
          // Info styling
          notification.type === 'info' && [
            'border-l-4 border-l-blue-500',
            'bg-gradient-to-r from-blue-50/80 to-white/80',
            'dark:from-blue-900/20 dark:to-slate-800/80',
            'shadow-blue-500/10'
          ]
        ]"
      >
        <!-- Animated border effect -->
        <div 
          :class="[
            'absolute inset-0 rounded-2xl opacity-20',
            notification.type === 'success' && 'bg-gradient-to-r from-emerald-400 to-emerald-600',
            notification.type === 'error' && 'bg-gradient-to-r from-red-400 to-red-600',
            notification.type === 'warning' && 'bg-gradient-to-r from-amber-400 to-amber-600',
            notification.type === 'info' && 'bg-gradient-to-r from-blue-400 to-blue-600'
          ]"
        ></div>
        
        <div class="relative p-5">
          <div class="flex items-start gap-4">
            <!-- Icon with enhanced styling -->
            <div class="flex-shrink-0">
              <div 
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center',
                  'shadow-lg backdrop-blur-sm',
                  notification.type === 'success' && 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400',
                  notification.type === 'error' && 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400',
                  notification.type === 'warning' && 'bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400',
                  notification.type === 'info' && 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                ]"
              >
                <!-- Success Icon -->
                <CheckCircleIcon 
                  v-if="notification.type === 'success'"
                  class="h-6 w-6"
                />
                <!-- Error Icon -->
                <XCircleIcon 
                  v-else-if="notification.type === 'error'"
                  class="h-6 w-6"
                />
                <!-- Warning Icon -->
                <ExclamationTriangleIcon 
                  v-else-if="notification.type === 'warning'"
                  class="h-6 w-6"
                />
                <!-- Info Icon -->
                <InformationCircleIcon 
                  v-else
                  class="h-6 w-6"
                />
              </div>
            </div>
            
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-1">
                {{ notification.title || getDefaultTitle(notification.type) }}
              </h4>
              <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                {{ notification.message }}
              </p>
              
              <!-- Enhanced progress bar -->
              <div 
                v-if="notification.showProgress && notification.duration > 0"
                class="mt-3"
              >
                <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mb-1">
                  <span>Progress</span>
                  <span>{{ Math.round(notification.progress || 0) }}%</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
                  <div 
                    :class="[
                      'h-2 rounded-full transition-all duration-300 ease-out',
                      notification.type === 'success' && 'bg-gradient-to-r from-emerald-400 to-emerald-600',
                      notification.type === 'error' && 'bg-gradient-to-r from-red-400 to-red-600',
                      notification.type === 'warning' && 'bg-gradient-to-r from-amber-400 to-amber-600',
                      notification.type === 'info' && 'bg-gradient-to-r from-blue-400 to-blue-600'
                    ]"
                    :style="{ width: `${notification.progress || 0}%` }"
                  ></div>
                </div>
              </div>
            </div>
            
            <!-- Close button with enhanced styling -->
            <div class="flex-shrink-0">
              <button
                v-if="notification.dismissible !== false"
                @click="dismiss(notification.id)"
                class="group p-1.5 rounded-lg transition-all duration-200 hover:bg-gray-100 dark:hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              >
                <XMarkIcon class="h-4 w-4 text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 transition-colors" />
                <span class="sr-only">Close notification</span>
              </button>
            </div>
          </div>
        </div>
        
        <!-- Auto-dismiss progress bar -->
        <div 
          v-if="notification.duration > 0 && !notification.showProgress"
          class="absolute bottom-0 left-0 right-0 h-1 bg-gray-200 dark:bg-gray-700"
        >
          <div 
            :class="[
              'h-1 transition-all ease-linear',
              notification.type === 'success' && 'bg-emerald-500',
              notification.type === 'error' && 'bg-red-500',
              notification.type === 'warning' && 'bg-amber-500',
              notification.type === 'info' && 'bg-blue-500'
            ]"
            :style="{ 
              width: '100%',
              animation: `shrink ${notification.duration}ms linear forwards`
            }"
          ></div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { 
  CheckCircleIcon, 
  XCircleIcon, 
  ExclamationTriangleIcon, 
  InformationCircleIcon,
  XMarkIcon 
} from '@heroicons/vue/24/outline'
import { useNotifications, registerNotificationManager } from '@/composables/useNotifications'

// Notification state
const notifications = ref([])
const timers = new Map()

// Notification manager methods
const show = (options) => {
  const notification = {
    id: options.id || Date.now() + Math.random(),
    timestamp: Date.now(),
    duration: options.duration || 5000,
    dismissible: options.dismissible !== false,
    showProgress: options.showProgress || false,
    progress: 0,
    ...options
  }
  
  notifications.value.unshift(notification)
  
  // Auto dismiss if duration > 0
  if (notification.duration > 0) {
    const timer = setTimeout(() => {
      dismiss(notification.id)
    }, notification.duration)
    timers.set(notification.id, timer)
  }
  
  return notification.id
}

const dismiss = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
  
  // Clear timer
  const timer = timers.get(id)
  if (timer) {
    clearTimeout(timer)
    timers.delete(id)
  }
}

const update = (id, updates) => {
  const notification = notifications.value.find(n => n.id === id)
  if (notification) {
    Object.assign(notification, updates)
  }
}

const clear = () => {
  // Clear all timers
  timers.forEach(timer => clearTimeout(timer))
  timers.clear()
  
  // Clear notifications
  notifications.value = []
}

// Helper function
const getDefaultTitle = (type) => {
  const titles = {
    success: 'Success',
    error: 'Error', 
    warning: 'Warning',
    info: 'Information'
  }
  return titles[type] || 'Notification'
}

// Register the notification manager
onMounted(() => {
  registerNotificationManager({
    show,
    dismiss,
    update,
    clear
  })
})

// Cleanup on unmount
onUnmounted(() => {
  clear()
})
</script>

<style scoped>
/* Enhanced notification animations */
.notification-enter-active {
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.notification-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.6, 1);
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.8);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.8);
}

.notification-move {
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.6, 1);
}

/* Auto-dismiss progress bar animation */
@keyframes shrink {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

/* Hover effects */
.notification-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Enhanced shadow effects */
.shadow-3xl {
  box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
}

/* Glass morphism effect */
.backdrop-blur-xl {
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}

/* Custom scrollbar for notification container */
.notification-container::-webkit-scrollbar {
  width: 4px;
}

.notification-container::-webkit-scrollbar-track {
  background: transparent;
}

.notification-container::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.3);
  border-radius: 2px;
}

.notification-container::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.5);
}

/* Dark mode enhancements */
@media (prefers-color-scheme: dark) {
  .notification-item {
    border-color: rgba(255, 255, 255, 0.1);
  }
}

/* Responsive design */
@media (max-width: 640px) {
  .notification-container {
    left: 1rem;
    right: 1rem;
    max-width: none;
  }
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .notification-enter-active,
  .notification-leave-active,
  .notification-move {
    transition: opacity 0.2s ease;
  }
  
  .notification-enter-from,
  .notification-leave-to {
    transform: none;
  }
}
</style>