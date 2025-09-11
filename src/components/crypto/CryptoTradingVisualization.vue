<template>
  <div class="crypto-trading-visualization">
    <svg 
      ref="tradingSvg"
      class="trading-svg w-full h-full"
      :width="width"
      :height="height"
      :viewBox="`0 0 ${width} ${height}`"
    >
      <!-- Definitions -->
      <defs>
        <!-- Candlestick Gradients -->
        <linearGradient id="bullishGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" :style="`stop-color:${theme.success};stop-opacity:1`" />
          <stop offset="100%" :style="`stop-color:${theme.success};stop-opacity:0.7`" />
        </linearGradient>
        
        <linearGradient id="bearishGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" :style="`stop-color:${theme.danger};stop-opacity:0.7`" />
          <stop offset="100%" :style="`stop-color:${theme.danger};stop-opacity:1`" />
        </linearGradient>
        
        <!-- Volume Gradient -->
        <linearGradient id="volumeGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" :style="`stop-color:${theme.primary};stop-opacity:0.8`" />
          <stop offset="100%" :style="`stop-color:${theme.primary};stop-opacity:0.2`" />
        </linearGradient>
        
        <!-- Orderbook Gradients -->
        <linearGradient id="bidsGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :style="`stop-color:${theme.success};stop-opacity:0.1`" />
          <stop offset="100%" :style="`stop-color:${theme.success};stop-opacity:0.5`" />
        </linearGradient>
        
        <linearGradient id="asksGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" :style="`stop-color:${theme.danger};stop-opacity:0.5`" />
          <stop offset="100%" :style="`stop-color:${theme.danger};stop-opacity:0.1`" />
        </linearGradient>
      </defs>
      
      <!-- Background -->
      <rect width="100%" height="100%" :fill="themeStore.isDark ? '#1f2937' : '#ffffff'" />
      
      <!-- Price Chart Area -->
      <g class="price-chart-area">
        <!-- Price Grid -->
        <g class="price-grid" opacity="0.1">
          <g v-for="(gridLine, index) in priceGridLines" :key="`price-grid-${index}`">
            <line
              x1="50"
              :y1="gridLine.y"
              :x2="chartWidth"
              :y2="gridLine.y"
              :stroke="themeStore.isDark ? '#ffffff' : '#000000'"
              stroke-width="0.5"
            />
            <text
              x="40"
              :y="gridLine.y + 4"
              :fill="themeStore.isDark ? '#9ca3af' : '#6b7280'"
              font-size="10"
              text-anchor="end"
            >${{ gridLine.price.toFixed(2) }}</text>
          </g>
        </g>
        
        <!-- Time Grid -->
        <g class="time-grid" opacity="0.1">
          <g v-for="(gridLine, index) in timeGridLines" :key="`time-grid-${index}`">
            <line
              :x1="gridLine.x"
              y1="50"
              :x2="gridLine.x"
              :y2="chartHeight - 100"
              :stroke="themeStore.isDark ? '#ffffff' : '#000000'"
              stroke-width="0.5"
            />
            <text
              :x="gridLine.x"
              :y="chartHeight - 85"
              :fill="themeStore.isDark ? '#9ca3af' : '#6b7280'"
              font-size="10"
              text-anchor="middle"
            >{{ formatTime(gridLine.timestamp) }}</text>
          </g>
        </g>
        
        <!-- Candlesticks -->
        <g class="candlesticks">
          <g v-for="(candle, index) in visibleCandles" :key="`candle-${index}`" class="candlestick">
            <!-- Wick -->
            <line
              :x1="candle.x"
              :y1="candle.highY"
              :x2="candle.x"
              :y2="candle.lowY"
              :stroke="candle.isBullish ? theme.success : theme.danger"
              stroke-width="1"
              class="wick"
            />
            
            <!-- Body -->
            <rect
              :x="candle.x - candleWidth/2"
              :y="Math.min(candle.openY, candle.closeY)"
              :width="candleWidth"
              :height="Math.abs(candle.closeY - candle.openY) || 1"
              :fill="candle.isBullish ? 'url(#bullishGradient)' : 'url(#bearishGradient)'"
              :stroke="candle.isBullish ? theme.success : theme.danger"
              stroke-width="1"
              class="candle-body cursor-pointer"
              @mouseover="handleCandleHover(candle, $event)"
              @mouseleave="hideTooltip"
              @click="selectCandle(candle)"
            />
          </g>
        </g>
        
        <!-- Moving Averages -->
        <g v-if="showMovingAverages" class="moving-averages">
          <path
            v-for="(ma, index) in movingAverages"
            :key="`ma-${ma.period}`"
            :d="ma.path"
            fill="none"
            :stroke="ma.color"
            :stroke-width="ma.width"
            opacity="0.8"
            class="moving-average-line"
          />
        </g>
        
        <!-- Support and Resistance Lines -->
        <g v-if="showSupportResistance" class="support-resistance">
          <g v-for="level in supportResistanceLevels" :key="`sr-${level.price}`">
            <line
              x1="50"
              :y1="priceToY(level.price)"
              :x2="chartWidth"
              :y2="priceToY(level.price)"
              :stroke="level.type === 'support' ? theme.success : theme.danger"
              stroke-width="2"
              stroke-dasharray="5,5"
              opacity="0.6"
              class="sr-line"
            />
            <text
              :x="chartWidth - 10"
              :y="priceToY(level.price) - 5"
              :fill="level.type === 'support' ? theme.success : theme.danger"
              font-size="11"
              text-anchor="end"
              font-weight="600"
            >{{ level.type.toUpperCase() }} ${{ level.price.toFixed(2) }}</text>
          </g>
        </g>
      </g>
      
      <!-- Volume Chart -->
      <g class="volume-chart" :transform="`translate(0, ${chartHeight - 80})`">
        <g v-for="(volume, index) in volumeData" :key="`volume-${index}`">
          <rect
            :x="volume.x - candleWidth/2"
            :y="volume.height"
            :width="candleWidth"
            :height="60 - volume.height"
            fill="url(#volumeGradient)"
            opacity="0.6"
            class="volume-bar"
          />
        </g>
        
        <!-- Volume Scale -->
        <text
          x="10"
          y="15"
          :fill="themeStore.isDark ? '#9ca3af' : '#6b7280'"
          font-size="10"
        >Volume</text>
      </g>
      
      <!-- Order Book -->
      <g v-if="showOrderBook" class="order-book" :transform="`translate(${chartWidth + 20}, 50)`">
        <rect
          x="0"
          y="0"
          width="150"
          :height="chartHeight - 150"
          :fill="themeStore.isDark ? 'rgba(0,0,0,0.3)' : 'rgba(255,255,255,0.8)'"
          stroke="rgba(255,255,255,0.1)"
          rx="4"
        />
        
        <text
          x="75"
          y="20"
          text-anchor="middle"
          :fill="themeStore.isDark ? '#ffffff' : '#000000'"
          font-size="12"
          font-weight="600"
        >Order Book</text>
        
        <!-- Asks (Sell Orders) -->
        <g class="asks" :transform="`translate(0, 30)`">
          <g v-for="(ask, index) in orderbookAsks" :key="`ask-${index}`">
            <rect
              x="0"
              :y="index * 15"
              :width="(ask.size / maxOrderSize) * 140"
              height="12"
              fill="url(#asksGradient)"
              opacity="0.7"
            />
            <text
              x="5"
              :y="index * 15 + 9"
              :fill="theme.danger"
              font-size="9"
              font-weight="500"
            >${{ ask.price.toFixed(2) }}</text>
            <text
              x="135"
              :y="index * 15 + 9"
              :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
              font-size="9"
              text-anchor="end"
            >{{ ask.size.toFixed(3) }}</text>
          </g>
        </g>
        
        <!-- Spread -->
        <g class="spread" :transform="`translate(0, ${30 + orderbookAsks.length * 15})`">
          <rect
            x="0"
            y="0"
            width="140"
            height="20"
            :fill="themeStore.isDark ? 'rgba(59, 130, 246, 0.1)' : 'rgba(59, 130, 246, 0.05)'"
            stroke="rgba(59, 130, 246, 0.3)"
            rx="2"
          />
          <text
            x="70"
            y="13"
            text-anchor="middle"
            :fill="theme.primary"
            font-size="10"
            font-weight="600"
          >Spread: ${{ currentSpread.toFixed(2) }}</text>
        </g>
        
        <!-- Bids (Buy Orders) -->
        <g class="bids" :transform="`translate(0, ${50 + orderbookAsks.length * 15})`">
          <g v-for="(bid, index) in orderbookBids" :key="`bid-${index}`">
            <rect
              x="0"
              :y="index * 15"
              :width="(bid.size / maxOrderSize) * 140"
              height="12"
              fill="url(#bidsGradient)"
              opacity="0.7"
            />
            <text
              x="5"
              :y="index * 15 + 9"
              :fill="theme.success"
              font-size="9"
              font-weight="500"
            >${{ bid.price.toFixed(2) }}</text>
            <text
              x="135"
              :y="index * 15 + 9"
              :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
              font-size="9"
              text-anchor="end"
            >{{ bid.size.toFixed(3) }}</text>
          </g>
        </g>
      </g>
      
      <!-- Trade Flow Animation -->
      <g v-if="showTradeFlow" class="trade-flow">
        <g v-for="trade in activeTradeFlows" :key="trade.id" class="trade-animation">
          <circle
            :r="trade.size"
            :fill="trade.isBuy ? theme.success : theme.danger"
            opacity="0.8"
            class="trade-dot"
          >
            <animateMotion
              :dur="trade.duration"
              begin="0s"
            >
              <mpath :href="`#trade-path-${trade.id}`" />
            </animateMotion>
            <animate
              attributeName="opacity"
              values="0;0.8;0"
              :dur="trade.duration"
              begin="0s"
            />
          </circle>
          
          <!-- Trade path -->
          <path
            :id="`trade-path-${trade.id}`"
            :d="trade.path"
            fill="none"
            stroke="none"
            opacity="0"
          />
        </g>
      </g>
      
      <!-- Current Price Line -->
      <g class="current-price">
        <line
          x1="50"
          :y1="currentPriceY"
          :x2="chartWidth"
          :y2="currentPriceY"
          :stroke="theme.primary"
          stroke-width="2"
          stroke-dasharray="3,3"
          opacity="0.8"
          class="current-price-line"
        >
          <animate
            attributeName="opacity"
            values="0.8;0.4;0.8"
            dur="2s"
            repeatCount="indefinite"
          />
        </line>
        
        <rect
          :x="chartWidth - 80"
          :y="currentPriceY - 10"
          width="70"
          height="20"
          :fill="theme.primary"
          rx="4"
          opacity="0.9"
        />
        
        <text
          :x="chartWidth - 45"
          :y="currentPriceY + 4"
          text-anchor="middle"
          fill="white"
          font-size="11"
          font-weight="600"
        >${{ currentPrice.toFixed(2) }}</text>
      </g>
      
      <!-- Trading Statistics -->
      <g class="trading-stats">
        <rect
          x="10"
          y="10"
          width="200"
          height="100"
          :fill="themeStore.isDark ? 'rgba(0,0,0,0.8)' : 'rgba(255,255,255,0.9)'"
          stroke="none"
          rx="8"
        />
        
        <text x="20" y="30" :fill="themeStore.isDark ? '#ffffff' : '#000000'" font-size="12" font-weight="600">
          {{ selectedPair }} Statistics
        </text>
        
        <text x="20" y="50" :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'" font-size="10">
          24h High: <tspan :fill="theme.success" font-weight="600">${{ high24h.toFixed(2) }}</tspan>
        </text>
        
        <text x="20" y="65" :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'" font-size="10">
          24h Low: <tspan :fill="theme.danger" font-weight="600">${{ low24h.toFixed(2) }}</tspan>
        </text>
        
        <text x="20" y="80" :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'" font-size="10">
          Volume: <tspan :fill="theme.primary" font-weight="600">{{ formatVolume(volume24h) }}</tspan>
        </text>
        
        <text x="20" y="95" :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'" font-size="10">
          Change: <tspan :fill="getChangeColor(change24h)" font-weight="600">{{ formatChange(change24h) }}</tspan>
        </text>
      </g>
    </svg>
    
    <!-- Tooltip -->
    <Transition name="fade">
      <div
        v-if="tooltip.visible"
        class="absolute bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-3 py-2 rounded-lg shadow-lg text-xs pointer-events-none z-10"
        :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
      >
        <div class="grid grid-cols-2 gap-2">
          <div><span class="opacity-75">Open:</span> ${{ tooltip.data.open?.toFixed(2) }}</div>
          <div><span class="opacity-75">High:</span> ${{ tooltip.data.high?.toFixed(2) }}</div>
          <div><span class="opacity-75">Low:</span> ${{ tooltip.data.low?.toFixed(2) }}</div>
          <div><span class="opacity-75">Close:</span> ${{ tooltip.data.close?.toFixed(2) }}</div>
          <div class="col-span-2"><span class="opacity-75">Volume:</span> {{ formatVolume(tooltip.data.volume) }}</div>
        </div>
        <div class="text-center mt-1 opacity-75">{{ formatTime(tooltip.data.timestamp) }}</div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useThemeStore } from '@/stores/theme'

