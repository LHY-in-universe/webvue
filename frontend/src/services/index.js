/**
 * Services Index
 * 统一导出所有API服务
 */

export { default as authService } from './authService.js'
export { default as p2paiService } from './p2paiService.js'
export { default as edgeaiService } from './edgeaiService.js'
export { default as apiClient } from './apiClient.js'

// 导出特定服务的子模块
export {
  projectService as p2paiProjectService,
  trainingService as p2paiTrainingService,
  nodeService as p2paiNodeService,
  datasetService as p2paiDatasetService,
  modelService as p2paiModelService
} from './p2paiService.js'

export {
  projectService as edgeaiProjectService,
  nodeService as edgeaiNodeService,
  trainingService as edgeaiTrainingService,
  performanceService as edgeaiPerformanceService,
  logService as edgeaiLogService,
  taskService as edgeaiTaskService
} from './edgeaiService.js'