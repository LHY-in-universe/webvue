import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useResponsive } from './useResponsive'

export function useAnimations() {
  const { isMobile } = useResponsive()
  
  const prefersReducedMotion = ref(false)
  const animationsEnabled = ref(true)
  
  // Check for reduced motion preference
  const checkReducedMotion = () => {
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
      prefersReducedMotion.value = mediaQuery.matches
      return mediaQuery
    }
    return null
  }
  
  // Animation presets with mobile optimizations
  const animationPresets = {
    // Fade animations
    fade: {
      duration: 300,
      easing: 'ease',
      mobile: { duration: 250 }
    },
    
    // Slide animations
    slideUp: {
      duration: 300,
      easing: 'cubic-bezier(0.25, 0.8, 0.25, 1)',
      transform: 'translateY(20px)',
      mobile: { duration: 250, transform: 'translateY(15px)' }
    },
    
    slideDown: {
      duration: 300,
      easing: 'cubic-bezier(0.25, 0.8, 0.25, 1)',
      transform: 'translateY(-20px)',
      mobile: { duration: 250, transform: 'translateY(-15px)' }
    },
    
    slideLeft: {
      duration: 300,
      easing: 'cubic-bezier(0.25, 0.8, 0.25, 1)',
      transform: 'translateX(20px)',
      mobile: { duration: 250, transform: 'translateX(15px)' }
    },
    
    slideRight: {
      duration: 300,
      easing: 'cubic-bezier(0.25, 0.8, 0.25, 1)',
      transform: 'translateX(-20px)',
      mobile: { duration: 250, transform: 'translateX(-15px)' }
    },
    
    // Scale animations
    scale: {
      duration: 300,
      easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      transform: 'scale(0.8)',
      mobile: { duration: 250, transform: 'scale(0.9)' }
    },
    
    scaleFade: {
      duration: 300,
      easing: 'ease-out',
      transform: 'scale(0.95)',
      mobile: { duration: 250 }
    },
    
    // Bounce animation
    bounce: {
      duration: 600,
      easing: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
      transform: 'scale(0.3)',
      mobile: { duration: 300, easing: 'ease-out' } // Simplified on mobile
    },
    
    // Zoom animation
    zoom: {
      duration: 300,
      easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
      transform: 'scale(0.9)',
      mobile: { duration: 250 }
    },
    
    // Flip animation
    flip: {
      duration: 400,
      easing: 'cubic-bezier(0.23, 1, 0.32, 1)',
      transform: 'rotateY(-90deg)',
      mobile: { duration: 300, transform: 'scale(0.9)' } // Simplified on mobile
    },
    
    // Rotate animation
    rotate: {
      duration: 300,
      easing: 'ease-out',
      transform: 'rotate(-10deg) scale(0.9)',
      mobile: { duration: 250, transform: 'scale(0.9)' }
    }
  }
  
  // Get optimized animation settings
  const getAnimationConfig = (presetName, customConfig = {}) => {
    const preset = animationPresets[presetName]
    if (!preset) return customConfig
    
    const baseConfig = { ...preset }
    
    // Apply mobile optimizations
    if (isMobile.value && preset.mobile) {
      Object.assign(baseConfig, preset.mobile)
    }
    
    // Apply custom overrides
    return { ...baseConfig, ...customConfig }
  }
  
  // Check if animations should be enabled
  const shouldAnimate = computed(() => {
    return animationsEnabled.value && !prefersReducedMotion.value
  })
  
  // Create CSS transition string
  const createTransition = (properties, duration = 300, easing = 'ease') => {
    if (!shouldAnimate.value) return 'none'
    
    const props = Array.isArray(properties) ? properties : [properties]
    return props.map(prop => `${prop} ${duration}ms ${easing}`).join(', ')
  }
  
  // Animate element with GSAP-like API
  const animate = (element, to = {}, options = {}) => {
    if (!element || !shouldAnimate.value) {
      return Promise.resolve()
    }
    
    const {
      duration = 300,
      delay = 0,
      easing = 'ease',
      from = {},
      onStart,
      onComplete,
      onUpdate
    } = options
    
    return new Promise((resolve) => {
      // Set initial values
      Object.entries(from).forEach(([property, value]) => {
        element.style[property] = value
      })
      
      // Call onStart callback
      onStart && onStart()
      
      // Create transition
      const properties = Object.keys(to)
      element.style.transition = createTransition(properties, duration, easing)
      
      // Apply final values after delay
      const applyAnimation = () => {
        Object.entries(to).forEach(([property, value]) => {
          element.style[property] = value
        })
        
        // Call onUpdate callback
        onUpdate && onUpdate()
      }
      
      if (delay > 0) {
        setTimeout(applyAnimation, delay)
      } else {
        applyAnimation()
      }
      
      // Resolve promise when animation completes
      const handleTransitionEnd = () => {
        element.removeEventListener('transitionend', handleTransitionEnd)
        onComplete && onComplete()
        resolve()
      }
      
      element.addEventListener('transitionend', handleTransitionEnd)
      
      // Fallback timeout
      setTimeout(() => {
        element.removeEventListener('transitionend', handleTransitionEnd)
        resolve()
      }, duration + delay + 50)
    })
  }
  
  // Stagger animations for multiple elements
  const staggerAnimate = (elements, to = {}, options = {}) => {
    const {
      stagger = 100,
      ...animateOptions
    } = options
    
    const promises = Array.from(elements).map((element, index) => {
      return animate(element, to, {
        ...animateOptions,
        delay: (animateOptions.delay || 0) + (index * stagger)
      })
    })
    
    return Promise.all(promises)
  }
  
  // Slide animation utilities
  const slideIn = (element, direction = 'up', options = {}) => {
    const transforms = {
      up: 'translateY(20px)',
      down: 'translateY(-20px)',
      left: 'translateX(20px)',
      right: 'translateX(-20px)'
    }
    
    return animate(element, {
      opacity: '1',
      transform: 'translateX(0) translateY(0)'
    }, {
      ...options,
      from: {
        opacity: '0',
        transform: transforms[direction] || transforms.up
      }
    })
  }
  
  const slideOut = (element, direction = 'up', options = {}) => {
    const transforms = {
      up: 'translateY(-20px)',
      down: 'translateY(20px)',
      left: 'translateX(-20px)',
      right: 'translateX(20px)'
    }
    
    return animate(element, {
      opacity: '0',
      transform: transforms[direction] || transforms.up
    }, options)
  }
  
  // Fade animation utilities
  const fadeIn = (element, options = {}) => {
    return animate(element, { opacity: '1' }, {
      ...options,
      from: { opacity: '0' }
    })
  }
  
  const fadeOut = (element, options = {}) => {
    return animate(element, { opacity: '0' }, options)
  }
  
  // Scale animation utilities
  const scaleIn = (element, options = {}) => {
    return animate(element, {
      opacity: '1',
      transform: 'scale(1)'
    }, {
      ...options,
      from: {
        opacity: '0',
        transform: 'scale(0.8)'
      }
    })
  }
  
  const scaleOut = (element, options = {}) => {
    return animate(element, {
      opacity: '0',
      transform: 'scale(0.8)'
    }, options)
  }
  
  // Intersection Observer for scroll animations
  const observeIntersection = (element, callback, options = {}) => {
    if (!window.IntersectionObserver) {
      callback(element, true)
      return null
    }
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        callback(entry.target, entry.isIntersecting, entry)
      })
    }, {
      threshold: 0.1,
      rootMargin: '50px',
      ...options
    })
    
    observer.observe(element)
    return observer
  }
  
  // Animate on scroll
  const animateOnScroll = (element, animationType = 'slideUp', options = {}) => {
    if (!shouldAnimate.value) return null
    
    const {
      threshold = 0.1,
      rootMargin = '50px',
      once = true,
      ...animateOptions
    } = options
    
    let hasAnimated = false
    
    return observeIntersection(element, (el, isIntersecting) => {
      if (isIntersecting && (!hasAnimated || !once)) {
        if (animationType === 'slideUp') {
          slideIn(el, 'up', animateOptions)
        } else if (animationType === 'slideDown') {
          slideIn(el, 'down', animateOptions)
        } else if (animationType === 'slideLeft') {
          slideIn(el, 'left', animateOptions)
        } else if (animationType === 'slideRight') {
          slideIn(el, 'right', animateOptions)
        } else if (animationType === 'fadeIn') {
          fadeIn(el, animateOptions)
        } else if (animationType === 'scaleIn') {
          scaleIn(el, animateOptions)
        }
        
        hasAnimated = true
      }
    }, { threshold, rootMargin })
  }
  
  // Performance utilities
  const optimizeForAnimation = (element) => {
    if (element) {
      element.style.willChange = 'transform, opacity'
      element.style.transform = 'translateZ(0)' // Force GPU acceleration
    }
  }
  
  const cleanupAnimation = (element) => {
    if (element) {
      element.style.willChange = 'auto'
      element.style.transition = ''
    }
  }
  
  // Spring animation (simplified)
  const spring = (element, to = {}, config = {}) => {
    const {
      tension = 280,
      friction = 120,
      mass = 1
    } = config
    
    // Calculate spring duration (simplified)
    const duration = Math.sqrt(mass / tension) * friction
    
    return animate(element, to, {
      duration,
      easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)'
    })
  }
  
  // Lifecycle management
  onMounted(() => {
    const mediaQuery = checkReducedMotion()
    
    if (mediaQuery) {
      const handleChange = (e) => {
        prefersReducedMotion.value = e.matches
      }
      
      mediaQuery.addListener(handleChange)
      
      onUnmounted(() => {
        mediaQuery.removeListener(handleChange)
      })
    }
  })
  
  return {
    // State
    prefersReducedMotion,
    animationsEnabled,
    shouldAnimate,
    
    // Configuration
    animationPresets,
    getAnimationConfig,
    createTransition,
    
    // Core animation functions
    animate,
    staggerAnimate,
    
    // Animation utilities
    slideIn,
    slideOut,
    fadeIn,
    fadeOut,
    scaleIn,
    scaleOut,
    spring,
    
    // Scroll animations
    observeIntersection,
    animateOnScroll,
    
    // Performance utilities
    optimizeForAnimation,
    cleanupAnimation
  }
}

// Animation directive for easy usage in templates
export const vAnimate = {
  mounted(el, binding) {
    const { useAnimations } = require('./useAnimations')
    const { animateOnScroll } = useAnimations()
    
    const { value = 'slideUp', modifiers = {}, arg } = binding
    
    const options = {
      threshold: modifiers.threshold ? parseFloat(arg) : 0.1,
      once: !modifiers.repeat,
      delay: modifiers.delay ? parseInt(arg) : 0
    }
    
    animateOnScroll(el, value, options)
  }
}

export default useAnimations