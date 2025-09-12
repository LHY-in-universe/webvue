<template>
  <div v-if="hasError" class="error-boundary">
    <div class="error-container">
      <div class="error-icon">
        <svg class="w-16 h-16 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
        </svg>
      </div>
      
      <div class="error-content">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          Something went wrong
        </h2>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          {{ errorMessage || 'An unexpected error occurred. Please try refreshing the page.' }}
        </p>
        
        <!-- Error Details (Collapsed by default) -->
        <div v-if="showDetails" class="error-details">
          <button 
            @click="toggleDetails"
            class="flex items-center text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 mb-3"
          >
            <svg 
              :class="['w-4 h-4 mr-2 transform transition-transform', detailsExpanded ? 'rotate-90' : '']"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
            Error Details
          </button>
          
          <div v-if="detailsExpanded" class="error-stack">
            <pre class="text-xs text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-4 rounded-lg overflow-auto max-h-40">{{ errorInfo }}</pre>
          </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="error-actions">
          <button 
            @click="retry"
            class="btn-primary mr-3"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            Try Again
          </button>
          
          <button 
            @click="goHome"
            class="btn-secondary mr-3"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
            </svg>
            Go Home
          </button>
          
          <button 
            @click="reportError"
            class="btn-ghost"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
            Report Issue
          </button>
        </div>
      </div>
    </div>
  </div>
  
  <slot v-else></slot>
</template>

<script setup>
import { ref, onErrorCaptured, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useResponsive } from '@/composables/useResponsive'

const router = useRouter()
const { isMobile } = useResponsive()

const hasError = ref(false)
const errorMessage = ref('')
const errorInfo = ref('')
const errorId = ref('')
const errorTimestamp = ref('')
const detailsExpanded = ref(false)
const errorCount = ref(0)

const props = defineProps({
  showDetails: {
    type: Boolean,
    default: true
  },
  onError: {
    type: Function,
    default: null
  },
  maxRetries: {
    type: Number,
    default: 3
  },
  fallbackComponent: {
    type: [Object, Function],
    default: null
  },
  enableAnalytics: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['error', 'retry'])

onErrorCaptured((error, instance, info) => {
  errorCount.value++
  
  // Generate unique error ID and timestamp
  errorId.value = `ERR_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  errorTimestamp.value = new Date().toISOString()
  
  hasError.value = true
  errorMessage.value = error.message
  errorInfo.value = error.stack || error.toString()
  
  // Enhanced error information
  const errorDetails = {
    id: errorId.value,
    timestamp: errorTimestamp.value,
    message: error.message,
    stack: error.stack,
    component: instance?.$options.name || 'Unknown',
    route: router.currentRoute.value.fullPath,
    userAgent: navigator.userAgent,
    viewport: { width: window.innerWidth, height: window.innerHeight },
    count: errorCount.value,
    retryable: errorCount.value < props.maxRetries
  }
  
  // Analytics tracking
  if (props.enableAnalytics && typeof window.gtag === 'function') {
    window.gtag('event', 'exception', {
      description: error.message,
      fatal: false,
      custom_map: {
        error_id: errorId.value,
        component: errorDetails.component
      }
    })
  }
  
  // Call custom error handler if provided
  if (props.onError) {
    props.onError(error, instance, info, errorDetails)
  }
  
  emit('error', { error, instance, info, details: errorDetails })
  
  console.group(`🚨 ErrorBoundary [${errorId.value}]`)
  console.error('Error:', error)
  console.error('Component:', instance)
  console.error('Info:', info)
  console.error('Details:', errorDetails)
  console.groupEnd()
  
  return false
})

const retry = () => {
  hasError.value = false
  errorMessage.value = ''
  errorInfo.value = ''
  detailsExpanded.value = false
  emit('retry')
}

const goHome = () => {
  router.push('/')
}

const reportError = () => {
  const subject = `Error Report: ${errorMessage.value}`
  const body = `Error Details:\n\n${errorInfo.value}\n\nPage: ${window.location.href}\nUser Agent: ${navigator.userAgent}\nTimestamp: ${new Date().toISOString()}`
  
  const mailto = `mailto:support@example.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
  window.open(mailto, '_blank')
}

const toggleDetails = () => {
  detailsExpanded.value = !detailsExpanded.value
}
</script>

<style scoped>
.error-boundary {
  @apply min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4;
}

.error-container {
  @apply max-w-lg w-full;
}

.error-icon {
  @apply flex justify-center mb-6;
  animation: shake 0.5s ease-in-out;
}

.error-content {
  @apply text-center;
}

.error-stack {
  @apply text-left;
  animation: slideDown 0.3s ease-out;
}

.error-actions {
  @apply flex flex-wrap justify-center items-center gap-2;
}

.btn-primary {
  @apply inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200;
}

.btn-secondary {
  @apply inline-flex items-center px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg transition-colors duration-200;
}

.btn-ghost {
  @apply inline-flex items-center px-4 py-2 text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800 font-medium rounded-lg transition-colors duration-200;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>