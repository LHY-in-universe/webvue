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

      <!-- Statistics Cards -->
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import ModelUploadModal from '@/components/edgeai/ModelUploadModal.vue'
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

// Reactive data
const searchQuery = ref('')
const typeFilter = ref('')
const showUploadModal = ref(false)
const showImportModal = ref(false)

// Statistics
const totalModels = ref(12)
const activeModels = ref(8)
const modelVersions = ref(24)
const storageUsed = ref(156.7)

// Models data
const models = ref([
  {
    id: 1,
    name: 'Gemma-7B-Instruct',
    description: 'Large language model for instruction following',
    type: 'LLM',
    version: 'v2.1.0',
    status: 'Active',
    size: '14.2 GB',
    lastUpdated: '2024-01-15'
  },
  {
    id: 2,
    name: 'ResNet-50',
    description: 'Residual neural network for image classification',
    type: 'Vision',
    version: 'v1.8.3',
    status: 'Active',
    size: '98 MB',
    lastUpdated: '2024-01-12'
  },
  {
    id: 3,
    name: 'YOLO-v8',
    description: 'Object detection and segmentation model',
    type: 'Vision',
    version: 'v8.0.2',
    status: 'Inactive',
    size: '6.2 GB',
    lastUpdated: '2024-01-10'
  },
  {
    id: 4,
    name: 'Whisper-Large',
    description: 'Automatic speech recognition model',
    type: 'Audio',
    version: 'v3.0.0',
    status: 'Active',
    size: '3.1 GB',
    lastUpdated: '2024-01-08'
  },
  {
    id: 5,
    name: 'BERT-Base',
    description: 'Bidirectional encoder for language understanding',
    type: 'LLM',
    version: 'v1.2.1',
    status: 'Inactive',
    size: '440 MB',
    lastUpdated: '2024-01-05'
  },
  {
    id: 6,
    name: 'EfficientNet-B7',
    description: 'Efficient convolutional neural network',
    type: 'Vision',
    version: 'v2.0.1',
    status: 'Active',
    size: '256 MB',
    lastUpdated: '2024-01-03'
  }
])

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

// Handler functions
const refreshModels = () => {
  console.log('Refreshing models...')
}

const deployModel = (model) => {
  if (model.status !== 'Active') {
    model.status = 'Active'
    activeModels.value++
    console.log('Deployed model:', model.name)
  }
}

const viewModelDetails = (model) => {
  console.log('Viewing model details:', model.name)
  router.push(`/edgeai/model-details/${model.id}`)
}

const deleteModel = (model) => {
  if (confirm(`Are you sure you want to delete ${model.name}?`)) {
    const index = models.value.findIndex(m => m.id === model.id)
    if (index !== -1) {
      models.value.splice(index, 1)
      totalModels.value--
      if (model.status === 'Active') {
        activeModels.value--
      }
      console.log('Deleted model:', model.name)
    }
  }
}

const handleModelUploaded = (newModel) => {
  models.value.unshift(newModel)
  totalModels.value++
  console.log('New model uploaded:', newModel.name)
}
</script>