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
            <ServerStackIcon class="h-8 w-8 text-blue-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Create New EdgeAI Cluster
            </h1>
          </div>

          <div class="flex items-center space-x-4">
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

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white dark:bg-gray-800 shadow-sm rounded-lg border border-gray-200 dark:border-gray-700">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Cluster Configuration</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Set up your new EdgeAI cluster for distributed computing</p>
        </div>

        <form @submit.prevent="createCluster" class="p-6 space-y-6">
          <!-- Basic Information -->
          <div class="grid grid-cols-1 gap-6">
            <Input
              v-model="clusterData.name"
              label="Cluster Name *"
              placeholder="Enter cluster name"
              required
              :error="errors.name"
            />

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Project Association (Optional)
              </label>
              <select
                v-model="clusterData.project_id"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select a project (optional)</option>
                <option v-for="project in availableProjects" :key="project.id" :value="project.id">
                  {{ project.name }}
                </option>
              </select>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                Associate this cluster with an existing project
              </p>
            </div>
          </div>

          <!-- Additional Information -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Additional Information</h3>
            <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-blue-800 dark:text-blue-200">
                    Cluster Creation
                  </h3>
                  <div class="mt-2 text-sm text-blue-700 dark:text-blue-300">
                    <p>
                      A cluster is a logical grouping of computing resources. You can associate this cluster with a project to organize your EdgeAI workloads. 
                      Additional configuration can be done after cluster creation.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
            <Button
              @click="goBack"
              variant="outline"
              type="button"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              :loading="creating"
              class="bg-blue-600 hover:bg-blue-700 focus:ring-blue-500"
            >
              Create Cluster
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ServerStackIcon, ArrowLeftIcon, SunIcon, MoonIcon } from '@heroicons/vue/24/outline'
import Input from '@/components/ui/Input.vue'
import Button from '@/components/ui/Button.vue'
import { useEdgeAIStore } from '@/stores/edgeai.js'
import { useUIStore } from '@/stores/ui.js'
import { useThemeStore } from '@/stores/theme.js'
import { useFormValidation } from '@/composables/useFormValidation'
import edgeaiService from '@/services/edgeaiService'

// Stores
const edgeaiStore = useEdgeAIStore()
const uiStore = useUIStore()
const themeStore = useThemeStore()
const router = useRouter()

// Form validation
const {
  errors,
  validateField,
  validators,
  clearErrors
} = useFormValidation()

// Reactive state
const creating = ref(false)
const availableProjects = ref([])

const clusterData = ref({
  // Basic Information
  name: '',
  project_id: ''
})

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const goBack = () => {
  router.push('/edgeai/cluster-management')
}

// Load available projects
const loadProjects = async () => {
  try {
    const projects = await edgeaiService.projects.getProjects()
    availableProjects.value = projects || []
  } catch (error) {
    console.error('Error loading projects:', error)
    availableProjects.value = []
  }
}

const createCluster = async () => {
  creating.value = true
  errors.value = {}

  try {
    // Basic validation
    if (!clusterData.value.name.trim()) {
      errors.value.name = 'Cluster name is required'
      return
    }

    // Build payload for cluster creation
    const payload = {
      name: clusterData.value.name.trim(),
      project_id: clusterData.value.project_id ? parseInt(clusterData.value.project_id) : null
    }

    console.log('Creating cluster with payload:', JSON.stringify(payload, null, 2))

    // Use EdgeAI service to create cluster
    const result = await edgeaiService.clusters.createCluster(payload)

    if (result) {
      console.log('Cluster created successfully:', result)

      uiStore.addNotification({
        type: 'success',
        title: 'Cluster Created Successfully',
        message: `EdgeAI cluster "${clusterData.value.name}" has been created and is ready for use.`,
        actions: [
          {
            label: 'View Cluster',
            handler: () => router.push('/edgeai/cluster-management')
          }
        ]
      })

      // Redirect to cluster management
      router.push('/edgeai/cluster-management')
    } else {
      throw new Error('Failed to create cluster')
    }

  } catch (error) {
    console.error('Error creating cluster:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Cluster Creation Failed',
      message: error.message || 'There was an error creating your cluster. Please try again.'
    })
  } finally {
    creating.value = false
  }
}

// Initialize data on component mount
onMounted(() => {
  loadProjects()
})
</script>
