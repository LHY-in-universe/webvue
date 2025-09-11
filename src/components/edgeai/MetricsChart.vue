<template>
  <div class="metrics-chart" :style="{ height: height + 'px' }">
    <div v-if="loading" class="flex items-center justify-center h-full">
      <LoadingSpinner />
    </div>
    
    <div v-else-if="error" class="flex items-center justify-center h-full text-red-500">
      <ExclamationTriangleIcon class="w-6 h-6 mr-2" />
      {{ error }}
    </div>
    
    <canvas 
      v-else
      ref="chartCanvas"
      :width="width"
      :height="height"
      class="w-full h-full"
    ></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  type: {
    type: String,
    default: 'line',
    validator: value => ['line', 'bar', 'pie', 'doughnut', 'radar', 'area'].includes(value)
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
    default: 300
  },
  responsive: {
    type: Boolean,
    default: true
  },
  animated: {
    type: Boolean,
    default: true
  },
  theme: {
    type: String,
    default: 'light',
    validator: value => ['light', 'dark'].includes(value)
  }
})

const emit = defineEmits(['click', 'hover', 'legend-click'])

const chartCanvas = ref(null)
const chartInstance = ref(null)
const loading = ref(true)
const error = ref(null)
const animationId = ref(null)

// Chart configuration based on type and theme
const getChartConfig = () => {
  const isDark = props.theme === 'dark'
  const colors = {
    primary: '#10b981',
    secondary: '#3b82f6',
    accent: '#8b5cf6',
    warning: '#f59e0b',
    danger: '#ef4444',
    text: isDark ? '#f9fafb' : '#111827',
    grid: isDark ? '#374151' : '#e5e7eb',
    background: isDark ? '#1f2937' : '#ffffff'
  }

  const baseConfig = {
    responsive: props.responsive,
    maintainAspectRatio: false,
    animation: props.animated ? {
      duration: 1000,
      easing: 'easeInOutQuart'
    } : false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: colors.text,
          usePointStyle: true,
          padding: 20
        }
      },
      tooltip: {
        enabled: true,
        backgroundColor: colors.background,
        titleColor: colors.text,
        bodyColor: colors.text,
        borderColor: colors.grid,
        borderWidth: 1,
        cornerRadius: 8,
        displayColors: true
      }
    },
    scales: {
      x: {
        type: 'linear',
        display: true,
        grid: {
          color: colors.grid,
          drawBorder: false
        },
        ticks: {
          color: colors.text
        }
      },
      y: {
        type: 'linear',
        display: true,
        grid: {
          color: colors.grid,
          drawBorder: false
        },
        ticks: {
          color: colors.text
        }
      }
    },
    interaction: {
      mode: 'index',
      intersect: false
    },
    onClick: (event, elements) => {
      if (elements.length > 0) {
        emit('click', { event, elements })
      }
    },
    onHover: (event, elements) => {
      emit('hover', { event, elements })
    }
  }

  // Type-specific configurations
  switch (props.type) {
    case 'line':
    case 'area':
      return {
        ...baseConfig,
        elements: {
          line: {
            tension: 0.3,
            borderWidth: 3,
            fill: props.type === 'area'
          },
          point: {
            radius: 4,
            hoverRadius: 6,
            borderWidth: 2
          }
        }
      }
    
    case 'bar':
      return {
        ...baseConfig,
        elements: {
          bar: {
            borderRadius: 4,
            borderSkipped: false
          }
        }
      }
    
    case 'pie':
    case 'doughnut':
      return {
        ...baseConfig,
        cutout: props.type === 'doughnut' ? '60%' : 0,
        scales: {}, // Remove scales for pie charts
        elements: {
          arc: {
            borderWidth: 2,
            borderColor: colors.background
          }
        }
      }
    
    case 'radar':
      return {
        ...baseConfig,
        scales: {
          r: {
            beginAtZero: true,
            grid: {
              color: colors.grid
            },
            pointLabels: {
              color: colors.text
            },
            ticks: {
              color: colors.text,
              backdropColor: 'transparent'
            }
          }
        },
        elements: {
          line: {
            borderWidth: 2
          },
          point: {
            radius: 4,
            hoverRadius: 6
          }
        }
      }
    
    default:
      return baseConfig
  }
}

