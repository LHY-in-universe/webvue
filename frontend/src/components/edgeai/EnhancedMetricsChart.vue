<template>
  <div class="enhanced-metrics-chart">
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      <span class="ml-2 text-gray-600 dark:text-gray-400">Loading chart...</span>
    </div>
    
    <div v-else-if="error" class="flex items-center justify-center h-64">
      <div class="text-center">
        <div class="text-red-400 mb-2">
          <svg class="w-8 h-8 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z"></path>
          </svg>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-400">{{ error }}</p>
        <Button @click="retry" variant="ghost" size="sm" class="mt-2">
          Retry
        </Button>
      </div>
    </div>
    
    <div v-else class="relative">
      <!-- Chart Header -->
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ title }}</h3>
          <p v-if="subtitle" class="text-sm text-gray-500 dark:text-gray-400">{{ subtitle }}</p>
        </div>
        
        <div class="flex items-center space-x-2">
          <!-- Time Range Selector -->
          <select 
            v-model="selectedTimeRange"
            @change="onTimeRangeChange"
            class="text-xs border border-gray-300 dark:border-gray-600 rounded px-2 py-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            <option value="1h">Last Hour</option>
            <option value="6h">Last 6 Hours</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
          </select>
          
          <!-- Refresh Button -->
          <Button 
            @click="refreshData" 
            variant="ghost" 
            size="xs"
            :loading="refreshing"
            class="p-1"
          >
            <ArrowPathIcon class="w-4 h-4" />
          </Button>
          
          <!-- Export Button -->
          <Button 
            @click="exportChart" 
            variant="ghost" 
            size="xs"
            class="p-1"
          >
            <ArrowDownTrayIcon class="w-4 h-4" />
          </Button>
        </div>
      </div>
      
      <!-- Real-time Indicator -->
      <div v-if="realTime" class="absolute top-2 right-2 z-10">
        <div class="flex items-center space-x-1 bg-green-100 dark:bg-green-900/30 px-2 py-1 rounded-full">
          <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span class="text-xs text-green-700 dark:text-green-300">Live</span>
        </div>
      </div>
      
      <!-- Chart Container -->
      <div 
        ref="chartContainer" 
        :style="{ height: height + 'px' }"
        class="relative bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4"
      >
        <!-- Chart Canvas -->
        <canvas 
          ref="chartCanvas" 
          :width="canvasWidth" 
          :height="canvasHeight"
          class="w-full h-full"
        ></canvas>
        
        <!-- Chart Overlay for Interactions -->
        <div 
          v-if="showTooltip" 
          ref="tooltipEl"
          class="absolute bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 text-xs rounded px-2 py-1 pointer-events-none z-20 shadow-lg"
          :style="tooltipStyle"
        >
          <div v-for="item in tooltipData" :key="item.label" class="flex items-center space-x-2">
            <div 
              class="w-2 h-2 rounded-full" 
              :style="{ backgroundColor: item.color }"
            ></div>
            <span>{{ item.label }}: {{ item.value }}</span>
          </div>
          <div class="text-xs opacity-75 mt-1">{{ tooltipTime }}</div>
        </div>
      </div>
      
      <!-- Chart Legend -->
      <div v-if="showLegend && datasets.length > 1" class="flex flex-wrap justify-center mt-4 space-x-4">
        <div 
          v-for="dataset in datasets" 
          :key="dataset.label"
          @click="toggleDataset(dataset)"
          class="flex items-center space-x-1 cursor-pointer hover:opacity-75 transition-opacity"
          :class="{ 'opacity-50': dataset.hidden }"
        >
          <div 
            class="w-3 h-3 rounded-full" 
            :style="{ backgroundColor: dataset.borderColor }"
          ></div>
          <span class="text-sm text-gray-700 dark:text-gray-300">{{ dataset.label }}</span>
        </div>
      </div>
      
      <!-- Statistics Summary -->
      <div v-if="showStats" class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
        <div 
          v-for="stat in statistics" 
          :key="stat.label"
          class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 text-center"
        >
          <div class="text-lg font-semibold" :style="{ color: stat.color }">
            {{ stat.value }}
          </div>
          <div class="text-xs text-gray-600 dark:text-gray-400">{{ stat.label }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useResizeObserver } from '@/composables/useResizeObserver'
