<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Navigation -->
    <nav class="glass-effect shadow-soft border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors micro-bounce"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            
            <div class="w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center mr-3 micro-bounce hover-glow-primary">
              <CircleStackIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gradient text-shadow-soft">
              Dataset Management
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <Button 
              @click="showCreateModal = true"
              variant="primary"
              :leftIcon="PlusIcon"
              size="sm"
            >
              New Dataset
            </Button>
            <Button 
              @click="toggleTheme" 
              variant="ghost" 
              size="sm"
              iconOnly
              :leftIcon="themeStore.isDark ? SunIcon : MoonIcon"
            />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between mb-8 animate-fade-in-up">
        <div>
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Dataset Management
          </h2>
          <p class="text-gray-600 dark:text-gray-400">
            Manage and organize your training datasets
          </p>
        </div>
        
        <div class="flex items-center space-x-4">
          <!-- Search -->
          <div class="relative">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search datasets..."
              class="input-base pl-10 w-64"
            />
          </div>
          
          <!-- Filter -->
          <select v-model="selectedFilter" class="input-base w-40">
            <option value="">All Types</option>
            <option value="image">Images</option>
            <option value="text">Text</option>
            <option value="tabular">Tabular</option>
            <option value="audio">Audio</option>
          </select>
        </div>
      </div>

      <!-- Dataset Statistics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 stagger-children">
        <StatCard
          title="Total Datasets"
          :value="totalDatasets"
          :icon="CircleStackIcon"
          variant="primary"
          :trend="5.2"
          trend-label="vs last month"
          description="All datasets"
          animated
        />
        
        <StatCard
          title="Total Storage"
          :value="totalStorage"
          unit="GB"
          :precision="1"
          :icon="CircleStackIcon"
          variant="success"
          :progress="storageUsagePercent"
          description="Used storage"
          animated
        />
        
        <StatCard
          title="Active Datasets"
          :value="activeDatasets"
          :icon="CheckCircleIcon"
          variant="info"
          description="Currently in use"
          animated
        />

        <StatCard
          title="Processing Queue"
          :value="processingQueue"
          :icon="ClockIcon"
          variant="warning"
          description="Awaiting processing"
          animated
        />
      </div>

      <!-- Dataset Actions Bar -->
      <Card class="glass-effect mb-8">
        <div class="p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <Button
                v-if="selectedDatasets.length > 0"
                @click="bulkDelete"
                variant="danger"
                :leftIcon="TrashIcon"
                size="sm"
              >
                Delete Selected ({{ selectedDatasets.length }})
              </Button>
              
              <Button
                v-if="selectedDatasets.length > 0"
                @click="bulkDownload"
                variant="secondary"
                :leftIcon="ArrowDownTrayIcon"
                size="sm"
              >
                Download Selected
              </Button>
              
              <Button
                @click="refreshDatasets"
                variant="ghost"
                :leftIcon="ArrowPathIcon"
                size="sm"
              >
                Refresh
              </Button>
            </div>
            
            <div class="flex items-center space-x-4">
              <span class="text-sm text-gray-600 dark:text-gray-400">
                Showing {{ filteredDatasets.length }} of {{ datasets.length }} datasets
              </span>
              
              <div class="flex items-center space-x-2">
                <Button
                  @click="viewMode = 'grid'"
                  :variant="viewMode === 'grid' ? 'primary' : 'ghost'"
                  size="sm"
                  iconOnly
                  :leftIcon="Squares2X2Icon"
                />
                <Button
                  @click="viewMode = 'list'"
                  :variant="viewMode === 'list' ? 'primary' : 'ghost'"
                  size="sm"
                  iconOnly
                  :leftIcon="ListBulletIcon"
                />
              </div>
            </div>
          </div>
        </div>
      </Card>

      <!-- Dataset Grid/List View -->
      <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card 
          v-for="dataset in filteredDatasets" 
          :key="dataset.id"
          class="glass-effect hover-lift-strong cursor-pointer"
          @click="selectDataset(dataset)"
        >
          <div class="p-6">
            <!-- Dataset Header -->
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center space-x-3">
                <input
                  type="checkbox"
                  :checked="selectedDatasets.includes(dataset.id)"
                  @click.stop
                  @change="toggleDatasetSelection(dataset.id)"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <div 
                  :class="[
                    'w-12 h-12 rounded-lg flex items-center justify-center',
                    getTypeIcon(dataset.type).bgClass
                  ]"
                >
                  <component :is="getTypeIcon(dataset.type).icon" class="w-6 h-6 text-white" />
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ dataset.name }}
                  </h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    {{ dataset.type }} • {{ formatFileSize(dataset.size) }}
                  </p>
                </div>
              </div>
              
              <div class="flex items-center space-x-2">
                <span 
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    getStatusClasses(dataset.status)
                  ]"
                >
                  {{ dataset.status }}
                </span>
              </div>
            </div>

            <!-- Dataset Info -->
            <div class="space-y-3 mb-4">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Samples:</span>
                <span class="font-medium">{{ dataset.samples.toLocaleString() }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Features:</span>
                <span class="font-medium">{{ dataset.features }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Created:</span>
                <span class="font-medium">{{ formatDate(dataset.createdAt) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Last Used:</span>
                <span class="font-medium">{{ formatDate(dataset.lastUsed) }}</span>
              </div>
            </div>

            <!-- Progress Bar (if processing) -->
            <div v-if="dataset.status === 'processing'" class="mb-4">
              <ProgressBar 
                :percentage="dataset.progress || 0"
                variant="primary"
                :animated="true"
                :show-percentage="true"
                size="sm"
              />
              <p class="text-xs text-gray-500 dark:text-gray-400 text-center mt-1">
                Processing...
              </p>
            </div>

            <!-- Dataset Actions -->
            <div class="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
              <div class="flex items-center space-x-2">
                <Button
                  @click.stop="previewDataset(dataset)"
                  variant="ghost"
                  size="xs"
                  :leftIcon="EyeIcon"
                >
                  Preview
                </Button>
                <Button
                  @click.stop="downloadDataset(dataset)"
                  variant="ghost"
                  size="xs"
                  :leftIcon="ArrowDownTrayIcon"
                >
                  Download
                </Button>
              </div>
              
              <div class="flex items-center space-x-2">
                <Button
                  @click.stop="editDataset(dataset)"
                  variant="ghost"
                  size="xs"
                  :leftIcon="PencilIcon"
                />
                <Button
                  @click.stop="deleteDataset(dataset)"
                  variant="ghost"
                  size="xs"
                  :leftIcon="TrashIcon"
                  class="text-red-600 hover:text-red-700"
                />
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- List View -->
      <Card v-else class="glass-effect">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 dark:bg-slate-700">
              <tr>
                <th class="px-6 py-3 text-left">
                  <input
                    type="checkbox"
                    :checked="selectedDatasets.length === filteredDatasets.length"
                    :indeterminate="selectedDatasets.length > 0 && selectedDatasets.length < filteredDatasets.length"
                    @change="toggleAllSelection"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Dataset
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Type
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Samples
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Size
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Created
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
              <tr 
                v-for="dataset in filteredDatasets" 
                :key="dataset.id"
                class="hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors cursor-pointer"
                @click="selectDataset(dataset)"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <input
                    type="checkbox"
                    :checked="selectedDatasets.includes(dataset.id)"
                    @click.stop
                    @change="toggleDatasetSelection(dataset.id)"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div 
                      :class="[
                        'w-8 h-8 rounded-lg flex items-center justify-center mr-3',
                        getTypeIcon(dataset.type).bgClass
                      ]"
                    >
                      <component :is="getTypeIcon(dataset.type).icon" class="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-900 dark:text-white">
                        {{ dataset.name }}
                      </div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">
                        {{ dataset.description }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ dataset.type }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ dataset.samples.toLocaleString() }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ formatFileSize(dataset.size) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      getStatusClasses(dataset.status)
                    ]"
                  >
                    {{ dataset.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ formatDate(dataset.createdAt) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex items-center space-x-2">
                    <Button
                      @click.stop="previewDataset(dataset)"
                      variant="ghost"
                      size="xs"
                      :leftIcon="EyeIcon"
                    />
                    <Button
                      @click.stop="editDataset(dataset)"
                      variant="ghost"
                      size="xs"
                      :leftIcon="PencilIcon"
                    />
                    <Button
                      @click.stop="deleteDataset(dataset)"
                      variant="ghost"
                      size="xs"
                      :leftIcon="TrashIcon"
                      class="text-red-600 hover:text-red-700"
                    />
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>

    <!-- Create Dataset Modal -->
    <Modal
      :isOpen="showCreateModal"
      @close="showCreateModal = false"
      title="Create New Dataset"
      size="lg"
    >
      <div class="space-y-6">
        <div class="grid grid-cols-1 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Dataset Name
            </label>
            <input
              v-model="newDataset.name"
              type="text"
              placeholder="Enter dataset name..."
              class="input-base"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Description
            </label>
            <textarea
              v-model="newDataset.description"
              placeholder="Describe your dataset..."
              rows="3"
              class="input-base"
            ></textarea>
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Dataset Type
              </label>
              <select v-model="newDataset.type" class="input-base">
                <option value="image">Image</option>
                <option value="text">Text</option>
                <option value="tabular">Tabular</option>
                <option value="audio">Audio</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Format
              </label>
              <select v-model="newDataset.format" class="input-base">
                <option value="csv">CSV</option>
                <option value="json">JSON</option>
                <option value="parquet">Parquet</option>
                <option value="hdf5">HDF5</option>
              </select>
            </div>
          </div>
          
          <!-- File Upload Area -->
          <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6">
            <div class="text-center">
              <CloudArrowUpIcon class="mx-auto h-12 w-12 text-gray-400" />
              <div class="mt-2">
                <Button variant="primary" @click="triggerFileUpload">
                  Upload Files
                </Button>
                <input
                  ref="fileInput"
                  type="file"
                  multiple
                  class="hidden"
                  @change="handleFileUpload"
                />
              </div>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                Or drag and drop files here
              </p>
            </div>
          </div>
          
          <!-- Upload Progress -->
          <div v-if="uploadProgress > 0" class="space-y-2">
            <ProgressBar 
              :percentage="uploadProgress"
              variant="primary"
              :animated="uploadProgress < 100"
              :show-percentage="true"
            />
            <p class="text-sm text-gray-600 dark:text-gray-400 text-center">
              Uploading... {{ uploadProgress }}%
            </p>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button @click="showCreateModal = false" variant="secondary">
            Cancel
          </Button>
          <Button 
            @click="createDataset" 
            variant="primary"
            :disabled="!canCreateDataset"
          >
            Create Dataset
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Dataset Preview Modal -->
    <Modal
      :isOpen="showPreviewModal"
      @close="showPreviewModal = false"
      :title="`Preview: ${selectedDataset?.name || ''}`"
      size="xl"
    >
      <div v-if="selectedDataset" class="space-y-6">
        <!-- Dataset Info -->
        <div class="grid grid-cols-2 gap-6">
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Dataset Information</h4>
            <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
              <p>Type: {{ selectedDataset.type }}</p>
              <p>Samples: {{ selectedDataset.samples.toLocaleString() }}</p>
              <p>Features: {{ selectedDataset.features }}</p>
              <p>Size: {{ formatFileSize(selectedDataset.size) }}</p>
            </div>
          </div>
          
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Statistics</h4>
            <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
              <p>Created: {{ formatDate(selectedDataset.createdAt) }}</p>
              <p>Last Modified: {{ formatDate(selectedDataset.lastUsed) }}</p>
              <p>Status: {{ selectedDataset.status }}</p>
            </div>
          </div>
        </div>
        
        <!-- Data Preview -->
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Data Preview</h4>
          <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4 h-64 overflow-auto">
            <div class="text-center text-gray-500 dark:text-gray-400">
              <CircleStackIcon class="w-12 h-12 mx-auto mb-2" />
              <p>Dataset preview will be displayed here</p>
              <p class="text-xs mt-1">Preview functionality coming soon</p>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button @click="showPreviewModal = false" variant="secondary">
            Close
          </Button>
          <Button @click="startTrainingWithDataset" variant="primary">
            Use for Training
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useApiOptimization } from '@/composables/useApiOptimization.js'
import p2paiService from '@/services/p2paiService.js'
import performanceMonitor from '@/utils/performanceMonitor.js'
import {
  ArrowLeftIcon,
  CircleStackIcon,
  SunIcon,
  MoonIcon,
  PlusIcon,
  MagnifyingGlassIcon,
  CheckCircleIcon,
  ClockIcon,
  TrashIcon,
  ArrowDownTrayIcon,
  ArrowPathIcon,
  Squares2X2Icon,
  ListBulletIcon,
  EyeIcon,
  PencilIcon,
  CloudArrowUpIcon,
  PhotoIcon,
  DocumentTextIcon,
  TableCellsIcon,
  SpeakerWaveIcon
} from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import Modal from '@/components/ui/Modal.vue'

const router = useRouter()
const themeStore = useThemeStore()
const { cachedApiCall } = useApiOptimization()

// API loading state
const loading = ref(true)
const error = ref(null)

// State
const searchQuery = ref('')
const selectedFilter = ref('')
const viewMode = ref('grid')
const selectedDatasets = ref([])
const showCreateModal = ref(false)
const showPreviewModal = ref(false)
const selectedDataset = ref(null)
const uploadProgress = ref(0)

// File upload
const fileInput = ref(null)

// New dataset form
const newDataset = ref({
  name: '',
  description: '',
  type: 'image',
  format: 'csv'
})

// Dataset data - will be loaded from API
const datasets = ref([])
const datasetStats = ref({
  totalDatasets: 0,
  totalStorage: 0,
  activeDatasets: 0,
  processingQueue: 0
})

// Load datasets from API
const loadDatasetsData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('DatasetDashboard')
  loading.value = true
  error.value = null
  
  try {
    // Load datasets and statistics in parallel
    const [datasetsResponse, statsResponse] = await Promise.all([
      cachedApiCall('datasets-list', () => p2paiService.datasets.getDatasets(), 2 * 60 * 1000),
      cachedApiCall('datasets-stats', () => p2paiService.datasets.getDatasetStats(), 5 * 60 * 1000)
    ])
    
    // Update datasets list
    if (datasetsResponse.data?.datasets) {
      datasets.value = datasetsResponse.data.datasets.map(dataset => ({
        id: dataset.id,
        name: dataset.name,
        description: dataset.description,
        type: dataset.type,
        samples: dataset.samples || dataset.total_samples || 0,
        features: dataset.features || dataset.feature_count || 0,
        size: dataset.size || dataset.size_bytes || 0,
        status: dataset.status || 'ready',
        createdAt: new Date(dataset.created_at || Date.now()),
        lastUsed: new Date(dataset.last_used || dataset.updated_at || Date.now()),
        progress: dataset.progress || (dataset.status === 'ready' ? 100 : 0)
      }))
    }
    
    // Update statistics
    if (statsResponse.data) {
      datasetStats.value = {
        totalDatasets: statsResponse.data.total_datasets || datasets.value.length,
        totalStorage: (statsResponse.data.total_size_bytes || 0) / (1024 * 1024 * 1024), // Convert to GB
        activeDatasets: statsResponse.data.active_datasets || datasets.value.filter(d => d.status === 'ready').length,
        processingQueue: statsResponse.data.processing_datasets || datasets.value.filter(d => d.status === 'processing').length
      }
    }
    
    console.log('📊 Dataset data loaded successfully')
  } catch (err) {
    console.error('❌ Failed to load dataset data:', err)
    error.value = err.message || 'Failed to load dataset data'
  } finally {
    loading.value = false
    pageMonitor.end()
  }
}

// Refresh datasets data
const refreshDatasets = async () => {
  await loadDatasetsData()
}

// Computed properties
const filteredDatasets = computed(() => {
  return datasets.value.filter(dataset => {
    const matchesSearch = dataset.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         dataset.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesFilter = !selectedFilter.value || dataset.type === selectedFilter.value
    
    return matchesSearch && matchesFilter
  })
})

const totalDatasets = computed(() => datasetStats.value.totalDatasets)
const totalStorage = computed(() => datasetStats.value.totalStorage)
const storageUsagePercent = computed(() => (totalStorage.value / 1000) * 100)
const activeDatasets = computed(() => datasetStats.value.activeDatasets)
const processingQueue = computed(() => datasetStats.value.processingQueue)

const canCreateDataset = computed(() => {
  return newDataset.value.name && newDataset.value.description
})

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const getTypeIcon = (type) => {
  const icons = {
    image: { icon: PhotoIcon, bgClass: 'bg-blue-500' },
    text: { icon: DocumentTextIcon, bgClass: 'bg-green-500' },
    tabular: { icon: TableCellsIcon, bgClass: 'bg-purple-500' },
    audio: { icon: SpeakerWaveIcon, bgClass: 'bg-orange-500' }
  }
  return icons[type] || icons.tabular
}

const getStatusClasses = (status) => {
  const classes = {
    ready: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    processing: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    pending: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
  }
  return classes[status] || classes.pending
}

const formatFileSize = (bytes) => {
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let size = bytes
  let unitIndex = 0
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  
  return `${size.toFixed(1)} ${units[unitIndex]}`
}

const formatDate = (date) => {
  return date.toLocaleDateString()
}

const toggleDatasetSelection = (datasetId) => {
  const index = selectedDatasets.value.indexOf(datasetId)
  if (index > -1) {
    selectedDatasets.value.splice(index, 1)
  } else {
    selectedDatasets.value.push(datasetId)
  }
}

const toggleAllSelection = () => {
  if (selectedDatasets.value.length === filteredDatasets.value.length) {
    selectedDatasets.value = []
  } else {
    selectedDatasets.value = filteredDatasets.value.map(d => d.id)
  }
}

const selectDataset = (dataset) => {
  selectedDataset.value = dataset
  showPreviewModal.value = true
}

const previewDataset = (dataset) => {
  selectedDataset.value = dataset
  showPreviewModal.value = true
}

const editDataset = (dataset) => {
  console.log('Editing dataset:', dataset.name)
}

const deleteDataset = async (dataset) => {
  if (confirm(`Are you sure you want to delete "${dataset.name}"?`)) {
    try {
      const response = await p2paiService.datasets.deleteDataset(dataset.id)
      
      if (response.success) {
        // Remove from local list
        const index = datasets.value.findIndex(d => d.id === dataset.id)
        if (index > -1) {
          datasets.value.splice(index, 1)
        }
        console.log('✅ Dataset deleted successfully')
        
        // Refresh stats
        await refreshDatasets()
      } else {
        throw new Error(response.error || 'Failed to delete dataset')
      }
    } catch (err) {
      console.error('❌ Failed to delete dataset:', err)
      alert('Failed to delete dataset: ' + err.message)
    }
  }
}

const downloadDataset = async (dataset) => {
  try {
    console.log('💾 Downloading dataset:', dataset.name)
    const filename = `${dataset.name.replace(/[^a-zA-Z0-9]/g, '_')}.zip`
    await p2paiService.datasets.downloadDataset(dataset.id, filename)
    console.log('✅ Dataset download initiated')
  } catch (err) {
    console.error('❌ Failed to download dataset:', err)
    alert('Failed to download dataset: ' + err.message)
  }
}

const bulkDelete = () => {
  if (confirm(`Are you sure you want to delete ${selectedDatasets.value.length} datasets?`)) {
    datasets.value = datasets.value.filter(d => !selectedDatasets.value.includes(d.id))
    selectedDatasets.value = []
  }
}

const bulkDownload = () => {
  console.log('Bulk downloading datasets:', selectedDatasets.value)
}


const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = async (event) => {
  const files = event.target.files
  if (files && files.length > 0) {
    try {
      console.log('📤 Uploading files:', files.length)
      
      const formData = new FormData()
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i])
      }
      
      // Add metadata
      formData.append('name', newDataset.value.name || 'Uploaded Dataset')
      formData.append('description', newDataset.value.description || 'Uploaded via web interface')
      formData.append('type', newDataset.value.type)
      
      // Upload with progress tracking
      const response = await p2paiService.datasets.uploadDataset(formData, (progress) => {
        uploadProgress.value = progress
      })
      
      if (response.success) {
        console.log('✅ Dataset uploaded successfully:', response.data)
        
        // Reset progress after a short delay
        setTimeout(() => {
          uploadProgress.value = 0
        }, 2000)
        
        // Refresh datasets list
        await refreshDatasets()
      } else {
        throw new Error(response.error || 'Upload failed')
      }
    } catch (err) {
      console.error('❌ Failed to upload dataset:', err)
      uploadProgress.value = 0
      alert('Failed to upload dataset: ' + err.message)
    }
  }
}

