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
            <CpuChipIcon class="h-8 w-8 text-blue-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Model Management
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
          AI Model Management
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          Manage AI models, versions, and deployment configurations for your EdgeAI projects
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600 dark:text-gray-400">Loading models data...</span>
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
              Failed to load models data
            </h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </div>
            <div class="mt-3">
              <Button @click="loadModelsData" variant="ghost" size="sm" class="text-red-800 dark:text-red-200 hover:bg-red-100 dark:hover:bg-red-800/30">
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
          title="Total Models"
          :value="totalModels"
          :icon="CpuChipIcon"
          variant="primary"
          description="Available AI models"
        />
        <StatCard
          title="Active Models"
          :value="activeModels"
          :icon="PlayCircleIcon"
          variant="success"
          description="Currently deployed"
        />
        <StatCard
          title="Model Versions"
          :value="modelVersions"
          :icon="TagIcon"
          variant="info"
          description="Total versions"
        />
        <StatCard
          title="Storage Used"
          :value="storageUsed"
          unit="GB"
          :icon="ServerIcon"
          variant="warning"
          description="Model storage usage"
        />
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap gap-4 mb-8">
        <Button 
          @click="showUploadModal = true"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium"
        >
          <PlusIcon class="w-5 h-5 mr-2" />
          Upload New Model
        </Button>
        
        <Button 
          @click="showImportModal = true"
          variant="secondary"
          class="px-6 py-3 rounded-lg font-medium"
        >
          <ArrowDownTrayIcon class="w-5 h-5 mr-2" />
          Import from Hub
        </Button>
        
        <Button 
          @click="refreshModels"
          variant="secondary" 
          class="px-6 py-3 rounded-lg font-medium"
        >
          <ArrowPathIcon class="w-5 h-5 mr-2" />
          Refresh
        </Button>
      </div>

      <!-- Models List -->
      <Card class="mb-8">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <CpuChipIcon class="w-6 h-6 text-blue-600 mr-3" />
              <h2 class="text-lg font-semibold">Available Models</h2>
            </div>
            <div class="flex items-center space-x-4">
              <!-- Search -->
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search models..."
                  class="w-64 pl-4 pr-10 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <MagnifyingGlassIcon class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              </div>
              
              <!-- Filter -->
              <select
                v-model="typeFilter"
                class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Types</option>
                <option value="LLM">Language Models</option>
                <option value="Vision">Computer Vision</option>
                <option value="Audio">Audio Processing</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
        </template>

        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Model Name
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Type
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Version
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Size
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Last Updated
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="model in filteredModels" :key="model.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                      <div class="h-10 w-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                        <CpuChipIcon class="h-6 w-6 text-blue-600 dark:text-blue-400" />
                      </div>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900 dark:text-white">
                        {{ model.name }}
                      </div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">
                        {{ model.description }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getTypeColor(model.type)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ model.type }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ model.version }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusColor(model.status)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                    {{ model.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ model.size }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ model.lastUpdated }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <Button 
                    @click="deployModel(model)" 
                    variant="primary" 
                    size="sm"
                    :disabled="model.status === 'Active'"
                  >
                    {{ model.status === 'Active' ? 'Deployed' : 'Deploy' }}
                  </Button>
                  <Button 
                    @click="viewModelDetails(model)" 
                    variant="ghost" 
                    size="sm"
                  >
                    Details
                  </Button>
                  <Button 
                    @click="deleteModel(model)" 
                    variant="ghost" 
                    size="sm"
                    class="text-red-600 hover:text-red-700"
                  >
                    Delete
                  </Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>

      <!-- Upload Modal -->
      <ModelUploadModal 
        :show="showUploadModal"
        @close="showUploadModal = false"
        @uploaded="handleModelUploaded"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import ModelUploadModal from '@/components/edgeai/ModelUploadModal.vue'
