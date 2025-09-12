// Performance optimization utilities

/**
 * Debounce function to limit the rate of function execution
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @param {boolean} immediate - Execute immediately on first call
 */
export function debounce(func, wait, immediate = false) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      timeout = null
      if (!immediate) func(...args)
    }
    const callNow = immediate && !timeout
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
    if (callNow) func(...args)
  }
}

/**
 * Throttle function to limit execution to once per time period
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 */
export function throttle(func, limit) {
  let inThrottle
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

/**
 * Lazy load images with intersection observer
 * @param {string} selector - CSS selector for images to lazy load
 */
export function lazyLoadImages(selector = 'img[data-src]') {
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target
          img.src = img.dataset.src
          img.classList.remove('lazy')
          imageObserver.unobserve(img)
        }
      })
    })

    const images = document.querySelectorAll(selector)
    images.forEach(img => imageObserver.observe(img))
  }
}

/**
 * Preload critical resources
 * @param {Array} resources - Array of resource objects with url and type
 */
export function preloadResources(resources) {
  resources.forEach(resource => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.href = resource.url
    link.as = resource.type
    if (resource.crossorigin) link.crossOrigin = resource.crossorigin
    document.head.appendChild(link)
  })
}

/**
 * Measure and report performance metrics
 */
export function reportWebVitals() {
  // Core Web Vitals
  const observer = new PerformanceObserver((list) => {
    list.getEntries().forEach((entry) => {
      console.log(`${entry.name}:`, entry.value)
      
      // Send to analytics (replace with your analytics service)
      // analytics.track('web-vital', {
      //   name: entry.name,
      //   value: entry.value,
      //   rating: entry.rating
      // })
    })
  })

  // Observe different performance metrics
  try {
    observer.observe({ entryTypes: ['navigation', 'measure', 'paint'] })
  } catch (e) {
    // Fallback for older browsers
    console.warn('Performance Observer not supported')
  }
}

/**
 * Optimize large lists with virtual scrolling helper
 * @param {Array} items - Array of items
 * @param {number} containerHeight - Container height in pixels
 * @param {number} itemHeight - Item height in pixels
 * @param {number} buffer - Buffer size for smooth scrolling
 */
export function getVisibleRange(items, containerHeight, itemHeight, scrollTop, buffer = 5) {
  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - buffer)
  const endIndex = Math.min(
    items.length - 1,
    Math.ceil((scrollTop + containerHeight) / itemHeight) + buffer
  )
  
  return {
    startIndex,
    endIndex,
    visibleItems: items.slice(startIndex, endIndex + 1)
  }
}

/**
 * Memory cleanup utilities
 */
export const memoryUtils = {
  /**
   * Clear unused event listeners
   */
  clearEventListeners(element) {
    if (element && element.cloneNode) {
      const clone = element.cloneNode(true)
      element.parentNode.replaceChild(clone, element)
      return clone
    }
  },

  /**
   * Force garbage collection (development only)
   */
  forceGC() {
    if (window.gc && process.env.NODE_ENV === 'development') {
      window.gc()
    }
  },

  /**
   * Monitor memory usage
   */
  getMemoryInfo() {
    if (performance.memory) {
      return {
        used: Math.round(performance.memory.usedJSHeapSize / 1048576),
        total: Math.round(performance.memory.totalJSHeapSize / 1048576),
        limit: Math.round(performance.memory.jsHeapSizeLimit / 1048576)
      }
    }
    return null
  }
}

/**
 * Animation performance utilities
 */
export const animationUtils = {
  /**
   * Request animation frame with fallback
   */
  raf(callback) {
    return (window.requestAnimationFrame || 
            window.webkitRequestAnimationFrame || 
            window.mozRequestAnimationFrame || 
            function(callback) { setTimeout(callback, 16) })(callback)
  },

  /**
   * Cancel animation frame with fallback
   */
  cancelRaf(id) {
    return (window.cancelAnimationFrame || 
            window.webkitCancelAnimationFrame || 
            window.mozCancelAnimationFrame || 
            clearTimeout)(id)
  },

  /**
   * Check for reduced motion preference
   */
  prefersReducedMotion() {
    return window.matchMedia && 
           window.matchMedia('(prefers-reduced-motion: reduce)').matches
  }
}

/**
 * Bundle size optimization hints
 */
export const bundleOptimization = {
  /**
   * Dynamic import with error handling
   */
  async dynamicImport(modulePath) {
    try {
      const module = await import(/* @vite-ignore */ modulePath)
      return module
    } catch (error) {
      console.error(`Failed to load module: ${modulePath}`, error)
      throw error
    }
  },

  /**
   * Preload module for better UX
   */
  preloadModule(modulePath) {
    const link = document.createElement('link')
    link.rel = 'modulepreload'
    link.href = modulePath
    document.head.appendChild(link)
  }
}