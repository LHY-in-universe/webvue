import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'

export const useWebAnimations = () => {
  const animations = reactive(new Map())
  const isSupported = ref(false)
  
  // Check Web Animations API support
  const checkSupport = () => {
    isSupported.value = typeof window !== 'undefined' && 
                       'animate' in Element.prototype
  }

  onMounted(() => {
    checkSupport()
  })

  // Advanced animation presets
  const animationPresets = {
    // Theme transition presets
    themeRipple: (element, options = {}) => ({
      keyframes: [
        { 
          clipPath: `circle(0% at ${options.x || 50}% ${options.y || 50}%)`,
          opacity: 0.8
        },
        { 
          clipPath: `circle(150% at ${options.x || 50}% ${options.y || 50}%)`,
          opacity: 1
        }
      ],
      options: {
        duration: options.duration || 600,
        easing: 'cubic-bezier(0.4, 0.0, 0.2, 1)',
        fill: 'both',
        ...options.animationOptions
      }
    }),

    // Color morphing
    colorMorph: (element, options = {}) => ({
      keyframes: [
        { 
          filter: 'hue-rotate(0deg) brightness(1) saturate(1)',
          background: options.fromColor || 'currentColor'
        },
        { 
          filter: `hue-rotate(${options.hueShift || 180}deg) brightness(1.2) saturate(1.3)`,
          background: options.midColor || 'currentColor'
        },
        { 
          filter: 'hue-rotate(0deg) brightness(1) saturate(1)',
          background: options.toColor || 'currentColor'
        }
      ],
      options: {
        duration: options.duration || 800,
        easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
        fill: 'both'
      }
    }),

    // Particle explosion
    particleExplosion: (element, options = {}) => ({
      keyframes: [
        { 
          transform: 'scale(0) rotate(0deg)',
          opacity: 0,
          filter: 'blur(0px)'
        },
        { 
          transform: 'scale(1.2) rotate(180deg)',
          opacity: 1,
          filter: 'blur(1px)'
        },
        { 
          transform: 'scale(0) rotate(360deg)',
          opacity: 0,
          filter: 'blur(3px)'
        }
      ],
      options: {
        duration: options.duration || 1000,
        easing: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
        delay: options.delay || 0
      }
    }),

    // Morphing shapes
    morphShape: (element, options = {}) => ({
      keyframes: [
        { 
          borderRadius: options.fromRadius || '0%',
          transform: 'scale(1) rotate(0deg)'
        },
        { 
          borderRadius: options.midRadius || '50%',
          transform: 'scale(1.1) rotate(180deg)'
        },
        { 
          borderRadius: options.toRadius || '0%',
          transform: 'scale(1) rotate(360deg)'
        }
      ],
      options: {
        duration: options.duration || 1200,
        easing: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
        iterationCount: options.loop ? 'infinite' : 1
      }
    }),

    // Glass morphism effect
    glassMorph: (element, options = {}) => ({
      keyframes: [
        { 
          backdropFilter: 'blur(0px) saturate(100%)',
          background: options.fromBg || 'rgba(255, 255, 255, 0.1)'
        },
        { 
          backdropFilter: 'blur(20px) saturate(180%)',
          background: options.midBg || 'rgba(255, 255, 255, 0.25)'
        },
        { 
          backdropFilter: options.blur || 'blur(10px) saturate(150%)',
          background: options.toBg || 'rgba(255, 255, 255, 0.15)'
        }
      ],
      options: {
        duration: options.duration || 600,
        easing: 'ease-in-out',
        fill: 'both'
      }
    }),

    // Lightning effect
    lightning: (element, options = {}) => ({
      keyframes: [
        { 
          boxShadow: '0 0 5px rgba(59, 130, 246, 0.5)',
          filter: 'brightness(1)'
        },
        { 
          boxShadow: '0 0 30px rgba(59, 130, 246, 0.8), 0 0 60px rgba(59, 130, 246, 0.6)',
          filter: 'brightness(1.5)'
        },
        { 
          boxShadow: '0 0 5px rgba(59, 130, 246, 0.3)',
          filter: 'brightness(1)'
        }
      ],
      options: {
        duration: options.duration || 150,
        easing: 'ease-in-out',
        iterationCount: options.flashes || 3
      }
    })
  }

  // Create and manage animation
  const createAnimation = (element, preset, options = {}) => {
    if (!isSupported.value || !element) return null

    const animationConfig = animationPresets[preset]?.(element, options)
    if (!animationConfig) return null

    const animation = element.animate(
      animationConfig.keyframes,
      animationConfig.options
    )

    // Store animation reference
    const animationId = Symbol('animation')
    animations.set(animationId, animation)

    // Auto-cleanup on finish
    animation.addEventListener('finish', () => {
      animations.delete(animationId)
    })

    return {
      animation,
      id: animationId,
      play: () => animation.play(),
      pause: () => animation.pause(),
      cancel: () => {
        animation.cancel()
        animations.delete(animationId)
      },
      reverse: () => animation.reverse(),
      updatePlaybackRate: (rate) => {
        animation.updatePlaybackRate(rate)
      }
    }
  }

  // Create complex animation sequences
  const createSequence = async (sequences) => {
    if (!isSupported.value) return

    const results = []
    
    for (const sequence of sequences) {
      const { element, preset, options = {}, wait = true } = sequence
      
      const animation = createAnimation(element, preset, options)
      if (animation) {
        results.push(animation)
        
        if (wait) {
          await new Promise(resolve => {
            animation.animation.addEventListener('finish', resolve)
          })
        }
      }
    }

    return results
  }

  // Parallel animations
  const createParallel = (animations) => {
    if (!isSupported.value) return []

    return animations.map(({ element, preset, options }) => 
      createAnimation(element, preset, options)
    ).filter(Boolean)
  }

  // Staggered animations
  const createStaggered = (elements, preset, options = {}) => {
    if (!isSupported.value) return []

    const { staggerDelay = 100, ...animationOptions } = options
    
    return elements.map((element, index) => 
      createAnimation(element, preset, {
        ...animationOptions,
        animationOptions: {
          ...animationOptions.animationOptions,
          delay: (animationOptions.animationOptions?.delay || 0) + (index * staggerDelay)
        }
      })
    ).filter(Boolean)
  }

  // Theme-aware animations
  const createThemeAnimation = (element, isDark, options = {}) => {
    const themeColors = {
      light: {
        primary: '#3b82f6',
        bg: 'rgba(255, 255, 255, 0.1)',
        shadow: 'rgba(0, 0, 0, 0.1)'
      },
      dark: {
        primary: '#60a5fa',
        bg: 'rgba(0, 0, 0, 0.3)',
        shadow: 'rgba(255, 255, 255, 0.1)'
      }
    }

    const colors = themeColors[isDark ? 'dark' : 'light']
    
    return createAnimation(element, 'colorMorph', {
      fromColor: colors.bg,
      toColor: colors.primary,
      ...options
    })
  }

  // Performance monitoring
  const monitorPerformance = (animation) => {
    if (!animation?.animation) return

    const startTime = performance.now()
    let frameCount = 0
    
    const monitor = () => {
      frameCount++
      if (animation.animation.playState === 'running') {
        requestAnimationFrame(monitor)
      } else {
        const endTime = performance.now()
        const duration = endTime - startTime
        const fps = Math.round((frameCount * 1000) / duration)
        
        console.log(`Animation Performance:`, {
          duration: `${duration.toFixed(2)}ms`,
          frames: frameCount,
          averageFPS: fps
        })
      }
    }

    requestAnimationFrame(monitor)
  }

  // Batch operations
  const pauseAll = () => {
    animations.forEach(animation => animation.pause())
  }

  const playAll = () => {
    animations.forEach(animation => animation.play())
  }

  const cancelAll = () => {
    animations.forEach(animation => animation.cancel())
    animations.clear()
  }

  // Animation state management
  const getAnimationStates = () => {
    const states = {}
    animations.forEach((animation, id) => {
      states[id.description || id] = {
        playState: animation.playState,
        currentTime: animation.currentTime,
        playbackRate: animation.playbackRate
      }
    })
    return states
  }

  // Cleanup
  onUnmounted(() => {
    cancelAll()
  })

  return {
    // State
    isSupported,
    animations,
    animationPresets,
    
    // Core methods
    createAnimation,
    createSequence,
    createParallel,
    createStaggered,
    createThemeAnimation,
    
    // Batch operations
    pauseAll,
    playAll,
    cancelAll,
    
    // Utilities
    monitorPerformance,
    getAnimationStates
  }
}

