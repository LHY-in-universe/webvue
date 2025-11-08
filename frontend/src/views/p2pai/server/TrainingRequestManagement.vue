<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Training Request Management</h1>
      <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
        Handle client federated training requests
      </p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-4 gap-4">
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Total Requests</div>
        <div class="text-2xl font-bold">{{ requests.length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Pending</div>
        <div class="text-2xl font-bold text-yellow-600">{{ requests.filter(r => r.status === 'pending').length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Approved</div>
        <div class="text-2xl font-bold text-green-600">{{ requests.filter(r => r.status === 'approved').length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Rejected</div>
        <div class="text-2xl font-bold text-red-600">{{ requests.filter(r => r.status === 'rejected').length }}</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-slate-800 rounded-lg p-4 flex gap-4">
      <Input v-model="searchQuery" placeholder="Search client or project..." class="flex-1" />
      <select v-model="filterType" class="input-base w-40">
        <option value="all">All Types</option>
        <option value="federated">Federated</option>
        <option value="mpc">MPC</option>
      </select>
      <select v-model="filterStatus" class="input-base w-40">
        <option value="all">All Status</option>
        <option value="pending">Pending</option>
        <option value="approved">Approved</option>
        <option value="rejected">Rejected</option>
      </select>
    </div>

    <!-- Request List -->
    <div class="space-y-4">
      <div v-for="request in filteredRequests" :key="request.id"
           class="bg-white dark:bg-slate-800 rounded-lg p-5">
        <!-- Header -->
        <div class="flex justify-between items-start mb-4">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <span :class="getTypeBadge(request.type)">{{ request.type }}</span>
              <span :class="getStatusBadge(request.status)">{{ request.status }}</span>
              <span class="text-xs text-gray-500">{{ formatDate(request.created_time) }}</span>
            </div>
            <h3 class="text-lg font-semibold mb-1">{{ request.project_name }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">{{ request.description }}</p>
          </div>
        </div>

        <!-- Client Info -->
        <div class="grid grid-cols-3 gap-3 mb-4 text-sm">
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-xs text-gray-500">Client</div>
            <div class="font-medium">{{ request.client_name }}</div>
          </div>
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-xs text-gray-500">IP Address</div>
            <div class="font-medium">{{ request.client_ip }}</div>
          </div>
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-xs text-gray-500">Algorithm</div>
            <div class="font-medium">{{ request.requested_config.training_alg }}</div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-2">
          <Button v-if="request.status === 'pending'" @click="approveRequest(request)" variant="success" size="sm">
            Approve
          </Button>
          <Button v-if="request.status === 'pending'" @click="rejectRequest(request)" variant="danger" size="sm">
            Reject
          </Button>
          <Button @click="viewDetails(request)" variant="outline" size="sm">Details</Button>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <Modal v-model:isOpen="showDetailsModal" title="Request Details" size="lg">
      <div v-if="selectedRequest" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <div class="text-sm text-gray-500">Client Name</div>
            <div class="font-medium">{{ selectedRequest.client_name }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">IP Address</div>
            <div class="font-medium">{{ selectedRequest.client_ip }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Type</div>
            <span :class="getTypeBadge(selectedRequest.type)">{{ selectedRequest.type }}</span>
          </div>
          <div>
            <div class="text-sm text-gray-500">Status</div>
            <span :class="getStatusBadge(selectedRequest.status)">{{ selectedRequest.status }}</span>
          </div>
        </div>
        <div>
          <div class="text-sm text-gray-500 mb-1">Project Name</div>
          <div class="font-medium">{{ selectedRequest.project_name }}</div>
        </div>
        <div>
          <div class="text-sm text-gray-500 mb-1">Description</div>
          <div class="text-sm">{{ selectedRequest.description }}</div>
        </div>
        <div>
          <div class="text-sm font-medium mb-2">Requested Configuration</div>
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div v-for="(value, key) in selectedRequest.requested_config" :key="key"
                 class="bg-slate-50 dark:bg-slate-700 rounded p-2">
              <div class="text-xs text-gray-500">{{ formatKey(key) }}</div>
              <div class="font-medium">{{ value }}</div>
            </div>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div class="text-xs text-gray-500">Request Time</div>
            <div>{{ formatDate(selectedRequest.created_time) }}</div>
          </div>
          <div>
            <div class="text-xs text-gray-500">Last Updated</div>
            <div>{{ formatDate(selectedRequest.updated_time) }}</div>
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

const uiStore = useUIStore()

// Data
const requests = ref([
  {
    id: 1,
    client_id: 4,
    client_name: 'Client-004',
    client_ip: '192.168.1.104',
    type: 'federated',
    project_name: 'FL Text Sentiment Analysis',
    description: 'BERT-based multilingual sentiment analysis',
    requested_config: {
      training_alg: 'FedAvg',
      num_rounds: 80,
      batch_size: 32,
      lr: 0.0001,
      num_clients: 4,
      model_name_or_path: 'bert-base'
    },
    status: 'pending',
    created_time: new Date('2024-02-10'),
    updated_time: new Date('2024-02-10')
  },
  {
    id: 2,
    client_id: 5,
    client_name: 'Client-005',
    client_ip: '192.168.1.105',
    type: 'mpc',
    project_name: 'MPC Joint Statistical Analysis',
    description: 'Multi-party secure computation',
    requested_config: {
      training_alg: 'SecureAgg',
      num_rounds: 20,
      threshold: 3,
      num_clients: 3
    },
    status: 'pending',
    created_time: new Date('2024-02-09'),
    updated_time: new Date('2024-02-09')
  },
  {
    id: 3,
    client_id: 6,
    client_name: 'Client-006',
    client_ip: '192.168.1.106',
    type: 'federated',
    project_name: 'FL Recommendation System',
    description: 'Federated recommendation model',
    requested_config: {
      training_alg: 'FedProx',
      num_rounds: 60,
      batch_size: 128,
      lr: 0.001,
      num_clients: 5
    },
    status: 'approved',
    ray_id: 1,
    created_time: new Date('2024-02-08'),
    updated_time: new Date('2024-02-09')
  }
])

// State
const searchQuery = ref('')
const filterType = ref('all')
const filterStatus = ref('all')
const showDetailsModal = ref(false)
const selectedRequest = ref(null)

// Computed
const filteredRequests = computed(() => {
  return requests.value.filter(r => {
    const searchLower = searchQuery.value.toLowerCase()
    const matchSearch = r.client_name.toLowerCase().includes(searchLower) ||
                       r.project_name.toLowerCase().includes(searchLower)
    const matchType = filterType.value === 'all' || r.type === filterType.value
    const matchStatus = filterStatus.value === 'all' || r.status === filterStatus.value
    return matchSearch && matchType && matchStatus
  })
})

// Methods
const getTypeBadge = (type) => {
  return type === 'federated'
    ? 'px-2 py-1 bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300 text-xs rounded'
    : 'px-2 py-1 bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300 text-xs rounded'
}

const getStatusBadge = (status) => {
  const badges = {
    pending: 'px-2 py-1 bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300 text-xs rounded',
    approved: 'px-2 py-1 bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 text-xs rounded',
    rejected: 'px-2 py-1 bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300 text-xs rounded'
  }
  return badges[status] || badges.pending
}

const formatDate = (date) => new Date(date).toLocaleDateString()

const formatKey = (key) => {
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

const viewDetails = (request) => {
  selectedRequest.value = request
  showDetailsModal.value = true
}

const approveRequest = (request) => {
  request.status = 'approved'
  request.updated_time = new Date()
  uiStore.addNotification({ type: 'success', message: 'Request approved' })
}

const rejectRequest = (request) => {
  request.status = 'rejected'
  request.updated_time = new Date()
  uiStore.addNotification({ type: 'info', message: 'Request rejected' })
}
</script>
