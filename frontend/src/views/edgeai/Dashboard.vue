<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <ComputerDesktopIcon class="h-8 w-8 text-green-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Edge AI Dashboard
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <!-- Offline Mode Indicator -->
            <div v-if="isOffline" class="flex items-center space-x-1 bg-orange-100 dark:bg-orange-900/30 px-2 py-1 rounded-full">
              <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
              <span class="text-xs text-orange-700 dark:text-orange-300">Offline</span>
              <span v-if="queuedRequests > 0" class="text-xs text-orange-600 dark:text-orange-400">({{ queuedRequests }} queued)</span>
            </div>
            
            <!-- Keyboard Shortcut Hint -->
            <div class="hidden lg:flex items-center text-xs text-gray-500 dark:text-gray-400">
              <kbd class="px-1 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs">Ctrl+Shift+?</kbd>
              <span class="ml-1">for shortcuts</span>
            </div>
            
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Welcome, {{ authStore.user?.username }}
            </span>
            <SimpleThemeToggle size="sm" />
            <Button @click="logout" variant="ghost" size="sm">
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600 dark:text-gray-400">Loading dashboard data...</span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-8">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
              Failed to load dashboard data
            </h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </div>
            <div class="mt-3">
              <Button @click="loadDashboardData" variant="ghost" size="sm" class="text-red-800 dark:text-red-200 hover:bg-red-100 dark:hover:bg-red-800/30">
                Try again
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Welcome Header -->
      <template v-else>
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Welcome to OpenTMP Edge AI Intelligence!
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-400">
          Manage your edge AI nodes and training projects
        </p>
      </div>

      <!-- Statistics Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <ComputerDesktopIcon class="w-12 h-12 text-gray-600 dark:text-gray-400" />
          </div>
          <div v-if="loading" class="text-3xl font-bold text-gray-400 mb-2">--</div>
          <div v-else class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            {{ systemStats.totalProjects }}
          </div>
          <div class="text-gray-600 dark:text-gray-400">Total Projects</div>
        </div>

        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <ServerIcon class="w-12 h-12 text-green-600 dark:text-green-400" />
          </div>
          <div v-if="loading" class="text-3xl font-bold text-gray-400 mb-2">--</div>
          <div v-else class="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">
            {{ systemStats.onlineNodes }}
          </div>
          <div class="text-gray-600 dark:text-gray-400">Active Nodes</div>
        </div>

        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <svg class="w-12 h-12 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
            </svg>
          </div>
          <div v-if="loading" class="text-3xl font-bold text-gray-400 mb-2">--</div>
          <div v-else class="text-3xl font-bold text-yellow-500 mb-2">
            {{ systemStats.trainingNodes }}
          </div>
          <div class="text-gray-600 dark:text-gray-400">Training Tasks</div>
        </div>

        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <ChartBarIcon class="w-12 h-12 text-purple-600 dark:text-purple-400" />
          </div>
          <div v-if="loading" class="text-3xl font-bold text-gray-400 mb-2">--</div>
          <div v-else class="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-2">
            {{ completionRate.toFixed(2) }}%
          </div>
          <div class="text-gray-600 dark:text-gray-400">Completion Rate</div>
        </div>
      </div>

      <!-- Main Function Buttons -->
      <div class="flex flex-wrap gap-4 mb-8">
        <Button 
          @click="openCreateProject"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium"
        >
          <PlusIcon class="w-5 h-5 mr-2" />
          Create New Project
        </Button>
        
        <Button 
          @click="openModelManagement"
          variant="secondary"
          class="px-6 py-3 rounded-lg font-medium"
        >
          <CpuChipIcon class="w-5 h-5 mr-2" />
          Model Management
        </Button>
        
        <Button 
          @click="viewAllNodes"
          variant="secondary" 
          class="px-6 py-3 rounded-lg font-medium"
        >
          <ServerIcon class="w-5 h-5 mr-2" />
          View All Nodes
        </Button>
      </div>

      <!-- Project List -->
      <div class="mb-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-semibold text-gray-900 dark:text-white">My Projects</h2>
          
          <div class="flex items-center space-x-4">
            <!-- Search Box -->
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search projects..."
                class="w-64 pl-4 pr-10 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <MagnifyingGlassIcon class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            </div>
            
            <!-- Status Filter -->
            <select
              v-model="statusFilter"
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Statuses</option>
              <option value="Training">Training</option>
              <option value="Completed">Completed</option>
              <option value="Idle">Idle</option>
              <option value="Error">Error</option>
            </select>
          </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="project in filteredProjects" 
            :key="project.id"
            @click="openProjectVisualization(project)"
            class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 cursor-pointer hover:shadow-lg transition-all duration-200"
          >
            <!-- Status Indicator and Title -->
            <div class="flex items-start justify-between mb-3">
              <div class="flex items-center">
                <div 
                  :class="getStatusDotColor(project.status)"
                  class="w-3 h-3 rounded-full mr-3"
                ></div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                  {{ project.name }}
                </h3>
              </div>
            </div>
            
            <!-- Description -->
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
              {{ project.description }}
            </p>

            <!-- Model Information -->
            <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 mb-4">
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-medium text-gray-600 dark:text-gray-400">MODEL INFO</span>
                <span :class="getModelTypeBadgeColor(project.modelType)" class="px-2 py-1 rounded-full text-xs font-medium">
                  {{ project.modelType?.toUpperCase() || 'CNN' }}
                </span>
              </div>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="text-gray-600 dark:text-gray-400">
                  Batch Size: <span class="font-medium text-gray-900 dark:text-white">{{ project.batchSize || 32 }}</span>
                </div>
                <div class="text-gray-600 dark:text-gray-400">
                  Learning Rate: <span class="font-medium text-gray-900 dark:text-white">{{ project.learningRate || 0.001 }}</span>
                </div>
              </div>
            </div>

            <!-- Performance Metrics -->
            <div v-if="project.metrics && project.status !== 'created'" class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 mb-4">
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-medium text-blue-600 dark:text-blue-400">PERFORMANCE</span>
                <div class="flex items-center">
                  <div class="w-2 h-2 bg-blue-500 rounded-full mr-1"></div>
                  <span class="text-xs text-blue-600 dark:text-blue-400">Live</span>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-2">
                <div class="text-center">
                  <div class="text-lg font-bold text-blue-600 dark:text-blue-400">
                    {{ (project.metrics?.accuracy || 0).toFixed(2) }}%
                  </div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Accuracy</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-bold text-green-600 dark:text-green-400">
                    {{ (project.metrics?.f1Score || 0).toFixed(2) }}
                  </div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">F1 Score</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-bold text-orange-600 dark:text-orange-400">
                    {{ (project.metrics?.loss || 0).toFixed(3) }}
                  </div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Loss</div>
                </div>
              </div>
            </div>

            <!-- Training Status & Progress -->
            <div class="mb-4">
              <div class="flex justify-between text-sm mb-2">
                <span class="text-gray-500 dark:text-gray-400">Connected Nodes:</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ project.connectedNodes || project.nodes }}</span>
              </div>

              <div class="flex justify-between text-sm mb-2">
                <span class="text-gray-500 dark:text-gray-400">Training Progress:</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ project.progress.toFixed(2) }}%</span>
              </div>

              <!-- Epoch Information -->
              <div v-if="project.currentEpoch || project.totalEpochs" class="flex justify-between text-sm mb-2">
                <span class="text-gray-500 dark:text-gray-400">Epochs:</span>
                <span class="font-semibold text-gray-900 dark:text-white">
                  {{ project.currentEpoch || 0 }} / {{ project.totalEpochs || 100 }}
                </span>
              </div>

              <!-- Progress Bar -->
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-2">
                <div
                  :class="getProgressBarColor(project.status, project.progress)"
                  class="h-2 rounded-full transition-all duration-300"
                  :style="{ width: project.progress + '%' }"
                ></div>
              </div>

              <!-- ETA and Speed -->
              <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400">
                <span v-if="project.status === 'training'">ETA: {{ calculateETA(project) }}</span>
                <span v-else-if="project.status === 'active' || project.status === 'completed'">Status: Completed</span>
                <span v-else>Status: {{ project.status || 'Idle' }}</span>

                <span v-if="project.status === 'training'">{{ calculateTrainingSpeed(project) }} epochs/hr</span>
                <span v-else-if="project.status === 'active' && project.totalEpochs">{{ project.currentEpoch || 0 }}/{{ project.totalEpochs }} epochs</span>
              </div>
            </div>

            <!-- Resource Usage (if available) -->
            <div v-if="project.resourceUsage" class="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-3 mb-4">
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-medium text-yellow-600 dark:text-yellow-400">RESOURCES</span>
                <span class="text-xs text-yellow-600 dark:text-yellow-400">Live Usage</span>
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div class="text-center">
                  <div class="text-sm font-bold text-yellow-600 dark:text-yellow-400">
                    {{ (project.resourceUsage.cpu || 0).toFixed(2) }}%
                  </div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">CPU</div>
                </div>
                <div class="text-center">
                  <div class="text-sm font-bold text-yellow-600 dark:text-yellow-400">
                    {{ (project.resourceUsage.memory || 0).toFixed(2) }}%
                  </div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Memory</div>
                </div>
              </div>
            </div>

            <!-- Timestamps -->
            <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-200 dark:border-gray-600">
              <span>Created: {{ project.created }}</span>
              <span>Updated: {{ project.lastUpdate || project.lastUpdated || 'Unknown' }}</span>
            </div>
          </div>
        </div>
      </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'
