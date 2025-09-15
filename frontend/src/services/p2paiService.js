/**
 * P2P AI Service
 * 处理P2P AI模块相关的API调用
 */

import apiClient, { uploadWithProgress, downloadFile } from './apiClient.js'
import { API_ENDPOINTS, buildApiUrl, WS_ENDPOINTS } from '@/config/api.js'

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
    const response = await apiClient.get(API_ENDPOINTS.P2P_AI.PROJECTS, { params })
    return response.data
  },

  /**
   * 获取项目详情
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 项目详情
   */
  async getProject(projectId) {
    const url = API_ENDPOINTS.P2P_AI.PROJECT_DETAIL.replace('{id}', projectId)
    const response = await apiClient.get(url)
    return response.data
  },

  /**
   * 创建项目
   * @param {Object} projectData - 项目数据
   * @returns {Promise<Object>} 创建结果
   */
  async createProject(projectData) {
    const response = await apiClient.post(API_ENDPOINTS.P2P_AI.PROJECTS, projectData)
    return response.data
  },

  /**
   * 更新项目
   * @param {string} projectId - 项目ID
   * @param {Object} projectData - 项目数据
   * @returns {Promise<Object>} 更新结果
   */
  async updateProject(projectId, projectData) {
    const url = API_ENDPOINTS.P2P_AI.PROJECT_DETAIL.replace('{id}', projectId)
    const response = await apiClient.put(url, projectData)
    return response.data
  },

  /**
   * 删除项目
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteProject(projectId) {
    const url = API_ENDPOINTS.P2P_AI.PROJECT_DETAIL.replace('{id}', projectId)
    const response = await apiClient.delete(url)
    return response.data
  },

  /**
   * 获取项目统计
   * @returns {Promise<Object>} 项目统计数据
   */
  async getProjectStats() {
    const response = await apiClient.get(API_ENDPOINTS.P2P_AI.PROJECT_STATS)
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
    const response = await apiClient.post(API_ENDPOINTS.P2P_AI.TRAINING.START, trainingConfig)
    return response.data
  },

  /**
   * 停止训练
   * @param {string} sessionId - 训练会话ID
   * @returns {Promise<Object>} 停止响应
   */
  async stopTraining(sessionId) {
    const response = await apiClient.post(API_ENDPOINTS.P2P_AI.TRAINING.STOP, { session_id: sessionId })
    return response.data
  },

  /**
   * 开始本地训练
   * @param {Object} localConfig - 本地训练配置
   * @returns {Promise<Object>} 训练响应
   */
  async startLocalTraining(localConfig) {
    const response = await apiClient.post(API_ENDPOINTS.P2P_AI.TRAINING.LOCAL, localConfig)
    return response.data
  },

  /**
   * 开始联邦学习
   * @param {Object} federatedConfig - 联邦学习配置
   * @returns {Promise<Object>} 训练响应
   */
  async startFederatedTraining(federatedConfig) {
    const response = await apiClient.post(API_ENDPOINTS.P2P_AI.TRAINING.FEDERATED, federatedConfig)
    return response.data
  },

  /**
   * 开始MPC训练
   * @param {Object} mpcConfig - MPC训练配置
   * @returns {Promise<Object>} 训练响应
   */
  async startMPCTraining(mpcConfig) {
    const response = await apiClient.post(API_ENDPOINTS.P2P_AI.TRAINING.MPC, mpcConfig)
    return response.data
  },

  /**
   * 获取训练会话
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 训练会话列表
   */
  async getTrainingSessions(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.P2P_AI.TRAINING.SESSIONS, { params })
    return response.data
  },

  /**
   * 获取训练指标
   * @param {string} projectId - 项目ID
   * @returns {Promise<Object>} 训练指标
   */
  async getTrainingMetrics(projectId) {
    const url = API_ENDPOINTS.P2P_AI.TRAINING.METRICS.replace('{projectId}', projectId)
    const response = await apiClient.get(url)
    return response.data
  },

  /**
   * 创建训练WebSocket连接
   * @param {string} projectId - 项目ID
   * @param {Object} callbacks - 回调函数
   * @returns {WebSocket} WebSocket实例
   */
  createTrainingWebSocket(projectId, callbacks = {}) {
    const wsUrl = WS_ENDPOINTS.P2P_TRAINING(projectId)
    const ws = new WebSocket(wsUrl)

    ws.onopen = (event) => {
      console.log('Training WebSocket connected:', wsUrl)
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
      console.error('Training WebSocket error:', event)
      callbacks.onError?.(event)
    }

    ws.onclose = (event) => {
      console.log('Training WebSocket closed:', event)
      callbacks.onClose?.(event)
    }

    return ws
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
    const response = await apiClient.get(API_ENDPOINTS.P2P_AI.NODES.LIST, { params })
    return response.data
  },

  /**
   * 获取节点详情
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 节点详情
   */
  async getNode(nodeId) {
    const url = API_ENDPOINTS.P2P_AI.NODES.DETAIL.replace('{id}', nodeId)
    const response = await apiClient.get(url)
    return response.data
  },

  /**
   * 启动节点
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 操作结果
   */
  async startNode(nodeId) {
    const url = API_ENDPOINTS.P2P_AI.NODES.START.replace('{id}', nodeId)
    const response = await apiClient.post(url)
    return response.data
  },

  /**
   * 停止节点
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 操作结果
   */
  async stopNode(nodeId) {
    const url = API_ENDPOINTS.P2P_AI.NODES.STOP.replace('{id}', nodeId)
    const response = await apiClient.post(url)
    return response.data
  },

  /**
   * 重启节点
   * @param {string} nodeId - 节点ID
   * @returns {Promise<Object>} 操作结果
   */
  async restartNode(nodeId) {
    const url = API_ENDPOINTS.P2P_AI.NODES.RESTART.replace('{id}', nodeId)
    const response = await apiClient.post(url)
    return response.data
  },

  /**
   * 获取节点统计
   * @returns {Promise<Object>} 节点统计数据
   */
  async getNodeStats() {
    const response = await apiClient.get(API_ENDPOINTS.P2P_AI.NODES.STATS)
    return response.data
  }
}

