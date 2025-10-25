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
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">MPC Training</h1>
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
            <div class="text-sm text-gray-500 dark:text-gray-400">Parties</div>
            <div class="font-medium text-purple-600">{{ connectedParties }}/{{ numParties }}</div>
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
        <!-- Project & MPC -->
        <div class="bg-white dark:bg-slate-800 rounded-lg p-6">
          <h3 class="font-semibold mb-4">MPC Configuration</h3>
          <div class="space-y-4">
            <div>
              <label class="text-sm text-gray-600 dark:text-gray-400">Project Name</label>
              <input v-model="projectName" type="text" class="input-base" :disabled="isTraining" placeholder="Enter project name" />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">MPC Protocol</label>
                <select v-model="mpcProtocol" class="input-base" :disabled="isTraining">
                  <option value="SecretSharing">Secret Sharing</option>
                  <option value="Shamir">Shamir</option>
                  <option value="SPDZ">SPDZ</option>
                </select>
              </div>
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Dataset</label>
                <input v-model="datasetName" type="text" class="input-base" :disabled="isTraining" placeholder="Dataset name" />
              </div>
            </div>
            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Rounds</label>
                <input v-model.number="numRounds" type="number" class="input-base" :disabled="isTraining" />
              </div>
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Total Parties</label>
                <input v-model.number="numParties" type="number" class="input-base" :disabled="isTraining" />
              </div>
              <div>
                <label class="text-sm text-gray-600 dark:text-gray-400">Threshold</label>
                <input v-model.number="threshold" type="number" class="input-base" :disabled="isTraining" />
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
                <option value="logistic">Logistic Regression</option>
                <option value="cnn">CNN</option>
                <option value="neural">Neural Network</option>
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
              <label class="text-sm text-gray-600 dark:text-gray-400">Total Epochs</label>
              <input v-model="totalEpochs" type="number" class="input-base" :disabled="isTraining" />
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
          <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Security Level</div>
          <div class="text-2xl font-bold text-purple-600">{{ securityLevel }}</div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
          <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Duration</div>
          <div class="text-2xl font-bold">{{ formatDuration(trainingDuration) }}</div>
        </div>
      </div>

      <!-- MPC Parties -->
      <div class="bg-white dark:bg-slate-800 rounded-lg p-6">
        <h3 class="font-semibold mb-4">MPC Parties</h3>
        <div class="grid grid-cols-2 lg:grid-cols-3 gap-3">
          <div v-for="party in mpcParties" :key="party.id"
               class="flex items-center gap-3 p-3 bg-slate-50 dark:bg-slate-700 rounded">
            <div :class="['w-2 h-2 rounded-full',
              party.status === 'computing' ? 'bg-purple-500' :
              party.status === 'ready' ? 'bg-green-500' : 'bg-red-500']"></div>
            <div class="flex-1">
              <div class="text-sm font-medium">{{ party.name }}</div>
              <div class="text-xs text-gray-500 capitalize">{{ party.status }}</div>
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
const trainingAlg = ref('SecureAgg')
const fedAlg = ref('SecureFedAvg')
const mpcProtocol = ref('SecretSharing')
const numRounds = ref(10)
const numParties = ref(3)
const threshold = ref(2)
const datasetName = ref('')

// Training state
const isTraining = ref(false)
const trainingStatus = ref('Ready')
const currentRound = ref(0)
const trainingDuration = ref(0)
const sessionId = ref(null)
const sessionStartTime = ref(null)
const mpcWebSocket = ref(null)

// Training configuration
const selectedModel = ref('logistic')
const learningRate = ref(0.001)
const batchSize = ref(32)
const totalEpochs = ref(50)

// Metrics
const currentAccuracy = ref(0)
const currentLoss = ref(0)
const bestAccuracy = ref(0)
const bestLoss = ref(Infinity)
const connectedParties = ref(3)
const securityLevel = ref('High')

