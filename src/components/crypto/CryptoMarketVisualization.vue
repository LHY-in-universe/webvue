<template>
  <div class="crypto-market-visualization">
    <svg 
      ref="marketSvg"
      class="market-svg w-full h-full"
      :width="width"
      :height="height"
      :viewBox="`0 0 ${width} ${height}`"
    >
      <!-- Definitions -->
      <defs>
        <!-- Price Gradient -->
        <linearGradient id="priceGradientUp" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" :style="`stop-color:${theme.success};stop-opacity:0.8`" />
          <stop offset="100%" :style="`stop-color:${theme.success};stop-opacity:0.1`" />
        </linearGradient>
        
        <linearGradient id="priceGradientDown" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" :style="`stop-color:${theme.danger};stop-opacity:0.8`" />
          <stop offset="100%" :style="`stop-color:${theme.danger};stop-opacity:0.1`" />
        </linearGradient>
        
        <!-- Glow filter -->
        <filter id="cryptoGlow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        
        <!-- Market Cap Gradient -->
        <radialGradient id="marketCapGradient" cx="50%" cy="50%" r="50%">
          <stop offset="0%" :style="`stop-color:${theme.primary};stop-opacity:0.6`" />
          <stop offset="100%" :style="`stop-color:${theme.primary};stop-opacity:0.1`" />
        </radialGradient>
      </defs>
      
      <!-- Background -->
      <rect width="100%" height="100%" :fill="themeStore.isDark ? '#1f2937' : '#ffffff'" />
      
      <!-- Grid Lines -->
      <g class="grid-lines" opacity="0.1">
        <defs>
          <pattern id="cryptoGrid" width="50" height="40" patternUnits="userSpaceOnUse">
            <path d="M 50 0 L 0 0 0 40" fill="none" :stroke="themeStore.isDark ? '#ffffff' : '#000000'" stroke-width="0.5"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#cryptoGrid)" />
      </g>
      
      <!-- Market Bubbles -->
      <g class="market-bubbles">
        <g v-for="crypto in positionedCryptos" :key="crypto.symbol" class="crypto-bubble">
          <!-- Bubble -->
          <circle
            :cx="crypto.x"
            :cy="crypto.y"
            :r="crypto.radius"
            :fill="getBubbleColor(crypto)"
            :stroke="getBubbleBorderColor(crypto)"
            stroke-width="2"
            :opacity="crypto.opacity || 0.7"
            class="bubble-circle transition-all duration-300 cursor-pointer"
            @click="selectCrypto(crypto)"
            @mouseover="handleBubbleHover(crypto, $event)"
            @mouseleave="handleBubbleLeave(crypto)"
          >
            <animate
              v-if="crypto.isVolatile"
              attributeName="r"
              :values="`${crypto.radius};${crypto.radius * 1.1};${crypto.radius}`"
              dur="2s"
              repeatCount="indefinite"
            />
          </circle>
          
          <!-- Volume Ring -->
          <circle
            v-if="crypto.volume24h > 1000000"
            :cx="crypto.x"
            :cy="crypto.y"
            :r="crypto.radius + 5"
            fill="none"
            :stroke="theme.secondary"
            stroke-width="2"
            stroke-dasharray="3,2"
            opacity="0.5"
            class="volume-ring"
          >
            <animateTransform
              attributeName="transform"
              type="rotate"
              :values="`0 ${crypto.x} ${crypto.y};360 ${crypto.x} ${crypto.y}`"
              dur="10s"
              repeatCount="indefinite"
            />
          </circle>
          
          <!-- Symbol Text -->
          <text
            :x="crypto.x"
            :y="crypto.y - 2"
            text-anchor="middle"
            :fill="getTextColor(crypto)"
            :font-size="getSymbolFontSize(crypto)"
            font-weight="700"
            class="crypto-symbol"
          >{{ crypto.symbol }}</text>
          
          <!-- Price Text -->
          <text
            :x="crypto.x"
            :y="crypto.y + 10"
            text-anchor="middle"
            :fill="getPriceColor(crypto)"
            font-size="10"
            font-weight="600"
          >${{ formatPrice(crypto.price) }}</text>
          
          <!-- Change Percentage -->
          <text
            :x="crypto.x"
            :y="crypto.y + crypto.radius + 15"
            text-anchor="middle"
            :fill="getChangeColor(crypto.change24h)"
            font-size="9"
            font-weight="500"
          >{{ formatChange(crypto.change24h) }}</text>
          
          <!-- Trend Arrow -->
          <g v-if="Math.abs(crypto.change24h) > 5" class="trend-arrow">
            <path
              v-if="crypto.change24h > 0"
              :d="`M ${crypto.x + crypto.radius - 8} ${crypto.y - crypto.radius + 8} L ${crypto.x + crypto.radius - 4} ${crypto.y - crypto.radius + 4} L ${crypto.x + crypto.radius - 12} ${crypto.y - crypto.radius + 4} Z`"
              :fill="theme.success"
              class="arrow-up"
            />
            <path
              v-else
              :d="`M ${crypto.x + crypto.radius - 8} ${crypto.y - crypto.radius + 12} L ${crypto.x + crypto.radius - 4} ${crypto.y - crypto.radius + 8} L ${crypto.x + crypto.radius - 12} ${crypto.y - crypto.radius + 8} Z`"
              :fill="theme.danger"
              class="arrow-down"
            />
          </g>
        </g>
      </g>
      
      <!-- Connection Lines for Portfolio -->
      <g v-if="showPortfolioConnections" class="portfolio-connections">
        <g v-for="connection in portfolioConnections" :key="connection.id" class="portfolio-line">
          <line
            :x1="connection.from.x"
            :y1="connection.from.y"
            :x2="connection.to.x"
            :y2="connection.to.y"
            :stroke="connection.color"
            :stroke-width="connection.width"
            stroke-dasharray="2,2"
            opacity="0.4"
            class="connection-line"
          />
        </g>
      </g>
      
      <!-- Market Cap Sectors -->
      <g v-if="showMarketCap" class="market-cap-sectors">
        <g v-for="(sector, index) in marketCapSectors" :key="sector.name" class="sector-arc">
          <path
            :d="generateSectorArc(sector, index)"
            :fill="getSectorColor(sector)"
            :stroke="themeStore.isDark ? '#374151' : '#ffffff'"
            stroke-width="2"
            opacity="0.6"
            class="sector-path cursor-pointer"
            @click="selectSector(sector)"
            @mouseover="handleSectorHover(sector, $event)"
            @mouseleave="handleSectorLeave"
          />
          
          <!-- Sector Label -->
          <text
            :x="getSectorLabelPosition(sector, index).x"
            :y="getSectorLabelPosition(sector, index).y"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#ffffff' : '#000000'"
            font-size="12"
            font-weight="600"
          >{{ sector.name }}</text>
          
          <text
            :x="getSectorLabelPosition(sector, index).x"
            :y="getSectorLabelPosition(sector, index).y + 15"
            text-anchor="middle"
            :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
            font-size="10"
          >${{ formatMarketCap(sector.value) }}</text>
        </g>
      </g>
      
      <!-- Market Statistics -->
      <g class="market-stats">
        <rect
          :x="width - 220"
          y="10"
          width="210"
          height="160"
          :fill="themeStore.isDark ? 'rgba(0,0,0,0.8)' : 'rgba(255,255,255,0.9)'"
          stroke="none"
          rx="8"
          class="stats-panel"
        />
        
        <text
          :x="width - 115"
          y="30"
          text-anchor="middle"
          :fill="themeStore.isDark ? '#ffffff' : '#000000'"
          font-size="14"
          font-weight="700"
        >Market Overview</text>
        
        <text
          :x="width - 210"
          y="50"
          :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
          font-size="11"
        >Total Market Cap</text>
        <text
          :x="width - 210"
          y="65"
          :fill="theme.primary"
          font-size="13"
          font-weight="600"
        >${{ formatMarketCap(totalMarketCap) }}</text>
        
        <text
          :x="width - 210"
          y="85"
          :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
          font-size="11"
        >24h Volume</text>
        <text
          :x="width - 210"
          y="100"
          :fill="theme.secondary"
          font-size="13"
          font-weight="600"
        >${{ formatMarketCap(total24hVolume) }}</text>
        
        <text
          :x="width - 210"
          y="120"
          :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
          font-size="11"
        >BTC Dominance</text>
        <text
          :x="width - 210"
          y="135"
          :fill="theme.warning"
          font-size="13"
          font-weight="600"
        >{{ btcDominance }}%</text>
        
        <text
          :x="width - 210"
          y="155"
          :fill="themeStore.isDark ? '#d1d5db' : '#6b7280'"
          font-size="11"
        >Fear & Greed Index</text>
        <text
          :x="width - 210"
          y="170"
          :fill="getFearGreedColor(fearGreedIndex)"
          font-size="13"
          font-weight="600"
        >{{ fearGreedIndex }} - {{ getFearGreedLabel(fearGreedIndex) }}</text>
      </g>
      
      <!-- Price Movement Indicators -->
      <g v-if="showPriceMovements" class="price-movements">
        <g v-for="movement in priceMovements" :key="movement.id" class="price-movement">
          <circle
            :cx="movement.x"
            :cy="movement.y"
            :r="movement.size"
            :fill="movement.color"
            opacity="0.7"
            class="movement-circle"
          >
            <animate
              attributeName="r"
              :values="`0;${movement.size};0`"
              dur="1s"
              begin="0s"
            />
            <animate
              attributeName="opacity"
              values="0;0.7;0"
              dur="1s"
              begin="0s"
            />
          </circle>
        </g>
      </g>
    </svg>
    
    <!-- Tooltip -->
    <Transition name="fade">
      <div
        v-if="tooltip.visible"
        class="absolute bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 px-4 py-3 rounded-lg shadow-xl text-sm pointer-events-none z-50"
        :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
      >
        <div v-if="tooltip.type === 'crypto'">
          <div class="font-bold text-base">{{ tooltip.crypto.name }}</div>
          <div class="text-xs opacity-75">{{ tooltip.crypto.symbol }}</div>
          <div class="mt-2 grid grid-cols-2 gap-2 text-xs">
            <div>
              <span class="opacity-75">Price:</span>
              <span class="font-semibold ml-1">${{ formatPrice(tooltip.crypto.price) }}</span>
            </div>
            <div>
              <span class="opacity-75">24h:</span>
              <span 
                class="font-semibold ml-1"
                :class="tooltip.crypto.change24h > 0 ? 'text-green-400' : 'text-red-400'"
              >
                {{ formatChange(tooltip.crypto.change24h) }}
              </span>
            </div>
            <div>
              <span class="opacity-75">Market Cap:</span>
              <span class="font-semibold ml-1">${{ formatMarketCap(tooltip.crypto.marketCap) }}</span>
            </div>
            <div>
              <span class="opacity-75">Volume:</span>
              <span class="font-semibold ml-1">${{ formatMarketCap(tooltip.crypto.volume24h) }}</span>
            </div>
          </div>
        </div>
        
        <div v-else-if="tooltip.type === 'sector'">
          <div class="font-bold text-base">{{ tooltip.sector.name }} Sector</div>
          <div class="mt-2 text-xs">
            <div><span class="opacity-75">Market Cap:</span> ${{ formatMarketCap(tooltip.sector.value) }}</div>
            <div><span class="opacity-75">Share:</span> {{ tooltip.sector.percentage }}%</div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
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
  cryptos: {
    type: Array,
    default: () => []
  },
  showPortfolioConnections: {
    type: Boolean,
    default: false
  },
  showMarketCap: {
    type: Boolean,
    default: true
  },
  showPriceMovements: {
    type: Boolean,
    default: false
  },
  isRealTime: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['crypto-select', 'sector-select', 'price-alert'])

