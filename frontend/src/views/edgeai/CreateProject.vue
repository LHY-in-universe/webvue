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

          <!-- Model Configuration (aligned with Training Settings form) -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Model Configuration</h3>

            <!-- Row 1: training_alg / fed_alg -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Training Algorithm (training_alg)</label>
                <select v-model="projectData.training_alg"
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500">
                  <option value="sft">SFT (Supervised Fine-Tuning)</option>
                  <option value="dpo">DPO</option>
                  <option value="ppo">PPO</option>
                </select>
              </div>
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Federated Algorithm (fed_alg)</label>
                <select v-model="projectData.fed_alg"
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500">
                  <option value="fedavg">FedAvg</option>
                  <option value="fedprox">FedProx</option>
                  <option value="fedadam">FedAdam</option>
                </select>
              </div>
            </div>

            <!-- Row 2: secure_aggregation / num_computers -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Secure Aggregation (secure_aggregation)</label>
                <select v-model="projectData.secure_aggregation"
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500">
                  <option value="shamir_threshold">Shamir Threshold</option>
                  <option value="paillier">Paillier</option>
                  <option value="none">None</option>
                </select>
              </div>
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Num Computers (num_computers)</label>
                <input v-model.number="projectData.num_computers" type="number" min="1" max="100"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
              </div>
            </div>

            <!-- Row 3: threshold / num_rounds -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Threshold (threshold)</label>
                <input v-model.number="projectData.threshold" type="number" min="1" :max="projectData.num_computers || 100"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
              </div>
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Rounds (num_rounds)</label>
                <input v-model.number="projectData.num_rounds" type="number" min="1" max="1000"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
              </div>
            </div>

            <!-- Row 4: num_clients / sample_clients -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Num Clients (num_clients)</label>
                <input v-model.number="projectData.num_clients" type="number" min="1" max="100"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
              </div>
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Sample Clients (sample_clients)</label>
                <input v-model.number="projectData.sample_clients" type="number" min="1" :max="projectData.num_clients || 100"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
              </div>
            </div>

            <!-- Row 5: max_steps / lr -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Max Steps (max_steps)</label>
                <input v-model.number="projectData.max_steps" type="number" min="1" max="10000"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
              </div>
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Learning Rate (lr)</label>
                <input v-model="projectData.lr" type="text" placeholder="1e-4"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
              </div>
            </div>

            <!-- Row 6: model_name_or_path / dataset_name -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Model Path (model_name_or_path)</label>
                <input v-model="projectData.model_name_or_path" type="text" placeholder="sshleifer/tiny-gpt2"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
              </div>
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Dataset Name (dataset_name)</label>
                <input v-model="projectData.dataset_name" type="text" placeholder="vicgalle/alpaca-gpt4"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
              </div>
            </div>

            <!-- Row 7: dataset_sample -->
            <div class="grid grid-cols-1 md:grid-cols-1 gap-6 mt-4">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Dataset Sample (dataset_sample)</label>
                <input v-model.number="projectData.dataset_sample" type="number" min="1" max="100000"
                       class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500" />
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ComputerDesktopIcon, ArrowLeftIcon, SunIcon, MoonIcon } from '@heroicons/vue/24/outline'
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

  // Model/Training Configuration (aligned with Training Settings)
  training_alg: 'sft',
  fed_alg: 'fedavg',
  secure_aggregation: 'shamir_threshold',
  num_computers: 3,
  threshold: 2,
  num_rounds: 10,
  num_clients: 2,
  sample_clients: 2,
  max_steps: 100,
  lr: '1e-4',
  model_name_or_path: 'sshleifer/tiny-gpt2',
  dataset_name: 'vicgalle/alpaca-gpt4',
  dataset_sample: 50,

  // Training Configuration
  epochs: 100,
  batch_size: 32,
  learning_rate: 0.001,

  // Node Configuration
  node_ip: ''  // 与数据库node table连接的字段
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
    // Comprehensive validation
    if (!projectData.value.name.trim()) {
      errors.value.name = 'Project name is required'
      return
    }

    if (!projectData.value.description.trim()) {
      errors.value.description = 'Project description is required'
      return
    }

    

    if (!projectData.value.node_ip.trim()) {
      errors.value.node_ip = 'Node IP address is required'
      return
    }

    // Build payload matching backend API
    const payload = {
      name: projectData.value.name.trim(),
      description: projectData.value.description.trim(),
      model: projectData.value.model,
      training_strategy: projectData.value.training_strategy,
      protocol: projectData.value.protocol,
      
      node_ip: projectData.value.node_ip.trim()
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