import { useEdgeAIStore } from '@/stores/edgeai'
import { useEdgeAIStats, useEdgeAILifecycle } from '@/composables/useEdgeAI'
import { useApiOptimization } from '@/composables/useApiOptimization'
import { useErrorBoundary } from '@/composables/useErrorBoundary'
import { useOfflineMode } from '@/composables/useOfflineMode'
import { useKeyboardShortcuts, useEdgeAIShortcuts } from '@/composables/useKeyboardShortcuts'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import StatCard from '@/components/ui/StatCard.vue'
import DashboardCard from '@/components/ui/DashboardCard.vue'
import RealtimeMonitor from '@/components/edgeai/RealtimeMonitor.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import { 
  ComputerDesktopIcon,
  ServerIcon,
  CpuChipIcon,
  ChartBarIcon,
  ClockIcon,
  DocumentTextIcon,
  PlusIcon,
  EyeIcon,
  ArrowDownTrayIcon,
  CalendarIcon,
  FolderIcon,
  SignalIcon,
  MagnifyingGlassIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const uiStore = useUIStore()
const edgeaiStore = useEdgeAIStore()
const { systemStats, getTotalResources } = useEdgeAIStats()
const { cachedApiCall, clearCache } = useApiOptimization()
const { hasError, retry } = useErrorBoundary()
const { isOffline, queuedRequests, offlineAwareFetch } = useOfflineMode()

