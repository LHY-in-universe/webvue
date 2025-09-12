<template>
  <div class="chart-container" :class="{ 'loading': isLoading }">
    <!-- Loading State -->
    <div v-if="isLoading" class="chart-loading">
      <div class="loading-spinner">
        <div class="spinner"></div>
      </div>
      <p class="loading-text">Loading chart...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="hasError" class="chart-error">
      <div class="error-icon">
        <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
        </svg>
      </div>
      <p class="error-text">Failed to load chart</p>
      <button @click="retryChart" class="retry-button">Retry</button>
    </div>
    
    <!-- Chart Canvas -->
    <canvas 
      v-else
      :id="chartId" 
      :width="width" 
      :height="height"
      class="chart-canvas"
    ></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

const props = defineProps({
  type: {
    type: String,
    default: 'line',
    validator: (value) => ['line', 'bar', 'pie', 'doughnut'].includes(value)
  },
  data: {
    type: Object,
    required: true
  },
  options: {
    type: Object,
    default: () => ({})
  },
  width: {
    type: Number,
    default: 400
  },
  height: {
    type: Number,
    default: 200
  }
})

const chartId = ref(`chart-${Math.random().toString(36).substr(2, 9)}`)
const isLoading = ref(true)
const hasError = ref(false)
let chartInstance = null

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: false,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.1)',
      },
      ticks: {
        color: 'rgba(0, 0, 0, 0.6)',
      }
    },
    x: {
      grid: {
        color: 'rgba(0, 0, 0, 0.1)',
      },
      ticks: {
        color: 'rgba(0, 0, 0, 0.6)',
      }
    }
  }
}

const createChart = async () => {
  try {
    isLoading.value = true
    hasError.value = false
    
    // Small delay to show loading state
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const canvas = document.getElementById(chartId.value)
    if (!canvas) {
      throw new Error('Canvas element not found')
    }

    const ctx = canvas.getContext('2d')
    
    // Merge default options with provided options
    const mergedOptions = {
      ...defaultOptions,
      ...props.options
    }

    // Remove scales for pie/doughnut charts
    if (props.type === 'pie' || props.type === 'doughnut') {
      delete mergedOptions.scales
    }

    chartInstance = new ChartJS(ctx, {
      type: props.type,
      data: props.data,
      options: mergedOptions
    })
    
    isLoading.value = false
  } catch (error) {
    console.error('Chart creation error:', error)
    isLoading.value = false
    hasError.value = true
  }
}

const updateChart = () => {
  if (chartInstance) {
    chartInstance.data = props.data
    chartInstance.update()
  }
}

const destroyChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
  isLoading.value = false
  hasError.value = false
}

const retryChart = () => {
  destroyChart()
  createChart()
}

// Watch for data changes
watch(() => props.data, updateChart, { deep: true })

onMounted(() => {
  createChart()
})

onUnmounted(() => {
  destroyChart()
})
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 100%;
  width: 100%;
  min-height: 200px;
}

.chart-canvas {
  max-height: 100%;
  max-width: 100%;
  opacity: 1;
  transition: opacity 0.3s ease;
}

/* Loading State */
.chart-loading {
  @apply absolute inset-0 flex flex-col items-center justify-center;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
}

.dark .chart-loading {
  background: rgba(17, 24, 39, 0.9);
}

.loading-spinner {
  @apply mb-3;
}

.spinner {
  @apply w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin;
}

.loading-text {
  @apply text-sm text-gray-600 dark:text-gray-400 font-medium;
}

/* Error State */
.chart-error {
  @apply absolute inset-0 flex flex-col items-center justify-center text-center p-4;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
}

.dark .chart-error {
  background: rgba(17, 24, 39, 0.9);
}

.error-icon {
  @apply mb-3;
}

.error-text {
  @apply text-sm text-gray-600 dark:text-gray-400 font-medium mb-3;
}

.retry-button {
  @apply px-3 py-1 text-xs bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors duration-200;
}

/* Container loading state */
.chart-container.loading {
  @apply opacity-90;
}

/* Smooth transitions */
.chart-loading,
.chart-error {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>