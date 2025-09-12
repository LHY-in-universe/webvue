<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <ComputerDesktopIcon class="h-8 w-8 text-green-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Edge AI Dashboard
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

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Welcome to OpenTMP Edge AI Intelligence!
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-400">
          Manage your edge AI nodes and training projects
        </p>
      </div>

      <!-- Statistics Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <ComputerDesktopIcon class="w-12 h-12 text-gray-600 dark:text-gray-400" />
          </div>
          <div class="text-3xl font-bold text-gray-900 dark:text-white mb-2">5</div>
          <div class="text-gray-600 dark:text-gray-400">Total Projects</div>
        </div>

        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <ServerIcon class="w-12 h-12 text-green-600 dark:text-green-400" />
          </div>
          <div class="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">12</div>
          <div class="text-gray-600 dark:text-gray-400">Active Nodes</div>
        </div>

        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <svg class="w-12 h-12 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="text-3xl font-bold text-yellow-500 mb-2">3</div>
          <div class="text-gray-600 dark:text-gray-400">Training Tasks</div>
        </div>

        <div class="text-center">
          <div class="flex items-center justify-center mb-4">
            <ChartBarIcon class="w-12 h-12 text-purple-600 dark:text-purple-400" />
          </div>
          <div class="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-2">87%</div>
          <div class="text-gray-600 dark:text-gray-400">Completion Rate</div>
        </div>
      </div>

      <!-- Main Function Buttons -->
      <div class="flex flex-wrap gap-4 mb-8">
        <Button 
          @click="openCreateProject"
          class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium"
        >
          <PlusIcon class="w-5 h-5 mr-2" />
          Create New Project
        </Button>
        
        <Button 
          @click="openModelManagement"
          variant="secondary"
          class="px-6 py-3 rounded-lg font-medium"
        >
          <CpuChipIcon class="w-5 h-5 mr-2" />
          Model Management
        </Button>
        
        <Button 
          @click="viewAllNodes"
          variant="secondary" 
          class="px-6 py-3 rounded-lg font-medium"
        >
          <ServerIcon class="w-5 h-5 mr-2" />
          View All Nodes
        </Button>
      </div>

      <!-- Project List -->
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useEdgeAIStore } from '@/stores/edgeai'
import { useEdgeAIStats, useEdgeAILifecycle } from '@/composables/useEdgeAI'
import Button from '@/components/ui/Button.vue'
import StatCard from '@/components/ui/StatCard.vue'
import DashboardCard from '@/components/ui/DashboardCard.vue'
import RealtimeMonitor from '@/components/edgeai/RealtimeMonitor.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import { 
  ComputerDesktopIcon,
  ServerIcon,
  CpuChipIcon,
  ChartBarIcon,
  ClockIcon,
  DocumentTextIcon,
  PlusIcon,
  EyeIcon,
  ArrowDownTrayIcon,
  CalendarIcon,
  FolderIcon,
  SignalIcon,
  MagnifyingGlassIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const edgeaiStore = useEdgeAIStore()
const { systemStats, getTotalResources } = useEdgeAIStats()

useEdgeAILifecycle()


const activeNodes = computed(() => systemStats.value.onlineNodes)
const runningTasks = computed(() => systemStats.value.trainingNodes)
const completedTasks = computed(() => systemStats.value.activeProjects)
const avgResponseTime = ref(245)
const offlineNodes = computed(() => systemStats.value.totalNodes - systemStats.value.onlineNodes)

const totalResources = computed(() => getTotalResources())

const systemLogs = ref([
  { id: 1, message: 'Node edge-01 connected successfully', time: 'just now' },
  { id: 2, message: 'Task task-123 execution completed', time: '2 minutes ago' },
  { id: 3, message: 'New edge node added', time: '5 minutes ago' },
  { id: 4, message: 'System performance check completed', time: '10 minutes ago' }
])

// Search and filter state
const searchQuery = ref('')
const statusFilter = ref('')

const projectsList = ref([
  {
    id: 1,
    name: 'Smart Manufacturing Monitor',
    description: 'EdgeAI-based real-time factory equipment monitoring and predictive maintenance',
    status: 'Training',
    progress: 65,
    nodes: 8,
    created: '2024-01-15',
    lastUpdated: '2 hours ago'
  },
  {
    id: 2,
    name: 'Urban Traffic Optimization',
    description: 'Intelligent traffic signal control and flow prediction system',
    status: 'Completed',
    progress: 100,
    nodes: 15,
    created: '2024-01-10',
    lastUpdated: '30 minutes ago'
  },
  {
    id: 3,
    name: 'Medical Image Diagnosis',
    description: 'Distributed medical imaging AI diagnostic system',
    status: 'Training',
    progress: 45,
    nodes: 5,
    created: '2024-01-08',
    lastUpdated: '1 day ago'
  },
  {
    id: 4,
    name: 'Retail Traffic Analysis',
    description: 'Shopping mall traffic analysis and product recommendation system',
    status: 'Training',
    progress: 78,
    nodes: 12,
    created: '2024-01-12',
    lastUpdated: '45 minutes ago'
  },
  {
    id: 5,
    name: 'Agricultural Environment Monitor',
    description: 'Farmland environmental data collection and crop growth prediction',
    status: 'Error',
    progress: 23,
    nodes: 3,
    created: '2024-01-05',
    lastUpdated: '3 hours ago'
  }
])

// Computed property for filtered projects
const filteredProjects = computed(() => {
  let filtered = projectsList.value

  // Filter by search query
  if (searchQuery.value) {
    filtered = filtered.filter(project => 
      project.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      project.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Filter by status
  if (statusFilter.value) {
    filtered = filtered.filter(project => project.status === statusFilter.value)
  }

  return filtered
})

const logout = () => {
  authStore.logout()
  router.push('/')
}

// StatCard click handlers
const viewNodes = () => {
  router.push('/edgeai/all-nodes')
}

const viewTasks = () => {
  router.push('/edgeai/task-manager')
}

const viewCompletedTasks = () => {
  router.push('/edgeai/project-manager')
}

const viewPerformanceMetrics = () => {
  router.push('/edgeai/performance-metrics')
}

// Node Management handlers
const addNewNode = () => {
  router.push('/edgeai/create-project')
}

const viewAllNodes = () => {
  router.push('/edgeai/all-nodes')
}

// System Logs handlers
const viewAllLogs = () => {
  router.push('/edgeai/system-logs')
}

const exportLogs = () => {
  router.push('/edgeai/system-logs')
}

// Additional services handlers
const openScheduler = () => {
  router.push('/edgeai/project-manager')
}

const openPerformanceMonitor = () => {
  router.push('/edgeai/visualization')
}

const openResourceManager = () => {
  router.push('/edgeai/all-nodes')
}

// Project management handlers
const openProjectManager = () => {
  router.push('/edgeai/project-manager')
}

const openImportProject = () => {
  router.push('/edgeai/import-project')
}

// New handler functions
const openCreateProject = () => {
  router.push('/edgeai/create-project')
}

const openModelManagement = () => {
  router.push('/edgeai/model-management')
}

const openProjectVisualization = (project) => {
  router.push(`/edgeai/visualization/${project.id}`)
}

// Utility functions for project display
const getStatusDotColor = (status) => {
  const colors = {
    Training: 'bg-blue-500',
    Completed: 'bg-green-500', 
    Idle: 'bg-gray-500',
    Error: 'bg-red-500'
  }
  return colors[status] || 'bg-gray-500'
}
</script>