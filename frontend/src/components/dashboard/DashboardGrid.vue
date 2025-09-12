<template>
  <div 
    ref="gridContainer"
    :class="[
      'dashboard-grid relative',
      editMode && 'edit-mode',
      showGrid && 'show-grid'
    ]"
    :style="gridStyles"
  >
    <!-- Grid Background (Edit Mode) -->
    <div
      v-if="editMode && showGrid"
      class="absolute inset-0 pointer-events-none opacity-10"
      :style="gridBackgroundStyle"
    ></div>

    <!-- Drop Zone Indicator -->
    <div
      v-if="editMode && isDragging"
      class="absolute inset-0 border-2 border-dashed border-blue-400 bg-blue-50/20 dark:bg-blue-900/20 rounded-lg flex items-center justify-center pointer-events-none"
    >
      <div class="text-blue-600 dark:text-blue-400 text-lg font-medium">
        Drop widget here
      </div>
    </div>

    <!-- Grid Items (Widgets) -->
    <div
      v-for="item in layoutItems"
      :key="item.i"
      :class="[
        'grid-item absolute transition-all duration-200 ease-out',
        editMode && 'editable',
        item.isDragging && 'dragging',
        item.isResizing && 'resizing'
      ]"
      :style="getItemStyle(item)"
      @mousedown="startDrag(item, $event)"
      @touchstart="startDrag(item, $event)"
    >
      <!-- Widget Content -->
      <div class="widget-content h-full w-full relative">
        <!-- Edit Overlay -->
        <div
          v-if="editMode"
          class="absolute inset-0 z-10 opacity-0 hover:opacity-100 transition-opacity duration-200"
          :class="item.isDragging && 'opacity-100'"
        >
          <div class="absolute inset-0 bg-blue-500/10 border-2 border-blue-500 rounded-lg"></div>
          
          <!-- Widget Controls -->
          <div class="absolute top-2 right-2 flex space-x-1">
            <button
              @click.stop="configureWidget(item.i)"
              class="p-1 bg-white dark:bg-gray-800 rounded shadow-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              title="Configure"
            >
              <CogIcon class="w-4 h-4 text-gray-600 dark:text-gray-400" />
            </button>
            <button
              @click.stop="duplicateWidget(item.i)"
              class="p-1 bg-white dark:bg-gray-800 rounded shadow-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              title="Duplicate"
            >
              <DocumentDuplicateIcon class="w-4 h-4 text-gray-600 dark:text-gray-400" />
            </button>
            <button
              @click.stop="removeWidget(item.i)"
              class="p-1 bg-white dark:bg-gray-800 rounded shadow-md hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
              title="Remove"
            >
              <TrashIcon class="w-4 h-4 text-red-500" />
            </button>
          </div>

          <!-- Resize Handle -->
          <div
            class="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize"
            @mousedown.stop="startResize(item, $event)"
            @touchstart.stop="startResize(item, $event)"
          >
            <div class="absolute bottom-1 right-1 w-2 h-2 bg-blue-500 rounded-sm"></div>
          </div>

          <!-- Drag Handle -->
          <div
            class="absolute top-0 left-0 right-0 h-8 cursor-move flex items-center justify-center"
            title="Drag to move"
          >
            <div class="w-6 h-1 bg-gray-400 dark:bg-gray-500 rounded"></div>
          </div>
        </div>

        <!-- Actual Widget Component -->
        <DashboardWidget
          :widget="widgets[item.i]"
          :edit-mode="editMode"
          :width="item.w"
          :height="item.h"
        />
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-if="!layoutItems.length"
      class="absolute inset-0 flex items-center justify-center"
    >
      <EmptyState
        icon="PlusCircleIcon"
        title="No Widgets"
        :description="editMode ? 'Add widgets from the panel on the left' : 'This dashboard is empty'"
        size="lg"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import DashboardWidget from './DashboardWidget.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import {
  CogIcon,
  DocumentDuplicateIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  layout: {
    type: Array,
    required: true
  },
  widgets: {
    type: Object,
    required: true
  },
  editMode: {
    type: Boolean,
    default: false
  },
  gridSize: {
    type: Number,
    default: 12
  },
  gap: {
    type: Number,
    default: 16
  },
  responsive: {
    type: Boolean,
    default: true
  },
  showGrid: {
    type: Boolean,
    default: false
  },
  minItemWidth: {
    type: Number,
    default: 200
  },
  minItemHeight: {
    type: Number,
    default: 150
  }
})