const themeStore = useThemeStore()
const marketSvg = ref(null)

// Default crypto data
const defaultCryptos = ref([
  {
    symbol: 'BTC',
    name: 'Bitcoin',
    price: 43250.75,
    change24h: 2.45,
    marketCap: 850000000000,
    volume24h: 18500000000,
    rank: 1
  },
  {
    symbol: 'ETH',
    name: 'Ethereum',
    price: 2850.32,
    change24h: -1.23,
    marketCap: 340000000000,
    volume24h: 12300000000,
    rank: 2
  },
  {
    symbol: 'BNB',
    name: 'Binance Coin',
    price: 335.67,
    change24h: 0.87,
    marketCap: 52000000000,
    volume24h: 1800000000,
    rank: 3
  },
  {
    symbol: 'ADA',
    name: 'Cardano',
    price: 0.485,
    change24h: 5.32,
    marketCap: 17000000000,
    volume24h: 850000000,
    rank: 4
  },
  {
    symbol: 'SOL',
    name: 'Solana',
    price: 98.45,
    change24h: -3.21,
    marketCap: 42000000000,
    volume24h: 2100000000,
    rank: 5
  },
  {
    symbol: 'DOT',
    name: 'Polkadot',
    price: 7.23,
    change24h: 1.65,
    marketCap: 8500000000,
    volume24h: 450000000,
    rank: 6
  }
])

