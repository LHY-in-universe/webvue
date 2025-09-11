<template>
  <div class="advanced-chart" :class="containerClasses">
    <!-- Chart Header -->
    <div v-if="showHeader" class="chart-header mb-4">
      <div class="flex items-center justify-between">
        <div>
          <h3 v-if="title" class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ title }}
          </h3>
          <p v-if="subtitle" class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {{ subtitle }}
          </p>
        </div>
        
        <div class="flex items-center space-x-2">
          <!-- Export Menu -->
          <div v-if="exportable" class="relative">
            <Button
              variant="ghost"
              size="sm"
              :leftIcon="ArrowDownTrayIcon"
              @click="showExportMenu = !showExportMenu"
            >
              Export
            </Button>
            
            <!-- Export Dropdown -->
            <div
              v-if="showExportMenu"
              class="absolute right-0 top-full mt-1 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg border border-gray-200 dark:border-gray-700 z-20"
              @click.stop
            >
              <div class="py-1">
                <button
                  v-for="format in exportFormats"
                  :key="format.type"
                  @click="exportChart(format.type)"
                  class="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  <component :is="format.icon" class="w-4 h-4 inline mr-2" />
                  {{ format.label }}
                </button>
              </div>
            </div>
          </div>
          
          <!-- Fullscreen Toggle -->
          <Button
            v-if="fullscreenable"
            variant="ghost"
            size="sm"
            :leftIcon="isFullscreen ? ArrowsPointingInIcon : ArrowsPointingOutIcon"
            @click="toggleFullscreen"
          />
          
          <!-- Refresh Button -->
          <Button
            v-if="refreshable"
            variant="ghost"
            size="sm"
            :leftIcon="ArrowPathIcon"
            @click="refreshChart"
            :disabled="loading"
          />
        </div>
      </div>
    </div>

    <!-- Chart Container -->
    <div 
      ref="chartContainer"
      :class="chartContainerClasses"
      :style="chartContainerStyles"
    >
      <!-- Loading Overlay -->
      <div 
        v-if="loading"
        class="absolute inset-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm rounded-lg flex items-center justify-center z-10"
      >
        <LoadingSpinner size="lg" text="Loading chart data..." />
      </div>

      <!-- Error State -->
      <div 
        v-else-if="error"
        class="absolute inset-0 flex items-center justify-center rounded-lg bg-red-50 dark:bg-red-900/20"
      >
        <div class="text-center p-6">
          <ExclamationCircleIcon class="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-red-900 dark:text-red-100 mb-2">
            Chart Error
          </h3>
          <p class="text-sm text-red-700 dark:text-red-300 mb-4">
            {{ error }}
          </p>
          <Button
            variant="primary"
            size="sm"
            @click="refreshChart"
          >
            Try Again
          </Button>
        </div>
      </div>

      <!-- Empty State -->
      <div 
        v-else-if="!hasData"
        class="absolute inset-0 flex items-center justify-center"
      >
        <EmptyState
          :icon="ChartBarIcon"
          title="No Data Available"
          description="Connect a data source to display chart visualization"
          size="md"
        />
      </div>

      <!-- Chart Component -->
      <component
        v-else
        :is="chartComponent"
        v-bind="chartProps"
        :data="processedData"
        :options="finalChartOptions"
        :class="chartClasses"
        @click="handleChartClick"
        @hover="handleChartHover"
      />
    </div>

    <!-- Chart Legend (External) -->
    <div 
      v-if="showExternalLegend && legendData?.length"
      class="chart-legend mt-4"
    >
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        <div
          v-for="(item, index) in legendData"
          :key="index"
          class="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-colors"
          @click="toggleLegendItem(index)"
        >
          <div 
            class="w-3 h-3 rounded-full flex-shrink-0"
            :style="{ backgroundColor: item.color }"
          ></div>
          <span class="text-sm text-gray-700 dark:text-gray-300 truncate">
            {{ item.label }}
          </span>
          <span v-if="item.value" class="text-xs text-gray-500 dark:text-gray-400">
            {{ formatValue(item.value) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Chart Stats -->
    <div 
      v-if="showStats && chartStats"
      class="chart-stats mt-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
    >
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="(stat, key) in chartStats" :key="key" class="text-center">
          <div class="text-sm font-medium text-gray-500 dark:text-gray-400">
            {{ formatStatLabel(key) }}
          </div>
          <div class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ formatValue(stat) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Click outside handler -->
    <div
      v-if="showExportMenu"
      @click="showExportMenu = false"
      class="fixed inset-0 z-10"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import Button from '@/components/ui/Button.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import Chart from '@/components/ui/Chart.vue'
import {
  ArrowDownTrayIcon,
  ArrowsPointingInIcon,
  ArrowsPointingOutIcon,
  ArrowPathIcon,
  ExclamationCircleIcon,
  ChartBarIcon,
  PhotoIcon,
  DocumentIcon,
  ClipboardDocumentIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  // Chart configuration
  type: {
    type: String,
    default: 'line',
    validator: value => ['line', 'bar', 'pie', 'doughnut', 'area', 'scatter', 'bubble', 'radar', 'polarArea'].includes(value)
  },
  data: {
    type: [Object, Array],
    required: true
  },
  options: {
    type: Object,
    default: () => ({})
  },
  
  // Display options
  title: String,
  subtitle: String,
  showHeader: {
    type: Boolean,
    default: true
  },
  height: {
    type: [String, Number],
    default: 400
  },
  width: {
    type: [String, Number],
    default: '100%'
  },
  
  // Features
  loading: {
    type: Boolean,
    default: false
  },
  error: String,
  refreshable: {
    type: Boolean,
    default: false
  },
  exportable: {
    type: Boolean,
    default: true
  },
  fullscreenable: {
    type: Boolean,
    default: true
  },
  
  // Legend and stats
  showExternalLegend: {
    type: Boolean,
    default: false
  },
  showStats: {
    type: Boolean,
    default: false
  },
  
  // Theming
  theme: {
    type: String,
    default: 'default'
  },
  colorScheme: {
    type: Array,
    default: () => ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16', '#F97316']
  }
})

const emit = defineEmits(['refresh', 'export', 'chart-click', 'chart-hover', 'legend-click'])

// Responsive functionality
const { 
  isMobile, 
  isTablet, 
  getChartDimensions, 
  getResponsiveValue, 
  containerPadding 
} = useResponsive()

// Refs
const chartContainer = ref(null)

// State
const showExportMenu = ref(false)
const isFullscreen = ref(false)
const hiddenDatasets = ref(new Set())

// Chart components mapping
const chartComponents = {
  line: Chart,
  bar: Chart,
  pie: Chart,
  doughnut: Chart,
  area: Chart,
  scatter: Chart,
  bubble: Chart,
  radar: Chart,
  polarArea: Chart
}

// Export formats
const exportFormats = ref([
  { type: 'png', label: 'PNG Image', icon: PhotoIcon },
  { type: 'jpg', label: 'JPEG Image', icon: PhotoIcon },
  { type: 'svg', label: 'SVG Vector', icon: DocumentIcon },
  { type: 'pdf', label: 'PDF Document', icon: DocumentIcon },
  { type: 'csv', label: 'CSV Data', icon: ClipboardDocumentIcon },
  { type: 'json', label: 'JSON Data', icon: ClipboardDocumentIcon }
])

// Computed properties
const hasData = computed(() => {
  if (Array.isArray(props.data)) {
    return props.data.length > 0
  }
  if (typeof props.data === 'object' && props.data !== null) {
    return props.data.datasets && props.data.datasets.length > 0
  }
  return false
})

const chartComponent = computed(() => {
  return chartComponents[props.type] || Chart
})

const containerClasses = computed(() => {
  return [
    'relative',
    isFullscreen.value && 'fixed inset-0 z-50 bg-white dark:bg-gray-900 p-6'
  ]
})

const chartContainerClasses = computed(() => {
  return [
    'relative rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800',
    props.loading && 'pointer-events-none'
  ]
})

const chartContainerStyles = computed(() => {
  return {
    height: typeof props.height === 'number' ? `${props.height}px` : props.height,
    width: typeof props.width === 'number' ? `${props.width}px` : props.width
  }
})

const chartClasses = computed(() => {
  return 'w-full h-full p-4'
})

const processedData = computed(() => {
  if (!hasData.value) return null
  
  let data = { ...props.data }
  
  // Apply color scheme
  if (data.datasets) {
    data.datasets = data.datasets.map((dataset, index) => ({
      ...dataset,
      backgroundColor: dataset.backgroundColor || props.colorScheme[index % props.colorScheme.length],
      borderColor: dataset.borderColor || props.colorScheme[index % props.colorScheme.length],
      hidden: hiddenDatasets.value.has(index)
    }))
  }
  
  return data
})

const finalChartOptions = computed(() => {
  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: 'index'
    },
    plugins: {
      legend: {
        display: !props.showExternalLegend,
        position: getResponsiveValue({ xs: 'bottom', md: 'top' }),
        labels: {
          usePointStyle: true,
          padding: getResponsiveValue({ xs: 10, md: 20 }),
          color: 'rgb(107, 114, 128)',
          font: {
            size: getResponsiveValue({ xs: 10, md: 12 })
          }
        }
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgb(17, 24, 39)',
        titleColor: 'white',
        bodyColor: 'white',
        borderColor: 'rgb(55, 65, 81)',
        borderWidth: 1,
        cornerRadius: 8,
        padding: getResponsiveValue({ xs: 8, md: 12 }),
        titleFont: {
          size: getResponsiveValue({ xs: 11, md: 13 })
        },
        bodyFont: {
          size: getResponsiveValue({ xs: 10, md: 12 })
        },
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
    scales: props.type !== 'pie' && props.type !== 'doughnut' ? {
      x: {
        ticks: {
          font: {
            size: getResponsiveValue({ xs: 9, md: 11 })
          },
          color: 'rgb(107, 114, 128)',
          maxRotation: isMobile.value ? 45 : 0
        },
        grid: {
          color: 'rgba(107, 114, 128, 0.1)'
        }
      },
      y: {
        ticks: {
          font: {
            size: getResponsiveValue({ xs: 9, md: 11 })
          },
          color: 'rgb(107, 114, 128)'
        },
        grid: {
          color: 'rgba(107, 114, 128, 0.1)'
        }
      }
    } : undefined
  }
  
  // Merge with provided options
  return mergeDeep(baseOptions, props.options)
})

const legendData = computed(() => {
  if (!hasData.value || !props.data.datasets) return []
  
  return props.data.datasets.map((dataset, index) => ({
    label: dataset.label,
    color: dataset.backgroundColor || props.colorScheme[index % props.colorScheme.length],
    value: dataset.data ? dataset.data.reduce((sum, val) => sum + (typeof val === 'number' ? val : val.y || 0), 0) : 0,
    hidden: hiddenDatasets.value.has(index)
  }))
})

const chartStats = computed(() => {
  if (!hasData.value) return null
  
  const allValues = []
  props.data.datasets?.forEach(dataset => {
    if (dataset.data) {
      dataset.data.forEach(val => {
        const numVal = typeof val === 'number' ? val : val.y || 0
        allValues.push(numVal)
      })
    }
  })
  
  if (allValues.length === 0) return null
  
  return {
    total: allValues.reduce((sum, val) => sum + val, 0),
    average: allValues.reduce((sum, val) => sum + val, 0) / allValues.length,
    min: Math.min(...allValues),
    max: Math.max(...allValues)
  }
})

const chartProps = computed(() => {
  return {
    type: props.type,
    ...props.options
  }
})

// Methods
const formatValue = (value) => {
  if (typeof value !== 'number') return value
  
  if (value >= 1000000) {
    return `${(value / 1000000).toFixed(1)}M`
  } else if (value >= 1000) {
    return `${(value / 1000).toFixed(1)}K`
  } else {
    return value.toFixed(1)
  }
}

const formatStatLabel = (key) => {
  const labels = {
    total: 'Total',
    average: 'Average',
    min: 'Minimum',
    max: 'Maximum'
  }
  return labels[key] || key
}

const refreshChart = () => {
  emit('refresh')
}

const exportChart = async (format) => {
  showExportMenu.value = false
  
  try {
    let exportData
    
    switch (format) {
      case 'png':
      case 'jpg':
        exportData = await exportAsImage(format)
        break
      case 'svg':
        exportData = await exportAsSVG()
        break
      case 'pdf':
        exportData = await exportAsPDF()
        break
      case 'csv':
        exportData = exportAsCSV()
        break
      case 'json':
        exportData = exportAsJSON()
        break
    }
    
    emit('export', { format, data: exportData })
    
    // Download file
    downloadFile(exportData, `chart.${format}`, format)
    
  } catch (error) {
    console.error('Export failed:', error)
  }
}

const exportAsImage = async (format) => {
  const canvas = chartContainer.value?.querySelector('canvas')
  if (!canvas) throw new Error('No canvas found')
  
  return canvas.toDataURL(`image/${format}`)
}

const exportAsSVG = async () => {
  // SVG export implementation would go here
  throw new Error('SVG export not implemented')
}

const exportAsPDF = async () => {
  // PDF export implementation would go here
  throw new Error('PDF export not implemented')
}

const exportAsCSV = () => {
  const csv = []
  csv.push(['Label', ...props.data.datasets.map(d => d.label)])
  
  props.data.labels?.forEach((label, index) => {
    const row = [label]
    props.data.datasets.forEach(dataset => {
      row.push(dataset.data[index] || 0)
    })
    csv.push(row)
  })
  
  return csv.map(row => row.join(',')).join('\n')
}

const exportAsJSON = () => {
  return JSON.stringify(props.data, null, 2)
}

const downloadFile = (data, filename, format) => {
  let blob
  let url
  
  if (format === 'png' || format === 'jpg') {
    // Convert data URL to blob
    const byteString = atob(data.split(',')[1])
    const mimeString = data.split(',')[0].split(':')[1].split(';')[0]
    const ab = new ArrayBuffer(byteString.length)
    const ia = new Uint8Array(ab)
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i)
    }
    blob = new Blob([ab], { type: mimeString })
    url = URL.createObjectURL(blob)
  } else {
    const mimeTypes = {
      csv: 'text/csv',
      json: 'application/json',
      svg: 'image/svg+xml',
      pdf: 'application/pdf'
    }
    
    blob = new Blob([data], { type: mimeTypes[format] || 'text/plain' })
    url = URL.createObjectURL(blob)
  }
  
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
}

