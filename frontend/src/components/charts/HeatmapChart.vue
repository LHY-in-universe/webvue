<template>
  <div class="heatmap-chart" :style="containerStyles">
    <!-- Chart Header -->
    <div v-if="title" class="mb-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        {{ title }}
      </h3>
    </div>

    <!-- Heatmap Container -->
    <div class="relative">
      <!-- Y-axis labels -->
      <div 
        v-if="showYLabels"
        class="absolute left-0 top-0 flex flex-col justify-between h-full pr-2"
        :style="{ width: `${yLabelWidth}px` }"
      >
        <div
          v-for="(label, index) in yLabels"
          :key="index"
          class="flex items-center justify-end h-0 text-sm text-gray-600 dark:text-gray-400"
          :style="{ transform: `translateY(${cellHeight / 2}px)` }"
        >
          {{ label }}
        </div>
      </div>

      <!-- Main heatmap -->
      <div 
        class="heatmap-grid"
        :style="gridStyles"
        :class="{ 'ml-20': showYLabels }"
      >
        <!-- Grid cells -->
        <div
          v-for="(cell, index) in gridData"
          :key="index"
          class="heatmap-cell relative group cursor-pointer transition-all duration-200 hover:scale-105 hover:z-10"
          :style="getCellStyles(cell)"
          @mouseenter="handleCellHover(cell, $event)"
          @mouseleave="hideTooltip"
          @click="handleCellClick(cell)"
        >
          <!-- Cell value display -->
          <div 
            v-if="showValues && cell.value !== null"
            class="absolute inset-0 flex items-center justify-center text-xs font-medium"
            :class="getValueTextColor(cell.value)"
          >
            {{ formatCellValue(cell.value) }}
          </div>
          
          <!-- Loading state -->
          <div 
            v-if="cell.loading"
            class="absolute inset-0 flex items-center justify-center bg-white/80 dark:bg-gray-900/80"
          >
            <div class="w-3 h-3 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        </div>
      </div>

      <!-- X-axis labels -->
      <div 
        v-if="showXLabels"
        class="flex mt-2"
        :class="{ 'ml-20': showYLabels }"
      >
        <div
          v-for="(label, index) in xLabels"
          :key="index"
          class="flex-1 text-center text-sm text-gray-600 dark:text-gray-400"
        >
          {{ label }}
        </div>
      </div>

      <!-- Color Legend -->
      <div v-if="showLegend" class="mt-6 flex items-center justify-center">
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-600 dark:text-gray-400">{{ minValue.toFixed(1) }}</span>
          <div class="flex">
            <div
              v-for="(color, index) in legendColors"
              :key="index"
              class="w-6 h-4"
              :style="{ backgroundColor: color }"
            ></div>
          </div>
          <span class="text-sm text-gray-600 dark:text-gray-400">{{ maxValue.toFixed(1) }}</span>
        </div>
      </div>
    </div>

    <!-- Tooltip -->
    <div
      v-if="tooltip.show"
      class="fixed z-50 bg-gray-900 text-white text-sm rounded-lg shadow-lg px-3 py-2 pointer-events-none"
      :style="tooltipStyles"
    >
      <div class="font-medium">{{ tooltip.title }}</div>
      <div class="text-gray-300 mt-1">
        Value: {{ formatCellValue(tooltip.value) }}
      </div>
      <div v-if="tooltip.description" class="text-gray-400 text-xs mt-1">
        {{ tooltip.description }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
    // Format: [{ x: 0, y: 0, value: 10, label: 'Optional' }, ...]
  },
  xLabels: {
    type: Array,
    default: () => []
  },
  yLabels: {
    type: Array,
    default: () => []
  },
  title: String,
  
  // Dimensions
  width: {
    type: Number,
    default: 600
  },
  height: {
    type: Number,
    default: 400
  },
  cellSize: {
    type: Number,
    default: 30
  },
  gap: {
    type: Number,
    default: 1
  },
  
  // Display options
  showValues: {
    type: Boolean,
    default: false
  },
  showXLabels: {
    type: Boolean,
    default: true
  },
  showYLabels: {
    type: Boolean,
    default: true
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  
  // Color scheme
  colorScheme: {
    type: String,
    default: 'blues',
    validator: value => ['blues', 'greens', 'reds', 'grays', 'rainbow'].includes(value)
  },
  
  // Value formatting
  valueFormat: {
    type: String,
    default: 'number',
    validator: value => ['number', 'percentage', 'currency'].includes(value)
  },
  precision: {
    type: Number,
    default: 1
  }
})

const emit = defineEmits(['cell-click', 'cell-hover'])

// State
const tooltip = ref({
  show: false,
  x: 0,
  y: 0,
  title: '',
  value: null,
  description: ''
})

// Color schemes
const colorSchemes = {
  blues: ['#f0f9ff', '#e0f2fe', '#bae6fd', '#7dd3fc', '#38bdf8', '#0ea5e9', '#0284c7', '#0369a1'],
  greens: ['#f0fdf4', '#dcfce7', '#bbf7d0', '#86efac', '#4ade80', '#22c55e', '#16a34a', '#15803d'],
  reds: ['#fef2f2', '#fecaca', '#fca5a5', '#f87171', '#ef4444', '#dc2626', '#b91c1c', '#991b1b'],
  grays: ['#fafafa', '#f4f4f5', '#e4e4e7', '#d4d4d8', '#a1a1aa', '#71717a', '#52525b', '#3f3f46'],
  rainbow: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316']
}