// Reactive data
const activeCryptos = computed(() => props.cryptos.length > 0 ? props.cryptos : defaultCryptos.value)
const selectedCrypto = ref(null)
const tooltip = ref({ visible: false, x: 0, y: 0, type: null, crypto: null, sector: null })
const priceMovements = ref([])

// Market statistics
const totalMarketCap = computed(() => 
  activeCryptos.value.reduce((sum, crypto) => sum + crypto.marketCap, 0)
)

const total24hVolume = computed(() => 
  activeCryptos.value.reduce((sum, crypto) => sum + crypto.volume24h, 0)
)

const btcDominance = computed(() => {
  const btc = activeCryptos.value.find(c => c.symbol === 'BTC')
  return btc ? ((btc.marketCap / totalMarketCap.value) * 100).toFixed(1) : 0
})

const fearGreedIndex = ref(65)

// Market cap sectors
const marketCapSectors = computed(() => [
  { name: 'Bitcoin', value: 850000000000, percentage: 42.5 },
  { name: 'Ethereum', value: 340000000000, percentage: 17.0 },
  { name: 'Alt Coins', value: 610000000000, percentage: 30.5 },
  { name: 'Stable Coins', value: 200000000000, percentage: 10.0 }
])

// Position cryptos in bubbles
const positionedCryptos = computed(() => {
  const centerX = props.width / 2
  const centerY = props.height / 2
  const maxRadius = Math.min(props.width, props.height) / 3
  
  return activeCryptos.value.map((crypto, index) => {
    const angle = (index / activeCryptos.value.length) * 2 * Math.PI
    const distance = maxRadius * (0.3 + (crypto.rank - 1) * 0.1)
    
    // Calculate bubble size based on market cap
    const maxMarketCap = Math.max(...activeCryptos.value.map(c => c.marketCap))
    const radius = Math.max(15, Math.min(50, (crypto.marketCap / maxMarketCap) * 50 + 10))
    
    return {
      ...crypto,
      x: centerX + Math.cos(angle) * distance,
      y: centerY + Math.sin(angle) * distance,
      radius,
      isVolatile: Math.abs(crypto.change24h) > 5
    }
  })
})