const createDataset = async () => {
  if (!canCreateDataset.value) return
  
  try {
    console.log('🎆 Creating dataset:', newDataset.value)
    
    const datasetData = {
      name: newDataset.value.name,
      description: newDataset.value.description,
      type: newDataset.value.type,
      format: newDataset.value.format
    }
    
    const response = await p2paiService.datasets.createDataset(datasetData)
    
    if (response.success) {
      // Reset form
      newDataset.value = {
        name: '',
        description: '',
        type: 'image',
        format: 'csv'
      }
      
      showCreateModal.value = false
      
      // Refresh datasets list
      await refreshDatasets()
      
      console.log('✅ Dataset created successfully:', response.data)
    } else {
      throw new Error(response.error || 'Failed to create dataset')
    }
  } catch (err) {
    console.error('❌ Failed to create dataset:', err)
    alert('Failed to create dataset: ' + err.message)
  }
}

const startTrainingWithDataset = () => {
  if (selectedDataset.value) {
    router.push('/p2pai/local-training')
    showPreviewModal.value = false
  }
}

// Auto-refresh interval
let refreshInterval = null

// Lifecycle
onMounted(async () => {
  console.group('📁 Dataset Dashboard mounted')
  console.log('Loading datasets data...')
  
  // Load initial data
  await loadDatasetsData()
  
  // Set up auto-refresh every 2 minutes
  refreshInterval = setInterval(() => {
    if (!loading.value) {
      refreshDatasets()
    }
  }, 2 * 60 * 1000)
  
  console.log('Dataset dashboard initialized with auto-refresh')
  console.groupEnd()
})

onUnmounted(() => {
  console.log('🧹 Cleaning up Dataset Dashboard')
  
  // Clear refresh interval
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  
  console.log('Dataset Dashboard unmounted')
})
</script>

<style scoped>
/* Custom scrollbar for table */
.overflow-x-auto::-webkit-scrollbar {
  height: 4px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.dark .overflow-x-auto::-webkit-scrollbar-track {
  background: #1e293b;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.dark .overflow-x-auto::-webkit-scrollbar-thumb {
  background: #475569;
}
</style>