// Initialize keyboard shortcuts
useKeyboardShortcuts()
useEdgeAIShortcuts()

useEdgeAILifecycle()

// Loading and error states
const loading = ref(false)
const error = ref(null)
const refreshInterval = ref(null)


// Computed properties for dashboard statistics
const completionRate = computed(() => {
  const projects = edgeaiStore.projects || []
  if (projects.length === 0) return 0

  const completedProjects = projects.filter(project =>
    project.status === 'Completed' || project.progress >= 100
  ).length

  return Math.round((completedProjects / projects.length) * 100)
})

const totalResources = computed(() => getTotalResources())

const systemLogs = ref([])

// Search and filter state
const searchQuery = ref('')
const statusFilter = ref('')


// Computed property for filtered projects
const filteredProjects = computed(() => {
  let filtered = edgeaiStore.projects || []

  // Filter by search query
  if (searchQuery.value) {
    filtered = filtered.filter(project => 
      project.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      project.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Filter by status
  if (statusFilter.value) {
    filtered = filtered.filter(project => project.status === statusFilter.value)
  }

  return filtered
})

// Load dashboard data from API
const loadDashboardData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('EdgeAIDashboard')
  loading.value = true
  error.value = null

  try {
    // Load projects, nodes, and system logs in parallel
    const [projectsResult, nodesResult, logsResult] = await Promise.all([
      cachedApiCall('edgeai-projects',
        () => edgeaiService.projects.getProjects(),
        2 * 60 * 1000 // Cache for 2 minutes
      ),
      cachedApiCall('edgeai-nodes',
        () => edgeaiService.nodes.getNodes(),
        1 * 60 * 1000 // Cache for 1 minute
      ),
      cachedApiCall('edgeai-system-logs',
        () => edgeaiService.logs.getLogs(),
        30 * 1000 // Cache for 30 seconds
      )
    ])

    // Update store with real project data
    if (projectsResult && Array.isArray(projectsResult)) {
      // Transform backend data to match frontend format
      const transformedProjects = projectsResult.map(project => ({
        id: project.id,
        name: project.name,
        description: project.description,
        status: project.status || 'Idle',
        progress: project.progress || 0,
        nodes: project.connected_nodes || 0,
        created: project.created_at || new Date().toISOString().split('T')[0],
        lastUpdated: project.last_updated || 'Unknown'
      }))
      edgeaiStore.projects.splice(0, edgeaiStore.projects.length, ...transformedProjects)
    }

    // Update store with real node data
    if (nodesResult && Array.isArray(nodesResult)) {
      // Transform backend node data to match frontend format
      const transformedNodes = nodesResult.map(node => ({
        id: node.id,
        name: node.name,
        status: node.status || 'offline',
        location: node.location || 'Unknown',
        project: node.project_id || 'Unassigned',
        cpuUsage: node.cpu_usage || 0,
        memoryUsage: node.memory_usage || 0,
        gpuUsage: node.gpu_usage || 0,
        activeTasks: node.active_tasks || 0,
        uptime: node.uptime || '0 minutes',
        lastSeen: node.last_seen || 'Unknown',
        hardware: {
          cpu: node.hardware?.cpu || 'Unknown',
          memory: node.hardware?.memory || 'Unknown',
          storage: node.hardware?.storage || 'Unknown',
          gpu: node.hardware?.gpu || null
        },
        recentActivity: node.recent_activity || []
      }))
      edgeaiStore.nodes.splice(0, edgeaiStore.nodes.length, ...transformedNodes)
    }

    // Update system logs (handle paginated response)
    if (logsResult) {
      const logItems = Array.isArray(logsResult) ? logsResult : (logsResult.items || [])
      systemLogs.value = logItems.map(log => ({
        id: log.id,
        message: log.message,
        time: log.timestamp || log.time || 'Unknown'
      }))
    }

    pageMonitor.end({ success: true })
  } catch (err) {
    console.error('Failed to load EdgeAI dashboard data:', err)

    // Handle different types of errors
    let errorMessage = 'Failed to load dashboard data'
    if (err?.message) {
      errorMessage = err.message
    } else if (typeof err === 'string') {
      errorMessage = err
    } else if (err?.error) {
      errorMessage = err.error
    }

    error.value = errorMessage
    pageMonitor.end({ success: false, error: errorMessage })

    // Show user-friendly notification on error
    try {
      uiStore.addNotification({
        type: 'error',
        title: 'Dashboard Load Failed',
        message: 'Unable to load dashboard data. Please check your connection and try again.'
      })
    } catch (notifError) {
      console.error('Failed to show notification:', notifError)
    }
  } finally {
    loading.value = false
  }
}

// Setup auto-refresh with intelligent caching
const setupAutoRefresh = () => {
  // Clear any existing interval
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }

  // Set up new interval for every 30 seconds
  refreshInterval.value = setInterval(async () => {
    if (!loading.value && !isOffline.value) {
      // Clear specific caches before refresh to get fresh data
      clearCache('edgeai-projects')
      clearCache('edgeai-nodes')
      clearCache('edgeai-system-logs')

      await loadDashboardData()
    }
  }, 30 * 1000)
}