const emit = defineEmits([
  'update-layout',
  'remove-widget',
  'configure-widget',
  'duplicate-widget'
])

// Responsive functionality
const { isMobile, isTablet, gridCols, getResponsiveValue } = useResponsive()

// Refs
const gridContainer = ref(null)

// State
const isDragging = ref(false)
const dragItem = ref(null)
const dragStartPos = ref({ x: 0, y: 0 })
const dragStartItemPos = ref({ x: 0, y: 0 })
const resizeItem = ref(null)
const resizeStartSize = ref({ w: 0, h: 0 })
const containerSize = ref({ width: 0, height: 0 })

// Layout state with dragging/resizing flags
const layoutItems = ref([])

// Computed properties
const gridStyles = computed(() => {
  return {
    padding: `${props.gap}px`,
    minHeight: '100%'
  }
})

const gridBackgroundStyle = computed(() => {
  const cellWidth = (containerSize.value.width - props.gap * 2) / props.gridSize
  const cellHeight = 60 // Base height for grid cells
  
  return {
    backgroundImage: `
      linear-gradient(to right, #e5e7eb 1px, transparent 1px),
      linear-gradient(to bottom, #e5e7eb 1px, transparent 1px)
    `,
    backgroundSize: `${cellWidth}px ${cellHeight}px`
  }
})

// Methods
const updateContainerSize = () => {
  if (gridContainer.value) {
    const rect = gridContainer.value.getBoundingClientRect()
    containerSize.value = {
      width: rect.width,
      height: rect.height
    }
  }
}

const getItemStyle = (item) => {
  const containerWidth = containerSize.value.width - props.gap * 2
  const cellWidth = containerWidth / props.gridSize
  const cellHeight = 60 // Base height for grid cells
  
  const x = item.x * cellWidth + (item.x * props.gap)
  const y = item.y * cellHeight + (item.y * props.gap)
  const width = item.w * cellWidth + ((item.w - 1) * props.gap)
  const height = item.h * cellHeight + ((item.h - 1) * props.gap)

  return {
    transform: `translate(${x}px, ${y}px)`,
    width: `${width}px`,
    height: `${height}px`,
    zIndex: item.isDragging || item.isResizing ? 1000 : 1
  }
}

const startDrag = (item, event) => {
  if (!props.editMode) return

  event.preventDefault()
  
  const clientX = event.clientX || event.touches?.[0]?.clientX
  const clientY = event.clientY || event.touches?.[0]?.clientY

  if (!clientX || !clientY) return

  dragItem.value = item
  isDragging.value = true
  dragStartPos.value = { x: clientX, y: clientY }
  dragStartItemPos.value = { x: item.x, y: item.y }

  // Set dragging state
  const itemIndex = layoutItems.value.findIndex(i => i.i === item.i)
  if (itemIndex > -1) {
    layoutItems.value[itemIndex].isDragging = true
  }

  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', endDrag)
  document.addEventListener('touchmove', handleDrag)
  document.addEventListener('touchend', endDrag)
}

const handleDrag = (event) => {
  if (!dragItem.value) return

  const clientX = event.clientX || event.touches?.[0]?.clientX
  const clientY = event.clientY || event.touches?.[0]?.clientY

  if (!clientX || !clientY) return

  const deltaX = clientX - dragStartPos.value.x
  const deltaY = clientY - dragStartPos.value.y

  const containerWidth = containerSize.value.width - props.gap * 2
  const cellWidth = containerWidth / props.gridSize
  const cellHeight = 60

  const newX = Math.max(0, Math.min(
    props.gridSize - dragItem.value.w,
    Math.round(dragStartItemPos.value.x + deltaX / cellWidth)
  ))
  const newY = Math.max(0, Math.round(dragStartItemPos.value.y + deltaY / cellHeight))

  // Update item position
  const itemIndex = layoutItems.value.findIndex(i => i.i === dragItem.value.i)
  if (itemIndex > -1) {
    layoutItems.value[itemIndex].x = newX
    layoutItems.value[itemIndex].y = newY
  }
}

const endDrag = () => {
  if (dragItem.value) {
    const itemIndex = layoutItems.value.findIndex(i => i.i === dragItem.value.i)
    if (itemIndex > -1) {
      layoutItems.value[itemIndex].isDragging = false
    }
  }

  dragItem.value = null
  isDragging.value = false
  
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', endDrag)
  document.removeEventListener('touchmove', handleDrag)
  document.removeEventListener('touchend', endDrag)

  // Emit layout update
  emit('update-layout', layoutItems.value.map(({ isDragging, isResizing, ...item }) => item))
}

