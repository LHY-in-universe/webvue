import { ref, reactive } from 'vue'

// Global notification state
const notifications = ref([])
const confirmations = ref([])

// Notification manager instance
let notificationManager = null

// Register notification manager
export const registerNotificationManager = (manager) => {
  notificationManager = manager
}

// Core notification functions
export const useNotifications = () => {
  
  // Show notification using the manager
  const show = (options) => {
    if (notificationManager) {
      return notificationManager.show(options)
    } else {
      // Fallback: add to internal array for components to consume
      const notification = {
        id: Date.now() + Math.random(),
        timestamp: Date.now(),
        ...options
      }
      notifications.value.unshift(notification)
      return notification.id
    }
  }

  // Convenience methods
  const success = (message, options = {}) => {
    return show({ 
      type: 'success', 
      message, 
      ...options 
    })
  }

  const error = (message, options = {}) => {
    return show({ 
      type: 'error', 
      message, 
      duration: options.duration || 8000, // Errors last longer
      ...options 
    })
  }

  const warning = (message, options = {}) => {
    return show({ 
      type: 'warning', 
      message, 
      ...options 
    })
  }

  const info = (message, options = {}) => {
    return show({ 
      type: 'info', 
      message, 
      ...options 
    })
  }

  // Loading notifications
  const loading = (message = 'Loading...', options = {}) => {
    return show({
      type: 'info',
      message,
      duration: 0, // No auto-dismiss
      dismissible: false,
      showProgress: false,
      ...options
    })
  }

  const updateLoading = (id, message) => {
    if (notificationManager && notificationManager.update) {
      return notificationManager.update(id, { message })
    }
    // Fallback update logic
    const notification = notifications.value.find(n => n.id === id)
    if (notification) {
      notification.message = message
    }
  }

  const stopLoading = (id, finalMessage, finalType = 'success') => {
    if (notificationManager && notificationManager.dismiss) {
      notificationManager.dismiss(id)
      if (finalMessage) {
        return show({
          type: finalType,
          message: finalMessage,
          duration: 3000
        })
      }
    }
  }

  // Dismiss notifications
  const dismiss = (id) => {
    if (notificationManager && notificationManager.dismiss) {
      return notificationManager.dismiss(id)
    }
    // Fallback dismiss
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const dismissAll = () => {
    if (notificationManager && notificationManager.dismissAll) {
      return notificationManager.dismissAll()
    }
    notifications.value.splice(0)
  }

  // Confirmation dialogs
  const confirm = (options) => {
    return new Promise((resolve) => {
      const confirmation = {
        id: Date.now() + Math.random(),
        isOpen: true,
        onConfirm: (result) => {
          confirmation.isOpen = false
          resolve({ confirmed: true, ...result })
        },
        onCancel: () => {
          confirmation.isOpen = false
          resolve({ confirmed: false })
        },
        ...options
      }
      
      confirmations.value.push(confirmation)
    })
  }

  // Confirmation variants
  const confirmDelete = (itemName, options = {}) => {
    return confirm({
      type: 'delete',
      title: 'Delete Confirmation',
      message: `Are you sure you want to delete "${itemName}"? This action cannot be undone.`,
      confirmText: 'Delete',
      requiresInput: options.requiresTyping,
      inputRequired: options.requiresTyping ? itemName : undefined,
      inputLabel: options.requiresTyping ? `Type "${itemName}" to confirm deletion:` : undefined,
      ...options
    })
  }

  const confirmDanger = (message, options = {}) => {
    return confirm({
      type: 'danger',
      title: 'Dangerous Action',
      message,
      confirmText: 'Yes, Continue',
      requiresCheckbox: true,
      checkboxLabel: 'I understand this action cannot be undone',
      ...options
    })
  }

  const confirmWarning = (message, options = {}) => {
    return confirm({
      type: 'warning',
      message,
      confirmText: 'Continue',
      ...options
    })
  }

  // Async action helpers
  const withLoading = async (asyncFn, loadingMessage = 'Processing...') => {
    const loadingId = loading(loadingMessage)
    
    try {
      const result = await asyncFn()
      stopLoading(loadingId)
      return result
    } catch (error) {
      stopLoading(loadingId)
      error(`Failed: ${error.message}`)
      throw error
    }
  }

  const withConfirmation = async (asyncFn, confirmOptions) => {
    const result = await confirm(confirmOptions)
    
    if (result.confirmed) {
      return await asyncFn(result)
    }
    
    return { cancelled: true }
  }

  // Progress notifications
  const progress = (message, initialProgress = 0) => {
    const progressNotification = {
      id: Date.now() + Math.random(),
      type: 'info',
      message,
      progress: initialProgress,
      duration: 0,
      dismissible: false,
      showProgress: true,
      isProgress: true
    }

    const id = show(progressNotification)

    const updateProgress = (newProgress, newMessage) => {
      progressNotification.progress = newProgress
      if (newMessage) progressNotification.message = newMessage
      
      if (newProgress >= 100) {
        setTimeout(() => dismiss(id), 1000)
      }
    }

    return { id, updateProgress }
  }

  // Batch operations
  const batch = (operations) => {
    const batchId = Date.now()
    const batchNotifications = []

    operations.forEach((operation, index) => {
      const id = show({
        ...operation,
        batchId,
        batchIndex: index
      })
      batchNotifications.push(id)
    })

    const dismissBatch = () => {
      batchNotifications.forEach(id => dismiss(id))
    }

    return { batchNotifications, dismissBatch }
  }

  return {
    // State
    notifications: notifications.value,
    confirmations: confirmations.value,
    
    // Basic methods
    show,
    success,
    error,
    warning,
    info,
    dismiss,
    dismissAll,
    
    // Loading methods
    loading,
    updateLoading,
    stopLoading,
    
    // Confirmation methods
    confirm,
    confirmDelete,
    confirmDanger,
    confirmWarning,
    
    // Utility methods
    withLoading,
    withConfirmation,
    progress,
    batch
  }
}

// Global instance for easy access
export const $notify = useNotifications()

// Plugin installation
export default {
  install(app) {
    app.config.globalProperties.$notify = $notify
    app.provide('notifications', $notify)
  }
}