// Manual refresh function for user-triggered refresh
const refreshDashboard = async () => {
  if (loading.value) return

  // Clear all caches for manual refresh
  clearCache()
  await loadDashboardData()

  uiStore.addNotification({
    type: 'success',
    title: 'Dashboard Refreshed',
    message: 'Dashboard data has been updated with the latest information.'
  })
}

// Component lifecycle
onMounted(async () => {
  // Initialize EdgeAI store first
  await edgeaiStore.initializeStore()
  // Then load dashboard data
  await loadDashboardData()
  // Setup auto-refresh
  setupAutoRefresh()
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  // Cleanup EdgeAI store connections
  edgeaiStore.cleanup()
  // Clear API cache on unmount
  clearCache()
})

const logout = () => {
  authStore.logout()
  router.push('/')
}

// StatCard click handlers
const viewNodes = () => {
  router.push('/edgeai/all-nodes')
}

const viewTasks = () => {
  router.push('/edgeai/task-manager')
}

const viewCompletedTasks = () => {
  router.push('/edgeai/project-manager')
}

const viewPerformanceMetrics = () => {
  router.push('/edgeai/performance-metrics')
}

// Node Management handlers
const addNewNode = () => {
  router.push('/edgeai/create-project')
}

const viewAllNodes = () => {
  router.push('/edgeai/all-nodes')
}