const mpcParties = ref([
  { id: 1, name: 'Party-A', status: 'computing' },
  { id: 2, name: 'Party-B', status: 'ready' },
  { id: 3, name: 'Party-C', status: 'computing' },
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
  return !isTraining.value && projectName.value.trim() !== '' && datasetName.value.trim() !== '' && connectedParties.value >= threshold.value
})

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const startTraining = async () => {
  if (!canStartTraining.value) return

  try {
    const mpcConfig = {
      type: 'mpc',
      name: projectName.value,
      training_alg: trainingAlg.value,
      fed_alg: fedAlg.value,
      mpc_protocol: mpcProtocol.value,
      model_name_or_path: selectedModel.value,
      dataset_name: datasetName.value,
      total_epochs: totalEpochs.value,
      num_rounds: numRounds.value,
      batch_size: batchSize.value,
      lr: learningRate.value,
      num_parties: numParties.value,
      threshold: threshold.value,
      hyperparameters: {
        security_level: securityLevel.value
      }
    }

    console.log('Starting MPC training:', mpcConfig)
    const response = await p2paiService.training.startMPCTraining(mpcConfig)

    if (response.success) {
      sessionId.value = response.data.session_id
      sessionStartTime.value = new Date(response.data.start_time)
      isTraining.value = true
      trainingStatus.value = 'Training'
      currentRound.value = 0
      setupMPCWebSocket(sessionId.value)
      console.log('MPC training started:', response.data)
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
      if (mpcWebSocket.value) {
        mpcWebSocket.value.close()
        mpcWebSocket.value = null
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
const setupMPCWebSocket = (sid) => {
  if (mpcWebSocket.value) {
    mpcWebSocket.value.close()
  }

  try {
    mpcWebSocket.value = p2paiService.training.createTrainingWebSocket(sid, {
      onOpen: () => console.log('MPC WebSocket connected'),
      onMessage: (data) => updateMPCMetrics(data),
      onError: (error) => console.error('MPC WebSocket error:', error),
      onClose: () => {
        console.log('MPC WebSocket closed')
        if (isTraining.value) {
          setTimeout(() => setupMPCWebSocket(sid), 3000)
        }
      }
    })
  } catch (err) {
    console.error('Failed to setup MPC WebSocket:', err)
  }
}

// Update metrics from WebSocket
const updateMPCMetrics = (data) => {
  if (data.type === 'mpc_round') {
    currentRound.value = data.round || currentRound.value
    currentAccuracy.value = data.accuracy || currentAccuracy.value
    currentLoss.value = data.loss || currentLoss.value
    connectedParties.value = data.connected_parties || connectedParties.value

    if (data.accuracy > bestAccuracy.value) {
      bestAccuracy.value = data.accuracy
    }
    if (data.loss < bestLoss.value) {
      bestLoss.value = data.loss
    }

    if (data.parties) {
      mpcParties.value = data.parties.map(party => ({
        id: party.id,
        name: party.name,
        status: party.status
      }))
    }
  } else if (data.type === 'mpc_completed') {
    trainingStatus.value = 'Completed'
    isTraining.value = false
  } else if (data.type === 'mpc_error') {
    trainingStatus.value = 'Error'
    isTraining.value = false
  }
}

// Load parties data
const loadPartiesData = async () => {
  try {
    const partiesResponse = await cachedApiCall(
      'mpc-parties',
      () => p2paiService.nodes.getNodes({ type: 'mpc' }),
      30 * 1000
    )

    if (partiesResponse.data?.nodes) {
      mpcParties.value = partiesResponse.data.nodes.map(party => ({
        id: party.id,
        name: party.name,
        status: party.status || 'offline'
      }))
      connectedParties.value = mpcParties.value.filter(p => p.status === 'ready' || p.status === 'computing').length
    }
  } catch (err) {
    console.warn('Failed to load parties data:', err)
  }
}

onMounted(async () => {
  currentAccuracy.value = 0
  currentLoss.value = 2.5
  bestLoss.value = 2.5
  await loadPartiesData()
})

onUnmounted(() => {
  if (mpcWebSocket.value) {
    mpcWebSocket.value.close()
    mpcWebSocket.value = null
  }
  if (isTraining.value) {
    stopTraining()
  }
})
</script>