// Computed properties
const containerStyles = computed(() => ({
  width: `${props.width}px`,
  maxWidth: '100%'
}))

const yLabelWidth = computed(() => 80)

const cellWidth = computed(() => props.cellSize)
const cellHeight = computed(() => props.cellSize)

const gridColumns = computed(() => {
  return Math.max(1, ...props.data.map(item => item.x + 1))
})

const gridRows = computed(() => {
  return Math.max(1, ...props.data.map(item => item.y + 1))
})

const gridStyles = computed(() => ({
  display: 'grid',
  gridTemplateColumns: `repeat(${gridColumns.value}, ${cellWidth.value}px)`,
  gridTemplateRows: `repeat(${gridRows.value}, ${cellHeight.value}px)`,
  gap: `${props.gap}px`,
  width: 'fit-content'
}))

const minValue = computed(() => {
  const values = props.data.map(item => item.value).filter(val => val !== null)
  return values.length ? Math.min(...values) : 0
})

const maxValue = computed(() => {
  const values = props.data.map(item => item.value).filter(val => val !== null)
  return values.length ? Math.max(...values) : 100
})

const valueRange = computed(() => maxValue.value - minValue.value)

const colors = computed(() => colorSchemes[props.colorScheme] || colorSchemes.blues)

const legendColors = computed(() => colors.value)

// Create grid data with proper positioning
const gridData = computed(() => {
  const grid = []
  
  for (let y = 0; y < gridRows.value; y++) {
    for (let x = 0; x < gridColumns.value; x++) {
      const dataPoint = props.data.find(item => item.x === x && item.y === y)
      
      grid.push({
        x,
        y,
        value: dataPoint?.value ?? null,
        label: dataPoint?.label ?? '',
        loading: dataPoint?.loading ?? false,
        gridColumn: x + 1,
        gridRow: y + 1
      })
    }
  }
  
  return grid
})

const tooltipStyles = computed(() => ({
  left: `${tooltip.value.x}px`,
  top: `${tooltip.value.y}px`,
  transform: 'translate(-50%, -100%)',
  marginTop: '-8px'
}))

// Methods
const getCellStyles = (cell) => {
  const styles = {
    gridColumn: cell.gridColumn,
    gridRow: cell.gridRow,
    width: `${cellWidth.value}px`,
    height: `${cellHeight.value}px`,
    borderRadius: '4px'
  }
  
  if (cell.value !== null) {
    styles.backgroundColor = getColorForValue(cell.value)
  } else {
    styles.backgroundColor = '#f3f4f6'
    styles.opacity = '0.3'
  }
  
  return styles
}

const getColorForValue = (value) => {
  if (valueRange.value === 0) return colors.value[0]
  
  const normalizedValue = (value - minValue.value) / valueRange.value
  const colorIndex = Math.floor(normalizedValue * (colors.value.length - 1))
  const clampedIndex = Math.max(0, Math.min(colors.value.length - 1, colorIndex))
  
  return colors.value[clampedIndex]
}

const getValueTextColor = (value) => {
  const normalizedValue = (value - minValue.value) / valueRange.value
  return normalizedValue > 0.5 ? 'text-white' : 'text-gray-900'
}

const formatCellValue = (value) => {
  if (value === null || value === undefined) return 'N/A'
  
  switch (props.valueFormat) {
    case 'percentage':
      return `${value.toFixed(props.precision)}%`
    case 'currency':
      return `$${value.toFixed(props.precision)}`
    case 'number':
    default:
      return value.toFixed(props.precision)
  }
}

const handleCellHover = (cell, event) => {
  if (cell.value === null) return
  
  const rect = event.target.getBoundingClientRect()
  tooltip.value = {
    show: true,
    x: rect.left + rect.width / 2,
    y: rect.top,
    title: cell.label || `Cell (${cell.x}, ${cell.y})`,
    value: cell.value,
    description: props.yLabels[cell.y] && props.xLabels[cell.x] 
      ? `${props.yLabels[cell.y]} × ${props.xLabels[cell.x]}`
      : null
  }
  
  emit('cell-hover', cell)
}

const hideTooltip = () => {
  tooltip.value.show = false
}

const handleCellClick = (cell) => {
  emit('cell-click', cell)
}

// Handle window scroll to hide tooltip
const handleScroll = () => {
  hideTooltip()
}

// Lifecycle
onMounted(() => {
  window.addEventListener('scroll', handleScroll, true)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll, true)
})
</script>

<style scoped>
.heatmap-chart {
  @apply overflow-x-auto;
}

.heatmap-grid {
  @apply relative;
}

.heatmap-cell {
  @apply border border-white dark:border-gray-800;
}

.heatmap-cell:hover {
  @apply ring-2 ring-blue-500 ring-opacity-50;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .heatmap-chart {
    @apply text-xs;
  }
}
</style>