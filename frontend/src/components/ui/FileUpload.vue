<template>
  <div :class="containerClasses">
    <!-- Label -->
    <label v-if="label" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>

    <!-- Drop Zone -->
    <div
      ref="dropZone"
      :class="dropZoneClasses"
      @click="triggerFileInput"
      @dragover="handleDragOver"
      @dragenter="handleDragEnter"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
      @keydown="handleKeydown"
      tabindex="0"
      role="button"
      :aria-label="dropzoneAriaLabel"
    >
      <!-- Upload Content -->
      <div class="flex flex-col items-center justify-center space-y-4 p-6">
        <!-- Upload Icon/Animation -->
        <div class="relative">
          <CloudArrowUpIcon 
            v-if="!isDragging && !uploading" 
            :class="iconClasses" 
          />
          <div 
            v-else-if="uploading" 
            class="flex items-center justify-center"
          >
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
          <div 
            v-else 
            class="animate-bounce"
          >
            <CloudArrowDownIcon :class="[iconClasses, 'text-blue-600']" />
          </div>
        </div>

        <!-- Upload Text -->
        <div class="text-center">
          <div v-if="isDragging" class="text-blue-600 dark:text-blue-400 font-medium">
            {{ dragText }}
          </div>
          <div v-else-if="uploading" class="text-gray-600 dark:text-gray-400">
            {{ uploadingText }}
          </div>
          <div v-else class="text-gray-600 dark:text-gray-400">
            <span class="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-500 cursor-pointer">
              {{ clickText }}
            </span>
            {{ dragDropText }}
          </div>
          
          <!-- File Constraints -->
          <div v-if="showConstraints" class="mt-2 text-xs text-gray-500 dark:text-gray-400 space-y-1">
            <div v-if="acceptedTypes.length > 0">
              Accepted: {{ acceptedTypesText }}
            </div>
            <div v-if="maxFileSize">
              Max size: {{ formatFileSize(maxFileSize) }}
            </div>
            <div v-if="maxFiles > 1">
              Max files: {{ maxFiles }}
            </div>
          </div>
        </div>
      </div>

      <!-- Hidden File Input -->
      <input
        ref="fileInput"
        type="file"
        :accept="acceptAttribute"
        :multiple="maxFiles > 1"
        :disabled="disabled"
        class="hidden"
        @change="handleFileSelect"
      />
    </div>

    <!-- File Preview List -->
    <div v-if="previewFiles.length > 0" class="mt-4 space-y-3">
      <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100">
        {{ previewFiles.length === 1 ? 'Selected File' : `Selected Files (${previewFiles.length})` }}
      </h4>
      
      <div class="space-y-2 max-h-64 overflow-y-auto">
        <div
          v-for="(file, index) in previewFiles"
          :key="file.id"
          :class="fileItemClasses"
        >
          <!-- File Icon -->
          <div class="flex-shrink-0">
            <div v-if="isImage(file.type)" class="relative">
              <img
                v-if="file.preview"
                :src="file.preview"
                :alt="file.name"
                class="w-10 h-10 rounded-lg object-cover"
              />
              <PhotoIcon v-else class="w-10 h-10 text-gray-400" />
            </div>
            <div v-else-if="isVideo(file.type)" class="w-10 h-10 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
              <VideoCameraIcon class="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div v-else-if="isAudio(file.type)" class="w-10 h-10 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
              <MusicalNoteIcon class="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <div v-else-if="isPDF(file.type)" class="w-10 h-10 bg-red-100 dark:bg-red-900 rounded-lg flex items-center justify-center">
              <DocumentTextIcon class="w-6 h-6 text-red-600 dark:text-red-400" />
            </div>
            <div v-else class="w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
              <DocumentIcon class="w-6 h-6 text-gray-600 dark:text-gray-400" />
            </div>
          </div>

          <!-- File Info -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between">
              <h5 class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                {{ file.name }}
              </h5>
              <button
                v-if="!disabled && !file.uploading"
                @click="removeFile(index)"
                class="ml-2 p-1 text-gray-400 hover:text-red-500 transition-colors"
                :aria-label="`Remove ${file.name}`"
              >
                <XMarkIcon class="w-4 h-4" />
              </button>
            </div>
            
            <div class="flex items-center justify-between mt-1">
              <span class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatFileSize(file.size) }}
              </span>
              
              <!-- Upload Status -->
              <div class="flex items-center space-x-2">
                <div v-if="file.error" class="flex items-center text-red-600 dark:text-red-400">
                  <ExclamationTriangleIcon class="w-4 h-4 mr-1" />
                  <span class="text-xs">{{ file.error }}</span>
                </div>
                <div v-else-if="file.uploaded" class="flex items-center text-green-600 dark:text-green-400">
                  <CheckCircleIcon class="w-4 h-4 mr-1" />
                  <span class="text-xs">Uploaded</span>
                </div>
                <div v-else-if="file.uploading" class="flex items-center text-blue-600 dark:text-blue-400">
                  <div class="animate-spin rounded-full h-3 w-3 border border-blue-600 border-t-transparent mr-1"></div>
                  <span class="text-xs">{{ file.progress ? `${file.progress}%` : 'Uploading...' }}</span>
                </div>
                <span v-else class="text-xs text-gray-400">Ready</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div v-if="file.uploading && file.progress !== undefined" class="mt-2">
              <div class="bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
                <div 
                  class="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
                  :style="{ width: `${file.progress}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Upload All Button -->
      <div v-if="showUploadButton && hasFilesToUpload" class="flex justify-end">
        <button
          @click="uploadAll"
          :disabled="uploading"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <CloudArrowUpIcon class="w-4 h-4 mr-2" />
          {{ uploading ? 'Uploading...' : 'Upload All' }}
        </button>
      </div>
    </div>

    <!-- Error Messages -->
    <div v-if="errorMessages.length > 0" class="mt-3 space-y-1">
      <div
        v-for="(error, index) in errorMessages"
        :key="index"
        class="flex items-start text-sm text-red-600 dark:text-red-400"
      >
        <ExclamationTriangleIcon class="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" />
        <span>{{ error }}</span>
      </div>
    </div>

    <!-- Help Text -->
    <div v-if="helpText && errorMessages.length === 0" class="mt-2 text-sm text-gray-500 dark:text-gray-400">
      {{ helpText }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import {
  CloudArrowUpIcon,
  CloudArrowDownIcon,
  PhotoIcon,
  VideoCameraIcon,
  MusicalNoteIcon,
  DocumentTextIcon,
  DocumentIcon,
  XMarkIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'

const { isMobile } = useResponsive()

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  label: {
    type: String,
    default: ''
  },
  helpText: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  maxFiles: {
    type: Number,
    default: 1
  },
  maxFileSize: {
    type: Number,
    default: 10 * 1024 * 1024 // 10MB
  },
  acceptedTypes: {
    type: Array,
    default: () => []
  },
  autoUpload: {
    type: Boolean,
    default: false
  },
  uploadUrl: {
    type: String,
    default: ''
  },
  uploadHeaders: {
    type: Object,
    default: () => ({})
  },
  showUploadButton: {
    type: Boolean,
    default: true
  },
  showConstraints: {
    type: Boolean,
    default: true
  },
  generatePreview: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  },
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'bordered', 'filled'].includes(value)
  },
  // Text customization
  clickText: {
    type: String,
    default: 'Click to upload'
  },
  dragDropText: {
    type: String,
    default: ' or drag and drop'
  },
  dragText: {
    type: String,
    default: 'Drop files here'
  },
  uploadingText: {
    type: String,
    default: 'Uploading files...'
  }
})

