<template>
  <div class="base-chart" :style="{ height: chartHeight }">
    <div v-if="title" class="chart-header mb-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ title }}</h3>
      <p v-if="description" class="text-sm text-gray-600 dark:text-gray-400">{{ description }}</p>
    </div>
    
    <div class="chart-container relative" :style="{ height: containerHeight }">
      <svg 
        ref="chartSvg"
        class="w-full h-full"
        :viewBox="`0 0 ${viewBoxWidth} ${viewBoxHeight}`"
        preserveAspectRatio="xMidYMid meet"
      >
        <!-- Chart Definitions -->
        <defs>
          <!-- Grid Pattern -->
          <pattern id="chartGrid" width="40" height="30" patternUnits="userSpaceOnUse">
            <path 
              d="M 40 0 L 0 0 0 30" 
              fill="none" 
              :stroke="themeStore.isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'" 
              stroke-width="0.5"
            />
          </pattern>
          
          <!-- Gradients for different chart types -->
          <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" :style="`stop-color:${theme.primary};stop-opacity:0.3`" />
            <stop offset="100%" :style="`stop-color:${theme.primary};stop-opacity:0.05`" />
          </linearGradient>
          
          <linearGradient id="barGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" :style="`stop-color:${theme.primary};stop-opacity:1`" />
            <stop offset="100%" :style="`stop-color:${theme.primary};stop-opacity:0.8`" />
          </linearGradient>
        </defs>
        
        <!-- Background -->
        <rect 
          width="100%" 
          height="100%" 
          :fill="themeStore.isDark ? '#1f2937' : '#ffffff'"
          stroke="none"
        />
        
        <!-- Grid (if enabled) -->
        <rect 
          v-if="showGrid" 
          width="100%" 
          height="100%" 
          fill="url(#chartGrid)" 
        />
        
        <!-- Chart Content -->
        <g class="chart-content" :transform="`translate(${margin.left}, ${margin.top})`">
          <!-- Y Axis -->
          <g class="y-axis" v-if="showYAxis">
            <line 
              x1="0" 
              y1="0" 
              x2="0" 
              :y2="plotHeight" 
              :stroke="axisColor" 
              stroke-width="1"
            />
            <g v-for="(tick, index) in yTicks" :key="`y-${index}`">
              <line 
                x1="-5" 
                :y1="tick.position" 
                x2="0" 
                :y2="tick.position" 
                :stroke="axisColor" 
                stroke-width="1"
              />
              <text 
                x="-10" 
                :y="tick.position + 4" 
                :fill="textColor" 
                text-anchor="end" 
                font-size="12"
              >
                {{ formatValue(tick.value) }}
              </text>
            </g>
          </g>
          
          <!-- X Axis -->
          <g class="x-axis" v-if="showXAxis">
            <line 
              x1="0" 
              :y1="plotHeight" 
              :x2="plotWidth" 
              :y2="plotHeight" 
              :stroke="axisColor" 
              stroke-width="1"
            />
            <g v-for="(tick, index) in xTicks" :key="`x-${index}`">
              <line 
                :x1="tick.position" 
                :y1="plotHeight" 
                :x2="tick.position" 
                :y2="plotHeight + 5" 
                :stroke="axisColor" 
                stroke-width="1"
              />
              <text 
                :x="tick.position" 
                :y="plotHeight + 18" 
                :fill="textColor" 
                text-anchor="middle" 
                font-size="12"
              >
                {{ formatLabel(tick.label) }}
              </text>
            </g>
          </g>
          
          <!-- Chart Type Specific Content -->
          <slot 
            name="chart-content" 
            :plotWidth="plotWidth" 
            :plotHeight="plotHeight"
            :xScale="xScale"
            :yScale="yScale"
            :theme="theme"
          />
          
          <!-- Line Chart -->
          <g v-if="type === 'line'" class="line-chart">
            <g v-for="(series, seriesIndex) in dataSeries" :key="`line-${seriesIndex}`">
              <path 
                :d="getLinePath(series.data)"
                fill="none"
                :stroke="series.color || theme.primary"
                :stroke-width="series.strokeWidth || 2"
                stroke-linecap="round"
                stroke-linejoin="round"
                :class="{ 'animate-draw': animate }"
              />
              
              <!-- Data Points -->
              <g v-if="showDataPoints">
                <circle
                  v-for="(point, pointIndex) in series.data"
                  :key="`point-${seriesIndex}-${pointIndex}`"
                  :cx="xScale(point.x)"
                  :cy="yScale(point.y)"
                  :r="series.pointRadius || 3"
                  :fill="series.color || theme.primary"
                  :stroke="themeStore.isDark ? '#1f2937' : '#ffffff'"
                  stroke-width="2"
                  class="chart-point"
                  @mouseover="handlePointHover(point, series, $event)"
                  @mouseleave="hideTooltip"
                />
              </g>
            </g>
          </g>
          
          <!-- Area Chart -->
          <g v-if="type === 'area'" class="area-chart">
            <g v-for="(series, seriesIndex) in dataSeries" :key="`area-${seriesIndex}`">
              <path 
                :d="getAreaPath(series.data)"
                fill="url(#areaGradient)"
                :stroke="series.color || theme.primary"
                stroke-width="2"
                :class="{ 'animate-draw': animate }"
              />
            </g>
          </g>
          
          <!-- Bar Chart -->
          <g v-if="type === 'bar'" class="bar-chart">
            <g v-for="(series, seriesIndex) in dataSeries" :key="`bar-${seriesIndex}`">
              <rect
                v-for="(point, pointIndex) in series.data"
                :key="`bar-${seriesIndex}-${pointIndex}`"
                :x="xScale(point.x) - (barWidth / 2)"
                :y="yScale(point.y)"
                :width="barWidth"
                :height="plotHeight - yScale(point.y)"
                :fill="series.color || theme.primary"
                :class="{ 'animate-grow': animate }"
                @mouseover="handlePointHover(point, series, $event)"
                @mouseleave="hideTooltip"
              />
            </g>
          </g>
        </g>
        
        <!-- Legend -->
        <g v-if="showLegend && dataSeries.length > 1" class="legend" :transform="`translate(${margin.left}, ${viewBoxHeight - 20})`">
          <g v-for="(series, index) in dataSeries" :key="`legend-${index}`" :transform="`translate(${index * 100}, 0)`">
            <rect 
              x="0" 
              y="-8" 
              width="12" 
              height="8" 
              :fill="series.color || theme.primary"
            />
            <text 
              x="16" 
              y="0" 
              :fill="textColor" 
              font-size="12"
            >
              {{ series.name }}
            </text>
          </g>
        </g>
      </svg>
      
      <!-- Tooltip -->
      <Transition name="fade">
        <div
          v-if="tooltip.visible"
          class="absolute bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-3 py-2 rounded-lg shadow-lg text-sm pointer-events-none z-10"
          :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
        >
          <div class="font-semibold">{{ tooltip.label }}</div>
          <div>{{ tooltip.value }}</div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'

