<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Header -->
    <nav class="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button @click="goBack" class="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg">
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">Local Training</h1>
          </div>
          <SimpleThemeToggle size="sm" />
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Status Bar -->
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4 mb-6 flex items-center justify-between">
        <div class="flex items-center gap-6">
          <div>
            <div class="text-sm text-gray-500 dark:text-gray-400">Status</div>
            <div class="font-medium" :class="statusColor">{{ trainingStatus }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 dark:text-gray-400">Epoch</div>
            <div class="font-medium">{{ currentEpoch }} / {{ maxEpochs }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 dark:text-gray-400">Accuracy</div>
            <div class="font-medium text-green-600">{{ currentAccuracy.toFixed(2) }}%</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 dark:text-gray-400">Loss</div>
            <div class="font-medium text-red-600">{{ currentLoss.toFixed(4) }}</div>
          </div>
        </div>
        <div class="flex gap-2">
          <Button v-if="!isTraining" @click="startTraining" variant="primary" :disabled="!canStartTraining">
            Start Training
          </Button>
          <Button v-else @click="stopTraining" variant="danger">
            Stop
          </Button>
        </div>
      </div>

      <!-- Configuration -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Project & Dataset -->
        <div class="bg-white dark:bg-slate-800 rounded-lg p-6">
          <h3 class="font-semibold mb-4">Project Configuration</h3>
          <div class="space-y-4">
            <div>
              <label class="text-sm text-gray-600 dark:text-gray-400">Project Name</label>
              <input v-model="projectName" type="text" class="input-base" :disabled="isTraining" placeholder="Enter project name" />
            </div>
            <div>
              <label class="text-sm text-gray-600 dark:text-gray-400">Dataset</label>
              <select v-model="selectedDataset" class="input-base" @change="onDatasetChange" :disabled="isTraining">
                <option value="">Select dataset...</option>
                <option value="cifar10">CIFAR-10</option>
                <option value="mnist">MNIST</option>
                <option value="custom">Custom</option>
              </select>
            </div>
            <div v-if="selectedDataset">
              <div class="text-sm space-y-1 bg-slate-50 dark:bg-slate-700 p-3 rounded">
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Total:</span>
                  <span>{{ datasetInfo.totalSamples.toLocaleString() }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600 dark:text-gray-400">Train/Val Split:</span>
                  <span>{{ trainSplit }}% / {{ 100 - trainSplit }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Model Configuration -->
        <div class="bg-white dark:bg-slate-800 rounded-lg p-6">
          <h3 class="font-semibold mb-4">Model Configuration</h3>
          <div class="space-y-4">
            <div>
              <label class="text-sm text-gray-600 dark:text-gray-400">Model</label>
              <select v-model="selectedModel" class="input-base" @change="onModelChange" :disabled="isTraining">
                <option value="cnn">CNN</option>
                <option value="resnet">ResNet</option>
                <option value="vgg">VGG</option>
                <option value="mobilenet">MobileNet</option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Learning Rate</label>
                <input v-model="learningRate" type="number" step="0.0001" class="input-base" :disabled="isTraining" />
              </div>
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Batch Size</label>
                <input v-model="batchSize" type="number" class="input-base" :disabled="isTraining" />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Epochs</label>
                <input v-model="maxEpochs" type="number" class="input-base" :disabled="isTraining" />
              </div>
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Optimizer</label>
                <select v-model="optimizer" class="input-base" :disabled="isTraining">
                  <option value="adam">Adam</option>
                  <option value="sgd">SGD</option>
                  <option value="rmsprop">RMSprop</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress -->
      <div v-if="isTraining" class="bg-white dark:bg-slate-800 rounded-lg p-6 mb-6">
        <h3 class="font-semibold mb-4">Training Progress</h3>
        <ProgressBar :percentage="epochProgress" :animated="true" class="mb-2" />
        <div class="text-sm text-gray-600 dark:text-gray-400 text-center">
          Epoch {{ currentEpoch }} / {{ maxEpochs }} - {{ epochProgress.toFixed(1) }}%
        </div>
      </div>

      <!-- Metrics Grid -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
          <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Accuracy</div>
          <div class="text-2xl font-bold text-green-600">{{ currentAccuracy.toFixed(2) }}%</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
          <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Loss</div>
          <div class="text-2xl font-bold text-red-600">{{ currentLoss.toFixed(4) }}</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
          <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Val Accuracy</div>
          <div class="text-2xl font-bold text-blue-600">{{ validationAccuracy.toFixed(2) }}%</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
          <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Duration</div>
          <div class="text-2xl font-bold">{{ formatDuration(trainingDuration) }}</div>
        </div>
      </div>

      <!-- Training History -->
      <div v-if="trainingHistory.length > 0" class="bg-white dark:bg-slate-800 rounded-lg p-6">
        <h3 class="font-semibold mb-4">Training History</h3>
        <div class="space-y-2">
          <div v-for="(record, index) in trainingHistory.slice(0, 5)" :key="index"
               class="flex justify-between items-center p-3 bg-slate-50 dark:bg-slate-700 rounded">
            <span class="text-sm">Epoch {{ record.epoch }}</span>
            <div class="flex gap-4 text-sm">
              <span class="text-green-600">Acc: {{ record.accuracy.toFixed(2) }}%</span>
              <span class="text-red-600">Loss: {{ record.loss.toFixed(4) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useApiOptimization } from '@/composables/useApiOptimization.js'
import p2paiService from '@/services/p2paiService.js'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'

const router = useRouter()
const { cachedApiCall } = useApiOptimization()

// Project information
const projectName = ref('')
const trainingAlg = ref('Adam')

// Training state
const isTraining = ref(false)
const trainingStatus = ref('Ready')
const currentEpoch = ref(0)
const trainingDuration = ref(0)
const sessionId = ref(null)
const sessionStartTime = ref(null)
const trainingWebSocket = ref(null)

// Dataset configuration
const selectedDataset = ref('')
const trainSplit = ref(80)

// Model configuration
const selectedModel = ref('cnn')
const learningRate = ref(0.001)
const batchSize = ref(32)
const maxEpochs = ref(50)
const optimizer = ref('adam')

// Training metrics
const currentAccuracy = ref(0)
const currentLoss = ref(0)
const validationAccuracy = ref(0)
const bestAccuracy = ref(0)

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
const statusColor = computed(() => {
  switch (trainingStatus.value) {
    case 'Training': return 'text-green-600'
    case 'Completed': return 'text-blue-600'
    case 'Error': return 'text-red-600'
    default: return 'text-gray-600 dark:text-gray-400'
  }
})

const epochProgress = computed(() => {
  return (currentEpoch.value / maxEpochs.value) * 100
})

const canStartTraining = computed(() => {
  return !isTraining.value && projectName.value.trim() !== '' && selectedDataset.value && selectedModel.value
})

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const onDatasetChange = async () => {
  if (selectedDataset.value) {
    try {
      const datasetStats = await cachedApiCall(
        `dataset-${selectedDataset.value}`,
        () => p2paiService.datasets.getDatasets({ name: selectedDataset.value }),
        5 * 60 * 1000
      )

      if (datasetStats.data && datasetStats.data.length > 0) {
        const dataset = datasetStats.data[0]
        datasetInfo.value = {
          totalSamples: dataset.total_samples || 0,
          trainingSamples: Math.floor((dataset.total_samples || 0) * trainSplit.value / 100),
          validationSamples: Math.floor((dataset.total_samples || 0) * (100 - trainSplit.value) / 100),
          testSamples: dataset.test_samples || 0
        }
      } else {
        const datasets = {
          cifar10: { totalSamples: 60000, trainingSamples: 48000, validationSamples: 6000, testSamples: 6000 },
          mnist: { totalSamples: 70000, trainingSamples: 56000, validationSamples: 7000, testSamples: 7000 },
          custom: { totalSamples: 0, trainingSamples: 0, validationSamples: 0, testSamples: 0 }
        }
        datasetInfo.value = datasets[selectedDataset.value] || datasets.custom
      }
    } catch (err) {
      console.warn('Failed to load dataset info:', err)
      datasetInfo.value = { totalSamples: 1000, trainingSamples: 800, validationSamples: 200, testSamples: 0 }
    }
  }
}

const onModelChange = () => {
  console.log('Model changed to:', selectedModel.value)
}

const startTraining = async () => {
  if (!canStartTraining.value) return

  try {
    const trainingConfig = {
      type: 'local',
      name: projectName.value,
      training_alg: trainingAlg.value,
      model_name_or_path: selectedModel.value,
      dataset_name: selectedDataset.value,
      total_epochs: maxEpochs.value,
      batch_size: batchSize.value,
      lr: learningRate.value,
      num_computers: 1,
      hyperparameters: { optimizer: optimizer.value },
      data_split: {
        train_ratio: trainSplit.value / 100,
        validation_ratio: (100 - trainSplit.value) / 100
      }
    }

    console.log('Starting training:', trainingConfig)
    const response = await p2paiService.training.startLocalTraining(trainingConfig)

    if (response.success) {
      sessionId.value = response.data.session_id
      sessionStartTime.value = new Date(response.data.start_time)
      isTraining.value = true
      trainingStatus.value = 'Training'
      currentEpoch.value = 0
      trainingHistory.value = []
      setupTrainingWebSocket(sessionId.value)
      console.log('Training started:', response.data)
    } else {
      throw new Error(response.error || 'Failed to start training')
    }
  } catch (err) {
    console.error('Training failed:', err)
    trainingStatus.value = 'Error'
  }
}

const stopTraining = async () => {
  if (!sessionId.value) {
    isTraining.value = false
    trainingStatus.value = 'Ready'
    return
  }

  try {
    console.log('Stopping training:', sessionId.value)
    const response = await p2paiService.training.stopTraining(sessionId.value)

    if (response.success) {
      isTraining.value = false
      trainingStatus.value = 'Stopped'
      if (trainingWebSocket.value) {
        trainingWebSocket.value.close()
        trainingWebSocket.value = null
      }
      console.log('Training stopped')
    }
  } catch (err) {
    console.error('Failed to stop training:', err)
    isTraining.value = false
    trainingStatus.value = 'Error'
  }
}

const formatDuration = (ms) => {
  const seconds = Math.floor(ms / 1000) % 60
  const minutes = Math.floor(ms / (1000 * 60)) % 60
  const hours = Math.floor(ms / (1000 * 60 * 60))
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

// Watch for dataset split changes
watch(trainSplit, (newSplit) => {
  if (selectedDataset.value && datasetInfo.value.totalSamples > 0) {
    const total = datasetInfo.value.totalSamples
    datasetInfo.value.trainingSamples = Math.floor(total * newSplit / 100)
    datasetInfo.value.validationSamples = Math.floor(total * (100 - newSplit) / 100)
  }
})

// Setup WebSocket for real-time updates
const setupTrainingWebSocket = (sid) => {
  if (trainingWebSocket.value) {
    trainingWebSocket.value.close()
  }

  try {
    trainingWebSocket.value = p2paiService.training.createTrainingWebSocket(sid, {
      onOpen: () => console.log('WebSocket connected'),
      onMessage: (data) => updateTrainingMetrics(data),
      onError: (error) => console.error('WebSocket error:', error),
      onClose: () => {
        console.log('WebSocket closed')
        if (isTraining.value) {
          setTimeout(() => setupTrainingWebSocket(sid), 3000)
        }
      }
    })
  } catch (err) {
    console.error('Failed to setup WebSocket:', err)
  }
}

// Update metrics from WebSocket
const updateTrainingMetrics = (data) => {
  if (data.type === 'training_progress') {
    currentEpoch.value = data.epoch || currentEpoch.value
    currentAccuracy.value = data.accuracy || currentAccuracy.value
    currentLoss.value = data.loss || currentLoss.value
    validationAccuracy.value = data.validation_accuracy || validationAccuracy.value

    if (data.accuracy > bestAccuracy.value) {
      bestAccuracy.value = data.accuracy
    }

    trainingHistory.value.unshift({
      epoch: data.epoch,
      accuracy: data.accuracy,
      loss: data.loss,
      timestamp: new Date()
    })

    if (trainingHistory.value.length > 10) {
      trainingHistory.value = trainingHistory.value.slice(0, 10)
    }
  } else if (data.type === 'training_completed') {
    trainingStatus.value = 'Completed'
    isTraining.value = false
  } else if (data.type === 'training_error') {
    trainingStatus.value = 'Error'
    isTraining.value = false
  }
}

onMounted(() => {
  currentAccuracy.value = 0
  currentLoss.value = 2.5
  validationAccuracy.value = 0
})

onUnmounted(() => {
  if (trainingWebSocket.value) {
    trainingWebSocket.value.close()
    trainingWebSocket.value = null
  }
  if (isTraining.value) {
    stopTraining()
  }
})
</script>