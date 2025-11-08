/**
 * 统一的日志工具
 * 在开发环境输出日志，生产环境静默（除了error）
 */

const isDev = import.meta.env.DEV
const isDebugMode = import.meta.env.VITE_DEBUG_API === 'true'

/**
 * 日志级别
 */
const LogLevel = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
  NONE: 4
}

/**
 * 当前日志级别配置
 * 生产环境只显示ERROR
 * 开发环境显示所有
 */
const currentLevel = isDev ? LogLevel.DEBUG : LogLevel.ERROR

/**
 * 格式化日志前缀
 */
const formatPrefix = (level, category = '') => {
  const timestamp = new Date().toLocaleTimeString()
  const categoryStr = category ? ` [${category}]` : ''
  return `[${timestamp}]${categoryStr}`
}

/**
 * 统一的logger对象
 */
export const logger = {
  /**
   * 调试日志 - 仅在开发环境且DEBUG模式下显示
   * @param  {...any} args 
   */
  debug: (...args) => {
    if (currentLevel <= LogLevel.DEBUG && isDebugMode) {
      console.log(formatPrefix('DEBUG'), ...args)
    }
  },

  /**
   * 信息日志 - 开发环境显示
   * @param  {...any} args 
   */
  log: (...args) => {
    if (currentLevel <= LogLevel.INFO) {
      console.log(formatPrefix('INFO'), ...args)
    }
  },

  /**
   * 信息日志（别名）
   * @param  {...any} args 
   */
  info: (...args) => {
    if (currentLevel <= LogLevel.INFO) {
      console.info(formatPrefix('INFO'), ...args)
    }
  },

  /**
   * 警告日志 - 开发环境显示
   * @param  {...any} args 
   */
  warn: (...args) => {
    if (currentLevel <= LogLevel.WARN) {
      console.warn(formatPrefix('WARN'), ...args)
    }
  },

  /**
   * 错误日志 - 始终显示
   * @param  {...any} args 
   */
  error: (...args) => {
    if (currentLevel <= LogLevel.ERROR) {
      console.error(formatPrefix('ERROR'), ...args)
    }
  },

  /**
   * 分组日志 - 开发环境显示
   * @param {string} label 
   * @param {Function} fn 
   */
  group: (label, fn) => {
    if (currentLevel <= LogLevel.INFO) {
      console.group(formatPrefix('GROUP'), label)
      fn()
      console.groupEnd()
    }
  },

  /**
   * 性能计时开始
   * @param {string} label 
   */
  time: (label) => {
    if (currentLevel <= LogLevel.DEBUG) {
      console.time(label)
    }
  },

  /**
   * 性能计时结束
   * @param {string} label 
   */
  timeEnd: (label) => {
    if (currentLevel <= LogLevel.DEBUG) {
      console.timeEnd(label)
    }
  },

  /**
   * 表格输出 - 开发环境显示
   * @param {*} data 
   */
  table: (data) => {
    if (currentLevel <= LogLevel.INFO) {
      console.table(data)
    }
  }
}

/**
 * 创建带分类的logger
 * @param {string} category - 分类名称
 * @returns {Object} logger实例
 */
export const createLogger = (category) => {
  return {
    debug: (...args) => {
      if (currentLevel <= LogLevel.DEBUG && isDebugMode) {
        console.log(formatPrefix('DEBUG', category), ...args)
      }
    },
    log: (...args) => {
      if (currentLevel <= LogLevel.INFO) {
        console.log(formatPrefix('INFO', category), ...args)
      }
    },
    info: (...args) => {
      if (currentLevel <= LogLevel.INFO) {
        console.info(formatPrefix('INFO', category), ...args)
      }
    },
    warn: (...args) => {
      if (currentLevel <= LogLevel.WARN) {
        console.warn(formatPrefix('WARN', category), ...args)
      }
    },
    error: (...args) => {
      if (currentLevel <= LogLevel.ERROR) {
        console.error(formatPrefix('ERROR', category), ...args)
      }
    }
  }
}

/**
 * API调用日志
 */
export const apiLogger = {
  ...createLogger('API'),
  
  /**
   * 开始日志组 - 用于API请求
   */
  logStart: (message) => {
    if (currentLevel <= LogLevel.INFO) {
      console.group(`[${new Date().toLocaleTimeString()}] [API] ${message}`)
    }
  },
  
  /**
   * 结束日志组
   */
  logEnd: () => {
    if (currentLevel <= LogLevel.INFO) {
      console.groupEnd()
    }
  }
}

/**
 * Store日志
 */
export const storeLogger = createLogger('Store')

/**
 * WebSocket日志
 */
export const wsLogger = createLogger('WebSocket')

/**
 * 性能日志
 */
export const perfLogger = createLogger('Performance')

// 开发环境下暴露到全局
if (isDev) {
  window.logger = logger
}

export default logger

