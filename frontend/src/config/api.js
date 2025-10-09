/**
 * API Configuration
 * 统一管理所有API端点和配置
 */

// API基础配置
export const API_CONFIG = {
  // 基础URL - 开发环境
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://175.178.24.56:8000',
  
  // API版本
  VERSION: 'v1',
  
  // 超时设置
  TIMEOUT: 10000,
  
  // 重试次数
  RETRY_ATTEMPTS: 3,
  
  // WebSocket配置
  WS_URL: import.meta.env.VITE_WS_BASE_URL || 'ws://175.178.24.56:8000'
}

// API端点配置
export const API_ENDPOINTS = {
  // 认证相关
  AUTH: {
    LOGIN: '/api/common/auth/login',
    LOGOUT: '/api/common/auth/logout',
    USER: '/api/common/auth/user',
    PREFERENCES: '/api/common/auth/user/{id}/preferences'
  },
  
  // 系统相关
  SYSTEM: {
    HEALTH: '/api/common/system/health',
    INFO: '/api/common/system/system-info',
    LOGS: '/api/common/system/logs',
    NOTIFICATIONS: '/api/common/system/notifications',
    STATS: '/api/common/system/stats'
  },
  
  // P2P AI模块
  P2P_AI: {
    // 项目管理
    PROJECTS: '/api/p2pai/projects',
    PROJECT_DETAIL: '/api/p2pai/projects/{id}',
    PROJECT_STATS: '/api/p2pai/projects/stats/overview',
    
    // 训练管理
    TRAINING: {
      START: '/api/p2pai/training/start',
      STOP: '/api/p2pai/training/stop',
      LOCAL: '/api/p2pai/training/local',
      FEDERATED: '/api/p2pai/training/federated/start',
      MPC: '/api/p2pai/training/mpc/start',
      SESSIONS: '/api/p2pai/training/sessions',
      METRICS: '/api/p2pai/training/metrics/{projectId}',
      WS: '/api/p2pai/training/ws/{projectId}',
      // 新增训练控制相关API
      TRAIN: '/api/p2pai/training/train',
      MONITOR: '/api/p2pai/training/monitor/{taskId}',
      TASKS_LIST: '/api/p2pai/training/tasksList',
      TASK_DELETE: '/api/p2pai/training/tasks/{taskId}',
      RAY_CLUSTER: '/api/p2pai/training/monitorRayCluster/node',
      ROUND_PROGRESS: '/api/p2pai/training/roundProgress/{taskId}'
    },
    
    // 节点管理
    NODES: {
      LIST: '/api/p2pai/nodes',
      DETAIL: '/api/p2pai/nodes/{id}',
      START: '/api/p2pai/nodes/{id}/start',
      STOP: '/api/p2pai/nodes/{id}/stop',
      RESTART: '/api/p2pai/nodes/{id}/restart',
      STATS: '/api/p2pai/nodes/stats/overview'
    },
    
    // 数据集管理
    DATASETS: {
      LIST: '/api/p2pai/datasets',
      UPLOAD: '/api/p2pai/datasets/upload',
      CREATE: '/api/p2pai/datasets',
      DELETE: '/api/p2pai/datasets/{id}',
      DOWNLOAD: '/api/p2pai/datasets/{id}/download',
      STATS: '/api/p2pai/datasets/stats/overview'
    },
    
    // 模型管理
    MODELS: {
      LIST: '/api/p2pai/models',
      EXPORT: '/api/p2pai/models/{id}/export',
      DEPLOY: '/api/p2pai/models/{id}/deploy',
      EVALUATE: '/api/p2pai/models/{id}/evaluate',
      VERSIONS: '/api/p2pai/models/{id}/versions',
      STATS: '/api/p2pai/models/stats/overview'
    }
  },
  
  // Edge AI模块
  EDGE_AI: {
    // 项目管理
    PROJECTS: {
      LIST: '/api/edgeai/projects/',
      CREATE: '/api/edgeai/projects/',
      DETAIL: '/api/edgeai/projects/{id}/',
      IMPORT: '/api/edgeai/projects/import/',
      EXPORT: '/api/edgeai/projects/{id}/export/',
      START: '/api/edgeai/projects/{id}/start/',
      PAUSE: '/api/edgeai/projects/{id}/pause/',
      STOP: '/api/edgeai/projects/{id}/stop/',
      TEMPLATES: '/api/edgeai/projects/templates/',
      IMPORT_HISTORY: '/api/edgeai/projects/import-history/',
      LOAD_FROM_URL: '/api/edgeai/projects/load-from-url/'
    },

    // 节点管理
    NODES: {
      LIST: '/api/edgeai/nodes/',
      OPERATION: '/api/edgeai/nodes/{id}/operation/',
      START_TRAINING: '/api/edgeai/nodes/{id}/start-training/',
      STOP_TRAINING: '/api/edgeai/nodes/{id}/stop-training/',
      VISUALIZATION: '/api/edgeai/nodes/visualization/{projectId}/',
      WS: '/api/edgeai/nodes/ws/{id}'
    },

    // 训练管理
    TRAINING: {
      START: '/api/edgeai/training/start/',
      STOP: '/api/edgeai/training/stop/',
      BATCH_START: '/api/edgeai/training/batch-start/',
      BATCH_STOP: '/api/edgeai/training/batch-stop/',
      CONFIG: '/api/edgeai/training/config/{projectId}/',
      WS: '/api/edgeai/training/ws/{projectId}'
    },

    // 性能监控
    PERFORMANCE: {
      METRICS: '/api/edgeai/performance/metrics/',
      SUMMARY: '/api/edgeai/performance/summary/',
      ALERTS: '/api/edgeai/performance/alerts/',
      TRENDS: '/api/edgeai/performance/trends/',
      HEALTH: '/api/edgeai/performance/health/'
    },

    // 日志管理
    LOGS: {
      LIST: '/api/edgeai/logs/',
      SEARCH: '/api/edgeai/logs/search/',
      EXPORT: '/api/edgeai/logs/export/',
      CLEANUP: '/api/edgeai/logs/cleanup/',
      REALTIME: '/api/edgeai/logs/realtime/'
    },

    // 任务管理
    TASKS: {
      LIST: '/api/edgeai/tasks/',
      CREATE: '/api/edgeai/tasks/',
      START: '/api/edgeai/tasks/{id}/start/',
      STOP: '/api/edgeai/tasks/{id}/stop/',
      BATCH_CREATE: '/api/edgeai/tasks/batch-create/',
      QUEUE: '/api/edgeai/tasks/queue/'
    },

    // 模型管理
    MODELS: {
      LIST: '/api/edgeai/models/',
      DETAIL: '/api/edgeai/models/{id}/',
      DEPLOY: '/api/edgeai/models/{id}/deploy/',
      DELETE: '/api/edgeai/models/{id}/',
      DOWNLOAD: '/api/edgeai/models/{id}/download/',
      EXPORT: '/api/edgeai/models/{id}/export/',
      STATS: '/api/edgeai/models/stats/overview/',
      PERFORMANCE: '/api/edgeai/models/{id}/performance/'
    }
  }
}

