<template>
  <div class="local-training-chart w-full h-full">
    <div class="chart-container h-full" ref="chartContainer">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useThemeStore } from '@/stores/theme'

const props = defineProps({
  trainingData: {
    type: Object,
    required: true,
    default: () => ({
      rounds: [],
      accuracy: [],
      loss: [],
      cpu: [],
      gpu: [],
      memory: []
    })
  },
  isTraining: {
    type: Boolean,
    default: false
  },
  chartType: {
    type: String,
    default: 'all',
    validator: (value) => ['all', 'accuracy', 'loss', 'cpu', 'memory'].includes(value)
  }
})

const chartContainer = ref(null)
const chartCanvas = ref(null)
const chart = ref(null)
const themeStore = useThemeStore()

let Chart = null

// Chart type configurations
const getChartConfig = () => {
  const baseConfig = {
    type: 'line',
    data: {
      labels: props.trainingData.rounds || [],
      datasets: []
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: props.isTraining ? 200 : 800,
        easing: 'easeInOutQuart'
      },
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        title: {
          display: false
        },
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: themeStore.isDark ? '#374151' : '#ffffff',
          titleColor: themeStore.isDark ? '#f9fafb' : '#111827',
          bodyColor: themeStore.isDark ? '#d1d5db' : '#374151',
          borderColor: themeStore.isDark ? '#4b5563' : '#d1d5db',
          borderWidth: 1,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              if (context.parsed.y !== null) {
                if (label.includes('Accuracy') || label.includes('Usage')) {
                  label += context.parsed.y.toFixed(1) + '%';
                } else if (label.includes('Loss')) {
                  label += context.parsed.y.toFixed(3);
                } else {
                  label += context.parsed.y.toFixed(2);
                }
              }
              return label;
            }
          }
        }
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: 'Training Rounds',
            color: themeStore.isDark ? '#d1d5db' : '#374151',
            font: {
              size: 12,
              weight: 'bold'
            }
          },
          grid: {
            color: themeStore.isDark ? '#374151' : '#e5e7eb',
            drawBorder: false
          },
          ticks: {
            color: themeStore.isDark ? '#9ca3af' : '#6b7280',
            maxTicksLimit: 8
          }
        },
        y: {
          display: true,
          grid: {
            color: themeStore.isDark ? '#374151' : '#e5e7eb',
            drawBorder: false
          },
          ticks: {
            color: themeStore.isDark ? '#9ca3af' : '#6b7280'
          }
        }
      }
    }
  }

  // Configure based on chart type
  switch (props.chartType) {
    case 'accuracy':
      baseConfig.data.datasets = [{
        label: 'Training Accuracy',
        data: props.trainingData.accuracy || [],
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
      baseConfig.options.scales.y.min = 0
      baseConfig.options.scales.y.max = 100
      baseConfig.options.scales.y.ticks.callback = function(value) {
        return value + '%'
      }
      break

    case 'loss':
      baseConfig.data.datasets = [{
        label: 'Training Loss',
        data: props.trainingData.loss || [],
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
      baseConfig.options.scales.y.min = 0
      baseConfig.options.scales.y.ticks.callback = function(value) {
        return value.toFixed(2)
      }
      break

    case 'cpu':
      baseConfig.data.datasets = [{
        label: 'CPU Usage',
        data: props.trainingData.cpu || [],
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
      baseConfig.options.scales.y.min = 0
      baseConfig.options.scales.y.max = 100
      baseConfig.options.scales.y.ticks.callback = function(value) {
        return value + '%'
      }
      break

    case 'memory':
      baseConfig.data.datasets = [{
        label: 'Memory Usage',
        data: props.trainingData.memory || [],
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
      baseConfig.options.scales.y.min = 0
      baseConfig.options.scales.y.max = 100
      baseConfig.options.scales.y.ticks.callback = function(value) {
        return value + '%'
      }
      break

    default: // 'all' - 多指标图表
      baseConfig.data.datasets = [
        {
          label: 'Training Accuracy (%)',
          data: props.trainingData.accuracy || [],
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          borderWidth: 2,
          fill: false,
          tension: 0.4,
          pointRadius: 3,
          pointHoverRadius: 5,
          yAxisID: 'y-accuracy'
        },
        {
          label: 'Loss',
          data: props.trainingData.loss || [],
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          borderWidth: 2,
          fill: false,
          tension: 0.4,
          pointRadius: 3,
          pointHoverRadius: 5,
          yAxisID: 'y-loss'
        },
        {
          label: 'CPU Usage (%)',
          data: props.trainingData.cpu || [],
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          borderWidth: 2,
          fill: false,
          tension: 0.4,
          pointRadius: 2,
          pointHoverRadius: 4,
          yAxisID: 'y-resources'
        },
        {
          label: 'Memory Usage (%)',
          data: props.trainingData.memory || [],
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 2,
          fill: false,
          tension: 0.4,
          pointRadius: 2,
          pointHoverRadius: 4,
          yAxisID: 'y-resources'
        }
      ]
      
      // 多轴配置
      baseConfig.options.plugins.legend.display = true
      baseConfig.options.plugins.title.display = true
      baseConfig.options.plugins.title.text = 'Real-time Training Metrics'
      baseConfig.options.plugins.title.color = themeStore.isDark ? '#f9fafb' : '#111827'
      baseConfig.options.plugins.title.font = { size: 16, weight: 'bold' }
      baseConfig.options.plugins.legend.labels = {
        color: themeStore.isDark ? '#d1d5db' : '#374151',
        usePointStyle: true,
        pointStyle: 'circle',
        padding: 20,
        font: { size: 12 }
      }
      
      baseConfig.options.scales = {
        x: baseConfig.options.scales.x,
        'y-accuracy': {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Accuracy (%)',
            color: '#3b82f6',
            font: { size: 12, weight: 'bold' }
          },
          min: 0,
          max: 100,
          grid: {
            color: themeStore.isDark ? '#374151' : '#e5e7eb',
            drawBorder: false
          },
          ticks: {
            color: '#3b82f6',
            callback: function(value) { return value + '%' }
          }
        },
        'y-loss': {
          type: 'linear',
          display: false,
          position: 'right',
          min: 0,
          grid: { drawOnChartArea: false },
          ticks: { color: '#ef4444' }
        },
        'y-resources': {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Resource Usage (%)',
            color: themeStore.isDark ? '#d1d5db' : '#374151',
            font: { size: 12, weight: 'bold' }
          },
          min: 0,
          max: 100,
          grid: { drawOnChartArea: false },
          ticks: {
            color: themeStore.isDark ? '#9ca3af' : '#6b7280',
            callback: function(value) { return value + '%' }
          }
        }
      }
  }

  return baseConfig
}

const initChart = async () => {
  try {
    // Dynamic import Chart.js
    const { default: ChartJS } = await import('chart.js/auto')
    Chart = ChartJS
    
    if (!chartCanvas.value) return
    
    const ctx = chartCanvas.value.getContext('2d')
    const config = getChartConfig()
    
    chart.value = new Chart(ctx, config)
    
  } catch (error) {
    console.error('Failed to initialize chart:', error)
  }
}

const updateChart = () => {
  if (!chart.value) return
  
  // 重新配置图表
  const newConfig = getChartConfig()
  chart.value.data = newConfig.data
  chart.value.options = newConfig.options
  chart.value.update('none')
}

const updateTheme = () => {
  if (!chart.value) return
  updateChart() // 重新生成配置以应用主题
}

const resizeChart = () => {
  if (chart.value) {
    chart.value.resize()
  }
}

// Watch for data changes
watch(() => props.trainingData, updateChart, { deep: true })

// Watch for chart type changes
watch(() => props.chartType, updateChart)

// Watch for theme changes
watch(() => themeStore.isDark, updateTheme)

// Watch for training state changes
watch(() => props.isTraining, (newVal) => {
  if (chart.value) {
    chart.value.options.animation.duration = newVal ? 200 : 800
  }
})

onMounted(async () => {
  await nextTick()
  await initChart()
  
  // Add resize listener
  window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
  if (chart.value) {
    chart.value.destroy()
  }
  window.removeEventListener('resize', resizeChart)
})
</script>

<style scoped>
.local-training-chart {
  position: relative;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 200px;
}

canvas {
  max-width: 100%;
  height: auto;
}

/* Ensure proper sizing */
.chart-container canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100% !important;
  height: 100% !important;
}
</style>