// Specialized animation hooks
export const useThemeRipple = () => {
  const { createAnimation, isSupported } = useWebAnimations()

  const triggerRipple = async (triggerElement, targetElement = document.body) => {
    if (!isSupported.value || !triggerElement) return

    const rect = triggerElement.getBoundingClientRect()
    const centerX = ((rect.left + rect.width / 2) / window.innerWidth) * 100
    const centerY = ((rect.top + rect.height / 2) / window.innerHeight) * 100

    // Create ripple overlay
    const rippleOverlay = document.createElement('div')
    Object.assign(rippleOverlay.style, {
      position: 'fixed',
      top: '0',
      left: '0',
      width: '100vw',
      height: '100vh',
      pointerEvents: 'none',
      zIndex: '9999',
      mixBlendMode: 'soft-light'
    })

    targetElement.appendChild(rippleOverlay)

    const animation = createAnimation(rippleOverlay, 'themeRipple', {
      x: centerX,
      y: centerY,
      duration: 800
    })

    if (animation) {
      animation.animation.addEventListener('finish', () => {
        rippleOverlay.remove()
      })
    }

    return animation
  }

  return {
    triggerRipple,
    isSupported
  }
}

export const useParticleSystem = () => {
  const { createAnimation, createParallel, isSupported } = useWebAnimations()

  const createParticleExplosion = (element, particleCount = 12, options = {}) => {
    if (!isSupported.value || !element) return []

    const particles = []
    const rect = element.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div')
      
      Object.assign(particle.style, {
        position: 'fixed',
        left: `${centerX}px`,
        top: `${centerY}px`,
        width: '4px',
        height: '4px',
        borderRadius: '50%',
        background: options.color || '#3b82f6',
        pointerEvents: 'none',
        zIndex: '9998'
      })

      document.body.appendChild(particle)
      particles.push(particle)

      // Add random direction
      const angle = (i / particleCount) * Math.PI * 2
      const distance = 50 + Math.random() * 50
      const endX = centerX + Math.cos(angle) * distance
      const endY = centerY + Math.sin(angle) * distance

      particle.animate([
        { transform: 'translate(-50%, -50%) scale(0)', opacity: 1 },
        { transform: `translate(${endX - centerX}px, ${endY - centerY}px) scale(1)`, opacity: 0.5 },
        { transform: `translate(${endX - centerX}px, ${endY - centerY}px) scale(0)`, opacity: 0 }
      ], {
        duration: 800 + Math.random() * 400,
        easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
        delay: Math.random() * 200
      }).addEventListener('finish', () => {
        particle.remove()
      })
    }

    return particles
  }

  return {
    createParticleExplosion,
    isSupported
  }
}