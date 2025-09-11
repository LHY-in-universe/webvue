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
            <FolderArrowDownIcon class="h-8 w-8 text-green-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Import EdgeAI Project
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
      <!-- Import Options -->
      <div class="bg-white dark:bg-gray-800 shadow-sm rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-8">
        <div class="text-center mb-8">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Import Project Configuration</h2>
          <p class="text-gray-600 dark:text-gray-400">Choose how you'd like to import your EdgeAI project</p>
        </div>

        <!-- Import Method Selection -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div 
            @click="importMethod = 'file'"
            :class="[
              'border-2 rounded-lg p-6 cursor-pointer transition-all',
              importMethod === 'file' 
                ? 'border-green-500 bg-green-50 dark:bg-green-900/20' 
                : 'border-gray-200 dark:border-gray-700 hover:border-green-300'
            ]"
          >
            <div class="text-center">
              <DocumentIcon class="w-12 h-12 mx-auto mb-4 text-green-600" />
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Upload Configuration File</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">Import from JSON or YAML configuration file</p>
            </div>
          </div>

          <div 
            @click="importMethod = 'url'"
            :class="[
              'border-2 rounded-lg p-6 cursor-pointer transition-all',
              importMethod === 'url' 
                ? 'border-green-500 bg-green-50 dark:bg-green-900/20' 
                : 'border-gray-200 dark:border-gray-700 hover:border-green-300'
            ]"
          >
            <div class="text-center">
              <LinkIcon class="w-12 h-12 mx-auto mb-4 text-blue-600" />
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Import from URL</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">Load configuration from remote URL</p>
            </div>
          </div>

          <div 
            @click="importMethod = 'template'"
            :class="[
              'border-2 rounded-lg p-6 cursor-pointer transition-all',
              importMethod === 'template' 
                ? 'border-green-500 bg-green-50 dark:bg-green-900/20' 
                : 'border-gray-200 dark:border-gray-700 hover:border-green-300'
            ]"
          >
            <div class="text-center">
              <TemplateIcon class="w-12 h-12 mx-auto mb-4 text-purple-600" />
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Use Template</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">Start from pre-configured template</p>
            </div>
          </div>
        </div>

        <!-- File Upload Section -->
        <div v-if="importMethod === 'file'" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Configuration File
            </label>
            <FileUpload
              @file-selected="handleFileUpload"
              accept=".json,.yaml,.yml,.toml"
              :multiple="false"
              class="mb-4"
            >
              <template #default="{ isDragOver }">
                <div 
                  :class="[
                    'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
                    isDragOver 
                      ? 'border-green-400 bg-green-50 dark:bg-green-900/20' 
                      : 'border-gray-300 dark:border-gray-600'
                  ]"
                >
                  <DocumentArrowUpIcon class="w-12 h-12 mx-auto mb-4 text-gray-400" />
                  <p class="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    Drop configuration file here
                  </p>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    or click to browse files
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-500">
                    Supports JSON, YAML, and TOML formats
                  </p>
                </div>
              </template>
            </FileUpload>
          </div>

          <!-- File Preview -->
          <div v-if="uploadedFile" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <DocumentIcon class="w-5 h-5 text-green-600 mr-2" />
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ uploadedFile.name }}</span>
                <span class="text-xs text-gray-500 ml-2">({{ formatFileSize(uploadedFile.size) }})</span>
              </div>
              <Button @click="removeFile" variant="ghost" size="xs" :leftIcon="XMarkIcon" />
            </div>
            
            <!-- Configuration Preview -->
            <div v-if="parsedConfig" class="bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-600 p-4">
              <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Configuration Preview</h4>
              <pre class="text-xs bg-gray-900 text-green-400 p-3 rounded overflow-x-auto">{{ JSON.stringify(parsedConfig, null, 2) }}</pre>
            </div>

            <!-- Validation Results -->
            <div v-if="validationResults.length > 0" class="mt-4">
              <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Validation Results</h4>
              <div class="space-y-2">
                <div 
                  v-for="result in validationResults" 
                  :key="result.field"
                  :class="[
                    'flex items-center text-sm p-2 rounded',
                    result.type === 'error' 
                      ? 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300'
                      : result.type === 'warning'
                      ? 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-300'
                      : 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300'
                  ]"
                >
                  <CheckCircleIcon v-if="result.type === 'success'" class="w-4 h-4 mr-2" />
                  <ExclamationTriangleIcon v-else-if="result.type === 'warning'" class="w-4 h-4 mr-2" />
                  <XCircleIcon v-else class="w-4 h-4 mr-2" />
                  <span>{{ result.message }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- URL Import Section -->
        <div v-if="importMethod === 'url'" class="space-y-6">
          <div>
            <label for="configUrl" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Configuration URL
            </label>
            <Input
              id="configUrl"
              v-model="configUrl"
              type="url"
              placeholder="https://example.com/config.json"
              :error="urlError"
            />
          </div>

          <div class="flex items-center space-x-2">
            <input
              id="requireAuth"
              v-model="urlRequireAuth"
              type="checkbox"
              class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
            />
            <label for="requireAuth" class="text-sm text-gray-700 dark:text-gray-300">
              URL requires authentication
            </label>
          </div>

          <div v-if="urlRequireAuth" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              v-model="urlAuth.username"
              label="Username"
              placeholder="Enter username"
            />
            <Input
              v-model="urlAuth.password"
              type="password"
              label="Password"
              placeholder="Enter password"
            />
          </div>

          <Button 
            @click="loadFromUrl"
            variant="primary"
            :loading="loadingUrl"
            :disabled="!configUrl"
          >
            Load Configuration
          </Button>

          <!-- URL Preview -->
          <div v-if="urlConfig" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Loaded Configuration</h4>
            <pre class="text-xs bg-gray-900 text-green-400 p-3 rounded overflow-x-auto">{{ JSON.stringify(urlConfig, null, 2) }}</pre>
          </div>
        </div>

        <!-- Template Selection Section -->
        <div v-if="importMethod === 'template'" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div
              v-for="template in templates"
              :key="template.id"
              @click="selectedTemplate = template"
              :class="[
                'border-2 rounded-lg p-4 cursor-pointer transition-all',
                selectedTemplate?.id === template.id
                  ? 'border-green-500 bg-green-50 dark:bg-green-900/20'
                  : 'border-gray-200 dark:border-gray-700 hover:border-green-300'
              ]"
            >
              <div class="flex items-start">
                <div class="flex-shrink-0">
                  <div :class="['w-10 h-10 rounded-lg flex items-center justify-center', template.color]">
                    <component :is="template.icon" class="w-6 h-6 text-white" />
                  </div>
                </div>
                <div class="ml-4 flex-1">
                  <h4 class="text-lg font-semibold text-gray-900 dark:text-white">{{ template.name }}</h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">{{ template.description }}</p>
                  <div class="flex items-center mt-2">
                    <span class="text-xs bg-gray-100 dark:bg-gray-600 text-gray-700 dark:text-gray-300 px-2 py-1 rounded">
                      {{ template.nodes }} nodes
                    </span>
                    <span class="text-xs bg-gray-100 dark:bg-gray-600 text-gray-700 dark:text-gray-300 px-2 py-1 rounded ml-2">
                      {{ template.type }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Template Preview -->
          <div v-if="selectedTemplate" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Template Configuration</h4>
            <pre class="text-xs bg-gray-900 text-green-400 p-3 rounded overflow-x-auto">{{ JSON.stringify(selectedTemplate.config, null, 2) }}</pre>
          </div>
        </div>

        <!-- Import Actions -->
        <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
          <Button @click="goBack" variant="outline">
            Cancel
          </Button>
          <Button 
            @click="importProject"
            variant="primary"
            :loading="importing"
            :disabled="!canImport"
            class="bg-green-600 hover:bg-green-700 focus:ring-green-500"
          >
            Import Project
          </Button>
        </div>
      </div>

      <!-- Import History -->
      <div class="bg-white dark:bg-gray-800 shadow-sm rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Imports</h3>
        
        <div v-if="importHistory.length === 0" class="text-center py-8">
          <FolderIcon class="w-12 h-12 mx-auto text-gray-400 mb-4" />
          <p class="text-gray-500 dark:text-gray-400">No recent imports</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="item in importHistory"
            :key="item.id"
            class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center">
              <div :class="['w-10 h-10 rounded-lg flex items-center justify-center', getStatusColor(item.status)]">
                <CheckCircleIcon v-if="item.status === 'success'" class="w-6 h-6 text-white" />
                <XCircleIcon v-else-if="item.status === 'error'" class="w-6 h-6 text-white" />
                <ClockIcon v-else class="w-6 h-6 text-white" />
              </div>
              <div class="ml-4">
                <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ item.name }}</h4>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ item.timestamp }}</p>
                <p class="text-xs text-gray-600 dark:text-gray-300">{{ item.method }} • {{ item.size || 'N/A' }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <Button 
                @click="reimportProject(item)"
                variant="outline" 
                size="xs"
                :disabled="item.status === 'error'"
              >
                Reimport
              </Button>
              <Button 
                @click="removeFromHistory(item.id)"
                variant="ghost" 
                size="xs" 
                iconOnly
                :leftIcon="TrashIcon"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'
import { useEdgeAIStore } from '@/stores/edgeai'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import FileUpload from '@/components/ui/FileUpload.vue'
import {
  ArrowLeftIcon,
  FolderArrowDownIcon,
  SunIcon,
  MoonIcon,
  DocumentIcon,
  LinkIcon,
  DocumentArrowUpIcon,
  XMarkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  ClockIcon,
  FolderIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

// Icons for templates
import {
  CpuChipIcon,
  BuildingOfficeIcon,
  TruckIcon,
  HeartIcon,
  ShoppingBagIcon,
  BeakerIcon
} from '@heroicons/vue/24/solid'

const TemplateIcon = CpuChipIcon

const router = useRouter()
const themeStore = useThemeStore()
const uiStore = useUIStore()
const edgeaiStore = useEdgeAIStore()

// Component state
const importMethod = ref('file')
const importing = ref(false)
const loadingUrl = ref(false)

// File import
const uploadedFile = ref(null)
const parsedConfig = ref(null)
const validationResults = ref([])

// URL import
const configUrl = ref('')
const urlError = ref('')
const urlRequireAuth = ref(false)
const urlAuth = ref({ username: '', password: '' })
const urlConfig = ref(null)

// Template selection
const selectedTemplate = ref(null)

// Import history
const importHistory = ref([
  {
    id: 1,
    name: 'Manufacturing Project Template',
    method: 'Template',
    status: 'success',
    timestamp: '2024-01-15 10:30:00',
    size: '2.1 KB'
  },
  {
    id: 2,
    name: 'config-backup-20240114.json',
    method: 'File Upload',
    status: 'success',
    timestamp: '2024-01-14 16:45:00',
    size: '5.3 KB'
  },
  {
    id: 3,
    name: 'Remote Configuration',
    method: 'URL',
    status: 'error',
    timestamp: '2024-01-13 09:15:00',
    size: null
  }
])

// Templates
const templates = ref([
  {
    id: 'manufacturing',
    name: 'Smart Manufacturing',
    description: 'Industrial IoT and predictive maintenance setup',
    type: 'Industrial',
    nodes: 8,
    icon: BuildingOfficeIcon,
    color: 'bg-blue-600',
    config: {
      name: 'Smart Manufacturing Project',
      type: 'manufacturing',
      modelType: 'cnn',
      strategy: 'fedavg',
      nodes: { min: 3, max: 8, target: 5 },
      security: { encryption: true, auth: true }
    }
  },
  {
    id: 'traffic',
    name: 'Traffic Optimization',
    description: 'Smart city traffic flow management',
    type: 'Transportation',
    nodes: 15,
    icon: TruckIcon,
    color: 'bg-green-600',
    config: {
      name: 'Urban Traffic Control',
      type: 'traffic',
      modelType: 'rnn',
      strategy: 'fedprox',
      nodes: { min: 5, max: 15, target: 10 },
      security: { encryption: true, auth: true }
    }
  },
  {
    id: 'healthcare',
    name: 'Healthcare Analytics',
    description: 'Medical imaging and diagnostic AI',
    type: 'Healthcare',
    nodes: 5,
    icon: HeartIcon,
    color: 'bg-red-600',
    config: {
      name: 'Medical Imaging Analysis',
      type: 'healthcare',
      modelType: 'transformer',
      strategy: 'scaffold',
      nodes: { min: 3, max: 8, target: 5 },
      security: { encryption: true, auth: true }
    }
  },
  {
    id: 'retail',
    name: 'Retail Analytics',
    description: 'Customer behavior and inventory optimization',
    type: 'Retail',
    nodes: 12,
    icon: ShoppingBagIcon,
    color: 'bg-purple-600',
    config: {
      name: 'Retail Intelligence',
      type: 'retail',
      modelType: 'cnn',
      strategy: 'fedavg',
      nodes: { min: 5, max: 12, target: 8 },
      security: { encryption: true, auth: false }
    }
  },
  {
    id: 'research',
    name: 'Research Project',
    description: 'General purpose research and experimentation',
    type: 'Research',
    nodes: 10,
    icon: BeakerIcon,
    color: 'bg-indigo-600',
    config: {
      name: 'Research Project',
      type: 'research',
      modelType: 'custom',
      strategy: 'fedopt',
      nodes: { min: 2, max: 20, target: 10 },
      security: { encryption: false, auth: false }
    }
  }
])

// Computed properties
const canImport = computed(() => {
  switch (importMethod.value) {
    case 'file':
      return uploadedFile.value && parsedConfig.value && !hasValidationErrors.value
    case 'url':
      return urlConfig.value
    case 'template':
      return selectedTemplate.value
    default:
      return false
  }
})

const hasValidationErrors = computed(() => {
  return validationResults.value.some(result => result.type === 'error')
})

// Methods
const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const goBack = () => {
  router.push('/edgeai/dashboard')
}

const handleFileUpload = (file) => {
  uploadedFile.value = file
  parseConfigFile(file)
}

const parseConfigFile = async (file) => {
  try {
    const text = await file.text()
    let config
    
    if (file.name.endsWith('.json')) {
      config = JSON.parse(text)
    } else if (file.name.endsWith('.yaml') || file.name.endsWith('.yml')) {
      config = parseYAML(text)
    } else if (file.name.endsWith('.toml')) {
      config = parseTOML(text)
    } else {
      throw new Error('Unsupported file format. Please use JSON, YAML, or TOML.')
    }
    
    parsedConfig.value = config
    validateConfig(config)
    
  } catch (error) {
    uiStore.addNotification({
      type: 'error',
      title: 'Parse Error',
      message: 'Failed to parse configuration file: ' + error.message
    })
    validationResults.value = [{
      field: 'file',
      type: 'error',
      message: 'Invalid file format: ' + error.message
    }]
  }
}

// Enhanced parsers for different formats
const parseYAML = (text) => {
  // Basic YAML-like parsing (for demo purposes)
  // In a real implementation, you'd use a YAML parser library
  try {
    // Try to parse as JSON first
    return JSON.parse(text)
  } catch {
    // Simple YAML parsing for common cases
    const lines = text.split('\n')
    const config = {}
    let currentKey = null
    
    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed || trimmed.startsWith('#')) continue
      
      if (trimmed.includes(':')) {
        const [key, value] = trimmed.split(':').map(s => s.trim())
        if (value) {
          // Parse common types
          if (value === 'true') config[key] = true
          else if (value === 'false') config[key] = false
          else if (!isNaN(value)) config[key] = Number(value)
          else if (value.startsWith('"') && value.endsWith('"')) {
            config[key] = value.slice(1, -1)
          }
          else config[key] = value
        } else {
          currentKey = key
          config[key] = {}
        }
      }
    }
    
    return config
  }
}