const emit = defineEmits([
  'update:modelValue',
  'files-added',
  'files-removed',
  'upload-start',
  'upload-progress',
  'upload-success',
  'upload-error',
  'upload-complete'
])

// Refs
const dropZone = ref(null)
const fileInput = ref(null)

// State
const isDragging = ref(false)
const uploading = ref(false)
const previewFiles = ref([])
const errorMessages = ref([])
const fileIdCounter = ref(0)

// Computed
const containerClasses = computed(() => 'w-full')

const dropZoneClasses = computed(() => {
  const baseClasses = 'relative border-2 border-dashed rounded-lg transition-colors duration-200 cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500'
  
  const sizeClasses = {
    sm: 'min-h-32',
    md: 'min-h-40',
    lg: 'min-h-48'
  }
  
  const variantClasses = {
    default: 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500',
    bordered: 'border-gray-400 dark:border-gray-500 bg-gray-50 dark:bg-gray-800',
    filled: 'border-blue-300 dark:border-blue-600 bg-blue-50 dark:bg-blue-900/20'
  }
  
  const stateClasses = {
    dragging: 'border-blue-400 bg-blue-50 dark:bg-blue-900/20',
    disabled: 'opacity-50 cursor-not-allowed',
    error: 'border-red-300 dark:border-red-600'
  }
  
  return [
    baseClasses,
    sizeClasses[props.size],
    variantClasses[props.variant],
    isDragging.value && stateClasses.dragging,
    props.disabled && stateClasses.disabled,
    errorMessages.value.length > 0 && stateClasses.error
  ]
})

