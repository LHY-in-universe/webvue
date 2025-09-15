<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 overflow-y-auto"
    aria-labelledby="modal-title"
    role="dialog"
    aria-modal="true"
  >
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div 
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
        @click="close"
      ></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <div class="sm:flex sm:items-start">
          <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900 sm:mx-0 sm:h-10 sm:w-10">
            <CloudArrowUpIcon class="h-6 w-6 text-blue-600 dark:text-blue-400" />
          </div>
          <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left flex-1">
            <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white" id="modal-title">
              Upload New Model
            </h3>
            <div class="mt-4">
              <form @submit.prevent="uploadModel" class="space-y-4">
                <!-- Model Name -->
                <div>
                  <label for="modelName" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Model Name
                  </label>
                  <input
                    v-model="form.name"
                    type="text"
                    id="modelName"
                    required
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
                    placeholder="e.g. My Custom Model"
                  />
                </div>

                <!-- Model Type -->
                <div>
                  <label for="modelType" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Model Type
                  </label>
                  <select
                    v-model="form.type"
                    id="modelType"
                    required
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
                  >
                    <option value="">Select type</option>
                    <option value="LLM">Language Model</option>
                    <option value="Vision">Computer Vision</option>
                    <option value="Audio">Audio Processing</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <!-- Description -->
                <div>
                  <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Description
                  </label>
                  <textarea
                    v-model="form.description"
                    id="description"
                    rows="3"
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
                    placeholder="Brief description of your model..."
                  ></textarea>
                </div>

                <!-- File Upload -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Model File
                  </label>
                  <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-md">
                    <div class="space-y-1 text-center">
                      <CloudArrowUpIcon class="mx-auto h-12 w-12 text-gray-400" />
                      <div class="flex text-sm text-gray-600 dark:text-gray-400">
                        <label
                          for="file-upload"
                          class="relative cursor-pointer bg-white dark:bg-gray-800 rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500"
                        >
                          <span>Upload a file</span>
                          <input
                            id="file-upload"
                            name="file-upload"
                            type="file"
                            class="sr-only"
                            @change="handleFileSelect"
                            accept=".pt,.pth,.onnx,.pb,.h5,.pkl,.safetensors"
                          />
                        </label>
                        <p class="pl-1">or drag and drop</p>
                      </div>
                      <p class="text-xs text-gray-500 dark:text-gray-400">
                        PT, ONNX, H5, PKL up to 10GB
                      </p>
                      <p v-if="selectedFile" class="text-sm text-green-600 dark:text-green-400">
                        Selected: {{ selectedFile.name }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Version -->
                <div>
                  <label for="version" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Version
                  </label>
                  <input
                    v-model="form.version"
                    type="text"
                    id="version"
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
                    placeholder="v1.0.0"
                  />
                </div>
              </form>
            </div>
          </div>
        </div>
        
        <!-- Upload Progress -->
        <div v-if="uploading" class="mt-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Uploading...</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">{{ uploadProgress }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-600 h-2 rounded-full transition-all duration-300" 
              :style="{ width: uploadProgress + '%' }"
            ></div>
          </div>
        </div>

        <!-- Action buttons -->
        <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
          <Button
            @click="uploadModel"
            :disabled="!canUpload || uploading"
            class="w-full sm:w-auto sm:ml-3"
          >
            {{ uploading ? 'Uploading...' : 'Upload Model' }}
          </Button>
          <Button
            @click="close"
            variant="secondary"
            :disabled="uploading"
            class="mt-3 w-full sm:mt-0 sm:w-auto"
          >
            Cancel
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUIStore } from '@/stores/ui'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import { CloudArrowUpIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'uploaded'])

const uiStore = useUIStore()

const form = ref({
  name: '',
  type: '',
  description: '',
  version: 'v1.0.0'
})

const selectedFile = ref(null)
const uploading = ref(false)
const uploadProgress = ref(0)

const canUpload = computed(() => {
  return form.value.name && form.value.type && selectedFile.value
})

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
  }
}

const uploadModel = async () => {
  if (!canUpload.value || uploading.value) return

  const pageMonitor = performanceMonitor.monitorPageLoad('ModelUpload')
  uploading.value = true
  uploadProgress.value = 0

  try {
    // Create FormData for file upload
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('name', form.value.name)
    formData.append('description', form.value.description)
    formData.append('model_type', form.value.type)
    formData.append('version', form.value.version)

    // Upload with progress tracking
    const result = await edgeaiService.models.uploadModel(formData, (progress) => {
      uploadProgress.value = Math.round(progress)
    })

    if (result.success) {
      const newModel = {
        id: result.data.id,
        name: result.data.name,
        description: result.data.description,
        type: result.data.model_type,
        version: result.data.version,
        status: result.data.status || 'Inactive',
        size: formatFileSize(result.data.file_size),
        lastUpdated: 'just now',
        accuracy: result.data.accuracy || 0,
        latency: result.data.latency || 0,
        downloads: 0,
        deployments: 0
      }

      uiStore.addNotification({
        type: 'success',
        title: 'Model Uploaded',
        message: `${form.value.name} has been uploaded successfully`
      })

      emit('uploaded', newModel)
      close()
    } else {
      throw new Error(result.error || 'Failed to upload model')
    }

    pageMonitor.end()

  } catch (err) {
    console.error('Failed to upload model:', err)
    uiStore.addNotification({
      type: 'error',
      title: 'Upload Failed',
      message: err.message || 'Failed to upload model'
    })
    pageMonitor.end()
  } finally {
    uploading.value = false
  }
}

const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const close = () => {
  if (!uploading.value) {
    // Reset form
    form.value = {
      name: '',
      type: '',
      description: '',
      version: 'v1.0.0'
    }
    selectedFile.value = null
    uploadProgress.value = 0
    emit('close')
  }
}
</script>