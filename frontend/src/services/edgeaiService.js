/**
 * Edge AI Service
 * 处理Edge AI模块相关的API调用
 */

import apiClient, { uploadWithProgress, downloadFile } from './apiClient.js'
import { API_ENDPOINTS, WS_ENDPOINTS } from '@/config/api.js'

/**
 * API响应验证工具
 */
const validateApiResponse = (response, expectedFields = []) => {
  if (!response || typeof response !== 'object') {
    throw new Error('Invalid API response format')
  }

  // 检查必需字段
  for (const field of expectedFields) {
    if (!(field in response)) {
      console.warn(`Missing expected field: ${field} in API response`)
    }
  }

  return response
}

const validateProjectResponse = (project) => {
  return validateApiResponse(project, ['id', 'name', 'type', 'status'])
}

const validateNodeResponse = (node) => {
  // Map backend 'state' field to frontend 'status' field for consistency
  if (node.state && !node.status) {
    node.status = node.state
  }
  return validateApiResponse(node, ['id', 'name', 'type', 'status'])
}

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
    const data = response.data

    // 验证响应格式
    if (Array.isArray(data)) {
      return data.map(validateProjectResponse)
    } else if (data && Array.isArray(data.data)) {
      return data.data.map(validateProjectResponse)
    }

    return data
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
  },

  /**
   * 获取项目模板
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 模板列表
   */
  async getTemplates(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.PROJECTS.TEMPLATES, { params })
    return response.data
  },

  /**
   * 获取导入历史
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 导入历史
   */
  async getImportHistory(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.PROJECTS.IMPORT_HISTORY, { params })
    return response.data
  },

  /**
   * 从URL加载配置
   * @param {string} url - 配置URL
   * @returns {Promise<Object>} 配置数据
   */
  async loadFromUrl(url) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.PROJECTS.LOAD_FROM_URL, { url })
    return response.data
  },

  /**
   * 获取单个项目详情
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 项目详情
   */
  async getProject(projectId) {
    const url = API_ENDPOINTS.EDGE_AI.PROJECTS.DETAIL.replace('{id}', projectId)
    const response = await apiClient.get(url)
    return response.data
  },

  /**
   * 删除项目
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteProject(projectId) {
    const url = API_ENDPOINTS.EDGE_AI.PROJECTS.DETAIL.replace('{id}', projectId)
    const response = await apiClient.delete(url)
    return response.data
  },

  /**
   * 获取项目可视化数据
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 项目可视化数据
   */
  async getProjectVisualization(projectId) {
    const url = API_ENDPOINTS.EDGE_AI.PROJECTS.VISUALIZATION.replace('{id}', projectId)
    const response = await apiClient.get(url)
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
    const data = response.data

    // 验证响应格式并映射状态字段
    let nodes = []
    if (Array.isArray(data)) {
      nodes = data
    } else if (data && Array.isArray(data.data)) {
      nodes = data.data
    } else {
      return data
    }

    // 映射state字段到status，确保前后端字段一致
    return nodes.map(node => {
      const validatedNode = validateNodeResponse(node)
      // 确保state映射到status
      if (validatedNode.state && !validatedNode.status) {
        validatedNode.status = validatedNode.state
      }
      return validatedNode
    })
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
   * 添加新节点
   * @param {Object} nodeData - 节点数据
   * @param {number} projectId - 项目ID
   * @returns {Promise<Object>} 添加结果
   */
  async addNode(nodeData, projectId = null) {
    const params = projectId ? { project_id: projectId } : {}
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.NODES.LIST, nodeData, { params })
    return response.data
  },

  /**
   * 重启节点
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 重启结果
   */
  async restartNode(nodeId) {
    const url = API_ENDPOINTS.EDGE_AI.NODES.OPERATION.replace('{id}', nodeId)
    const response = await apiClient.post(url, { operation: 'restart' })
    return response.data
  },

  /**
   * 连接到节点
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 连接结果
   */
  async connectToNode(nodeId) {
    const url = API_ENDPOINTS.EDGE_AI.NODES.OPERATION.replace('{id}', nodeId)
    const response = await apiClient.post(url, { operation: 'start' })
    return response.data
  },

  /**
   * 断开节点连接
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 断开结果
   */
  async disconnectFromNode(nodeId) {
    const url = API_ENDPOINTS.EDGE_AI.NODES.OPERATION.replace('{id}', nodeId)
    const response = await apiClient.post(url, { operation: 'stop' })
    return response.data
  },

  /**
   * 在指定集群中创建节点（使用现有API）
   * @param {number} clusterId - 集群ID
   * @param {Object} nodeData - 节点数据
   * @returns {Promise<Object>} 创建结果
   */
  async createNodeInCluster(clusterId, nodeData) {
    // 1. 先创建节点
    const createResponse = await apiClient.post(API_ENDPOINTS.EDGE_AI.NODES.LIST, nodeData)
    const node = createResponse.data

    // 2. 将节点分配到集群 - 使用请求体传递cluster_id
    const assignUrl = `${API_ENDPOINTS.EDGE_AI.NODES.LIST.replace(/\/$/, '')}/${node.id}/assign-cluster`
    await apiClient.post(assignUrl, null, {
      params: { cluster_id: clusterId }
    })

    return node
  },

  /**
   * 获取集群下的所有节点（使用现有API）
   * @param {number} clusterId - 集群ID
   * @returns {Promise<Array>} 节点列表
   */
  async getClusterNodes(clusterId) {
    // 获取所有节点，然后过滤出属于指定集群的节点
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.NODES.LIST)
    let allNodes = response.data

    // 确保是数组
    if (!Array.isArray(allNodes)) {
      allNodes = allNodes.data || []
    }

    // 过滤出属于指定集群的节点，并映射状态字段
    // 使用宽松相等（==）以处理字符串和数字类型的cluster_id
    return allNodes
      .filter(node => node.cluster_id == clusterId)
      .map(node => {
        // 映射state字段到status
        if (node.state && !node.status) {
          node.status = node.state
        }
        return node
      })
  },

  /**
   * 导出节点数据
   * @param {Object} exportParams - 导出参数
   * @returns {Promise<Object>} 导出结果
   */
  async exportNodes(exportParams = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.NODES.LIST, { 
      params: { ...exportParams, export: true },
      responseType: 'blob'
    })
    
    // 创建下载
    const blob = new Blob([response.data], { type: 'text/csv' })
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    link.download = 'nodes_export.csv'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)
    
    return { success: true, message: 'Nodes exported successfully' }
  },

  /**
   * 获取节点统计
   * @returns {Promise<Object>} 节点统计
   */
  async getNodeStats() {
    const response = await apiClient.get('/api/edgeai/nodes/stats/overview')
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
  },

  /**
   * 删除节点
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteNode(nodeId) {
    const url = API_ENDPOINTS.EDGE_AI.NODES.DETAIL.replace('{id}', nodeId)
    const response = await apiClient.delete(url)
    return response.data
  },

  /**
   * 批量删除节点
   * @param {Array} nodeIds - 节点ID数组
   * @returns {Promise<Object>} 批量删除结果
   */
  async batchDeleteNodes(nodeIds) {
    const response = await apiClient.delete(API_ENDPOINTS.EDGE_AI.NODES.BATCH_DELETE, {
      data: nodeIds
    })
    return response.data
  },

  /**
   * 获取可视化节点数据
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 可视化节点数据
   */
  async getVisualizationNodes(projectId) {
    const url = API_ENDPOINTS.EDGE_AI.NODES.VISUALIZATION.replace('{projectId}', projectId)
    const response = await apiClient.get(url)
    return response.data
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
  },

  /**
   * 获取训练配置
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 训练配置
   */
  async getTrainingConfig(projectId) {
    const url = API_ENDPOINTS.EDGE_AI.TRAINING.CONFIG.replace('{projectId}', projectId)
    const response = await apiClient.get(url)
    return response.data
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

/**
 * 集群管理服务
 */
export const clusterService = {
  /**
   * 获取集群列表
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 集群列表
   */
  async getClusters(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.CLUSTERS.LIST, { params })
    return response.data
  },

  /**
   * 获取集群详情
   * @param {string} clusterId - 集群ID
   * @returns {Promise<Object>} 集群详情
   */
  async getCluster(clusterId) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.DETAIL.replace('{id}', clusterId)
    const response = await apiClient.get(url)
    return response.data
  },

  /**
   * 创建集群
   * @param {Object} clusterData - 集群数据
   * @returns {Promise<Object>} 创建结果
   */
  async createCluster(clusterData) {
    const response = await apiClient.post(API_ENDPOINTS.EDGE_AI.CLUSTERS.CREATE, clusterData)
    return response.data
  },

  /**
   * 更新集群
   * @param {string} clusterId - 集群ID
   * @param {Object} clusterData - 集群数据
   * @returns {Promise<Object>} 更新结果
   */
  async updateCluster(clusterId, clusterData) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.DETAIL.replace('{id}', clusterId)
    const response = await apiClient.put(url, clusterData)
    return response.data
  },

  /**
   * 删除集群
   * @param {string} clusterId - 集群ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteCluster(clusterId) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.DELETE.replace('{id}', clusterId)
    const response = await apiClient.delete(url)
    return response.data
  },

  /**
   * 启动集群
   * @param {string} clusterId - 集群ID
   * @param {Object} startConfig - 启动配置
   * @returns {Promise<Object>} 启动结果
   */
  async startCluster(clusterId, startConfig = {}) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.START.replace('{id}', clusterId)
    const response = await apiClient.post(url, startConfig)
    return response.data
  },

  /**
   * 停止集群
   * @param {string} clusterId - 集群ID
   * @returns {Promise<Object>} 停止结果
   */
  async stopCluster(clusterId) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.STOP.replace('{id}', clusterId)
    const response = await apiClient.post(url)
    return response.data
  },

  /**
   * 重启集群
   * @param {string} clusterId - 集群ID
   * @returns {Promise<Object>} 重启结果
   */
  async restartCluster(clusterId) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.RESTART.replace('{id}', clusterId)
    const response = await apiClient.post(url)
    return response.data
  },

  /**
   * 获取集群统计
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 集群统计
   */
  async getClusterStats(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.CLUSTERS.STATS, { params })
    return response.data
  },

  /**
   * 获取集群性能指标
   * @param {string} clusterId - 集群ID
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 集群性能指标
   */
  async getClusterPerformance(clusterId, params = {}) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.PERFORMANCE.replace('{id}', clusterId)
    const response = await apiClient.get(url, { params })
    return response.data
  },

  /**
   * 添加节点到集群
   * @param {string} clusterId - 集群ID
   * @param {Object} nodeData - 节点数据
   * @returns {Promise<Object>} 添加结果
   */
  async addNodeToCluster(clusterId, nodeData) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.ADD_NODE.replace('{id}', clusterId)
    const response = await apiClient.post(url, nodeData)
    return response.data
  },

  /**
   * 从集群移除节点
   * @param {string} clusterId - 集群ID
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 移除结果
   */
  async removeNodeFromCluster(clusterId, nodeId) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.REMOVE_NODE.replace('{id}', clusterId).replace('{nodeId}', nodeId)
    const response = await apiClient.delete(url)
    return response.data
  },

  /**
   * 获取集群节点列表
   * @param {string} clusterId - 集群ID
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 集群节点列表
   */
  async getClusterNodes(clusterId, params = {}) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.NODES.replace('{id}', clusterId)
    const response = await apiClient.get(url, { params })
    return response.data
  },

  /**
   * 导出集群配置
   * @param {string} clusterId - 集群ID
   * @param {Object} exportConfig - 导出配置
   * @returns {Promise<Object>} 导出结果
   */
  async exportClusterConfig(clusterId, exportConfig = {}) {
    const url = API_ENDPOINTS.EDGE_AI.CLUSTERS.EXPORT.replace('{id}', clusterId)
    const response = await apiClient.post(url, exportConfig)
    return response.data
  },

  /**
   * 创建集群WebSocket连接
   * @param {string} clusterId - 集群ID
   * @param {Object} callbacks - 回调函数
   * @returns {WebSocket} WebSocket实例
   */
  createClusterWebSocket(clusterId, callbacks = {}) {
    const wsUrl = WS_ENDPOINTS.EDGE_CLUSTER(clusterId)
    const ws = new WebSocket(wsUrl)

    ws.onopen = (event) => {
      console.log('Cluster WebSocket connected:', wsUrl)
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
      console.error('Cluster WebSocket error:', event)
      callbacks.onError?.(event)
    }

    ws.onclose = (event) => {
      console.log('Cluster WebSocket closed:', event)
      callbacks.onClose?.(event)
    }

    return ws
  }
}

