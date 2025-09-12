<template>
  <Card :class="cardClasses" :variant="variant">
    <!-- Chart Header -->
    <template v-if="showHeader" #header>
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ title }}
          </h3>
          <p v-if="subtitle" class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {{ subtitle }}
          </p>
        </div>
        
        <div class="flex items-center space-x-3">
          <!-- Current Value Display -->
          <div v-if="currentValue" class="text-right">
            <div class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ formatValue(currentValue) }}
            </div>
            <div v-if="trend !== null" class="flex items-center text-sm">
              <component :is="trendIcon" :class="trendClasses" class="w-4 h-4 mr-1" />
              <span :class="trendClasses">{{ Math.abs(trend).toFixed(1) }}%</span>
            </div>
          </div>
          
          <!-- Time Range Selector -->
          <select 
            v-if="timeRanges && timeRanges.length"
            v-model="selectedTimeRange"
            class="text-sm border-0 bg-transparent text-gray-600 dark:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-md"
            @change="handleTimeRangeChange"
          >
            <option 
              v-for="range in timeRanges" 
              :key="range.value" 
              :value="range.value"
            >
              {{ range.label }}
            </option>
          </select>

          <!-- Refresh Button -->
          <button
            v-if="refreshable"
            @click="handleRefresh"
            :disabled="loading"
            class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <ArrowPathIcon :class="['w-4 h-4', { 'animate-spin': loading }]" />
          </button>
        </div>
      </div>
    </template>

    <!-- Chart Content -->
    <div :class="contentClasses">
      <!-- Empty State -->
      <EmptyState
        v-if="!loading && (!chartData || !chartData.datasets?.length)"
        :icon="ChartBarIcon"
        title="No Data Available"
        description="There's no data to display for the selected time period."
        size="sm"
        variant="info"
        :primary-action="refreshable ? {
          label: 'Refresh Data',
          handler: handleRefresh,
          variant: 'primary',
          icon: ArrowPathIcon
        } : null"
      />

      <!-- Chart -->
      <Chart
        v-else
        :type="chartType"
        :data="processedChartData"
        :options="chartOptions"
        :class="chartClasses"
      />

      <!-- Chart Overlay (Loading) -->
      <div v-if="loading" class="absolute inset-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm rounded-lg flex items-center justify-center">
        <LoadingSpinner size="md" text="Loading chart data..." />
      </div>
    </div>

    <!-- Chart Footer (Legend/Additional Info) -->
    <template v-if="$slots.footer || showLegend" #footer>
      <slot name="footer">
        <div v-if="showLegend && legendData" class="flex flex-wrap gap-4">
          <div 
            v-for="(item, index) in legendData" 
            :key="index"
            class="flex items-center space-x-2"
          >
            <div 
              class="w-3 h-3 rounded-full"
              :style="{ backgroundColor: item.color }"
            ></div>
            <span class="text-sm text-gray-600 dark:text-gray-400">
              {{ item.label }}
              <span v-if="item.value" class="font-medium text-gray-900 dark:text-white ml-1">
                ({{ formatValue(item.value) }})
              </span>
            </span>
          </div>
        </div>
      </slot>
    </template>
  </Card>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import Card from '@/components/ui/Card.vue'
import Chart from '@/components/ui/Chart.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { 
  ArrowUpIcon, 
  ArrowDownIcon, 
  MinusIcon,
  ArrowPathIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  title: String,
  subtitle: String,
  chartType: {
    type: String,
    default: 'line',
    validator: value => ['line', 'bar', 'pie', 'doughnut', 'area', 'scatter'].includes(value)
  },
  chartData: {
    type: Object,
    required: true
  },
  currentValue: [Number, String],
  trend: Number, // percentage change
  unit: String,
  variant: {
    type: String,
    default: 'elevated'
  },
  loading: {
    type: Boolean,
    default: false
  },
  refreshable: {
    type: Boolean,
    default: false
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  showLegend: {
    type: Boolean,
    default: false
  },
  timeRanges: Array, // [{ label: string, value: string }]
  defaultTimeRange: String,
  height: {
    type: String,
    default: '300px'
  },
  colors: {
    type: Array,
    default: () => ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
  },
  options: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['refresh', 'timeRangeChange'])

const selectedTimeRange = ref(props.defaultTimeRange || props.timeRanges?.[0]?.value)

const cardClasses = computed(() => {
  return 'relative overflow-hidden'
})

const contentClasses = computed(() => {
  return `relative ${props.height ? `h-[${props.height}]` : 'h-[300px]'}`
})

const chartClasses = computed(() => {
  return 'w-full h-full'
})

const trendIcon = computed(() => {
  if (props.trend === null || props.trend === undefined) return null
  if (props.trend > 0) return ArrowUpIcon
  if (props.trend < 0) return ArrowDownIcon
  return MinusIcon
})

const trendClasses = computed(() => {
  if (props.trend === null || props.trend === undefined) return 'text-gray-400'
  if (props.trend > 0) return 'text-green-600 dark:text-green-400'
  if (props.trend < 0) return 'text-red-600 dark:text-red-400'
  return 'text-gray-400'
})

const processedChartData = computed(() => {
  if (!props.chartData) return null

  // Apply colors to datasets if not already set
  const processedData = { ...props.chartData }
  
  if (processedData.datasets) {
    processedData.datasets = processedData.datasets.map((dataset, index) => ({
      ...dataset,
      backgroundColor: dataset.backgroundColor || props.colors[index % props.colors.length],
      borderColor: dataset.borderColor || props.colors[index % props.colors.length],
      // Add transparency for area charts
      ...(props.chartType === 'area' && {
        fill: true,
        backgroundColor: `${props.colors[index % props.colors.length]}20`
      })
    }))
  }
  
  return processedData
})

const chartOptions = computed(() => {
  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: !props.showLegend,
        position: 'top'
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: (context) => {
            let label = context.dataset.label || ''
            if (label) {
              label += ': '
            }
            label += formatValue(context.parsed.y || context.parsed)
            return label
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(156, 163, 175, 0.2)'
        },
        ticks: {
          callback: (value) => formatValue(value)
        }
      },
      x: {
        grid: {
          color: 'rgba(156, 163, 175, 0.2)'
        }
      }
    }
  }

  // Remove scales for pie/doughnut charts
  if (props.chartType === 'pie' || props.chartType === 'doughnut') {
    delete baseOptions.scales
  }

  // Merge with provided options
  return { ...baseOptions, ...props.options }
})

const legendData = computed(() => {
  if (!props.chartData?.datasets) return null
  
  return props.chartData.datasets.map((dataset, index) => ({
    label: dataset.label,
    color: dataset.backgroundColor || props.colors[index % props.colors.length],
    value: dataset.data?.reduce((a, b) => (typeof b === 'number' ? a + b : a), 0)
  }))
})

const formatValue = (value) => {
  if (typeof value !== 'number') return value
  
  // Format large numbers
  if (value >= 1000000) {
    return (value / 1000000).toFixed(1) + 'M' + (props.unit || '')
  } else if (value >= 1000) {
    return (value / 1000).toFixed(1) + 'K' + (props.unit || '')
  }
  
  return value.toFixed(1) + (props.unit || '')
}

const handleRefresh = () => {
  emit('refresh')
}

const handleTimeRangeChange = () => {
  emit('timeRangeChange', selectedTimeRange.value)
}

// Watch for default time range changes
watch(() => props.defaultTimeRange, (newValue) => {
  if (newValue && selectedTimeRange.value !== newValue) {
    selectedTimeRange.value = newValue
  }
})
</script>
</template>