<template>
  <div class="widget-panel h-full flex flex-col">
    <!-- Panel Header -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        Add Widgets
      </h3>
      <div class="relative">
        <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search widgets..."
          class="w-full pl-10 pr-4 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
    </div>

    <!-- Category Filter -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex flex-wrap gap-2">
        <button
          v-for="category in widgetCategories"
          :key="category.id"
          @click="selectedCategory = selectedCategory === category.id ? null : category.id"
          :class="[
            'px-3 py-1 text-xs font-medium rounded-full transition-colors',
            selectedCategory === category.id
              ? 'bg-blue-500 text-white'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
          ]"
        >
          {{ category.name }}
        </button>
        <button
          v-if="selectedCategory"
          @click="selectedCategory = null"
          class="px-3 py-1 text-xs font-medium rounded-full bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
        >
          Clear
        </button>
      </div>
    </div>

    <!-- Widget List -->
    <div class="flex-1 overflow-y-auto p-4">
      <div class="space-y-3">
        <div
          v-for="widget in filteredWidgets"
          :key="widget.id"
          class="widget-item p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-blue-300 dark:hover:border-blue-600 hover:shadow-md transition-all duration-200 cursor-pointer group"
          @click="addWidget(widget.id)"
          @dragstart="handleDragStart(widget, $event)"
          @dragend="handleDragEnd"
          draggable="true"
        >
          <div class="flex items-start space-x-3">
            <!-- Widget Icon -->
            <div class="flex-shrink-0 w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center group-hover:bg-blue-100 dark:group-hover:bg-blue-900/20 transition-colors">
              <component 
                :is="getWidgetIcon(widget.icon)" 
                class="w-5 h-5 text-gray-600 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-400"
              />
            </div>

            <!-- Widget Info -->
            <div class="flex-1 min-w-0">
              <h4 class="text-sm font-medium text-gray-900 dark:text-white group-hover:text-blue-900 dark:group-hover:text-blue-100">
                {{ widget.title }}
              </h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
                {{ widget.description }}
              </p>
              
              <!-- Widget Size Info -->
              <div class="flex items-center mt-2 text-xs text-gray-400 dark:text-gray-500">
                <div class="flex items-center mr-3">
                  <div class="w-3 h-3 border border-current rounded-sm mr-1"></div>
                  {{ widget.defaultSize.w }}×{{ widget.defaultSize.h }}
                </div>
                <span v-if="widget.configurable" class="flex items-center">
                  <CogIcon class="w-3 h-3 mr-1" />
                  Configurable
                </span>
              </div>
            </div>

            <!-- Add Button -->
            <div class="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
              <PlusIcon class="w-5 h-5 text-blue-500" />
            </div>
          </div>

          <!-- Quick Preview (Expandable) -->
          <div 
            v-if="widget.preview && expandedWidget === widget.id"
            class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700"
          >
            <div class="aspect-video bg-gray-50 dark:bg-gray-800 rounded-md flex items-center justify-center">
              <img 
                :src="widget.preview" 
                :alt="`${widget.title} preview`"
                class="max-w-full max-h-full rounded"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!filteredWidgets.length" class="text-center py-8">
        <component 
          :is="searchQuery ? MagnifyingGlassIcon : PuzzlePieceIcon" 
          class="w-12 h-12 text-gray-400 mx-auto mb-4"
        />
        <h3 class="text-sm font-medium text-gray-900 dark:text-white mb-1">
          {{ searchQuery ? 'No widgets found' : 'No widgets available' }}
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          {{ searchQuery ? 'Try adjusting your search terms' : 'Check back later for new widgets' }}
        </p>
      </div>
    </div>

    <!-- Panel Footer -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
      <div class="text-xs text-gray-500 dark:text-gray-400 space-y-1">
        <p>• Click to add widget</p>
        <p>• Drag to position on dashboard</p>
        <p>• Hover over widgets for quick actions</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  MagnifyingGlassIcon,
  PlusIcon,
  CogIcon,
  PuzzlePieceIcon,
  ChartBarIcon,
  ChartLineIcon,
  TableCellsIcon,
  ArrowPathIcon,
  RssIcon,
  PresentationChartLineIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  availableWidgets: {
    type: Array,
    required: true
  },
  widgetCategories: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['add-widget', 'drag-widget'])