/**
 * 数据集管理服务
 */
export const datasetService = {
  /**
   * 获取数据集列表
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} 数据集列表
   */
  async getDatasets(params = {}) {
    const response = await apiClient.get(API_ENDPOINTS.P2P_AI.DATASETS.LIST, { params })
    return response.data
  },

  /**
   * 上传数据集
   * @param {FormData} formData - 表单数据
   * @param {Function} onProgress - 上传进度回调
   * @returns {Promise<Object>} 上传结果
   */
  async uploadDataset(formData, onProgress) {
    return await uploadWithProgress(API_ENDPOINTS.P2P_AI.DATASETS.UPLOAD, formData, onProgress)
  },

  /**
   * 创建数据集记录
   * @param {Object} datasetData - 数据集数据
   * @returns {Promise<Object>} 创建结果
   */
  async createDataset(datasetData) {
    const response = await apiClient.post(API_ENDPOINTS.P2P_AI.DATASETS.CREATE, datasetData)
    return response.data
  },

  /**
   * 删除数据集
   * @param {string} datasetId - 数据集ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteDataset(datasetId) {
    const url = API_ENDPOINTS.P2P_AI.DATASETS.DELETE.replace('{id}', datasetId)
    const response = await apiClient.delete(url)
    return response.data
  },

  /**
   * 下载数据集
   * @param {string} datasetId - 数据集ID
   * @param {string} filename - 文件名
   * @returns {Promise} 下载响应
   */
  async downloadDataset(datasetId, filename) {
    const url = API_ENDPOINTS.P2P_AI.DATASETS.DOWNLOAD.replace('{id}', datasetId)
    return await downloadFile(url, filename)
  },

  /**
   * 获取数据集统计
   * @returns {Promise<Object>} 数据集统计
   */
  async getDatasetStats() {
    const response = await apiClient.get(API_ENDPOINTS.P2P_AI.DATASETS.STATS)
    return response.data
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
    const response = await apiClient.get(API_ENDPOINTS.P2P_AI.MODELS.LIST, { params })
    return response.data
  },

  /**
   * 导出模型
   * @param {string} modelId - 模型ID
   * @param {Object} exportConfig - 导出配置
   * @returns {Promise<Object>} 导出结果
   */
  async exportModel(modelId, exportConfig) {
    const url = API_ENDPOINTS.P2P_AI.MODELS.EXPORT.replace('{id}', modelId)
    const response = await apiClient.post(url, exportConfig)
    return response.data
  },

  /**
   * 部署模型
   * @param {string} modelId - 模型ID
   * @param {Object} deployConfig - 部署配置
   * @returns {Promise<Object>} 部署结果
   */
  async deployModel(modelId, deployConfig) {
    const url = API_ENDPOINTS.P2P_AI.MODELS.DEPLOY.replace('{id}', modelId)
    const response = await apiClient.post(url, deployConfig)
    return response.data
  },

  /**
   * 评估模型
   * @param {string} modelId - 模型ID
   * @param {Object} evalConfig - 评估配置
   * @returns {Promise<Object>} 评估结果
   */
  async evaluateModel(modelId, evalConfig) {
    const url = API_ENDPOINTS.P2P_AI.MODELS.EVALUATE.replace('{id}', modelId)
    const response = await apiClient.post(url, evalConfig)
    return response.data
  },

  /**
   * 获取模型版本
   * @param {string} modelId - 模型ID
   * @returns {Promise<Object>} 模型版本列表
   */
  async getModelVersions(modelId) {
    const url = API_ENDPOINTS.P2P_AI.MODELS.VERSIONS.replace('{id}', modelId)
    const response = await apiClient.get(url)
    return response.data
  },

  /**
   * 获取模型统计
   * @returns {Promise<Object>} 模型统计
   */
  async getModelStats() {
    const response = await apiClient.get(API_ENDPOINTS.P2P_AI.MODELS.STATS)
    return response.data
  }
}

// 导出所有服务
export default {
  projects: projectService,
  training: trainingService,
  nodes: nodeService,
  datasets: datasetService,
  models: modelService
}