// WebSocket端点
export const WS_ENDPOINTS = {
  P2P_TRAINING: (projectId) => `${API_CONFIG.WS_URL}/api/p2pai/training/ws/${projectId}`,
  EDGE_TRAINING: (projectId) => `${API_CONFIG.WS_URL}/api/edgeai/training/ws/${projectId}`,
  EDGE_NODE: (nodeId) => `${API_CONFIG.WS_URL}/api/edgeai/nodes/ws/${nodeId}`
}

// HTTP状态码
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_ERROR: 500
}

// API响应格式
export const API_RESPONSE_FORMAT = {
  SUCCESS: 'success',
  ERROR: 'error',
  DATA: 'data',
  MESSAGE: 'message',
  CODE: 'code'
}

/**
 * 构建完整的API URL
 * @param {string} endpoint - API端点
 * @param {Object} params - URL参数
 * @returns {string} 完整的URL
 */
export function buildApiUrl(endpoint, params = {}) {
  let url = `${API_CONFIG.BASE_URL}${endpoint}`
  
  // 替换路径参数
  Object.entries(params).forEach(([key, value]) => {
    url = url.replace(`{${key}}`, value)
  })
  
  return url
}

/**
 * 构建WebSocket URL
 * @param {string} endpoint - WebSocket端点
 * @returns {string} WebSocket URL
 */
export function buildWsUrl(endpoint) {
  return `${API_CONFIG.WS_URL}${endpoint}`
}