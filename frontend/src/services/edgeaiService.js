/**
 * Edge AI Service
 * 处理Edge AI模块相关的API调用
 */

import apiClient, { uploadWithProgress, downloadFile } from './apiClient.js'
import { API_ENDPOINTS, WS_ENDPOINTS } from '@/config/api.js'

/**
 * 项目管理服务
 */
export const projectService = {
  /**
   * 获取项目列表
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 项目列表
   */
  async getProjects(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.PROJECTS.LIST, { params })
    return response.data
  },

  /**
   * 创建项目
   * @param {Object} projectData - 项目数据
   * @returns {Promise<Object>} 创建结果
   */
  async createProject(projectData) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.PROJECTS.CREATE, projectData)
    return response.data
  },

  /**
   * 导入项目
   * @param {FormData} formData - 项目文件数据
   * @param {Function} onProgress - 上传进度回调
   * @returns {Promise<Object>} 导入结果
   */
  async importProject(formData, onProgress) {
    return await uploadWithProgress(API_ENDPOINTS.EDGE_AI.PROJECTS.IMPORT, formData, onProgress)
  },

  /**
   * 导出项目
   * @param {string} projectId - 项目ID
   * @param {Object} exportConfig - 导出配置
   * @returns {Promise<Object>} 导出结果
   */
  async exportProject(projectId, exportConfig) {
    const url = API_ENDPOINTS.EDGE_AI.PROJECTS.EXPORT.replace('{id}', projectId)
    const response = await apiClient.post(url, exportConfig)
    return response.data
  },

  /**
   * 启动项目
   * @param {string} projectId - 项目ID
   * @param {Object} startConfig - 启动配置
   * @returns {Promise<Object>} 启动结果
   */
  async startProject(projectId, startConfig) {
    const url = API_ENDPOINTS.EDGE_AI.PROJECTS.START.replace('{id}', projectId)
    const response = await apiClient.post(url, startConfig)
    return response.data
  },

  /**
   * 暂停项目
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 暂停结果
   */
  async pauseProject(projectId) {
    const url = API_ENDPOINTS.EDGE_AI.PROJECTS.PAUSE.replace('{id}', projectId)
    const response = await apiClient.post(url)
    return response.data
  },

  /**
   * 停止项目
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 停止结果
   */
  async stopProject(projectId) {
    const url = API_ENDPOINTS.EDGE_AI.PROJECTS.STOP.replace('{id}', projectId)
    const response = await apiClient.post(url)
    return response.data
  }
}

/**
 * 节点管理服务
 */
export const nodeService = {
  /**
   * 获取节点列表
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 节点列表
   */
  async getNodes(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.NODES.LIST, { params })
    return response.data
  },

  /**
   * 执行节点操作
   * @param {string} nodeId - 节点ID
   * @param {Object} operation - 操作配置
   * @returns {Promise<Object>} 操作结果
   */
  async executeNodeOperation(nodeId, operation) {
    const url = API_ENDPOINTS.EDGE_AI.NODES.OPERATION.replace('{id}', nodeId)
    const response = await apiClient.post(url, operation)
    return response.data
  },

  /**
   * 启动节点训练
   * @param {string} nodeId - 节点ID
   * @param {Object} trainingConfig - 训练配置
   * @returns {Promise<Object>} 启动结果
   */
  async startNodeTraining(nodeId, trainingConfig) {
    const url = API_ENDPOINTS.EDGE_AI.NODES.START_TRAINING.replace('{id}', nodeId)
    const response = await apiClient.post(url, trainingConfig)
    return response.data
  },

  /**
   * 停止节点训练
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 停止结果
   */
  async stopNodeTraining(nodeId) {
    const url = API_ENDPOINTS.EDGE_AI.NODES.STOP_TRAINING.replace('{id}', nodeId)
    const response = await apiClient.post(url)
    return response.data
  },

  /**
   * 创建节点WebSocket连接
   * @param {string} nodeId - 节点ID
   * @param {Object} callbacks - 回调函数
   * @returns {WebSocket} WebSocket实例
   */
  createNodeWebSocket(nodeId, callbacks = {}) {
    const wsUrl = WS_ENDPOINTS.EDGE_NODE(nodeId)
    const ws = new WebSocket(wsUrl)

    ws.onopen = (event) => {
      console.log('Node WebSocket connected:', wsUrl)
      callbacks.onOpen?.(event)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        callbacks.onMessage?.(data)
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
        callbacks.onError?.(error)
      }
    }

    ws.onerror = (event) => {
      console.error('Node WebSocket error:', event)
      callbacks.onError?.(event)
    }

    ws.onclose = (event) => {
      console.log('Node WebSocket closed:', event)
      callbacks.onClose?.(event)
    }

    return ws
  }
}

/**
 * 训练管理服务
 */
