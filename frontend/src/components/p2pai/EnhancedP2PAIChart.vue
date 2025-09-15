<template>
  <div class="enhanced-p2pai-chart">
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
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
            <option value="30d">Last 30 Days</option>
          </select>
          
          <!-- P2PAI Specific Filters -->
          <select 
            v-model="selectedMetric"
            @change="onMetricChange"
            class="text-xs border border-gray-300 dark:border-gray-600 rounded px-2 py-1 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            <option value="accuracy">Accuracy</option>
            <option value="loss">Loss</option>
            <option value="participants">Participants</option>
            <option value="rounds">Training Rounds</option>
          </select>
          
          <!-- Refresh Button -->
          <Button 
            @click="refreshData" 
            variant="ghost" 
            size="xs"
            :loading="refreshing"
            class="p-1"
          >
            <ArrowPathIcon class="w-3 h-3" />
          </Button>
          
          <!-- Export Button -->
          <Button 
            @click="exportChart" 
            variant="ghost" 
            size="xs"
            class="p-1"
          >
            <ArrowDownTrayIcon class="w-3 h-3" />
          </Button>
        </div>
      </div>
      
      <!-- Chart Container -->
      <div 
        ref="chartContainer" 
        :style="{ height: height + 'px' }"
        class="w-full relative"
      >
        <!-- Canvas for Chart.js -->
        <canvas 
          ref="chartCanvas"
          :class="['w-full h-full', animated ? 'transition-all duration-500' : '']"
        ></canvas>
        
        <!-- Overlay for Real-time Status -->
        <div v-if="realTime" class="absolute top-2 right-2">
          <div class="flex items-center space-x-1 px-2 py-1 bg-black/20 backdrop-blur-sm rounded text-xs text-white">
            <div class="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></div>
            <span>Live</span>
          </div>
        </div>
      </div>
      
      <!-- Chart Statistics -->
      <div v-if="showStats && chartStats" class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <div class="text-sm font-medium text-gray-900 dark:text-white">{{ chartStats.avg.toFixed(2) }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Average</div>
        </div>
        <div class="text-center p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <div class="text-sm font-medium text-gray-900 dark:text-white">{{ chartStats.max.toFixed(2) }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Maximum</div>
        </div>
        <div class="text-center p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <div class="text-sm font-medium text-gray-900 dark:text-white">{{ chartStats.min.toFixed(2) }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Minimum</div>
        </div>
        <div class="text-center p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <div class="text-sm font-medium text-gray-900 dark:text-white">{{ chartStats.trend > 0 ? '+' : '' }}{{ chartStats.trend.toFixed(1) }}%</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">Trend</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { ArrowPathIcon, ArrowDownTrayIcon } from '@heroicons/vue/24/outline'
import { Chart, registerables } from 'chart.js'
import Button from '@/components/ui/Button.vue'

Chart.register(...registerables)

const props = defineProps({
  title: {
    type: String,
    default: 'P2PAI Metrics'
  },
  subtitle: String,
  data: {
    type: Object,
    required: true
  },
  type: {
    type: String,
    default: 'line'
  },
  height: {
    type: Number,
    default: 300
  },
  theme: {
    type: String,
    default: 'light'
  },
  realTime: {
    type: Boolean,
    default: false
  },
  showStats: {
    type: Boolean,
    default: false
  },
  animated: {
    type: Boolean,
    default: true
  },
  refreshInterval: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['refresh', 'export', 'time-range-change', 'metric-change'])

// Refs
const chartContainer = ref(null)
const chartCanvas = ref(null)
const chart = ref(null)

// State
const loading = ref(false)
const error = ref(null)
const refreshing = ref(false)
const selectedTimeRange = ref('24h')
const selectedMetric = ref('accuracy')

// Auto-refresh interval
let refreshIntervalId = null

// Chart theme colors for P2PAI
const themeColors = computed(() => {
  if (props.theme === 'dark') {
    return {
      text: '#f8fafc',
      grid: '#374151',
      background: 'rgba(147, 51, 234, 0.1)', // Purple theme for P2PAI
      primary: '#9333ea',
      secondary: '#06b6d4',
      accent: '#10b981'
    }
  }
  return {
    text: '#1f2937',
    grid: '#e5e7eb',
    background: 'rgba(147, 51, 234, 0.05)',
    primary: '#9333ea',
    secondary: '#06b6d4',
    accent: '#10b981'
  }
})

// Calculate chart statistics
const chartStats = computed(() => {
  if (!props.data?.datasets?.[0]?.data) return null
  
  const data = props.data.datasets[0].data
  const values = data.filter(v => v !== null && v !== undefined)
  
  if (values.length === 0) return null
  
  const sum = values.reduce((a, b) => a + b, 0)
  const avg = sum / values.length
  const max = Math.max(...values)
  const min = Math.min(...values)
  
  // Calculate trend (comparing first and last value)
  const trend = values.length > 1 
    ? ((values[values.length - 1] - values[0]) / values[0]) * 100 
    : 0
  
  return { avg, max, min, trend }
})

// Chart configuration
const chartConfig = computed(() => ({
  type: props.type,
  data: {
    ...props.data,
    datasets: props.data.datasets?.map(dataset => ({
      ...dataset,
      borderColor: dataset.borderColor || themeColors.value.primary,
      backgroundColor: dataset.backgroundColor || themeColors.value.background,
      pointBackgroundColor: themeColors.value.primary,
      pointBorderColor: themeColors.value.primary,
      tension: props.type === 'line' ? 0.4 : 0,
      fill: props.type === 'line' ? 'origin' : false
    }))
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: props.animated ? {
      duration: 750,
      easing: 'easeInOutQuart'
    } : false,
    interaction: {
      intersect: false,
      mode: 'index'
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: themeColors.value.text,
          usePointStyle: true,
          pointStyle: 'circle'
        }
      },
      tooltip: {
        backgroundColor: props.theme === 'dark' ? '#1f2937' : '#ffffff',
        titleColor: themeColors.value.text,
        bodyColor: themeColors.value.text,
        borderColor: themeColors.value.grid,
        borderWidth: 1,
        displayColors: true,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            label += context.parsed.y;
            
            // Add units based on selected metric
            if (selectedMetric.value === 'accuracy') {
              label += '%';
            } else if (selectedMetric.value === 'participants') {
              label += ' nodes';
            } else if (selectedMetric.value === 'rounds') {
              label += ' rounds';
            }
            
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        display: true,
        grid: {
          color: themeColors.value.grid,
          drawBorder: false
        },
        ticks: {
          color: themeColors.value.text,
          maxTicksLimit: 8
        }
      },
      y: {
        display: true,
        grid: {
          color: themeColors.value.grid,
          drawBorder: false
        },
        ticks: {
          color: themeColors.value.text,
          callback: function(value) {
            if (selectedMetric.value === 'accuracy') {
              return value + '%';
            } else if (selectedMetric.value === 'participants') {
              return value + ' nodes';
            }
            return value;
          }
        }
      }
    }
  }
}))