// State
const searchQuery = ref('')
const selectedCategory = ref(null)
const expandedWidget = ref(null)
const draggedWidget = ref(null)

// Icon mapping
const iconMap = {
  ChartBarIcon,
  ChartLineIcon, 
  TableCellsIcon,
  ArrowPathIcon,
  RssIcon,
  PresentationChartLineIcon,
  DocumentTextIcon,
  PuzzlePieceIcon
}

// Computed
const filteredWidgets = computed(() => {
  let widgets = props.availableWidgets

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    widgets = widgets.filter(widget => 
      widget.title.toLowerCase().includes(query) ||
      widget.description.toLowerCase().includes(query) ||
      widget.category.toLowerCase().includes(query)
    )
  }

  // Filter by category
  if (selectedCategory.value) {
    widgets = widgets.filter(widget => widget.category === selectedCategory.value)
  }

  return widgets
})

// Methods
const getWidgetIcon = (iconName) => {
  return iconMap[iconName] || PuzzlePieceIcon
}

const addWidget = (widgetId) => {
  emit('add-widget', widgetId)
}

const toggleExpanded = (widgetId) => {
  expandedWidget.value = expandedWidget.value === widgetId ? null : widgetId
}

const handleDragStart = (widget, event) => {
  draggedWidget.value = widget
  
  // Set drag data
  event.dataTransfer.effectAllowed = 'copy'
  event.dataTransfer.setData('application/json', JSON.stringify(widget))
  
  // Create custom drag image
  const dragImage = createDragImage(widget)
  event.dataTransfer.setDragImage(dragImage, 50, 30)
  
  emit('drag-widget', { widget, action: 'start' })
}

const handleDragEnd = () => {
  draggedWidget.value = null
  emit('drag-widget', { action: 'end' })
}

const createDragImage = (widget) => {
  // Create a custom drag image
  const dragImage = document.createElement('div')
  dragImage.style.cssText = `
    position: absolute;
    top: -1000px;
    left: -1000px;
    width: 200px;
    height: 60px;
    background: white;
    border: 2px solid #3B82F6;
    border-radius: 8px;
    padding: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    font-family: system-ui, -apple-system, sans-serif;
    display: flex;
    align-items: center;
    gap: 12px;
  `
  
  dragImage.innerHTML = `
    <div style="width: 24px; height: 24px; background: #EFF6FF; border-radius: 4px; display: flex; align-items: center; justify-content: center;">
      <svg width="16" height="16" fill="#3B82F6" viewBox="0 0 24 24">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
      </svg>
    </div>
    <div>
      <div style="font-weight: 500; font-size: 14px; color: #111827;">${widget.title}</div>
      <div style="font-size: 12px; color: #6B7280;">${widget.defaultSize.w}×${widget.defaultSize.h}</div>
    </div>
  `
  
  document.body.appendChild(dragImage)
  
  // Clean up after a short delay
  setTimeout(() => {
    if (dragImage.parentNode) {
      dragImage.parentNode.removeChild(dragImage)
    }
  }, 100)
  
  return dragImage
}
</script>

<style scoped>
.widget-panel {
  @apply bg-gray-50 dark:bg-gray-900;
}

.widget-item {
  @apply select-none;
}

.widget-item:active {
  @apply scale-95;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Drag animation */
.widget-item[draggable="true"] {
  @apply cursor-grab;
}

.widget-item[draggable="true"]:active {
  @apply cursor-grabbing;
}
</style>