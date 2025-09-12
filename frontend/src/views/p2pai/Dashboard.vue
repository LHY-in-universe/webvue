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
            <SimpleThemeToggle size="sm" />
            <Button @click="logout" variant="ghost" size="sm">
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>

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
              <select
                v-model="statusFilter"
                class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Statuses</option>
                <option value="Training">Training</option>
                <option value="Completed">Completed</option>
                <option value="Idle">Idle</option>
                <option value="Error">Error</option>
              </select>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
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
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()


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

// 项目搜索和过滤 - 复制EdgeAI功能
const searchQuery = ref('')
const statusFilter = ref('')

// 项目数据 - 完全按照EdgeAI格式
const projects = ref([
  {
    id: 'federated-1',
    name: 'Federated Learning Project A',
    description: 'Standard federated learning with 6 edge nodes for image classification',
    status: 'Training',
    nodes: 6,
    progress: 65,
    created: '2024-01-15',
    lastUpdated: '2 hours ago'
  },
  {
    id: 'mpc-1',
    name: 'MPC Privacy Training',
    description: 'Secure multi-party computation with cryptographic protection for sensitive data',
    status: 'Training',
    nodes: 3,
    progress: 43,
    created: '2024-01-18',
    lastUpdated: '1 hour ago'
  },
  {
    id: 'local-1',
    name: 'Local Model Training',
    description: 'Standalone training with local data for rapid prototyping',
    status: 'Completed',
    nodes: 1,
    progress: 100,
    created: '2024-01-10',
    lastUpdated: '3 days ago'
  },
  {
    id: 'federated-2',
    name: 'Large Scale Federated Network',
    description: 'Distributed training across 15 edge devices with advanced aggregation',
    status: 'Idle',
    nodes: 15,
    progress: 25,
    created: '2024-01-20',
    lastUpdated: '5 hours ago'
  },
  {
    id: 'mpc-2',
    name: 'Healthcare MPC Training',
    description: 'Privacy-preserving training for medical data with differential privacy',
    status: 'Error',
    nodes: 4,
    progress: 15,
    created: '2024-01-22',
    lastUpdated: '12 hours ago'
  }
])

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

onMounted(() => {
  // Initialize with some demo data
  accuracy.value = parseFloat((75 + Math.random() * 10).toFixed(2))
  
  // Handle role from URL parameters
  const role = route.query.role
  if (role && (role === 'client' || role === 'server')) {
    authStore.setUserType(role)
  }
})
</script>