import { ref, computed, nextTick, onMounted, onUnmounted, watch } from 'vue'
import { useThemeStore } from '@/stores/theme'

export const useThemeTransition = (options = {}) => {
  const {
    duration = 800,
    easing = 'cubic-bezier(0.4, 0.0, 0.2, 1)',
    enableRipple = false,
    enableColorInterpolation = true,
    enableParticles = false,
    respectReducedMotion = true
  } = options

  const themeStore = useThemeStore()
  
  // Reactive state
  const isTransitioning = ref(false)
  const transitionProgress = ref(0)
  const rippleElement = ref(null)
  const prefersReducedMotion = ref(false)
  
  // Computed properties
  const shouldAnimate = computed(() => 
    !prefersReducedMotion.value || !respectReducedMotion
  )
  
  const transitionDuration = computed(() => 
    shouldAnimate.value ? duration : 50
  )

  // Check for reduced motion preference
  const checkReducedMotion = () => {
    if (typeof window !== 'undefined') {
      prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    }
  }

  // Color interpolation utility
  const interpolateColor = (color1, color2, factor) => {
    if (!enableColorInterpolation) return color2
    
    const rgb1 = hexToRgb(color1)
    const rgb2 = hexToRgb(color2)
    
    if (!rgb1 || !rgb2) return color2
    
    const r = Math.round(rgb1.r + factor * (rgb2.r - rgb1.r))
    const g = Math.round(rgb1.g + factor * (rgb2.g - rgb1.g))
    const b = Math.round(rgb1.b + factor * (rgb2.b - rgb1.b))
    
    return `rgb(${r}, ${g}, ${b})`
  }

  // Hex to RGB converter
  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null
  }

  // Ripple effect
  const createRipple = async (originElement, targetElement = document.body) => {
    if (!enableRipple || !shouldAnimate.value) return

    const rect = originElement?.getBoundingClientRect()
    if (!rect) return

    const ripple = document.createElement('div')
    ripple.className = 'theme-ripple-effect'
    
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2
    
    // Calculate maximum distance to corner
    const maxDistance = Math.max(
      Math.sqrt(centerX ** 2 + centerY ** 2),
      Math.sqrt((window.innerWidth - centerX) ** 2 + centerY ** 2),
      Math.sqrt(centerX ** 2 + (window.innerHeight - centerY) ** 2),
      Math.sqrt((window.innerWidth - centerX) ** 2 + (window.innerHeight - centerY) ** 2)
    )

    Object.assign(ripple.style, {
      position: 'fixed',
      left: `${centerX}px`,
      top: `${centerY}px`,
      width: '0px',
      height: '0px',
      borderRadius: '50%',
      background: themeStore.isDark 
        ? 'radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%)'
        : 'radial-gradient(circle, rgba(249, 115, 22, 0.3) 0%, transparent 70%)',
      transform: 'translate(-50%, -50%)',
      pointerEvents: 'none',
      zIndex: '9999'
    })

    targetElement.appendChild(ripple)
    rippleElement.value = ripple

    // Animate ripple expansion
    const animation = ripple.animate([
      { 
        width: '0px', 
        height: '0px', 
        opacity: '0.7' 
      },
      { 
        width: `${maxDistance * 2}px`, 
        height: `${maxDistance * 2}px`, 
        opacity: '0' 
      }
    ], {
      duration: transitionDuration.value * 1.5,
      easing,
      fill: 'forwards'
    })

    animation.addEventListener('finish', () => {
      ripple.remove()
      rippleElement.value = null
    })

    return animation
  }

  // Particle system
  const createParticles = async () => {
    if (!enableParticles || !shouldAnimate.value) return

    const particleCount = 20
    const particles = []

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div')
      particle.className = 'theme-particle'
      
      Object.assign(particle.style, {
        position: 'fixed',
        width: '4px',
        height: '4px',
        borderRadius: '50%',
        background: themeStore.isDark ? '#3b82f6' : '#f59e0b',
        pointerEvents: 'none',
        zIndex: '9998',
        left: `${Math.random() * window.innerWidth}px`,
        top: `${Math.random() * window.innerHeight}px`
      })

      document.body.appendChild(particle)
      particles.push(particle)

      // Animate particle
      particle.animate([
        { 
          transform: 'scale(0) rotate(0deg)', 
          opacity: '0' 
        },
        { 
          transform: 'scale(1) rotate(180deg)', 
          opacity: '1' 
        },
        { 
          transform: 'scale(0) rotate(360deg)', 
          opacity: '0' 
        }
      ], {
        duration: transitionDuration.value + Math.random() * 200,
        easing: 'ease-out',
        delay: Math.random() * 100
      }).addEventListener('finish', () => {
        particle.remove()
      })
    }

    return particles
  }

  // Enhanced theme transition
  const transitionTheme = async (originElement) => {
    if (isTransitioning.value) return

    isTransitioning.value = true
    transitionProgress.value = 0

    try {
      // Create visual effects
      const effects = await Promise.all([
        enableRipple ? createRipple(originElement) : null,
        enableParticles ? createParticles() : null
      ])

      // Apply theme change with smooth color transition
      if (enableColorInterpolation && shouldAnimate.value) {
        const steps = 20
        const stepDuration = transitionDuration.value / steps

        for (let i = 0; i <= steps; i++) {
          const progress = i / steps
          transitionProgress.value = progress

          // Apply intermediate colors if needed
          if (i < steps) {
            await new Promise(resolve => setTimeout(resolve, stepDuration))
          }
        }
      }

      // Cleanup
      await nextTick()
      
    } finally {
      isTransitioning.value = false
      transitionProgress.value = 0
    }
  }

  // Color wave effect
  const createColorWave = (direction = 'horizontal') => {
    if (!shouldAnimate.value) return

    const wave = document.createElement('div')
    wave.className = 'theme-color-wave'
    
    Object.assign(wave.style, {
      position: 'fixed',
      top: '0',
      left: '0',
      width: '100vw',
      height: '100vh',
      background: themeStore.isDark 
        ? 'linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent)'
        : 'linear-gradient(90deg, transparent, rgba(249, 115, 22, 0.1), transparent)',
      pointerEvents: 'none',
      zIndex: '9997'
    })

    document.body.appendChild(wave)

    const keyframes = direction === 'horizontal' 
      ? [
          { transform: 'translateX(-100%)' },
          { transform: 'translateX(100vw)' }
        ]
      : [
          { transform: 'translateY(-100%)' },
          { transform: 'translateY(100vh)' }
        ]

    wave.animate(keyframes, {
      duration: transitionDuration.value * 0.8,
      easing: 'ease-in-out'
    }).addEventListener('finish', () => {
      wave.remove()
    })
  }

  // Theme-aware element transitions
  const transitionElement = (element, options = {}) => {
    if (!element || !shouldAnimate.value) return

    const {
      type = 'fade',
      delay = 0,
      customDuration = transitionDuration.value
    } = options

    const animations = {
      fade: [
        { opacity: 0.7, filter: 'brightness(1.2)' },
        { opacity: 1, filter: 'brightness(1)' }
      ],
      scale: [
        { transform: 'scale(0.98)', opacity: 0.8 },
        { transform: 'scale(1)', opacity: 1 }
      ],
      slide: [
        { transform: 'translateY(10px)', opacity: 0.8 },
        { transform: 'translateY(0)', opacity: 1 }
      ]
    }

    return element.animate(animations[type] || animations.fade, {
      duration: customDuration,
      easing,
      delay,
      fill: 'both'
    })
  }

  // Batch element transitions
  const transitionElements = (selector, options = {}) => {
    if (!shouldAnimate.value) return []

    const elements = document.querySelectorAll(selector)
    const animations = []
    
    elements.forEach((element, index) => {
      const animation = transitionElement(element, {
        ...options,
        delay: (options.stagger || 50) * index
      })
      animations.push(animation)
    })

    return animations
  }

  // Setup reduced motion listener
  onMounted(() => {
    checkReducedMotion()
    
    if (typeof window !== 'undefined') {
      const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
      const handler = () => checkReducedMotion()
      
      mediaQuery.addEventListener('change', handler)
      
      onUnmounted(() => {
        mediaQuery.removeEventListener('change', handler)
      })
    }
  })

  // Watch theme changes
  watch(
    () => themeStore.currentTheme,
    (newTheme, oldTheme) => {
      if (oldTheme && newTheme !== oldTheme) {
        // Auto-trigger transitions for global theme changes
        createColorWave()
      }
    }
  )

  return {
    // State
    isTransitioning,
    transitionProgress,
    prefersReducedMotion,
    shouldAnimate,
    transitionDuration,
    
    // Methods
    transitionTheme,
    createRipple,
    createParticles,
    createColorWave,
    transitionElement,
    transitionElements,
    interpolateColor,
    
    // Utilities
    hexToRgb
  }
}

