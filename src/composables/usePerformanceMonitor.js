import { ref, onMounted, onUnmounted, nextTick } from 'vue'

// Global performance state
const performanceData = ref({
  components: new Map(),
  renders: [],
  memory: [],
  vitals: {},
  errors: []
})

const isMonitoringEnabled = ref(false)
const monitoringConfig = ref({
  enableComponentTracking: true,
  enableMemoryTracking: true,
  enableRenderTracking: true,
  enableVitalsTracking: true,
  maxHistorySize: 1000,
  samplingRate: 1.0,
  trackAnonymous: false
})

// Performance monitoring composable
export const usePerformanceMonitor = () => {
  
  // Component performance tracking
  const trackComponentRender = (componentName, startTime, endTime) => {
    if (!isMonitoringEnabled.value || !monitoringConfig.value.enableComponentTracking) return
    
    const renderTime = endTime - startTime
    const timestamp = Date.now()
    
    if (!performanceData.value.components.has(componentName)) {
      performanceData.value.components.set(componentName, {
        name: componentName,
        totalRenders: 0,
        totalRenderTime: 0,
        averageRenderTime: 0,
        maxRenderTime: 0,
        minRenderTime: Infinity,
        lastRenderTime: 0,
        renderHistory: [],
        memoryUsage: 0,
        errorCount: 0
      })
    }
    
    const component = performanceData.value.components.get(componentName)
    component.totalRenders++
    component.totalRenderTime += renderTime
    component.averageRenderTime = component.totalRenderTime / component.totalRenders
    component.maxRenderTime = Math.max(component.maxRenderTime, renderTime)
    component.minRenderTime = Math.min(component.minRenderTime, renderTime)
    component.lastRenderTime = renderTime
    
    // Keep render history
    component.renderHistory.push({
      timestamp,
      renderTime,
      memoryUsage: getMemoryUsage()
    })
    
    // Limit history size
    if (component.renderHistory.length > monitoringConfig.value.maxHistorySize) {
      component.renderHistory.shift()
    }
    
    // Add to global render history
    if (monitoringConfig.value.enableRenderTracking) {
      performanceData.value.renders.push({
        timestamp,
        componentName,
        renderTime,
        memoryUsage: getMemoryUsage()
      })
      
      // Limit global history
      if (performanceData.value.renders.length > monitoringConfig.value.maxHistorySize) {
        performanceData.value.renders.shift()
      }
    }
  }

  // Memory usage tracking
  const trackMemoryUsage = () => {
    if (!isMonitoringEnabled.value || !monitoringConfig.value.enableMemoryTracking) return
    
    const memory = getMemoryUsage()
    if (memory) {
      performanceData.value.memory.push({
        timestamp: Date.now(),
        ...memory
      })
      
      // Limit memory history
      if (performanceData.value.memory.length > monitoringConfig.value.maxHistorySize) {
        performanceData.value.memory.shift()
      }
    }
  }

  // Web Vitals tracking
  const trackWebVitals = () => {
    if (!isMonitoringEnabled.value || !monitoringConfig.value.enableVitalsTracking) return
    
    // Track Core Web Vitals if available
    if ('web-vitals' in window || window.webVitals) {
      import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
        getCLS((metric) => {
          performanceData.value.vitals.cls = metric
        })
        
        getFID((metric) => {
          performanceData.value.vitals.fid = metric
        })
        
        getFCP((metric) => {
          performanceData.value.vitals.fcp = metric
        })
        
        getLCP((metric) => {
          performanceData.value.vitals.lcp = metric
        })
        
        getTTFB((metric) => {
          performanceData.value.vitals.ttfb = metric
        })
      }).catch(() => {
        // Fallback to basic performance metrics
        trackBasicVitals()
      })
    } else {
      trackBasicVitals()
    }
  }

  // Basic vitals fallback
  const trackBasicVitals = () => {
    if (performance && performance.timing) {
      const timing = performance.timing
      performanceData.value.vitals = {
        domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
        loadComplete: timing.loadEventEnd - timing.navigationStart,
        firstPaint: performance.getEntriesByType('paint')
          .find(entry => entry.name === 'first-paint')?.startTime || 0,
        firstContentfulPaint: performance.getEntriesByType('paint')
          .find(entry => entry.name === 'first-contentful-paint')?.startTime || 0
      }
    }
  }

  // Error tracking
  const trackError = (error, componentName = 'Unknown') => {
    if (!isMonitoringEnabled.value) return
    
    const errorData = {
      timestamp: Date.now(),
      message: error.message || String(error),
      stack: error.stack,
      componentName,
      userAgent: navigator.userAgent,
      url: window.location.href
    }
    
    performanceData.value.errors.push(errorData)
    
    // Limit error history
    if (performanceData.value.errors.length > monitoringConfig.value.maxHistorySize) {
      performanceData.value.errors.shift()
    }
    
    // Update component error count
    if (performanceData.value.components.has(componentName)) {
      performanceData.value.components.get(componentName).errorCount++
    }
  }

  // Get memory usage
  const getMemoryUsage = () => {
    if (performance && performance.memory) {
      return {
        usedJSHeapSize: performance.memory.usedJSHeapSize,
        totalJSHeapSize: performance.memory.totalJSHeapSize,
        jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
      }
    }
    return null
  }

  // Performance analysis
  const analyzePerformance = () => {
    const analysis = {
      summary: {
        totalComponents: performanceData.value.components.size,
        totalRenders: Array.from(performanceData.value.components.values())
          .reduce((sum, comp) => sum + comp.totalRenders, 0),
        averageRenderTime: 0,
        totalErrors: performanceData.value.errors.length,
        memoryTrend: 'stable'
      },
      slowComponents: [],
      errorProneComponents: [],
      memoryLeaks: [],
      recommendations: []
    }
    
    // Calculate average render time
    const components = Array.from(performanceData.value.components.values())
    if (components.length > 0) {
      analysis.summary.averageRenderTime = components
        .reduce((sum, comp) => sum + comp.averageRenderTime, 0) / components.length
    }
    
    // Identify slow components (>16ms average render time)
    analysis.slowComponents = components
      .filter(comp => comp.averageRenderTime > 16)
      .sort((a, b) => b.averageRenderTime - a.averageRenderTime)
      .slice(0, 10)
    
    // Identify error-prone components
    analysis.errorProneComponents = components
      .filter(comp => comp.errorCount > 0)
      .sort((a, b) => b.errorCount - a.errorCount)
      .slice(0, 10)
    
    // Analyze memory trend
    if (performanceData.value.memory.length > 1) {
      const recent = performanceData.value.memory.slice(-10)
      const trend = recent[recent.length - 1].usedJSHeapSize - recent[0].usedJSHeapSize
      analysis.summary.memoryTrend = trend > 0 ? 'increasing' : trend < 0 ? 'decreasing' : 'stable'
    }
    
    // Generate recommendations
    if (analysis.slowComponents.length > 0) {
      analysis.recommendations.push({
        type: 'performance',
        severity: 'high',
        message: `${analysis.slowComponents.length} components are rendering slowly (>16ms)`,
        components: analysis.slowComponents.map(c => c.name)
      })
    }
    
    if (analysis.errorProneComponents.length > 0) {
      analysis.recommendations.push({
        type: 'reliability',
        severity: 'high', 
        message: `${analysis.errorProneComponents.length} components have errors`,
        components: analysis.errorProneComponents.map(c => c.name)
      })
    }
    
    if (analysis.summary.memoryTrend === 'increasing') {
      analysis.recommendations.push({
        type: 'memory',
        severity: 'medium',
        message: 'Memory usage is increasing - potential memory leak',
        action: 'Review component cleanup and event listeners'
      })
    }
    
    return analysis
  }

  // Export performance data
  const exportPerformanceData = (format = 'json') => {
    const data = {
      timestamp: Date.now(),
      config: monitoringConfig.value,
      components: Array.from(performanceData.value.components.entries())
        .map(([name, data]) => ({ name, ...data })),
      renders: performanceData.value.renders,
      memory: performanceData.value.memory,
      vitals: performanceData.value.vitals,
      errors: performanceData.value.errors,
      analysis: analyzePerformance()
    }
    
    switch (format) {
      case 'csv':
        return exportToCSV(data)
      case 'json':
      default:
        return JSON.stringify(data, null, 2)
    }
  }

  // Export to CSV format
  const exportToCSV = (data) => {
    const csvData = []
    
    // Components data
    csvData.push('Component Performance Data')
    csvData.push('Name,Total Renders,Avg Render Time,Max Render Time,Error Count')
    data.components.forEach(comp => {
      csvData.push(`${comp.name},${comp.totalRenders},${comp.averageRenderTime.toFixed(2)},${comp.maxRenderTime.toFixed(2)},${comp.errorCount}`)
    })
    
    csvData.push('')
    csvData.push('Memory Usage Data')
    csvData.push('Timestamp,Used Heap Size,Total Heap Size')
    data.memory.forEach(mem => {
      csvData.push(`${new Date(mem.timestamp).toISOString()},${mem.usedJSHeapSize},${mem.totalJSHeapSize}`)
    })
    
    return csvData.join('\n')
  }

  // Clear performance data
  const clearPerformanceData = () => {
    performanceData.value.components.clear()
    performanceData.value.renders = []
    performanceData.value.memory = []
    performanceData.value.vitals = {}
    performanceData.value.errors = []
  }

  // Configuration
  const enableMonitoring = () => {
    isMonitoringEnabled.value = true
    startMemoryTracking()
    trackWebVitals()
  }

  const disableMonitoring = () => {
    isMonitoringEnabled.value = false
    stopMemoryTracking()
  }

  const updateConfig = (newConfig) => {
    monitoringConfig.value = { ...monitoringConfig.value, ...newConfig }
  }

  // Memory tracking interval
  let memoryTrackingInterval = null
  
  const startMemoryTracking = () => {
    if (memoryTrackingInterval) clearInterval(memoryTrackingInterval)
    
    memoryTrackingInterval = setInterval(() => {
      trackMemoryUsage()
    }, 5000) // Track every 5 seconds
  }
  
  const stopMemoryTracking = () => {
    if (memoryTrackingInterval) {
      clearInterval(memoryTrackingInterval)
      memoryTrackingInterval = null
    }
  }

  return {
    // State
    performanceData: performanceData.value,
    isMonitoringEnabled,
    monitoringConfig,
    
    // Core tracking functions
    trackComponentRender,
    trackMemoryUsage,
    trackWebVitals,
    trackError,
    
    // Analysis
    analyzePerformance,
    exportPerformanceData,
    
    // Control
    enableMonitoring,
    disableMonitoring,
    updateConfig,
    clearPerformanceData
  }
}

