<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <Button 
              @click="$router.back()" 
              variant="ghost" 
              size="sm" 
              class="mr-4"
            >
              ← Back
            </Button>
            <ServerStackIcon class="h-8 w-8 text-blue-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Cluster Management
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Cluster Management
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          Manage and monitor your EdgeAI clusters, create new clusters, and configure cluster settings
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600 dark:text-gray-400">Loading clusters data...</span>
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
              Failed to load clusters data
            </h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </div>
            <div class="mt-3">
              <Button @click="loadClustersData" variant="ghost" size="sm" class="text-red-800 dark:text-red-200 hover:bg-red-100 dark:hover:bg-red-800/30">
                Try again
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistics Cards -->
      <template v-else>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Clusters"
          :value="totalClusters"
          :icon="ServerStackIcon"
          variant="primary"
          description="Available clusters"
        />
        <StatCard
          title="Active Clusters"
          :value="activeClusters"
          :icon="PlayCircleIcon"
          variant="success"
          description="Currently running"
        />
        <StatCard
          title="Total Nodes"
          :value="totalNodes"
          :icon="ServerIcon"
          variant="info"
          description="Cluster nodes"
        />
        <StatCard
          title="Resources Used"
          :value="resourcesUsed"
          unit="%"
          :icon="CpuChipIcon"
          variant="warning"
          description="Cluster resource usage"
        />
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap gap-4 mb-8">
        <Button 
          @click="openCreateCluster"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium"
        >
          <PlusIcon class="w-5 h-5 mr-2" />
          Create New Cluster
        </Button>
        
        <Button 
          @click="refreshClusters"
          variant="secondary"
          class="px-6 py-3 rounded-lg font-medium"
          :loading="refreshing"
        >
          <ArrowPathIcon class="w-5 h-5 mr-2" />
          Refresh Clusters
        </Button>
        
      </div>

      <!-- Search and Filter -->
      <div class="flex flex-col sm:flex-row gap-4 mb-6">
        <div class="relative flex-1">
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search clusters..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        <select
          v-model="statusFilter"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">All Statuses</option>
          <option value="Active">Active</option>
          <option value="Inactive">Inactive</option>
          <option value="Error">Error</option>
          <option value="Maintenance">Maintenance</option>
        </select>
        
        <select
          v-model="typeFilter"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">All Types</option>
          <option value="Training">Training</option>
          <option value="Inference">Inference</option>
          <option value="Hybrid">Hybrid</option>
        </select>
      </div>

      <!-- Clusters Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="cluster in filteredClusters" 
          :key="cluster.id"
          @click="openClusterDetails(cluster)"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 cursor-pointer hover:shadow-lg transition-all duration-200"
        >
          <!-- Status Indicator and Title -->
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center">
              <div 
                :class="getStatusDotColor(cluster.status)"
                class="w-3 h-3 rounded-full mr-3"
              ></div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ cluster.name }}
              </h3>
            </div>
            <span :class="getTypeBadgeColor(cluster.type)" class="px-2 py-1 rounded-full text-xs font-medium">
              {{ cluster.type }}
            </span>
          </div>
          
          <!-- Description -->
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
            {{ cluster.description }}
          </p>

          <!-- Cluster Information -->
          <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 mb-4">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-medium text-gray-600 dark:text-gray-400">CLUSTER INFO</span>
              <span :class="getStatusBadgeColor(cluster.status)" class="px-2 py-1 rounded-full text-xs font-medium">
                {{ cluster.status }}
              </span>
            </div>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="text-gray-600 dark:text-gray-400">
                Nodes: <span class="font-medium text-gray-900 dark:text-white">{{ cluster.nodeCount }}</span>
              </div>
              <div class="text-gray-600 dark:text-gray-400">
                CPU: <span class="font-medium text-gray-900 dark:text-white">{{ cluster.cpuCores }} cores</span>
              </div>
              <div class="text-gray-600 dark:text-gray-400">
                Memory: <span class="font-medium text-gray-900 dark:text-white">{{ cluster.memory }}GB</span>
              </div>
              <div class="text-gray-600 dark:text-gray-400">
                GPU: <span class="font-medium text-gray-900 dark:text-white">{{ cluster.gpuCount }}</span>
              </div>
            </div>
          </div>

          <!-- Performance Metrics -->
          <div v-if="cluster.metrics" class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3 mb-4">
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
                  {{ (cluster.metrics.cpuUsage || 0).toFixed(1) }}%
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400">CPU</div>
              </div>
              <div class="text-center">
                <div class="text-lg font-bold text-green-600 dark:text-green-400">
                  {{ (cluster.metrics.memoryUsage || 0).toFixed(1) }}%
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400">Memory</div>
              </div>
              <div class="text-center">
                <div class="text-lg font-bold text-purple-600 dark:text-purple-400">
                  {{ (cluster.metrics.gpuUsage || 0).toFixed(1) }}%
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400">GPU</div>
              </div>
            </div>
          </div>

          <!-- Active Projects -->
          <div v-if="cluster.activeProjects > 0" class="bg-green-50 dark:bg-green-900/20 rounded-lg p-3 mb-4">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-medium text-green-600 dark:text-green-400">ACTIVE PROJECTS</span>
              <span class="text-xs text-green-600 dark:text-green-400">{{ cluster.activeProjects }} running</span>
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              {{ cluster.activeProjectNames?.join(', ') || 'Multiple projects running' }}
            </div>
          </div>

          <!-- Timestamps -->
          <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-200 dark:border-gray-600">
            <span>Created: {{ cluster.created }}</span>
            <span>Updated: {{ cluster.lastUpdated }}</span>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredClusters.length === 0 && !loading" class="text-center py-12">
        <ServerStackIcon class="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No clusters found</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          {{ searchQuery || statusFilter || typeFilter ? 'No clusters match your current filters.' : 'Get started by creating your first cluster.' }}
        </p>
        <Button 
          @click="openCreateCluster"
          class="bg-blue-600 hover:bg-blue-700 text-white"
        >
          <PlusIcon class="w-5 h-5 mr-2" />
          Create New Cluster
        </Button>
      </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApiOptimization } from '@/composables/useApiOptimization'