const props = defineProps({
  type: {
    type: String,
    default: 'line',
    validator: value => ['line', 'area', 'bar', 'pie'].includes(value)
  },
  data: {
    type: Array,
    default: () => []
  },
  title: String,
  description: String,
  width: {
    type: Number,
    default: 400
  },
  height: {
    type: Number,
    default: 200
  },
  theme: {
    type: Object,
    default: () => ({
      primary: '#3b82f6',
      secondary: '#10b981',
      accent: '#8b5cf6',
      warning: '#f59e0b',
      danger: '#ef4444'
    })
  },
  margin: {
    type: Object,
    default: () => ({ top: 20, right: 20, bottom: 40, left: 50 })
  },
  showGrid: {
    type: Boolean,
    default: true
  },
  showXAxis: {
    type: Boolean,
    default: true
  },
  showYAxis: {
    type: Boolean,
    default: true
  },
  showLegend: {
    type: Boolean,
    default: false
  },
  showDataPoints: {
    type: Boolean,
    default: false
  },
  animate: {
    type: Boolean,
    default: true
  },
  formatValue: {
    type: Function,
    default: (value) => value.toString()
  },
  formatLabel: {
    type: Function,
    default: (label) => label.toString()
  }
})

const emit = defineEmits(['point-click', 'point-hover', 'point-leave'])

const themeStore = useThemeStore()
const chartSvg = ref(null)

// Chart dimensions
const viewBoxWidth = ref(props.width)
const viewBoxHeight = ref(props.height)
const chartHeight = computed(() => `${props.height}px`)
const containerHeight = computed(() => `${props.height - (props.title ? 60 : 0)}px`)

const plotWidth = computed(() => viewBoxWidth.value - props.margin.left - props.margin.right)
const plotHeight = computed(() => viewBoxHeight.value - props.margin.top - props.margin.bottom - (props.showLegend ? 30 : 0))

