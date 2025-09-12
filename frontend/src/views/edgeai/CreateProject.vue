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
            <ComputerDesktopIcon class="h-8 w-8 text-green-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Create New EdgeAI Project
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
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Project Configuration</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Set up your new EdgeAI training project</p>
        </div>

        <form @submit.prevent="createProject" class="p-6 space-y-6">
          <!-- Basic Information -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Input
              v-model="projectData.name"
              label="Project Name"
              placeholder="Enter project name"
              required
              :error="errors.name"
            />


          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Project Description
            </label>
            <textarea
              v-model="projectData.description"
              rows="3"
              placeholder="Describe your EdgeAI project and its objectives"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500 resize-none"
            ></textarea>
          </div>

          <!-- Model Configuration -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Model Configuration</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Model Type
                </label>
                <select 
                  v-model="projectData.modelType" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="Gemma">Gemma</option>
                  <option value="OpenVLA">OpenVLA</option>
                  <option value="LLaMA">LLaMA</option>
                  <option value="Qwen">Qwen</option>
                </select>
              </div>

              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Training Strategy
                </label>
                <select 
                  v-model="projectData.modelType" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="sft">sft</option>
                  <option value="dpo">dpo</option>
                  <option value="grpo">grpo</option>
                  <option value="ipo">ipo</option>
                  <option value="kto">kto</option>
                </select>
              </div>
              
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Protocal
                </label>
                <select 
                  v-model="projectData.modelType" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="fedavg">fedavg</option>
                  <option value="fedygi">fedygi</option>
                  <option value="fedadam">fedadam</option>
                  <option value="fedavgm">fedavgm</option>
                </select>
              </div>


            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
              <Input
                v-model.number="projectData.epochs"
                type="number"
                label="Training Epochs"
                placeholder="100"
                min="1"
                max="1000"
              />

              <Input
                v-model.number="projectData.batchSize"
                type="number"
                label="Batch Size"
                placeholder="32"
                min="1"
                max="512"
              />

              <Input
                v-model.number="projectData.learningRate"
                type="number"
                step="0.0001"
                label="Learning Rate"
                placeholder="0.001"
                min="0.0001"
                max="1"
              />



            </div>
          </div>

          <!-- Node Configuration -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Node Configuration</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                v-model.number="projectData.targetNodes"
                type="number"
                label="Target Node Count"
                placeholder="5"
                min="1"
                max="50"
              />

              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Resource Requirements
                </label>
                <select 
                  v-model="projectData.resourceLevel" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="low">Low (CPU: 2 cores, RAM: 4GB)</option>
                  <option value="medium">Medium (CPU: 4 cores, RAM: 8GB)</option>
                  <option value="high">High (CPU: 8 cores, RAM: 16GB)</option>
                  <option value="gpu">GPU Required (GPU: 1x, RAM: 16GB)</option>
                </select>
              </div>
            </div>

            <!-- Auto-scaling Configuration -->
            <div class="mt-4">
              <div class="flex items-center space-x-3">
                <input
                  id="autoScaling"
                  v-model="projectData.autoScaling"
                  type="checkbox"
                  class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label for="autoScaling" class="text-sm text-gray-700 dark:text-gray-300">
                  Enable auto-scaling based on workload
                </label>
              </div>
              <div v-if="projectData.autoScaling" class="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  v-model.number="projectData.minNodes"
                  type="number"
                  label="Min Nodes"
                  placeholder="1"
                  min="1"
                  size="sm"
                />
                <Input
                  v-model.number="projectData.maxNodes"
                  type="number"
                  label="Max Nodes"
                  placeholder="10"
                  min="1"
                  size="sm"
                />
              </div>
            </div>
          </div>

          <!-- Advanced Settings -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Advanced Settings</h3>
            
            <div class="space-y-4">
              <div class="flex items-center space-x-3">
                <input
                  id="enableMonitoring"
                  v-model="projectData.enableMonitoring"
                  type="checkbox"
                  class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label for="enableMonitoring" class="text-sm text-gray-700 dark:text-gray-300">
                  Enable real-time monitoring and alerts
                </label>
              </div>

              <div class="flex items-center space-x-3">
                <input
                  id="dataEncryption"
                  v-model="projectData.dataEncryption"
                  type="checkbox"
                  class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label for="dataEncryption" class="text-sm text-gray-700 dark:text-gray-300">
                  Enable data encryption in transit and at rest
                </label>
              </div>

              <div class="flex items-center space-x-3">
                <input
                  id="checkpointing"
                  v-model="projectData.checkpointing"
                  type="checkbox"
                  class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label for="checkpointing" class="text-sm text-gray-700 dark:text-gray-300">
                  Enable automatic checkpointing and recovery
                </label>
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
              class="bg-green-600 hover:bg-green-700 focus:ring-green-500"
            >
              Create Project
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'
import { useEdgeAIStore } from '@/stores/edgeai'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import { 
  ComputerDesktopIcon,
  ArrowLeftIcon,
  SunIcon,
  MoonIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const themeStore = useThemeStore()
const uiStore = useUIStore()
const edgeaiStore = useEdgeAIStore()

const creating = ref(false)
const errors = ref({})

const projectData = ref({
  name: '',
  type: 'manufacturing',
  description: '',
  modelType: 'cnn',
  epochs: 100,
  batchSize: 32,
  learningRate: 0.001,
  optimizer: 'adam',
  targetNodes: 5,
  resourceLevel: 'medium',
  autoScaling: false,
  minNodes: 1,
  maxNodes: 10,
  enableMonitoring: true,
  dataEncryption: true,
  checkpointing: true
})

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const goBack = () => {
  router.push('/edgeai/dashboard')
}

const createProject = async () => {
  creating.value = true
  errors.value = {}
  
  try {
    // Validation
    if (!projectData.value.name.trim()) {
      errors.value.name = 'Project name is required'
      return
    }

    // Use EdgeAI store to create project
    const result = await edgeaiStore.createProject(projectData.value)
    
    if (result.success) {
      console.log('Project created:', result.project)
      
      uiStore.addNotification({
        type: 'success',
        title: 'Project Created Successfully',
        message: `EdgeAI project "${projectData.value.name}" has been created and is ready for deployment.`,
        actions: [
          {
            label: 'View Project',
            handler: () => router.push(`/edgeai/project/${result.project.id}`)
          }
        ]
      })
      
      // Redirect to dashboard
      router.push('/edgeai/dashboard')
    } else {
      throw new Error(result.error || 'Unknown error occurred')
    }
    
  } catch (error) {
    console.error('Error creating project:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Project Creation Failed',
      message: error.message || 'There was an error creating your project. Please try again.'
    })
  } finally {
    creating.value = false
  }
}
</script>