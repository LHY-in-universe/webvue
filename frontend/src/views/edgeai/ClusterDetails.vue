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
            <div>
              <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                {{ cluster?.name || 'Cluster Details' }}
              </h1>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Cluster ID: {{ clusterId }}
              </p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600 dark:text-gray-400">Loading cluster details...</span>
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
              Failed to load cluster details
            </h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </div>
            <div class="mt-3">
              <Button @click="loadClusterDetails" variant="ghost" size="sm" class="text-red-800 dark:text-red-200 hover:bg-red-100 dark:hover:bg-red-800/30">
                Try again
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Cluster Details -->
      <template v-else-if="cluster">
        <!-- Header Section -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-8">
          <div class="flex items-start justify-between mb-6">
            <div class="flex items-center">
              <div 
                :class="getStatusDotColor(cluster.status)"
                class="w-4 h-4 rounded-full mr-4"
              ></div>
              <div>
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
                  {{ cluster.name }}
                </h1>
                <p class="text-gray-600 dark:text-gray-400 mt-1">
                  {{ cluster.description || 'No description available' }}
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <span :class="getStatusBadgeColor(cluster.status)" class="px-3 py-1 rounded-full text-sm font-medium">
                {{ cluster.status }}
              </span>
              <span :class="getTypeBadgeColor(cluster.type)" class="px-3 py-1 rounded-full text-sm font-medium">
                {{ cluster.type }}
              </span>
            </div>
          </div>

          <!-- Delete Cluster Button -->
          <div class="flex justify-end mt-6">
            <Button 
              @click="deleteCluster"
              :loading="deleting"
              variant="outline"
              class="border-red-300 text-red-700 hover:bg-red-50 dark:border-red-700 dark:text-red-400 dark:hover:bg-red-900/20"
            >
              <TrashIcon class="w-4 h-4 mr-2" />
              Delete Cluster
            </Button>
          </div>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Nodes"
            :value="cluster.nodeCount || 0"
            :icon="ServerIcon"
            variant="primary"
            description="Cluster nodes"
          />
          <StatCard
            title="CPU Cores"
            :value="cluster.cpuCores || 0"
            :icon="CpuChipIcon"
            variant="info"
            description="Total CPU cores"
          />
          <StatCard
            title="Memory"
            :value="cluster.memory || 0"
            unit="GB"
            :icon="MemoryIcon"
            variant="warning"
            description="Total memory"
          />
          <StatCard
            title="GPU Count"
            :value="cluster.gpuCount || 0"
            :icon="CpuChipIcon"
            variant="success"
            description="GPU devices"
          />
        </div>

        <!-- Main Content -->
        <div class="space-y-8">
            <!-- Cluster Information -->
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Cluster Information</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Cluster ID</label>
                  <p class="text-gray-900 dark:text-white font-mono text-sm">{{ cluster.id }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Type</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.type }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Status</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.status }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Created</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.created }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Last Updated</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.lastUpdated }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Projects</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.activeProjects || 0 }}</p>
                </div>
              </div>
            </div>

            <!-- Performance Metrics -->
            <div v-if="cluster.metrics" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Performance Metrics</h2>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="text-center">
                  <div class="text-3xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                    {{ (cluster.metrics.cpuUsage || 0).toFixed(1) }}%
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">CPU Usage</div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-2">
                    <div 
                      class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${cluster.metrics.cpuUsage || 0}%` }"
                    ></div>
                  </div>
                </div>
                <div class="text-center">
                  <div class="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">
                    {{ (cluster.metrics.memoryUsage || 0).toFixed(1) }}%
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">Memory Usage</div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-2">
                    <div 
                      class="bg-green-600 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${cluster.metrics.memoryUsage || 0}%` }"
                    ></div>
                  </div>
                </div>
                <div class="text-center">
                  <div class="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-2">
                    {{ (cluster.metrics.gpuUsage || 0).toFixed(1) }}%
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">GPU Usage</div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-2">
                    <div 
                      class="bg-purple-600 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${cluster.metrics.gpuUsage || 0}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Cluster Nodes Section - DISABLED -->
            <!-- 
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Cluster Nodes</h2>
                <Button 
                  @click="refreshNodes"
                  variant="ghost"
                  size="sm"
                  :loading="nodesLoading"
                >
                  <ArrowPathIcon class="w-4 h-4 mr-2" />
                  Refresh
                </Button>
              </div>
              
              <div v-if="nodesLoading" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
              
              <div v-else-if="clusterNodes.length === 0" class="text-center py-8">
                <ServerIcon class="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No nodes found</h3>
                <p class="text-gray-600 dark:text-gray-400 mb-4">This cluster doesn't have any nodes yet.</p>
                <Button @click="addNode" class="bg-blue-600 hover:bg-blue-700 text-white">
                  <PlusIcon class="w-4 h-4 mr-2" />
                  Add Node
                </Button>
              </div>
              
              <div v-else class="space-y-4">
                <div 
                  v-for="node in clusterNodes" 
                  :key="node.id"
                  class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
                >
                  <div class="flex items-center">
                    <div 
                      :class="getNodeStatusColor(node.status)"
                      class="w-3 h-3 rounded-full mr-3"
                    ></div>
                    <div>
                      <h3 class="font-medium text-gray-900 dark:text-white">{{ node.name }}</h3>
                      <p class="text-sm text-gray-600 dark:text-gray-400">{{ node.type }} • {{ node.status }}</p>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <Button 
                      @click="viewNodeDetails(node)"
                      variant="ghost"
                      size="sm"
                    >
                      View Details
                    </Button>
                    <Button 
                      @click="removeNode(node)"
                      variant="ghost"
                      size="sm"
                      class="text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20"
                    >
                      Remove
                    </Button>
                  </div>
                </div>
              </div>
            </div>
            -->
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApiOptimization } from '@/composables/useApiOptimization'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import StatCard from '@/components/ui/StatCard.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import {
  ServerStackIcon,
  ServerIcon,
  CpuChipIcon,
  // ArrowPathIcon, // DISABLED - no longer needed
  // PlusIcon, // DISABLED - no longer needed
  TrashIcon
} from '@heroicons/vue/24/outline'

