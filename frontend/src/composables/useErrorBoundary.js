import { ref, onErrorCaptured } from 'vue'
import { useUIStore } from '@/stores/ui'

export function useErrorBoundary() {
  const uiStore = useUIStore()
  const error = ref(null)
  const hasError = ref(false)
  const errorInfo = ref(null)

  const captureError = (err, instance, info) => {
    error.value = err
    hasError.value = true
    errorInfo.value = {
      componentStack: info,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href
    }

    // Log error to console for debugging
    console.error('Error captured by boundary:', err)
    console.error('Component info:', info)
    console.error('Error info:', errorInfo.value)

    // Send error notification to user
    uiStore.addNotification({
      type: 'error',
      title: 'Application Error',
      message: 'Something went wrong. The error has been logged.',
      duration: 5000
    })

    // In production, you might want to send this to an error reporting service
    if (import.meta.env.PROD) {
      // Example: Sentry.captureException(err, { extra: errorInfo.value })
      reportError(err, errorInfo.value)
    }

    return false // Don't propagate to parent
  }

  const reportError = async (error, info) => {
    try {
      // This would typically send to your error reporting service
      console.log('Reporting error to service:', { error: error.message, info })
      
      // Example API call to error reporting endpoint
      // await fetch('/api/errors', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     message: error.message,
      //     stack: error.stack,
      //     info
      //   })
      // })
    } catch (reportingError) {
      console.error('Failed to report error:', reportingError)
    }
  }

  const resetError = () => {
    error.value = null
    hasError.value = false
    errorInfo.value = null
  }

  const retry = (retryFunction) => {
    resetError()
    if (typeof retryFunction === 'function') {
      try {
        retryFunction()
      } catch (err) {
        captureError(err, null, 'Retry function')
      }
    }
  }

  // Set up error capture
  onErrorCaptured(captureError)

  return {
    error,
    hasError,
    errorInfo,
    resetError,
    retry,
    captureError
  }
}

// Global error handler for uncaught errors
export function setupGlobalErrorHandler() {
  const uiStore = useUIStore()

  window.addEventListener('error', (event) => {
    console.error('Global error:', event.error)
    
    uiStore.addNotification({
      type: 'error',
      title: 'System Error',
      message: 'An unexpected error occurred.',
      duration: 5000
    })
  })

  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason)
    
    uiStore.addNotification({
      type: 'error',
      title: 'Network Error',
      message: 'A network request failed. Please check your connection.',
      duration: 5000
    })
  })
}