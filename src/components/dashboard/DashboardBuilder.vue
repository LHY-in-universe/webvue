<template>
  <div class="dashboard-builder">
    <!-- Builder Header -->
    <div class="flex items-center justify-between p-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center space-x-4">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
          {{ editMode ? 'Edit Dashboard' : dashboardTitle }}
        </h2>
        <div v-if="editMode" class="flex items-center space-x-2">
          <span class="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full">
            Edit Mode
          </span>
          <Button
            variant="ghost"
            size="sm"
            @click="previewDashboard"
          >
            Preview
          </Button>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        <!-- Save/Reset Actions -->
        <div v-if="editMode" class="flex items-center space-x-2">
          <Button
            variant="ghost"
            size="sm"
            @click="resetDashboard"
            :disabled="!hasChanges"
          >
            Reset
          </Button>
          <Button
            variant="primary"
            size="sm"
            @click="saveDashboard"
            :loading="saving"
            :disabled="!hasChanges"
          >
            Save Dashboard
          </Button>
        </div>
        
        <!-- Edit Toggle -->
        <Button
          v-if="!editMode"
          variant="ghost"
          size="sm"
          :leftIcon="PencilIcon"
          @click="enableEditMode"
        >
          Edit
        </Button>

        <!-- Settings -->
        <Button
          variant="ghost"
          size="sm"
          :leftIcon="CogIcon"
          @click="openSettings"
        >
          Settings
        </Button>

        <!-- Export -->
        <Button
          variant="ghost"
          size="sm"
          :leftIcon="ArrowDownTrayIcon"
          @click="exportDashboard"
        >
          Export
        </Button>
      </div>
    </div>

    <div class="flex h-[calc(100vh-73px)]">
      <!-- Widget Panel (Edit Mode Only) -->
      <div
        v-if="editMode"
        class="w-80 bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 overflow-y-auto"
      >
        <WidgetPanel
          :available-widgets="availableWidgets"
          :widget-categories="widgetCategories"
          @add-widget="addWidget"
        />
      </div>

      <!-- Main Dashboard Area -->
      <div class="flex-1 overflow-auto">
        <DashboardGrid
          ref="dashboardGrid"
          :layout="dashboardLayout"
          :widgets="dashboardWidgets"
          :edit-mode="editMode"
          :grid-size="gridSize"
          :gap="gridGap"
          :responsive="responsive"
          @update-layout="updateLayout"
          @remove-widget="removeWidget"
          @configure-widget="configureWidget"
          @duplicate-widget="duplicateWidget"
        />
      </div>
    </div>

    <!-- Widget Configuration Modal -->
    <Modal
      v-model:is-open="configModalOpen"
      :title="`Configure ${currentWidget?.title || 'Widget'}`"
      size="lg"
    >
      <WidgetConfigurator
        v-if="currentWidget"
        :widget="currentWidget"
        :configuration="currentWidget.config"
        @update-config="updateWidgetConfig"
        @close="configModalOpen = false"
      />
    </Modal>

    <!-- Dashboard Settings Modal -->
    <Modal
      v-model:is-open="settingsModalOpen"
      title="Dashboard Settings"
      size="md"
    >
      <DashboardSettings
        :settings="dashboardSettings"
        @update-settings="updateDashboardSettings"
        @close="settingsModalOpen = false"
      />
    </Modal>

    <!-- Export Modal -->
    <Modal
      v-model:is-open="exportModalOpen"
      title="Export Dashboard"
      size="sm"
    >
      <DashboardExporter
        :dashboard="dashboardConfig"
        @export="handleExport"
        @close="exportModalOpen = false"
      />
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import Button from '@/components/ui/Button.vue'
import Modal from '@/components/ui/Modal.vue'
import DashboardGrid from './DashboardGrid.vue'
import WidgetPanel from './WidgetPanel.vue'
import WidgetConfigurator from './WidgetConfigurator.vue'
import DashboardSettings from './DashboardSettings.vue'
import DashboardExporter from './DashboardExporter.vue'
import { $notify } from '@/composables/useNotifications'
import {
  PencilIcon,
  CogIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  initialLayout: {
    type: Array,
    default: () => []
  },
  initialWidgets: {
    type: Object,
    default: () => ({})
  },
  dashboardId: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: 'Dashboard'
  },
  editable: {
    type: Boolean,
    default: true
  },
  autoSave: {
    type: Boolean,
    default: true
  },
  autoSaveInterval: {
    type: Number,
    default: 30000 // 30 seconds
  }
})

const emit = defineEmits(['save', 'reset', 'export', 'change'])