// Memory icon (using CpuChipIcon as fallback)
const MemoryIcon = CpuChipIcon

const route = useRoute()
const router = useRouter()
const { cachedApiCall, clearCache } = useApiOptimization()

// Get cluster ID from route params
const clusterId = computed(() => route.params.id)

// Reactive data
const loading = ref(false)
// const nodesLoading = ref(false) // DISABLED
const deleting = ref(false)
const error = ref(null)
const cluster = ref(null)
// const clusterNodes = ref([]) // DISABLED
const refreshInterval = ref(null)


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

// Node status color function - DISABLED
/*
const getNodeStatusColor = (status) => {
  const colors = {
    Active: 'bg-green-500',
    Inactive: 'bg-gray-500',
    Error: 'bg-red-500',
    Maintenance: 'bg-yellow-500'
  }
  return colors[status] || 'bg-gray-500'
}
*/


// Load cluster details
const loadClusterDetails = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('EdgeAIClusterDetails')
  loading.value = true
  error.value = null
  
  console.log('🔄 Loading cluster details for ID:', clusterId.value)
  
  // Validate cluster ID
  if (!clusterId.value || clusterId.value === 'undefined' || clusterId.value === undefined) {
    console.error('❌ Invalid cluster ID:', clusterId.value)
    error.value = 'Invalid cluster ID. Please check the URL and try again.'
    loading.value = false
    return
  }
  
  try {
    // Load cluster details
    const clusterResult = await cachedApiCall(`edgeai-cluster-${clusterId.value}`, 
      () => edgeaiService.clusters.getCluster(clusterId.value), 
      2 * 60 * 1000 // Cache for 2 minutes
    )
    
    console.log('📊 Cluster result:', clusterResult)

    if (clusterResult) {
      cluster.value = {
        id: clusterResult.id,
        name: clusterResult.name,
        description: clusterResult.description || 'No description available',
        type: clusterResult.type || 'Hybrid',
        status: clusterResult.status || 'Active',
        nodeCount: clusterResult.node_count || 0,
        cpuCores: clusterResult.cpu_cores || 0,
        memory: clusterResult.memory || 0,
        gpuCount: clusterResult.gpu_count || 0,
        activeProjects: clusterResult.active_projects || 0,
        activeProjectNames: clusterResult.active_project_names || [],
        metrics: clusterResult.metrics || null,
        created: clusterResult.created_time ? new Date(clusterResult.created_time).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
        lastUpdated: clusterResult.last_updated_time ? new Date(clusterResult.last_updated_time).toISOString().split('T')[0] : new Date().toISOString().split('T')[0]
      }
      console.log('📋 Mapped cluster:', cluster.value)
    } else {
      throw new Error('Cluster not found')
    }

    // Load cluster nodes - DISABLED
    // await loadClusterNodes()

    pageMonitor.end({ success: true, clusterId: clusterId.value })
  } catch (err) {
    console.error('Failed to load cluster details:', err)
    error.value = err.message || 'Failed to load cluster details'
    pageMonitor.end({ success: false, error: err.message })
  } finally {
    loading.value = false
  }
}