const startResize = (item, event) => {
  if (!props.editMode) return

  event.preventDefault()
  event.stopPropagation()

  const clientX = event.clientX || event.touches?.[0]?.clientX
  const clientY = event.clientY || event.touches?.[0]?.clientY

  if (!clientX || !clientY) return

  resizeItem.value = item
  dragStartPos.value = { x: clientX, y: clientY }
  resizeStartSize.value = { w: item.w, h: item.h }

  // Set resizing state
  const itemIndex = layoutItems.value.findIndex(i => i.i === item.i)
  if (itemIndex > -1) {
    layoutItems.value[itemIndex].isResizing = true
  }

  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', endResize)
  document.addEventListener('touchmove', handleResize)
  document.addEventListener('touchend', endResize)
}

const handleResize = (event) => {
  if (!resizeItem.value) return

  const clientX = event.clientX || event.touches?.[0]?.clientX
  const clientY = event.clientY || event.touches?.[0]?.clientY

  if (!clientX || !clientY) return

  const deltaX = clientX - dragStartPos.value.x
  const deltaY = clientY - dragStartPos.value.y

  const containerWidth = containerSize.value.width - props.gap * 2
  const cellWidth = containerWidth / props.gridSize
  const cellHeight = 60

  const newW = Math.max(
    resizeItem.value.minW || 1,
    Math.min(
      resizeItem.value.maxW || props.gridSize,
      Math.max(1, resizeStartSize.value.w + Math.round(deltaX / cellWidth))
    )
  )
  const newH = Math.max(
    resizeItem.value.minH || 1,
    Math.min(
      resizeItem.value.maxH || 20,
      Math.max(1, resizeStartSize.value.h + Math.round(deltaY / cellHeight))
    )
  )

  // Update item size
  const itemIndex = layoutItems.value.findIndex(i => i.i === resizeItem.value.i)
  if (itemIndex > -1) {
    layoutItems.value[itemIndex].w = newW
    layoutItems.value[itemIndex].h = newH
  }
}

const endResize = () => {
  if (resizeItem.value) {
    const itemIndex = layoutItems.value.findIndex(i => i.i === resizeItem.value.i)
    if (itemIndex > -1) {
      layoutItems.value[itemIndex].isResizing = false
    }
  }

  resizeItem.value = null
  
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', endResize)
  document.removeEventListener('touchmove', handleResize)
  document.removeEventListener('touchend', endResize)

  // Emit layout update
  emit('update-layout', layoutItems.value.map(({ isDragging, isResizing, ...item }) => item))
}

const removeWidget = (widgetId) => {
  emit('remove-widget', widgetId)
}

const configureWidget = (widgetId) => {
  emit('configure-widget', widgetId)
}

const duplicateWidget = (widgetId) => {
  emit('duplicate-widget', widgetId)
}

// Initialize layout items with additional state
const initializeLayoutItems = () => {
  layoutItems.value = props.layout.map(item => ({
    ...item,
    isDragging: false,
    isResizing: false
  }))
}

// Handle window resize
const handleResize = () => {
  updateContainerSize()
}

// Watch for layout changes
watch(() => props.layout, () => {
  initializeLayoutItems()
}, { deep: true })

// Lifecycle
onMounted(() => {
  initializeLayoutItems()
  updateContainerSize()
  window.addEventListener('resize', handleResize)
  
  // Observer for container size changes
  if (window.ResizeObserver) {
    const resizeObserver = new ResizeObserver(updateContainerSize)
    resizeObserver.observe(gridContainer.value)
    
    onUnmounted(() => {
      resizeObserver.disconnect()
    })
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard-grid {
  @apply min-h-full bg-white dark:bg-gray-800;
}

.grid-item {
  @apply rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm;
}

.grid-item.editable:hover {
  @apply border-blue-300 dark:border-blue-600 shadow-md;
}

.grid-item.dragging {
  @apply shadow-xl ring-2 ring-blue-500 ring-opacity-50;
}

.grid-item.resizing {
  @apply shadow-xl ring-2 ring-green-500 ring-opacity-50;
}

.widget-content {
  @apply overflow-hidden rounded-lg;
}

.edit-mode {
  @apply select-none;
}

.show-grid {
  background-image: 
    linear-gradient(to right, #e5e7eb 1px, transparent 1px),
    linear-gradient(to bottom, #e5e7eb 1px, transparent 1px);
}
</style>