// Methods
const createChart = async () => {
  if (!chartCanvas.value) return
  
  destroyChart()
  
  await nextTick()
  
  try {
    chart.value = new Chart(chartCanvas.value, chartConfig.value)
  } catch (err) {
    console.error('Failed to create chart:', err)
    error.value = 'Failed to create chart'
  }
}

const destroyChart = () => {
  if (chart.value) {
    chart.value.destroy()
    chart.value = null
  }
}

const updateChart = () => {
  if (chart.value) {
    chart.value.data = chartConfig.value.data
    chart.value.options = chartConfig.value.options
    chart.value.update(props.animated ? 'active' : 'none')
  }
}

const refreshData = () => {
  refreshing.value = true
  emit('refresh')
  setTimeout(() => {
    refreshing.value = false
  }, 1000)
}

const exportChart = () => {
  if (chart.value) {
    const url = chart.value.toBase64Image()
    const link = document.createElement('a')
    link.download = `p2pai-chart-${Date.now()}.png`
    link.href = url
    link.click()
  }
  emit('export')
}

const onTimeRangeChange = () => {
  emit('time-range-change', selectedTimeRange.value)
}

const onMetricChange = () => {
  emit('metric-change', selectedMetric.value)
}

const retry = () => {
  error.value = null
  refreshData()
}

// Setup auto-refresh
const setupAutoRefresh = () => {
  if (props.refreshInterval > 0) {
    refreshIntervalId = setInterval(() => {
      if (props.realTime && !refreshing.value) {
        refreshData()
      }
    }, props.refreshInterval)
  }
}

const clearAutoRefresh = () => {
  if (refreshIntervalId) {
    clearInterval(refreshIntervalId)
    refreshIntervalId = null
  }
}

// Watchers
watch(() => props.data, () => {
  updateChart()
}, { deep: true })

watch(() => props.theme, () => {
  createChart()
})

watch(() => props.refreshInterval, () => {
  clearAutoRefresh()
  setupAutoRefresh()
})

// Lifecycle
onMounted(async () => {
  await nextTick()
  await createChart()
  setupAutoRefresh()
})

onUnmounted(() => {
  destroyChart()
  clearAutoRefresh()
})
</script>

<style scoped>
.enhanced-p2pai-chart {
  @apply w-full;
}

select {
  @apply focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent;
}
</style>