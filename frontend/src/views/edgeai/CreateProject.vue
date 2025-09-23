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
          <div class="grid grid-cols-1 gap-6">
            <Input
              v-model="projectData.name"
              label="Project Name *"
              placeholder="Enter project name"
              required
              :error="errors.name"
            />

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Project Description *
              </label>
              <textarea
                v-model="projectData.description"
                rows="3"
                placeholder="Describe your EdgeAI project and its objectives"
                :class="[
                  'w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500 resize-none',
                  errors.description ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
                ]"
              ></textarea>
              <p v-if="errors.description" class="mt-1 text-sm text-red-600 dark:text-red-400">
                {{ errors.description }}
              </p>
            </div>
          </div>

          <!-- Model Configuration -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Model Configuration</h3>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Model *
                </label>
                <select
                  v-model="projectData.model"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="Gemma">Gemma</option>
                  <option value="OpenVLA">OpenVLA</option>
                  <option value="LLaMA">LLaMA</option>
                  <option value="Qwen">Qwen</option>
                </select>
                <p class="text-xs text-gray-500 dark:text-gray-400">Connected to database table IP</p>
              </div>

              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Training Strategy *
                </label>
                <select
                  v-model="projectData.training_strategy"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="sft">SFT (Supervised Fine-Tuning)</option>
                  <option value="dpo">DPO (Direct Preference Optimization)</option>
                  <option value="grpo">GRPO (Generalized RPO)</option>
                  <option value="ipo">IPO (Identity Policy Optimization)</option>
                  <option value="kto">KTO (Kahneman-Tversky Optimization)</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-1 gap-6 mt-4">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Protocol *
                </label>
                <select
                  v-model="projectData.protocol"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="fedavg">FedAvg (Federated Averaging)</option>
                  <option value="fedygi">FedYgi (Federated YGI)</option>
                  <option value="fedadam">FedAdam (Federated Adam)</option>
                  <option value="fedavgm">FedAvgM (Federated Averaging with Momentum)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Training Configuration -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Training Configuration</h3>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Input
                v-model.number="projectData.epochs"
                type="number"
                label="Epochs *"
                placeholder="100"
                min="1"
                max="1000"
                required
                :error="errors.epochs"
              />

              <Input
                v-model.number="projectData.batch_size"
                type="number"
                label="Batch Size *"
                placeholder="32"
                min="1"
                max="512"
                required
                :error="errors.batch_size"
              />

              <Input
                v-model.number="projectData.learning_rate"
                type="number"
                step="0.0001"
                label="Learning Rate *"
                placeholder="0.001"
                min="0.0001"
                max="1"
                required
                :error="errors.learning_rate"
              />
            </div>
          </div>

          <!-- Node Configuration -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">Node Configuration</h3>
              <Button
                @click="addNode"
                variant="outline"
                size="sm"
                class="flex items-center space-x-2"
              >
                <PlusIcon class="w-4 h-4" />
                <span>Add Node</span>
              </Button>
            </div>

            <div class="space-y-4">
              <div
                v-for="(node, index) in projectData.nodes"
                :key="index"
                class="flex items-end space-x-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600"
              >
                <div class="flex-1">
                  <Input
                    v-model="node.ip"
                    :label="`Node ${index + 1} IP Address *`"
                    placeholder="192.168.1.100"
                    required
                    :error="errors[`node_${index}`]"
                  />
                </div>
                <div class="flex-1">
                  <Input
                    v-model="node.name"
                    :label="`Node ${index + 1} Name`"
                    placeholder="Node Name (Optional)"
                  />
                </div>
                <Button
                  @click="removeNode(index)"
                  variant="ghost"
                  size="sm"
                  class="text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-red-900/20"
                  :disabled="projectData.nodes.length === 1"
                >
                  <TrashIcon class="w-4 h-4" />
                </Button>
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-400">Connected to database node table</p>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ComputerDesktopIcon, ArrowLeftIcon, SunIcon, MoonIcon, PlusIcon, TrashIcon } from '@heroicons/vue/24/outline'
import Input from '@/components/ui/Input.vue'
import Button from '@/components/ui/Button.vue'
import { useEdgeAIStore } from '@/stores/edgeai.js'
import { useUIStore } from '@/stores/ui.js'
import { useThemeStore } from '@/stores/theme.js'

// Stores
const edgeaiStore = useEdgeAIStore()
const uiStore = useUIStore()
const themeStore = useThemeStore()
const router = useRouter()

// Reactive state
const creating = ref(false)
const errors = ref({})

const projectData = ref({
  // Basic Information
  name: '',
  description: '',

  // Model Configuration
  model: 'Gemma',  // 与数据库table IP连接的字段
  training_strategy: 'sft',
  protocol: 'fedavg',

  // Training Configuration
  epochs: 100,
  batch_size: 32,
  learning_rate: 0.001,

  // Node Configuration
  nodes: [
    {
      ip: '',
      name: ''
    }
  ]  // 与数据库node table连接的字段
})

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const goBack = () => {
  router.push('/edgeai/dashboard')
}

// Node management methods
const addNode = () => {
  projectData.value.nodes.push({
    ip: '',
    name: ''
  })
}

const removeNode = (index) => {
  if (projectData.value.nodes.length > 1) {
    projectData.value.nodes.splice(index, 1)
  }
}

const createProject = async () => {
  creating.value = true
  errors.value = {}

  try {
    // Comprehensive validation
    if (!projectData.value.name.trim()) {
      errors.value.name = 'Project name is required'
      return
    }

    if (!projectData.value.description.trim()) {
      errors.value.description = 'Project description is required'
      return
    }

    if (projectData.value.epochs < 1 || projectData.value.epochs > 1000) {
      errors.value.epochs = 'Epochs must be between 1 and 1000'
      return
    }

    if (projectData.value.batch_size < 1 || projectData.value.batch_size > 512) {
      errors.value.batch_size = 'Batch size must be between 1 and 512'
      return
    }

    if (projectData.value.learning_rate < 0.0001 || projectData.value.learning_rate > 1) {
      errors.value.learning_rate = 'Learning rate must be between 0.0001 and 1'
      return
    }

    // Validate nodes
    let hasValidNodes = false
    projectData.value.nodes.forEach((node, index) => {
      if (!node.ip.trim()) {
        errors.value[`node_${index}`] = 'Node IP address is required'
      } else {
        hasValidNodes = true
      }
    })
    
    if (!hasValidNodes) {
      return
    }

    // Build payload matching backend API
    const payload = {
      name: projectData.value.name.trim(),
      description: projectData.value.description.trim(),
      model: projectData.value.model,
      training_strategy: projectData.value.training_strategy,
      protocol: projectData.value.protocol,
      epochs: projectData.value.epochs,
      batch_size: projectData.value.batch_size,
      learning_rate: projectData.value.learning_rate,
      nodes: projectData.value.nodes.filter(node => node.ip.trim()).map(node => ({
        ip: node.ip.trim(),
        name: node.name.trim() || `Node ${node.ip}`,
        description: node.description.trim() || ''
      }))
    }

    console.log('Creating project with payload:', JSON.stringify(payload, null, 2))

    // Use EdgeAI store to create project with formatted payload
    const result = await edgeaiStore.createProject(payload)

    if (result.success) {
      console.log('Project created successfully:', result.project)

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

// Initialize data on component mount
onMounted(() => {
  // Any initialization logic if needed
})
</script>