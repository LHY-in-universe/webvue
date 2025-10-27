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
              ← Back to Models
            </Button>
            <CpuChipIcon class="h-8 w-8 text-blue-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              {{ model.name }} Details
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600 dark:text-gray-400">Loading model details...</span>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <div class="w-12 h-12 text-red-400 mx-auto mb-4">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>
        <p class="text-red-500 dark:text-red-400 mb-4">{{ error }}</p>
        <Button @click="loadModelDetails" variant="ghost" size="sm">
          Retry
        </Button>
      </div>
      
      <!-- Model Content -->
      <div v-else>
        <!-- Model Header -->
      <Card class="mb-8">
        <div class="flex items-start justify-between">
          <div class="flex items-center">
            <div class="h-16 w-16 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center mr-6">
              <CpuChipIcon class="h-8 w-8 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{{ model.name }}</h1>
              <p class="text-gray-600 dark:text-gray-400 mb-4">{{ model.description }}</p>
              <div class="flex items-center space-x-4">
                <span :class="getStatusColor(model.status)" class="inline-flex px-3 py-1 text-sm font-semibold rounded-full">
                  {{ model.status }}
                </span>
                <span :class="getTypeColor(model.type)" class="inline-flex px-3 py-1 text-sm font-semibold rounded-full">
                  {{ model.type }}
                </span>
                <span class="text-sm text-gray-500 dark:text-gray-400">Version {{ model.version }}</span>
              </div>
            </div>
          </div>
          
          <div class="flex space-x-3">
            <Button 
              @click="deployModel" 
              :variant="model.status === 'Active' ? 'secondary' : 'primary'"
              :disabled="model.status === 'Active' || loading"
              :loading="loading"
            >
              {{ model.status === 'Active' ? 'Deployed' : 'Deploy Model' }}
            </Button>
            <Button variant="secondary" @click="downloadModel">
              <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
              Download
            </Button>
          </div>
        </div>
      </Card>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Model Information -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Model Specifications -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Model Specifications</h3>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Architecture</label>
                <p class="text-gray-900 dark:text-white">{{ model.architecture }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Framework</label>
                <p class="text-gray-900 dark:text-white">{{ model.framework }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Parameters</label>
                <p class="text-gray-900 dark:text-white">{{ model.parameters }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Input Size</label>
                <p class="text-gray-900 dark:text-white">{{ model.inputSize }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">File Size</label>
                <p class="text-gray-900 dark:text-white">{{ model.size }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">License</label>
                <p class="text-gray-900 dark:text-white">{{ model.license }}</p>
              </div>
            </div>
          </Card>

          <!-- Performance Metrics -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Performance Metrics</h3>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div class="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-2">{{ modelPerformance.accuracy || 0 }}%</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Accuracy</div>
              </div>
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div class="text-2xl font-bold text-green-600 dark:text-green-400 mb-2">{{ modelPerformance.latency || 0 }}ms</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Latency</div>
              </div>
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div class="text-2xl font-bold text-purple-600 dark:text-purple-400 mb-2">{{ modelPerformance.throughput || 'N/A' }}</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Throughput</div>
              </div>
            </div>
          </Card>

          <!-- Usage Examples -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Usage Examples</h3>
            </template>
            
            <div class="space-y-4">
              <div>
                <h4 class="font-medium text-gray-900 dark:text-white mb-2">Python API</h4>
                <pre class="bg-gray-800 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm"><code>import edgeai

# Load the model
model = edgeai.load_model('{{ model.name ? model.name.toLowerCase().replace(/[^a-z0-9]/g, '-') : 'model' }}')

# Make predictions
result = model.predict(input_data)
print(result)</code></pre>
              </div>
              
              <div>
                <h4 class="font-medium text-gray-900 dark:text-white mb-2">REST API</h4>
                <pre class="bg-gray-800 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm"><code>curl -X POST "https://api.edgeai.com/v1/models/{{ model.name ? model.name.toLowerCase().replace(/[^a-z0-9]/g, '-') : 'model' }}/predict" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "your_input_data"}'</code></pre>
              </div>
            </div>
          </Card>
        </div>

        <!-- Sidebar -->
        <div class="space-y-8">
          <!-- Quick Actions -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Quick Actions</h3>
            </template>
            
            <div class="space-y-3">
              <Button 
                class="w-full justify-start" 
                variant="ghost"
                @click="testModel"
              >
                <PlayIcon class="w-4 h-4 mr-2" />
                Test Model
              </Button>
              <Button 
                class="w-full justify-start" 
                variant="ghost"
                @click="viewLogs"
              >
                <DocumentTextIcon class="w-4 h-4 mr-2" />
                View Logs
              </Button>
              <Button 
                class="w-full justify-start" 
                variant="ghost"
                @click="exportModel"
              >
                <ShareIcon class="w-4 h-4 mr-2" />
                Export Model
              </Button>
              <Button 
                class="w-full justify-start text-red-600 hover:text-red-700" 
                variant="ghost"
                @click="deleteModel"
              >
                <TrashIcon class="w-4 h-4 mr-2" />
                Delete Model
              </Button>
            </div>
          </Card>

          <!-- Model Statistics -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Statistics</h3>
            </template>
            
            <div class="space-y-4">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Downloads:</span>
                <span class="font-medium">{{ modelStats.downloads || 0 }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Deployments:</span>
                <span class="font-medium">{{ modelStats.deployments || 0 }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Created:</span>
                <span class="font-medium">{{ model.created || 'N/A' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Last Updated:</span>
                <span class="font-medium">{{ model.lastUpdated || 'N/A' }}</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUIStore } from '@/stores/ui'
import { useApiOptimization } from '@/composables/useApiOptimization'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import {
  CpuChipIcon,
  ArrowDownTrayIcon,
  PlayIcon,
  DocumentTextIcon,
  ShareIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()
const uiStore = useUIStore()
const { cachedApiCall } = useApiOptimization()

// State
const loading = ref(false)
const error = ref(null)
const model = ref({})
const modelStats = ref({})
const modelPerformance = ref({})

// Utility functions
const getStatusColor = (status) => {
  const colors = {
    Active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    Inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    Error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return colors[status] || colors.Inactive
}

const getTypeColor = (type) => {
  const colors = {
    LLM: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    Vision: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    Audio: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    Other: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
  }
  return colors[type] || colors.Other
}

// Load model details from API
const loadModelDetails = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('ModelDetails')
  loading.value = true
  error.value = null
  
  try {
    const modelId = route.params.id
    
    const [modelResult, statsResult, performanceResult] = await Promise.all([
      cachedApiCall(`edgeai-model-${modelId}`, 
        () => edgeaiService.models.getModel(modelId), 
        120 * 1000 // Cache for 2 minutes
      ),
      cachedApiCall(`edgeai-model-stats-${modelId}`,
        () => edgeaiService.models.getModelStats(),
        60 * 1000 // Cache for 1 minute
      ),
      cachedApiCall(`edgeai-model-performance-${modelId}`, 
        () => edgeaiService.models.getModelPerformance(modelId), 
        300 * 1000 // Cache for 5 minutes
      )
    ])
    
    if (modelResult) {
      model.value = {
        id: modelResult.id,
        name: modelResult.name,
        description: modelResult.description,
        type: modelResult.type || 'Custom',
        version: modelResult.version,
        status: modelResult.status,
        size: modelResult.size || 'Unknown',
        architecture: modelResult.architecture || 'Unknown',
        framework: modelResult.framework || 'Unknown',
        parameters: modelResult.parameters || 'N/A',
        inputSize: modelResult.input_size || 'N/A',
        license: modelResult.license || 'N/A',
        created: modelResult.created_date || 'N/A',
        lastUpdated: modelResult.last_updated || 'N/A',
        accuracy: modelResult.accuracy || 0,
        deploymentCount: modelResult.deployment_count || 0,
        projects: modelResult.projects || [],
        metrics: modelResult.metrics || {},
        performance: modelResult.performance || {}
      }
    }
    
    if (statsResult) {
      modelStats.value = {
        downloads: statsResult.downloads || 0,
        deployments: statsResult.deployments || 0,
        usage_count: statsResult.usage_count || 0
      }
    }
    
    if (performanceResult) {
      modelPerformance.value = {
        accuracy: performanceResult.accuracy || 0,
        latency: performanceResult.latency || 0,
        throughput: performanceResult.throughput || 'N/A'
      }
    }
    
    pageMonitor.end()
    
  } catch (err) {
    console.error('Failed to load model details:', err)
    error.value = err.message || 'Failed to load model details'
    pageMonitor.end()
  } finally {
    loading.value = false
  }
}

// Format utilities
const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return 'N/A'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (timestamp) => {
  if (!timestamp) return 'N/A'
  return new Date(timestamp).toLocaleDateString('zh-CN')
}

const formatRelativeTime = (timestamp) => {
  if (!timestamp) return 'N/A'
  
  const now = new Date()
  const date = new Date(timestamp)
  const diffMs = now - date
  const diffMinutes = Math.floor(diffMs / 60000)
  
  if (diffMinutes < 1) return '刚刚'
  if (diffMinutes < 60) return `${diffMinutes} 分钟前`
  
  const diffHours = Math.floor(diffMinutes / 60)
  if (diffHours < 24) return `${diffHours} 小时前`
  
  const diffDays = Math.floor(diffHours / 24)
  return `${diffDays} 天前`
}

// Handler functions
const deployModel = async () => {
  if (model.value.status === 'Active') return
  
  try {
    loading.value = true
    const result = await edgeaiService.models.deployModel(model.value.id)
    
    if (result.success) {
      model.value.status = 'Active'
      uiStore.addNotification({
        type: 'success',
        title: 'Model Deployed',
        message: `${model.value.name} has been deployed successfully`
      })
    } else {
      throw new Error(result.error || 'Failed to deploy model')
    }
  } catch (err) {
    uiStore.addNotification({
      type: 'error',
      title: 'Deployment Failed',
      message: err.message || 'Failed to deploy model'
    })
  } finally {
    loading.value = false
  }
}

const downloadModel = async () => {
  try {
    await edgeaiService.models.downloadModel(model.value.id, model.value.name)
    uiStore.addNotification({
      type: 'success',
      title: 'Download Started',
      message: `Downloading ${model.value.name}...`
    })
  } catch (err) {
    uiStore.addNotification({
      type: 'error',
      title: 'Download Failed',
      message: err.message || 'Failed to download model'
    })
  }
}

const testModel = () => {
  router.push(`/edgeai/models/${model.value.id}/test`)
}

const viewLogs = () => {
  router.push(`/edgeai/models/${model.value.id}/logs`)
}

const exportModel = async () => {
  try {
    await edgeaiService.models.exportModel(model.value.id)
    uiStore.addNotification({
      type: 'success',
      title: 'Export Started',
      message: `Exporting ${model.value.name}...`
    })
  } catch (err) {
    uiStore.addNotification({
      type: 'error',
      title: 'Export Failed',
      message: err.message || 'Failed to export model'
    })
  }
}

const deleteModel = async () => {
  if (!confirm(`Are you sure you want to delete ${model.value.name}?`)) {
    return
  }
  
  try {
    loading.value = true
    const result = await edgeaiService.models.deleteModel(model.value.id)
    
    if (result.success) {
      uiStore.addNotification({
        type: 'success',
        title: 'Model Deleted',
        message: `${model.value.name} has been deleted`
      })
      router.push('/edgeai/model-management')
    } else {
      throw new Error(result.error || 'Failed to delete model')
    }
  } catch (err) {
    uiStore.addNotification({
      type: 'error',
      title: 'Delete Failed',
      message: err.message || 'Failed to delete model'
    })
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadModelDetails()
})
</script>