// Colors
const axisColor = computed(() => themeStore.isDark ? '#6b7280' : '#9ca3af')
const textColor = computed(() => themeStore.isDark ? '#d1d5db' : '#374151')

// Data processing
const dataSeries = computed(() => {
  if (!Array.isArray(props.data)) return []
  
  // If data is simple array of objects, wrap in series
  if (props.data.length > 0 && !props.data[0].name) {
    return [{
      name: 'Series 1',
      data: props.data,
      color: props.theme.primary
    }]
  }
  
  return props.data
})

const dataExtent = computed(() => {
  if (dataSeries.value.length === 0) return { xMin: 0, xMax: 1, yMin: 0, yMax: 1 }
  
  let xMin = Infinity, xMax = -Infinity, yMin = Infinity, yMax = -Infinity
  
  dataSeries.value.forEach(series => {
    series.data.forEach(point => {
      xMin = Math.min(xMin, point.x)
      xMax = Math.max(xMax, point.x)
      yMin = Math.min(yMin, point.y)
      yMax = Math.max(yMax, point.y)
    })
  })
  
  return { xMin, xMax, yMin, yMax }
})

// Scales
const xScale = computed(() => {
  const { xMin, xMax } = dataExtent.value
  const range = xMax - xMin || 1
  return (value) => ((value - xMin) / range) * plotWidth.value
})

const yScale = computed(() => {
  const { yMin, yMax } = dataExtent.value
  const range = yMax - yMin || 1
  return (value) => plotHeight.value - ((value - yMin) / range) * plotHeight.value
})

// Ticks
const xTicks = computed(() => {
  const { xMin, xMax } = dataExtent.value
  const tickCount = 6
  const step = (xMax - xMin) / (tickCount - 1)
  
  return Array.from({ length: tickCount }, (_, i) => {
    const value = xMin + i * step
    return {
      value,
      position: xScale.value(value),
      label: value
    }
  })
})

const yTicks = computed(() => {
  const { yMin, yMax } = dataExtent.value
  const tickCount = 5
  const step = (yMax - yMin) / (tickCount - 1)
  
  return Array.from({ length: tickCount }, (_, i) => {
    const value = yMin + i * step
    return {
      value,
      position: yScale.value(value)
    }
  })
})

// Bar chart specific
const barWidth = computed(() => {
  if (props.type !== 'bar' || dataSeries.value.length === 0) return 0
  return Math.max(10, plotWidth.value / dataSeries.value[0].data.length * 0.8)
})

// Tooltip
const tooltip = ref({
  visible: false,
  x: 0,
  y: 0,
  label: '',
  value: ''
})

// Path generators
const getLinePath = (data) => {
  if (data.length === 0) return ''
  
  let path = `M ${xScale.value(data[0].x)} ${yScale.value(data[0].y)}`
  
  for (let i = 1; i < data.length; i++) {
    path += ` L ${xScale.value(data[i].x)} ${yScale.value(data[i].y)}`
  }
  
  return path
}

const getAreaPath = (data) => {
  if (data.length === 0) return ''
  
  let path = `M ${xScale.value(data[0].x)} ${plotHeight.value}`
  path += ` L ${xScale.value(data[0].x)} ${yScale.value(data[0].y)}`
  
  for (let i = 1; i < data.length; i++) {
    path += ` L ${xScale.value(data[i].x)} ${yScale.value(data[i].y)}`
  }
  
  path += ` L ${xScale.value(data[data.length - 1].x)} ${plotHeight.value} Z`
  
  return path
}

// Event handlers
const handlePointHover = (point, series, event) => {
  const rect = chartSvg.value.getBoundingClientRect()
  tooltip.value = {
    visible: true,
    x: event.clientX - rect.left + 10,
    y: event.clientY - rect.top - 10,
    label: props.formatLabel(point.x),
    value: props.formatValue(point.y)
  }
  emit('point-hover', point, series)
}

const hideTooltip = () => {
  tooltip.value.visible = false
  emit('point-leave')
}
</script>

<style scoped>
.base-chart {
  width: 100%;
}

.chart-container {
  background: var(--color-background);
  border-radius: 0.5rem;
}

.chart-point {
  cursor: pointer;
  transition: r 0.2s ease;
}

.chart-point:hover {
  r: 5;
}

.animate-draw {
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: drawPath 1s ease-out forwards;
}

.animate-grow {
  transform-origin: bottom;
  animation: growBar 0.8s ease-out forwards;
}

@keyframes drawPath {
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes growBar {
  from {
    transform: scaleY(0);
  }
  to {
    transform: scaleY(1);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>