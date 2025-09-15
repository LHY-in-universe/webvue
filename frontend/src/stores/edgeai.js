import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import edgeaiService from '@/services/edgeaiService'

export const useEdgeAIStore = defineStore('edgeai', () => {
  // State
  const projects = ref([])
  const nodes = ref([])
  const currentProject = ref(null)
  const selectedNode = ref(null)
  const isConnected = ref(false)
  const lastUpdate = ref(null)
  const connectionError = ref(null)
  
  // WebSocket connection
  const ws = ref(null)
  const connectionRetries = ref(0)
  const maxRetries = 3
  
  // Loading states
  const loading = ref({
    projects: false,
    nodes: false,
    operations: false
  })
  
  // Configuration
  const config = ref({
    autoRefresh: true,
    refreshInterval: 5000,
    enableAnimations: true,
    showNotifications: true
  })

  // Computed properties
  const activeProjects = computed(() => 
    projects.value.filter(p => p.status === 'active' || p.status === 'training')
  )
  
  const onlineNodes = computed(() => 
    nodes.value.filter(n => ['online', 'training', 'idle'].includes(n.status))
  )
  
  const trainingNodes = computed(() => 
    nodes.value.filter(n => n.status === 'training')
  )
  
  const errorNodes = computed(() => 
    nodes.value.filter(n => n.status === 'error')
  )
  
  const nodesByProject = computed(() => {
    const grouped = {}
    nodes.value.forEach(node => {
      const project = node.project || 'unassigned'
      if (!grouped[project]) {
        grouped[project] = []
      }
      grouped[project].push(node)
    })
    return grouped
  })

  const systemStats = computed(() => ({
    totalProjects: projects.value.length,
    activeProjects: activeProjects.value.length,
    totalNodes: nodes.value.length,
    onlineNodes: onlineNodes.value.length,
    trainingNodes: trainingNodes.value.length,
    errorNodes: errorNodes.value.length,
    completionRate: projects.value.length > 0 
      ? Math.round((activeProjects.value.length / projects.value.length) * 100)
      : 0
  }))

  // Actions
  const initializeStore = async () => {
    // Load real data from API
    await loadRealData()
    
    // Setup WebSocket connection if enabled
    if (config.value.autoRefresh) {
      connectWebSocket()
    }
  }
  
  const loadRealData = async () => {
    loading.value.projects = true
    loading.value.nodes = true
    
    try {
      // Load projects and nodes from API
      const [projectsResult, nodesResult] = await Promise.all([
        edgeaiService.projects.getProjects(),
        edgeaiService.nodes.getNodes()
      ])
      
      if (projectsResult && projectsResult.data) {
        projects.value = projectsResult.data.map(project => ({
          id: project.id,
          name: project.name,
          description: project.description,
          type: project.project_type || 'general',
          status: project.status,
          progress: project.progress || 0,
          connectedNodes: project.connected_nodes || 0,
          currentEpoch: project.current_epoch || 0,
          totalEpochs: project.total_epochs || 100,
          modelType: project.model_type || 'neural_network',
          batchSize: project.batch_size || 32,
          learningRate: project.learning_rate || 0.001,
          created: project.created_at,
          lastUpdate: project.updated_at,
          metrics: project.metrics || {
            accuracy: 0,
            loss: 0,
            f1Score: 0
          }
        }))
      }
      
      if (nodesResult && nodesResult.data) {
        nodes.value = nodesResult.data.map(node => ({
          id: node.id,
          name: node.name,
          type: node.node_type || 'edge',
          status: node.status,
          project: node.current_project || 'unassigned',
          location: node.location || 'Unknown',
          cpuUsage: node.cpu_usage || 0,
          memoryUsage: node.memory_usage || 0,
          gpuUsage: node.gpu_usage || 0,
          progress: node.progress || 0,
          currentEpoch: node.current_epoch || 0,
          totalEpochs: node.total_epochs || 0,
          lastSeen: node.last_seen || 'unknown',
          connections: node.connections || []
        }))
      }
      
      lastUpdate.value = new Date().toISOString()
      
      return { success: true }
    } catch (error) {
      console.error('Failed to load real data:', error)
      // Fallback to mock data
      loadMockData()
      return { success: false, error: error.message }
    } finally {
      loading.value.projects = false
      loading.value.nodes = false
    }
  }

  const loadMockData = () => {
    // Mock projects data
    projects.value = [
      {
        id: 'proj-001',
        name: 'Smart Manufacturing Monitor',
        description: 'EdgeAI-based real-time factory equipment monitoring and predictive maintenance system',
        type: 'manufacturing',
        status: 'training',
        progress: 65,
        connectedNodes: 8,
        currentEpoch: 65,
        totalEpochs: 100,
        modelType: 'cnn',
        batchSize: 32,
        learningRate: 0.001,
        created: '2024-01-15',
        lastUpdate: '2 hours ago',
        metrics: {
          accuracy: 87.5,
          loss: 0.234,
          f1Score: 85.2
        }
      },
      {
        id: 'proj-002',
        name: 'Urban Traffic Optimization',
        description: 'Intelligent traffic signal control and flow prediction system',
        type: 'traffic',
        status: 'active',
        progress: 100,
        connectedNodes: 15,
        currentEpoch: 100,
        totalEpochs: 100,
        modelType: 'rnn',
        batchSize: 64,
        learningRate: 0.0001,
        created: '2024-01-10',
        lastUpdate: '30 minutes ago',
        metrics: {
          accuracy: 92.1,
          loss: 0.156,
          f1Score: 90.8
        }
      },
      {
        id: 'proj-003',
        name: 'Medical Image Diagnosis',
        description: 'Distributed medical imaging AI diagnostic system',
        type: 'medical',
        status: 'paused',
        progress: 45,
        connectedNodes: 5,
        currentEpoch: 45,
        totalEpochs: 100,
        modelType: 'transformer',
        batchSize: 16,
        learningRate: 0.0005,
        created: '2024-01-08',
        lastUpdate: '1 day ago',
        metrics: {
          accuracy: 78.3,
          loss: 0.412,
          f1Score: 76.5
        }
      }
    ]

    // Mock nodes data
    nodes.value = [
      {
        id: 'control-1',
        name: 'Control Center',
        type: 'control',
        status: 'online',
        project: 'System',
        location: 'US East',
        cpuUsage: 35,
        memoryUsage: 45,
        gpuUsage: 0,
        progress: 0,
        lastSeen: '1 second ago',
        connections: ['edge-1', 'edge-2', 'edge-3']
      },
      {
        id: 'edge-1',
        name: 'Factory Node A',
        type: 'edge',
        status: 'training',
        project: 'Smart Manufacturing Monitor',
        location: 'US East',
        cpuUsage: 75,
        memoryUsage: 68,
        gpuUsage: 85,
        progress: 65,
        currentEpoch: 65,
        totalEpochs: 100,
        lastSeen: '2 seconds ago',
        connections: ['control-1']
      },
      {
        id: 'edge-2',
        name: 'Traffic Hub Central',
        type: 'edge',
        status: 'training',
        project: 'Urban Traffic Optimization',
        location: 'US West',
        cpuUsage: 82,
        memoryUsage: 71,
        gpuUsage: 88,
        progress: 78,
        currentEpoch: 78,
        totalEpochs: 100,
        lastSeen: '1 minute ago',
        connections: ['control-1']
      },
      {
        id: 'edge-3',
        name: 'Medical Center Node',
        type: 'edge',
        status: 'idle',
        project: 'Medical Image Diagnosis',
        location: 'EU Central',
        cpuUsage: 15,
        memoryUsage: 25,
        gpuUsage: 0,
        progress: 0,
        lastSeen: '30 seconds ago',
        connections: ['control-1']
      },
      {
        id: 'edge-4',
        name: 'Retail Analytics Hub',
        type: 'edge',
        status: 'error',
        project: 'Retail Traffic Analysis',
        location: 'Asia Pacific',
        cpuUsage: 0,
        memoryUsage: 0,
        gpuUsage: 0,
        progress: 23,
        currentEpoch: 23,
        totalEpochs: 100,
        lastSeen: '2 hours ago',
        connections: []
      }
    ]

    lastUpdate.value = new Date().toISOString()
  }

  const connectWebSocket = () => {
    // Disable WebSocket in development mode for demo purposes
    if (import.meta.env.MODE === 'development') {
      console.log('EdgeAI WebSocket disabled in development mode')
      // Simulate connection for demo
      setTimeout(() => {
        isConnected.value = true
        connectionError.value = null
        console.log('EdgeAI WebSocket simulated connection (demo mode)')
      }, 1000)
      return
    }

    if (ws.value) {
      ws.value.close()
    }

    try {
      // Mock WebSocket URL (in real implementation, this would be actual WebSocket server)
      ws.value = new WebSocket('ws://localhost:8080/edgeai/ws')
      
      ws.value.onopen = () => {
        isConnected.value = true
        connectionError.value = null
        connectionRetries.value = 0
        console.log('EdgeAI WebSocket connected')
      }

      ws.value.onmessage = (event) => {
        handleWebSocketMessage(JSON.parse(event.data))
      }

      ws.value.onclose = () => {
        isConnected.value = false
        if (connectionRetries.value < maxRetries) {
          setTimeout(() => {
            connectionRetries.value++
            connectWebSocket()
          }, 3000 * Math.pow(2, connectionRetries.value))
        }
      }

      ws.value.onerror = (error) => {
        connectionError.value = 'WebSocket connection failed'
        console.error('EdgeAI WebSocket error:', error)
      }
    } catch (error) {
      connectionError.value = 'Failed to establish WebSocket connection'
      console.error('WebSocket connection error:', error)
    }
  }

  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'node_update':
        updateNode(data.payload)
        break
      case 'project_update':
        updateProject(data.payload)
        break
      case 'task_update':
        // Handle task status updates
        if (data.payload && data.payload.id) {
          // Find and update task if it exists in any project
          console.log('Task update received:', data.payload)
        }
        break
      case 'model_update':
        // Handle model deployment/status changes
        if (data.payload && data.payload.id) {
          console.log('Model update received:', data.payload)
        }
        break
      case 'system_stats':
        // Handle system statistics update
        lastUpdate.value = new Date().toISOString()
        break
      case 'system_log':
        // Handle new system log entries
        if (data.payload && data.payload.message) {
          console.log('New system log:', data.payload)
        }
        break
      case 'training_progress':
        // Handle training progress updates
        if (data.payload && data.payload.project_id) {
          updateProjectProgress(data.payload)
        }
        break
      default:
        console.log('Unknown WebSocket message type:', data.type, data)
    }
  }
  
  // Enhanced project progress update handler
  const updateProjectProgress = (progressData) => {
    const project = projects.value.find(p => p.id === progressData.project_id)
    if (project) {
      project.progress = progressData.progress || project.progress
      project.currentEpoch = progressData.current_epoch || project.currentEpoch
      if (progressData.metrics) {
        project.metrics = { ...project.metrics, ...progressData.metrics }
      }
      project.lastUpdate = 'just now'
    }
  }

  const disconnectWebSocket = () => {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
    isConnected.value = false
  }

  // Project management
  const createProject = async (projectData) => {
    loading.value.projects = true
    try {
      // Call real API to create project
      const result = await edgeaiService.projects.createProject(projectData)
      
      if (result && result.data) {
        const newProject = {
          id: result.data.id,
          name: result.data.name,
          description: result.data.description,
          type: result.data.project_type || 'general',
          status: result.data.status || 'created',
          progress: result.data.progress || 0,
          connectedNodes: result.data.connected_nodes || 0,
          currentEpoch: result.data.current_epoch || 0,
          totalEpochs: result.data.total_epochs || 100,
          modelType: result.data.model_type || 'neural_network',
          batchSize: result.data.batch_size || 32,
          learningRate: result.data.learning_rate || 0.001,
          created: result.data.created_at,
          lastUpdate: result.data.updated_at,
          metrics: result.data.metrics || {
            accuracy: 0,
            loss: 0,
            f1Score: 0
          }
        }
        
        projects.value.push(newProject)
        return { success: true, project: newProject }
      } else {
        return { success: false, error: 'Invalid API response' }
      }
    } catch (error) {
      console.error('Failed to create project:', error)
      return { success: false, error: error.message || 'Failed to create project' }
    } finally {
      loading.value.projects = false
    }
  }

  const updateProject = (updatedProject) => {
    const index = projects.value.findIndex(p => p.id === updatedProject.id)
    if (index !== -1) {
      projects.value[index] = { ...projects.value[index], ...updatedProject }
    }
  }

  const deleteProject = async (projectId) => {
    loading.value.operations = true
    try {
      // Call real API to delete project
      const result = await edgeaiService.projects.deleteProject(projectId)
      
      if (result && result.success !== false) {
        projects.value = projects.value.filter(p => p.id !== projectId)
        return { success: true }
      } else {
        return { success: false, error: result?.error || 'Failed to delete project' }
      }
    } catch (error) {
      console.error('Failed to delete project:', error)
      return { success: false, error: error.message || 'Failed to delete project' }
    } finally {
      loading.value.operations = false
    }
  }

  const setCurrentProject = (project) => {
    currentProject.value = project
  }

  // Node management
  const updateNode = (updatedNode) => {
    const index = nodes.value.findIndex(n => n.id === updatedNode.id)
    if (index !== -1) {
      nodes.value[index] = { ...nodes.value[index], ...updatedNode }
    }
  }

  const startNodeTraining = async (nodeId) => {
    loading.value.operations = true
    try {
      await new Promise(resolve => setTimeout(resolve, 800))
      const node = nodes.value.find(n => n.id === nodeId)
      if (node) {
        node.status = 'training'
        node.lastSeen = 'just now'
      }
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }

  const stopNodeTraining = async (nodeId) => {
    loading.value.operations = true
    try {
      await new Promise(resolve => setTimeout(resolve, 800))
      const node = nodes.value.find(n => n.id === nodeId)
      if (node) {
        node.status = 'idle'
        node.lastSeen = 'just now'
      }
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }

  const restartNode = async (nodeId) => {
    loading.value.operations = true
    try {
      await new Promise(resolve => setTimeout(resolve, 1200))
      const node = nodes.value.find(n => n.id === nodeId)
      if (node) {
        node.status = 'online'
        node.cpuUsage = Math.random() * 30 + 10
        node.memoryUsage = Math.random() * 40 + 20
        node.lastSeen = 'just now'
      }
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }

  const setSelectedNode = (node) => {
    selectedNode.value = node
  }

  // Configuration management
  const updateConfig = (newConfig) => {
    config.value = { ...config.value, ...newConfig }
    
    // Apply configuration changes
    if (newConfig.autoRefresh !== undefined) {
      if (newConfig.autoRefresh && !isConnected.value) {
        connectWebSocket()
      } else if (!newConfig.autoRefresh && isConnected.value) {
        disconnectWebSocket()
      }
    }
  }

  // Data refresh
  const refreshData = async () => {
    return await loadRealData()
  }

  // Import/Export
  const importProject = async (projectData) => {
    loading.value.projects = true
    try {
      // Call real API to import project
      const result = await edgeaiService.projects.importProject(projectData)
      
      if (result && result.data) {
        const importedProject = {
          id: result.data.id,
          name: result.data.name,
          description: result.data.description,
          type: result.data.project_type || 'general',
          status: result.data.status || 'imported',
          progress: result.data.progress || 0,
          connectedNodes: result.data.connected_nodes || 0,
          currentEpoch: result.data.current_epoch || 0,
          totalEpochs: result.data.total_epochs || 100,
          modelType: result.data.model_type || 'neural_network',
          batchSize: result.data.batch_size || 32,
          learningRate: result.data.learning_rate || 0.001,
          created: result.data.created_at,
          lastUpdate: result.data.updated_at,
          metrics: result.data.metrics || {
            accuracy: 0,
            loss: 0,
            f1Score: 0
          }
        }
        
        projects.value.push(importedProject)
        return { success: true, project: importedProject }
      } else {
        return { success: false, error: 'Invalid API response' }
      }
    } catch (error) {
      console.error('Failed to import project:', error)
      return { success: false, error: error.message || 'Failed to import project' }
    } finally {
      loading.value.projects = false
    }
  }

  const exportProject = async (projectId) => {
    const project = projects.value.find(p => p.id === projectId)
    if (!project) {
      return { success: false, error: 'Project not found' }
    }

    try {
      const exportData = {
        ...project,
        exportedAt: new Date().toISOString(),
        version: '1.0.0'
      }
      
      return { success: true, data: exportData }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }

  // Cleanup
  const cleanup = () => {
    disconnectWebSocket()
  }

  return {
    // State
    projects,
    nodes,
    currentProject,
    selectedNode,
    isConnected,
    lastUpdate,
    connectionError,
    loading,
    config,
    
    // Computed
    activeProjects,
    onlineNodes,
    trainingNodes,
    errorNodes,
    nodesByProject,
    systemStats,
    
    // Actions
    initializeStore,
    connectWebSocket,
    disconnectWebSocket,
    createProject,
    updateProject,
    updateProjectProgress,
    deleteProject,
    setCurrentProject,
    updateNode,
    startNodeTraining,
    stopNodeTraining,
    restartNode,
    setSelectedNode,
    updateConfig,
    refreshData,
    importProject,
    exportProject,
    cleanup
  }
})