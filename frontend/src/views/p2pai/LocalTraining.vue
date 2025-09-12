<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Navigation -->
    <nav class="glass-effect shadow-soft border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors micro-bounce"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            
            <div class="w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center mr-3 micro-bounce hover-glow-primary">
              <ShieldCheckIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gradient text-shadow-soft">
              Local Training
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Device: {{ deviceName }}
            </span>
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-6xl mx-auto px-6 py-8">
      <!-- Page Header -->
      <div class="text-center mb-8 animate-fade-in-up">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Local Model Training
        </h2>
        <p class="text-gray-600 dark:text-gray-400">
          Train AI models using your local data with complete privacy protection
        </p>
      </div>

      <!-- Training Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 stagger-children">
        <StatCard
          title="Training Status"
          :value="trainingStatus"
          :icon="statusIcon"
          :variant="statusVariant"
          description="Current training state"
          clickable
          animated
          @click="viewStatusDetails"
        />
        
        <StatCard
          title="Current Epoch"
          :value="currentEpoch"
          unit="/ 50"
          :icon="ArrowPathIcon"
          variant="primary"
          :progress="epochProgress"
          description="Training epochs"
          animated
        />
        
        <StatCard
          title="Accuracy"
          :value="currentAccuracy"
          unit="%"
          :precision="2"
          :icon="CheckCircleIcon"
          variant="success"
          :trend="accuracyTrend"
          trend-label="improvement"
          description="Model accuracy"
          animated
        />

        <StatCard
          title="Dataset Size"
          :value="datasetSize"
          unit="samples"
          :icon="CircleStackIcon"
          variant="info"
          description="Training samples"
          animated
        />
      </div>

      <!-- Dataset and Model Configuration -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Dataset Configuration -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <CircleStackIcon class="w-5 h-5 mr-2 text-green-500" />
              Dataset Configuration
            </h3>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Select Dataset
                </label>
                <select 
                  v-model="selectedDataset" 
                  class="input-base"
                  @change="onDatasetChange"
                >
                  <option value="">Choose a dataset...</option>
                  <option value="cifar10">CIFAR-10 (Image Classification)</option>
                  <option value="mnist">MNIST (Handwritten Digits)</option>
                  <option value="custom">Custom Dataset</option>
                </select>
              </div>
              
              <div v-if="selectedDataset">
                <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
                  <div class="text-sm space-y-2">
                    <div class="flex justify-between">
                      <span class="text-gray-600 dark:text-gray-400">Total Samples:</span>
                      <span class="font-medium">{{ datasetInfo.totalSamples.toLocaleString() }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-600 dark:text-gray-400">Training Set:</span>
                      <span class="font-medium">{{ datasetInfo.trainingSamples.toLocaleString() }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-600 dark:text-gray-400">Validation Set:</span>
                      <span class="font-medium">{{ datasetInfo.validationSamples.toLocaleString() }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-600 dark:text-gray-400">Test Set:</span>
                      <span class="font-medium">{{ datasetInfo.testSamples.toLocaleString() }}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="selectedDataset === 'custom'">
                <Button 
                  @click="uploadDataset"
                  variant="outline"
                  :leftIcon="CloudArrowUpIcon"
                  class="w-full"
                >
                  Upload Custom Dataset
                </Button>
              </div>

              <!-- Data Split Configuration -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Train/Validation Split: {{ trainSplit }}% / {{ 100 - trainSplit }}%
                </label>
                <input 
                  v-model="trainSplit" 
                  type="range" 
                  min="60" 
                  max="90" 
                  step="5"
                  class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
                />
              </div>
            </div>
          </div>
        </Card>

        <!-- Model Configuration -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <CpuChipIcon class="w-5 h-5 mr-2 text-blue-500" />
              Model Configuration
            </h3>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Model Architecture
                </label>
                <select 
                  v-model="selectedModel" 
                  class="input-base"
                  @change="onModelChange"
                >
                  <option value="cnn">Convolutional Neural Network</option>
                  <option value="resnet">ResNet</option>
                  <option value="vgg">VGG</option>
                  <option value="mobilenet">MobileNet</option>
                </select>
              </div>
              
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Learning Rate
                  </label>
                  <input 
                    v-model="learningRate" 
                    type="number" 
                    step="0.0001" 
                    min="0.0001" 
                    max="1"
                    class="input-base"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Batch Size
                  </label>
                  <input 
                    v-model="batchSize" 
                    type="number" 
                    min="8" 
                    max="512" 
                    step="8"
                    class="input-base"
                  />
                </div>
              </div>
              
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Epochs
                  </label>
                  <input 
                    v-model="maxEpochs" 
                    type="number" 
                    min="10" 
                    max="200"
                    class="input-base"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Optimizer
                  </label>
                  <select v-model="optimizer" class="input-base">
                    <option value="adam">Adam</option>
                    <option value="sgd">SGD</option>
                    <option value="rmsprop">RMSprop</option>
                  </select>
                </div>
              </div>

              <!-- Advanced Options -->
              <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Advanced Options</span>
                  <button 
                    @click="showAdvanced = !showAdvanced"
                    class="text-xs text-blue-600 hover:text-blue-700"
                  >
                    {{ showAdvanced ? 'Hide' : 'Show' }}
                  </button>
                </div>
                
                <div v-if="showAdvanced" class="space-y-3">
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                        Dropout Rate
                      </label>
                      <input 
                        v-model="dropoutRate" 
                        type="number" 
                        step="0.1" 
                        min="0" 
                        max="0.9"
                        class="input-base text-sm"
                      />
                    </div>
                    
                    <div>
                      <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                        Weight Decay
                      </label>
                      <input 
                        v-model="weightDecay" 
                        type="number" 
                        step="0.0001" 
                        min="0"
                        class="input-base text-sm"
                      />
                    </div>
                  </div>
                  
                  <div class="flex items-center">
                    <input 
                      id="early-stopping" 
                      v-model="earlyStopping" 
                      type="checkbox"
                      class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <label for="early-stopping" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                      Enable Early Stopping
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Training Controls and Progress -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Training Controls -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <PlayIcon class="w-5 h-5 mr-2 text-green-500" />
              Training Controls
            </h3>
            
            <div class="space-y-4">
              <div class="flex space-x-3">
                <Button 
                  v-if="!isTraining" 
                  @click="startTraining"
                  variant="primary"
                  :leftIcon="PlayIcon"
                  class="flex-1"
                  :disabled="!canStartTraining"
                >
                  Start Training
                </Button>
                <Button 
                  v-else
                  @click="stopTraining"
                  variant="danger"
                  :leftIcon="StopIcon"
                  class="flex-1"
                >
                  Stop Training
                </Button>
                
                <Button 
                  v-if="isTraining"
                  @click="pauseTraining"
                  variant="warning"
                  :leftIcon="PauseIcon"
                  :disabled="isPaused"
                >
                  {{ isPaused ? 'Paused' : 'Pause' }}
                </Button>
              </div>
              
              <!-- Training Progress -->
              <div class="space-y-3">
                <ProgressBar 
                  :percentage="overallProgress"
                  variant="success"
                  :animated="isTraining"
                  :show-percentage="true"
                />
                <p class="text-xs text-gray-500 dark:text-gray-400 text-center">
                  Overall Training Progress
                </p>
                
                <ProgressBar 
                  :percentage="epochProgress"
                  variant="primary"
                  :animated="isTraining"
                  :show-percentage="true"
                  size="sm"
                />
                <p class="text-xs text-gray-500 dark:text-gray-400 text-center">
                  Current Epoch Progress
                </p>
              </div>
              
              <!-- Quick Stats -->
              <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
                <div class="text-sm text-gray-700 dark:text-gray-300 space-y-2">
                  <div class="flex justify-between">
                    <span>Training Time:</span>
                    <span class="font-medium">{{ formatDuration(trainingDuration) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Current Loss:</span>
                    <span class="font-medium text-red-600">{{ currentLoss.toFixed(4) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Best Accuracy:</span>
                    <span class="font-medium text-green-600">{{ bestAccuracy.toFixed(2) }}%</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Data Privacy:</span>
                    <span class="font-medium text-blue-600">100% Local</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>

        <!-- Real-time Metrics -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <ChartBarIcon class="w-5 h-5 mr-2 text-purple-500" />
              Training Metrics
            </h3>
            
            <div class="space-y-4">
              <!-- Live metrics display -->
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                  <div class="text-sm text-gray-600 dark:text-gray-400">Current Accuracy</div>
                  <div class="text-xl font-bold text-green-600">{{ currentAccuracy.toFixed(2) }}%</div>
                </div>
                
                <div class="text-center p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                  <div class="text-sm text-gray-600 dark:text-gray-400">Current Loss</div>
                  <div class="text-xl font-bold text-red-600">{{ currentLoss.toFixed(4) }}</div>
                </div>
                
                <div class="text-center p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                  <div class="text-sm text-gray-600 dark:text-gray-400">Validation Acc</div>
                  <div class="text-xl font-bold text-blue-600">{{ validationAccuracy.toFixed(2) }}%</div>
                </div>
                
                <div class="text-center p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                  <div class="text-sm text-gray-600 dark:text-gray-400">Learning Rate</div>
                  <div class="text-xl font-bold text-purple-600">{{ learningRate }}</div>
                </div>
              </div>
              
              <!-- Chart placeholder -->
              <div class="h-48 bg-gray-50 dark:bg-slate-700 rounded-lg flex items-center justify-center">
                <div class="text-center">
                  <ChartBarIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
                  <p class="text-gray-500 dark:text-gray-400">Live training charts</p>
                  <p class="text-xs text-gray-400 mt-1">Chart.js integration pending</p>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Model Performance -->
      <Card class="glass-effect">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <BeakerIcon class="w-5 h-5 mr-2 text-orange-500" />
            Model Performance
          </h3>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Training History -->
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Training History</h4>
              <div class="space-y-2">
                <div 
                  v-for="(record, index) in trainingHistory" 
                  :key="index"
                  class="flex items-center justify-between p-2 bg-gray-50 dark:bg-slate-700 rounded"
                >
                  <span class="text-xs text-gray-600 dark:text-gray-400">
                    Epoch {{ record.epoch }}
                  </span>
                  <div class="text-xs">
                    <span class="text-green-600">{{ record.accuracy.toFixed(2) }}%</span>
                    <span class="text-gray-400 mx-1">|</span>
                    <span class="text-red-600">{{ record.loss.toFixed(4) }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- System Resources -->
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">System Resources</h4>
              <div class="space-y-3">
                <div>
                  <div class="flex justify-between text-xs mb-1">
                    <span>CPU Usage</span>
                    <span>{{ cpuUsage }}%</span>
                  </div>
                  <ProgressBar :percentage="cpuUsage" variant="info" size="sm" />
                </div>
                
                <div>
                  <div class="flex justify-between text-xs mb-1">
                    <span>Memory Usage</span>
                    <span>{{ memoryUsage }}%</span>
                  </div>
                  <ProgressBar :percentage="memoryUsage" variant="warning" size="sm" />
                </div>
                
                <div>
                  <div class="flex justify-between text-xs mb-1">
                    <span>GPU Usage</span>
                    <span>{{ gpuUsage }}%</span>
                  </div>
                  <ProgressBar :percentage="gpuUsage" variant="success" size="sm" />
                </div>
              </div>
            </div>
            
            <!-- Model Info -->
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Model Information</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Parameters:</span>
                  <span class="font-medium">{{ formatNumber(modelParams) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Model Size:</span>
                  <span class="font-medium">{{ modelSize }} MB</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">FLOPs:</span>
                  <span class="font-medium">{{ formatNumber(flops) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Inference Time:</span>
                  <span class="font-medium">{{ inferenceTime }}ms</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- Training Details Modal -->
    <Modal
      :isOpen="showTrainingModal"
      @close="showTrainingModal = false"
      title="Training Session Details"
      size="lg"
    >
      <div class="space-y-4">
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Session Information</h4>
          <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
            <p>Session ID: {{ sessionId }}</p>
            <p>Started: {{ formatDateTime(sessionStartTime) }}</p>
            <p>Duration: {{ formatDuration(trainingDuration) }}</p>
            <p>Dataset: {{ selectedDataset || 'Not selected' }}</p>
            <p>Model: {{ selectedModel }}</p>
          </div>
        </div>
        
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Hyperparameters</h4>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p class="text-gray-600 dark:text-gray-400">Learning Rate:</p>
              <p class="font-medium">{{ learningRate }}</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Batch Size:</p>
              <p class="font-medium">{{ batchSize }}</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Optimizer:</p>
              <p class="font-medium">{{ optimizer }}</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Max Epochs:</p>
              <p class="font-medium">{{ maxEpochs }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button @click="showTrainingModal = false" variant="secondary">
            Close
          </Button>
          <Button @click="exportModel" variant="primary">
            Export Model
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import {
  ArrowLeftIcon,
  ShieldCheckIcon,
  
  
  CpuChipIcon,
  CircleStackIcon,
  PlayIcon,
  StopIcon,
  PauseIcon,
  ChartBarIcon,
  BeakerIcon,
  CheckCircleIcon,
  ArrowPathIcon,
  CloudArrowUpIcon
} from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import Modal from '@/components/ui/Modal.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'

const router = useRouter()
const themeStore = useThemeStore()

// Training state
const isTraining = ref(false)
const isPaused = ref(false)
const trainingStatus = ref('Ready')
const currentEpoch = ref(0)
const trainingDuration = ref(0)
const sessionId = ref('LOCAL-2024-001')
const sessionStartTime = ref(new Date())
const deviceName = ref('MacBook-Pro-M1')

// Dataset configuration
const selectedDataset = ref('')
const trainSplit = ref(80)
const datasetSize = ref(0)
const showAdvanced = ref(false)

// Model configuration
const selectedModel = ref('cnn')
const learningRate = ref(0.001)
const batchSize = ref(32)
const maxEpochs = ref(50)
const optimizer = ref('adam')
const dropoutRate = ref(0.2)
const weightDecay = ref(0.0001)
const earlyStopping = ref(true)

// Training metrics
const currentAccuracy = ref(0)
const currentLoss = ref(0)
const validationAccuracy = ref(0)
const bestAccuracy = ref(0)
const accuracyTrend = ref(0)

// System resources
const cpuUsage = ref(45)
const memoryUsage = ref(68)
const gpuUsage = ref(72)

// Model info
const modelParams = ref(1250000)
const modelSize = ref(12.5)
const flops = ref(2400000)
const inferenceTime = ref(15)

// UI state
const showTrainingModal = ref(false)

// Dataset information
const datasetInfo = ref({
  totalSamples: 0,
  trainingSamples: 0,
  validationSamples: 0,
  testSamples: 0
})

// Training history
const trainingHistory = ref([])

// Computed properties
const statusIcon = computed(() => {
  switch (trainingStatus.value) {
    case 'Training': return PlayIcon
    case 'Paused': return PauseIcon
    case 'Completed': return CheckCircleIcon
    case 'Error': return XCircleIcon
    default: return ShieldCheckIcon
  }
})

const statusVariant = computed(() => {
  switch (trainingStatus.value) {
    case 'Training': return 'success'
    case 'Paused': return 'warning'
    case 'Completed': return 'info'
    case 'Error': return 'danger'
    default: return 'default'
  }
})

const epochProgress = computed(() => {
  return (currentEpoch.value / maxEpochs.value) * 100
})

const overallProgress = computed(() => {
  return epochProgress.value * 0.7 + (currentAccuracy.value / 100) * 30
})

const canStartTraining = computed(() => {
  return !isTraining.value && selectedDataset.value && selectedModel.value
})

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const onDatasetChange = () => {
  if (selectedDataset.value) {
    // Simulate loading dataset information
    const datasets = {
      cifar10: {
        totalSamples: 60000,
        trainingSamples: 48000,
        validationSamples: 6000,
        testSamples: 6000
      },
      mnist: {
        totalSamples: 70000,
        trainingSamples: 56000,
        validationSamples: 7000,
        testSamples: 7000
      },
      custom: {
        totalSamples: 0,
        trainingSamples: 0,
        validationSamples: 0,
        testSamples: 0
      }
    }
    
    datasetInfo.value = datasets[selectedDataset.value]
    datasetSize.value = datasetInfo.value.totalSamples
  }
}

const onModelChange = () => {
  // Update model parameters based on selection
  const modelConfigs = {
    cnn: { params: 1250000, size: 12.5, flops: 2400000 },
    resnet: { params: 23500000, size: 94.2, flops: 4100000000 },
    vgg: { params: 138000000, size: 553.4, flops: 15300000000 },
    mobilenet: { params: 4200000, size: 16.9, flops: 569000000 }
  }
  
  const config = modelConfigs[selectedModel.value]
  modelParams.value = config.params
  modelSize.value = config.size
  flops.value = config.flops
}

const uploadDataset = () => {
  // Implementation for dataset upload
  console.log('Uploading custom dataset...')
}

const startTraining = async () => {
  if (!canStartTraining.value) return
  
  isTraining.value = true
  trainingStatus.value = 'Training'
  sessionStartTime.value = new Date()
  currentEpoch.value = 0
  trainingHistory.value = []
  
  // Simulate training progress
  const trainingInterval = setInterval(() => {
    if (!isTraining.value || isPaused.value) return
    
    trainingDuration.value += 1000
    
    // Simulate epoch completion
    if (Math.random() > 0.8) {
      currentEpoch.value++
      const newAccuracy = Math.min(95, 20 + Math.log(currentEpoch.value) * 15 + Math.random() * 5)
      const newLoss = Math.max(0.01, 2.5 * Math.exp(-currentEpoch.value * 0.1) + Math.random() * 0.1)
      
      currentAccuracy.value = newAccuracy
      currentLoss.value = newLoss
      validationAccuracy.value = newAccuracy - Math.random() * 3
      
      if (newAccuracy > bestAccuracy.value) {
        accuracyTrend.value = ((newAccuracy - bestAccuracy.value) / bestAccuracy.value * 100)
        bestAccuracy.value = newAccuracy
      }
      
      // Add to history
      trainingHistory.value.unshift({
        epoch: currentEpoch.value,
        accuracy: newAccuracy,
        loss: newLoss,
        timestamp: new Date()
      })
      
      // Keep only last 10 records
      if (trainingHistory.value.length > 10) {
        trainingHistory.value = trainingHistory.value.slice(0, 10)
      }
      
      // Simulate resource usage changes
      cpuUsage.value = 40 + Math.random() * 30
      memoryUsage.value = 60 + Math.random() * 25
      gpuUsage.value = 70 + Math.random() * 25
    }
    
    if (currentEpoch.value >= maxEpochs.value) {
      stopTraining()
      trainingStatus.value = 'Completed'
    }
  }, 1000)
}

const stopTraining = () => {
  isTraining.value = false
  isPaused.value = false
  trainingStatus.value = 'Ready'
}

const pauseTraining = () => {
  isPaused.value = !isPaused.value
  trainingStatus.value = isPaused.value ? 'Paused' : 'Training'
}

const viewStatusDetails = () => {
  showTrainingModal.value = true
}

const exportModel = () => {
  console.log('Exporting trained model...')
}

const formatDuration = (ms) => {
  const seconds = Math.floor(ms / 1000) % 60
  const minutes = Math.floor(ms / (1000 * 60)) % 60
  const hours = Math.floor(ms / (1000 * 60 * 60))
  
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

const formatDateTime = (date) => {
  return date.toLocaleString()
}

const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

// Watch for dataset split changes
watch(trainSplit, (newSplit) => {
  if (selectedDataset.value && datasetInfo.value.totalSamples > 0) {
    const total = datasetInfo.value.totalSamples
    datasetInfo.value.trainingSamples = Math.floor(total * newSplit / 100)
    datasetInfo.value.validationSamples = Math.floor(total * (100 - newSplit) / 100)
  }
})

// Lifecycle
onMounted(() => {
  // Initialize default values
  currentAccuracy.value = 0
  currentLoss.value = 2.5
  validationAccuracy.value = 0
})

onUnmounted(() => {
  if (isTraining.value) {
    stopTraining()
  }
})
</script>

<style scoped>
input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
}
</style>