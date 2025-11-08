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
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">Federated Training</h1>
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
            <div class="text-sm text-gray-500 dark:text-gray-400">Round</div>
            <div class="font-medium">{{ currentRound }} / {{ numRounds }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 dark:text-gray-400">Accuracy</div>
            <div class="font-medium text-green-600">{{ currentAccuracy.toFixed(2) }}%</div>
          </div>
          <div>
            <div class="text-sm text-gray-500 dark:text-gray-400">Nodes</div>
            <div class="font-medium text-blue-600">{{ connectedNodes }}/{{ numClients }}</div>
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
        <!-- Project & Federation -->
        <div class="bg-white dark:bg-slate-800 rounded-lg p-6">
          <h3 class="font-semibold mb-4">Federation Configuration</h3>
          <div class="space-y-4">
            <div>
              <label class="text-sm text-gray-600 dark:text-gray-400">Project Name</label>
              <input v-model="projectName" type="text" class="input-base" :disabled="isTraining" placeholder="Enter project name" />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Fed Algorithm</label>
                <select v-model="fedAlg" class="input-base" :disabled="isTraining">
                  <option value="FedAvg">FedAvg</option>
                  <option value="FedYgi">FedYgi</option>
                  <option value="FedAdam">FedAdam</option>
                  <option value="FedAvgM">FedAvgM</option>
                </select>
              </div>
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Dataset</label>
                <input v-model="datasetName" type="text" class="input-base" :disabled="isTraining" placeholder="CIFAR-10" />
              </div>
            </div>
            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Rounds</label>
                <input v-model.number="numRounds" type="number" class="input-base" :disabled="isTraining" />
              </div>
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Total Clients</label>
                <input v-model.number="numClients" type="number" class="input-base" :disabled="isTraining" />
              </div>
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Sample/Round</label>
                <input v-model.number="sampleClients" type="number" class="input-base" :disabled="isTraining" />
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
              <select v-model="selectedModel" class="input-base" :disabled="isTraining">
                <option value="cnn">CNN</option>
                <option value="rnn">RNN</option>
                <option value="lstm">LSTM</option>
                <option value="transformer">Transformer</option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Learning Rate</label>
                <input v-model="learningRate" type="number" step="0.001" class="input-base" :disabled="isTraining" />
              </div>
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Batch Size</label>
                <input v-model="batchSize" type="number" class="input-base" :disabled="isTraining" />
              </div>
            </div>
            <div>
              <label class="text-sm text-gray-600 dark:text-gray-400">Local Epochs</label>
              <input v-model="localEpochs" type="number" class="input-base" :disabled="isTraining" />
            </div>
          </div>
        </div>
      </div>

      <!-- Progress -->
      <div v-if="isTraining" class="bg-white dark:bg-slate-800 rounded-lg p-6 mb-6">
        <h3 class="font-semibold mb-4">Training Progress</h3>
        <ProgressBar :percentage="roundProgress" :animated="true" class="mb-2" />
        <div class="text-sm text-gray-600 dark:text-gray-400 text-center">
          Round {{ currentRound }} / {{ numRounds }} - {{ roundProgress.toFixed(1) }}%
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
          <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Connected Nodes</div>
          <div class="text-2xl font-bold text-blue-600">{{ connectedNodes }}</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
          <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Duration</div>
          <div class="text-2xl font-bold">{{ formatDuration(trainingDuration) }}</div>
        </div>
      </div>

      <!-- Network Nodes -->
      <div class="bg-white dark:bg-slate-800 rounded-lg p-6">
        <h3 class="font-semibold mb-4">Network Nodes</h3>
        <div class="grid grid-cols-2 lg:grid-cols-3 gap-3">
          <div v-for="node in networkNodes" :key="node.id"
               class="flex items-center gap-3 p-3 bg-slate-50 dark:bg-slate-700 rounded">
            <div :class="['w-2 h-2 rounded-full',
              node.status === 'online' ? 'bg-green-500' :
              node.status === 'training' ? 'bg-blue-500' : 'bg-red-500']"></div>
            <div class="flex-1">
              <div class="text-sm font-medium">{{ node.name }}</div>
              <div class="text-xs text-gray-500 capitalize">{{ node.status }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
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
const fedAlg = ref('FedAvg')
const numRounds = ref(10)
const numClients = ref(5)
const sampleClients = ref(3)
const datasetName = ref('')

// Training state
const isTraining = ref(false)
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

const networkNodes = ref([
  { id: 1, name: 'Node-001', status: 'training' },
  { id: 2, name: 'Node-002', status: 'online' },
  { id: 3, name: 'Node-003', status: 'training' },
  { id: 4, name: 'Node-004', status: 'online' },
  { id: 5, name: 'Node-005', status: 'offline' },
  { id: 6, name: 'Node-006', status: 'online' },
])

// Computed
const statusColor = computed(() => {
  switch (trainingStatus.value) {
    case 'Training': return 'text-green-600'
    case 'Completed': return 'text-blue-600'
    case 'Error': return 'text-red-600'
    default: return 'text-gray-600 dark:text-gray-400'
  }
})

const roundProgress = computed(() => {
  return (currentRound.value / numRounds.value) * 100
})

const canStartTraining = computed(() => {
  return !isTraining.value && projectName.value.trim() !== '' && datasetName.value.trim() !== '' && connectedNodes.value >= 2
})

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const startTraining = async () => {
  if (!canStartTraining.value) return

  try {
    const federatedConfig = {
      type: 'federated',
      name: projectName.value,
      training_alg: trainingAlg.value,
      fed_alg: fedAlg.value,
      model_name_or_path: selectedModel.value,
      dataset_name: datasetName.value,
      total_epochs: numRounds.value * localEpochs.value,
      num_rounds: numRounds.value,
      batch_size: batchSize.value,
      lr: learningRate.value,
      num_clients: numClients.value,
      sample_clients: sampleClients.value,
      hyperparameters: {
        local_epochs: localEpochs.value,
        max_rounds: numRounds.value
      }
    }

    console.log('Starting federated training:', federatedConfig)
    const response = await p2paiService.training.startFederatedTraining(federatedConfig)

    if (response.success) {
      sessionId.value = response.data.session_id
      sessionStartTime.value = new Date(response.data.start_time)
      isTraining.value = true
      trainingStatus.value = 'Training'
      currentRound.value = 0
      setupFederatedWebSocket(sessionId.value)
      console.log('Federated training started:', response.data)
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
      if (federatedWebSocket.value) {
        federatedWebSocket.value.close()
        federatedWebSocket.value = null
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

// Setup WebSocket
const setupFederatedWebSocket = (sid) => {
  if (federatedWebSocket.value) {
    federatedWebSocket.value.close()
  }

  try {
    federatedWebSocket.value = p2paiService.training.createTrainingWebSocket(sid, {
      onOpen: () => console.log('WebSocket connected'),
      onMessage: (data) => updateFederatedMetrics(data),
      onError: (error) => console.error('WebSocket error:', error),
      onClose: () => {
        console.log('WebSocket closed')
        if (isTraining.value) {
          setTimeout(() => setupFederatedWebSocket(sid), 3000)
        }
      }
    })
  } catch (err) {
    console.error('Failed to setup WebSocket:', err)
  }
}

// Update metrics from WebSocket
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
  } else if (data.type === 'federated_error') {
    trainingStatus.value = 'Error'
    isTraining.value = false
  }
}

// Load nodes data
const loadNodesData = async () => {
  try {
    const nodesResponse = await cachedApiCall(
      'federated-nodes',
      () => p2paiService.nodes.getNodes({ type: 'federated' }),
      30 * 1000
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

onMounted(async () => {
  currentAccuracy.value = 0
  currentLoss.value = 2.5
  bestLoss.value = 2.5
  await loadNodesData()
})

onUnmounted(() => {
  if (federatedWebSocket.value) {
    federatedWebSocket.value.close()
    federatedWebSocket.value = null
  }
  if (isTraining.value) {
    stopTraining()
  }
})
</script>