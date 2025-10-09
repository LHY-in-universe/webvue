<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Navigation -->
    <nav class="glass-effect shadow-soft border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center mr-3 micro-bounce hover-glow-primary">
              <CpuChipIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gradient text-shadow-soft">
              {{ userTypeText === 'Client' ? 'Client Control Panel' : 'Server Control Panel' }}
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Welcome, {{ authStore.user?.username }}
            </span>
            
            <!-- Offline/Online Status -->
            <div v-if="isOffline" class="flex items-center space-x-2 text-sm text-yellow-600 dark:text-yellow-400">
              <div class="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
              <span>Offline Mode</span>
              <span v-if="queuedRequests > 0">({{ queuedRequests }} queued)</span>
            </div>
            
            <!-- Refresh Button -->
            <Button 
              @click="refreshData" 
              variant="ghost" 
              size="sm"
              :disabled="loading"
              :leftIcon="loading ? undefined : ChartBarIcon"
            >
              <LoadingSpinner v-if="loading" size="sm" />
              <span v-else>Refresh</span>
            </Button>
            
            <SimpleThemeToggle size="sm" />
            <Button @click="logout" variant="ghost" size="sm">
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Error State -->
    <div v-if="error && !loading" class="max-w-4xl mx-auto px-6 py-4">
      <Card class="bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800">
        <div class="p-4 flex items-center space-x-3">
          <div class="flex-shrink-0">
            <svg class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
              Failed to load dashboard data
            </h3>
            <p class="mt-1 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </p>
          </div>
          <Button @click="refreshData" variant="secondary" size="sm">
            Retry
          </Button>
        </div>
      </Card>
    </div>

    <div class="max-w-4xl mx-auto px-6 py-8">
      <!-- Client Dashboard -->
      <div v-if="authStore.userType === 'client'">
        <!-- Welcome Section -->
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Welcome Back!
          </h2>
          <p class="text-gray-600 dark:text-gray-400">Create new training projects or manage existing ones</p>
        </div>

        <!-- Project Creation Section -->
        <div class="grid md:grid-cols-3 gap-6 mb-8">
          <!-- Local Training Project Creation -->
          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="createLocalProject">
            <div class="text-center p-6">
              <div class="w-14 h-14 bg-gray-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <ShieldCheckIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Local Model Training</h3>
              <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">Train models independently using local data while protecting data privacy</p>
              
              <div class="space-y-2 mb-4">
                <div class="flex justify-between text-xs">
                  <span class="text-gray-500 dark:text-gray-400">Data Security:</span>
                  <span class="text-gray-700 dark:text-gray-300 font-medium">Local Storage</span>
                </div>
                <div class="flex justify-between text-xs">
                  <span class="text-gray-500 dark:text-gray-400">Training Speed:</span>
                  <span class="text-gray-700 dark:text-gray-300 font-medium">Fast</span>
                </div>
                <div class="flex justify-between text-xs">
                  <span class="text-gray-500 dark:text-gray-400">Model Performance:</span>
                  <span class="text-gray-700 dark:text-gray-300 font-medium">Limited by local data</span>
                </div>
              </div>
              
              <div class="text-gray-600 dark:text-gray-400 font-medium text-sm">
                Start Local Training →
              </div>
            </div>
          </Card>

          <!-- Federated Learning Project Creation -->
          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="createFederatedProject">
            <div class="text-center p-6">
              <div class="w-14 h-14 bg-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <UsersIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Federated Learning Training</h3>
              <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">Participate in distributed federated learning for better model performance</p>
              
              <div class="space-y-2 mb-4">
                <div class="flex justify-between text-xs">
                  <span class="text-gray-500 dark:text-gray-400">Data Security:</span>
                  <span class="text-gray-700 dark:text-gray-300 font-medium">Privacy Protected</span>
                </div>
                <div class="flex justify-between text-xs">
                  <span class="text-gray-500 dark:text-gray-400">Training Speed:</span>
                  <span class="text-gray-700 dark:text-gray-300 font-medium">Moderate</span>
                </div>
                <div class="flex justify-between text-xs">
                  <span class="text-gray-500 dark:text-gray-400">Model Performance:</span>
                  <span class="text-gray-700 dark:text-gray-300 font-medium">Excellent</span>
                </div>
              </div>
              
              <div class="text-blue-600 font-medium text-sm">
                Start Federated Learning →
              </div>
            </div>
          </Card>

          <!-- MPC Training Project Creation -->
          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="createMPCProject">
            <div class="text-center p-6">
              <div class="w-14 h-14 bg-green-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <LockClosedIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">MPC Training</h3>
              <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">Secure multi-party computation with cryptographic privacy guarantees</p>
              
              <div class="space-y-2 mb-4">
                <div class="flex justify-between text-xs">
                  <span class="text-gray-500 dark:text-gray-400">Data Security:</span>
                  <span class="text-gray-700 dark:text-gray-300 font-medium">Cryptographic</span>
                </div>
                <div class="flex justify-between text-xs">
                  <span class="text-gray-500 dark:text-gray-400">Training Speed:</span>
                  <span class="text-gray-700 dark:text-gray-300 font-medium">Secure</span>
                </div>
                <div class="flex justify-between text-xs">
                  <span class="text-gray-500 dark:text-gray-400">Model Performance:</span>
                  <span class="text-gray-700 dark:text-gray-300 font-medium">High with Privacy</span>
                </div>
              </div>
              
              <div class="text-green-600 font-medium text-sm">
                Start MPC Training →
              </div>
            </div>
          </Card>
        </div>

        <!-- Management Centers -->
        <div class="grid md:grid-cols-2 gap-6 mb-8">
          <!-- Dataset Management -->
          <Card class="cursor-pointer hover:shadow-lg transition-shadow" @click="openDatasetCenter">
            <div class="text-center p-6">
              <div class="w-14 h-14 bg-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <CircleStackIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Dataset Management Center</h3>
              <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">Manage and organize training datasets, upload new datasets</p>
              <div class="text-blue-600 font-medium text-sm">
                Enter Dataset Center →
              </div>
            </div>
          </Card>

          <!-- Model Management -->
          <Card class="cursor-pointer hover:shadow-lg transition-shadow" @click="openModelCenter">
            <div class="text-center p-6">
              <div class="w-14 h-14 bg-green-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <CubeIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Model Management Center</h3>
              <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">View and manage trained models, import new models</p>
              <div class="text-green-600 font-medium text-sm">
                Enter Model Center →
              </div>
            </div>
          </Card>
        </div>

        <!-- Training Status Overview -->
        <Card class="mb-8">
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Training Status Overview</h3>
          </template>
          <div class="grid md:grid-cols-3 gap-6">
            <div class="text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-slate-700 p-3 rounded-lg transition-colors" 
                 @click="viewCompletedTraining">
              <div class="text-2xl font-bold text-gray-700 dark:text-gray-300">{{ completedTraining }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Completed Training</div>
              <div class="text-xs text-blue-600 mt-1">Click to view details</div>
            </div>
            <div class="text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-slate-700 p-3 rounded-lg transition-colors"
                 @click="viewOngoingTraining">
              <div class="text-2xl font-bold text-gray-700 dark:text-gray-300">{{ ongoingTraining }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Ongoing Training</div>
              <div class="text-xs text-blue-600 mt-1">Click to view details</div>
            </div>
            <div class="text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-slate-700 p-3 rounded-lg transition-colors"
                 @click="viewAccuracyStats">
              <div class="text-2xl font-bold text-gray-700 dark:text-gray-300">{{ averageAccuracy.toFixed(2) }}%</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Average Accuracy</div>
              <div class="text-xs text-blue-600 mt-1">Click to view details</div>
            </div>
          </div>
        </Card>

        <!-- My Projects - 完全复制EdgeAI设计 -->
        <div class="mb-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-white">My Projects</h2>
            
            <div class="flex items-center space-x-4">
              <!-- Search Box -->
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search projects..."
                  class="w-64 pl-4 pr-10 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <MagnifyingGlassIcon class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              </div>
              
              <!-- Status Filter -->
              <CustomSelect
                v-model="statusFilter"
                :options="statusOptions"
                placeholder="All Statuses"
                class="w-48"
              />
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div 
              v-for="project in filteredProjects" 
              :key="project.id"
              @click="openProjectVisualization(project)"
              class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 cursor-pointer hover:shadow-lg transition-all duration-200"
            >
              <!-- Status Indicator and Title -->
              <div class="flex items-start justify-between mb-3">
                <div class="flex items-center">
                  <div 
                    :class="getStatusDotColor(project.status)"
                    class="w-3 h-3 rounded-full mr-3"
                  ></div>
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ project.name }}
                  </h3>
                </div>
              </div>
              
              <!-- Description -->
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                {{ project.description }}
              </p>
              
              <!-- Connected Nodes -->
              <div class="flex justify-between text-sm mb-2">
                <span class="text-gray-500 dark:text-gray-400">Connected Nodes:</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ project.nodes }}</span>
              </div>
              
              <!-- Training Progress -->
              <div class="flex justify-between text-sm mb-2">
                <span class="text-gray-500 dark:text-gray-400">Training Progress:</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ project.progress }}%</span>
              </div>
              
              <!-- Progress Bar -->
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-4">
                <div 
                  class="bg-green-500 h-2 rounded-full transition-all duration-300"
                  :style="{ width: project.progress + '%' }"
                ></div>
              </div>
              
              <!-- Timestamps -->
              <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400">
                <span>Created: {{ project.created }}</span>
                <span>Updated: {{ project.lastUpdated }}</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Server Dashboard -->
      <div v-else-if="authStore.userType === 'server'">
        <!-- Server Welcome Section -->
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Server Management Center
          </h2>
          <p class="text-gray-600 dark:text-gray-400">Monitor and manage federated learning processes</p>
        </div>

        <!-- Server Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 stagger-children">
          <StatCard
            title="Connected Clients"
            :value="connectedClients"
            :icon="ServerIcon"
            variant="primary"
            :trend="2.5"
            trend-label="vs yesterday"
            description="Active client connections"
            clickable
            animated
            @click="viewClientDetails"
          />
          
          <StatCard
            title="Active Training"
            :value="activeTrainingSessions"
            :icon="CpuChipIcon"
            variant="success"
            :progress="75"
            description="Training sessions in progress"
            clickable
            animated
            @click="viewTrainingDetails"
          />
          
          <StatCard
            title="Pending Requests"
            :value="pendingRequests"
            :icon="ClockIcon"
            variant="warning"
            :trend="-15.2"
            trend-label="vs last hour"
            description="Queued training requests"
            clickable
            animated
            @click="viewPendingRequests"
          />
          
          <StatCard
            title="System Uptime"
            :value="systemUptime"
            unit="h"
            :precision="2"
            :icon="ChartBarIcon"
            variant="info"
            :progress="99.2"
            description="Continuous operation time"
            clickable
            animated
            @click="viewSystemStatus"
          />
        </div>

        <!-- Global Training Control -->
        <Card class="mb-8">
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Global Training Control</h3>
          </template>
          
          <div class="space-y-4">
            <Button 
              @click="startGlobalTraining" 
              variant="primary" 
              size="lg" 
              block
              :loading="globalTrainingActive"
              :disabled="globalTrainingActive"
            >
              {{ globalTrainingActive ? 'Training in Progress...' : 'Start Global Training' }}
            </Button>
            
            <div v-if="globalTrainingActive" class="space-y-4">
              <div class="text-center py-2 text-gray-600 dark:text-gray-400">
                <p>Training Round: {{ trainingRounds }} / 10</p>
                <p>Current Accuracy: {{ accuracy.toFixed(2) }}%</p>
              </div>
              
              <ProgressBar
                :percentage="(trainingRounds / 10) * 100"
                label="Training Progress"
                variant="success"
                :animated="true"
                :info="`Round ${trainingRounds} of 10`"
              />
            </div>
          </div>
        </Card>

        <!-- Client Management & System Logs -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Connected Clients</h3>
            </template>
            
            <div class="space-y-3">
              <div v-for="client in clientList" :key="client.id" class="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                <div>
                  <div class="font-medium text-gray-900 dark:text-white">{{ client.name }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">{{ client.ip }}</div>
                </div>
                <div class="text-right">
                  <div class="text-sm font-medium" :class="client.status === 'online' ? 'text-green-600' : 'text-gray-400'">
                    {{ client.status }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">{{ client.lastSeen }}</div>
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <template #header>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">System Logs</h3>
            </template>
            
            <div class="space-y-3">
              <div v-for="log in systemLogs" :key="log.id" class="text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-900 dark:text-white">{{ log.message }}</span>
                  <span class="text-gray-500 dark:text-gray-400">{{ log.time }}</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>

    <!-- Training Details Modal -->
    <Modal
      v-model:isOpen="showTrainingModal"
      title="Training Details"
      :icon="ChartBarIcon"
      size="lg"
      @confirm="handleTrainingAction"
      @cancel="closeTrainingModal"
    >
      <div class="space-y-6">
        <!-- Training Summary -->
        <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-3">Training Summary</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Model Type</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ selectedTraining?.name || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Training Type</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ selectedTraining?.trainingType || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Accuracy</p>
              <p class="font-medium text-gray-900 dark:text-white">
                {{ selectedTraining?.accuracy ? `${selectedTraining.accuracy.toFixed(2)}%` : 'N/A' }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Date</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ selectedTraining?.date || 'N/A' }}</p>
            </div>
          </div>
        </div>

        <!-- Training Progress (if applicable) -->
        <div v-if="selectedTraining?.progress">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-3">Training Progress</h4>
          <ProgressBar
            :percentage="selectedTraining.progress"
            label="Completion Rate"
            variant="success"
            :animated="true"
          />
        </div>

        <!-- Loading State -->
        <div v-if="modalLoading" class="flex justify-center py-8">
          <LoadingSpinner 
            size="lg" 
            text="Loading training details..." 
            color="primary"
          />
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button @click="closeTrainingModal" variant="ghost">
            Close
          </Button>
          <Button @click="handleTrainingAction" variant="primary">
            View Full Report
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { useP2PAIStore } from '@/stores/p2pai'
import { useApiOptimization } from '@/composables/useApiOptimization.js'
import { useErrorBoundary } from '@/composables/useErrorBoundary'
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts'
import { useOfflineMode } from '@/composables/useOfflineMode'
import p2paiService from '@/services/p2paiService.js'
import performanceMonitor from '@/utils/performanceMonitor.js'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import CustomSelect from '@/components/ui/CustomSelect.vue'
import { 
  CpuChipIcon, 
  ClockIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  UsersIcon,
  CircleStackIcon,
  CubeIcon,
  ServerIcon,
  LockClosedIcon,
  MagnifyingGlassIcon,
  PlayIcon,
  CheckCircleIcon,
  PauseIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const uiStore = useUIStore()
const p2paiStore = useP2PAIStore()
const { cachedApiCall, clearCache } = useApiOptimization()
const { hasError, retry, captureError } = useErrorBoundary()
const { enableShortcuts, disableShortcuts } = useKeyboardShortcuts()
const { 
  isOffline, 
  queuedRequests, 
  hasOfflineData, 
  offlineAwareFetch 
} = useOfflineMode()

// API loading state
const loading = ref(true)
const error = ref(null)


// Common data
const trainingRounds = ref(0)
const accuracy = ref(0)

// Modal data
const showTrainingModal = ref(false)
const selectedTraining = ref(null)
const modalLoading = ref(false)

// Client-specific data
const completedTraining = ref(3)
const ongoingTraining = ref(1)
const averageAccuracy = ref(92.47)


// Server-specific data
const globalTrainingActive = ref(false)
const connectedClients = ref(4)
const activeTrainingSessions = ref(2)
const pendingRequests = ref(1)
const systemUptime = ref(48.73)

// Enhanced API data loading function
const loadDashboardData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('P2PAIDashboard')
  loading.value = true
  error.value = null
  
  try {
    // Load all dashboard data in parallel using cached API calls
    const [projectStats, nodeStats, trainingData, modelStats, datasetStats] = await Promise.all([
      cachedApiCall('project-stats', () => p2paiService.projects.getProjectStats(), 2 * 60 * 1000),
      cachedApiCall('node-stats', () => p2paiService.nodes.getNodeStats(), 1 * 60 * 1000),
      cachedApiCall('training-sessions', () => p2paiService.training.getTrainingSessions({ limit: 10 }), 30 * 1000),
      cachedApiCall('model-stats', () => p2paiService.models.getModelStats(), 5 * 60 * 1000),
      cachedApiCall('dataset-stats', () => p2paiService.datasets.getDatasetStats(), 5 * 60 * 1000)
    ])
    
    // Update project data with real API data
    if (projectStats.data?.projects) {
      projects.value = projectStats.data.projects.map(project => ({
        ...project,
        lastUpdated: formatTime(project.last_updated)
      }))
    }
    
    // Update dashboard statistics
    completedTraining.value = trainingData.data?.completed_sessions || 0
    ongoingTraining.value = trainingData.data?.active_sessions || 0
    averageAccuracy.value = trainingData.data?.average_accuracy || 0
    connectedClients.value = nodeStats.data?.connected_nodes || 0
    activeTrainingSessions.value = trainingData.data?.active_sessions || 0
    pendingRequests.value = trainingData.data?.pending_requests || 0
    systemUptime.value = nodeStats.data?.uptime_hours || 0
    
    // Sync with main P2PAI store
    await p2paiStore.loadRealData()
    
    console.log('📊 Dashboard data loaded successfully')
    pageMonitor.end()
  } catch (err) {
    console.error('❌ Failed to load dashboard data:', err)
    error.value = err.message || 'Failed to load dashboard data'
    captureError(err, null, 'Dashboard data loading failed')
    pageMonitor.end()
  } finally {
    loading.value = false
  }
}

// Enhanced refresh dashboard data
const refreshData = async () => {
  // Clear all caches for fresh data
  clearCache('project-stats')
  clearCache('node-stats')
  clearCache('training-sessions')
  clearCache('model-stats')
  clearCache('dataset-stats')
  
  await loadDashboardData()
  
  uiStore.addNotification({
    type: 'success',
    title: 'Dashboard Refreshed',
    message: 'All data has been updated',
    duration: 2000
  })
}

// Format time helper for real timestamps
const formatTime = (timestamp) => {
  if (!timestamp) return 'Unknown'
  
  const now = new Date()
  const time = new Date(timestamp)
  const diffInMinutes = Math.floor((now - time) / (1000 * 60))
  
  if (diffInMinutes < 1) return 'Just now'
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`
  
  const hours = Math.floor(diffInMinutes / 60)
  if (hours < 24) return `${hours}h ago`
  
  const days = Math.floor(hours / 24)
  return `${days}d ago`
}

// 项目搜索和过滤 - 复制EdgeAI功能
const searchQuery = ref('')
const statusFilter = ref('')

// Status filter options with icons
const statusOptions = ref([
  { value: '', label: 'All Statuses', icon: null },
  { value: 'Training', label: 'Training', icon: PlayIcon },
  { value: 'Completed', label: 'Completed', icon: CheckCircleIcon },
  { value: 'Idle', label: 'Idle', icon: PauseIcon },
  { value: 'Error', label: 'Error', icon: ExclamationTriangleIcon }
])

// 项目数据 - 初始为空，将从API加载
const projects = ref([])

// 计算属性 - 复制EdgeAI的过滤逻辑
const filteredProjects = computed(() => {
  let filtered = projects.value

  // 按搜索查询过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(project => 
      project.name.toLowerCase().includes(query) ||
      project.description.toLowerCase().includes(query)
    )
  }

  // 按状态过滤
  if (statusFilter.value) {
    filtered = filtered.filter(project => project.status === statusFilter.value)
  }

  return filtered
})

// 状态点颜色 - 复制EdgeAI逻辑
const getStatusDotColor = (status) => {
  const colors = {
    'Training': 'bg-blue-500',
    'Completed': 'bg-green-500', 
    'Idle': 'bg-gray-500',
    'Error': 'bg-red-500'
  }
  return colors[status] || 'bg-gray-500'
}

const clientList = ref([
  {
    id: 'client_001',
    name: 'Client-001',
    ip: '192.168.1.101',
    status: 'online',
    lastSeen: '2 mins ago'
  },
  {
    id: 'client_002', 
    name: 'Client-002',
    ip: '192.168.1.102',
    status: 'online',
    lastSeen: '5 mins ago'
  },
  {
    id: 'client_003',
    name: 'Client-003',
    ip: '192.168.1.103',
    status: 'offline',
    lastSeen: '1 hour ago'
  },
  {
    id: 'client_004',
    name: 'Client-004',
    ip: '192.168.1.104',
    status: 'online',
    lastSeen: '1 min ago'
  }
])

const systemLogs = ref([
  { id: 1, message: 'Global training session started', time: 'just now' },
  { id: 2, message: 'Client-004 joined training session', time: '2 minutes ago' },
  { id: 3, message: 'Model parameters updated', time: '5 minutes ago' },
  { id: 4, message: 'Training round 8 completed', time: '8 minutes ago' }
])

const userTypeText = computed(() => {
  return authStore.userType === 'server' ? 'Server' : 'Client'
})

// Project Creation Methods
const createLocalProject = () => {
  router.push('/p2pai/local-training')
}

const createFederatedProject = () => {
  router.push('/p2pai/federated-training')
}

const createMPCProject = () => {
  router.push('/p2pai/mpc-training')
}

const openDatasetCenter = () => {
  router.push('/p2pai/datasets')
}

const openModelCenter = () => {
  router.push('/p2pai/models')
}


const openProjectVisualization = (project) => {
  // 如果传入的是字符串（旧的调用方式），则直接使用
  if (typeof project === 'string') {
    router.push(`/p2pai/visualization/${project}`)
  } else {
    // 如果传入的是项目对象（新的EdgeAI样式），使用项目ID
    router.push(`/p2pai/visualization/${project.id}`)
  }
}

const viewCompletedTraining = () => {
  console.log('Viewing completed training details')
  // TODO: Show completed training modal
}

const viewOngoingTraining = () => {
  console.log('Viewing ongoing training details')
  // TODO: Show ongoing training modal  
}

const viewAccuracyStats = () => {
  console.log('Viewing accuracy statistics')
  // TODO: Show accuracy stats modal
}


// Server methods
const startGlobalTraining = () => {
  globalTrainingActive.value = true
  console.log('Starting global training')
  
  // Simulate training progress
  const interval = setInterval(() => {
    trainingRounds.value++
    accuracy.value = parseFloat(Math.min(95, accuracy.value + Math.random() * 3).toFixed(2))
    
    if (trainingRounds.value >= 10) {
      globalTrainingActive.value = false
      clearInterval(interval)
      
      // Add completion log
      systemLogs.value.unshift({
        id: Date.now(),
        message: 'Global training completed successfully',
        time: 'just now'
      })
    }
  }, 3000)
}

const viewClientDetails = () => {
  router.push('/p2pai/monitor')
}

const viewTrainingDetails = () => {
  router.push('/p2pai/monitor')
}

const viewPendingRequests = () => {
  router.push('/p2pai/models')
}

const viewSystemStatus = () => {
  router.push('/p2pai/monitor')
}

// Modal methods
const closeTrainingModal = () => {
  showTrainingModal.value = false
  selectedTraining.value = null
  modalLoading.value = false
}

const handleTrainingAction = () => {
  console.log('Handling training action for:', selectedTraining.value?.id)
  // TODO: Navigate to full training report
  closeTrainingModal()
}

const logout = () => {
  authStore.logout()
  router.push('/')
}

// Auto-refresh interval
let refreshInterval = null

onMounted(async () => {
  console.group('🚀 P2P AI Dashboard mounted')
  console.log('Loading dashboard data...')
  
  // Enable modern functionality
  enableShortcuts()
  
  // Initialize with some demo data for backwards compatibility
  accuracy.value = parseFloat((75 + Math.random() * 10).toFixed(2))
  
  // Handle role from URL parameters
  const role = route.query.role
  if (role && (role === 'client' || role === 'server')) {
    authStore.setUserType(role)
  }
  
  // Load initial data from API
  await loadDashboardData()
  
  // Set up auto-refresh every 30 seconds
  refreshInterval = setInterval(() => {
    if (!loading.value) {
      refreshData()
    }
  }, 30000)
  
  // Show welcome notification
  uiStore.addNotification({
    type: 'info',
    title: 'P2PAI Dashboard',
    message: 'Dashboard loaded with enhanced features',
    duration: 3000
  })
  
  console.log('Dashboard initialized with auto-refresh and modern features')
  console.groupEnd()
})

onUnmounted(() => {
  console.log('🧹 Cleaning up P2P AI Dashboard')
  
  // Disable modern functionality
  disableShortcuts()
  
  // Clear refresh interval
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  
  console.log('P2P AI Dashboard unmounted')
})
</script>