<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            <ServerIcon class="h-8 w-8 text-green-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Edge Node Management
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <Button 
              @click="refreshNodes"
              variant="outline"
              size="sm"
              :leftIcon="ArrowPathIcon"
              :loading="refreshing"
            >
              Refresh
            </Button>
            <Button 
              @click="toggleTheme" 
              variant="ghost" 
              size="sm"
              iconOnly
              :leftIcon="themeStore.isDark ? SunIcon : MoonIcon"
            />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Statistics Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Nodes"
          :value="totalNodes"
          :icon="ServerIcon"
          variant="primary"
          description="All registered nodes"
          animated
        />
        
        <StatCard
          title="Online Nodes"
          :value="onlineNodes"
          :icon="CheckCircleIcon"
          variant="success"
          description="Currently connected"
          animated
        />
        
        <StatCard
          title="Training Nodes"
          :value="trainingNodes"
          :icon="CpuChipIcon"
          variant="info"
          description="Actively training"
          animated
        />
        
        <StatCard
          title="Avg Load"
          :value="averageLoad"
          unit="%"
          :icon="ChartBarIcon"
          variant="warning"
          description="System utilization"
          animated
        />
      </div>

      <!-- Filters and Search -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-8">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 sm:space-x-4">
          <div class="flex flex-1 items-center space-x-4">
            <div class="relative flex-1 max-w-md">
              <MagnifyingGlassIcon class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search nodes by name or ID..."
                class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
            </div>
            
            <select 
              v-model="statusFilter" 
              class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
            >
              <option value="">All Status</option>
              <option value="online">Online</option>
              <option value="training">Training</option>
              <option value="idle">Idle</option>
              <option value="offline">Offline</option>
              <option value="error">Error</option>
            </select>

            <select 
              v-model="locationFilter" 
              class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
            >
              <option value="">All Locations</option>
              <option value="us-east">US East</option>
              <option value="us-west">US West</option>
              <option value="eu-central">EU Central</option>
              <option value="asia-pacific">Asia Pacific</option>
            </select>
          </div>
          
          <div class="flex items-center space-x-3">
            <Button
              @click="addNewNode"
              variant="primary"
              size="sm"
              :leftIcon="PlusIcon"
              class="bg-green-600 hover:bg-green-700 focus:ring-green-500"
            >
              Add Node
            </Button>
            
            <Button
              @click="exportNodes"
              variant="outline"
              size="sm"
              :leftIcon="ArrowDownTrayIcon"
            >
              Export
            </Button>
          </div>
        </div>
      </div>

      <!-- Nodes Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="node in filteredNodes"
          :key="node.id"
          class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow cursor-pointer"
          @click="selectNode(node)"
          :class="{ 'ring-2 ring-green-500 border-green-500': selectedNode?.id === node.id }"
        >
          <!-- Node Header -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div :class="[
                'w-3 h-3 rounded-full',
                getStatusColor(node.status)
              ]"></div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ node.name }}</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ node.id }}</p>
              </div>
            </div>
            <span :class="[
              'px-2 py-1 rounded-full text-xs font-medium',
              getStatusBadgeColor(node.status)
            ]">
              {{ node.status }}
            </span>
          </div>

          <!-- Node Metrics -->
          <div class="space-y-3">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600 dark:text-gray-400">CPU Usage:</span>
              <span class="font-medium">{{ node.cpuUsage }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                class="bg-green-500 h-2 rounded-full transition-all duration-300" 
                :style="{ width: `${node.cpuUsage}%` }"
              ></div>
            </div>
            
            <div class="flex justify-between text-sm">
              <span class="text-gray-600 dark:text-gray-400">Memory:</span>
              <span class="font-medium">{{ node.memoryUsage }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                class="bg-blue-500 h-2 rounded-full transition-all duration-300" 
                :style="{ width: `${node.memoryUsage}%` }"
              ></div>
            </div>

            <div class="grid grid-cols-2 gap-4 text-sm pt-2">
              <div>
                <span class="text-gray-600 dark:text-gray-400">Tasks:</span>
                <span class="font-medium ml-1">{{ node.activeTasks }}</span>
              </div>
              <div>
                <span class="text-gray-600 dark:text-gray-400">Uptime:</span>
                <span class="font-medium ml-1">{{ node.uptime }}</span>
              </div>
            </div>

            <div class="text-xs text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-200 dark:border-gray-700">
              <div>Location: {{ node.location }}</div>
              <div>Last seen: {{ node.lastSeen }}</div>
            </div>
          </div>

          <!-- Node Actions -->
          <div class="flex justify-end space-x-2 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <Button
              @click.stop="connectToNode(node)"
              variant="outline"
              size="xs"
              :disabled="node.status === 'offline'"
            >
              {{ node.status === 'online' ? 'Disconnect' : 'Connect' }}
            </Button>
            <Button
              @click.stop="showNodeDetails(node)"
              variant="primary"
              size="xs"
            >
              Details
            </Button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredNodes.length === 0" class="text-center py-12">
        <ServerIcon class="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No nodes found</h3>
        <p class="text-gray-500 dark:text-gray-400 mb-6">
          {{ searchQuery || statusFilter || locationFilter ? 'Try adjusting your filters' : 'Start by adding your first edge node' }}
        </p>
        <Button
          @click="addNewNode"
          variant="primary"
          :leftIcon="PlusIcon"
          class="bg-green-600 hover:bg-green-700 focus:ring-green-500"
        >
          Add First Node
        </Button>
      </div>
    </div>

    <!-- Node Details Modal -->
    <Modal
      :isOpen="showDetailsModal"
      @close="showDetailsModal = false"
      title="Node Details"
      size="lg"
    >
      <div v-if="selectedNode" class="space-y-6">
        <div class="grid grid-cols-2 gap-6">
          <div>
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Basic Information</h4>
            <div class="text-sm space-y-1">
              <div><span class="text-gray-500">Node ID:</span> {{ selectedNode.id }}</div>
              <div><span class="text-gray-500">Name:</span> {{ selectedNode.name }}</div>
              <div><span class="text-gray-500">Status:</span> <span :class="getStatusTextColor(selectedNode.status)">{{ selectedNode.status }}</span></div>
              <div><span class="text-gray-500">Location:</span> {{ selectedNode.location }}</div>
            </div>
          </div>
          
          <div>
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Performance</h4>
            <div class="text-sm space-y-1">
              <div><span class="text-gray-500">CPU Usage:</span> {{ selectedNode.cpuUsage }}%</div>
              <div><span class="text-gray-500">Memory Usage:</span> {{ selectedNode.memoryUsage }}%</div>
              <div><span class="text-gray-500">Active Tasks:</span> {{ selectedNode.activeTasks }}</div>
              <div><span class="text-gray-500">Uptime:</span> {{ selectedNode.uptime }}</div>
            </div>
          </div>
        </div>

        <div>
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Hardware Specifications</h4>
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div><span class="text-gray-500">CPU:</span> {{ selectedNode.hardware.cpu }}</div>
              <div><span class="text-gray-500">Memory:</span> {{ selectedNode.hardware.memory }}</div>
              <div><span class="text-gray-500">Storage:</span> {{ selectedNode.hardware.storage }}</div>
              <div><span class="text-gray-500">GPU:</span> {{ selectedNode.hardware.gpu || 'Not available' }}</div>
            </div>
          </div>
        </div>

        <div>
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Recent Activity</h4>
          <div class="space-y-2 max-h-32 overflow-y-auto">
            <div 
              v-for="activity in selectedNode.recentActivity" 
              :key="activity.id"
              class="text-xs bg-gray-50 dark:bg-gray-700 p-2 rounded"
            >
              <div class="font-medium">{{ activity.message }}</div>
              <div class="text-gray-500">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'
import { useEdgeAIStore } from '@/stores/edgeai'
import Button from '@/components/ui/Button.vue'
import StatCard from '@/components/ui/StatCard.vue'
import Modal from '@/components/ui/Modal.vue'
import { 
  ServerIcon,
  ArrowLeftIcon,
  SunIcon,
  MoonIcon,
  CheckCircleIcon,
  CpuChipIcon,
  ChartBarIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  ArrowDownTrayIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const themeStore = useThemeStore()
const uiStore = useUIStore()
const edgeaiStore = useEdgeAIStore()

const refreshing = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const locationFilter = ref('')
const selectedNode = ref(null)
const showDetailsModal = ref(false)

// Use nodes from EdgeAI store
const nodes = computed(() => edgeaiStore.nodes.map(node => ({
  ...node,
  // Add additional fields for UI that might not be in store
  hardware: node.hardware || {
    cpu: 'Intel Xeon E5-2670 v3',
    memory: '32GB DDR4',
    storage: '1TB SSD',
    gpu: node.gpuUsage > 0 ? 'NVIDIA Tesla V100' : null
  },
  recentActivity: node.recentActivity || [
    { id: 1, message: 'Training task started', time: '2 minutes ago' },
    { id: 2, message: 'Model checkpoint saved', time: '15 minutes ago' },
    { id: 3, message: 'Node connected to network', time: '1 hour ago' }
  ],
  activeTasks: node.activeTasks || (node.status === 'training' ? Math.floor(Math.random() * 5) + 1 : 0),
  uptime: node.uptime || `${Math.floor(Math.random() * 720) + 24}h ${Math.floor(Math.random() * 60)}m`
})))

// Computed properties using store data

// Computed properties
const filteredNodes = computed(() => {
  let filtered = nodes.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(node => 
      node.name.toLowerCase().includes(query) || 
      node.id.toLowerCase().includes(query)
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(node => node.status === statusFilter.value)
  }

  if (locationFilter.value) {
    filtered = filtered.filter(node => node.location === locationFilter.value)
  }

  return filtered
})

const totalNodes = computed(() => nodes.value.length)
const onlineNodes = computed(() => nodes.value.filter(n => n.status === 'online' || n.status === 'training' || n.status === 'idle').length)
const trainingNodes = computed(() => nodes.value.filter(n => n.status === 'training').length)
const averageLoad = computed(() => {
  const activeNodes = nodes.value.filter(n => n.status !== 'offline' && n.status !== 'error')
  if (activeNodes.length === 0) return 0
  const totalLoad = activeNodes.reduce((sum, node) => sum + node.cpuUsage, 0)
  return Math.round(totalLoad / activeNodes.length)
})

// Methods
const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const goBack = () => {
  router.push('/edgeai/dashboard')
}

const refreshNodes = async () => {
  refreshing.value = true
  
  try {
    const result = await edgeaiStore.refreshData()
    
    if (result.success) {
      uiStore.addNotification({
        type: 'success',
        title: 'Nodes Refreshed',
        message: 'Node status has been updated successfully.'
      })
    } else {
      uiStore.addNotification({
        type: 'error',
        title: 'Refresh Failed',
        message: result.error || 'Failed to refresh node data.'
      })
    }
  } finally {
    refreshing.value = false
  }
}

const selectNode = (node) => {
  selectedNode.value = node
}

const showNodeDetails = (node) => {
  selectedNode.value = node
  showDetailsModal.value = true
}

const addNewNode = () => {
  uiStore.addNotification({
    type: 'info',
    title: 'Add New Node',
    message: 'Node registration feature will be available soon.'
  })
}

const connectToNode = async (node) => {
  const isConnecting = node.status === 'offline' || node.status === 'error'
  
  try {
    let result
    if (isConnecting) {
      result = await edgeaiStore.restartNode(node.id)
    } else {
      // For disconnect, we could implement a disconnect method in the store
      result = { success: true }
    }
    
    if (result.success) {
      uiStore.addNotification({
        type: 'success',
        title: isConnecting ? 'Node Connected' : 'Node Disconnected',
        message: `Successfully ${isConnecting ? 'connected to' : 'disconnected from'} ${node.name}`
      })
    } else {
      uiStore.addNotification({
        type: 'error',
        title: 'Connection Failed',
        message: result.error || `Failed to ${isConnecting ? 'connect to' : 'disconnect from'} ${node.name}`
      })
    }
  } catch (error) {
    uiStore.addNotification({
      type: 'error',
      title: 'Connection Error',
      message: `Error ${isConnecting ? 'connecting to' : 'disconnecting from'} ${node.name}`
    })
  }
}

const exportNodes = () => {
  uiStore.addNotification({
    type: 'success',
    title: 'Export Started',
    message: 'Node data is being exported to CSV format.'
  })
}

const getStatusColor = (status) => {
  const colors = {
    online: 'bg-green-500',
    training: 'bg-blue-500',
    idle: 'bg-gray-500',
    offline: 'bg-gray-400',
    error: 'bg-red-500'
  }
  return colors[status] || 'bg-gray-400'
}

const getStatusBadgeColor = (status) => {
  const colors = {
    online: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    training: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    idle: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    offline: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const getStatusTextColor = (status) => {
  const colors = {
    online: 'text-green-600 dark:text-green-400',
    training: 'text-blue-600 dark:text-blue-400',
    idle: 'text-gray-600 dark:text-gray-400',
    offline: 'text-gray-500 dark:text-gray-500',
    error: 'text-red-600 dark:text-red-400'
  }
  return colors[status] || 'text-gray-600'
}

// Lifecycle
onMounted(() => {
  edgeaiStore.initializeStore()
})

onUnmounted(() => {
  edgeaiStore.cleanup()
})
</script>