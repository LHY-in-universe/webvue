import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useApiOptimization } from '@/composables/useApiOptimization'
import p2paiService from '@/services/p2paiService'
import performanceMonitor from '@/utils/performanceMonitor'
import { storeLogger } from '@/utils/logger'

export const useP2PAIStore = defineStore('p2pai', () => {
  // State
  const projects = ref([])
  const participants = ref([])
  const currentProject = ref(null)
  const selectedParticipant = ref(null)
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
    participants: false,
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
  
  const onlineParticipants = computed(() => 
    participants.value.filter(p => ['online', 'training', 'idle'].includes(p.status))
  )
  
  const trainingParticipants = computed(() => 
    participants.value.filter(p => p.status === 'training')
  )
  
  const errorParticipants = computed(() => 
    participants.value.filter(p => p.status === 'error')
  )
  
  const participantsByProject = computed(() => {
    const grouped = {}
    participants.value.forEach(participant => {
      const project = participant.project || 'unassigned'
      if (!grouped[project]) {
        grouped[project] = []
      }
      grouped[project].push(participant)
    })
    return grouped
  })

  const systemStats = computed(() => ({
    totalProjects: projects.value.length,
    activeProjects: activeProjects.value.length,
    totalParticipants: participants.value.length,
    onlineParticipants: onlineParticipants.value.length,
    trainingParticipants: trainingParticipants.value.length,
    errorParticipants: errorParticipants.value.length,
    completionRate: projects.value.length > 0 
      ? Math.round((activeProjects.value.length / projects.value.length) * 100)
      : 0
  }))

  // Actions
  const initializeStore = async () => {
    // Initialize with real data from API
    await loadRealData()
    
    // Setup WebSocket connection if enabled
    if (config.value.autoRefresh) {
      connectWebSocket()
    }
  }

  // Load real data from API
  const loadRealData = async () => {
    const pageMonitor = performanceMonitor.monitorPageLoad('P2PAIStore')
    const { cachedApiCall } = useApiOptimization()
    
    loading.value.projects = true
    loading.value.participants = true
    
    try {
      const [projectsResult, nodesResult] = await Promise.all([
        cachedApiCall('p2pai-projects', 
          () => p2paiService.projects.getProjects(), 
          60 * 1000 // Cache for 1 minute
        ),
        cachedApiCall('p2pai-nodes', 
          () => p2paiService.nodes.getNodes(), 
          30 * 1000 // Cache for 30 seconds
        )
      ])
      
      if (projectsResult && projectsResult.data) {
        projects.value = projectsResult.data.map(project => ({
          id: project.id,
          name: project.name,
          description: project.description,
          type: project.project_type || 'general',
          status: project.status,
          progress: project.progress || 0,
          participantCount: project.participant_count || 0,
          currentRound: project.current_round || 0,
          totalRounds: project.total_rounds || 100,
          modelType: project.model_type || 'neural_network',
          privacyLevel: project.privacy_level || 'standard',
          created: formatDate(project.created_at),
          lastUpdate: formatRelativeTime(project.updated_at),
          metrics: {
            accuracy: project.accuracy || 0,
            precision: project.precision || 0,
            recall: project.recall || 0,
            f1Score: project.f1_score || 0
          },
          trainingData: project.training_data || {
            rounds: [],
            accuracy: [],
            loss: [],
            cpu: [],
            gpu: [],
            memory: []
          }
        }))
      }
      
      if (nodesResult && nodesResult.data) {
        participants.value = nodesResult.data.map(node => ({
          id: node.id,
          name: node.name,
          type: node.node_type || 'general',
          status: node.status,
          project: node.project_name || 'Unassigned',
          location: node.location || 'Unknown',
          dataSize: formatFileSize(node.data_size || 0),
          cpuUsage: node.cpu_usage || 0,
          memoryUsage: node.memory_usage || 0,
          networkLatency: node.network_latency || 0,
          contribution: node.contribution || 0,
          lastSeen: formatRelativeTime(node.last_seen),
          connections: node.connections || []
        }))
      }
      
      lastUpdate.value = new Date().toISOString()
      pageMonitor.end()
      
    } catch (error) {
      console.error('Failed to load P2PAI data:', error)
      connectionError.value = error.message || 'Failed to load data'
      pageMonitor.end()
    } finally {
      loading.value.projects = false
      loading.value.participants = false
    }
  }
  
  // Utility functions for data formatting
  const formatDate = (timestamp) => {
    if (!timestamp) return 'Unknown'
    return new Date(timestamp).toLocaleDateString()
  }
  
  const formatRelativeTime = (timestamp) => {
    if (!timestamp) return 'Unknown'
    
    const now = new Date()
    const date = new Date(timestamp)
    const diffMs = now - date
    const diffMinutes = Math.floor(diffMs / 60000)
    
    if (diffMinutes < 1) return 'just now'
    if (diffMinutes < 60) return `${diffMinutes} minutes ago`
    
    const diffHours = Math.floor(diffMinutes / 60)
    if (diffHours < 24) return `${diffHours} hours ago`
    
    const diffDays = Math.floor(diffHours / 24)
    return `${diffDays} days ago`
  }
  
  const formatFileSize = (bytes) => {
    if (!bytes || bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
  }

  const connectWebSocket = () => {
    // Disable WebSocket in development mode for demo purposes
    if (import.meta.env.MODE === 'development') {
      storeLogger.log('P2PAI WebSocket disabled in development mode')
      // Simulate connection for demo
      setTimeout(() => {
        isConnected.value = true
        connectionError.value = null
        storeLogger.log('P2PAI WebSocket simulated connection (demo mode)')
      }, 1000)
      return
    }

    if (ws.value) {
      ws.value.close()
    }

    try {
      ws.value = new WebSocket('ws://localhost:8000/p2pai/ws')
      
      ws.value.onopen = () => {
        isConnected.value = true
        connectionError.value = null
        connectionRetries.value = 0
        storeLogger.log('P2PAI WebSocket connected')
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
        console.error('P2PAI WebSocket error:', error)
      }
    } catch (error) {
      connectionError.value = 'Failed to establish WebSocket connection'
      console.error('WebSocket connection error:', error)
    }
  }

  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'participant_update':
        updateParticipant(data.payload)
        break
      case 'project_update':
        updateProject(data.payload)
        break
      case 'training_progress':
        if (data.payload && data.payload.project_id) {
          updateProjectProgress(data.payload)
        }
        break
      default:
        storeLogger.log('Unknown P2PAI WebSocket message type:', data.type, data)
    }
  }
  
  const updateProjectProgress = (progressData) => {
    const project = projects.value.find(p => p.id === progressData.project_id)
    if (project) {
      project.progress = progressData.progress || project.progress
      project.currentRound = progressData.current_round || project.currentRound
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

  const updateProject = (updatedProject) => {
    const index = projects.value.findIndex(p => p.id === updatedProject.id)
    if (index !== -1) {
      projects.value[index] = { ...projects.value[index], ...updatedProject }
    }
  }

  const updateParticipant = (updatedParticipant) => {
    const index = participants.value.findIndex(p => p.id === updatedParticipant.id)
    if (index !== -1) {
      participants.value[index] = { ...participants.value[index], ...updatedParticipant }
    }
  }

  const setCurrentProject = (project) => {
    currentProject.value = project
  }

  const setSelectedParticipant = (participant) => {
    selectedParticipant.value = participant
  }

  const refreshData = async () => {
    await loadRealData()
    return { success: true }
  }
  
  // Enhanced project management methods
  const createProject = async (projectData) => {
    loading.value.operations = true
    
    try {
      const result = await p2paiService.projects.createProject(projectData)
      
      if (result.success) {
        await loadRealData() // Refresh data after creation
        return { success: true, data: result.data }
      } else {
        throw new Error(result.error || 'Failed to create project')
      }
    } catch (error) {
      console.error('Failed to create project:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }
  
  const deleteProject = async (projectId) => {
    loading.value.operations = true
    
    try {
      const result = await p2paiService.projects.deleteProject(projectId)
      
      if (result.success) {
        projects.value = projects.value.filter(p => p.id !== projectId)
        return { success: true }
      } else {
        throw new Error(result.error || 'Failed to delete project')
      }
    } catch (error) {
      console.error('Failed to delete project:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }
  
  // Enhanced training management
  const startTraining = async (projectId, trainingConfig) => {
    loading.value.operations = true
    
    try {
      const result = await p2paiService.training.startTraining({
        project_id: projectId,
        ...trainingConfig
      })
      
      if (result.success) {
        // Update project status
        const project = projects.value.find(p => p.id === projectId)
        if (project) {
          project.status = 'training'
          project.lastUpdate = 'just now'
        }
        return { success: true, data: result.data }
      } else {
        throw new Error(result.error || 'Failed to start training')
      }
    } catch (error) {
      console.error('Failed to start training:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }
  
  const stopTraining = async (sessionId) => {
    loading.value.operations = true
    
    try {
      const result = await p2paiService.training.stopTraining(sessionId)
      
      if (result.success) {
        // Update project status based on session
        await loadRealData() // Refresh to get updated statuses
        return { success: true }
      } else {
        throw new Error(result.error || 'Failed to stop training')
      }
    } catch (error) {
      console.error('Failed to stop training:', error)
      return { success: false, error: error.message }
    } finally {
      loading.value.operations = false
    }
  }

  const cleanup = () => {
    disconnectWebSocket()
  }

  return {
    // State
    projects,
    participants,
    currentProject,
    selectedParticipant,
    isConnected,
    lastUpdate,
    connectionError,
    loading,
    config,
    
    // Computed
    activeProjects,
    onlineParticipants,
    trainingParticipants,
    errorParticipants,
    participantsByProject,
    systemStats,
    
    // Actions
    initializeStore,
    connectWebSocket,
    disconnectWebSocket,
    updateProject,
    updateProjectProgress,
    updateParticipant,
    setCurrentProject,
    setSelectedParticipant,
    refreshData,
    loadRealData,
    createProject,
    deleteProject,
    startTraining,
    stopTraining,
    cleanup
  }
})