// State
const editMode = ref(false)
const saving = ref(false)
const configModalOpen = ref(false)
const settingsModalOpen = ref(false)
const exportModalOpen = ref(false)
const currentWidget = ref(null)
const dashboardGrid = ref(null)

// Dashboard data
const dashboardLayout = ref([...props.initialLayout])
const dashboardWidgets = ref({ ...props.initialWidgets })
const originalLayout = ref([...props.initialLayout])
const originalWidgets = ref({ ...props.initialWidgets })

// Dashboard settings
const dashboardSettings = ref({
  title: props.title,
  description: '',
  theme: 'default',
  backgroundColor: 'white',
  gridSize: 12,
  gap: 16,
  responsive: true,
  autoRefresh: false,
  refreshInterval: 60000,
  showHeader: true,
  showGrid: false
})

// Widget definitions
const availableWidgets = ref([
  {
    id: 'stat-card',
    title: 'Stat Card',
    category: 'metrics',
    icon: 'ChartBarIcon',
    description: 'Display key metrics and statistics',
    defaultSize: { w: 3, h: 2 },
    configurable: true,
    defaultConfig: {
      title: 'Metric',
      value: 0,
      trend: 0,
      format: 'number'
    }
  },
  {
    id: 'line-chart',
    title: 'Line Chart',
    category: 'charts',
    icon: 'ChartLineIcon',
    description: 'Time series data visualization',
    defaultSize: { w: 6, h: 4 },
    configurable: true,
    defaultConfig: {
      title: 'Chart',
      dataSource: null,
      xAxis: '',
      yAxis: ''
    }
  },
  {
    id: 'table',
    title: 'Data Table',
    category: 'data',
    icon: 'TableCellsIcon',
    description: 'Display tabular data',
    defaultSize: { w: 8, h: 4 },
    configurable: true,
    defaultConfig: {
      title: 'Data Table',
      dataSource: null,
      columns: []
    }
  },
  {
    id: 'progress-ring',
    title: 'Progress Ring',
    category: 'metrics',
    icon: 'ArrowPathIcon',
    description: 'Circular progress indicator',
    defaultSize: { w: 2, h: 2 },
    configurable: true,
    defaultConfig: {
      title: 'Progress',
      value: 50,
      max: 100,
      color: 'blue'
    }
  },
  {
    id: 'activity-feed',
    title: 'Activity Feed',
    category: 'content',
    icon: 'RssIcon',
    description: 'Recent activities and updates',
    defaultSize: { w: 4, h: 6 },
    configurable: true,
    defaultConfig: {
      title: 'Recent Activity',
      maxItems: 10,
      showTimestamps: true
    }
  }
])

const widgetCategories = ref([
  { id: 'metrics', name: 'Metrics', icon: 'ChartBarIcon' },
  { id: 'charts', name: 'Charts', icon: 'PresentationChartLineIcon' },
  { id: 'data', name: 'Data', icon: 'TableCellsIcon' },
  { id: 'content', name: 'Content', icon: 'DocumentTextIcon' }
])

// Computed properties
const dashboardTitle = computed(() => dashboardSettings.value.title)
const gridSize = computed(() => dashboardSettings.value.gridSize)
const gridGap = computed(() => dashboardSettings.value.gap)
const responsive = computed(() => dashboardSettings.value.responsive)

const hasChanges = computed(() => {
  return JSON.stringify(dashboardLayout.value) !== JSON.stringify(originalLayout.value) ||
         JSON.stringify(dashboardWidgets.value) !== JSON.stringify(originalWidgets.value)
})

const dashboardConfig = computed(() => ({
  id: props.dashboardId,
  title: dashboardSettings.value.title,
  layout: dashboardLayout.value,
  widgets: dashboardWidgets.value,
  settings: dashboardSettings.value,
  version: '1.0.0',
  createdAt: new Date().toISOString()
}))

// Methods
const enableEditMode = () => {
  if (!props.editable) {
    $notify.warning('This dashboard is not editable')
    return
  }
  editMode.value = true
}

const previewDashboard = () => {
  editMode.value = false
}

const addWidget = (widgetType) => {
  const widget = availableWidgets.value.find(w => w.id === widgetType)
  if (!widget) return

  const widgetId = `${widgetType}_${Date.now()}`
  const layoutItem = {
    i: widgetId,
    x: 0,
    y: 0,
    w: widget.defaultSize.w,
    h: widget.defaultSize.h,
    minW: 1,
    minH: 1,
    maxW: 12,
    maxH: 12
  }

  dashboardLayout.value.push(layoutItem)
  dashboardWidgets.value[widgetId] = {
    id: widgetId,
    type: widgetType,
    title: widget.title,
    config: { ...widget.defaultConfig }
  }

  $notify.success(`Added ${widget.title} to dashboard`)
}

