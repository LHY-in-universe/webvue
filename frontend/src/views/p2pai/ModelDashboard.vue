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
              <CpuChipIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gradient text-shadow-soft">
              Model Management
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <Button 
              @click="showCreateModal = true"
              variant="primary"
              :leftIcon="PlusIcon"
              size="sm"
            >
              New Model
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
            Model Management
          </h2>
          <p class="text-gray-600 dark:text-gray-400">
            Deploy, monitor and manage your AI models
          </p>
        </div>
        
        <div class="flex items-center space-x-4">
          <!-- Search -->
          <div class="relative">
            <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search models..."
              class="input-base pl-10 w-64"
            />
          </div>
          
          <!-- Filter -->
          <select v-model="selectedFilter" class="input-base w-40">
            <option value="">All Status</option>
            <option value="deployed">Deployed</option>
            <option value="training">Training</option>
            <option value="ready">Ready</option>
            <option value="error">Error</option>
          </select>
        </div>
      </div>

      <!-- Model Statistics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 stagger-children">
        <StatCard
          title="Total Models"
          :value="totalModels"
          :icon="CpuChipIcon"
          variant="primary"
          :trend="8.3"
          trend-label="vs last month"
          description="All models"
          :loading="loading.models"
          animated
        />
        
        <StatCard
          title="Deployed Models"
          :value="deployedModels"
          :icon="CloudIcon"
          variant="success"
          :progress="deploymentRate"
          description="Active deployments"
          :loading="loading.models"
          animated
        />
        
        <StatCard
          title="Training Models"
          :value="trainingModels"
          :icon="ArrowPathIcon"
          variant="warning"
          description="Currently training"
          :loading="loading.models"
          animated
        />

        <StatCard
          title="Model Performance"
          :value="averageAccuracy"
          unit="%"
          :precision="1"
          :icon="ChartBarIcon"
          variant="info"
          :trend="2.1"
          trend-label="improvement"
          description="Average accuracy"
          :loading="loading.models"
          animated
        />
      </div>

      <!-- Model Actions Bar -->
      <Card class="glass-effect mb-8">
        <div class="p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <Button
                v-if="selectedModels.length > 0"
                @click="bulkDeploy"
                variant="success"
                :leftIcon="RocketLaunchIcon"
                size="sm"
              >
                Deploy Selected ({{ selectedModels.length }})
              </Button>
              
              <Button
                v-if="selectedModels.length > 0"
                @click="bulkDownload"
                variant="secondary"
                :leftIcon="ArrowDownTrayIcon"
                size="sm"
              >
                Download Selected
              </Button>
              
              <Button
                v-if="selectedModels.length > 0"
                @click="bulkDelete"
                variant="danger"
                :leftIcon="TrashIcon"
                size="sm"
              >
                Delete Selected
              </Button>
              
              <Button
                @click="refreshModels"
                variant="ghost"
                :leftIcon="ArrowPathIcon"
                :loading="refreshing"
                size="sm"
              >
                Refresh
              </Button>
            </div>
            
            <div class="flex items-center space-x-4">
              <span class="text-sm text-gray-600 dark:text-gray-400">
                Showing {{ filteredModels.length }} of {{ models.length }} models
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

      <!-- Model Grid View -->
      <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card 
          v-for="model in filteredModels" 
          :key="model.id"
          class="glass-effect hover-lift-strong cursor-pointer"
          @click="selectModel(model)"
        >
          <div class="p-6">
            <!-- Model Header -->
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center space-x-3">
                <input
                  type="checkbox"
                  :checked="selectedModels.includes(model.id)"
                  @click.stop
                  @change="toggleModelSelection(model.id)"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <div class="w-12 h-12 rounded-lg flex items-center justify-center bg-blue-500">
                  <CpuChipIcon class="w-6 h-6 text-white" />
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ model.name }}
                  </h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    {{ model.version }}
                  </p>
                </div>
              </div>
              
              <div class="flex items-center space-x-2">
                <span 
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded-full',
                    getStatusClasses(model.status)
                  ]"
                >
                  {{ model.status }}
                </span>
              </div>
            </div>

            <!-- Model Metrics -->
            <div class="space-y-3 mb-4">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Accuracy:</span>
                <span class="font-medium text-green-600">{{ (model.accuracy * 100).toFixed(2) }}%</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Loss:</span>
                <span class="font-medium">{{ model.loss ? model.loss.toFixed(6) : 'N/A' }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Size:</span>
                <span class="font-medium">{{ formatFileSize(model.size) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">File Path:</span>
                <span class="font-medium text-xs truncate max-w-[150px]" :title="model.file_path">{{ model.file_path }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Created:</span>
                <span class="font-medium">{{ formatDate(model.created_time) }}</span>
              </div>
            </div>

            <!-- Training Progress (if training) -->
            <div v-if="model.status === 'training'" class="mb-4">
              <ProgressBar 
                :percentage="model.progress || 0"
                variant="primary"
                :animated="true"
                :show-percentage="true"
                size="sm"
              />
              <p class="text-xs text-gray-500 dark:text-gray-400 text-center mt-1">
                Training Progress: {{ model.progress.toFixed(2) }}%
              </p>
            </div>

            <!-- Model Actions -->
            <div class="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
              <div class="flex items-center space-x-2">
                <Button
                  v-if="model.status === 'ready'"
                  @click.stop="deployModel(model)"
                  variant="success"
                  size="xs"
                  :leftIcon="RocketLaunchIcon"
                >
                  Deploy
                </Button>
                <Button
                  v-else-if="model.status === 'deployed'"
                  @click.stop="stopModel(model)"
                  variant="warning"
                  size="xs"
                  :leftIcon="StopIcon"
                >
                  Stop
                </Button>
                <Button
                  @click.stop="testModel(model)"
                  variant="ghost"
                  size="xs"
                  :leftIcon="BeakerIcon"
                >
                  Test
                </Button>
              </div>
              
              <div class="flex items-center space-x-2">
                <Button
                  @click.stop="exportModel(model)"
                  variant="ghost"
                  size="xs"
                  :leftIcon="ArrowDownTrayIcon"
                />
                <Button
                  @click.stop="editModel(model)"
                  variant="ghost"
                  size="xs"
                  :leftIcon="PencilIcon"
                />
                <Button
                  @click.stop="deleteModel(model)"
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
                    :checked="selectedModels.length === filteredModels.length"
                    :indeterminate="selectedModels.length > 0 && selectedModels.length < filteredModels.length"
                    @change="toggleAllSelection"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Model
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  File Path
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Size
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Accuracy
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Loss
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
                v-for="model in filteredModels" 
                :key="model.id"
                class="hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors cursor-pointer"
                @click="selectModel(model)"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <input
                    type="checkbox"
                    :checked="selectedModels.includes(model.id)"
                    @click.stop
                    @change="toggleModelSelection(model.id)"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="w-8 h-8 rounded-lg flex items-center justify-center mr-3 bg-blue-500">
                      <CpuChipIcon class="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-900 dark:text-white">
                        {{ model.name }}
                      </div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">
                        {{ model.version }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  <span class="truncate max-w-[200px] inline-block" :title="model.file_path">{{ model.file_path }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ formatFileSize(model.size) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  <span class="text-green-600 font-medium">{{ (model.accuracy * 100).toFixed(2) }}%</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ model.loss ? model.loss.toFixed(6) : 'N/A' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      getStatusClasses(model.status)
                    ]"
                  >
                    {{ model.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ formatDate(model.created_time) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div class="flex items-center space-x-2">
                    <Button
                      v-if="model.status === 'ready'"
                      @click.stop="deployModel(model)"
                      variant="success"
                      size="xs"
                      :leftIcon="RocketLaunchIcon"
                    />
                    <Button
                      @click.stop="testModel(model)"
                      variant="ghost"
                      size="xs"
                      :leftIcon="BeakerIcon"
                    />
                    <Button
                      @click.stop="editModel(model)"
                      variant="ghost"
                      size="xs"
                      :leftIcon="PencilIcon"
                    />
                    <Button
                      @click.stop="deleteModel(model)"
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

    <!-- Create Model Modal -->
    <Modal
      :isOpen="showCreateModal"
      @close="showCreateModal = false"
      title="Create New Model"
      size="lg"
    >
      <div class="space-y-6">
        <div class="grid grid-cols-1 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Model Name
            </label>
            <input
              v-model="newModel.name"
              type="text"
              placeholder="Enter model name..."
              class="input-base"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Description
            </label>
            <textarea
              v-model="newModel.description"
              placeholder="Describe your model..."
              rows="3"
              class="input-base"
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              File Path
            </label>
            <input
              v-model="newModel.file_path"
              type="text"
              placeholder="e.g., /models/my-model.pth"
              class="input-base"
            />
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Model file storage path on server</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Version
            </label>
            <input
              v-model="newModel.version"
              type="text"
              placeholder="e.g., v1.0"
              class="input-base"
            />
          </div>
          
          <!-- Model Configuration (JSON) -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
            <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Class Configuration (JSON)
            </h4>
            <textarea
              v-model="newModel.class_config"
              placeholder='{"num_classes": 10, "input_shape": [3, 224, 224]}'
              rows="4"
              class="input-base font-mono text-sm"
            ></textarea>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">JSON configuration for model classes and structure</p>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button @click="showCreateModal = false" variant="secondary">
            Cancel
          </Button>
          <Button 
            @click="createModel" 
            variant="primary"
            :disabled="!canCreateModel"
          >
            Create Model
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Model Details Modal -->
    <Modal
      :isOpen="showDetailsModal"
      @close="showDetailsModal = false"
      :title="`Model Details: ${selectedModel?.name || ''}`"
      size="xl"
    >
      <div v-if="selectedModel" class="space-y-6 px-4">
        <!-- Model Overview -->
        <div class="grid grid-cols-2 gap-8">
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-3">Model Information</h4>
            <div class="text-sm text-gray-600 dark:text-gray-400 space-y-2 pl-2">
              <p><span class="font-medium">Name:</span> {{ selectedModel.name }}</p>
              <p><span class="font-medium">Version:</span> {{ selectedModel.version }}</p>
              <p><span class="font-medium">File Path:</span> {{ selectedModel.file_path }}</p>
              <p><span class="font-medium">Size:</span> {{ formatFileSize(selectedModel.size) }}</p>
              <p><span class="font-medium">Status:</span> {{ selectedModel.status }}</p>
            </div>
          </div>
          
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-3">Performance Metrics</h4>
            <div class="text-sm text-gray-600 dark:text-gray-400 space-y-2 pl-2">
              <p><span class="font-medium">Accuracy:</span> {{ (selectedModel.accuracy * 100).toFixed(2) }}%</p>
              <p><span class="font-medium">Loss:</span> {{ selectedModel.loss ? selectedModel.loss.toFixed(6) : 'N/A' }}</p>
              <p><span class="font-medium">Progress:</span> {{ selectedModel.progress.toFixed(2) }}%</p>
              <p><span class="font-medium">Created:</span> {{ formatDate(selectedModel.created_time) }}</p>
              <p><span class="font-medium">Updated:</span> {{ formatDate(selectedModel.updated_time) }}</p>
            </div>
          </div>
        </div>
        
        <!-- Class Configuration -->
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-3">Class Configuration</h4>
          <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
            <pre class="text-xs font-mono text-gray-800 dark:text-gray-200 overflow-auto">{{ JSON.stringify(selectedModel.class_config, null, 2) }}</pre>
          </div>
        </div>

        <!-- Description -->
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-3">Description</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400 pl-2">{{ selectedModel.description }}</p>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-between">
          <div class="flex space-x-3">
            <Button
              v-if="selectedModel?.status === 'ready'"
              @click="deployModel(selectedModel)"
              variant="success"
              :leftIcon="RocketLaunchIcon"
            >
              Deploy Model
            </Button>
            <Button
              v-else-if="selectedModel?.status === 'deployed'"
              @click="stopModel(selectedModel)"
              variant="warning"
              :leftIcon="StopIcon"
            >
              Stop Deployment
            </Button>
          </div>
          
          <div class="flex space-x-3">
            <Button @click="showDetailsModal = false" variant="secondary">
              Close
            </Button>
            <Button @click="exportModel(selectedModel)" variant="primary">
              Export Model
            </Button>
          </div>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'
import { useP2PAIStore } from '@/stores/p2pai'
import { useErrorBoundary } from '@/composables/useErrorBoundary'
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts'
import { useApiOptimization } from '@/composables/useApiOptimization'
import p2paiService from '@/services/p2paiService'
import performanceMonitor from '@/utils/performanceMonitor'
import {
  ArrowLeftIcon,
  CpuChipIcon,
  SunIcon,
  MoonIcon,
  PlusIcon,
  MagnifyingGlassIcon,
  CloudIcon,
  ArrowPathIcon,
  ChartBarIcon,
  RocketLaunchIcon,
  ArrowDownTrayIcon,
  TrashIcon,
  Squares2X2Icon,
  ListBulletIcon,
  StopIcon,
  BeakerIcon,
  PencilIcon,
  BoltIcon,
  CubeIcon,
  SparklesIcon
} from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import Modal from '@/components/ui/Modal.vue'

const router = useRouter()
const themeStore = useThemeStore()
const uiStore = useUIStore()
const p2paiStore = useP2PAIStore()
const { hasError, retry, captureError } = useErrorBoundary()
const { enableShortcuts, disableShortcuts } = useKeyboardShortcuts()
const { cachedApiCall, clearCache } = useApiOptimization()

// State
const searchQuery = ref('')
const selectedFilter = ref('')
const viewMode = ref('grid')
const selectedModels = ref([])
const showCreateModal = ref(false)
const showDetailsModal = ref(false)
const selectedModel = ref(null)

// New model form
const newModel = ref({
  name: '',
  description: '',
  file_path: '',
  version: '',
  class_config: {}
})

// Real data state
const models = ref([])
const loading = ref({
  models: false,
  operations: false
})
const refreshing = ref(false)

// Computed properties
const filteredModels = computed(() => {
  return models.value.filter(model => {
    const matchesSearch = model.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         model.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesFilter = !selectedFilter.value || model.status === selectedFilter.value
    
    return matchesSearch && matchesFilter
  })
})

const totalModels = computed(() => models.value.length)
const deployedModels = computed(() => models.value.filter(m => m.status === 'deployed').length)
const trainingModels = computed(() => models.value.filter(m => m.status === 'training').length)
const deploymentRate = computed(() => (deployedModels.value / totalModels.value) * 100)
const averageAccuracy = computed(() => {
  const accuracies = models.value.filter(m => m.accuracy).map(m => m.accuracy * 100)
  return accuracies.length > 0 ? accuracies.reduce((sum, acc) => sum + acc, 0) / accuracies.length : 0
})

const canCreateModel = computed(() => {
  return newModel.value.name && newModel.value.description
})

// 🔧 前端硬编码数据 - FRONTEND HARDCODED DATA
// 📁 文件位置: /frontend/src/views/p2pai/ModelDashboard.vue
// ⚠️ 这是前端硬编码的示例模型数据，仅用于展示
// 📋 数据库表: client_models (id, name, description, created_time, updated_time, user_id, project_id, file_path, version, size, class_config, status, progress, loss, accuracy)
const HARDCODED_MODELS = [
  {
    id: 1,
    name: '【前端硬编码】Image Classifier CNN',
    description: '⚠️ 前端硬编码示例数据 - 用于图像分类的卷积神经网络模型，训练于ImageNet数据集',
    file_path: '/models/hardcoded/image_classifier_cnn_v1.pth',
    version: 'v1.0',
    size: 95 * 1024 * 1024, // 95MB
    class_config: { num_classes: 10, input_shape: [3, 224, 224], output_layer: 'softmax' },
    status: 'deployed',
    progress: 100.00,
    loss: 0.045123,
    accuracy: 0.9450,
    created_time: new Date('2024-01-15'),
    updated_time: new Date('2024-03-20')
  }
]

// Real data loading
const loadModels = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('P2PAI-ModelDashboard')
  loading.value.models = true
  
  try {
    // 🔧 使用前端硬编码数据 - Using frontend hardcoded data
    console.warn('⚠️ 使用前端硬编码模型数据 - Using hardcoded model data')
    models.value = [...HARDCODED_MODELS]
    console.log('✅ Models loaded:', models.value)
    console.log('📊 Total models:', models.value.length)
    loading.value.models = false
    pageMonitor.end()
    return
    
    // 以下是实际API调用代码（已禁用）
    const result = await cachedApiCall(
      'p2pai-models', 
      () => p2paiService.models.getModels(), 
      60 * 1000 // Cache for 1 minute
    )
    
    if (result && result.data) {
      models.value = result.data.map(model => ({
        id: model.id,
        name: model.name,
        description: model.description,
        file_path: model.file_path || model.storage_path || model.path || `/models/${model.id}`,
        architecture: model.architecture || 'CNN',
        version: model.version || '1.0',
        parameters: model.parameters || 0,
        size: model.size || 0,
        accuracy: model.accuracy || 0,
        loss: model.loss || 0,
        f1Score: model.f1_score || 0,
        status: model.status || 'ready',
        createdAt: new Date(model.created_at || Date.now()),
        progress: model.progress || 0,
        currentEpoch: model.current_epoch || 0,
        totalEpochs: model.total_epochs || 100,
        inferenceTime: model.inference_time || 0,
        memoryUsage: model.memory_usage || 0,
        endpoint: model.endpoint || '',
        requestsToday: model.requests_today || 0
      }))
    }
    
    pageMonitor.end()
  } catch (error) {
    console.error('Failed to load models:', error)
    captureError(error, null, 'Model loading failed')
    pageMonitor.end()
  } finally {
    loading.value.models = false
  }
}

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const getArchitectureIcon = (architecture) => {
  const icons = {
    CNN: { icon: CubeIcon, bgClass: 'bg-blue-500' },
    RNN: { icon: ArrowPathIcon, bgClass: 'bg-green-500' },
    Transformer: { icon: SparklesIcon, bgClass: 'bg-purple-500' },
    ResNet: { icon: CpuChipIcon, bgClass: 'bg-red-500' },
    LSTM: { icon: ArrowPathIcon, bgClass: 'bg-yellow-500' },
    GAN: { icon: BoltIcon, bgClass: 'bg-pink-500' }
  }
  return icons[architecture] || icons.CNN
}

const getStatusClasses = (status) => {
  const classes = {
    deployed: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    training: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    ready: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return classes[status] || classes.ready
}

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatFileSize = (bytes) => {
  const units = ['B', 'KB', 'MB', 'GB']
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

const toggleModelSelection = (modelId) => {
  const index = selectedModels.value.indexOf(modelId)
  if (index > -1) {
    selectedModels.value.splice(index, 1)
  } else {
    selectedModels.value.push(modelId)
  }
}

const toggleAllSelection = () => {
  if (selectedModels.value.length === filteredModels.value.length) {
    selectedModels.value = []
  } else {
    selectedModels.value = filteredModels.value.map(m => m.id)
  }
}

const selectModel = (model) => {
  selectedModel.value = model
  showDetailsModal.value = true
}

const deployModel = async (model) => {
  loading.value.operations = true
  
  try {
    const result = await p2paiService.models.deployModel(model.id, {
      environment: 'production',
      auto_scale: true
    })
    
    if (result.success) {
      model.status = 'deployed'
      uiStore.addNotification({
        type: 'success',
        title: 'Model Deployed',
        message: `${model.name} has been successfully deployed`,
        duration: 3000
      })
    } else {
      throw new Error(result.error || 'Failed to deploy model')
    }
  } catch (error) {
    console.error('Failed to deploy model:', error)
    captureError(error, null, 'Model deployment failed')
  } finally {
    loading.value.operations = false
  }
}

const stopModel = async (model) => {
  loading.value.operations = true
  
  try {
    const result = await p2paiService.models.stopModel?.(model.id)
    
    if (result?.success) {
      model.status = 'ready'
      uiStore.addNotification({
        type: 'info',
        title: 'Model Stopped',
        message: `${model.name} deployment has been stopped`,
        duration: 3000
      })
    }
  } catch (error) {
    console.error('Failed to stop model:', error)
    captureError(error, null, 'Model stop failed')
  } finally {
    loading.value.operations = false
  }
}

const testModel = (model) => {
  console.log('Testing model:', model.name)
}

const editModel = (model) => {
  console.log('Editing model:', model.name)
}

const deleteModel = (model) => {
  if (confirm(`Are you sure you want to delete "${model.name}"?`)) {
    const index = models.value.findIndex(m => m.id === model.id)
    if (index > -1) {
      models.value.splice(index, 1)
    }
  }
}

const exportModel = (model) => {
  console.log('Exporting model:', model.name)
}

const bulkDeploy = () => {
  selectedModels.value.forEach(modelId => {
    const model = models.value.find(m => m.id === modelId)
    if (model && model.status === 'ready') {
      deployModel(model)
    }
  })
  selectedModels.value = []
}

const bulkDownload = () => {
  console.log('Bulk downloading models:', selectedModels.value)
}

const bulkDelete = () => {
  if (confirm(`Are you sure you want to delete ${selectedModels.value.length} models?`)) {
    models.value = models.value.filter(m => !selectedModels.value.includes(m.id))
    selectedModels.value = []
  }
}

const refreshModels = async () => {
  refreshing.value = true
  clearCache('p2pai-models')
  await loadModels()
  refreshing.value = false
  
  uiStore.addNotification({
    type: 'success',
    title: 'Models Refreshed',
    message: 'Model data has been updated',
    duration: 2000
  })
}

const createModel = async () => {
  if (!canCreateModel.value) return
  
  loading.value.operations = true
  
  try {
    // Parse class_config if it's a string
    let classConfig = newModel.value.class_config
    if (typeof classConfig === 'string') {
      try {
        classConfig = JSON.parse(classConfig)
      } catch (e) {
        classConfig = {}
      }
    }
    
    const modelData = {
      name: newModel.value.name,
      description: newModel.value.description,
      file_path: newModel.value.file_path || `/models/${newModel.value.name.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase()}.pth`,
      version: newModel.value.version || 'v1.0',
      class_config: classConfig
    }
    
    const result = await p2paiService.models.createModel?.(modelData)
    
    if (result?.success) {
      // Reset form
      newModel.value = {
        name: '',
        description: '',
        file_path: '',
        version: '',
        class_config: {}
      }
      
      showCreateModal.value = false
      
      // Refresh models list
      await loadModels()
      
      uiStore.addNotification({
        type: 'success',
        title: 'Model Created',
        message: `${modelData.name} has been created successfully`,
        duration: 3000
      })
    } else {
      throw new Error(result?.error || 'Failed to create model')
    }
  } catch (error) {
    console.error('Failed to create model:', error)
    captureError(error, null, 'Model creation failed')
  } finally {
    loading.value.operations = false
  }
}

// Lifecycle
onMounted(async () => {
  enableShortcuts()
  await loadModels()
  
  uiStore.addNotification({
    type: 'info',
    title: 'Model Dashboard',
    message: 'Model management interface loaded',
    duration: 2000
  })
})

onUnmounted(() => {
  disableShortcuts()
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