const parseTOML = (text) => {
  // Basic TOML parsing (for demo purposes)
  // In a real implementation, you'd use a TOML parser library
  const config = {}
  const lines = text.split('\n')
  let currentSection = config
  
  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed || trimmed.startsWith('#')) continue
    
    if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
      // Section header
      const sectionName = trimmed.slice(1, -1)
      currentSection = config[sectionName] = {}
    } else if (trimmed.includes('=')) {
      const [key, value] = trimmed.split('=').map(s => s.trim())
      
      // Parse value
      if (value.startsWith('"') && value.endsWith('"')) {
        currentSection[key] = value.slice(1, -1)
      } else if (value === 'true') {
        currentSection[key] = true
      } else if (value === 'false') {
        currentSection[key] = false
      } else if (!isNaN(value)) {
        currentSection[key] = Number(value)
      } else {
        currentSection[key] = value
      }
    }
  }
  
  return config
}

const validateConfig = (config) => {
  const results = []
  
  // Required fields validation
  if (!config.name) {
    results.push({ field: 'name', type: 'error', message: 'Project name is required' })
  } else {
    results.push({ field: 'name', type: 'success', message: 'Project name is valid' })
  }
  
  if (!config.type) {
    results.push({ field: 'type', type: 'warning', message: 'Project type not specified, will default to "custom"' })
  } else {
    results.push({ field: 'type', type: 'success', message: 'Project type is valid' })
  }
  
  if (!config.modelType) {
    results.push({ field: 'modelType', type: 'warning', message: 'Model type not specified, will default to "cnn"' })
  } else {
    results.push({ field: 'modelType', type: 'success', message: 'Model type is valid' })
  }
  
  // Node configuration validation
  if (config.nodes) {
    if (config.nodes.min > config.nodes.max) {
      results.push({ field: 'nodes', type: 'error', message: 'Minimum nodes cannot exceed maximum nodes' })
    } else {
      results.push({ field: 'nodes', type: 'success', message: 'Node configuration is valid' })
    }
  }
  
  validationResults.value = results
}

