<template>
  <div class="line-chart-widget h-full p-4">
    <!-- Chart Container -->
    <div class="h-full relative">
      <Chart
        v-if="hasData"
        type="line"
        :data="chartData"
        :options="chartOptions"
        class="w-full h-full"
      />
      
      <!-- Empty State -->
      <div v-else class="h-full flex items-center justify-center">
        <EmptyState
          icon="ChartLineIcon"
          title="No Data Available"
          description="Connect a data source to display chart"
          size="sm"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Chart from '@/components/ui/Chart.vue'
import EmptyState from '@/components/ui/EmptyState.vue'

const props = defineProps({
  widget: {
    type: Object,
    required: true
  },
  config: {
    type: Object,
    required: true
  },
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: String
})

// Computed properties
const hasData = computed(() => {
  return props.data && props.data.length > 0
})

const chartData = computed(() => {
  if (!hasData.value) return null

  const datasets = []
  const labels = []
  
  // Process data based on configuration
  if (props.config.datasets) {
    // Multi-dataset configuration
    datasets.push(...props.config.datasets.map((dataset, index) => ({
      label: dataset.label,
      data: props.data.map(item => item[dataset.field] || 0),
      borderColor: dataset.color || getDefaultColor(index),
      backgroundColor: `${dataset.color || getDefaultColor(index)}20`,
      tension: props.config.smooth ? 0.4 : 0,
      fill: dataset.fill || false,
      ...dataset.options
    })))
    
    labels.push(...props.data.map(item => item[props.config.xAxis] || item.label || ''))
  } else {
    // Simple single dataset
    const yField = props.config.yAxis || 'value'
    const xField = props.config.xAxis || 'label'
    
    datasets.push({
      label: props.config.label || 'Data',
      data: props.data.map(item => item[yField] || 0),
      borderColor: props.config.color || '#3B82F6',
      backgroundColor: `${props.config.color || '#3B82F6'}20`,
      tension: props.config.smooth ? 0.4 : 0,
      fill: props.config.fill || false
    })
    
    labels.push(...props.data.map(item => item[xField] || ''))
  }

  return {
    labels,
    datasets
  }
})

const chartOptions = computed(() => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      intersect: false,
      mode: 'index'
    },
    plugins: {
      legend: {
        display: props.config.showLegend !== false,
        position: props.config.legendPosition || 'top'
      },
      tooltip: {
        enabled: props.config.showTooltip !== false,
        callbacks: {
          label: (context) => {
            let label = context.dataset.label || ''
            if (label) {
              label += ': '
            }
            label += formatValue(context.parsed.y)
            return label
          }
        }
      }
    },
    scales: {
      x: {
        display: props.config.showXAxis !== false,
        title: {
          display: !!props.config.xAxisTitle,
          text: props.config.xAxisTitle
        },
        grid: {
          display: props.config.showGrid !== false,
          color: 'rgba(156, 163, 175, 0.2)'
        }
      },
      y: {
        display: props.config.showYAxis !== false,
        title: {
          display: !!props.config.yAxisTitle,
          text: props.config.yAxisTitle
        },
        grid: {
          display: props.config.showGrid !== false,
          color: 'rgba(156, 163, 175, 0.2)'
        },
        beginAtZero: props.config.beginAtZero !== false,
        ticks: {
          callback: (value) => formatValue(value)
        }
      }
    },
    elements: {
      point: {
        radius: props.config.pointRadius ?? 3,
        hoverRadius: props.config.pointHoverRadius ?? 5
      },
      line: {
        borderWidth: props.config.lineWidth ?? 2
      }
    }
  }
})

// Methods
const getDefaultColor = (index) => {
  const colors = [
    '#3B82F6', // blue
    '#10B981', // green
    '#F59E0B', // yellow
    '#EF4444', // red
    '#8B5CF6', // purple
    '#06B6D4', // cyan
    '#84CC16', // lime
    '#F97316'  // orange
  ]
  return colors[index % colors.length]
}

const formatValue = (value) => {
  if (typeof value !== 'number') return value
  
  const format = props.config.valueFormat || 'number'
  const unit = props.config.unit || ''
  
  switch (format) {
    case 'currency':
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: props.config.currency || 'USD'
      }).format(value)
    
    case 'percentage':
      return `${value.toFixed(props.config.precision || 1)}%`
    
    case 'bytes':
      return formatBytes(value)
    
    case 'number':
    default:
      if (value >= 1000000) {
        return `${(value / 1000000).toFixed(1)}M${unit}`
      } else if (value >= 1000) {
        return `${(value / 1000).toFixed(1)}K${unit}`
      } else {
        const precision = props.config.precision ?? 0
        return `${value.toFixed(precision)}${unit}`
      }
  }
}

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`
}
</script>

<style scoped>
.line-chart-widget {
  @apply overflow-hidden;
}
</style>