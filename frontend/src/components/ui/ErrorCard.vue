<template>
  <div 
    :class="[
      'card-base border-l-4 p-6',
      severityClasses.border,
      severityClasses.background
    ]"
  >
    <div class="flex items-start space-x-4">
      <!-- Error Icon -->
      <div 
        :class="[
          'flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center',
          severityClasses.iconBackground
        ]"
      >
        <component 
          :is="errorIcon" 
          :class="['w-6 h-6', severityClasses.iconColor]"
        />
      </div>
      
      <div class="flex-1 min-w-0">
        <!-- Error Header -->
        <div class="flex items-start justify-between">
          <div>
            <h3 class="text-heading-3 text-gray-900 dark:text-white">
              {{ title || defaultTitle }}
            </h3>
            <p 
              v-if="message" 
              class="mt-1 text-body text-gray-700 dark:text-gray-300"
            >
              {{ message }}
            </p>
          </div>
          
          <!-- Dismiss Button -->
          <button
            v-if="dismissible"
            @click="dismiss"
            class="flex-shrink-0 ml-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          >
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>

        <!-- Error Code & Timestamp -->
        <div v-if="errorCode || timestamp" class="mt-3 flex items-center space-x-4 text-body-sm text-gray-600 dark:text-gray-400">
          <span v-if="errorCode" class="font-mono bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
            {{ errorCode }}
          </span>
          <span v-if="timestamp">
            {{ formatTimestamp(timestamp) }}
          </span>
        </div>

        <!-- Error Details (Collapsible) -->
        <div v-if="details || stackTrace" class="mt-4">
          <button
            @click="showDetails = !showDetails"
            class="flex items-center text-body-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
          >
            <ChevronDownIcon 
              :class="[
                'w-4 h-4 mr-1 transition-transform duration-200',
                { 'transform rotate-180': showDetails }
              ]"
            />
            {{ showDetails ? '隐藏详情' : '显示详情' }}
          </button>
          
          <div v-if="showDetails" class="mt-3 animate-fade-in">
            <!-- Error Details -->
            <div v-if="details" class="mb-4 p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
              <h4 class="text-body-sm font-medium text-gray-900 dark:text-white mb-2">
                错误详情
              </h4>
              <div class="text-body-sm text-gray-700 dark:text-gray-300 space-y-1">
                <div v-for="(detail, key) in details" :key="key" class="flex">
                  <span class="font-medium min-w-20">{{ key }}:</span>
                  <span class="ml-2">{{ detail }}</span>
                </div>
              </div>
            </div>
            
            <!-- Stack Trace -->
            <div v-if="stackTrace" class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
              <h4 class="text-body-sm font-medium text-gray-900 dark:text-white mb-2">
                堆栈跟踪
              </h4>
              <pre class="text-xs text-gray-700 dark:text-gray-300 font-mono whitespace-pre-wrap overflow-x-auto scrollbar-thin">{{ stackTrace }}</pre>
            </div>
          </div>
        </div>

        <!-- Suggested Actions -->
        <div v-if="suggestions && suggestions.length" class="mt-4">
          <h4 class="text-body-sm font-medium text-gray-900 dark:text-white mb-2">
            建议的解决方案
          </h4>
          <ul class="space-y-1">
            <li 
              v-for="(suggestion, index) in suggestions" 
              :key="index"
              class="flex items-start space-x-2 text-body-sm text-gray-700 dark:text-gray-300"
            >
              <div class="flex-shrink-0 w-1.5 h-1.5 bg-primary-500 rounded-full mt-2"></div>
              <span>{{ suggestion }}</span>
            </li>
          </ul>
        </div>

        <!-- Action Buttons -->
        <div v-if="actions && actions.length" class="mt-6 flex flex-wrap gap-3">
          <button
            v-for="(action, index) in actions"
            :key="index"
            :class="[
              'btn-base px-4 py-2',
              action.variant === 'primary' ? 'btn-primary' :
              action.variant === 'secondary' ? 'btn-secondary' :
              action.variant === 'success' ? 'btn-success' :
              action.variant === 'warning' ? 'btn-warning' :
              action.variant === 'danger' ? 'btn-danger' :
              'btn-ghost'
            ]"
            @click="handleActionClick(action)"
          >
            <component v-if="action.icon" :is="action.icon" class="w-4 h-4 mr-2" />
            {{ action.label }}
          </button>
        </div>

        <!-- Retry Button -->
        <div v-if="retryable" class="mt-6">
          <button
            @click="retry"
            :disabled="retrying"
            class="btn-primary px-4 py-2"
          >
            <ArrowPathIcon v-if="retrying" class="w-4 h-4 mr-2 animate-spin" />
            <ArrowPathIcon v-else class="w-4 h-4 mr-2" />
            {{ retrying ? '重试中...' : '重试' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  ExclamationTriangleIcon, 
  XCircleIcon, 
  InformationCircleIcon,
  XMarkIcon,
  ChevronDownIcon,
  ArrowPathIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  severity: {
    type: String,
    default: 'error',
    validator: value => ['error', 'warning', 'info'].includes(value)
  },
  title: String,
  message: String,
  errorCode: String,
  details: Object,
  stackTrace: String,
  suggestions: Array,
  actions: Array,
  timestamp: [String, Date, Number],
  dismissible: {
    type: Boolean,
    default: true
  },
  retryable: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['dismiss', 'retry', 'action'])

const showDetails = ref(false)
const retrying = ref(false)

const severityClasses = computed(() => {
  const variants = {
    error: {
      border: 'border-l-danger-500',
      background: 'bg-danger-50/50 dark:bg-danger-900/10',
      iconBackground: 'bg-danger-100 dark:bg-danger-900/20',
      iconColor: 'text-danger-600 dark:text-danger-400'
    },
    warning: {
      border: 'border-l-warning-500',
      background: 'bg-warning-50/50 dark:bg-warning-900/10',
      iconBackground: 'bg-warning-100 dark:bg-warning-900/20',
      iconColor: 'text-warning-600 dark:text-warning-400'
    },
    info: {
      border: 'border-l-info-500',
      background: 'bg-info-50/50 dark:bg-info-900/10',
      iconBackground: 'bg-info-100 dark:bg-info-900/20',
      iconColor: 'text-info-600 dark:text-info-400'
    }
  }
  
  return variants[props.severity] || variants.error
})

const errorIcon = computed(() => {
  const icons = {
    error: XCircleIcon,
    warning: ExclamationTriangleIcon,
    info: InformationCircleIcon
  }
  
  return icons[props.severity] || icons.error
})

const defaultTitle = computed(() => {
  const titles = {
    error: '发生错误',
    warning: '警告',
    info: '信息'
  }
  
  return titles[props.severity] || titles.error
})

const dismiss = () => {
  emit('dismiss')
}

const retry = async () => {
  retrying.value = true
  try {
    await emit('retry')
  } finally {
    retrying.value = false
  }
}

const handleActionClick = (action) => {
  emit('action', action)
  if (action.handler) {
    action.handler()
  }
}

const formatTimestamp = (timestamp) => {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>