const toggleLegendItem = (index) => {
  if (hiddenDatasets.value.has(index)) {
    hiddenDatasets.value.delete(index)
  } else {
    hiddenDatasets.value.add(index)
  }
  hiddenDatasets.value = new Set(hiddenDatasets.value)
  
  emit('legend-click', { index, hidden: hiddenDatasets.value.has(index) })
}

const handleChartClick = (event) => {
  emit('chart-click', event)
}

const handleChartHover = (event) => {
  emit('chart-hover', event)
}

// Utility function for deep merging objects
const mergeDeep = (target, source) => {
  const result = { ...target }
  
  for (const key in source) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      result[key] = mergeDeep(result[key] || {}, source[key])
    } else {
      result[key] = source[key]
    }
  }
  
  return result
}

// Handle escape key for fullscreen
const handleKeydown = (event) => {
  if (event.key === 'Escape' && isFullscreen.value) {
    isFullscreen.value = false
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.advanced-chart {
  @apply w-full;
}

.chart-legend {
  @apply border-t border-gray-200 dark:border-gray-700 pt-4;
}

.chart-stats {
  @apply border-t border-gray-200 dark:border-gray-700;
}

/* Fullscreen styles */
.advanced-chart.fixed {
  backdrop-filter: blur(4px);
}
</style>