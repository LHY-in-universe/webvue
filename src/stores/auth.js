import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const isAuthenticated = ref(false)
  const userType = ref(null) // 'client', 'server', 'node', etc.
  const currentModule = ref(null) // 'p2pai', 'edgeai', 'blockchain', 'crypto'

  // Getters
  const getUserInfo = computed(() => user.value)
  const getIsAuthenticated = computed(() => isAuthenticated.value)
  const getUserType = computed(() => userType.value)
  const getCurrentModule = computed(() => currentModule.value)

  // Actions
  const login = async (credentials, moduleType) => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Mock user data with theme preferences
      user.value = {
        id: Date.now(),
        username: credentials.username,
        email: credentials.email || `${credentials.username}@example.com`,
        module: moduleType,
        preferences: {
          theme: 'auto', // 'light', 'dark', 'auto'
          autoTheme: true,
          language: 'zh',
          notifications: true
        }
      }
      
      isAuthenticated.value = true
      currentModule.value = moduleType
      
      // Persist to localStorage
      localStorage.setItem('isAuthenticated', 'true')
      localStorage.setItem('currentModule', moduleType)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  // Quick login for demo purposes - no delay
  const quickLogin = async (credentials, moduleType) => {
    try {
      // No API call delay for quick login
      user.value = {
        id: Date.now(),
        username: credentials.username,
        email: credentials.email || `${credentials.username}@example.com`,
        module: moduleType,
        preferences: {
          theme: 'auto',
          autoTheme: true,
          language: 'en', // English for demo
          notifications: true
        }
      }
      
      isAuthenticated.value = true
      currentModule.value = moduleType
      
      // Persist to localStorage
      localStorage.setItem('isAuthenticated', 'true')
      localStorage.setItem('currentModule', moduleType)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  const logout = () => {
    user.value = null
    isAuthenticated.value = false
    userType.value = null
    currentModule.value = null
    
    // Clear localStorage
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('currentModule')
    localStorage.removeItem('user')
    localStorage.removeItem('userType')
  }

  const setUserType = (type) => {
    userType.value = type
    localStorage.setItem('userType', type)
  }

  const updateUserThemePreference = (theme, autoTheme = false) => {
    if (user.value && user.value.preferences) {
      user.value.preferences.theme = theme
      user.value.preferences.autoTheme = autoTheme
      
      // Update localStorage
      localStorage.setItem('user', JSON.stringify(user.value))
      
      // Sync with theme store if available
      const themeStore = JSON.parse(localStorage.getItem('theme-store') || '{}')
      themeStore.theme = theme
      themeStore.autoTheme = autoTheme
      localStorage.setItem('theme-store', JSON.stringify(themeStore))
    }
  }

  const updateUserPreference = (key, value) => {
    if (user.value && user.value.preferences) {
      user.value.preferences[key] = value
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }

  const getUserThemePreference = computed(() => {
    return user.value?.preferences?.theme || 'auto'
  })

  const getUserAutoThemePreference = computed(() => {
    return user.value?.preferences?.autoTheme || true
  })

  const initializeAuth = () => {
    // Restore auth state from localStorage
    const savedAuth = localStorage.getItem('isAuthenticated')
    const savedModule = localStorage.getItem('currentModule') 
    const savedUser = localStorage.getItem('user')
    const savedUserType = localStorage.getItem('userType')

    if (savedAuth === 'true' && savedUser) {
      isAuthenticated.value = true
      currentModule.value = savedModule
      user.value = JSON.parse(savedUser)
      userType.value = savedUserType
    }
  }

  return {
    // State
    user,
    isAuthenticated, 
    userType,
    currentModule,
    
    // Getters
    getUserInfo,
    getIsAuthenticated,
    getUserType, 
    getCurrentModule,
    getUserThemePreference,
    getUserAutoThemePreference,
    
    // Actions
    login,
    quickLogin,
    logout,
    setUserType,
    updateUserThemePreference,
    updateUserPreference,
    initializeAuth
  }
})