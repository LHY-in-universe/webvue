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

          <!-- Training Algorithm Configuration -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Training Algorithm Configuration</h3>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Training Algorithm *
                </label>
                <select
                  v-model="projectData.training_alg"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="sft">SFT (Supervised Fine-Tuning)</option>
                  <option value="dpo">DPO (Direct Preference Optimization)</option>
                  <option value="grpo">GRPO (Generalized RPO)</option>
                  <option value="ipo">IPO (Identity Policy Optimization)</option>
                  <option value="kto">KTO (Kahneman-Tversky Optimization)</option>
                </select>
              </div>

              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Federated Algorithm *
                </label>
                <select
                  v-model="projectData.fed_alg"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="fedavg">FedAvg (Federated Averaging)</option>
                  <option value="fedygi">FedYgi (Federated YGI)</option>
                  <option value="fedadam">FedAdam (Federated Adam)</option>
                  <option value="fedavgm">FedAvgM (Federated Averaging with Momentum)</option>
                </select>
              </div>

              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Secure Aggregation *
                </label>
                <select
                  v-model="projectData.secure_aggregation"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
                >
                  <option value="shamir_threshold">Shamir Threshold</option>
                  <option value="none">None</option>
                  <option value="simple">Simple</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Basic Training Configuration -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Basic Training Configuration</h3>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
              <Input
                v-model.number="projectData.total_epochs"
                type="number"
                label="Total Epochs *"
                placeholder="100"
                min="1"
                max="1000"
                required
                :error="errors.total_epochs"
              />

              <Input
                v-model.number="projectData.num_rounds"
                type="number"
                label="Fed Rounds *"
                placeholder="10"
                min="1"
                max="100"
                required
                :error="errors.num_rounds"
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
                v-model="projectData.lr"
                label="Learning Rate *"
                placeholder="0.0001"
                required
                :error="errors.lr"
              />
            </div>
          </div>

          <!-- Model and Dataset Configuration -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Model and Dataset Configuration</h3>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  Model Selection *
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
              </div>

              <Input
                v-model="projectData.model_name_or_path"
                label="Model Path *"
                placeholder="sshleifer/tiny-gpt2"
                required
                :error="errors.model_name_or_path"
              />

              <Input
                v-model="projectData.dataset_name"
                label="Dataset Name *"
                placeholder="vicgalle/alpaca-gpt4"
                required
                :error="errors.dataset_name"
              />

              <Input
                v-model.number="projectData.dataset_sample"
                type="number"
                label="Dataset Sample *"
                placeholder="50"
                min="1"
                max="1000"
                required
                :error="errors.dataset_sample"
              />
            </div>
          </div>

          <!-- Advanced Federated Learning Parameters -->
          <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Advanced Federated Learning Parameters</h3>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Input
                v-model.number="projectData.num_computers"
                type="number"
                label="Number of Computers"
                placeholder="3"
                min="1"
                max="10"
              />

              <Input
                v-model.number="projectData.threshold"
                type="number"
                label="Threshold"
                placeholder="2"
                min="1"
                max="10"
              />

              <Input
                v-model.number="projectData.num_clients"
                type="number"
                label="Number of Clients"
                placeholder="2"
                min="1"
                max="10"
              />

              <Input
                v-model.number="projectData.sample_clients"
                type="number"
                label="Sample Clients"
                placeholder="2"
                min="1"
                max="10"
              />

              <Input
                v-model.number="projectData.max_steps"
                type="number"
                label="Max Steps"
                placeholder="100"
                min="1"
                max="10000"
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
import { useFormValidation } from '@/composables/useFormValidation'
import { parseNumericInput, formatToDecimal } from '@/utils/numberUtils'

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
  createNumericInputHandler,
  clearErrors
} = useFormValidation()

// Reactive state
const creating = ref(false)

const projectData = ref({
  // Basic Information
  name: '',
  description: '',

  // Model Configuration
  model: 'Gemma',

  // 统一的训练参数 (合并后的字段)
  training_alg: 'sft',                    // 原 training_strategy
  fed_alg: 'fedavg',                      // 原 protocol
  secure_aggregation: 'shamir_threshold',

  // 训练配置
  total_epochs: 100,                      // 原 epochs，重命名为total_epochs
  num_rounds: 10,                         // 联邦学习轮次
  batch_size: 32,
  lr: '0.0001',                          // 保持字符串类型

  // 模型和数据集配置
  model_name_or_path: 'sshleifer/tiny-gpt2',
  dataset_name: 'vicgalle/alpaca-gpt4',
  dataset_sample: 50,

  // 高级联邦学习参数
  num_computers: 3,
  threshold: 2,
  num_clients: 2,
  sample_clients: 2,
  max_steps: 100,

  // Node Configuration
  nodes: [
    {
      ip: '',
      name: ''
    }
  ]
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

    if (projectData.value.total_epochs < 1 || projectData.value.total_epochs > 1000) {
      errors.value.total_epochs = 'Total epochs must be between 1 and 1000'
      return
    }

    if (projectData.value.num_rounds < 1 || projectData.value.num_rounds > 100) {
      errors.value.num_rounds = 'Number of rounds must be between 1 and 100'
      return
    }

    if (projectData.value.batch_size < 1 || projectData.value.batch_size > 512) {
      errors.value.batch_size = 'Batch size must be between 1 and 512'
      return
    }

    if (!projectData.value.lr || projectData.value.lr.trim() === '') {
      errors.value.lr = 'Learning rate is required'
      return
    }
    
    // 验证学习率是否为有效数字且大于0
    const lrValue = parseFloat(projectData.value.lr.trim())
    if (isNaN(lrValue) || lrValue <= 0) {
      errors.value.lr = 'Learning rate must be a valid number greater than 0'
      return
    }

    if (!projectData.value.model_name_or_path || projectData.value.model_name_or_path.trim() === '') {
      errors.value.model_name_or_path = 'Model path is required'
      return
    }

    if (!projectData.value.dataset_name || projectData.value.dataset_name.trim() === '') {
      errors.value.dataset_name = 'Dataset name is required'
      return
    }

    if (projectData.value.dataset_sample < 1 || projectData.value.dataset_sample > 1000) {
      errors.value.dataset_sample = 'Dataset sample must be between 1 and 1000'
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

    // Build payload matching backend API (使用合并后的字段)
    const payload = {
      name: projectData.value.name.trim(),
      description: projectData.value.description.trim(),
      model: projectData.value.model,

      // 统一的训练参数
      training_alg: projectData.value.training_alg,
      fed_alg: projectData.value.fed_alg,
      secure_aggregation: projectData.value.secure_aggregation,

      // 训练配置
      total_epochs: projectData.value.total_epochs,
      num_rounds: projectData.value.num_rounds,
      batch_size: projectData.value.batch_size,
      lr: projectData.value.lr,

      // 模型和数据集配置
      model_name_or_path: projectData.value.model_name_or_path,
      dataset_name: projectData.value.dataset_name,
      dataset_sample: projectData.value.dataset_sample,

      // 高级联邦学习参数
      num_computers: projectData.value.num_computers,
      threshold: projectData.value.threshold,
      num_clients: projectData.value.num_clients,
      sample_clients: projectData.value.sample_clients,
      max_steps: projectData.value.max_steps,

      nodes: projectData.value.nodes.filter(node => node.ip.trim()).map(node => ({
        ip: node.ip.trim(),
        name: node.name.trim() || `Node ${node.ip}`
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