/**
 * 全局错误处理器
 * 处理常见的JavaScript错误
 */

// 处理playbackRate错误
export const handlePlaybackRateError = () => {
  // 监听全局错误
  window.addEventListener('error', (event) => {
    if (event.message && event.message.includes('playbackRate')) {
      console.warn('PlaybackRate error caught and handled:', event.message)
      event.preventDefault()
      return false
    }
  })
}

// 处理notifications错误
export const handleNotificationsError = () => {
  // 确保notifications对象存在
  if (!window.notifications) {
    window.notifications = {
      success: (message) => console.log('Success:', message),
      error: (message) => console.error('Error:', message),
      warning: (message) => console.warn('Warning:', message),
      info: (message) => console.info('Info:', message)
    }
  }
}

// 处理WebSocket错误
export const handleWebSocketError = () => {
  // 监听未处理的Promise rejection
  window.addEventListener('unhandledrejection', (event) => {
    if (event.reason && event.reason.message && 
        event.reason.message.includes('WebSocket')) {
      console.warn('WebSocket error caught and handled:', event.reason.message)
      event.preventDefault()
    }
  })
}

// 初始化所有错误处理器
export const initErrorHandlers = () => {
  handlePlaybackRateError()
  handleNotificationsError()
  handleWebSocketError()
  
  console.log('Error handlers initialized')
}