// Simple chart rendering without Chart.js dependency
const renderChart = () => {
  if (!chartCanvas.value) return

  const ctx = chartCanvas.value.getContext('2d')
  const config = getChartConfig()
  
  try {
    // Clear canvas
    ctx.clearRect(0, 0, props.width, props.height)
    
    // Set up canvas
    ctx.fillStyle = config.plugins.legend.labels.color
    ctx.font = '12px Inter, system-ui, sans-serif'
    
    // Render based on chart type
    switch (props.type) {
      case 'line':
        renderLineChart(ctx)
        break
      case 'bar':
        renderBarChart(ctx)
        break
      case 'pie':
        renderPieChart(ctx)
        break
      case 'doughnut':
        renderDoughnutChart(ctx)
        break
      case 'area':
        renderAreaChart(ctx)
        break
      default:
        renderLineChart(ctx)
    }
    
    loading.value = false
  } catch (err) {
    error.value = 'Failed to render chart: ' + err.message
    loading.value = false
  }
}

const renderLineChart = (ctx) => {
  const padding = 40
  const chartWidth = props.width - 2 * padding
  const chartHeight = props.height - 2 * padding
  
  if (!props.data.datasets || props.data.datasets.length === 0) return
  
  // Get data range
  const allValues = props.data.datasets.flatMap(dataset => dataset.data || [])
  const minVal = Math.min(...allValues)
  const maxVal = Math.max(...allValues)
  const range = maxVal - minVal || 1
  
  // Draw grid
  ctx.strokeStyle = props.theme === 'dark' ? '#374151' : '#e5e7eb'
  ctx.lineWidth = 1
  
  // Vertical grid lines
  const steps = 6
  for (let i = 0; i <= steps; i++) {
    const x = padding + (chartWidth * i) / steps
    ctx.beginPath()
    ctx.moveTo(x, padding)
    ctx.lineTo(x, padding + chartHeight)
    ctx.stroke()
  }
  
  // Horizontal grid lines
  for (let i = 0; i <= steps; i++) {
    const y = padding + (chartHeight * i) / steps
    ctx.beginPath()
    ctx.moveTo(padding, y)
    ctx.lineTo(padding + chartWidth, y)
    ctx.stroke()
  }
  
  // Draw datasets
  const colors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444']
  
  props.data.datasets.forEach((dataset, datasetIndex) => {
    const color = dataset.borderColor || colors[datasetIndex % colors.length]
    ctx.strokeStyle = color
    ctx.lineWidth = 3
    
    if (dataset.data && dataset.data.length > 0) {
      ctx.beginPath()
      
      dataset.data.forEach((value, index) => {
        const x = padding + (chartWidth * index) / (dataset.data.length - 1)
        const y = padding + chartHeight - ((value - minVal) / range) * chartHeight
        
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      
      ctx.stroke()
      
      // Draw points
      ctx.fillStyle = color
      dataset.data.forEach((value, index) => {
        const x = padding + (chartWidth * index) / (dataset.data.length - 1)
        const y = padding + chartHeight - ((value - minVal) / range) * chartHeight
        
        ctx.beginPath()
        ctx.arc(x, y, 4, 0, 2 * Math.PI)
        ctx.fill()
      })
    }
  })
  
  // Draw labels
  ctx.fillStyle = props.theme === 'dark' ? '#f9fafb' : '#111827'
  ctx.font = '11px Inter, system-ui, sans-serif'
  
  // Y-axis labels
  for (let i = 0; i <= steps; i++) {
    const value = maxVal - (range * i) / steps
    const y = padding + (chartHeight * i) / steps
    ctx.fillText(Math.round(value * 100) / 100, 5, y + 3)
  }
  
  // X-axis labels (if provided)
  if (props.data.labels) {
    props.data.labels.forEach((label, index) => {
      const x = padding + (chartWidth * index) / (props.data.labels.length - 1)
      ctx.save()
      ctx.translate(x, props.height - 10)
      ctx.rotate(-Math.PI / 4)
      ctx.fillText(label, 0, 0)
      ctx.restore()
    })
  }
}

const renderBarChart = (ctx) => {
  const padding = 40
  const chartWidth = props.width - 2 * padding
  const chartHeight = props.height - 2 * padding
  
  if (!props.data.datasets || props.data.datasets.length === 0) return
  
  const allValues = props.data.datasets.flatMap(dataset => dataset.data || [])
  const maxVal = Math.max(...allValues, 0)
  
  const barWidth = chartWidth / (props.data.labels?.length || 1) * 0.8
  const colors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444']
  
  props.data.datasets.forEach((dataset, datasetIndex) => {
    const color = dataset.backgroundColor || colors[datasetIndex % colors.length]
    ctx.fillStyle = color
    
    if (dataset.data && dataset.data.length > 0) {
      dataset.data.forEach((value, index) => {
        const x = padding + (chartWidth * index) / dataset.data.length + (chartWidth / dataset.data.length - barWidth) / 2
        const barHeight = (value / maxVal) * chartHeight
        const y = padding + chartHeight - barHeight
        
        // Rounded rectangle
        const radius = 4
        ctx.beginPath()
        ctx.roundRect(x, y, barWidth, barHeight, radius)
        ctx.fill()
      })
    }
  })
  
  // Labels
  ctx.fillStyle = props.theme === 'dark' ? '#f9fafb' : '#111827'
  ctx.font = '11px Inter, system-ui, sans-serif'
  
  if (props.data.labels) {
    props.data.labels.forEach((label, index) => {
      const x = padding + (chartWidth * index) / props.data.labels.length + chartWidth / props.data.labels.length / 2
      ctx.fillText(label, x - ctx.measureText(label).width / 2, props.height - 10)
    })
  }
}

const renderPieChart = (ctx) => {
  const centerX = props.width / 2
  const centerY = props.height / 2
  const radius = Math.min(props.width, props.height) / 2 - 40
  
  if (!props.data.datasets || props.data.datasets.length === 0) return
  
  const dataset = props.data.datasets[0]
  if (!dataset.data || dataset.data.length === 0) return
  
  const total = dataset.data.reduce((sum, value) => sum + value, 0)
  const colors = dataset.backgroundColor || ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444']
  
  let currentAngle = -Math.PI / 2
  
  dataset.data.forEach((value, index) => {
    const sliceAngle = (value / total) * 2 * Math.PI
    const color = colors[index % colors.length]
    
    ctx.fillStyle = color
    ctx.beginPath()
    ctx.moveTo(centerX, centerY)
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle)
    ctx.closePath()
    ctx.fill()
    
    // Slice border
    ctx.strokeStyle = props.theme === 'dark' ? '#1f2937' : '#ffffff'
    ctx.lineWidth = 2
    ctx.stroke()
    
    currentAngle += sliceAngle
  })
  
  // Legend
  if (props.data.labels) {
    ctx.font = '12px Inter, system-ui, sans-serif'
    ctx.fillStyle = props.theme === 'dark' ? '#f9fafb' : '#111827'
    
    const legendX = props.width - 120
    let legendY = 30
    
    props.data.labels.forEach((label, index) => {
      const color = colors[index % colors.length]
      
      // Legend color box
      ctx.fillStyle = color
      ctx.fillRect(legendX, legendY - 8, 12, 12)
      
      // Legend text
      ctx.fillStyle = props.theme === 'dark' ? '#f9fafb' : '#111827'
      ctx.fillText(label, legendX + 20, legendY + 2)
      
      legendY += 20
    })
  }
}

const renderDoughnutChart = (ctx) => {
  const centerX = props.width / 2
  const centerY = props.height / 2
  const outerRadius = Math.min(props.width, props.height) / 2 - 40
  const innerRadius = outerRadius * 0.6
  
  if (!props.data.datasets || props.data.datasets.length === 0) return
  
  const dataset = props.data.datasets[0]
  if (!dataset.data || dataset.data.length === 0) return
  
  const total = dataset.data.reduce((sum, value) => sum + value, 0)
  const colors = dataset.backgroundColor || ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444']
  
  let currentAngle = -Math.PI / 2
  
  dataset.data.forEach((value, index) => {
    const sliceAngle = (value / total) * 2 * Math.PI
    const color = colors[index % colors.length]
    
    ctx.fillStyle = color
    ctx.beginPath()
    ctx.arc(centerX, centerY, outerRadius, currentAngle, currentAngle + sliceAngle)
    ctx.arc(centerX, centerY, innerRadius, currentAngle + sliceAngle, currentAngle, true)
    ctx.closePath()
    ctx.fill()
    
    // Slice border
    ctx.strokeStyle = props.theme === 'dark' ? '#1f2937' : '#ffffff'
    ctx.lineWidth = 2
    ctx.stroke()
    
    currentAngle += sliceAngle
  })
  
  // Center text
  ctx.fillStyle = props.theme === 'dark' ? '#f9fafb' : '#111827'
  ctx.font = 'bold 16px Inter, system-ui, sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText('Total', centerX, centerY - 5)
  ctx.font = 'bold 20px Inter, system-ui, sans-serif'
  ctx.fillText(total.toString(), centerX, centerY + 15)
  ctx.textAlign = 'left'
}

const renderAreaChart = (ctx) => {
  const padding = 40
  const chartWidth = props.width - 2 * padding
  const chartHeight = props.height - 2 * padding
  
  if (!props.data.datasets || props.data.datasets.length === 0) return
  
  const allValues = props.data.datasets.flatMap(dataset => dataset.data || [])
  const minVal = Math.min(...allValues)
  const maxVal = Math.max(...allValues)
  const range = maxVal - minVal || 1
  
  const colors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444']
  
  props.data.datasets.forEach((dataset, datasetIndex) => {
    const color = dataset.backgroundColor || colors[datasetIndex % colors.length]
    
    if (dataset.data && dataset.data.length > 0) {
      // Create gradient
      const gradient = ctx.createLinearGradient(0, padding, 0, padding + chartHeight)
      gradient.addColorStop(0, color + '80') // 50% opacity
      gradient.addColorStop(1, color + '20') // 12.5% opacity
      
      ctx.fillStyle = gradient
      ctx.beginPath()
      
      // Start from bottom left
      const startX = padding
      const bottomY = padding + chartHeight
      ctx.moveTo(startX, bottomY)
      
      // Draw the area line
      dataset.data.forEach((value, index) => {
        const x = padding + (chartWidth * index) / (dataset.data.length - 1)
        const y = padding + chartHeight - ((value - minVal) / range) * chartHeight
        ctx.lineTo(x, y)
      })
      
      // Close the path at bottom right
      const endX = padding + chartWidth
      ctx.lineTo(endX, bottomY)
      ctx.closePath()
      ctx.fill()
      
      // Draw the line on top
      ctx.strokeStyle = color
      ctx.lineWidth = 3
      ctx.beginPath()
      
      dataset.data.forEach((value, index) => {
        const x = padding + (chartWidth * index) / (dataset.data.length - 1)
        const y = padding + chartHeight - ((value - minVal) / range) * chartHeight
        
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      
      ctx.stroke()
    }
  })
}

// Animation functions
const animate = () => {
  if (props.animated) {
    renderChart()
    animationId.value = requestAnimationFrame(animate)
  }
}

const startAnimation = () => {
  if (props.animated && !animationId.value) {
    animationId.value = requestAnimationFrame(animate)
  }
}

const stopAnimation = () => {
  if (animationId.value) {
    cancelAnimationFrame(animationId.value)
    animationId.value = null
  }
}

// Lifecycle
onMounted(async () => {
  await nextTick()
  renderChart()
  if (props.animated) {
    startAnimation()
  }
})

onUnmounted(() => {
  stopAnimation()
})

// Watch for data changes
watch(() => props.data, () => {
  renderChart()
}, { deep: true })

watch(() => props.theme, () => {
  renderChart()
})

// Add roundRect polyfill for older browsers
if (!CanvasRenderingContext2D.prototype.roundRect) {
  CanvasRenderingContext2D.prototype.roundRect = function(x, y, width, height, radius) {
    this.beginPath()
    this.moveTo(x + radius, y)
    this.lineTo(x + width - radius, y)
    this.quadraticCurveTo(x + width, y, x + width, y + radius)
    this.lineTo(x + width, y + height - radius)
    this.quadraticCurveTo(x + width, y + height, x + width - radius, y + height)
    this.lineTo(x + radius, y + height)
    this.quadraticCurveTo(x, y + height, x, y + height - radius)
    this.lineTo(x, y + radius)
    this.quadraticCurveTo(x, y, x + radius, y)
    this.closePath()
  }
}
</script>

<style scoped>
.metrics-chart {
  position: relative;
  overflow: hidden;
}

canvas {
  display: block;
}
</style>