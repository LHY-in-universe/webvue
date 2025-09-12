import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useEdgeAIStore } from '@/stores/edgeai'

export const useEdgeAINodes = () => {
  const edgeaiStore = useEdgeAIStore()
  
  const nodes = computed(() => edgeaiStore.nodes)
  const onlineNodes = computed(() => edgeaiStore.onlineNodes)
  const trainingNodes = computed(() => edgeaiStore.trainingNodes)
  const errorNodes = computed(() => edgeaiStore.errorNodes)
  
  const getNodesByProject = (projectId) => {
    return nodes.value.filter(node => node.project === projectId)
  }
  
  const getNodeStatus = (nodeId) => {
    const node = nodes.value.find(n => n.id === nodeId)
    return node ? node.status : 'unknown'
  }
  
  const startTraining = async (nodeId) => {
    return await edgeaiStore.startNodeTraining(nodeId)
  }
  
  const stopTraining = async (nodeId) => {
    return await edgeaiStore.stopNodeTraining(nodeId)
  }
  
  const restartNode = async (nodeId) => {
    return await edgeaiStore.restartNode(nodeId)
  }
  
  return {
    nodes,
    onlineNodes,
    trainingNodes,
    errorNodes,
    getNodesByProject,
    getNodeStatus,
    startTraining,
    stopTraining,
    restartNode
  }
}

export const useEdgeAIProjects = () => {
  const edgeaiStore = useEdgeAIStore()
  
  const projects = computed(() => edgeaiStore.projects)
  const activeProjects = computed(() => edgeaiStore.activeProjects)
  const currentProject = computed(() => edgeaiStore.currentProject)
  
  const getProject = (projectId) => {
    return projects.value.find(p => p.id === projectId)
  }
  
  const createProject = async (projectData) => {
    return await edgeaiStore.createProject(projectData)
  }
  
  const updateProject = (projectData) => {
    edgeaiStore.updateProject(projectData)
  }
  
  const deleteProject = async (projectId) => {
    return await edgeaiStore.deleteProject(projectId)
  }
  
  const setCurrentProject = (project) => {
    edgeaiStore.setCurrentProject(project)
  }
  
  return {
    projects,
    activeProjects,
    currentProject,
    getProject,
    createProject,
    updateProject,
    deleteProject,
    setCurrentProject
  }
}

export const useEdgeAIConnection = () => {
  const edgeaiStore = useEdgeAIStore()
  
  const isConnected = computed(() => edgeaiStore.isConnected)
  const connectionError = computed(() => edgeaiStore.connectionError)
  const lastUpdate = computed(() => edgeaiStore.lastUpdate)
  
  const connect = () => {
    edgeaiStore.connectWebSocket()
  }
  
  const disconnect = () => {
    edgeaiStore.disconnectWebSocket()
  }
  
  const refreshData = async () => {
    return await edgeaiStore.refreshData()
  }
  
  return {
    isConnected,
    connectionError,
    lastUpdate,
    connect,
    disconnect,
    refreshData
  }
}

export const useEdgeAIStats = () => {
  const edgeaiStore = useEdgeAIStore()
  
  const systemStats = computed(() => edgeaiStore.systemStats)
  const loading = computed(() => edgeaiStore.loading)
  
  const getTotalResources = () => {
    const nodes = edgeaiStore.nodes
    return {
      totalCPU: nodes.reduce((sum, node) => sum + (node.cpuCores || 0), 0),
      totalMemory: nodes.reduce((sum, node) => sum + (node.memoryGB || 0), 0),
      totalGPU: nodes.reduce((sum, node) => sum + (node.gpuCount || 0), 0),
      avgCPUUsage: nodes.length > 0 
        ? nodes.reduce((sum, node) => sum + node.cpuUsage, 0) / nodes.length 
        : 0,
      avgMemoryUsage: nodes.length > 0 
        ? nodes.reduce((sum, node) => sum + node.memoryUsage, 0) / nodes.length 
        : 0
    }
  }
  
  const getProjectProgress = (projectId) => {
    const project = edgeaiStore.projects.find(p => p.id === projectId)
    if (!project) return 0
    
    const projectNodes = edgeaiStore.nodes.filter(n => n.project === project.name)
    if (projectNodes.length === 0) return project.progress || 0
    
    return projectNodes.reduce((sum, node) => sum + (node.progress || 0), 0) / projectNodes.length
  }
  
  return {
    systemStats,
    loading,
    getTotalResources,
    getProjectProgress
  }
}

export const useEdgeAILifecycle = () => {
  const edgeaiStore = useEdgeAIStore()
  
  onMounted(() => {
    edgeaiStore.initializeStore()
  })
  
  onUnmounted(() => {
    edgeaiStore.cleanup()
  })
  
  return {
    initialize: () => edgeaiStore.initializeStore(),
    cleanup: () => edgeaiStore.cleanup()
  }
}

export const useEdgeAIImportExport = () => {
  const edgeaiStore = useEdgeAIStore()
  
  const importProject = async (projectData) => {
    return await edgeaiStore.importProject(projectData)
  }
  
  const exportProject = async (projectId) => {
    return await edgeaiStore.exportProject(projectId)
  }
  
  const downloadProjectData = (projectData, filename = 'project-export.json') => {
    const dataStr = JSON.stringify(projectData, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    link.click()
    
    URL.revokeObjectURL(url)
  }
  
  return {
    importProject,
    exportProject,
    downloadProjectData
  }
}

export const useEdgeAIConfig = () => {
  const edgeaiStore = useEdgeAIStore()
  
  const config = computed(() => edgeaiStore.config)
  
  const updateConfig = (newConfig) => {
    edgeaiStore.updateConfig(newConfig)
  }
  
  const toggleAutoRefresh = () => {
    updateConfig({ autoRefresh: !config.value.autoRefresh })
  }
  
  const toggleAnimations = () => {
    updateConfig({ enableAnimations: !config.value.enableAnimations })
  }
  
  const toggleNotifications = () => {
    updateConfig({ showNotifications: !config.value.showNotifications })
  }
  
  const setRefreshInterval = (interval) => {
    updateConfig({ refreshInterval: interval })
  }
  
  return {
    config,
    updateConfig,
    toggleAutoRefresh,
    toggleAnimations,
    toggleNotifications,
    setRefreshInterval
  }
}