import { useNotifications } from '@/composables/useNotifications'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import StatCard from '@/components/ui/StatCard.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import {
  ServerStackIcon,
  ServerIcon,
  CpuChipIcon,
  PlusIcon,
  ArrowPathIcon,
  MagnifyingGlassIcon,
  PlayCircleIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const { error: showError } = useNotifications()
const { cachedApiCall, clearCache } = useApiOptimization()

// Reactive data
const searchQuery = ref('')
const statusFilter = ref('')
const typeFilter = ref('')
const loading = ref(false)
const refreshing = ref(false)
const error = ref(null)
const refreshInterval = ref(null)

// Statistics (will be loaded from API)
const totalClusters = ref(0)
const activeClusters = ref(0)
const totalNodes = ref(0)
const resourcesUsed = ref(0)

// Clusters data (will be loaded from API)
const clusters = ref([])

// Computed properties
const filteredClusters = computed(() => {
  // 防御性检查：确保 clusters.value 是数组
  if (!clusters.value || !Array.isArray(clusters.value)) {
    return []
  }

  let filtered = clusters.value

  // Filter by search query
  if (searchQuery.value) {
    filtered = filtered.filter(cluster =>
      cluster.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      cluster.description?.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Filter by status
  if (statusFilter.value) {
    filtered = filtered.filter(cluster => cluster.status === statusFilter.value)
  }

  // Filter by type
  if (typeFilter.value) {
    filtered = filtered.filter(cluster => cluster.type === typeFilter.value)
  }

  return filtered
})

// Utility functions
const getStatusDotColor = (status) => {
  const colors = {
    Active: 'bg-green-500',
    Inactive: 'bg-gray-500',
    Error: 'bg-red-500',
    Maintenance: 'bg-yellow-500'
  }
  return colors[status] || 'bg-gray-500'
}

const getStatusBadgeColor = (status) => {
  const colors = {
    Active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    Inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    Error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    Maintenance: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
  }
  return colors[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

const getTypeBadgeColor = (type) => {
  const colors = {
    Training: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    Inference: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    Hybrid: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
  }
  return colors[type] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

// Load clusters data from API
const loadClustersData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('EdgeAIClusterManagement')
  loading.value = true
  error.value = null
  
  console.log('🔄 Loading clusters data...')
  
  try {
    // Load clusters data
    const clustersResult = await cachedApiCall('edgeai-clusters', 
      () => edgeaiService.clusters.getClusters(), 
      2 * 60 * 1000 // Cache for 2 minutes
    )
    
    console.log('📊 Clusters result:', clustersResult)

    // Update clusters data
    if (clustersResult && Array.isArray(clustersResult)) {
      console.log(`✅ Processing ${clustersResult.length} clusters`)
      clusters.value = clustersResult.map(cluster => {
        console.log('🔍 Processing cluster:', cluster)
        const mappedCluster = {
          id: cluster.id,
          name: cluster.name,
          description: cluster.description || 'No description available',
          type: cluster.type || 'Hybrid',
          status: cluster.status || 'Active', // Default to Active since we have clusters
          nodeCount: cluster.node_count || 0,
          cpuCores: cluster.cpu_cores || 0,
          memory: cluster.memory || 0,
          gpuCount: cluster.gpu_count || 0,
          activeProjects: cluster.active_projects || 0,
          activeProjectNames: cluster.active_project_names || [],
          metrics: cluster.metrics || null,
          created: cluster.created_time ? new Date(cluster.created_time).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
          lastUpdated: cluster.last_updated_time ? new Date(cluster.last_updated_time).toISOString().split('T')[0] : new Date().toISOString().split('T')[0]
        }
        console.log('📋 Mapped cluster:', mappedCluster)
        return mappedCluster
      })
      console.log('📋 All mapped clusters:', clusters.value)
    } else {
      console.log('⚠️ No clusters data received, using empty array')
      // If no data from API, use empty array (this will show empty state with create button)
      clusters.value = []
    }

    // Update statistics based on clusters data (with defensive checks)
    totalClusters.value = clusters.value?.length || 0
    activeClusters.value = clusters.value?.filter(c => c.status === 'Active').length || 0
    totalNodes.value = clusters.value?.reduce((sum, c) => sum + (c.nodeCount || 0), 0) || 0
    resourcesUsed.value = 0 // Default to 0 since we don't have resource usage data

    console.log('📈 Statistics updated:', {
      totalClusters: totalClusters.value,
      activeClusters: activeClusters.value,
      totalNodes: totalNodes.value,
      resourcesUsed: resourcesUsed.value
    })

    pageMonitor.end({ success: true, clusterCount: clusters.value.length })
  } catch (err) {
    console.error('Failed to load clusters data:', err)
    // Don't set error state, just use empty data so buttons are still visible
    console.log('Using empty cluster data due to API error')
    clusters.value = []
    totalClusters.value = 0
    activeClusters.value = 0
    totalNodes.value = 0
    resourcesUsed.value = 0
    // Don't set error.value to show error state, keep it null
    pageMonitor.end({ success: false, error: err.message })
  } finally {
    loading.value = false
  }
}

// Setup auto-refresh
const setupAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }

  refreshInterval.value = setInterval(async () => {
    if (!loading.value) {
      await loadClustersData()
    }
  }, 30 * 1000) // Refresh every 30 seconds
}

// Manual refresh
const refreshClusters = async () => {
  refreshing.value = true
  clearCache('edgeai-clusters')
  await loadClustersData()
  refreshing.value = false
}

// Navigation functions
const openCreateCluster = () => {
  router.push('/edgeai/create-cluster')
}

const openClusterDetails = (cluster) => {
  console.log('View cluster details:', cluster)
  
  // Validate cluster ID before navigation
  if (!cluster.id || cluster.id === 'undefined' || cluster.id === undefined) {
    console.error('❌ Invalid cluster ID:', cluster.id)
    showError('Invalid cluster ID. Please refresh the page and try again.')
    return
  }
  
  console.log('✅ Navigating to cluster details with ID:', cluster.id)
  router.push(`/edgeai/cluster-details/${cluster.id}`)
}


// Component lifecycle
onMounted(async () => {
  await loadClustersData()
  setupAutoRefresh()
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  clearCache()
})
</script>
