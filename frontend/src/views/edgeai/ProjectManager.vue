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
            <FolderIcon class="h-8 w-8 text-green-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Project Management
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <Button 
              @click="createNewProject"
              variant="primary"
              size="sm"
              :leftIcon="PlusIcon"
              class="bg-green-600 hover:bg-green-700 focus:ring-green-500"
            >
              New Project
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
          title="Total Projects"
          :value="totalProjects"
          :icon="FolderIcon"
          variant="primary"
          description="All registered projects"
          @click="resetFilters"
        />
        <StatCard
          title="Active Projects"
          :value="activeProjects"
          :icon="PlayIcon"
          variant="success"
          description="Currently running"
          @click="statusFilter = 'training'"
        />
        <StatCard
          title="Completed"
          :value="completedProjects"
          :icon="CheckCircleIcon"
          variant="info"
          description="Successfully finished"
          @click="statusFilter = 'completed'"
        />
        <StatCard
          title="Success Rate"
          :value="`${successRate}%`"
          :icon="ChartBarIcon"
          variant="warning"
          description="Overall completion rate"
        />
      </div>

      <!-- Filter and Search Bar -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-8">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-4">
            <div class="relative">
              <MagnifyingGlassIcon class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search projects..."
                class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
            </div>
            
            <select 
              v-model="statusFilter"
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
            >
              <option value="">All Status</option>
              <option value="training">Training</option>
              <option value="active">Active</option>
              <option value="paused">Paused</option>
              <option value="completed">Completed</option>
              <option value="error">Error</option>
            </select>

            <select 
              v-model="typeFilter"
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
            >
              <option value="">All Types</option>
              <option value="manufacturing">Manufacturing</option>
              <option value="traffic">Traffic</option>
              <option value="medical">Medical</option>
              <option value="retail">Retail</option>
              <option value="automotive">Automotive</option>
            </select>
          </div>

          <div class="flex items-center space-x-2">
            <Button @click="refreshProjects" variant="outline" size="sm" :loading="refreshing">
              <ArrowPathIcon class="w-4 h-4 mr-2" />
              Refresh
            </Button>
            <Button @click="exportProjects" variant="outline" size="sm">
              <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
              Export
            </Button>
          </div>
        </div>
      </div>

      <!-- Projects Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        <div
          v-for="project in filteredProjects"
          :key="project.id"
          class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer"
          @click="showProjectDetails(project)"
        >
          <!-- Project Header -->
          <div class="p-6 pb-4">
            <div class="flex items-start justify-between mb-4">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                  {{ project.name }}
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                  {{ project.description }}
                </p>
              </div>
              <div class="ml-4 flex items-center space-x-2">
                <span 
                  :class="[
                    'px-2 py-1 rounded-full text-xs font-medium',
                    getStatusBadgeColor(project.status)
                  ]"
                >
                  {{ project.status }}
                </span>
              </div>
            </div>

            <!-- Project Progress -->
            <div class="space-y-3">
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-600 dark:text-gray-400">Progress</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ project.progress }}%</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  :class="[
                    'h-2 rounded-full transition-all duration-500',
                    getProgressBarColor(project.status)
                  ]" 
                  :style="{ width: `${project.progress}%` }"
                ></div>
              </div>
            </div>

            <!-- Project Metrics -->
            <div class="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div class="text-center">
                <div class="text-sm font-medium text-gray-900 dark:text-white">{{ project.connectedNodes }}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">Nodes</div>
              </div>
              <div class="text-center">
                <div class="text-sm font-medium text-gray-900 dark:text-white">{{ project.currentEpoch }}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">Epoch</div>
              </div>
              <div class="text-center">
                <div class="text-sm font-medium text-green-600">{{ project.metrics?.accuracy || 0 }}%</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">Accuracy</div>
              </div>
            </div>
          </div>

          <!-- Project Actions -->
          <div class="px-6 pb-6">
            <div class="flex items-center justify-between space-x-2">
              <Button
                @click.stop="toggleProjectStatus(project)"
                :variant="project.status === 'training' ? 'outline' : 'primary'"
                size="xs"
                class="flex-1"
              >
                {{ project.status === 'training' ? 'Pause' : 'Start' }}
              </Button>
              <Button
                @click.stop="startTrainingWithAPI(project)"
                variant="primary"
                size="xs"
                class="flex-1 bg-blue-600 hover:bg-blue-700"
                :disabled="project.status === 'training'"
              >
                Train API
              </Button>
              <Button
                @click.stop="viewVisualization(project)"
                variant="outline"
                size="xs"
                class="flex-1"
              >
                Visualize
              </Button>
              <Button
                @click.stop="showProjectMenu(project)"
                variant="ghost"
                size="xs"
                iconOnly
                :leftIcon="EllipsisVerticalIcon"
              />
            </div>
          </div>

          <!-- Last Updated -->
          <div class="px-6 pb-4 text-xs text-gray-500 dark:text-gray-400">
            Last updated: {{ project.lastUpdate }}
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredProjects.length === 0" class="col-span-full text-center py-12">
          <FolderIcon class="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No projects found</h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6">
            {{ searchQuery || statusFilter || typeFilter ? 'Try adjusting your filters' : 'Start by creating your first project' }}
          </p>
          <Button
            @click="createNewProject"
            variant="primary"
            :leftIcon="PlusIcon"
            class="bg-green-600 hover:bg-green-700 focus:ring-green-500"
          >
            Create First Project
          </Button>
        </div>
      </div>
    </div>

    <!-- Project Details Modal -->
    <Modal
      :isOpen="showDetailsModal"
      @close="showDetailsModal = false"
      title="Project Details"
      size="xl"
    >
      <div v-if="selectedProject" class="space-y-6">
        <!-- Project Overview -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Project Information</h4>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Project ID:</span>
                <span class="font-mono">{{ selectedProject.id }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Name:</span>
                <span>{{ selectedProject.name }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Type:</span>
                <span class="capitalize">{{ selectedProject.type }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Status:</span>
                <span :class="getStatusTextColor(selectedProject.status)">{{ selectedProject.status }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Created:</span>
                <span>{{ selectedProject.created }}</span>
              </div>
            </div>
          </div>

          <div>
            <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Training Metrics</h4>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Accuracy:</span>
                <span class="font-medium">{{ selectedProject.metrics?.accuracy || 0 }}%</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Loss:</span>
                <span class="font-medium">{{ selectedProject.metrics?.loss || 0 }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">F1 Score:</span>
                <span class="font-medium">{{ selectedProject.metrics?.f1Score || 0 }}%</span>
              </div>
            </div>

            <!-- Training Configuration Section -->
            <div class="mt-6">
              <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Training Configuration</h4>
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 text-sm">
                <div class="space-y-3">
                  <div class="flex justify-between">
                    <span class="text-gray-500">Training Algorithm:</span>
                    <span class="capitalize">{{ selectedProject.training_alg || 'sft' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Federated Algorithm:</span>
                    <span class="capitalize">{{ selectedProject.fed_alg || 'fedavg' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Secure Aggregation:</span>
                    <span class="capitalize">{{ selectedProject.secure_aggregation || 'shamir_threshold' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Total Epochs:</span>
                    <span>{{ selectedProject.total_epochs || 100 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Fed Rounds:</span>
                    <span>{{ selectedProject.num_rounds || 10 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Batch Size:</span>
                    <span>{{ selectedProject.batch_size || 32 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Learning Rate:</span>
                    <span class="font-mono">{{ selectedProject.lr || '1e-4' }}</span>
                  </div>
                </div>

                <div class="space-y-3">
                  <div class="flex justify-between">
                    <span class="text-gray-500">Model Path:</span>
                    <span class="font-mono text-xs">{{ selectedProject.model_name_or_path || 'sshleifer/tiny-gpt2' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Dataset:</span>
                    <span class="font-mono text-xs">{{ selectedProject.dataset_name || 'vicgalle/alpaca-gpt4' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Dataset Sample:</span>
                    <span>{{ selectedProject.dataset_sample || 50 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Computers:</span>
                    <span>{{ selectedProject.num_computers || 3 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Clients:</span>
                    <span>{{ selectedProject.num_clients || 2 }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500">Max Steps:</span>
                    <span>{{ selectedProject.max_steps || 100 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Modal>

    <!-- Project Menu Modal -->
    <Modal
      :isOpen="showProjectMenuModal"
      @close="showProjectMenuModal = false"
      title="Project Actions"
      size="sm"
    >
      <div class="space-y-4">
        <div class="text-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {{ selectedProject?.name }}
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Choose an action for this project
          </p>
        </div>
        
        <div class="space-y-2">
          <Button
            @click="duplicateProject(selectedProject)"
            variant="outline"
            size="sm"
            class="w-full justify-start"
            :leftIcon="DocumentDuplicateIcon"
          >
            Duplicate Project
          </Button>
          
          <Button
            @click="exportProject(selectedProject)"
            variant="outline"
            size="sm"
            class="w-full justify-start"
            :leftIcon="ArrowDownTrayIcon"
          >
            Export Project
          </Button>
          
          <Button
            @click="showDeleteConfirmation(selectedProject)"
            variant="outline"
            size="sm"
            class="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-red-900/20"
            :leftIcon="TrashIcon"
          >
            Delete Project
          </Button>
        </div>
      </div>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal
      :isOpen="showDeleteModal"
      @close="showDeleteModal = false"
      title="Delete Project"
      size="sm"
    >
      <div class="space-y-4">
        <div class="text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 dark:bg-red-900/20 mb-4">
            <TrashIcon class="h-6 w-6 text-red-600 dark:text-red-400" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Delete Project
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Are you sure you want to delete <strong>{{ projectToDelete?.name }}</strong>? 
            This action cannot be undone and will delete all associated nodes and data.
          </p>
        </div>
        
        <div class="flex space-x-3">
          <Button
            @click="showDeleteModal = false"
            variant="outline"
            size="sm"
            class="flex-1"
          >
            Cancel
          </Button>
          <Button
            @click="confirmDeleteProject"
            variant="primary"
            size="sm"
            class="flex-1 bg-red-600 hover:bg-red-700 focus:ring-red-500"
            :loading="deletingProject"
          >
            Delete
          </Button>
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
import { useApiOptimization } from '@/composables/useApiOptimization'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import StatCard from '@/components/ui/StatCard.vue'
import Modal from '@/components/ui/Modal.vue'
import { 
  ArrowLeftIcon,
  FolderIcon,
  PlusIcon,
  SunIcon,
  MoonIcon,
  PlayIcon,
  CheckCircleIcon,
  ChartBarIcon,
  MagnifyingGlassIcon,
  ArrowPathIcon,
  ArrowDownTrayIcon,
  EllipsisVerticalIcon,
  DocumentDuplicateIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const themeStore = useThemeStore()
const uiStore = useUIStore()
const edgeaiStore = useEdgeAIStore()
const { cachedApiCall, clearCache } = useApiOptimization()

// Component state
const refreshing = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const typeFilter = ref('')
const selectedProject = ref(null)
const showDetailsModal = ref(false)
const showProjectMenuModal = ref(false)
const showDeleteModal = ref(false)
const projectToDelete = ref(null)
const deletingProject = ref(false)

// Computed properties using EdgeAI store
const projects = computed(() => edgeaiStore.projects)

const filteredProjects = computed(() => {
  let filtered = projects.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(project => 
      project.name.toLowerCase().includes(query) || 
      project.description?.toLowerCase().includes(query) ||
      project.type.toLowerCase().includes(query)
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(project => project.status === statusFilter.value)
  }

  if (typeFilter.value) {
    filtered = filtered.filter(project => project.type === typeFilter.value)
  }

  return filtered
})

const totalProjects = computed(() => projects.value.length)
const activeProjects = computed(() => projects.value.filter(p => p.status === 'training' || p.status === 'active').length)
const completedProjects = computed(() => projects.value.filter(p => p.status === 'completed').length)
const successRate = computed(() => {
  if (projects.value.length === 0) return 0
  return Math.round((completedProjects.value / projects.value.length) * 100)
})

// Methods
const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const goBack = () => {
  router.push('/edgeai/dashboard')
}

const createNewProject = () => {
  router.push('/edgeai/create-project')
}

const refreshProjects = async () => {
  const monitor = performanceMonitor.startTimer('EdgeAIProjectRefresh')
  refreshing.value = true
  
  try {
    // Clear cache to ensure fresh data
    clearCache()
    
    // Fetch fresh projects data
    const projectsResult = await edgeaiService.projects.getProjects()
    
    if (projectsResult && Array.isArray(projectsResult)) {
      // Transform and update store
      const transformedProjects = projectsResult.map(project => ({
        id: project.id,
        name: project.name,
        description: project.description,
        type: project.type || 'general',
        status: project.status || 'idle',
        progress: project.progress || 0,
        connectedNodes: project.connected_nodes || 0,
        currentEpoch: project.current_epoch || 0,
        totalEpochs: project.total_epochs || 100,
        created: project.created_at || new Date().toISOString().split('T')[0],
        lastUpdate: project.last_updated || 'Unknown',
        metrics: project.metrics || { accuracy: 0, loss: 0, f1Score: 0 }
      }))
      
      edgeaiStore.projects.splice(0, edgeaiStore.projects.length, ...transformedProjects)
      
      uiStore.addNotification({
        type: 'success',
        title: 'Projects Refreshed',
        message: 'Project data has been updated successfully.'
      })
      
      monitor.end({ success: true, count: transformedProjects.length })
    } else {
      throw new Error('Invalid response format')
    }
  } catch (error) {
    console.error('Failed to refresh projects:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Refresh Failed',
      message: error.message || 'Failed to refresh project data.'
    })
    monitor.end({ success: false, error: error.message })
  } finally {
    refreshing.value = false
  }
}

const showProjectDetails = (project) => {
  selectedProject.value = project
  showDetailsModal.value = true
}

const showProjectMenu = (project) => {
  // 设置当前选中的项目
  selectedProject.value = project
  showProjectMenuModal.value = true
}

const toggleProjectStatus = async (project) => {
  const monitor = performanceMonitor.startTimer('EdgeAIProjectStatusToggle')
  const isRunning = project.status === 'active' || project.status === 'training'
  const newStatus = isRunning ? 'paused' : 'training'
  
  try {
    // Call real API to change project status
    const result = await edgeaiService.projects.updateProjectStatus(project.id, newStatus)
    
    if (result && result.success) {
      // Update local project state
      project.status = newStatus
      
      uiStore.addNotification({
        type: 'success',
        title: `Project ${isRunning ? 'Paused' : 'Started'}`,
        message: `${project.name} is now ${newStatus}.`
      })
      
      monitor.end({ success: true, newStatus })
    } else {
      throw new Error(result?.error || 'Failed to update project status')
    }
  } catch (error) {
    console.error('Failed to toggle project status:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Status Change Failed',
      message: `Failed to change status for ${project.name}`
    })
    monitor.end({ success: false, error: error.message })
  }
}

// Add delete project functionality
const deleteProject = async (project) => {
  if (!confirm(`Are you sure you want to delete project "${project.name}"? This action cannot be undone.`)) {
    return
  }

  const monitor = performanceMonitor.startTimer('EdgeAIProjectDelete')
  
  try {
    const result = await edgeaiService.projects.deleteProject(project.id)
    
    if (result && result.success) {
      // Remove project from store
      const index = edgeaiStore.projects.findIndex(p => p.id === project.id)
      if (index !== -1) {
        edgeaiStore.projects.splice(index, 1)
      }
      
      uiStore.addNotification({
        type: 'success',
        title: 'Project Deleted',
        message: `Project "${project.name}" has been successfully deleted.`
      })
      
      monitor.end({ success: true })
    } else {
      throw new Error(result?.error || 'Failed to delete project')
    }
  } catch (error) {
    console.error('Failed to delete project:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Delete Failed',
      message: error.message || `Failed to delete project "${project.name}"`
    })
    monitor.end({ success: false, error: error.message })
  }
}

const viewVisualization = (project) => {
  edgeaiStore.setCurrentProject(project)
  router.push(`/edgeai/visualization/${project.id}`)
}

const exportProjects = async () => {
  const monitor = performanceMonitor.startTimer('EdgeAIProjectExport')
  
  try {
    const result = await edgeaiService.projects.exportProjects()
    
    if (result && result.success) {
      // Create and download the export file
      const blob = new Blob([result.data], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `edgeai-projects-${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      uiStore.addNotification({
        type: 'success',
        title: 'Export Complete',
        message: 'Project data has been successfully exported to CSV format.'
      })
      
      monitor.end({ success: true })
    } else {
      throw new Error(result?.error || 'Export failed')
    }
  } catch (error) {
    console.error('Failed to export projects:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Export Failed',
      message: error.message || 'Failed to export project data.'
    })
    monitor.end({ success: false, error: error.message })
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  statusFilter.value = ''
  typeFilter.value = ''
}

// Styling helper functions
const getStatusBadgeColor = (status) => {
  const colors = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    training: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    completed: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    paused: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const getStatusTextColor = (status) => {
  const colors = {
    active: 'text-green-600 dark:text-green-400',
    training: 'text-blue-600 dark:text-blue-400',
    completed: 'text-green-600 dark:text-green-400',
    paused: 'text-gray-600 dark:text-gray-400',
    error: 'text-red-600 dark:text-red-400'
  }
  return colors[status] || 'text-gray-600'
}

const getProgressBarColor = (status) => {
  const colors = {
    active: 'bg-green-500',
    training: 'bg-blue-500',
    completed: 'bg-green-600',
    paused: 'bg-gray-500',
    error: 'bg-red-500'
  }
  return colors[status] || 'bg-gray-400'
}

// Lifecycle
onMounted(() => {
  edgeaiStore.initializeStore()
})

// Project menu actions
const duplicateProject = (project) => {
  showProjectMenuModal.value = false
  uiStore.addNotification({
    type: 'info',
    title: 'Duplicate Project',
    message: `Duplicating ${project.name} will be available soon.`
  })
}

const exportProject = (project) => {
  showProjectMenuModal.value = false
  uiStore.addNotification({
    type: 'info',
    title: 'Export Project',
    message: `Exporting ${project.name} will be available soon.`
  })
}

const showDeleteConfirmation = (project) => {
  projectToDelete.value = project
  showProjectMenuModal.value = false
  showDeleteModal.value = true
}

const confirmDeleteProject = async () => {
  if (!projectToDelete.value) return

  deletingProject.value = true

  try {
    const result = await edgeaiService.projects.deleteProject(projectToDelete.value.id)

    if (result && result.success) {
      // 从本地状态中移除项目
      const projectIndex = projects.value.findIndex(p => p.id === projectToDelete.value.id)
      if (projectIndex !== -1) {
        projects.value.splice(projectIndex, 1)
      }

      uiStore.addNotification({
        type: 'success',
        title: 'Project Deleted',
        message: `${projectToDelete.value.name} has been deleted successfully.`
      })

      showDeleteModal.value = false
      projectToDelete.value = null
    } else {
      throw new Error(result?.error || 'Failed to delete project')
    }
  } catch (error) {
    console.error('Failed to delete project:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Delete Failed',
      message: error.message || 'Failed to delete project. Please try again.'
    })
  } finally {
    deletingProject.value = false
  }
}

// New function to start training with test API
const startTrainingWithAPI = async (project) => {
  const monitor = performanceMonitor.startTimer('EdgeAIAPITrainingStart')

  try {
    const response = await fetch(`/api/edgeai/training/start-with-api?project_id=${project.id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    const result = await response.json()

    if (response.ok && result.task_id) {
      // Update project status locally
      project.status = 'training'
      project.task_id = result.task_id

      uiStore.addNotification({
        type: 'success',
        title: 'Training Started',
        message: `Training started via API for ${project.name}. Task ID: ${result.task_id}`,
        actions: [
          {
            label: 'Monitor',
            handler: () => monitorTrainingProgress(result.task_id)
          }
        ]
      })

      monitor.end({ success: true, taskId: result.task_id })
    } else {
      throw new Error(result.detail || result.message || 'Failed to start training')
    }
  } catch (error) {
    console.error('Failed to start training with API:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Training Start Failed',
      message: error.message || `Failed to start training for ${project.name} via API.`
    })
    monitor.end({ success: false, error: error.message })
  }
}

// Function to monitor training progress
const monitorTrainingProgress = async (taskId) => {
  try {
    const response = await fetch(`/api/edgeai/training/monitor/${taskId}`)
    const result = await response.json()

    if (response.ok) {
      uiStore.addNotification({
        type: 'info',
        title: 'Training Monitor',
        message: `Monitor data: ${result.monitor_data}`
      })
    } else {
      throw new Error(result.detail || 'Failed to get monitor data')
    }
  } catch (error) {
    console.error('Failed to monitor training:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Monitor Failed',
      message: error.message || 'Failed to get training monitor data.'
    })
  }
}

onUnmounted(() => {
  edgeaiStore.cleanup()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>