import { useErrorBoundary } from '@/composables/useErrorBoundary'
import Button from '@/components/ui/Button.vue'
import { ArrowPathIcon, ArrowDownTrayIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  title: {
    type: String,
    default: 'Metrics Chart'
  },
  subtitle: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'line', // line, area, bar
    validator: (value) => ['line', 'area', 'bar'].includes(value)
  },
  data: {
    type: Object,
    required: true
  },
  height: {
    type: Number,
    default: 300
  },
  theme: {
    type: String,
    default: 'light',
    validator: (value) => ['light', 'dark'].includes(value)
  },
  realTime: {
    type: Boolean,
    default: false
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  showStats: {
    type: Boolean,
    default: false
  },
  animated: {
    type: Boolean,
    default: true
  },
  responsive: {
    type: Boolean,
    default: true
  },
  refreshInterval: {
    type: Number,
    default: 0 // 0 means no auto-refresh
  }
})

const emit = defineEmits(['refresh', 'export', 'timeRangeChange'])

const { hasError, retry } = useErrorBoundary()

// Refs
const chartContainer = ref(null)
const chartCanvas = ref(null)
const tooltipEl = ref(null)

// State
const loading = ref(false)
const error = ref(null)
const refreshing = ref(false)
const selectedTimeRange = ref('24h')
const showTooltip = ref(false)
const tooltipData = ref([])
const tooltipTime = ref('')
const tooltipStyle = ref({})
const canvasWidth = ref(800)
const canvasHeight = ref(400)

// Chart instance
let chartInstance = null
let animationFrame = null
let refreshTimer = null

// Computed
const datasets = computed(() => props.data?.datasets || [])
const statistics = computed(() => {
  if (!datasets.value.length) return []
  
  return datasets.value.map(dataset => {
    const values = dataset.data || []
    const sum = values.reduce((a, b) => a + b, 0)
    const avg = values.length ? (sum / values.length).toFixed(1) : 0
    const max = values.length ? Math.max(...values).toFixed(1) : 0
    const min = values.length ? Math.min(...values).toFixed(1) : 0
    
    return [
      { label: 'Average', value: avg, color: dataset.borderColor },
      { label: 'Maximum', value: max, color: dataset.borderColor },
      { label: 'Minimum', value: min, color: dataset.borderColor },
      { label: 'Current', value: values[values.length - 1]?.toFixed(1) || '0', color: dataset.borderColor }
    ]
  }).flat()
})

// Resize handling
const { width: containerWidth } = useResizeObserver(chartContainer)

watch(containerWidth, (newWidth) => {
  if (newWidth && props.responsive) {
    nextTick(() => {
      updateCanvasSize()
      redrawChart()
    })
  }
})

// Methods
const updateCanvasSize = () => {
  if (!chartContainer.value) return
  
  const container = chartContainer.value
  canvasWidth.value = container.clientWidth - 32 // Account for padding
  canvasHeight.value = props.height - 32
}

const createChart = () => {
  if (!chartCanvas.value) return
  
  try {
    const ctx = chartCanvas.value.getContext('2d')
    
    // Simple chart implementation (in a real app, you'd use Chart.js or similar)
    chartInstance = {
      ctx,
      data: props.data,
      options: {
        responsive: props.responsive,
        animation: props.animated,
        theme: props.theme
      }
    }
    
    redrawChart()
  } catch (err) {
    error.value = err.message
  }
}

const redrawChart = () => {
  if (!chartInstance || !chartInstance.ctx) return
  
  const ctx = chartInstance.ctx
  const canvas = chartCanvas.value
  
  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  // Draw chart based on type
  switch (props.type) {
    case 'line':
      drawLineChart(ctx)
      break
    case 'area':
      drawAreaChart(ctx)
      break
    case 'bar':
      drawBarChart(ctx)
      break
  }
}

const drawLineChart = (ctx) => {
  // Simple line chart implementation
  const data = props.data
  if (!data || !data.datasets || !data.datasets.length) return
  
  const width = canvasWidth.value
  const height = canvasHeight.value
  const padding = 40
  
  // Draw grid
  ctx.strokeStyle = props.theme === 'dark' ? '#374151' : '#e5e7eb'
  ctx.lineWidth = 1
  
  // Vertical lines
  for (let i = 0; i <= 10; i++) {
    const x = padding + (width - 2 * padding) * i / 10
    ctx.beginPath()
    ctx.moveTo(x, padding)
    ctx.lineTo(x, height - padding)
    ctx.stroke()
  }
  
  // Horizontal lines
  for (let i = 0; i <= 5; i++) {
    const y = padding + (height - 2 * padding) * i / 5
    ctx.beginPath()
    ctx.moveTo(padding, y)
    ctx.lineTo(width - padding, y)
    ctx.stroke()
  }
  
  // Draw datasets
  data.datasets.forEach((dataset, index) => {
    if (dataset.hidden) return
    
    const points = dataset.data || []
    if (!points.length) return
    
    const maxValue = Math.max(...points)
    const minValue = Math.min(...points)
    const range = maxValue - minValue || 1
    
    ctx.strokeStyle = dataset.borderColor || '#3b82f6'
    ctx.lineWidth = 2
    ctx.beginPath()
    
    points.forEach((point, i) => {
      const x = padding + (width - 2 * padding) * i / (points.length - 1)
      const y = height - padding - (height - 2 * padding) * (point - minValue) / range
      
      if (i === 0) {
        ctx.moveTo(x, y)
      } else {
        ctx.lineTo(x, y)
      }
    })
    
    ctx.stroke()
    
    // Draw points
    ctx.fillStyle = dataset.borderColor || '#3b82f6'
    points.forEach((point, i) => {
      const x = padding + (width - 2 * padding) * i / (points.length - 1)
      const y = height - padding - (height - 2 * padding) * (point - minValue) / range
      
      ctx.beginPath()
      ctx.arc(x, y, 3, 0, 2 * Math.PI)
      ctx.fill()
    })
  })
}

