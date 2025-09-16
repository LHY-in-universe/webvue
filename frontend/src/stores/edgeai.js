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
      
      if (projectsResult && Array.isArray(projectsResult)) {
        projects.value = projectsResult.map(project => ({
          id: project.id,
          name: project.name,
          description: project.description,
          type: project.type || 'general',
          status: project.status,
          progress: project.progress || 0,
          connectedNodes: project.connected_nodes || 0,
          currentEpoch: project.current_epoch || 0,
          totalEpochs: project.total_epochs || 100,
          modelType: project.model_type || 'cnn',
          batchSize: project.batch_size || 32,
          learningRate: project.learning_rate || 0.001,
          created: project.created,
          lastUpdate: project.last_update,
          metrics: project.metrics || {
            accuracy: 0,
            loss: 0,
            f1_score: 0,
            precision: 0,
            recall: 0
          }
        }))
      }
      
      if (nodesResult && Array.isArray(nodesResult)) {
        nodes.value = nodesResult.map(node => ({
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
      connectionError.value = `API Error: ${error.message}`
      
      // Clear any existing data on error
      projects.value = []
      nodes.value = []
      
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
    // Enable WebSocket in all modes, including development
    console.log('EdgeAI WebSocket connecting...')

    // Close existing connection if any
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }

    try {
      // Use proper WebSocket URL for EdgeAI monitoring
      const wsUrl = `ws://localhost:8000/api/edgeai/nodes/ws/control-1`
      console.log('Connecting to WebSocket:', wsUrl)

      ws.value = new WebSocket(wsUrl)

      ws.value.onopen = () => {
        isConnected.value = true
        connectionError.value = null
        connectionRetries.value = 0
        console.log('EdgeAI WebSocket connected')
        lastUpdate.value = new Date()
      }

      ws.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          handleWebSocketMessage(data)
          lastUpdate.value = new Date()
        } catch (parseError) {
          console.error('Error parsing WebSocket message:', parseError, 'Raw data:', event.data)
        }
      }

      ws.value.onclose = (event) => {
        isConnected.value = false
        console.log(`EdgeAI WebSocket closed. Code: ${event.code}, Reason: ${event.reason}`)

        // Only retry if it wasn't a manual close and we haven't exceeded max retries
        if (event.code !== 1000 && connectionRetries.value < maxRetries) {
          const retryDelay = 3000 * Math.pow(2, connectionRetries.value) // Exponential backoff
          console.log(`Retrying WebSocket connection in ${retryDelay}ms (attempt ${connectionRetries.value + 1}/${maxRetries})`)

          setTimeout(() => {
            connectionRetries.value++
            connectWebSocket()
          }, retryDelay)
        } else if (connectionRetries.value >= maxRetries) {
          connectionError.value = 'WebSocket connection failed after multiple retries. Running in offline mode.'
          console.warn('Max WebSocket retries reached. Switching to offline mode.')
        }
      }

      ws.value.onerror = (error) => {
        isConnected.value = false
        connectionError.value = 'WebSocket connection failed'
        console.error('EdgeAI WebSocket error:', {
          error,
          readyState: ws.value?.readyState,
          url: ws.value?.url
        })
      }

      // Set a timeout for connection establishment
      setTimeout(() => {
        if (ws.value && ws.value.readyState === WebSocket.CONNECTING) {
          console.warn('WebSocket connection timeout, closing...')
          ws.value.close()
        }
      }, 10000) // 10 second timeout

    } catch (error) {
      isConnected.value = false
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
      // Format data for API - only send required fields
      const apiData = {
        name: projectData.name,
        description: projectData.description,
        type: projectData.type || projectData.project_type || 'manufacturing',
        model_type: projectData.modelType || projectData.model_type || 'cnn'
      }

      console.log('EdgeAI Store - Original projectData:', projectData)
      console.log('EdgeAI Store - Sending apiData to backend:', apiData)

      // Call real API to create project
      const result = await edgeaiService.projects.createProject(apiData)
      
      if (result) {
        const newProject = {
          id: result.id,
          name: result.name,
          description: result.description,
          type: result.type || 'general',
          status: result.status || 'created',
          progress: result.progress || 0,
          connectedNodes: result.connected_nodes || 0,
          currentEpoch: result.current_epoch || 0,
          totalEpochs: result.total_epochs || 100,
          modelType: result.model_type || 'neural_network',
          batchSize: result.batch_size || 32,
          learningRate: result.learning_rate || 0.001,
          created: result.created_at,
          lastUpdate: result.updated_at,
          metrics: result.metrics || {
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
    if (!updatedProject || !updatedProject.id) {
      console.warn('Invalid project data received for update:', updatedProject)
      return
    }
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
    if (!updatedNode || !updatedNode.id) {
      console.warn('Invalid node data received for update:', updatedNode)
      return
    }
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
      const result = await edgeaiService.nodes.restartNode(nodeId)
      
      if (result && result.success !== false) {
        // Update node in local state
        const node = nodes.value.find(n => n.id === nodeId)
        if (node) {
          node.status = 'online'
          node.lastSeen = 'just now'
        }
        return { success: true }
      } else {
        return { success: false, error: result?.message || 'Failed to restart node' }
      }
    } catch (error) {
      console.error('Failed to restart node:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }

  const addNode = async (nodeData) => {
    loading.value.operations = true
    try {
      const result = await edgeaiService.nodes.addNode(nodeData)
      
      if (result && result.data) {
        const newNode = {
          id: result.data.id,
          name: result.data.name,
          type: result.data.node_type || 'edge',
          status: result.data.status || 'offline',
          project: result.data.current_project || 'unassigned',
          location: result.data.location || 'Unknown',
          cpuUsage: result.data.cpu_usage || 0,
          memoryUsage: result.data.memory_usage || 0,
          gpuUsage: result.data.gpu_usage || 0,
          progress: result.data.progress || 0,
          currentEpoch: result.data.current_epoch || 0,
          totalEpochs: result.data.total_epochs || 0,
          lastSeen: result.data.last_seen || 'unknown',
          connections: result.data.connections || []
        }
        
        nodes.value.push(newNode)
        return { success: true, node: newNode }
      } else {
        return { success: false, error: 'Invalid API response' }
      }
    } catch (error) {
      console.error('Failed to add node:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }

  const connectToNode = async (nodeId) => {
    loading.value.operations = true
    try {
      const result = await edgeaiService.nodes.connectToNode(nodeId)
      
      if (result && result.success !== false) {
        const node = nodes.value.find(n => n.id === nodeId)
        if (node) {
          node.status = 'online'
          node.lastSeen = 'just now'
        }
        return { success: true }
      } else {
        return { success: false, error: result?.message || 'Failed to connect to node' }
      }
    } catch (error) {
      console.error('Failed to connect to node:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }

  const disconnectFromNode = async (nodeId) => {
    loading.value.operations = true
    try {
      const result = await edgeaiService.nodes.disconnectFromNode(nodeId)
      
      if (result && result.success !== false) {
        const node = nodes.value.find(n => n.id === nodeId)
        if (node) {
          node.status = 'offline'
          node.lastSeen = 'just now'
        }
        return { success: true }
      } else {
        return { success: false, error: result?.message || 'Failed to disconnect from node' }
      }
    } catch (error) {
      console.error('Failed to disconnect from node:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }

  const exportNodes = async (exportParams = {}) => {
    loading.value.operations = true
    try {
      const result = await edgeaiService.nodes.exportNodes(exportParams)
      return result
    } catch (error) {
      console.error('Failed to export nodes:', error)
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
  const importProject = async (formData, onProgress) => {
    loading.value.projects = true
    try {
      // Call real API to import project with correct signature
      const result = await edgeaiService.projects.importProject(formData, onProgress)

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
    addNode,
    connectToNode,
    disconnectFromNode,
    exportNodes,
    setSelectedNode,
    updateConfig,
    refreshData,
    importProject,
    exportProject,
    cleanup
  }
})