// Color palette transitions
export const useColorTransition = () => {
  const getColorPalette = (isDark) => ({
    primary: isDark ? '#3b82f6' : '#2563eb',
    secondary: isDark ? '#8b5cf6' : '#7c3aed',
    success: isDark ? '#10b981' : '#059669',
    warning: isDark ? '#f59e0b' : '#d97706',
    error: isDark ? '#ef4444' : '#dc2626',
    surface: isDark ? '#1f2937' : '#ffffff',
    background: isDark ? '#111827' : '#f9fafb'
  })

  const transitionColors = (fromDark, toDark, progress) => {
    const fromPalette = getColorPalette(fromDark)
    const toPalette = getColorPalette(toDark)
    const result = {}

    Object.keys(fromPalette).forEach(key => {
      result[key] = interpolateColor(fromPalette[key], toPalette[key], progress)
    })

    return result
  }

  return {
    getColorPalette,
    transitionColors
  }
}

// Reduced motion utilities
export const useReducedMotion = () => {
  const prefersReducedMotion = ref(false)

  const checkReducedMotion = () => {
    if (typeof window !== 'undefined') {
      prefersReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    }
  }

  const safeAnimate = (element, keyframes, options) => {
    if (prefersReducedMotion.value) {
      options = { ...options, duration: 1 }
    }
    return element.animate(keyframes, options)
  }

  const safeCSSTransition = (duration) => 
    prefersReducedMotion.value ? '0.01ms' : `${duration}ms`

  onMounted(() => {
    checkReducedMotion()
    
    if (typeof window !== 'undefined') {
      const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
      mediaQuery.addEventListener('change', checkReducedMotion)
      
      onUnmounted(() => {
        mediaQuery.removeEventListener('change', checkReducedMotion)
      })
    }
  })

  return {
    prefersReducedMotion,
    checkReducedMotion,
    safeAnimate,
    safeCSSTransition
  }
}