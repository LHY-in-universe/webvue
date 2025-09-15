import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/authService.js'
import { useNotifications } from '@/composables/useNotifications.js'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(null)
  const isAuthenticated = ref(false)
  const userType = ref(null) // 'client', 'server', 'node', etc.
  const currentModule = ref(null) // 'p2pai', 'edgeai', 'blockchain', 'crypto'
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const getUserInfo = computed(() => user.value)
  const getIsAuthenticated = computed(() => isAuthenticated.value)
  const getUserType = computed(() => userType.value)
  const getCurrentModule = computed(() => currentModule.value)

  // Actions
  const login = async (credentials, moduleType) => {
    const { notifications } = useNotifications()
    
    try {
      loading.value = true
      error.value = null
      
      // 调用真实API
      const response = await authService.login({
        username: credentials.username,
        email: credentials.email,
        password: credentials.password,
        module: moduleType
      })
      
      // 处理响应数据
      if (response.success) {
        user.value = response.user
        token.value = response.token
        isAuthenticated.value = true
        currentModule.value = moduleType
        
        // Persist to localStorage
        localStorage.setItem('auth-token', response.token)
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('currentModule', moduleType)
        localStorage.setItem('user', JSON.stringify(response.user))
        
        notifications.success('登录成功')
        return { success: true, data: response }
      } else {
        error.value = response.error || '登录失败'
        notifications.error(error.value)
        return { success: false, error: error.value }
      }
    } catch (apiError) {
      error.value = apiError.error || '登录失败，请检查网络连接'
      notifications.error(error.value)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
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

  const logout = async () => {
    const { notifications } = useNotifications()
    
    try {
      loading.value = true
      
      // 调用API登出
      await authService.logout()
      
      // 清理本地状态
      user.value = null
      token.value = null
      isAuthenticated.value = false
      userType.value = null
      currentModule.value = null
      error.value = null
      
      // Clear localStorage
      localStorage.removeItem('auth-token')
      localStorage.removeItem('isAuthenticated')
      localStorage.removeItem('currentModule')
      localStorage.removeItem('user')
      localStorage.removeItem('userType')
      
      notifications.success('已安全退出')
    } catch (apiError) {
      // 即使API调用失败也要清理本地状态
      user.value = null
      token.value = null
      isAuthenticated.value = false
      userType.value = null
      currentModule.value = null
      
      localStorage.removeItem('auth-token')
      localStorage.removeItem('isAuthenticated')
      localStorage.removeItem('currentModule')
      localStorage.removeItem('user')
      localStorage.removeItem('userType')
      
      console.warn('Logout API call failed, but cleared local auth state:', apiError)
    } finally {
      loading.value = false
    }
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
    const savedToken = localStorage.getItem('auth-token')

    if (savedAuth === 'true' && savedUser && savedToken) {
      isAuthenticated.value = true
      currentModule.value = savedModule
      user.value = JSON.parse(savedUser)
      userType.value = savedUserType
      token.value = savedToken
    }
  }

  // 检查认证状态（验证token有效性）
  const checkAuthStatus = async () => {
    if (!token.value) return false
    
    try {
      const response = await authService.checkAuthStatus()
      return response.authenticated
    } catch (error) {
      console.warn('Auth status check failed:', error)
      // Token无效，清理认证状态
      await logout()
      return false
    }
  }

  // 更新用户偏好设置
  const updatePreferences = async (preferences) => {
    if (!user.value) return { success: false, error: '用户未登录' }
    
    try {
      loading.value = true
      const response = await authService.updateUserPreferences(user.value.id, preferences)
      
      if (response.success) {
        // 更新本地用户数据
        user.value.preferences = { ...user.value.preferences, ...preferences }
        localStorage.setItem('user', JSON.stringify(user.value))
        return { success: true, data: response }
      } else {
        return { success: false, error: response.error }
      }
    } catch (apiError) {
      return { success: false, error: apiError.error || '更新偏好设置失败' }
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    user,
    token,
    isAuthenticated, 
    userType,
    currentModule,
    loading,
    error,
    
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
    updatePreferences,
    initializeAuth,
    checkAuthStatus
  }
})