// Portfolio connections
const portfolioConnections = ref([])

// Styling functions
const getBubbleColor = (crypto) => {
  if (crypto.change24h > 0) return `url(#priceGradientUp)`
  if (crypto.change24h < 0) return `url(#priceGradientDown)`
  return props.theme.primary
}

const getBubbleBorderColor = (crypto) => {
  if (crypto.symbol === selectedCrypto.value?.symbol) return props.theme.warning
  if (crypto.change24h > 5) return props.theme.success
  if (crypto.change24h < -5) return props.theme.danger
  return themeStore.isDark ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.3)'
}

const getTextColor = (crypto) => {
  return themeStore.isDark ? '#ffffff' : '#000000'
}

const getPriceColor = (crypto) => {
  return themeStore.isDark ? '#d1d5db' : '#6b7280'
}

const getChangeColor = (change) => {
  if (change > 0) return props.theme.success
  if (change < 0) return props.theme.danger
  return themeStore.isDark ? '#d1d5db' : '#6b7280'
}

const getSymbolFontSize = (crypto) => {
  return Math.max(10, Math.min(16, crypto.radius / 3))
}

const getSectorColor = (sector) => {
  const colors = [props.theme.primary, props.theme.secondary, props.theme.warning, props.theme.danger]
  return colors[marketCapSectors.value.indexOf(sector) % colors.length]
}

const getFearGreedColor = (index) => {
  if (index < 25) return props.theme.danger
  if (index < 50) return props.theme.warning
  if (index < 75) return props.theme.secondary
  return props.theme.success
}

// Utility functions
const formatPrice = (price) => {
  if (price < 1) return price.toFixed(4)
  if (price < 10) return price.toFixed(2)
  return price.toLocaleString(undefined, { maximumFractionDigits: 0 })
}

const formatChange = (change) => {
  const sign = change >= 0 ? '+' : ''
  return `${sign}${change.toFixed(2)}%`
}