const removeFile = () => {
  uploadedFile.value = null
  parsedConfig.value = null
  validationResults.value = []
}

const loadFromUrl = async () => {
  loadingUrl.value = true
  urlError.value = ''
  
  try {
    // Simulate URL loading
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Mock successful load
    urlConfig.value = {
      name: 'Remote Configuration',
      type: 'manufacturing',
      modelType: 'cnn',
      strategy: 'fedavg',
      nodes: { min: 3, max: 10, target: 5 },
      security: { encryption: true, auth: true }
    }
    
    uiStore.addNotification({
      type: 'success',
      title: 'Configuration Loaded',
      message: 'Successfully loaded configuration from URL'
    })
    
  } catch (error) {
    urlError.value = 'Failed to load configuration from URL'
    uiStore.addNotification({
      type: 'error',
      title: 'Load Failed',
      message: 'Failed to load configuration from URL'
    })
  } finally {
    loadingUrl.value = false
  }
}

const importProject = async () => {
  importing.value = true
  
  try {
    let config
    let method
    
    switch (importMethod.value) {
      case 'file':
        config = parsedConfig.value
        method = 'File Upload'
        break
      case 'url':
        config = urlConfig.value
        method = 'URL'
        break
      case 'template':
        config = selectedTemplate.value.config
        method = 'Template'
        break
    }
    
    // Use EdgeAI store to import project
    const result = await edgeaiStore.importProject(config)
    
    if (result.success) {
      // Add to history
      importHistory.value.unshift({
        id: Date.now(),
        name: config.name,
        method: method,
        status: 'success',
        timestamp: new Date().toLocaleString(),
        size: importMethod.value === 'file' ? formatFileSize(uploadedFile.value.size) : null
      })
      
      uiStore.addNotification({
        type: 'success',
        title: 'Project Imported',
        message: `Successfully imported project "${config.name}"`
      })
      
      // Redirect to dashboard to see the new project
      router.push('/edgeai/dashboard')
    } else {
      throw new Error(result.error || 'Failed to import project')
    }
    
  } catch (error) {
    // Add to history as failed
    if (parsedConfig.value || urlConfig.value || selectedTemplate.value) {
      const config = parsedConfig.value || urlConfig.value || selectedTemplate.value.config
      importHistory.value.unshift({
        id: Date.now(),
        name: config.name || 'Unknown Project',
        method: importMethod.value === 'file' ? 'File Upload' : importMethod.value === 'url' ? 'URL' : 'Template',
        status: 'error',
        timestamp: new Date().toLocaleString(),
        size: importMethod.value === 'file' && uploadedFile.value ? formatFileSize(uploadedFile.value.size) : null
      })
    }
    
    uiStore.addNotification({
      type: 'error',
      title: 'Import Failed',
      message: error.message || 'Failed to import project configuration'
    })
  } finally {
    importing.value = false
  }
}

const reimportProject = (item) => {
  uiStore.addNotification({
    type: 'info',
    title: 'Reimport Started',
    message: `Reimporting ${item.name}...`
  })
}

const removeFromHistory = (id) => {
  importHistory.value = importHistory.value.filter(item => item.id !== id)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getStatusColor = (status) => {
  const colors = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    pending: 'bg-yellow-500'
  }
  return colors[status] || 'bg-gray-500'
}
</script>