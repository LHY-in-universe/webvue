<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Ray Cluster Management</h1>
        <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
          Create and manage Ray clusters for federated training
        </p>
      </div>
      <Button @click="showCreateModal = true" variant="primary">
        Create Cluster
      </Button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-4 gap-4">
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Total Clusters</div>
        <div class="text-2xl font-bold">{{ clusters.length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Running</div>
        <div class="text-2xl font-bold text-green-600">{{ clusters.filter(c => c.status === 'running').length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Idle</div>
        <div class="text-2xl font-bold text-gray-600">{{ clusters.filter(c => c.status === 'idle').length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Total Clients</div>
        <div class="text-2xl font-bold text-blue-600">{{ totalClients }}</div>
      </div>
    </div>

    <!-- Cluster List -->
    <div v-if="clusters.length > 0" class="space-y-4">
      <div v-for="cluster in clusters" :key="cluster.id"
           class="bg-white dark:bg-slate-800 rounded-lg p-5">
        <!-- Header -->
        <div class="flex justify-between items-start mb-4">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ cluster.name }}</h3>
              <span :class="getStatusBadge(cluster.status)">
                {{ cluster.status }}
              </span>
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400">{{ cluster.description }}</p>
          </div>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-3 gap-3 mb-4">
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-3 text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400">Clients</div>
            <div class="text-lg font-bold">{{ cluster.clients.length }}</div>
          </div>
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-3 text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400">Projects</div>
            <div class="text-lg font-bold">{{ cluster.project_count }}</div>
          </div>
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-3 text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400">Created</div>
            <div class="text-xs font-medium">{{ formatDate(cluster.created_time) }}</div>
          </div>
        </div>

        <!-- Clients -->
        <div v-if="cluster.clients.length > 0" class="mb-4">
          <h4 class="text-sm font-medium mb-2">Connected Clients</h4>
          <div class="grid grid-cols-2 gap-2">
            <div v-for="client in cluster.clients" :key="client.id"
                 class="flex items-center gap-2 p-2 bg-slate-50 dark:bg-slate-700 rounded text-sm">
              <div :class="client.status === 'connected' ? 'bg-green-500' : 'bg-gray-400'"
                   class="w-2 h-2 rounded-full"></div>
              <div class="flex-1">
                <div class="font-medium">{{ client.name }}</div>
                <div class="text-xs text-gray-500">{{ client.ipv4 }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-2">
          <Button v-if="cluster.status === 'idle'" @click="startCluster(cluster)" variant="success" size="sm">
            Start
          </Button>
          <Button v-else-if="cluster.status === 'running'" @click="stopCluster(cluster)" variant="warning" size="sm">
            Stop
          </Button>
          <Button @click="viewDetails(cluster)" variant="outline" size="sm">
            Details
          </Button>
          <Button @click="deleteCluster(cluster)" variant="danger" size="sm" :disabled="cluster.project_count > 0">
            Delete
          </Button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-white dark:bg-slate-800 rounded-lg p-12 text-center">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">No Ray Clusters</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-4">Create your first cluster to start federated training</p>
      <Button @click="showCreateModal = true" variant="primary">Create Cluster</Button>
    </div>

    <!-- Create Modal -->
    <Modal v-model:isOpen="showCreateModal" title="Create Ray Cluster">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Cluster Name</label>
          <Input v-model="newCluster.name" placeholder="e.g., Ray Cluster Alpha" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Description</label>
          <Textarea v-model="newCluster.description" placeholder="Describe the cluster purpose..." rows="2" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Select Clients</label>
          <div class="max-h-48 overflow-y-auto border rounded p-2 space-y-2">
            <div v-for="client in availableClients" :key="client.id" class="flex items-center gap-2">
              <input type="checkbox" :id="`client-${client.id}`" v-model="newCluster.selectedClients" :value="client" class="rounded" />
              <label :for="`client-${client.id}`" class="flex-1 text-sm cursor-pointer">
                <span class="font-medium">{{ client.name }}</span>
                <span class="text-gray-500 text-xs ml-2">{{ client.ipv4 }}</span>
              </label>
            </div>
          </div>
          <p class="text-xs text-gray-500 mt-2">Selected: {{ newCluster.selectedClients.length }}</p>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button @click="cancelCreate" variant="ghost">Cancel</Button>
          <Button @click="createCluster" variant="primary" :disabled="!newCluster.name">Create</Button>
        </div>
      </template>
    </Modal>

    <!-- Details Modal -->
    <Modal v-model:isOpen="showDetailsModal" title="Cluster Details" size="lg">
      <div v-if="selectedCluster" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <div class="text-sm text-gray-500">Cluster Name</div>
            <div class="font-medium">{{ selectedCluster.name }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Status</div>
            <span :class="getStatusBadge(selectedCluster.status)">{{ selectedCluster.status }}</span>
          </div>
          <div>
            <div class="text-sm text-gray-500">Created</div>
            <div class="font-medium">{{ formatDate(selectedCluster.created_time) }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Projects</div>
            <div class="font-medium">{{ selectedCluster.project_count }}</div>
          </div>
        </div>
        <div>
          <div class="text-sm text-gray-500 mb-2">Description</div>
          <div class="text-sm">{{ selectedCluster.description }}</div>
        </div>
        <div>
          <div class="text-sm font-medium mb-2">Clients ({{ selectedCluster.clients.length }})</div>
          <div class="space-y-2">
            <div v-for="client in selectedCluster.clients" :key="client.id"
                 class="flex items-center justify-between p-2 bg-slate-50 dark:bg-slate-700 rounded">
              <div class="flex items-center gap-2">
                <div :class="client.status === 'connected' ? 'bg-green-500' : 'bg-gray-400'" class="w-2 h-2 rounded-full"></div>
                <div>
                  <div class="text-sm font-medium">{{ client.name }}</div>
                  <div class="text-xs text-gray-500">{{ client.ipv4 }}</div>
                </div>
              </div>
              <Button @click="removeClient(client)" variant="danger" size="sm">Remove</Button>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <Button @click="showDetailsModal = false" variant="primary">Close</Button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUIStore } from '@/stores/ui'
import Button from '@/components/ui/Button.vue'
import Modal from '@/components/ui/Modal.vue'
import Input from '@/components/ui/Input.vue'
import Textarea from '@/components/ui/Textarea.vue'

const uiStore = useUIStore()

// Data
const clusters = ref([
  {
    id: 1,
    name: 'Ray Cluster Alpha',
    description: 'Primary training cluster for large-scale federated learning',
    status: 'running',
    created_time: new Date('2024-01-15'),
    clients: [
      { id: 1, name: 'Client-001', ipv4: '192.168.1.101', status: 'connected' },
      { id: 2, name: 'Client-002', ipv4: '192.168.1.102', status: 'connected' },
      { id: 3, name: 'Client-003', ipv4: '192.168.1.103', status: 'connected' }
    ],
    project_count: 2
  },
  {
    id: 2,
    name: 'Ray Cluster Beta',
    description: 'MPC cluster for high-security training',
    status: 'idle',
    created_time: new Date('2024-01-20'),
    clients: [
      { id: 4, name: 'Client-004', ipv4: '192.168.1.104', status: 'connected' },
      { id: 5, name: 'Client-005', ipv4: '192.168.1.105', status: 'idle' }
    ],
    project_count: 1
  }
])

const availableClients = ref([
  { id: 6, name: 'Client-006', ipv4: '192.168.1.106' },
  { id: 7, name: 'Client-007', ipv4: '192.168.1.107' },
  { id: 8, name: 'Client-008', ipv4: '192.168.1.108' }
])

// State
const showCreateModal = ref(false)
const showDetailsModal = ref(false)
const selectedCluster = ref(null)
const newCluster = ref({ name: '', description: '', selectedClients: [] })

// Computed
const totalClients = computed(() => {
  return clusters.value.reduce((sum, c) => sum + c.clients.length, 0)
})

// Methods
const getStatusBadge = (status) => {
  const badges = {
    running: 'px-2 py-1 bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 text-xs rounded',
    idle: 'px-2 py-1 bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300 text-xs rounded',
    stopped: 'px-2 py-1 bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300 text-xs rounded'
  }
  return badges[status] || badges.idle
}

const formatDate = (date) => new Date(date).toLocaleDateString()

const createCluster = () => {
  if (!newCluster.value.name) {
    uiStore.addNotification({ type: 'error', message: 'Please enter cluster name' })
    return
  }

  const cluster = {
    id: clusters.value.length + 1,
    name: newCluster.value.name,
    description: newCluster.value.description,
    status: 'idle',
    created_time: new Date(),
    clients: newCluster.value.selectedClients.map(c => ({ ...c, status: 'connected' })),
    project_count: 0
  }

  clusters.value.push(cluster)
  uiStore.addNotification({ type: 'success', message: `Cluster "${cluster.name}" created` })
  cancelCreate()
}

const cancelCreate = () => {
  showCreateModal.value = false
  newCluster.value = { name: '', description: '', selectedClients: [] }
}

const startCluster = (cluster) => {
  cluster.status = 'running'
  uiStore.addNotification({ type: 'success', message: `Cluster "${cluster.name}" started` })
}

const stopCluster = (cluster) => {
  cluster.status = 'stopped'
  uiStore.addNotification({ type: 'info', message: `Cluster "${cluster.name}" stopped` })
}

const viewDetails = (cluster) => {
  selectedCluster.value = cluster
  showDetailsModal.value = true
}

const removeClient = (client) => {
  const cluster = selectedCluster.value
  const index = cluster.clients.findIndex(c => c.id === client.id)
  if (index !== -1) {
    cluster.clients.splice(index, 1)
    uiStore.addNotification({ type: 'success', message: `Client "${client.name}" removed` })
  }
}

const deleteCluster = (cluster) => {
  if (cluster.project_count > 0) {
    uiStore.addNotification({ type: 'error', message: 'Cannot delete cluster with projects' })
    return
  }

  const index = clusters.value.findIndex(c => c.id === cluster.id)
  if (index !== -1) {
    clusters.value.splice(index, 1)
    uiStore.addNotification({ type: 'success', message: `Cluster "${cluster.name}" deleted` })
  }
}
</script>
