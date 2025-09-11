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
          animated
        />
        
        <StatCard
          title="Deployed Models"
          :value="deployedModels"
          :icon="CloudIcon"
          variant="success"
          :progress="deploymentRate"
          description="Active deployments"
          animated
        />
        
        <StatCard
          title="Training Models"
          :value="trainingModels"
          :icon="ArrowPathIcon"
          variant="warning"
          description="Currently training"
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
                <div 
                  :class="[
                    'w-12 h-12 rounded-lg flex items-center justify-center',
                    getArchitectureIcon(model.architecture).bgClass
                  ]"
                >
                  <component :is="getArchitectureIcon(model.architecture).icon" class="w-6 h-6 text-white" />
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ model.name }}
                  </h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">
                    {{ model.architecture }} • v{{ model.version }}
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
                <span class="font-medium text-green-600">{{ model.accuracy.toFixed(2) }}%</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Parameters:</span>
                <span class="font-medium">{{ formatNumber(model.parameters) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Size:</span>
                <span class="font-medium">{{ formatFileSize(model.size) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Created:</span>
                <span class="font-medium">{{ formatDate(model.createdAt) }}</span>
              </div>
            </div>

            <!-- Performance Chart Placeholder -->
            <div class="h-20 bg-gray-50 dark:bg-slate-700 rounded-lg mb-4 flex items-center justify-center">
              <ChartBarIcon class="w-8 h-8 text-gray-400" />
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
                Training: Epoch {{ model.currentEpoch }} / {{ model.totalEpochs }}
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
                  Architecture
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Accuracy
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Parameters
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
                    <div 
                      :class="[
                        'w-8 h-8 rounded-lg flex items-center justify-center mr-3',
                        getArchitectureIcon(model.architecture).bgClass
                      ]"
                    >
                      <component :is="getArchitectureIcon(model.architecture).icon" class="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-900 dark:text-white">
                        {{ model.name }}
                      </div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">
                        v{{ model.version }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ model.architecture }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  <span class="text-green-600 font-medium">{{ model.accuracy.toFixed(2) }}%</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                  {{ formatNumber(model.parameters) }}
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
                  {{ formatDate(model.createdAt) }}
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
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Architecture
              </label>
              <select v-model="newModel.architecture" class="input-base">
                <option value="CNN">Convolutional Neural Network</option>
                <option value="RNN">Recurrent Neural Network</option>
                <option value="Transformer">Transformer</option>
                <option value="ResNet">ResNet</option>
                <option value="LSTM">LSTM</option>
                <option value="GAN">Generative Adversarial Network</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Task Type
              </label>
              <select v-model="newModel.taskType" class="input-base">
                <option value="classification">Classification</option>
                <option value="regression">Regression</option>
                <option value="detection">Object Detection</option>
                <option value="segmentation">Segmentation</option>
                <option value="nlp">Natural Language Processing</option>
                <option value="generation">Generation</option>
              </select>
            </div>
          </div>
          
          <!-- Model Configuration -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
            <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Model Configuration
            </h4>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                  Input Shape
                </label>
                <input
                  v-model="newModel.inputShape"
                  type="text"
                  placeholder="e.g., (224, 224, 3)"
                  class="input-base text-sm"
                />
              </div>
              
              <div>
                <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                  Output Classes
                </label>
                <input
                  v-model="newModel.outputClasses"
                  type="number"
                  min="1"
                  class="input-base text-sm"
                />
              </div>
            </div>
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
      <div v-if="selectedModel" class="space-y-6">
        <!-- Model Overview -->
        <div class="grid grid-cols-2 gap-6">
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Model Information</h4>
            <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
              <p>Architecture: {{ selectedModel.architecture }}</p>
              <p>Version: v{{ selectedModel.version }}</p>
              <p>Parameters: {{ formatNumber(selectedModel.parameters) }}</p>
              <p>Size: {{ formatFileSize(selectedModel.size) }}</p>
              <p>Status: {{ selectedModel.status }}</p>
            </div>
          </div>
          
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Performance Metrics</h4>
            <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
              <p>Accuracy: {{ selectedModel.accuracy.toFixed(2) }}%</p>
              <p>Loss: {{ selectedModel.loss?.toFixed(4) || 'N/A' }}</p>
              <p>F1 Score: {{ selectedModel.f1Score?.toFixed(3) || 'N/A' }}</p>
              <p>Inference Time: {{ selectedModel.inferenceTime || 'N/A' }}ms</p>
              <p>Memory Usage: {{ selectedModel.memoryUsage || 'N/A' }} MB</p>
            </div>
          </div>
        </div>
        
        <!-- Performance Chart -->
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Training History</h4>
          <div class="h-64 bg-gray-50 dark:bg-slate-700 rounded-lg flex items-center justify-center">
            <div class="text-center">
              <ChartBarIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p class="text-gray-500 dark:text-gray-400">Training metrics chart</p>
              <p class="text-xs text-gray-400 mt-1">Chart.js integration pending</p>
            </div>
          </div>
        </div>

        <!-- Model Deployment Info -->
        <div v-if="selectedModel.status === 'deployed'">
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Deployment Information</h4>
          <div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
            <div class="text-sm space-y-2">
              <div class="flex justify-between">
                <span class="text-green-700 dark:text-green-300">Endpoint:</span>
                <span class="font-mono text-green-800 dark:text-green-200">{{ selectedModel.endpoint || '/api/model/' + selectedModel.id }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-green-700 dark:text-green-300">Requests Today:</span>
                <span class="font-medium text-green-800 dark:text-green-200">{{ selectedModel.requestsToday || Math.floor(Math.random() * 1000) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-green-700 dark:text-green-300">Avg Response Time:</span>
                <span class="font-medium text-green-800 dark:text-green-200">{{ selectedModel.avgResponseTime || Math.floor(Math.random() * 100) + 50 }}ms</span>
              </div>
            </div>
          </div>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
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
  architecture: 'CNN',
  taskType: 'classification',
  inputShape: '',
  outputClasses: 10
})

// Mock model data
const models = ref([
  {
    id: 1,
    name: 'Image Classifier v2.1',
    description: 'Advanced CNN for image classification',
    architecture: 'ResNet',
    version: '2.1',
    parameters: 25600000,
    size: 98304000,
    accuracy: 94.2,
    loss: 0.156,
    f1Score: 0.941,
    status: 'deployed',
    createdAt: new Date('2024-01-15'),
    progress: 100,
    currentEpoch: 50,
    totalEpochs: 50,
    inferenceTime: 12,
    memoryUsage: 256,
    endpoint: '/api/models/image-classifier',
    requestsToday: 1245
  },
  {
    id: 2,
    name: 'Sentiment Analyzer',
    description: 'BERT-based sentiment analysis model',
    architecture: 'Transformer',
    version: '1.3',
    parameters: 110000000,
    size: 440000000,
    accuracy: 91.8,
    loss: 0.203,
    f1Score: 0.915,
    status: 'training',
    createdAt: new Date('2024-02-10'),
    progress: 68,
    currentEpoch: 34,
    totalEpochs: 50,
    inferenceTime: 25,
    memoryUsage: 512
  },
  {
    id: 3,
    name: 'Object Detector',
    description: 'YOLOv5 for real-time object detection',
    architecture: 'CNN',
    version: '3.0',
    parameters: 46200000,
    size: 184800000,
    accuracy: 87.5,
    loss: 0.284,
    f1Score: 0.872,
    status: 'ready',
    createdAt: new Date('2024-01-25'),
    progress: 100,
    currentEpoch: 100,
    totalEpochs: 100,
    inferenceTime: 18,
    memoryUsage: 384
  },
  {
    id: 4,
    name: 'Speech Recognizer',
    description: 'Deep speech recognition model',
    architecture: 'RNN',
    version: '1.0',
    parameters: 78000000,
    size: 312000000,
    accuracy: 89.3,
    status: 'error',
    createdAt: new Date('2024-02-01'),
    progress: 0,
    currentEpoch: 0,
    totalEpochs: 75
  },
  {
    id: 5,
    name: 'GAN Generator',
    description: 'StyleGAN for image generation',
    architecture: 'GAN',
    version: '2.0',
    parameters: 95000000,
    size: 380000000,
    accuracy: 92.7,
    status: 'deployed',
    createdAt: new Date('2024-01-30'),
    progress: 100,
    currentEpoch: 200,
    totalEpochs: 200,
    inferenceTime: 45,
    memoryUsage: 768,
    requestsToday: 856
  }
])

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
  const accuracies = models.value.filter(m => m.accuracy).map(m => m.accuracy)
  return accuracies.length > 0 ? accuracies.reduce((sum, acc) => sum + acc, 0) / accuracies.length : 0
})

const canCreateModel = computed(() => {
  return newModel.value.name && newModel.value.description
})

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

const deployModel = (model) => {
  model.status = 'deployed'
  console.log('Deploying model:', model.name)
}

const stopModel = (model) => {
  model.status = 'ready'
  console.log('Stopping model:', model.name)
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

const refreshModels = () => {
  console.log('Refreshing models...')
}

const createModel = async () => {
  if (!canCreateModel.value) return
  
  const model = {
    id: models.value.length + 1,
    name: newModel.value.name,
    description: newModel.value.description,
    architecture: newModel.value.architecture,
    version: '1.0',
    parameters: Math.floor(Math.random() * 50000000) + 1000000,
    size: Math.floor(Math.random() * 200000000) + 10000000,
    accuracy: Math.random() * 20 + 75,
    status: 'training',
    createdAt: new Date(),
    progress: 0,
    currentEpoch: 0,
    totalEpochs: 50
  }
  
  models.value.push(model)
  
  // Reset form
  newModel.value = {
    name: '',
    description: '',
    architecture: 'CNN',
    taskType: 'classification',
    inputShape: '',
    outputClasses: 10
  }
  
  showCreateModal.value = false
  
  // Simulate training
  const trainingInterval = setInterval(() => {
    if (model.status !== 'training') {
      clearInterval(trainingInterval)
      return
    }
    
    model.progress += Math.random() * 5
    model.currentEpoch = Math.floor((model.progress / 100) * model.totalEpochs)
    
    if (model.progress >= 100) {
      model.status = 'ready'
      model.progress = 100
      model.currentEpoch = model.totalEpochs
      clearInterval(trainingInterval)
    }
  }, 1000)
}

// Lifecycle
onMounted(() => {
  // Initialize component
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