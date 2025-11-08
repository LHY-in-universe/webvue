<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Server Project Management</h1>
        <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
          Manage federated learning and MPC training projects
        </p>
      </div>
      <Button @click="showCreateModal = true" variant="primary">
        Create Project
      </Button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-4 gap-4">
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Total Projects</div>
        <div class="text-2xl font-bold">{{ projects.length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Training</div>
        <div class="text-2xl font-bold text-green-600">{{ projects.filter(p => p.status === 'training').length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Pending</div>
        <div class="text-2xl font-bold text-yellow-600">{{ projects.filter(p => p.status === 'pending').length }}</div>
      </div>
      <div class="bg-white dark:bg-slate-800 rounded-lg p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Completed</div>
        <div class="text-2xl font-bold text-blue-600">{{ projects.filter(p => p.status === 'completed').length }}</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-slate-800 rounded-lg p-4 flex gap-4">
      <Input v-model="searchQuery" placeholder="Search projects..." class="flex-1" />
      <select v-model="filterType" class="input-base w-40">
        <option value="all">All Types</option>
        <option value="federated">Federated</option>
        <option value="mpc">MPC</option>
      </select>
      <select v-model="filterStatus" class="input-base w-40">
        <option value="all">All Status</option>
        <option value="pending">Pending</option>
        <option value="training">Training</option>
        <option value="completed">Completed</option>
      </select>
    </div>

    <!-- Project List -->
    <div class="grid grid-cols-2 gap-4">
      <div v-for="project in filteredProjects" :key="project.id"
           class="bg-white dark:bg-slate-800 rounded-lg p-5">
        <!-- Header -->
        <div class="mb-4">
          <div class="flex items-center gap-2 mb-1">
            <span :class="getTypeBadge(project.type)">{{ project.type }}</span>
            <span :class="getStatusBadge(project.status)">{{ project.status }}</span>
          </div>
          <h3 class="text-lg font-semibold">{{ project.name }}</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ project.description }}</p>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-3 gap-2 mb-4 text-sm">
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-xs text-gray-500">Cluster</div>
            <div class="font-medium">{{ project.ray_name }}</div>
          </div>
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-xs text-gray-500">Algorithm</div>
            <div class="font-medium">{{ project.fed_alg || project.training_alg }}</div>
          </div>
          <div class="bg-slate-50 dark:bg-slate-700 rounded p-2">
            <div class="text-xs text-gray-500">Progress</div>
            <div class="font-medium">{{ project.progress }}%</div>
          </div>
        </div>

        <!-- Progress Bar -->
        <ProgressBar :percentage="project.progress" :animated="project.status === 'training'" class="mb-4" />

        <!-- Actions -->
        <div class="flex gap-2">
          <Button @click="viewDetails(project)" variant="outline" size="sm">Details</Button>
          <Button @click="editProject(project)" variant="primary" size="sm">Edit</Button>
          <Button @click="deleteProject(project)" variant="danger" size="sm">Delete</Button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <Modal v-model:isOpen="showCreateModal" :title="isEditing ? 'Edit Project' : 'Create Project'" size="lg">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">Project Name</label>
          <Input v-model="formData.name" placeholder="e.g., FL Medical Classification" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Description</label>
          <Textarea v-model="formData.description" rows="2" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">Type</label>
            <select v-model="formData.type" class="input-base">
              <option value="federated">Federated Learning</option>
              <option value="mpc">Multi-Party Computation</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Ray Cluster</label>
            <select v-model="formData.ray_id" class="input-base">
              <option v-for="ray in availableRays" :key="ray.id" :value="ray.id">{{ ray.name }}</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">Model</label>
            <Input v-model="formData.model_name_or_path" placeholder="e.g., resnet50" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Learning Rate</label>
            <Input v-model.number="formData.lr" type="number" step="0.0001" />
          </div>
        </div>
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">Batch Size</label>
            <Input v-model.number="formData.batch_size" type="number" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Rounds</label>
            <Input v-model.number="formData.num_rounds" type="number" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">Clients</label>
            <Input v-model.number="formData.num_clients" type="number" />
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button @click="cancelEdit" variant="ghost">Cancel</Button>
          <Button @click="saveProject" variant="primary">{{ isEditing ? 'Save' : 'Create' }}</Button>
        </div>
      </template>
    </Modal>

    <!-- Details Modal -->
    <Modal v-model:isOpen="showDetailsModal" title="Project Details" size="xl">
      <div v-if="selectedProject" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <div class="text-sm text-gray-500">Project Name</div>
            <div class="font-medium">{{ selectedProject.name }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Type</div>
            <span :class="getTypeBadge(selectedProject.type)">{{ selectedProject.type }}</span>
          </div>
          <div>
            <div class="text-sm text-gray-500">Status</div>
            <span :class="getStatusBadge(selectedProject.status)">{{ selectedProject.status }}</span>
          </div>
          <div>
            <div class="text-sm text-gray-500">Ray Cluster</div>
            <div class="font-medium">{{ selectedProject.ray_name }}</div>
          </div>
        </div>
        <div>
          <div class="text-sm text-gray-500 mb-1">Description</div>
          <div class="text-sm">{{ selectedProject.description }}</div>
        </div>
        <div class="grid grid-cols-3 gap-4">
          <div>
            <div class="text-sm text-gray-500">Training Algorithm</div>
            <div class="font-medium">{{ selectedProject.training_alg }}</div>
          </div>
          <div v-if="selectedProject.fed_alg">
            <div class="text-sm text-gray-500">Fed Algorithm</div>
            <div class="font-medium">{{ selectedProject.fed_alg }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Model</div>
            <div class="font-medium">{{ selectedProject.model_name_or_path }}</div>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-4 text-sm">
          <div>
            <div class="text-xs text-gray-500">Batch Size</div>
            <div class="font-medium">{{ selectedProject.batch_size }}</div>
          </div>
          <div>
            <div class="text-xs text-gray-500">Learning Rate</div>
            <div class="font-medium">{{ selectedProject.lr }}</div>
          </div>
          <div>
            <div class="text-xs text-gray-500">Rounds</div>
            <div class="font-medium">{{ selectedProject.num_rounds }}</div>
          </div>
          <div>
            <div class="text-xs text-gray-500">Clients</div>
            <div class="font-medium">{{ selectedProject.num_clients }}</div>
          </div>
        </div>
        <div>
          <div class="text-sm font-medium mb-2">Progress</div>
          <ProgressBar :percentage="selectedProject.progress" :animated="selectedProject.status === 'training'" />
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
import ProgressBar from '@/components/ui/ProgressBar.vue'

const uiStore = useUIStore()

// Data
const projects = ref([
  {
    id: 1,
    ray_id: 1,
    ray_name: 'Ray Cluster Alpha',
    type: 'federated',
    name: 'FL Medical Image Classification',
    description: 'Medical image classification with privacy protection',
    training_alg: 'FedAvg',
    fed_alg: 'FedAvg',
    num_rounds: 100,
    batch_size: 32,
    lr: 0.001,
    num_clients: 3,
    model_name_or_path: 'resnet50',
    status: 'training',
    progress: 45.5
  },
  {
    id: 2,
    ray_id: 1,
    ray_name: 'Ray Cluster Alpha',
    type: 'federated',
    name: 'FL Financial Risk Model',
    description: 'Multi-bank risk assessment model',
    training_alg: 'FedProx',
    fed_alg: 'FedProx',
    num_rounds: 50,
    batch_size: 64,
    lr: 0.0005,
    num_clients: 3,
    model_name_or_path: 'lstm',
    status: 'pending',
    progress: 0
  },
  {
    id: 3,
    ray_id: 2,
    ray_name: 'Ray Cluster Beta',
    type: 'mpc',
    name: 'MPC Data Analysis',
    description: 'Secure multi-party data analysis',
    training_alg: 'SecureAgg',
    fed_alg: null,
    num_rounds: 20,
    batch_size: 16,
    lr: 0.01,
    num_clients: 3,
    model_name_or_path: 'linear_regression',
    status: 'completed',
    progress: 100
  }
])

const availableRays = ref([
  { id: 1, name: 'Ray Cluster Alpha', status: 'running' },
  { id: 2, name: 'Ray Cluster Beta', status: 'idle' }
])

// State
const searchQuery = ref('')
const filterType = ref('all')
const filterStatus = ref('all')
const showCreateModal = ref(false)
const showDetailsModal = ref(false)
const selectedProject = ref(null)
const isEditing = ref(false)
const formData = ref({
  name: '',
  description: '',
  type: 'federated',
  ray_id: 1,
  model_name_or_path: '',
  lr: 0.001,
  batch_size: 32,
  num_rounds: 100,
  num_clients: 3
})

// Computed
const filteredProjects = computed(() => {
  return projects.value.filter(p => {
    const matchSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchType = filterType.value === 'all' || p.type === filterType.value
    const matchStatus = filterStatus.value === 'all' || p.status === filterStatus.value
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
    training: 'px-2 py-1 bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300 text-xs rounded',
    pending: 'px-2 py-1 bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300 text-xs rounded',
    completed: 'px-2 py-1 bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300 text-xs rounded'
  }
  return badges[status] || badges.pending
}

const viewDetails = (project) => {
  selectedProject.value = project
  showDetailsModal.value = true
}

const editProject = (project) => {
  isEditing.value = true
  formData.value = { ...project }
  showCreateModal.value = true
}

const cancelEdit = () => {
  showCreateModal.value = false
  isEditing.value = false
  formData.value = {
    name: '',
    description: '',
    type: 'federated',
    ray_id: 1,
    model_name_or_path: '',
    lr: 0.001,
    batch_size: 32,
    num_rounds: 100,
    num_clients: 3
  }
}

const saveProject = () => {
  if (!formData.value.name) {
    uiStore.addNotification({ type: 'error', message: 'Please enter project name' })
    return
  }

  if (isEditing.value) {
    const index = projects.value.findIndex(p => p.id === formData.value.id)
    if (index !== -1) {
      projects.value[index] = { ...formData.value }
      uiStore.addNotification({ type: 'success', message: 'Project updated' })
    }
  } else {
    const ray = availableRays.value.find(r => r.id === formData.value.ray_id)
    const project = {
      ...formData.value,
      id: projects.value.length + 1,
      ray_name: ray.name,
      status: 'pending',
      progress: 0,
      training_alg: formData.value.type === 'federated' ? 'FedAvg' : 'SecureAgg'
    }
    projects.value.push(project)
    uiStore.addNotification({ type: 'success', message: 'Project created' })
  }

  cancelEdit()
}

const deleteProject = (project) => {
  const index = projects.value.findIndex(p => p.id === project.id)
  if (index !== -1) {
    projects.value.splice(index, 1)
    uiStore.addNotification({ type: 'success', message: 'Project deleted' })
  }
}
</script>