const formatMarketCap = (value) => {
  if (value >= 1e12) return `${(value / 1e12).toFixed(1)}T`
  if (value >= 1e9) return `${(value / 1e9).toFixed(1)}B`
  if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`
  return value.toLocaleString()
}

const getFearGreedLabel = (index) => {
  if (index < 25) return 'Extreme Fear'
  if (index < 50) return 'Fear'
  if (index < 75) return 'Greed'
  return 'Extreme Greed'
}

// Sector arc generation
const generateSectorArc = (sector, index) => {
  const centerX = props.width - 100
  const centerY = props.height - 100
  const radius = 60
  const startAngle = marketCapSectors.value.slice(0, index).reduce((sum, s) => sum + (s.percentage / 100) * 2 * Math.PI, 0)
  const endAngle = startAngle + (sector.percentage / 100) * 2 * Math.PI
  
  const x1 = centerX + radius * Math.cos(startAngle)
  const y1 = centerY + radius * Math.sin(startAngle)
  const x2 = centerX + radius * Math.cos(endAngle)
  const y2 = centerY + radius * Math.sin(endAngle)
  
  const largeArcFlag = endAngle - startAngle <= Math.PI ? '0' : '1'
  
  return `M ${centerX} ${centerY} L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2} Z`
}

const getSectorLabelPosition = (sector, index) => {
  const centerX = props.width - 100
  const centerY = props.height - 100
  const radius = 40
  const startAngle = marketCapSectors.value.slice(0, index).reduce((sum, s) => sum + (s.percentage / 100) * 2 * Math.PI, 0)
  const midAngle = startAngle + (sector.percentage / 100) * Math.PI
  
  return {
    x: centerX + radius * Math.cos(midAngle),
    y: centerY + radius * Math.sin(midAngle)
  }
}

// Event handlers
const selectCrypto = (crypto) => {
  selectedCrypto.value = crypto
  emit('crypto-select', crypto)
}

const selectSector = (sector) => {
  emit('sector-select', sector)
}

const handleBubbleHover = (crypto, event) => {
  const rect = marketSvg.value.getBoundingClientRect()
  tooltip.value = {
    visible: true,
    x: event.clientX - rect.left + 10,
    y: event.clientY - rect.top - 10,
    type: 'crypto',
    crypto
  }
}

const handleBubbleLeave = (crypto) => {
  tooltip.value.visible = false
}

const handleSectorHover = (sector, event) => {
  const rect = marketSvg.value.getBoundingClientRect()
  tooltip.value = {
    visible: true,
    x: event.clientX - rect.left + 10,
    y: event.clientY - rect.top - 10,
    type: 'sector',
    sector
  }
}

const handleSectorLeave = () => {
  tooltip.value.visible = false
}

// Price movement animation
const animatePriceMovement = (crypto, isPositive) => {
  const movement = {
    id: Date.now() + Math.random(),
    x: crypto.x,
    y: crypto.y,
    size: 20,
    color: isPositive ? props.theme.success : props.theme.danger
  }
  
  priceMovements.value.push(movement)
  
  setTimeout(() => {
    const index = priceMovements.value.findIndex(m => m.id === movement.id)
    if (index > -1) {
      priceMovements.value.splice(index, 1)
    }
  }, 1000)
}

// Real-time updates
let updateInterval = null

const startRealTimeUpdates = () => {
  if (updateInterval) clearInterval(updateInterval)
  
  updateInterval = setInterval(() => {
    if (props.isRealTime) {
      defaultCryptos.value.forEach(crypto => {
        const oldPrice = crypto.price
        const change = (Math.random() - 0.5) * crypto.price * 0.02 // 2% max change
        crypto.price += change
        crypto.change24h += (Math.random() - 0.5) * 2 // Random 24h change adjustment
        
        if (Math.abs(change / oldPrice) > 0.005 && props.showPriceMovements) {
          const positioned = positionedCryptos.value.find(p => p.symbol === crypto.symbol)
          if (positioned) {
            animatePriceMovement(positioned, change > 0)
          }
        }
      })
      
      // Update Fear & Greed Index
      fearGreedIndex.value = Math.max(0, Math.min(100, fearGreedIndex.value + (Math.random() - 0.5) * 5))
    }
  }, 2000)
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
.crypto-market-visualization {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  background: var(--color-background);
  border-radius: 0.5rem;
}

.bubble-circle {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.bubble-circle:hover {
  filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.2));
  transform: scale(1.05);
}

.crypto-symbol {
  pointer-events: none;
  user-select: none;
}

.sector-path {
  transition: opacity 0.2s ease;
}

.sector-path:hover {
  opacity: 0.8;
}

.volume-ring {
  pointer-events: none;
}

.stats-panel {
  backdrop-filter: blur(8px);
}

.connection-line {
  transition: stroke-width 0.2s ease;
}

.connection-line:hover {
  stroke-width: 3px;
}

.trend-arrow {
  pointer-events: none;
}

.movement-circle {
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