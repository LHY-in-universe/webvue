<template>
  <div class="local-training-visualization min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Top Navigation Bar -->
    <nav class="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded-lg bg-blue-500 flex items-center justify-center">
                <CpuChipIcon class="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                  {{ projectInfo.name }}
                </h1>
                <div class="text-sm text-gray-600 dark:text-gray-400">
                  Local Training Visualization
                </div>
              </div>
            </div>
          </div>
          
          <div class="flex items-center space-x-3">
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <!-- Training Configuration Information -->
    <div class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Training Mode</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">Local Training</div>
          </div>
          
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Model</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ projectInfo.model }}</div>
          </div>
          
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Dataset</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ projectInfo.dataset }}</div>
          </div>
          
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Status</div>
            <div class="text-lg font-semibold" :class="statusColor">{{ projectInfo.status }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Training Progress Cards -->
      <div class="grid md:grid-cols-3 gap-6 mb-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Training Progress</h3>
            <ChartBarIcon class="w-5 h-5 text-blue-500" />
          </div>
          <div class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            {{ trainingProgress }}%
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div 
              class="bg-blue-500 h-2 rounded-full transition-all duration-500"
              :style="{ width: trainingProgress + '%' }"
            ></div>
          </div>
          <div class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Epoch {{ currentEpoch }} / {{ totalEpochs }}
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Model Accuracy</h3>
            <BeakerIcon class="w-5 h-5 text-green-500" />
          </div>
          <div class="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">
            {{ (modelAccuracy * 100).toFixed(2) }}%
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Current Best Accuracy
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Training Loss</h3>
            <ArrowPathIcon class="w-5 h-5 text-orange-500" />
          </div>
          <div class="text-3xl font-bold text-orange-600 dark:text-orange-400 mb-2">
            {{ modelLoss.toFixed(4) }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Current Loss Value
          </div>
        </div>
      </div>

      <!-- Resource Usage -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Resource Usage</h3>
        <div class="space-y-4">
          <div>
            <div class="flex justify-between mb-2">
              <span class="text-sm font-medium text-gray-600 dark:text-gray-300">CPU</span>
              <span class="text-sm font-bold text-gray-900 dark:text-white">{{ cpuUsage.toFixed(2) }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                class="bg-blue-500 h-2 rounded-full"
                :style="{ width: cpuUsage + '%' }"
              ></div>
            </div>
          </div>

          <div>
            <div class="flex justify-between mb-2">
              <span class="text-sm font-medium text-gray-600 dark:text-gray-300">GPU</span>
              <span class="text-sm font-bold text-gray-900 dark:text-white">{{ gpuUsage.toFixed(2) }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                class="bg-green-500 h-2 rounded-full"
                :style="{ width: gpuUsage + '%' }"
              ></div>
            </div>
          </div>

          <div>
            <div class="flex justify-between mb-2">
              <span class="text-sm font-medium text-gray-600 dark:text-gray-300">Memory</span>
              <span class="text-sm font-bold text-gray-900 dark:text-white">{{ memoryUsage.toFixed(2) }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                class="bg-orange-500 h-2 rounded-full"
                :style="{ width: memoryUsage + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Training Control Panel -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Control Panel</h3>
        <div class="flex items-center space-x-4">
          <button
            v-if="!isTraining"
            @click="startTraining"
            class="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center space-x-2"
          >
            <PlayIcon class="w-5 h-5" />
            <span>Start Training</span>
          </button>
          
          <button
            v-if="isTraining"
            @click="pauseTraining"
            class="px-6 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg transition-colors flex items-center space-x-2"
          >
            <PauseIcon class="w-5 h-5" />
            <span>Pause Training</span>
          </button>
          
          <button
            @click="stopTraining"
            :disabled="!isTraining"
            class="px-6 py-2 bg-red-500 hover:bg-red-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex items-center space-x-2"
          >
            <StopIcon class="w-5 h-5" />
            <span>Stop Training</span>
          </button>
          
          <button
            @click="resetTraining"
            class="px-6 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition-colors flex items-center space-x-2"
          >
            <ArrowPathIcon class="w-5 h-5" />
            <span>Reset</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  ArrowLeftIcon,
  CpuChipIcon,
  ChartBarIcon,
  BeakerIcon,
  ArrowPathIcon,
  PlayIcon,
  PauseIcon,
  StopIcon
} from '@heroicons/vue/24/outline'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'

const router = useRouter()
const route = useRoute()

// Project Information
const projectInfo = ref({
  id: route.params.projectId || 1,
  name: '[Frontend Demo] Local Training - Image Classification',
  model: 'ResNet-50',
  dataset: 'CIFAR-10',
  status: 'Training'
})

// Training Status
const isTraining = ref(true)
const trainingProgress = ref(65)
const currentEpoch = ref(65)
const totalEpochs = ref(100)
const modelAccuracy = ref(0.8520)
const modelLoss = ref(0.2346)

// Resource Usage
const cpuUsage = ref(75)
const gpuUsage = ref(85)
const memoryUsage = ref(68)

// Status Color
const statusColor = computed(() => {
  const colors = {
    'Training': 'text-blue-600 dark:text-blue-400',
    'Completed': 'text-green-600 dark:text-green-400',
    'Paused': 'text-yellow-600 dark:text-yellow-400',
    'Stopped': 'text-red-600 dark:text-red-400'
  }
  return colors[projectInfo.value.status] || 'text-gray-600 dark:text-gray-400'
})

// Training Control Methods
const startTraining = () => {
  isTraining.value = true
  projectInfo.value.status = 'Training'
}

const pauseTraining = () => {
  isTraining.value = false
  projectInfo.value.status = 'Paused'
}

const stopTraining = () => {
  isTraining.value = false
  projectInfo.value.status = 'Stopped'
}

const resetTraining = () => {
  trainingProgress.value = 0
  currentEpoch.value = 0
  modelAccuracy.value = 0
  modelLoss.value = 2.5
  isTraining.value = false
  projectInfo.value.status = 'Stopped'
}

const goBack = () => {
  router.push('/p2pai/dashboard')
}

// Simulate Training Progress Update
let trainingInterval = null

onMounted(() => {
  if (isTraining.value) {
    trainingInterval = setInterval(() => {
      if (currentEpoch.value < totalEpochs.value) {
        currentEpoch.value += 1
        trainingProgress.value = Math.round((currentEpoch.value / totalEpochs.value) * 100)
        
        // Simulate accuracy improvement and loss reduction
        modelAccuracy.value = Math.min(0.95, modelAccuracy.value + 0.001)
        modelLoss.value = Math.max(0.05, modelLoss.value * 0.995)
        
        // Simulate resource usage fluctuation
        cpuUsage.value = 70 + Math.random() * 20
        gpuUsage.value = 80 + Math.random() * 15
        memoryUsage.value = 60 + Math.random() * 25
      } else {
        projectInfo.value.status = 'Completed'
        isTraining.value = false
        clearInterval(trainingInterval)
      }
    }, 2000) // Update every 2 seconds
  }
})

onUnmounted(() => {
  if (trainingInterval) {
    clearInterval(trainingInterval)
  }
})
</script>

<style scoped>
.local-training-visualization {
  min-height: 100vh;
}
</style>

