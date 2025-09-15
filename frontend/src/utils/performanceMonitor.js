/**
 * Performance Monitor
 * 监控API调用和页面性能
 */

class PerformanceMonitor {
  constructor() {
    this.apiMetrics = new Map()
    this.pageMetrics = new Map()
    this.enabled = import.meta.env.DEV
  }

  /**
   * 开始监控API调用
   */
  startApiCall(key, method, url) {
    if (!this.enabled) return

    this.apiMetrics.set(key, {
      method,
      url,
      startTime: performance.now(),
      status: 'pending'
    })
  }

  /**
   * 结束API调用监控
   */
  endApiCall(key, success = true, status = 200) {
    if (!this.enabled) return

    const metric = this.apiMetrics.get(key)
    if (metric) {
      metric.endTime = performance.now()
      metric.duration = metric.endTime - metric.startTime
      metric.success = success
      metric.status = status

      // 记录慢请求
      if (metric.duration > 1000) {
        console.warn(`🐌 Slow API call detected:`, {
          url: metric.url,
          duration: `${metric.duration.toFixed(2)}ms`,
          status: metric.status
        })
      }

      // 记录失败请求
      if (!success) {
        console.error(`❌ Failed API call:`, {
          url: metric.url,
          duration: `${metric.duration.toFixed(2)}ms`,
          status: metric.status
        })
      }
    }
  }

  /**
   * 监控页面加载性能
   */
  monitorPageLoad(pageName) {
    if (!this.enabled) return

    const startTime = performance.now()

    return {
      end: () => {
        const endTime = performance.now()
        const duration = endTime - startTime

        this.pageMetrics.set(pageName, {
          startTime,
          endTime,
          duration,
          timestamp: Date.now()
        })

        if (duration > 2000) {
          console.warn(`🐌 Slow page load detected:`, {
            page: pageName,
            duration: `${duration.toFixed(2)}ms`
          })
        }

        console.log(`📊 Page load time for ${pageName}: ${duration.toFixed(2)}ms`)
      }
    }
  }

  /**
   * 获取API性能统计
   */
  getApiStats() {
    if (!this.enabled) return {}

    const calls = Array.from(this.apiMetrics.values())
    const successCalls = calls.filter(c => c.success)
    const failedCalls = calls.filter(c => !c.success)

    return {
      totalCalls: calls.length,
      successRate: `${((successCalls.length / calls.length) * 100).toFixed(1)}%`,
      averageTime: `${(calls.reduce((sum, c) => sum + (c.duration || 0), 0) / calls.length).toFixed(2)}ms`,
      slowCalls: calls.filter(c => (c.duration || 0) > 1000).length,
      failedCalls: failedCalls.length,
      calls: calls.slice(-10) // 最近10次调用
    }
  }

  /**
   * 获取页面性能统计
   */
  getPageStats() {
    if (!this.enabled) return {}

    const pages = Array.from(this.pageMetrics.values())
    
    return {
      totalPages: pages.length,
      averageLoadTime: `${(pages.reduce((sum, p) => sum + p.duration, 0) / pages.length).toFixed(2)}ms`,
      slowPages: pages.filter(p => p.duration > 2000).length,
      pages: Array.from(this.pageMetrics.entries()).slice(-5)
    }
  }

  /**
   * 清除所有统计数据
   */
  clear() {
    this.apiMetrics.clear()
    this.pageMetrics.clear()
  }

  /**
   * 生成性能报告
   */
  generateReport() {
    if (!this.enabled) return 'Performance monitoring disabled in production'

    const apiStats = this.getApiStats()
    const pageStats = this.getPageStats()

    console.group('📊 Performance Report')
    
    console.group('🌐 API Performance')
    console.table({
      'Total Calls': apiStats.totalCalls,
      'Success Rate': apiStats.successRate,
      'Average Time': apiStats.averageTime,
      'Slow Calls': apiStats.slowCalls,
      'Failed Calls': apiStats.failedCalls
    })
    console.groupEnd()

    console.group('📄 Page Performance')
    console.table({
      'Total Pages': pageStats.totalPages,
      'Average Load Time': pageStats.averageLoadTime,
      'Slow Pages': pageStats.slowPages
    })
    console.groupEnd()

    console.groupEnd()

    return { api: apiStats, pages: pageStats }
  }
}

// 创建全局实例
const performanceMonitor = new PerformanceMonitor()

// 在开发环境暴露到window对象
if (import.meta.env.DEV) {
  window.performance = window.performance || {}
  window.performance.monitor = performanceMonitor
  window.performance.report = () => performanceMonitor.generateReport()
  
  console.log('🔧 Performance monitor available:')
  console.log('   • window.performance.report() - 生成性能报告')
  console.log('   • window.performance.monitor - 访问监控实例')
}

export default performanceMonitor