<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Server Model Management</h1>
      <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
        Manage trained model files
      </p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-4 gap-4">
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Total Models</div>
        <div class="text-2xl font-bold">{{ models.length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Completed</div>
        <div class="text-2xl font-bold text-green-600">{{ models.filter(m => m.status === 'completed').length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Training</div>
        <div class="text-2xl font-bold text-yellow-600">{{ models.filter(m => m.status === 'training').length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Total Size</div>
        <div class="text-2xl font-bold text-blue-600">{{ totalSize.toFixed(2) }} GB</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-slate-800 rounded-lg p-4 flex gap-4">
      <Input v-model="searchQuery" placeholder="Search models..." class="flex-1" />
      <select v-model="filterStatus" class="input-base w-40">
        <option value="all">All Status</option>
        <option value="completed">Completed</option>
        <option value="training">Training</option>
      </select>
      <select v-model="sortBy" class="input-base w-40">
        <option value="created_time">Created Time</option>
        <option value="accuracy">Accuracy</option>
        <option value="size">File Size</option>
      </select>
    </div>

    <!-- Model List -->
    <div class="grid grid-cols-2 gap-4">
      <div v-for="model in filteredModels" :key="model.id"
           class="bg-white dark:bg-slate-800 rounded-lg p-5">
        <!-- Header -->
        <div class="mb-4">
          <div class="flex items-center gap-2 mb-1">
            <span :class="getStatusBadge(model.status)">{{ model.status }}</span>
            <span class="text-xs text-gray-500">v{{ model.version }}</span>
          </div>
          <h3 class="text-lg font-semibold mb-1">{{ model.name }}</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ model.description }}</p>
        </div>

        <!-- Info -->
        <div class="grid grid-cols-2 gap-3 mb-4 text-sm">
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-xs text-gray-500">Project</div>
            <div class="font-medium">{{ model.project_name }}</div>
          </div>
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-xs text-gray-500">Accuracy</div>
            <div class="font-medium text-green-600">{{ model.accuracy }}%</div>
          </div>
        </div>

        <!-- Metrics -->
        <div class="grid grid-cols-3 gap-2 mb-4 text-xs">
          <div class="text-center bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-gray-500">Size</div>
            <div class="font-medium">{{ model.size }} MB</div>
          </div>
          <div class="text-center bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-gray-500">Epochs</div>
            <div class="font-medium">{{ model.epochs }}</div>
          </div>
          <div class="text-center bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-gray-500">Created</div>
            <div class="font-medium">{{ formatDate(model.created_time) }}</div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-2">
          <Button @click="viewDetails(model)" variant="outline" size="sm">Details</Button>
          <Button @click="downloadModel(model)" variant="primary" size="sm" :disabled="model.status !== 'completed'">
            Download
          </Button>
          <Button @click="deleteModel(model)" variant="danger" size="sm">Delete</Button>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <Modal v-model:isOpen="showDetailsModal" title="Model Details" size="lg">
      <div v-if="selectedModel" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <div class="text-sm text-gray-500">Model Name</div>
            <div class="font-medium">{{ selectedModel.name }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Version</div>
            <div class="font-medium">v{{ selectedModel.version }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Status</div>
            <span :class="getStatusBadge(selectedModel.status)">{{ selectedModel.status }}</span>
          </div>
          <div>
            <div class="text-sm text-gray-500">Project</div>
            <div class="font-medium">{{ selectedModel.project_name }}</div>
          </div>
        </div>
        <div>
          <div class="text-sm text-gray-500 mb-1">Description</div>
          <div class="text-sm">{{ selectedModel.description }}</div>
        </div>
        <div class="grid grid-cols-4 gap-4 text-sm">
          <div>
            <div class="text-xs text-gray-500">Accuracy</div>
            <div class="font-medium text-green-600">{{ selectedModel.accuracy }}%</div>
          </div>
          <div>
            <div class="text-xs text-gray-500">Loss</div>
            <div class="font-medium text-red-600">{{ selectedModel.loss }}</div>
          </div>
          <div>
            <div class="text-xs text-gray-500">File Size</div>
            <div class="font-medium">{{ selectedModel.size }} MB</div>
          </div>
          <div>
            <div class="text-xs text-gray-500">Epochs</div>
            <div class="font-medium">{{ selectedModel.epochs }}</div>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div class="text-xs text-gray-500">Architecture</div>
            <div class="font-medium">{{ selectedModel.architecture }}</div>
          </div>
          <div>
            <div class="text-xs text-gray-500">Framework</div>
            <div class="font-medium">{{ selectedModel.framework }}</div>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <div class="text-xs text-gray-500">Created</div>
            <div>{{ formatDate(selectedModel.created_time) }}</div>
          </div>
          <div>
            <div class="text-xs text-gray-500">Updated</div>
            <div>{{ formatDate(selectedModel.updated_time) }}</div>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button @click="showDetailsModal = false" variant="ghost">Close</Button>
          <Button @click="downloadModel(selectedModel)" variant="primary" :disabled="selectedModel.status !== 'completed'">
            Download
          </Button>
        </div>
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
const models = ref([
  {
    id: 1,
    name: 'FL Medical ResNet Model',
    version: '1.0.0',
    description: 'Federated medical image classification model',
    project_name: 'FL Medical Image Classification',
    status: 'completed',
    accuracy: 94.5,
    loss: 0.123,
    size: 245.6,
    epochs: 100,
    architecture: 'ResNet-50',
    framework: 'PyTorch',
    created_time: new Date('2024-02-01'),
    updated_time: new Date('2024-02-10')
  },
  {
    id: 2,
    name: 'FL Financial LSTM Model',
    version: '2.1.0',
    description: 'Financial risk prediction model',
    project_name: 'FL Financial Risk Model',
    status: 'training',
    accuracy: 87.2,
    loss: 0.245,
    size: 128.4,
    epochs: 50,
    architecture: 'LSTM',
    framework: 'TensorFlow',
    created_time: new Date('2024-02-05'),
    updated_time: new Date('2024-02-10')
  },
  {
    id: 3,
    name: 'MPC Linear Regression Model',
    version: '1.0.0',
    description: 'Secure multi-party computation model',
    project_name: 'MPC Data Analysis',
    status: 'completed',
    accuracy: 91.8,
    loss: 0.089,
    size: 45.2,
    epochs: 20,
    architecture: 'Linear Regression',
    framework: 'PyTorch',
    created_time: new Date('2024-01-28'),
    updated_time: new Date('2024-02-08')
  }
])

// State
const searchQuery = ref('')
const filterStatus = ref('all')
const sortBy = ref('created_time')
const showDetailsModal = ref(false)
const selectedModel = ref(null)

// Computed
const totalSize = computed(() => {
  return models.value.reduce((sum, m) => sum + m.size, 0) / 1024
})

const filteredModels = computed(() => {
  let filtered = models.value.filter(m => {
    const matchSearch = m.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchStatus = filterStatus.value === 'all' || m.status === filterStatus.value
    return matchSearch && matchStatus
  })

  // Sort
  filtered.sort((a, b) => {
    if (sortBy.value === 'accuracy') return b.accuracy - a.accuracy
    if (sortBy.value === 'size') return b.size - a.size
    return b.created_time - a.created_time
  })

  return filtered
})

// Methods
const getStatusBadge = (status) => {
  const badges = {
    completed: 'px-2 py-1 bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 text-xs rounded',
    training: 'px-2 py-1 bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300 text-xs rounded'
  }
  return badges[status] || badges.training
}

const formatDate = (date) => new Date(date).toLocaleDateString()

const viewDetails = (model) => {
  selectedModel.value = model
  showDetailsModal.value = true
}

const downloadModel = (model) => {
  if (model.status !== 'completed') {
    uiStore.addNotification({ type: 'warning', message: 'Model is not ready for download' })
    return
  }
  uiStore.addNotification({ type: 'success', message: `Downloading ${model.name}...` })
}

const deleteModel = (model) => {
  const index = models.value.findIndex(m => m.id === model.id)
  if (index !== -1) {
    models.value.splice(index, 1)
    uiStore.addNotification({ type: 'success', message: 'Model deleted' })
  }
}
</script>