/**
 * 模型管理服务
 */
export const modelService = {
  /**
   * 获取模型列表
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 模型列表
   */
  async getModels(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.MODELS.LIST, { params })
    return response.data
  },

  /**
   * 获取模型详情
   * @param {string} modelId - 模型ID
   * @returns {Promise<Object>} 模型详情
   */
  async getModel(modelId) {
    const url = API_ENDPOINTS.EDGE_AI.MODELS.DETAIL.replace('{id}', modelId)
    const response = await apiClient.get(url)
    return response.data
  },

  /**
   * 部署模型
   * @param {string} modelId - 模型ID
   * @param {Object} deployConfig - 部署配置
   * @returns {Promise<Object>} 部署结果
   */
  async deployModel(modelId, deployConfig) {
    const url = API_ENDPOINTS.EDGE_AI.MODELS.DEPLOY.replace('{id}', modelId)
    const response = await apiClient.post(url, deployConfig)
    return response.data
  },

  /**
   * 删除模型
   * @param {string} modelId - 模型ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteModel(modelId) {
    const url = API_ENDPOINTS.EDGE_AI.MODELS.DELETE.replace('{id}', modelId)
    const response = await apiClient.delete(url)
    return response.data
  },

  /**
   * 下载模型
   * @param {string} modelId - 模型ID
   * @param {string} filename - 文件名
   * @returns {Promise} 下载响应
   */
  async downloadModel(modelId, filename) {
    const url = API_ENDPOINTS.EDGE_AI.MODELS.DOWNLOAD.replace('{id}', modelId)
    return await downloadFile(url, filename || `model_${modelId}.zip`)
  },

  /**
   * 导出模型
   * @param {string} modelId - 模型ID
   * @param {Object} exportConfig - 导出配置
   * @returns {Promise<Object>} 导出结果
   */
  async exportModel(modelId, exportConfig) {
    const url = API_ENDPOINTS.EDGE_AI.MODELS.EXPORT.replace('{id}', modelId)
    const response = await apiClient.post(url, exportConfig)
    return response.data
  },

  /**
   * 获取模型统计
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 模型统计
   */
  async getModelStats(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.EDGE_AI.MODELS.STATS, { params })
    return response.data
  },

  /**
   * 获取模型性能指标
   * @param {string} modelId - 模型ID
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 模型性能指标
   */
  async getModelPerformance(modelId, params = {}) {
    const url = API_ENDPOINTS.EDGE_AI.MODELS.PERFORMANCE.replace('{id}', modelId)
    const response = await apiClient.get(url, { params })
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
  tasks: taskService,
  models: modelService,
  clusters: clusterService
}