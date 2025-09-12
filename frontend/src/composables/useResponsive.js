import { ref, computed, onMounted, onUnmounted } from 'vue'

/**
 * Composable for responsive design utilities
 * Provides breakpoint detection, mobile/touch detection, and responsive helpers
 */
export function useResponsive() {
  // Breakpoint definitions (matching Tailwind CSS)
  const breakpoints = {
    sm: 640,
    md: 768,
    lg: 1024,
    xl: 1280,
    '2xl': 1536
  }

  // Reactive state
  const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)
  const windowHeight = ref(typeof window !== 'undefined' ? window.innerHeight : 768)
  
  // Device detection
  const isMobile = computed(() => windowWidth.value < breakpoints.md)
  const isTablet = computed(() => windowWidth.value >= breakpoints.md && windowWidth.value < breakpoints.lg)
  const isDesktop = computed(() => windowWidth.value >= breakpoints.lg)
  
  // Specific breakpoint checks
  const isSmall = computed(() => windowWidth.value < breakpoints.sm)
  const isMedium = computed(() => windowWidth.value >= breakpoints.sm && windowWidth.value < breakpoints.md)
  const isLarge = computed(() => windowWidth.value >= breakpoints.md && windowWidth.value < breakpoints.lg)
  const isXLarge = computed(() => windowWidth.value >= breakpoints.lg && windowWidth.value < breakpoints.xl)
  const is2XLarge = computed(() => windowWidth.value >= breakpoints.xl)

  // Touch device detection
  const isTouchDevice = computed(() => {
    if (typeof window === 'undefined') return false
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0
  })

  // Orientation
  const isPortrait = computed(() => windowHeight.value > windowWidth.value)
  const isLandscape = computed(() => windowWidth.value > windowHeight.value)

  // Responsive grid columns
  const gridCols = computed(() => {
    if (windowWidth.value >= breakpoints.xl) return 4
    if (windowWidth.value >= breakpoints.lg) return 3
    if (windowWidth.value >= breakpoints.md) return 2
    return 1
  })

  // Container padding based on screen size
  const containerPadding = computed(() => {
    if (windowWidth.value >= breakpoints.xl) return 'px-8'
    if (windowWidth.value >= breakpoints.lg) return 'px-6'
    if (windowWidth.value >= breakpoints.md) return 'px-4'
    return 'px-2'
  })

  // Font size scaling
  const fontScale = computed(() => {
    if (windowWidth.value < breakpoints.sm) return 0.9
    if (windowWidth.value < breakpoints.md) return 0.95
    return 1
  })

  // Chart dimensions based on screen size
  const getChartDimensions = (aspectRatio = 16/9) => {
    const maxWidth = windowWidth.value >= breakpoints.lg ? 800 : windowWidth.value - 32
    const width = Math.min(maxWidth, windowWidth.value * 0.9)
    const height = width / aspectRatio
    
    return { width, height }
  }

  // Modal size based on screen size
  const getModalSize = (preferredSize = 'md') => {
    if (windowWidth.value < breakpoints.md) return 'full'
    if (windowWidth.value < breakpoints.lg) return 'lg'
    return preferredSize
  }

  // Table display mode
  const tableDisplayMode = computed(() => {
    if (windowWidth.value < breakpoints.sm) return 'stacked'
    if (windowWidth.value < breakpoints.md) return 'scrollable'
    return 'full'
  })

  // Navigation layout
  const navLayout = computed(() => {
    if (windowWidth.value < breakpoints.lg) return 'mobile'
    return 'desktop'
  })

  // Update dimensions
  const updateDimensions = () => {
    windowWidth.value = window.innerWidth
    windowHeight.value = window.innerHeight
  }

  // Debounced resize handler
  let resizeTimeout
  const handleResize = () => {
    clearTimeout(resizeTimeout)
    resizeTimeout = setTimeout(updateDimensions, 100)
  }

  // Lifecycle
  onMounted(() => {
    if (typeof window !== 'undefined') {
      window.addEventListener('resize', handleResize, { passive: true })
      updateDimensions()
    }
  })

  onUnmounted(() => {
    if (typeof window !== 'undefined') {
      window.removeEventListener('resize', handleResize)
    }
    if (resizeTimeout) {
      clearTimeout(resizeTimeout)
    }
  })

  // Helper functions
  const getResponsiveValue = (values) => {
    const { xs, sm, md, lg, xl, '2xl': xxl } = values
    
    if (windowWidth.value >= breakpoints['2xl'] && xxl !== undefined) return xxl
    if (windowWidth.value >= breakpoints.xl && xl !== undefined) return xl
    if (windowWidth.value >= breakpoints.lg && lg !== undefined) return lg
    if (windowWidth.value >= breakpoints.md && md !== undefined) return md
    if (windowWidth.value >= breakpoints.sm && sm !== undefined) return sm
    return xs
  }

  const getResponsiveClasses = (classes) => {
    return getResponsiveValue(classes) || ''
  }

  // Touch gesture helpers
  const isSwiping = ref(false)
  const swipeDirection = ref(null)
  
  const handleTouchStart = (startX, startY) => {
    let startTouchX = startX
    let startTouchY = startY
    
    return {
      onTouchMove: (currentX, currentY) => {
        const deltaX = currentX - startTouchX
        const deltaY = currentY - startTouchY
        
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
          isSwiping.value = true
          swipeDirection.value = deltaX > 0 ? 'right' : 'left'
        } else if (Math.abs(deltaY) > 50) {
          isSwiping.value = true
          swipeDirection.value = deltaY > 0 ? 'down' : 'up'
        }
      },
      onTouchEnd: () => {
        const direction = swipeDirection.value
        isSwiping.value = false
        swipeDirection.value = null
        return direction
      }
    }
  }

  return {
    // Dimensions
    windowWidth,
    windowHeight,
    
    // Device type
    isMobile,
    isTablet,
    isDesktop,
    isTouchDevice,
    
    // Breakpoints
    isSmall,
    isMedium, 
    isLarge,
    isXLarge,
    is2XLarge,
    
    // Orientation
    isPortrait,
    isLandscape,
    
    // Utilities
    gridCols,
    containerPadding,
    fontScale,
    tableDisplayMode,
    navLayout,
    
    // Functions
    getChartDimensions,
    getModalSize,
    getResponsiveValue,
    getResponsiveClasses,
    handleTouchStart,
    
    // Swipe state
    isSwiping,
    swipeDirection
  }
}

/**
 * Composable for mobile-specific interactions
 */
export function useMobileInteractions() {
  const { isTouchDevice } = useResponsive()
  
  // Long press detection
  const useLongPress = (callback, delay = 500) => {
    let timeout
    
    const start = (event) => {
      timeout = setTimeout(() => {
        callback(event)
      }, delay)
    }
    
    const cancel = () => {
      if (timeout) {
        clearTimeout(timeout)
        timeout = null
      }
    }
    
    return {
      onTouchStart: start,
      onTouchEnd: cancel,
      onTouchMove: cancel,
      onMouseDown: isTouchDevice.value ? null : start,
      onMouseUp: isTouchDevice.value ? null : cancel,
      onMouseLeave: isTouchDevice.value ? null : cancel
    }
  }
  
  // Double tap detection
  const useDoubleTap = (callback, delay = 300) => {
    let lastTap = 0
    
    const handleTap = (event) => {
      const now = Date.now()
      if (now - lastTap < delay) {
        callback(event)
      }
      lastTap = now
    }
    
    return {
      onTouchEnd: handleTap,
      onClick: isTouchDevice.value ? null : handleTap
    }
  }
  
  return {
    useLongPress,
    useDoubleTap
  }
}