const drawAreaChart = (ctx) => {
  // Area chart implementation
  drawLineChart(ctx)
  
  // Add fill area
  const data = props.data
  if (!data || !data.datasets || !data.datasets.length) return
  
  const width = canvasWidth.value
  const height = canvasHeight.value
  const padding = 40
  
  data.datasets.forEach((dataset, index) => {
    if (dataset.hidden) return
    
    const points = dataset.data || []
    if (!points.length) return
    
    const maxValue = Math.max(...points)
    const minValue = Math.min(...points)
    const range = maxValue - minValue || 1
    
    ctx.fillStyle = dataset.backgroundColor || (dataset.borderColor + '20')
    ctx.beginPath()
    
    // Start from bottom
    ctx.moveTo(padding, height - padding)
    
    points.forEach((point, i) => {
      const x = padding + (width - 2 * padding) * i / (points.length - 1)
      const y = height - padding - (height - 2 * padding) * (point - minValue) / range
      ctx.lineTo(x, y)
    })
    
    // Close to bottom
    ctx.lineTo(width - padding, height - padding)
    ctx.closePath()
    ctx.fill()
  })
}

const drawBarChart = (ctx) => {
  // Bar chart implementation
  const data = props.data
  if (!data || !data.datasets || !data.datasets.length) return
  
  const width = canvasWidth.value
  const height = canvasHeight.value
  const padding = 40
  
  const dataset = data.datasets[0] // Simple single dataset bar chart
  const points = dataset.data || []
  if (!points.length) return
  
  const maxValue = Math.max(...points)
  const barWidth = (width - 2 * padding) / points.length * 0.8
  
  ctx.fillStyle = dataset.backgroundColor || dataset.borderColor || '#3b82f6'
  
  points.forEach((point, i) => {
    const x = padding + (width - 2 * padding) * i / points.length + barWidth * 0.1
    const barHeight = (height - 2 * padding) * point / maxValue
    const y = height - padding - barHeight
    
    ctx.fillRect(x, y, barWidth, barHeight)
  })
}

const toggleDataset = (dataset) => {
  dataset.hidden = !dataset.hidden
  redrawChart()
}

const refreshData = async () => {
  refreshing.value = true
  try {
    emit('refresh')
  } finally {
    refreshing.value = false
  }
}

const exportChart = () => {
  if (!chartCanvas.value) return
  
  try {
    const link = document.createElement('a')
    link.download = `${props.title.toLowerCase().replace(/\s+/g, '-')}-chart.png`
    link.href = chartCanvas.value.toDataURL()
    link.click()
    
    emit('export')
  } catch (err) {
    error.value = 'Failed to export chart'
  }
}

const onTimeRangeChange = () => {
  emit('timeRangeChange', selectedTimeRange.value)
}

// Setup auto-refresh
const setupAutoRefresh = () => {
  if (props.refreshInterval > 0) {
    refreshTimer = setInterval(refreshData, props.refreshInterval)
  }
}

const cleanupAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

// Lifecycle
onMounted(() => {
  nextTick(() => {
    updateCanvasSize()
    createChart()
    setupAutoRefresh()
  })
})

onUnmounted(() => {
  cleanupAutoRefresh()
  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
  }
})

// Watch for data changes
watch(() => props.data, () => {
  if (chartInstance) {
    redrawChart()
  }
}, { deep: true })

watch(() => props.theme, () => {
  if (chartInstance) {
    redrawChart()
  }
})

// Expose retry method for error boundary
const retryChart = () => {
  error.value = null
  loading.value = true
  
  nextTick(() => {
    try {
      updateCanvasSize()
      createChart()
      loading.value = false
    } catch (err) {
      error.value = err.message
      loading.value = false
    }
  })
}

defineExpose({
  retry: retryChart,
  export: exportChart,
  refresh: refreshData
})
</script>

<style scoped>
.enhanced-metrics-chart {
  @apply w-full;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>