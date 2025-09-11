<template>
  <div :class="widgetContainerClasses">
    <!-- Widget Header -->
    <div 
      v-if="showHeader" 
      class="widget-header px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50"
    >
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <component 
            v-if="widget.icon" 
            :is="getWidgetIcon(widget.icon)" 
            class="w-4 h-4 text-gray-500 dark:text-gray-400"
          />
          <h3 class="text-sm font-medium text-gray-900 dark:text-white truncate">
            {{ widget.title }}
          </h3>
        </div>
        
        <div v-if="!editMode" class="flex items-center space-x-1">
          <!-- Refresh Button -->
          <button
            v-if="widget.refreshable"
            @click="refreshWidget"
            :disabled="loading"
            class="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            title="Refresh"
          >
            <ArrowPathIcon :class="['w-4 h-4 text-gray-500 dark:text-gray-400', loading && 'animate-spin']" />
          </button>
          
          <!-- More Options -->
          <div v-if="hasActions" class="relative">
            <button
              @click="showActionsMenu = !showActionsMenu"
              class="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            >
              <EllipsisVerticalIcon class="w-4 h-4 text-gray-500 dark:text-gray-400" />
            </button>
            
            <!-- Actions Dropdown -->
            <div
              v-if="showActionsMenu"
              class="absolute right-0 top-full mt-1 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg border border-gray-200 dark:border-gray-700 z-10"
              @click.stop
            >
              <div class="py-1">
                <button
                  v-for="action in widget.actions"
                  :key="action.key"
                  @click="handleAction(action)"
                  class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <component :is="action.icon" class="w-4 h-4 inline mr-2" />
                  {{ action.label }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Widget Content -->
    <div :class="widgetContentClasses">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center h-full">
        <LoadingSpinner size="md" text="Loading..." />
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="flex items-center justify-center h-full p-4">
        <div class="text-center">
          <ExclamationCircleIcon class="w-8 h-8 text-red-500 mx-auto mb-2" />
          <p class="text-sm text-red-600 dark:text-red-400">{{ error }}</p>
          <Button
            variant="ghost"
            size="sm"
            @click="refreshWidget"
            class="mt-2"
          >
            Try Again
          </Button>
        </div>
      </div>

      <!-- Widget Type Components -->
      <component
        v-else
        :is="widgetComponent"
        v-bind="widgetProps"
        :widget="widget"
        :config="widget.config"
        :width="width"
        :height="height"
        :edit-mode="editMode"
        @action="handleWidgetAction"
        @error="handleWidgetError"
        @data-change="handleDataChange"
      />
    </div>

    <!-- Edit Mode Overlay -->
    <div
      v-if="editMode && !widget.content"
      class="absolute inset-0 bg-gray-100 dark:bg-gray-800 bg-opacity-90 flex items-center justify-center rounded-lg"
    >
      <div class="text-center">
        <component 
          :is="getWidgetIcon(widget.icon)" 
          class="w-12 h-12 text-gray-400 mx-auto mb-2"
        />
        <p class="text-sm text-gray-600 dark:text-gray-400 font-medium">
          {{ widget.title }}
        </p>
        <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
          Click to configure
        </p>
      </div>
    </div>

    <!-- Click outside handler for actions menu -->
    <div
      v-if="showActionsMenu"
      @click="showActionsMenu = false"
      class="fixed inset-0 z-0"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import {
  ArrowPathIcon,
  EllipsisVerticalIcon,
  ExclamationCircleIcon,
  ChartBarIcon,
  ChartLineIcon,
  TableCellsIcon,
  PuzzlePieceIcon
} from '@heroicons/vue/24/outline'

// Widget type components
import StatCardWidget from './widgets/StatCardWidget.vue'
import LineChartWidget from './widgets/LineChartWidget.vue'
import TableWidget from './widgets/TableWidget.vue'
import ProgressRingWidget from './widgets/ProgressRingWidget.vue'
import ActivityFeedWidget from './widgets/ActivityFeedWidget.vue'

const props = defineProps({
  widget: {
    type: Object,
    required: true
  },
  width: {
    type: Number,
    default: 1
  },
  height: {
    type: Number,
    default: 1
  },
  editMode: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['action', 'error', 'data-change', 'refresh'])

// State
const loading = ref(false)
const error = ref('')
const showActionsMenu = ref(false)
let refreshInterval = null

// Widget component mapping
const widgetComponents = {
  'stat-card': StatCardWidget,
  'line-chart': LineChartWidget,
  'table': TableWidget,
  'progress-ring': ProgressRingWidget,
  'activity-feed': ActivityFeedWidget
}

// Icon mapping
const iconMap = {
  ChartBarIcon,
  ChartLineIcon,
  TableCellsIcon,
  PuzzlePieceIcon
}

// Computed properties
const widgetComponent = computed(() => {
  return widgetComponents[props.widget.type] || 'div'
})

const widgetContainerClasses = computed(() => {
  return [
    'widget-container relative h-full w-full bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden',
    props.editMode && 'edit-mode'
  ]
})

const widgetContentClasses = computed(() => {
  return [
    'widget-content relative flex-1',
    showHeader.value ? 'h-[calc(100%-57px)]' : 'h-full'
  ]
})

const showHeader = computed(() => {
  return props.widget.title && !props.widget.config?.hideHeader
})

const hasActions = computed(() => {
  return props.widget.actions && props.widget.actions.length > 0
})

const widgetProps = computed(() => {
  const baseProps = {
    loading: loading.value,
    error: error.value
  }
  
  // Add widget-specific props based on type
  switch (props.widget.type) {
    case 'stat-card':
      return {
        ...baseProps,
        value: props.widget.config.value,
        trend: props.widget.config.trend,
        unit: props.widget.config.unit,
        format: props.widget.config.format
      }
    case 'line-chart':
      return {
        ...baseProps,
        data: props.widget.data || [],
        xAxis: props.widget.config.xAxis,
        yAxis: props.widget.config.yAxis
      }
    case 'table':
      return {
        ...baseProps,
        data: props.widget.data || [],
        columns: props.widget.config.columns || []
      }
    case 'progress-ring':
      return {
        ...baseProps,
        value: props.widget.config.value || 0,
        max: props.widget.config.max || 100,
        color: props.widget.config.color || 'blue'
      }
    case 'activity-feed':
      return {
        ...baseProps,
        activities: props.widget.data || [],
        maxItems: props.widget.config.maxItems || 10
      }
    default:
      return baseProps
  }
})

// Methods
const getWidgetIcon = (iconName) => {
  return iconMap[iconName] || PuzzlePieceIcon
}

const refreshWidget = async () => {
  if (loading.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    // Emit refresh event for parent to handle
    emit('refresh', props.widget)
    
    // Simulate refresh delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
  } catch (err) {
    error.value = err.message || 'Failed to refresh widget'
    emit('error', { widget: props.widget, error: err })
  } finally {
    loading.value = false
  }
}

const handleAction = (action) => {
  showActionsMenu.value = false
  action.handler?.()
  emit('action', { widget: props.widget, action })
}

const handleWidgetAction = (action) => {
  emit('action', { widget: props.widget, ...action })
}

const handleWidgetError = (err) => {
  error.value = err.message || 'Widget error occurred'
  emit('error', { widget: props.widget, error: err })
}

const handleDataChange = (data) => {
  emit('data-change', { widget: props.widget, data })
}

const startAutoRefresh = () => {
  const interval = props.widget.config?.refreshInterval || 30000
  if (props.widget.config?.autoRefresh && interval > 0) {
    refreshInterval = setInterval(refreshWidget, interval)
  }
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

// Watch for configuration changes
watch(() => props.widget.config, (newConfig) => {
  if (newConfig?.autoRefresh !== props.widget.config?.autoRefresh) {
    if (newConfig?.autoRefresh) {
      startAutoRefresh()
    } else {
      stopAutoRefresh()
    }
  }
}, { deep: true })

// Lifecycle
onMounted(() => {
  // Load initial data if needed
  if (props.widget.config?.loadOnMount !== false) {
    refreshWidget()
  }
  
  // Start auto-refresh if enabled
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.widget-container {
  @apply flex flex-col;
}

.widget-content {
  @apply overflow-hidden;
}

.edit-mode {
  @apply opacity-90;
}

.widget-header {
  @apply flex-shrink-0;
}

/* Animations */
.widget-container {
  @apply transition-all duration-200 ease-in-out;
}

.widget-container:hover {
  @apply shadow-md;
}

.edit-mode:hover {
  @apply opacity-100;
}
</style>