export const trainingService = {
  /**
   * 开始训练
   * @param {Object} trainingConfig - 训练配置
   * @returns {Promise<Object>} 训练响应
   */
  async startTraining(trainingConfig) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.TRAINING.START, trainingConfig)
    return response.data
  },

  /**
   * 停止训练
   * @param {string} sessionId - 训练会话ID
   * @returns {Promise<Object>} 停止响应
   */
  async stopTraining(sessionId) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.TRAINING.STOP, { session_id: sessionId })
    return response.data
  },

  /**
   * 批量开始训练
   * @param {Array} trainingConfigs - 训练配置数组
   * @returns {Promise<Object>} 批量训练响应
   */
  async batchStartTraining(trainingConfigs) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.TRAINING.BATCH_START, { trainings: trainingConfigs })
    return response.data
  },

  /**
   * 批量停止训练
   * @param {Array} sessionIds - 训练会话ID数组
   * @returns {Promise<Object>} 批量停止响应
   */
  async batchStopTraining(sessionIds) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.TRAINING.BATCH_STOP, { session_ids: sessionIds })
    return response.data
  },

  /**
   * 创建训练WebSocket连接
   * @param {string} projectId - 项目ID
   * @param {Object} callbacks - 回调函数
   * @returns {WebSocket} WebSocket实例
   */
  createTrainingWebSocket(projectId, callbacks = {}) {
    const wsUrl = WS_ENDPOINTS.EDGE_TRAINING(projectId)
    const ws = new WebSocket(wsUrl)

    ws.onopen = (event) => {
      console.log('EdgeAI Training WebSocket connected:', wsUrl)
      callbacks.onOpen?.(event)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        callbacks.onMessage?.(data)
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
        callbacks.onError?.(error)
      }
    }

    ws.onerror = (event) => {
      console.error('EdgeAI Training WebSocket error:', event)
      callbacks.onError?.(event)
    }

    ws.onclose = (event) => {
      console.log('EdgeAI Training WebSocket closed:', event)
      callbacks.onClose?.(event)
    }

    return ws
  }
}

/**
 * 性能监控服务
 */
export const performanceService = {
  /**
   * 获取性能指标
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 性能指标
   */
  async getMetrics(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.PERFORMANCE.METRICS, { params })
    return response.data
  },

  /**
   * 获取性能摘要
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 性能摘要
   */
  async getSummary(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.PERFORMANCE.SUMMARY, { params })
    return response.data
  },

  /**
   * 获取性能告警
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 性能告警
   */
  async getAlerts(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.PERFORMANCE.ALERTS, { params })
    return response.data
  },

  /**
   * 获取性能趋势
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 性能趋势
   */
  async getTrends(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.PERFORMANCE.TRENDS, { params })
    return response.data
  },

  /**
   * 获取系统健康状态
   * @returns {Promise<Object>} 系统健康状态
   */
  async getHealth() {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.PERFORMANCE.HEALTH)
    return response.data
  }
}

/**
 * 日志管理服务
 */
export const logService = {
  /**
   * 获取日志列表
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 日志列表
   */
  async getLogs(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.LOGS.LIST, { params })
    return response.data
  },

  /**
   * 搜索日志
   * @param {Object} searchParams - 搜索参数
   * @returns {Promise<Object>} 搜索结果
   */
  async searchLogs(searchParams) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.LOGS.SEARCH, { params: searchParams })
    return response.data
  },

  /**
   * 导出日志
   * @param {Object} exportParams - 导出参数
   * @param {string} filename - 文件名
   * @returns {Promise} 导出响应
   */
  async exportLogs(exportParams, filename) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.LOGS.EXPORT, { 
      params: exportParams,
      responseType: 'blob'
    })
    
    // 创建下载
    const blob = new Blob([response.data])
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = filename || 'logs_export.txt'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)
    
    return response
  },

  /**
   * 清理日志
   * @param {Object} cleanupParams - 清理参数
   * @returns {Promise<Object>} 清理结果
   */
  async cleanupLogs(cleanupParams) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.LOGS.CLEANUP, cleanupParams)
    return response.data
  },

  /**
   * 获取实时日志
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 实时日志
   */
  async getRealtimeLogs(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.LOGS.REALTIME, { params })
    return response.data
  }
}

/**
 * 任务管理服务
 */
export const taskService = {
  /**
   * 获取任务列表
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 任务列表
   */
  async getTasks(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.TASKS.LIST, { params })
    return response.data
  },

  /**
   * 创建任务
   * @param {Object} taskData - 任务数据
   * @returns {Promise<Object>} 创建结果
   */
  async createTask(taskData) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.TASKS.CREATE, taskData)
    return response.data
  },

  /**
   * 启动任务
   * @param {string} taskId - 任务ID
   * @param {Object} startConfig - 启动配置
   * @returns {Promise<Object>} 启动结果
   */
  async startTask(taskId, startConfig = {}) {
    const url = API_ENDPOINTS.EDGE_AI.TASKS.START.replace('{id}', taskId)
    const response = await apiClient.put(url, startConfig)
    return response.data
  },

  /**
   * 停止任务
   * @param {string} taskId - 任务ID
   * @returns {Promise<Object>} 停止结果
   */
  async stopTask(taskId) {
    const url = API_ENDPOINTS.EDGE_AI.TASKS.STOP.replace('{id}', taskId)
    const response = await apiClient.put(url)
    return response.data
  },

  /**
   * 批量创建任务
   * @param {Array} tasksData - 任务数据数组
   * @returns {Promise<Object>} 批量创建结果
   */
  async batchCreateTasks(tasksData) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.TASKS.BATCH_CREATE, { tasks: tasksData })
    return response.data
  },

  /**
   * 获取任务队列
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 任务队列
   */
  async getTaskQueue(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.TASKS.QUEUE, { params })
    return response.data
  }
}

// 导出所有服务
export default {
  projects: projectService,
  nodes: nodeService,
  training: trainingService,
  performance: performanceService,
  logs: logService,
  tasks: taskService
}