import { ref, onMounted, onUnmounted } from 'vue'

export function useResizeObserver(target) {
  const width = ref(0)
  const height = ref(0)
  
  let resizeObserver = null

  const updateSize = (entries) => {
    if (!entries || !entries.length) return
    
    const entry = entries[0]
    const { width: newWidth, height: newHeight } = entry.contentRect
    
    width.value = newWidth
    height.value = newHeight
  }

  const observe = () => {
    if (!target?.value) return
    
    if ('ResizeObserver' in window) {
      resizeObserver = new ResizeObserver(updateSize)
      resizeObserver.observe(target.value)
      
      // Initial size
      const rect = target.value.getBoundingClientRect()
      width.value = rect.width
      height.value = rect.height
    } else {
      // Fallback for browsers without ResizeObserver
      const handleResize = () => {
        if (target?.value) {
          const rect = target.value.getBoundingClientRect()
          width.value = rect.width
          height.value = rect.height
        }
      }
      
      window.addEventListener('resize', handleResize)
      handleResize() // Initial size
      
      // Store cleanup function
      resizeObserver = () => {
        window.removeEventListener('resize', handleResize)
      }
    }
  }

  const disconnect = () => {
    if (resizeObserver) {
      if (typeof resizeObserver.disconnect === 'function') {
        resizeObserver.disconnect()
      } else {
        resizeObserver() // Fallback cleanup function
      }
      resizeObserver = null
    }
  }

  onMounted(() => {
    observe()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    width,
    height,
    observe,
    disconnect
  }
}