/**
 * API Client Configuration
 * 配置Axios实例，包括拦截器、错误处理等
 */

import axios from 'axios'
import { API_CONFIG, HTTP_STATUS, API_RESPONSE_FORMAT } from '@/config/api.js'
import { useAuthStore } from '@/stores/auth.js'
import { useNotifications } from '@/composables/useNotifications.js'
import performanceMonitor from '@/utils/performanceMonitor.js'

/**
 * 创建Axios实例
 */
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  // 优化选项
  maxRedirects: 3,
  maxContentLength: 10 * 1024 * 1024, // 10MB
  maxBodyLength: 10 * 1024 * 1024, // 10MB
})

/**
 * 请求拦截器
 */
apiClient.interceptors.request.use(
  (config) => {
    // 开始性能监控
    const requestId = `${config.method?.toUpperCase()}_${config.url}_${Date.now()}`
    config.requestId = requestId
    performanceMonitor.startApiCall(requestId, config.method, config.url)

    // 添加认证token
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    
    // 开发环境下打印请求信息
    if (import.meta.env.VITE_DEBUG_API) {
      console.group(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`)
      console.log('Config:', config)
      console.groupEnd()
    }
    
    return config
  },
  (error) => {
    console.error('Request interceptor error:', error)
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 */
apiClient.interceptors.response.use(
  (response) => {
    // 结束性能监控
    if (response.config.requestId) {
      performanceMonitor.endApiCall(response.config.requestId, true, response.status)
    }

    // 开发环境下打印响应信息
    if (import.meta.env.VITE_DEBUG_API) {
      console.group(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url}`)
      console.log('Status:', response.status)
      console.log('Data:', response.data)
      console.groupEnd()
    }
    
    // 统一处理响应数据格式
    return handleApiResponse(response)
  },
  (error) => {
    // 结束性能监控（失败）
    if (error.config?.requestId) {
      performanceMonitor.endApiCall(error.config.requestId, false, error.response?.status)
    }

    // 开发环境下打印错误信息
    if (import.meta.env.VITE_DEBUG_API) {
      console.group(`❌ API Error: ${error.config?.method?.toUpperCase()} ${error.config?.url}`)
      console.error('Error:', error)
      console.groupEnd()
    }
    
    // 统一错误处理
    return handleApiError(error)
  }
)

/**
 * 处理API响应
 * @param {Object} response - Axios响应对象
 * @returns {Object} 处理后的响应数据
 */
function handleApiResponse(response) {
  const { data, status } = response
  
  // 如果后端返回标准格式
  if (data && typeof data === 'object' && 'success' in data) {
    if (data.success) {
      return {
        success: true,
        data: data.data || data,
        message: data.message || 'Success',
        status
      }
    } else {
      throw new Error(data.message || 'API returned success: false')
    }
  }
  
  // 直接返回数据（兼容性处理）
  return {
    success: true,
    data: data,
    message: 'Success',
    status
  }
}

/**
 * 处理API错误
 * @param {Object} error - Axios错误对象
 * @returns {Promise} 拒绝的Promise
 */
function handleApiError(error) {
  let errorMessage = 'An unexpected error occurred'
  let errorCode = 'UNKNOWN_ERROR'
  
  if (error.response) {
    // 服务器响应错误
    const { status, data } = error.response
    
    switch (status) {
      case HTTP_STATUS.BAD_REQUEST:
        errorMessage = data?.message || 'Bad request'
        errorCode = 'BAD_REQUEST'
        break
        
      case HTTP_STATUS.UNAUTHORIZED:
        errorMessage = 'Authentication required'
        errorCode = 'UNAUTHORIZED'
        // 清除认证状态
        const authStore = useAuthStore()
        authStore.logout()
        break
        
      case HTTP_STATUS.FORBIDDEN:
        errorMessage = 'Access denied'
        errorCode = 'FORBIDDEN'
        break
        
      case HTTP_STATUS.NOT_FOUND:
        errorMessage = 'Resource not found'
        errorCode = 'NOT_FOUND'
        break
        
      case HTTP_STATUS.INTERNAL_ERROR:
        errorMessage = 'Server error. Please try again later.'
        errorCode = 'INTERNAL_ERROR'
        break
        
      default:
        errorMessage = data?.message || `HTTP ${status} Error`
        errorCode = `HTTP_${status}`
    }
  } else if (error.request) {
    // 网络错误
    errorMessage = 'Network error. Please check your connection.'
    errorCode = 'NETWORK_ERROR'
  } else {
    // 其他错误
    errorMessage = error.message || 'An unexpected error occurred'
    errorCode = 'UNKNOWN_ERROR'
  }
  
  // 使用全局通知实例显示错误提示
  try {
    // 尝试导入全局通知实例
    import('@/composables/useNotifications.js').then(module => {
      const { $notify } = module
      if ($notify && $notify.error) {
        $notify.error(errorMessage)
      }
    }).catch(() => {
      // 如果导入失败，使用console输出
      console.error('API Error:', errorMessage)
    })
  } catch (e) {
    // 降级处理：使用console输出
    console.error('API Error:', errorMessage)
  }
  
  // 返回结构化错误
  const apiError = {
    success: false,
    error: errorMessage,
    code: errorCode,
    status: error.response?.status,
    data: error.response?.data
  }
  
  return Promise.reject(apiError)
}

/**
 * 重试请求
 * @param {Function} apiCall - API调用函数
 * @param {number} attempts - 重试次数
 * @returns {Promise} API响应
 */
export async function retryRequest(apiCall, attempts = API_CONFIG.RETRY_ATTEMPTS) {
  let lastError
  
  for (let i = 0; i < attempts; i++) {
    try {
      return await apiCall()
    } catch (error) {
      lastError = error
      
      // 如果是认证错误或客户端错误，不重试
      if (error.status >= 400 && error.status < 500) {
        break
      }
      
      // 等待一段时间后重试
      if (i < attempts - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)))
      }
    }
  }
  
  throw lastError
}

/**
 * 带有上传进度的POST请求
 * @param {string} url - 请求URL
 * @param {FormData} formData - 表单数据
 * @param {Function} onProgress - 进度回调
 * @returns {Promise} API响应
 */
export function uploadWithProgress(url, formData, onProgress) {
  return apiClient.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress && progressEvent.lengthComputable) {
        const percentage = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(percentage)
      }
    }
  })
}

/**
 * 下载文件
 * @param {string} url - 下载URL
 * @param {string} filename - 文件名
 * @returns {Promise} 下载响应
 */
export async function downloadFile(url, filename) {
  const response = await apiClient.get(url, {
    responseType: 'blob'
  })
  
  // 创建下载链接
  const blob = new Blob([response.data])
  const downloadUrl = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = downloadUrl
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(downloadUrl)
  
  return response
}

export default apiClient