const removeWidget = (widgetId) => {
  const index = dashboardLayout.value.findIndex(item => item.i === widgetId)
  if (index > -1) {
    dashboardLayout.value.splice(index, 1)
    delete dashboardWidgets.value[widgetId]
    $notify.success('Widget removed')
  }
}

const duplicateWidget = (widgetId) => {
  const originalWidget = dashboardWidgets.value[widgetId]
  const originalLayoutItem = dashboardLayout.value.find(item => item.i === widgetId)
  
  if (!originalWidget || !originalLayoutItem) return

  const newWidgetId = `${originalWidget.type}_${Date.now()}`
  const newLayoutItem = {
    ...originalLayoutItem,
    i: newWidgetId,
    x: (originalLayoutItem.x + originalLayoutItem.w) % gridSize.value,
    y: originalLayoutItem.y
  }

  dashboardLayout.value.push(newLayoutItem)
  dashboardWidgets.value[newWidgetId] = {
    ...originalWidget,
    id: newWidgetId,
    title: `${originalWidget.title} (Copy)`
  }

  $notify.success('Widget duplicated')
}

const configureWidget = (widgetId) => {
  currentWidget.value = dashboardWidgets.value[widgetId]
  configModalOpen.value = true
}

const updateWidgetConfig = (config) => {
  if (currentWidget.value) {
    currentWidget.value.config = { ...config }
    emit('change', { type: 'widget-config', widgetId: currentWidget.value.id, config })
  }
}

const updateLayout = (newLayout) => {
  dashboardLayout.value = newLayout
  emit('change', { type: 'layout', layout: newLayout })
}

const updateDashboardSettings = (settings) => {
  dashboardSettings.value = { ...dashboardSettings.value, ...settings }
  emit('change', { type: 'settings', settings: dashboardSettings.value })
}

const saveDashboard = async () => {
  saving.value = true
  
  try {
    const config = dashboardConfig.value
    emit('save', config)
    
    // Update original state
    originalLayout.value = [...dashboardLayout.value]
    originalWidgets.value = { ...dashboardWidgets.value }
    
    $notify.success('Dashboard saved successfully')
    
    // Exit edit mode after save
    setTimeout(() => {
      editMode.value = false
    }, 500)
    
  } catch (error) {
    $notify.error('Failed to save dashboard')
    console.error('Save error:', error)
  } finally {
    saving.value = false
  }
}

const resetDashboard = async () => {
  const result = await $notify.confirmWarning(
    'This will discard all unsaved changes. Are you sure?'
  )
  
  if (result.confirmed) {
    dashboardLayout.value = [...originalLayout.value]
    dashboardWidgets.value = { ...originalWidgets.value }
    emit('reset')
    $notify.info('Dashboard reset to last saved state')
  }
}

const openSettings = () => {
  settingsModalOpen.value = true
}

const exportDashboard = () => {
  exportModalOpen.value = true
}

const handleExport = (format) => {
  const config = dashboardConfig.value
  emit('export', { format, config })
  exportModalOpen.value = false
}

// Auto-save functionality
let autoSaveTimer = null
const startAutoSave = () => {
  if (!props.autoSave) return
  
  autoSaveTimer = setInterval(() => {
    if (hasChanges.value && editMode.value) {
      saveDashboard()
    }
  }, props.autoSaveInterval)
}

const stopAutoSave = () => {
  if (autoSaveTimer) {
    clearInterval(autoSaveTimer)
    autoSaveTimer = null
  }
}

// Keyboard shortcuts
const handleKeyboard = (event) => {
  if (!editMode.value) return
  
  if (event.ctrlKey || event.metaKey) {
    switch (event.key) {
      case 's':
        event.preventDefault()
        saveDashboard()
        break
      case 'z':
        event.preventDefault()
        // Undo functionality would go here
        break
    }
  }
  
  if (event.key === 'Escape') {
    editMode.value = false
  }
}

// Lifecycle
onMounted(() => {
  startAutoSave()
  document.addEventListener('keydown', handleKeyboard)
})

onUnmounted(() => {
  stopAutoSave()
  document.removeEventListener('keydown', handleKeyboard)
})

// Watch for changes
watch(hasChanges, (hasChanges) => {
  if (hasChanges) {
    // Could show unsaved changes indicator
  }
})
</script>

<style scoped>
.dashboard-builder {
  @apply h-screen bg-gray-50 dark:bg-gray-900;
}
</style>