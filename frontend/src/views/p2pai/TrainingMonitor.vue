<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Navigation -->
    <nav class="glass-effect shadow-soft border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            
            <div class="w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center mr-3">
              <ChartBarIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Training Monitor
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span class="text-sm text-gray-600 dark:text-gray-400">Live</span>
            </div>
            <Button 
              @click="refreshSessions" 
              variant="ghost" 
              size="sm"
              :loading="refreshing"
            >
              Refresh
            </Button>
            <Button 
              @click="toggleTheme" 
              variant="ghost" 
              size="sm"
            >
              Theme
            </Button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Training Monitor
          </h2>
          <p class="text-gray-600 dark:text-gray-400">
            Real-time monitoring of all training sessions
          </p>
        </div>
      </div>

      <!-- Training Overview Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Active Sessions"
          :value="trainingMetrics.activeSessions"
          :icon="PlayIcon"
          variant="success"
          description="Currently training"
          :loading="loading.metrics"
        />
        
        <StatCard
          title="Completed Today"
          :value="trainingMetrics.completedToday"
          :icon="CheckCircleIcon"
          variant="info"
          description="Successfully finished"
          :loading="loading.metrics"
        />
        
        <StatCard
          title="Total GPU Hours"
          :value="trainingMetrics.totalGpuHours"
          unit="h"
          :precision="1"
          :icon="CpuChipIcon"
          variant="warning"
          description="Resource usage"
          :loading="loading.metrics"
        />

        <StatCard
          title="Average Accuracy"
          :value="trainingMetrics.averageAccuracy"
          unit="%"
          :precision="1"
          :icon="TrophyIcon"
          variant="primary"
          description="Session performance"
          :loading="loading.metrics"
        />
      </div>

      <!-- Active Training Sessions -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Live Training Sessions -->
        <Card class="glass-effect">
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <PlayIcon class="w-5 h-5 mr-2 text-green-500" />
                Active Training Sessions
              </h3>
              <Button
                @click="refreshSessions"
                variant="ghost"
                size="sm"
              >
                Refresh
              </Button>
            </div>
            
            <div class="space-y-4">
              <div class="text-center py-8">
                <PlayIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
                <p class="text-gray-500 dark:text-gray-400">No active training sessions</p>
              </div>
            </div>
          </div>
        </Card>

        <!-- System Resources -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <ServerIcon class="w-5 h-5 mr-2 text-blue-500" />
              System Resources
            </h3>
            
            <div class="space-y-6">
              <!-- GPU Utilization -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">GPU Utilization</span>
                  <span class="text-sm text-gray-600 dark:text-gray-400">75%</span>
                </div>
                <ProgressBar :percentage="75" variant="success" />
              </div>
              
              <!-- CPU Usage -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">CPU Usage</span>
                  <span class="text-sm text-gray-600 dark:text-gray-400">45%</span>
                </div>
                <ProgressBar :percentage="45" variant="info" />
              </div>
              
              <!-- Memory Usage -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Memory Usage</span>
                  <span class="text-sm text-gray-600 dark:text-gray-400">68%</span>
                </div>
                <ProgressBar :percentage="68" variant="warning" />
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Performance Charts -->
      <Card class="glass-effect">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <ChartBarIcon class="w-5 h-5 mr-2 text-indigo-500" />
            Performance Analytics
          </h3>
          
          <!-- Chart placeholder -->
          <div class="h-64 bg-gray-50 dark:bg-slate-700 rounded-lg flex items-center justify-center">
            <div class="text-center">
              <ChartBarIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p class="text-gray-500 dark:text-gray-400">Training performance charts</p>
              <p class="text-xs text-gray-400 mt-1">Real-time analytics coming soon</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
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
  ChartBarIcon,
  PlayIcon,
  CheckCircleIcon,
  CpuChipIcon,
  TrophyIcon,
  ServerIcon
} from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'

const router = useRouter()
const themeStore = useThemeStore()
const uiStore = useUIStore()
const p2paiStore = useP2PAIStore()
const { hasError, retry, captureError } = useErrorBoundary()
const { enableShortcuts, disableShortcuts } = useKeyboardShortcuts()
const { cachedApiCall, clearCache } = useApiOptimization()

