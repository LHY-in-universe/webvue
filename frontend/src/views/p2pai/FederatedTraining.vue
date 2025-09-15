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
              <UsersIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gradient text-shadow-soft">
              Federated Learning Training
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Node: {{ nodeId }}
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
          Federated Training Session
        </h2>
        <p class="text-gray-600 dark:text-gray-400">
          Participate in collaborative model training while preserving data privacy
        </p>
      </div>

      <!-- Training Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 stagger-children">
        <StatCard
          title="Training Status"
          :value="trainingStatus"
          :icon="statusIcon"
          :variant="statusVariant"
          description="Current session status"
          clickable
          animated
          @click="viewStatusDetails"
        />
        
        <StatCard
          title="Current Round"
          :value="currentRound"
          unit="/ 100"
          :icon="ArrowPathIcon"
          variant="primary"
          :progress="roundProgress"
          description="Training progress"
          animated
        />
        
        <StatCard
          title="Connected Nodes"
          :value="connectedNodes"
          :icon="ServerIcon"
          variant="success"
          :trend="nodesTrend"
          trend-label="vs last round"
          description="Active participants"
          animated
        />
      </div>

      <!-- Training Configuration -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
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
                  <option value="cnn">Convolutional Neural Network (CNN)</option>
                  <option value="rnn">Recurrent Neural Network (RNN)</option>
                  <option value="lstm">Long Short-Term Memory (LSTM)</option>
                  <option value="transformer">Transformer</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Learning Rate: {{ learningRate }}
                </label>
                <input 
                  v-model="learningRate" 
                  type="range" 
                  min="0.001" 
                  max="0.1" 
                  step="0.001"
                  class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
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
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Local Epochs
                </label>
                <input 
                  v-model="localEpochs" 
                  type="number" 
                  min="1" 
                  max="20"
                  class="input-base"
                />
              </div>
            </div>
          </div>
        </Card>

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
              
              <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
                <div class="text-sm text-gray-700 dark:text-gray-300 space-y-2">
                  <div class="flex justify-between">
                    <span>Training Time:</span>
                    <span class="font-medium">{{ formatDuration(trainingDuration) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Current Accuracy:</span>
                    <span class="font-medium text-green-600">{{ currentAccuracy.toFixed(2) }}%</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Loss Value:</span>
                    <span class="font-medium text-red-600">{{ currentLoss.toFixed(4) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Data Privacy:</span>
                    <span class="font-medium text-blue-600">Protected</span>
                  </div>
                </div>
              </div>
              
              <ProgressBar 
                :percentage="overallProgress"
                variant="success"
                :animated="isTraining"
                :show-percentage="true"
              />
              <p class="text-xs text-gray-500 dark:text-gray-400 text-center">
                Overall Training Progress
              </p>
            </div>
          </div>
        </Card>
      </div>

      <!-- Training Metrics -->
      <Card class="glass-effect mb-8">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <ChartBarIcon class="w-5 h-5 mr-2 text-purple-500" />
            Training Metrics
          </h3>
          
          <div class="h-64 bg-gray-50 dark:bg-slate-700 rounded-lg flex items-center justify-center">
            <div class="text-center">
              <ChartBarIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p class="text-gray-500 dark:text-gray-400">Training charts will be displayed here</p>
              <p class="text-xs text-gray-400 mt-1">Chart.js integration coming soon</p>
            </div>
          </div>
        </div>
      </Card>

      <!-- Network Status -->
      <Card class="glass-effect">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <GlobeAltIcon class="w-5 h-5 mr-2 text-cyan-500" />
            Network Status
          </h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Connected Nodes</h4>
              <div class="space-y-2">
                <div 
                  v-for="node in networkNodes" 
                  :key="node.id"
                  class="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-700 rounded-lg"
                >
                  <div class="flex items-center">
                    <div :class="[
                      'w-3 h-3 rounded-full mr-3',
                      node.status === 'online' ? 'bg-green-500' : 
                      node.status === 'training' ? 'bg-blue-500' : 'bg-red-500'
                    ]"></div>
                    <span class="text-sm font-medium">{{ node.name }}</span>
                  </div>
                  <span class="text-xs text-gray-500 capitalize">{{ node.status }}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Communication Stats</h4>
              <div class="space-y-3">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600 dark:text-gray-400">Messages Sent:</span>
                  <span class="font-medium">{{ messagesSent.toLocaleString() }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600 dark:text-gray-400">Messages Received:</span>
                  <span class="font-medium">{{ messagesReceived.toLocaleString() }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600 dark:text-gray-400">Network Latency:</span>
                  <span class="font-medium">{{ networkLatency }}ms</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600 dark:text-gray-400">Data Transferred:</span>
                  <span class="font-medium">{{ formatDataSize(dataTransferred) }}</span>
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
          </div>
        </div>
        
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Performance Metrics</h4>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p class="text-gray-600 dark:text-gray-400">Current Accuracy:</p>
              <p class="font-medium text-green-600">{{ currentAccuracy.toFixed(2) }}%</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Best Accuracy:</p>
              <p class="font-medium text-green-600">{{ bestAccuracy.toFixed(2) }}%</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Current Loss:</p>
              <p class="font-medium text-red-600">{{ currentLoss.toFixed(4) }}</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Best Loss:</p>
              <p class="font-medium text-red-600">{{ bestLoss.toFixed(4) }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button @click="showTrainingModal = false" variant="secondary">
            Close
          </Button>
          <Button @click="exportTrainingLog" variant="primary">
            Export Log
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
  UsersIcon,
  
  
  CpuChipIcon,
  PlayIcon,
  StopIcon,
  PauseIcon,
  ChartBarIcon,
  GlobeAltIcon,
  ArrowPathIcon,
  ServerIcon
} from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import Modal from '@/components/ui/Modal.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'

const router = useRouter()
const themeStore = useThemeStore()
const { cachedApiCall } = useApiOptimization()

// API loading state
const apiLoading = ref(false)
const apiError = ref(null)

// Training state
const isTraining = ref(false)
const isPaused = ref(false)
const trainingStatus = ref('Ready')
const currentRound = ref(0)
const trainingDuration = ref(0)
const sessionId = ref(null)
const sessionStartTime = ref(null)
const federatedWebSocket = ref(null)

// Training configuration
const selectedModel = ref('cnn')
const learningRate = ref(0.001)
const batchSize = ref(32)
const localEpochs = ref(5)

// Metrics
const currentAccuracy = ref(0)
const currentLoss = ref(0)
const bestAccuracy = ref(0)
const bestLoss = ref(Infinity)
const connectedNodes = ref(8)
const nodesTrend = ref(12.5)

// Network stats
const messagesSent = ref(1247)
const messagesReceived = ref(1189)
const networkLatency = ref(45)
const dataTransferred = ref(2048576)

// UI state
const showTrainingModal = ref(false)
const nodeId = ref('Node-001')

// Computed properties
const statusIcon = computed(() => {
  switch (trainingStatus.value) {
    case 'Training': return PlayIcon
    case 'Paused': return PauseIcon
    case 'Completed': return CheckCircleIcon
    case 'Error': return XCircleIcon
    default: return CpuChipIcon
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

const roundProgress = computed(() => {
  return (currentRound.value / 100) * 100
})

const overallProgress = computed(() => {
  return roundProgress.value * 0.6 + (currentAccuracy.value / 100) * 40
})

const canStartTraining = computed(() => {
  return !isTraining.value && connectedNodes.value >= 2
})

const networkNodes = ref([
  { id: 1, name: 'Node-001', status: 'training' },
  { id: 2, name: 'Node-002', status: 'online' },
  { id: 3, name: 'Node-003', status: 'training' },
  { id: 4, name: 'Node-004', status: 'online' },
  { id: 5, name: 'Node-005', status: 'offline' },
  { id: 6, name: 'Node-006', status: 'online' },
])

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const startTraining = async () => {
  if (!canStartTraining.value) return
  
  apiLoading.value = true
  apiError.value = null
  
  try {
    // Prepare federated training configuration
    const federatedConfig = {
      model_architecture: selectedModel.value,
      hyperparameters: {
        learning_rate: learningRate.value,
        batch_size: batchSize.value,
        local_epochs: localEpochs.value,
        max_rounds: 100
      },
      node_selection: {
        min_nodes: threshold.value || 2,
        max_nodes: totalParties.value || 10
      }
    }
    
    console.log('🌐 Starting federated training with config:', federatedConfig)
    
    // Start federated training via API
    const response = await p2paiService.training.startFederatedTraining(federatedConfig)
    
    if (response.success) {
      // Update state with real session data
      sessionId.value = response.data.session_id
      sessionStartTime.value = new Date(response.data.start_time)
      isTraining.value = true
      trainingStatus.value = 'Training'
      currentRound.value = 0
      
      // Setup WebSocket connection for real-time updates
      setupFederatedWebSocket(sessionId.value)
      
      console.log('✅ Federated training started successfully:', response.data)
    } else {
      throw new Error(response.error || 'Failed to start federated training')
    }
  } catch (err) {
    console.error('❌ Failed to start federated training:', err)
    apiError.value = err.message || 'Failed to start federated training'
    trainingStatus.value = 'Error'
  } finally {
    apiLoading.value = false
  }
}

const stopTraining = async () => {
  if (!sessionId.value) {
    // Local stop for simulation mode
    isTraining.value = false
    isPaused.value = false
    trainingStatus.value = 'Ready'
    return
  }
  
  try {
    console.log('🛑 Stopping federated training session:', sessionId.value)
    
    const response = await p2paiService.training.stopTraining(sessionId.value)
    
    if (response.success) {
      isTraining.value = false
      isPaused.value = false
      trainingStatus.value = 'Stopped'
      
      // Close WebSocket connection
      if (federatedWebSocket.value) {
        federatedWebSocket.value.close()
        federatedWebSocket.value = null
      }
      
      console.log('✅ Federated training stopped successfully')
    }
  } catch (err) {
    console.error('❌ Failed to stop federated training:', err)
    // Still update local state even if API call fails
    isTraining.value = false
    isPaused.value = false
    trainingStatus.value = 'Error'
  }
}

const pauseTraining = () => {
  isPaused.value = !isPaused.value
  trainingStatus.value = isPaused.value ? 'Paused' : 'Training'
}

const viewStatusDetails = () => {
  showTrainingModal.value = true
}

const onModelChange = () => {
  console.log('Model changed to:', selectedModel.value)
}

const exportTrainingLog = () => {
  // Implementation for exporting training logs
  console.log('Exporting training log...')
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

const formatDataSize = (bytes) => {
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  
  return `${size.toFixed(2)} ${units[unitIndex]}`
}

// Setup WebSocket connection for real-time federated updates
const setupFederatedWebSocket = (sessionId) => {
  if (federatedWebSocket.value) {
    federatedWebSocket.value.close()
  }
  
  try {
    federatedWebSocket.value = p2paiService.training.createTrainingWebSocket(sessionId, {
      onOpen: () => {
        console.log('📡 Federated WebSocket connected')
      },
      onMessage: (data) => {
        console.log('📨 Federated update received:', data)
        updateFederatedMetrics(data)
      },
      onError: (error) => {
        console.error('❌ Federated WebSocket error:', error)
      },
      onClose: () => {
        console.log('🔌 Federated WebSocket closed')
        if (isTraining.value) {
          // Try to reconnect after 3 seconds
          setTimeout(() => setupFederatedWebSocket(sessionId), 3000)
        }
      }
    })
  } catch (err) {
    console.error('Failed to setup federated WebSocket:', err)
  }
}

// Update federated metrics from WebSocket data
const updateFederatedMetrics = (data) => {
  if (data.type === 'federated_round') {
    currentRound.value = data.round || currentRound.value
    currentAccuracy.value = data.accuracy || currentAccuracy.value
    currentLoss.value = data.loss || currentLoss.value
    connectedNodes.value = data.connected_nodes || connectedNodes.value
    
    if (data.accuracy > bestAccuracy.value) {
      bestAccuracy.value = data.accuracy
    }
    if (data.loss < bestLoss.value) {
      bestLoss.value = data.loss
    }
    
    // Update node information
    if (data.nodes) {
      networkNodes.value = data.nodes.map(node => ({
        id: node.id,
        name: node.name,
        status: node.status
      }))
    }
  } else if (data.type === 'federated_completed') {
    trainingStatus.value = 'Completed'
    isTraining.value = false
    isPaused.value = false
  } else if (data.type === 'federated_error') {
    trainingStatus.value = 'Error'
    apiError.value = data.message || 'Federated training error occurred'
    isTraining.value = false
    isPaused.value = false
  }
}

// Load connected nodes data
const loadNodesData = async () => {
  try {
    const nodesResponse = await cachedApiCall(
      'federated-nodes',
      () => p2paiService.nodes.getNodes({ type: 'federated' }),
      30 * 1000 // 30 second cache
    )
    
    if (nodesResponse.data?.nodes) {
      networkNodes.value = nodesResponse.data.nodes.map(node => ({
        id: node.id,
        name: node.name,
        status: node.status || 'offline'
      }))
      connectedNodes.value = networkNodes.value.filter(n => n.status === 'online' || n.status === 'training').length
    }
  } catch (err) {
    console.warn('Failed to load nodes data:', err)
  }
}

// Lifecycle
onMounted(async () => {
  console.log('🌐 Federated Training component mounted')
  
  // Initialize default values
  currentAccuracy.value = 0
  currentLoss.value = 2.5
  bestLoss.value = 2.5
  
  // Load initial nodes data
  await loadNodesData()
})

onUnmounted(() => {
  console.log('🧹 Cleaning up Federated Training component')
  
  // Close WebSocket connection
  if (federatedWebSocket.value) {
    federatedWebSocket.value.close()
    federatedWebSocket.value = null
  }
  
  // Stop training if active
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