// Load cluster nodes - DISABLED
/*
const loadClusterNodes = async () => {
  nodesLoading.value = true
  
  try {
    const nodesResult = await cachedApiCall(`edgeai-cluster-nodes-${clusterId.value}`, 
      () => edgeaiService.clusters.getClusterNodes(clusterId.value), 
      1 * 60 * 1000 // Cache for 1 minute
    )
    
    if (nodesResult && Array.isArray(nodesResult)) {
      clusterNodes.value = nodesResult.map(node => ({
        id: node.id,
        name: node.name,
        type: node.type || 'Worker',
        status: node.status || 'Active'
      }))
    } else {
      clusterNodes.value = []
    }
  } catch (err) {
    console.error('Failed to load cluster nodes:', err)
    clusterNodes.value = []
  } finally {
    nodesLoading.value = false
  }
}
*/

// Setup auto-refresh
const setupAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }

  refreshInterval.value = setInterval(async () => {
    if (!loading.value) {
      await loadClusterDetails()
    }
  }, 30 * 1000) // Refresh every 30 seconds
}


// Node-related functions - DISABLED
/*
const refreshNodes = async () => {
  clearCache(`edgeai-cluster-nodes-${clusterId.value}`)
  await loadClusterNodes()
}

const addNode = () => {
  // TODO: Implement add node functionality
  console.log('Add node to cluster:', clusterId.value)
}

const viewNodeDetails = (node) => {
  // TODO: Navigate to node details
  console.log('View node details:', node)
}

const removeNode = async (node) => {
  try {
    await edgeaiService.clusters.removeNodeFromCluster(clusterId.value, node.id)
    await loadClusterNodes()
  } catch (err) {
    console.error('Failed to remove node:', err)
  }
}
*/

// Delete cluster function
const deleteCluster = async () => {
  if (!confirm(`Are you sure you want to delete cluster "${cluster.value?.name}"? This action cannot be undone.`)) {
    return
  }

  deleting.value = true
  error.value = null
  
  try {
    console.log('🗑️ Deleting cluster:', clusterId.value)
    const result = await edgeaiService.clusters.deleteCluster(clusterId.value)
    
    // Show success message
    console.log('✅ Cluster deleted successfully:', result)
    
    // Clear cache to ensure fresh data on next load
    clearCache(`edgeai-cluster-${clusterId.value}`)
    clearCache('edgeai-clusters')
    
    // Redirect to cluster management page
    router.push('/edgeai/cluster-management')
  } catch (err) {
    console.error('❌ Failed to delete cluster:', err)
    error.value = err.message || 'Failed to delete cluster'
    
    // Show user-friendly error message
    alert(`Failed to delete cluster: ${err.message || 'Unknown error'}`)
  } finally {
    deleting.value = false
  }
}


// Component lifecycle
onMounted(async () => {
  // Wait for route params to be resolved
  await new Promise(resolve => setTimeout(resolve, 0))
  
  // Double check that clusterId is valid before loading
  if (clusterId.value && clusterId.value !== 'undefined') {
    await loadClusterDetails()
    setupAutoRefresh()
  } else {
    console.error('❌ Cluster ID not available on mount:', clusterId.value)
    error.value = 'Invalid cluster ID. Please check the URL and try again.'
  }
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  clearCache()
})
</script>