// State
const loading = ref({
  sessions: false,
  metrics: false
})
const refreshing = ref(false)
const trainingSessions = ref([])
const trainingMetrics = ref({
  activeSessions: 0,
  completedToday: 0,
  totalGpuHours: 0,
  averageAccuracy: 0
})

// Real-time WebSocket connection
let trainingWS = null

// Load training data from API
const loadTrainingData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('P2PAI-TrainingMonitor')
  loading.value.sessions = true
  loading.value.metrics = true
  
  try {
    const [sessionsResult, metricsResult] = await Promise.all([
      cachedApiCall(
        'p2pai-training-sessions',
        () => p2paiService.training.getTrainingSessions({ active: true }),
        30 * 1000 // Cache for 30 seconds
      ),
      cachedApiCall(
        'p2pai-training-metrics',
        () => p2paiService.training.getTrainingMetrics(),
        60 * 1000 // Cache for 1 minute
      )
    ])
    
    if (sessionsResult && sessionsResult.data) {
      trainingSessions.value = sessionsResult.data.map(session => ({
        id: session.id,
        name: session.name || 'Training Session',
        status: session.status || 'active',
        progress: session.progress || 0,
        accuracy: session.accuracy || 0,
        loss: session.loss || 0,
        epoch: session.current_epoch || 0,
        totalEpochs: session.total_epochs || 100,
        startTime: new Date(session.start_time || Date.now()),
        estimatedTimeRemaining: session.estimated_time_remaining || 0,
        nodes: session.participating_nodes || []
      }))
    }
    
    if (metricsResult && metricsResult.data) {
      trainingMetrics.value = {
        activeSessions: metricsResult.data.active_sessions || 0,
        completedToday: metricsResult.data.completed_today || 0,
        totalGpuHours: metricsResult.data.total_gpu_hours || 0,
        averageAccuracy: metricsResult.data.average_accuracy || 0
      }
    }
    
    pageMonitor.end()
  } catch (error) {
    console.error('Failed to load training data:', error)
    captureError(error, null, 'Training data loading failed')
    pageMonitor.end()
  } finally {
    loading.value.sessions = false
    loading.value.metrics = false
  }
}

// Setup real-time training updates
const setupRealtimeUpdates = () => {
  try {
    trainingWS = p2paiService.training.createTrainingWebSocket('*', {
      onMessage: (data) => {
        if (data.type === 'training_update') {
          updateTrainingSession(data.payload)
        } else if (data.type === 'training_metrics') {
          updateTrainingMetrics(data.payload)
        }
      },
      onError: (error) => {
        console.error('Training WebSocket error:', error)
      }
    })
  } catch (error) {
    console.error('Failed to setup real-time updates:', error)
  }
}

// Update training session data
const updateTrainingSession = (sessionData) => {
  const index = trainingSessions.value.findIndex(s => s.id === sessionData.id)
  if (index !== -1) {
    trainingSessions.value[index] = {
      ...trainingSessions.value[index],
      ...sessionData
    }
  }
}

// Update training metrics
const updateTrainingMetrics = (metricsData) => {
  trainingMetrics.value = {
    ...trainingMetrics.value,
    ...metricsData
  }
}

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const refreshSessions = async () => {
  refreshing.value = true
  clearCache('p2pai-training-sessions')
  clearCache('p2pai-training-metrics')
  await loadTrainingData()
  refreshing.value = false
  
  uiStore.addNotification({
    type: 'success',
    title: 'Training Data Refreshed',
    message: 'All training data has been updated',
    duration: 2000
  })
}

// Computed properties
const activeSessions = computed(() => trainingSessions.value.filter(s => s.status === 'active'))
const completedSessions = computed(() => trainingSessions.value.filter(s => s.status === 'completed'))

// Lifecycle
onMounted(async () => {
  enableShortcuts()
  await loadTrainingData()
  setupRealtimeUpdates()
  
  uiStore.addNotification({
    type: 'info',
    title: 'Training Monitor',
    message: 'Real-time training monitoring enabled',
    duration: 3000
  })
})

onUnmounted(() => {
  disableShortcuts()
  if (trainingWS) {
    trainingWS.close()
  }
})
</script>

<style scoped>
.glass-effect {
  @apply bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm;
}
</style>