const props = defineProps({
  width: {
    type: Number,
    default: 800
  },
  height: {
    type: Number,
    default: 500
  },
  theme: {
    type: Object,
    default: () => ({
      primary: '#3b82f6',
      secondary: '#10b981',
      warning: '#f59e0b',
      danger: '#ef4444',
      success: '#22c55e'
    })
  },
  selectedPair: {
    type: String,
    default: 'BTC/USDT'
  },
  candleData: {
    type: Array,
    default: () => []
  },
  showMovingAverages: {
    type: Boolean,
    default: true
  },
  showSupportResistance: {
    type: Boolean,
    default: true
  },
  showOrderBook: {
    type: Boolean,
    default: true
  },
  showTradeFlow: {
    type: Boolean,
    default: false
  },
  isRealTime: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['candle-select', 'trade-execute', 'price-alert'])

const themeStore = useThemeStore()
const tradingSvg = ref(null)

// Chart dimensions
const chartWidth = computed(() => props.showOrderBook ? props.width - 180 : props.width - 40)
const chartHeight = computed(() => props.height - 20)
const candleWidth = computed(() => Math.max(2, Math.min(10, chartWidth.value / Math.max(defaultCandleData.value.length, 1))))

// Sample data
const defaultCandleData = ref([
  { timestamp: Date.now() - 86400000, open: 43250, high: 43450, low: 43100, close: 43320, volume: 1250 },
  { timestamp: Date.now() - 82800000, open: 43320, high: 43520, low: 43280, close: 43480, volume: 1680 },
  { timestamp: Date.now() - 79200000, open: 43480, high: 43650, low: 43420, close: 43580, volume: 1420 },
  { timestamp: Date.now() - 75600000, open: 43580, high: 43680, low: 43480, close: 43520, volume: 1180 },
  { timestamp: Date.now() - 72000000, open: 43520, high: 43720, low: 43480, close: 43680, volume: 1890 },
  { timestamp: Date.now() - 68400000, open: 43680, high: 43750, low: 43580, close: 43620, volume: 1340 },
  { timestamp: Date.now() - 64800000, open: 43620, high: 43820, low: 43520, close: 43780, volume: 2120 },
  { timestamp: Date.now() - 61200000, open: 43780, high: 43880, low: 43720, close: 43850, volume: 1780 }
])

// Reactive data
const activeCandleData = computed(() => props.candleData.length > 0 ? props.candleData : defaultCandleData.value)
const tooltip = ref({ visible: false, x: 0, y: 0, data: {} })
const selectedCandle = ref(null)

// Market data
const currentPrice = ref(43850)
const high24h = ref(43880)
const low24h = ref(43100)
const volume24h = ref(12500)
const change24h = ref(2.45)

// Order book data
const orderbookBids = ref([
  { price: 43840, size: 2.45 },
  { price: 43835, size: 1.87 },
  { price: 43830, size: 3.21 },
  { price: 43825, size: 0.95 },
  { price: 43820, size: 2.12 }
])

const orderbookAsks = ref([
  { price: 43855, size: 1.23 },
  { price: 43860, size: 2.78 },
  { price: 43865, size: 1.56 },
  { price: 43870, size: 3.45 },
  { price: 43875, size: 0.89 }
])

const currentSpread = computed(() => 
  orderbookAsks.value[0].price - orderbookBids.value[0].price
)

const maxOrderSize = computed(() => 
  Math.max(...orderbookBids.value.map(b => b.size), ...orderbookAsks.value.map(a => a.size))
)

// Trading flows
const activeTradeFlows = ref([])

// Price calculations
const priceRange = computed(() => {
  if (activeCandleData.value.length === 0) return { min: 0, max: 1 }
  
  let min = Infinity
  let max = -Infinity
  
  activeCandleData.value.forEach(candle => {
    min = Math.min(min, candle.low)
    max = Math.max(max, candle.high)
  })
  
  const padding = (max - min) * 0.1
  return { min: min - padding, max: max + padding }
})

const priceToY = (price) => {
  const { min, max } = priceRange.value
  const range = max - min
  return 50 + ((max - price) / range) * (chartHeight.value - 150)
}

const currentPriceY = computed(() => priceToY(currentPrice.value))

// Grid lines
const priceGridLines = computed(() => {
  const { min, max } = priceRange.value
  const lines = []
  const step = (max - min) / 6
  
  for (let i = 0; i <= 6; i++) {
    const price = min + i * step
    lines.push({
      price,
      y: priceToY(price)
    })
  }
  
  return lines
})

const timeGridLines = computed(() => {
  const lines = []
  const step = chartWidth.value / 6
  
  for (let i = 0; i <= 6; i++) {
    const x = 50 + i * step
    const dataIndex = Math.floor((activeCandleData.value.length - 1) * i / 6)
    const timestamp = activeCandleData.value[dataIndex]?.timestamp || Date.now()
    
    lines.push({ x, timestamp })
  }
  
  return lines
})

// Visible candles with positions
const visibleCandles = computed(() => {
  const candles = []
  const stepX = (chartWidth.value - 50) / activeCandleData.value.length
  
  activeCandleData.value.forEach((candle, index) => {
    const x = 50 + (index + 0.5) * stepX
    const isBullish = candle.close >= candle.open
    
    candles.push({
      ...candle,
      x,
      openY: priceToY(candle.open),
      closeY: priceToY(candle.close),
      highY: priceToY(candle.high),
      lowY: priceToY(candle.low),
      isBullish
    })
  })
  
  return candles
})

// Volume data
const volumeData = computed(() => {
  const maxVolume = Math.max(...activeCandleData.value.map(c => c.volume))
  const stepX = (chartWidth.value - 50) / activeCandleData.value.length
  
  return activeCandleData.value.map((candle, index) => ({
    x: 50 + (index + 0.5) * stepX,
    height: 60 - (candle.volume / maxVolume) * 50
  }))
})

// Moving averages
const movingAverages = computed(() => {
  if (!props.showMovingAverages || activeCandleData.value.length < 20) return []
  
  const mas = [
    { period: 20, color: props.theme.primary, width: 1 },
    { period: 50, color: props.theme.secondary, width: 1.5 }
  ]
  
  return mas.map(ma => {
    const points = []
    const stepX = (chartWidth.value - 50) / activeCandleData.value.length
    
    for (let i = ma.period - 1; i < activeCandleData.value.length; i++) {
      const sum = activeCandleData.value.slice(i - ma.period + 1, i + 1)
        .reduce((acc, candle) => acc + candle.close, 0)
      const avg = sum / ma.period
      const x = 50 + (i + 0.5) * stepX
      const y = priceToY(avg)
      points.push(`${i === ma.period - 1 ? 'M' : 'L'} ${x} ${y}`)
    }
    
    return {
      ...ma,
      path: points.join(' ')
    }
  })
})

// Support and resistance levels
const supportResistanceLevels = computed(() => {
  if (!props.showSupportResistance) return []
  
  const prices = activeCandleData.value.map(c => [c.high, c.low]).flat()
  prices.sort((a, b) => b - a)
  
  return [
    { type: 'resistance', price: prices[Math.floor(prices.length * 0.1)] },
    { type: 'support', price: prices[Math.floor(prices.length * 0.9)] }
  ]
})

// Utility functions
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const formatVolume = (volume) => {
  if (volume >= 1000000) return `${(volume / 1000000).toFixed(1)}M`
  if (volume >= 1000) return `${(volume / 1000).toFixed(1)}K`
  return volume.toString()
}

const formatChange = (change) => {
  const sign = change >= 0 ? '+' : ''
  return `${sign}${change.toFixed(2)}%`
}

const getChangeColor = (change) => {
  return change >= 0 ? props.theme.success : props.theme.danger
}

// Event handlers
const handleCandleHover = (candle, event) => {
  const rect = tradingSvg.value.getBoundingClientRect()
  tooltip.value = {
    visible: true,
    x: event.clientX - rect.left + 10,
    y: event.clientY - rect.top - 10,
    data: candle
  }
}

const hideTooltip = () => {
  tooltip.value.visible = false
}

const selectCandle = (candle) => {
  selectedCandle.value = candle
  emit('candle-select', candle)
}

// Trade flow animation
const animateTradeFlow = (trade) => {
  const startX = props.showOrderBook ? chartWidth.value + 20 : chartWidth.value
  const endX = trade.price ? priceToY(trade.price) : currentPriceY.value
  
  const tradeFlow = {
    id: Date.now() + Math.random(),
    size: Math.max(3, Math.min(8, trade.size * 2)),
    isBuy: trade.side === 'buy',
    duration: '2s',
    path: `M ${startX} ${endX} L ${trade.x || currentPriceY.value} ${endX}`
  }
  
  activeTradeFlows.value.push(tradeFlow)
  
  setTimeout(() => {
    const index = activeTradeFlows.value.findIndex(t => t.id === tradeFlow.id)
    if (index > -1) {
      activeTradeFlows.value.splice(index, 1)
    }
  }, 2000)
}

// Real-time updates
let updateInterval = null

const startRealTimeUpdates = () => {
  if (updateInterval) clearInterval(updateInterval)
  
  updateInterval = setInterval(() => {
    if (props.isRealTime) {
      // Update current price
      const change = (Math.random() - 0.5) * currentPrice.value * 0.002
      currentPrice.value += change
      
      // Update 24h stats
      high24h.value = Math.max(high24h.value, currentPrice.value)
      low24h.value = Math.min(low24h.value, currentPrice.value)
      
      // Update order book
      orderbookBids.value.forEach(bid => {
        bid.price += (Math.random() - 0.5) * 2
        bid.size += (Math.random() - 0.5) * 0.5
        bid.size = Math.max(0.1, bid.size)
      })
      
      orderbookAsks.value.forEach(ask => {
        ask.price += (Math.random() - 0.5) * 2
        ask.size += (Math.random() - 0.5) * 0.5
        ask.size = Math.max(0.1, ask.size)
      })
      
      // Simulate trades
      if (Math.random() > 0.7 && props.showTradeFlow) {
        animateTradeFlow({
          price: currentPrice.value,
          size: Math.random() * 5,
          side: Math.random() > 0.5 ? 'buy' : 'sell'
        })
      }
    }
  }, 1000)
}

// Lifecycle
onMounted(() => {
  if (props.isRealTime) {
    startRealTimeUpdates()
  }
})

onUnmounted(() => {
  if (updateInterval) {
    clearInterval(updateInterval)
  }
})

// Watchers
watch(() => props.isRealTime, (newValue) => {
  if (newValue) {
    startRealTimeUpdates()
  } else if (updateInterval) {
    clearInterval(updateInterval)
    updateInterval = null
  }
})
</script>

<style scoped>
.crypto-trading-visualization {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  background: var(--color-background);
  border-radius: 0.5rem;
}

.candle-body {
  transition: opacity 0.2s ease;
}

.candle-body:hover {
  opacity: 0.8;
}

.moving-average-line {
  pointer-events: none;
}

.sr-line {
  pointer-events: none;
}

.current-price-line {
  pointer-events: none;
}

.volume-bar {
  transition: opacity 0.2s ease;
}

.volume-bar:hover {
  opacity: 0.9;
}

.trade-dot {
  pointer-events: none;
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