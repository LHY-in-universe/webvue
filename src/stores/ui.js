import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUIStore = defineStore('ui', () => {
  // UI Component States
  const sidebarOpen = ref(false)
  const mobileNavOpen = ref(false)
  const modalsStack = ref([])
  const notifications = ref([])
  
  // Loading States
  const globalLoading = ref(false)
  const loadingStates = ref({})
  
  // Getters
  const getIsSidebarOpen = computed(() => sidebarOpen.value)
  const getIsMobileNavOpen = computed(() => mobileNavOpen.value)
  const getActiveModals = computed(() => modalsStack.value)
  const getNotifications = computed(() => notifications.value)
  const getIsGlobalLoading = computed(() => globalLoading.value)
  
  // UI Component Actions
  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
  }
  
  const setSidebarOpen = (isOpen) => {
    sidebarOpen.value = isOpen
  }
  
  const toggleMobileNav = () => {
    mobileNavOpen.value = !mobileNavOpen.value
  }
  
  const setMobileNavOpen = (isOpen) => {
    mobileNavOpen.value = isOpen
  }
  
  // Modal Management
  const openModal = (modalId, options = {}) => {
    modalsStack.value.push({
      id: modalId,
      timestamp: Date.now(),
      ...options
    })
  }
  
  const closeModal = (modalId) => {
    modalsStack.value = modalsStack.value.filter(modal => modal.id !== modalId)
  }
  
  const closeAllModals = () => {
    modalsStack.value = []
  }
  
  const getModalById = (modalId) => {
    return modalsStack.value.find(modal => modal.id === modalId)
  }
  
  // Notification Management
  const addNotification = (notification) => {
    const id = `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    
    // 成功和信息类型的通知不显示，直接返回
    if (notification.type === 'success' || notification.type === 'info' || !notification.type) {
      return id
    }
    
    // 根据类型设置不同的持续时间
    let duration = 2500 // 默认持续时间
    if (notification.type === 'error') {
      duration = 2500 // 错误消息2.5秒
    } else if (notification.type === 'warning') {
      duration = 900 // 警告消息0.9秒
    }
    
    const newNotification = {
      id,
      timestamp: Date.now(),
      autoClose: true,
      duration,
      ...notification
    }
    
    notifications.value.push(newNotification)
    
    // Auto close notification
    if (newNotification.autoClose) {
      setTimeout(() => {
        removeNotification(id)
      }, newNotification.duration)
    }
    
    return id
  }
  
  const removeNotification = (id) => {
    notifications.value = notifications.value.filter(n => n.id !== id)
  }
  
  const clearAllNotifications = () => {
    notifications.value = []
  }
  
  // Success notification shortcut
  const notifySuccess = (message, title = '成功') => {
    return addNotification({
      type: 'success',
      title,
      message
    })
  }
  
  // Error notification shortcut
  const notifyError = (message, title = '错误') => {
    return addNotification({
      type: 'error',
      title,
      message,
      autoClose: false
    })
  }
  
  // Warning notification shortcut
  const notifyWarning = (message, title = '警告') => {
    return addNotification({
      type: 'warning',
      title,
      message
    })
  }
  
  // Info notification shortcut
  const notifyInfo = (message, title = '信息') => {
    return addNotification({
      type: 'info',
      title,
      message
    })
  }
  
  // Loading State Management
  const setGlobalLoading = (loading) => {
    globalLoading.value = loading
  }
  
  const setLoading = (key, loading) => {
    if (loading) {
      loadingStates.value[key] = true
    } else {
      delete loadingStates.value[key]
    }
  }
  
  const isLoading = (key) => {
    return !!loadingStates.value[key]
  }
  
  const clearAllLoading = () => {
    globalLoading.value = false
    loadingStates.value = {}
  }
  
  // Initialize UI State
  const initializeUI = () => {
    // Close mobile nav on resize
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setMobileNavOpen(false)
      }
    }
    
    window.addEventListener('resize', handleResize)
  }
  
  return {
    // State
    sidebarOpen,
    mobileNavOpen,
    modalsStack,
    notifications,
    globalLoading,
    loadingStates,
    
    // Getters
    getIsSidebarOpen,
    getIsMobileNavOpen,
    getActiveModals,
    getNotifications,
    getIsGlobalLoading,
    
    // UI Actions
    toggleSidebar,
    setSidebarOpen,
    toggleMobileNav,
    setMobileNavOpen,
    
    // Modal Actions
    openModal,
    closeModal,
    closeAllModals,
    getModalById,
    
    // Notification Actions
    addNotification,
    removeNotification,
    clearAllNotifications,
    notifySuccess,
    notifyError,
    notifyWarning,
    notifyInfo,
    
    // Loading Actions
    setGlobalLoading,
    setLoading,
    isLoading,
    clearAllLoading,
    
    // Initialize
    initializeUI
  }
})