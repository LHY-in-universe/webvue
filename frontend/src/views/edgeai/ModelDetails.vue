<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <Button 
              @click="$router.back()" 
              variant="ghost" 
              size="sm" 
              class="mr-4"
            >
              ← Back to Models
            </Button>
            <CpuChipIcon class="h-8 w-8 text-blue-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              {{ model.name }} Details
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Model Header -->
      <Card class="mb-8">
        <div class="flex items-start justify-between">
          <div class="flex items-center">
            <div class="h-16 w-16 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center mr-6">
              <CpuChipIcon class="h-8 w-8 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{{ model.name }}</h1>
              <p class="text-gray-600 dark:text-gray-400 mb-4">{{ model.description }}</p>
              <div class="flex items-center space-x-4">
                <span :class="getStatusColor(model.status)" class="inline-flex px-3 py-1 text-sm font-semibold rounded-full">
                  {{ model.status }}
                </span>
                <span :class="getTypeColor(model.type)" class="inline-flex px-3 py-1 text-sm font-semibold rounded-full">
                  {{ model.type }}
                </span>
                <span class="text-sm text-gray-500 dark:text-gray-400">Version {{ model.version }}</span>
              </div>
            </div>
          </div>
          
          <div class="flex space-x-3">
            <Button 
              @click="deployModel" 
              :variant="model.status === 'Active' ? 'secondary' : 'primary'"
              :disabled="model.status === 'Active'"
            >
              {{ model.status === 'Active' ? 'Deployed' : 'Deploy Model' }}
            </Button>
            <Button variant="secondary" @click="downloadModel">
              <ArrowDownTrayIcon class="w-4 h-4 mr-2" />
              Download
            </Button>
          </div>
        </div>
      </Card>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Model Information -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Model Specifications -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Model Specifications</h3>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Architecture</label>
                <p class="text-gray-900 dark:text-white">{{ model.architecture }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Framework</label>
                <p class="text-gray-900 dark:text-white">{{ model.framework }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Parameters</label>
                <p class="text-gray-900 dark:text-white">{{ model.parameters }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Input Size</label>
                <p class="text-gray-900 dark:text-white">{{ model.inputSize }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">File Size</label>
                <p class="text-gray-900 dark:text-white">{{ model.size }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">License</label>
                <p class="text-gray-900 dark:text-white">{{ model.license }}</p>
              </div>
            </div>
          </Card>

          <!-- Performance Metrics -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Performance Metrics</h3>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div class="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-2">{{ model.accuracy }}%</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Accuracy</div>
              </div>
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div class="text-2xl font-bold text-green-600 dark:text-green-400 mb-2">{{ model.latency }}ms</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Latency</div>
              </div>
              <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div class="text-2xl font-bold text-purple-600 dark:text-purple-400 mb-2">{{ model.throughput }}</div>
                <div class="text-sm text-gray-600 dark:text-gray-400">Throughput</div>
              </div>
            </div>
          </Card>

          <!-- Usage Examples -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Usage Examples</h3>
            </template>
            
            <div class="space-y-4">
              <div>
                <h4 class="font-medium text-gray-900 dark:text-white mb-2">Python API</h4>
                <pre class="bg-gray-800 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm"><code>import edgeai

# Load the model
model = edgeai.load_model('{{ model.name.toLowerCase().replace(/[^a-z0-9]/g, '-') }}')

# Make predictions
result = model.predict(input_data)
print(result)</code></pre>
              </div>
              
              <div>
                <h4 class="font-medium text-gray-900 dark:text-white mb-2">REST API</h4>
                <pre class="bg-gray-800 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm"><code>curl -X POST "https://api.edgeai.com/v1/models/{{ model.name.toLowerCase().replace(/[^a-z0-9]/g, '-') }}/predict" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "your_input_data"}'</code></pre>
              </div>
            </div>
          </Card>
        </div>

        <!-- Sidebar -->
        <div class="space-y-8">
          <!-- Quick Actions -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Quick Actions</h3>
            </template>
            
            <div class="space-y-3">
              <Button 
                class="w-full justify-start" 
                variant="ghost"
                @click="testModel"
              >
                <PlayIcon class="w-4 h-4 mr-2" />
                Test Model
              </Button>
              <Button 
                class="w-full justify-start" 
                variant="ghost"
                @click="viewLogs"
              >
                <DocumentTextIcon class="w-4 h-4 mr-2" />
                View Logs
              </Button>
              <Button 
                class="w-full justify-start" 
                variant="ghost"
                @click="exportModel"
              >
                <ShareIcon class="w-4 h-4 mr-2" />
                Export Model
              </Button>
              <Button 
                class="w-full justify-start text-red-600 hover:text-red-700" 
                variant="ghost"
                @click="deleteModel"
              >
                <TrashIcon class="w-4 h-4 mr-2" />
                Delete Model
              </Button>
            </div>
          </Card>

          <!-- Model Statistics -->
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold">Statistics</h3>
            </template>
            
            <div class="space-y-4">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Downloads:</span>
                <span class="font-medium">{{ model.downloads }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Deployments:</span>
                <span class="font-medium">{{ model.deployments }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Created:</span>
                <span class="font-medium">{{ model.created }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-400">Last Updated:</span>
                <span class="font-medium">{{ model.lastUpdated }}</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import {
  CpuChipIcon,
  ArrowDownTrayIcon,
  PlayIcon,
  DocumentTextIcon,
  ShareIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()

// Mock model data (in real app, would fetch based on route.params.id)
const model = ref({
  id: 1,
  name: 'Gemma-7B-Instruct',
  description: 'Large language model optimized for instruction following and conversational AI tasks',
  type: 'LLM',
  version: 'v2.1.0',
  status: 'Active',
  size: '14.2 GB',
  architecture: 'Transformer',
  framework: 'PyTorch',
  parameters: '7B',
  inputSize: '8192 tokens',
  license: 'Apache 2.0',
  accuracy: 94.2,
  latency: 156,
  throughput: '127 tokens/sec',
  downloads: 15420,
  deployments: 89,
  created: '2024-01-15',
  lastUpdated: '2 hours ago'
})

// Utility functions
const getStatusColor = (status) => {
  const colors = {
    Active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    Inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    Error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return colors[status] || colors.Inactive
}

const getTypeColor = (type) => {
  const colors = {
    LLM: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    Vision: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    Audio: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    Other: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
  }
  return colors[type] || colors.Other
}

// Handler functions
const deployModel = () => {
  if (model.value.status !== 'Active') {
    model.value.status = 'Active'
    console.log('Model deployed successfully')
  }
}

const downloadModel = () => {
  console.log('Downloading model:', model.value.name)
}

const testModel = () => {
  console.log('Testing model:', model.value.name)
}

const viewLogs = () => {
  console.log('Viewing model logs')
}

const exportModel = () => {
  console.log('Exporting model')
}

const deleteModel = () => {
  if (confirm(`Are you sure you want to delete ${model.value.name}?`)) {
    console.log('Deleting model')
    router.push('/edgeai/model-management')
  }
}

onMounted(() => {
  // In real app, fetch model details based on route.params.id
  console.log('Loading model details for ID:', route.params.id)
})
</script>