import { useApiOptimization } from '@/composables/useApiOptimization'
import { useNotifications } from '@/composables/useNotifications'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import {
  CpuChipIcon,
  PlusIcon,
  ArrowDownTrayIcon,
  ArrowPathIcon,
  MagnifyingGlassIcon,
  PlayCircleIcon,
  TagIcon,
  ServerIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const { cachedApiCall, clearCache } = useApiOptimization()
const notifications = useNotifications()
const showError = notifications.error

// Reactive data
const searchQuery = ref('')
const typeFilter = ref('')
const showUploadModal = ref(false)
const showImportModal = ref(false)
const loading = ref(false)
const error = ref(null)
const refreshInterval = ref(null)

// Statistics (will be loaded from API)
const totalModels = ref(0)
const activeModels = ref(0)
const modelVersions = ref(0)
const storageUsed = ref(0)

// Models data (will be loaded from API)
const models = ref([])

// Computed properties
const filteredModels = computed(() => {
  let filtered = models.value

  // Filter by search query
  if (searchQuery.value) {
    filtered = filtered.filter(model => 
      model.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      model.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Filter by type
  if (typeFilter.value) {
    filtered = filtered.filter(model => model.type === typeFilter.value)
  }

  return filtered
})

// Utility functions
const getTypeColor = (type) => {
  const colors = {
    LLM: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    Vision: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    Audio: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    Other: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
  }
  return colors[type] || colors.Other
}

const getStatusColor = (status) => {
  const colors = {
    Active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    Inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    Error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return colors[status] || colors.Inactive
}

// Load models data from API
const loadModelsData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('EdgeAIModelManagement')
  loading.value = true
  error.value = null
  
  try {
    // Load models and statistics in parallel
    const [modelsResult, statsResult] = await Promise.all([
      cachedApiCall('edgeai-models', 
        () => edgeaiService.models.getModels(), 
        2 * 60 * 1000 // Cache for 2 minutes
      ),
      cachedApiCall('edgeai-model-stats', 
        () => edgeaiService.models.getModelStats(), 
        1 * 60 * 1000 // Cache for 1 minute
      )
    ])

    // Update models data
    if (modelsResult && Array.isArray(modelsResult)) {
      models.value = modelsResult.map(model => ({
        id: model.id,
        name: model.name,
        description: model.description || 'No description available',
        type: model.type || 'Other',
        version: model.version || 'v1.0.0',
        status: model.status || 'Inactive',
        size: model.size || 'Unknown',
        lastUpdated: model.last_updated || new Date().toISOString().split('T')[0]
      }))
    }

    // Update statistics
    if (statsResult) {
      totalModels.value = statsResult.total || models.value.length
      activeModels.value = statsResult.active || models.value.filter(m => m.status === 'Active').length
      modelVersions.value = statsResult.versions || models.value.length
      storageUsed.value = statsResult.storage_used || 0
    }

    pageMonitor.end({ success: true, modelCount: models.value.length })
  } catch (err) {
    console.error('Failed to load models data:', err)
    error.value = err.message || 'Failed to load models data'
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
  
  refreshInterval.value = setInterval(() => {
    if (!loading.value) {
      loadModelsData()
    }
  }, 60 * 1000) // Refresh every minute
}

// Handler functions
const refreshModels = async () => {
  clearCache() // Clear cache to ensure fresh data
  await loadModelsData()
}

const deployModel = async (model) => {
  if (model.status === 'Active') {
    return // Already deployed
  }

  const monitor = performanceMonitor.monitorPageLoad('EdgeAIModelDeploy')
  
  try {
    const result = await edgeaiService.models.deployModel(model.id)
    
    if (result && result.success) {
      model.status = 'Active'
      activeModels.value++
      
      console.log('Deployed model:', model.name)
      monitor.end({ success: true, modelId: model.id })
    } else {
      throw new Error(result?.error || 'Failed to deploy model')
    }
  } catch (error) {
    console.error('Failed to deploy model:', error)
    monitor.end({ success: false, error: error.message })
  }
}

const viewModelDetails = (model) => {
  console.log('Viewing model details:', model.name)
  router.push(`/edgeai/model-details/${model.id}`)
}

const deleteModel = async (model) => {
  if (!confirm(`Are you sure you want to delete ${model.name}? This action cannot be undone.`)) {
    return
  }

  const monitor = performanceMonitor.monitorPageLoad('EdgeAIModelDelete')
  
  try {
    const result = await edgeaiService.models.deleteModel(model.id)
    
    if (result && result.success) {
      const index = models.value.findIndex(m => m.id === model.id)
      if (index !== -1) {
        models.value.splice(index, 1)
        totalModels.value--
        if (model.status === 'Active') {
          activeModels.value--
        }
      }
      
      console.log('Deleted model:', model.name)
      monitor.end({ success: true, modelId: model.id })
    } else {
      throw new Error(result?.error || 'Failed to delete model')
    }
  } catch (error) {
    console.error('Failed to delete model:', error)
    showError(`Failed to delete ${model.name}: ${error.message}`)
    monitor.end({ success: false, error: error.message })
  }
}

const handleModelUploaded = async (newModel) => {
  // Refresh the entire models list after upload
  await loadModelsData()
  console.log('New model uploaded:', newModel.name)
}

// Component lifecycle
onMounted(async () => {
  await loadModelsData()
  setupAutoRefresh()
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  clearCache()
})
</script>