const iconClasses = computed(() => [
  'w-8 h-8',
  isDragging.value ? 'text-blue-600 dark:text-blue-400' : 'text-gray-400 dark:text-gray-500'
])

const fileItemClasses = computed(() => [
  'flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700'
])

const acceptAttribute = computed(() => {
  return props.acceptedTypes.length > 0 ? props.acceptedTypes.join(',') : ''
})

const acceptedTypesText = computed(() => {
  if (props.acceptedTypes.length === 0) return 'All files'
  return props.acceptedTypes.map(type => {
    if (type.startsWith('.')) return type.toUpperCase()
    return type.split('/')[1]?.toUpperCase() || type
  }).join(', ')
})

const dropzoneAriaLabel = computed(() => {
  return `Upload files. ${props.acceptedTypes.length > 0 ? `Accepted types: ${acceptedTypesText.value}.` : ''} ${props.maxFileSize ? `Maximum size: ${formatFileSize(props.maxFileSize)}.` : ''}`
})

const hasFilesToUpload = computed(() => {
  return previewFiles.value.some(file => !file.uploaded && !file.uploading && !file.error)
})

// Methods
const triggerFileInput = () => {
  if (props.disabled) return
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  addFiles(files)
  // Reset input value to allow selecting the same file again
  event.target.value = ''
}

const handleDragOver = (event) => {
  event.preventDefault()
  event.stopPropagation()
}

const handleDragEnter = (event) => {
  event.preventDefault()
  event.stopPropagation()
  isDragging.value = true
}

const handleDragLeave = (event) => {
  event.preventDefault()
  event.stopPropagation()
  // Only set to false if leaving the dropzone entirely
  if (!dropZone.value?.contains(event.relatedTarget)) {
    isDragging.value = false
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  event.stopPropagation()
  isDragging.value = false
  
  if (props.disabled) return
  
  const files = Array.from(event.dataTransfer.files)
  addFiles(files)
}

const handleKeydown = (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault()
    triggerFileInput()
  }
}

const addFiles = async (files) => {
  errorMessages.value = []
  
  // Check file limits
  const remainingSlots = props.maxFiles - previewFiles.value.length
  if (files.length > remainingSlots) {
    errorMessages.value.push(`Can only add ${remainingSlots} more file${remainingSlots !== 1 ? 's' : ''}`)
    files = files.slice(0, remainingSlots)
  }
  
  const validFiles = []
  
  for (const file of files) {
    const validation = validateFile(file)
    if (validation.valid) {
      const fileObj = await createFileObject(file)
      validFiles.push(fileObj)
    } else {
      errorMessages.value.push(...validation.errors)
    }
  }
  
  if (validFiles.length > 0) {
    previewFiles.value.push(...validFiles)
    emit('files-added', validFiles)
    updateModelValue()
    
    if (props.autoUpload) {
      uploadFiles(validFiles)
    }
  }
}