// Vue component performance tracking mixin
export const createPerformanceTracker = (componentName) => {
  const { trackComponentRender, trackError } = usePerformanceMonitor()
  let renderStartTime = 0
  
  return {
    beforeCreate() {
      renderStartTime = performance.now()
    },
    
    mounted() {
      const renderEndTime = performance.now()
      trackComponentRender(componentName, renderStartTime, renderEndTime)
    },
    
    updated() {
      const updateStartTime = performance.now()
      nextTick(() => {
        const updateEndTime = performance.now()
        trackComponentRender(`${componentName}:update`, updateStartTime, updateEndTime)
      })
    },
    
    errorCaptured(error) {
      trackError(error, componentName)
    }
  }
}

// Performance monitoring directive
export const vPerformance = {
  beforeMount(el, binding) {
    const componentName = binding.arg || 'anonymous'
    const startTime = performance.now()
    
    el._performanceStartTime = startTime
    el._performanceComponentName = componentName
  },
  
  mounted(el) {
    const endTime = performance.now()
    const { trackComponentRender } = usePerformanceMonitor()
    
    if (el._performanceStartTime && el._performanceComponentName) {
      trackComponentRender(
        el._performanceComponentName,
        el._performanceStartTime,
        endTime
      )
    }
  }
}

// Auto-initialization for development
if (process.env.NODE_ENV === 'development') {
  const { enableMonitoring } = usePerformanceMonitor()
  enableMonitoring()
}