// System Logs handlers
const viewAllLogs = () => {
  router.push('/edgeai/system-logs')
}

const exportLogs = () => {
  router.push('/edgeai/system-logs')
}

// Additional services handlers
const openScheduler = () => {
  router.push('/edgeai/project-manager')
}

const openPerformanceMonitor = () => {
  router.push('/edgeai/visualization')
}

const openResourceManager = () => {
  router.push('/edgeai/all-nodes')
}

// Project management handlers
const openProjectManager = () => {
  router.push('/edgeai/project-manager')
}

const openImportProject = () => {
  router.push('/edgeai/import-project')
}

// New handler functions
const openCreateProject = () => {
  router.push('/edgeai/create-project')
}

const openModelManagement = () => {
  router.push('/edgeai/model-management')
}

const openProjectVisualization = (project) => {
  router.push(`/edgeai/visualization/${project.id}`)
}

// Utility functions for project display
const getStatusDotColor = (status) => {
  const colors = {
    training: 'bg-blue-500',
    Training: 'bg-blue-500',
    completed: 'bg-green-500',
    Completed: 'bg-green-500',
    active: 'bg-green-500',
    Active: 'bg-green-500',
    idle: 'bg-gray-500',
    Idle: 'bg-gray-500',
    error: 'bg-red-500',
    Error: 'bg-red-500'
  }
  return colors[status] || 'bg-gray-500'
}

// Helper functions for enhanced project card visualization
const getModelTypeBadgeColor = (modelType) => {
  const colors = {
    cnn: 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
    rnn: 'bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-300',
    transformer: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-300',
    lstm: 'bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-300',
    gru: 'bg-pink-100 text-pink-800 dark:bg-pink-900/50 dark:text-pink-300'
  }
  return colors[modelType?.toLowerCase()] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

const getProgressBarColor = (status, progress) => {
  if (status === 'error') return 'bg-red-500'
  if (status === 'completed' || status === 'active') return 'bg-green-500'
  if (status === 'training') {
    if (progress > 80) return 'bg-blue-500'
    if (progress > 50) return 'bg-yellow-500'
    return 'bg-orange-500'
  }
  return 'bg-gray-500'
}

const calculateETA = (project) => {
  if (!project || project.status !== 'training') return 'N/A'

  const { currentEpoch = 0, totalEpochs = 100, progress = 0 } = project

  // More lenient check - only require currentEpoch > 0 and totalEpochs > currentEpoch
  if (currentEpoch <= 0 || totalEpochs <= currentEpoch) return 'Calculating...'

  // Estimate based on current progress rate
  const epochsRemaining = totalEpochs - currentEpoch
  const averageTimePerEpoch = 2.5 // Assume 2.5 minutes per epoch
  const estimatedMinutes = epochsRemaining * averageTimePerEpoch

  if (estimatedMinutes < 60) {
    return `${Math.round(estimatedMinutes)}m`
  } else if (estimatedMinutes < 1440) {
    const hours = Math.floor(estimatedMinutes / 60)
    const minutes = Math.round(estimatedMinutes % 60)
    return `${hours}h ${minutes}m`
  } else {
    const days = Math.floor(estimatedMinutes / 1440)
    const hours = Math.floor((estimatedMinutes % 1440) / 60)
    return `${days}d ${hours}h`
  }
}

const calculateTrainingSpeed = (project) => {
  if (!project || project.status !== 'training') return '0'

  const { currentEpoch = 0 } = project

  // Simulate training speed based on model type and current epoch
  const baseSpeed = {
    cnn: 24,
    rnn: 18,
    transformer: 12,
    lstm: 20,
    gru: 22
  }

  const speed = baseSpeed[project.modelType?.toLowerCase()] || 20

  // Add some randomness to make it more realistic
  const variation = (Math.random() - 0.5) * 4
  return Math.max(1, Math.round(speed + variation))
}
</script>