const validateFile = (file) => {
  const errors = []
  
  // Check file type
  if (props.acceptedTypes.length > 0) {
    const isAccepted = props.acceptedTypes.some(type => {
      if (type.startsWith('.')) {
        return file.name.toLowerCase().endsWith(type.toLowerCase())
      }
      return file.type.includes(type) || file.type === type
    })
    
    if (!isAccepted) {
      errors.push(`${file.name}: File type not accepted`)
    }
  }
  
  // Check file size
  if (props.maxFileSize && file.size > props.maxFileSize) {
    errors.push(`${file.name}: File size exceeds ${formatFileSize(props.maxFileSize)}`)
  }
  
  return {
    valid: errors.length === 0,
    errors
  }
}

const createFileObject = async (file) => {
  const fileObj = {
    id: `file_${fileIdCounter.value++}`,
    name: file.name,
    size: file.size,
    type: file.type,
    lastModified: file.lastModified,
    file: file,
    preview: null,
    uploading: false,
    uploaded: false,
    progress: 0,
    error: null
  }
  
  // Generate preview for images
  if (props.generatePreview && isImage(file.type)) {
    try {
      fileObj.preview = await generatePreview(file)
    } catch (error) {
      console.warn('Failed to generate preview:', error)
    }
  }
  
  return fileObj
}

const generatePreview = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => resolve(e.target.result)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

const removeFile = (index) => {
  const removedFiles = previewFiles.value.splice(index, 1)
  emit('files-removed', removedFiles)
  updateModelValue()
}

const uploadAll = () => {
  const filesToUpload = previewFiles.value.filter(file => !file.uploaded && !file.uploading && !file.error)
  if (filesToUpload.length > 0) {
    uploadFiles(filesToUpload)
  }
}

const uploadFiles = async (files) => {
  if (!props.uploadUrl) {
    console.warn('No upload URL provided')
    return
  }
  
  uploading.value = true
  emit('upload-start', files)
  
  const uploadPromises = files.map(file => uploadSingleFile(file))
  
  try {
    await Promise.allSettled(uploadPromises)
  } catch (error) {
    console.error('Upload error:', error)
  } finally {
    uploading.value = false
    emit('upload-complete', files)
    updateModelValue()
  }
}

const uploadSingleFile = async (fileObj) => {
  fileObj.uploading = true
  fileObj.progress = 0
  fileObj.error = null
  
  const formData = new FormData()
  formData.append('file', fileObj.file)
  
  try {
    const response = await fetch(props.uploadUrl, {
      method: 'POST',
      headers: {
        ...props.uploadHeaders
      },
      body: formData
    })
    
    if (response.ok) {
      const result = await response.json()
      fileObj.uploaded = true
      fileObj.progress = 100
      emit('upload-success', { file: fileObj, response: result })
    } else {
      throw new Error(`Upload failed: ${response.statusText}`)
    }
  } catch (error) {
    fileObj.error = error.message
    emit('upload-error', { file: fileObj, error })
  } finally {
    fileObj.uploading = false
  }
}

const updateModelValue = () => {
  emit('update:modelValue', previewFiles.value)
}

// File type helpers
const isImage = (type) => type.startsWith('image/')
const isVideo = (type) => type.startsWith('video/')
const isAudio = (type) => type.startsWith('audio/')
const isPDF = (type) => type === 'application/pdf'

// Format file size
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  if (Array.isArray(newValue)) {
    previewFiles.value = [...newValue]
  }
})

// Expose methods
defineExpose({
  triggerFileInput,
  uploadAll,
  removeFile,
  addFiles
})
</script>

<style scoped>
/* Animation for file items */
.file-item-enter-active,
.file-item-leave-active {
  transition: all 0.3s ease;
}

.file-item-enter-from,
.file-item-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Custom scrollbar for file list */
.max-h-64::-webkit-scrollbar {
  width: 6px;
}

.max-h-64::-webkit-scrollbar-track {
  background: transparent;
}

.max-h-64::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.4);
  border-radius: 3px;
}

.max-h-64::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.6);
}
</style>