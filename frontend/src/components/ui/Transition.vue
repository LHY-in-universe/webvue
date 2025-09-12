<template>
  <Transition
    :name="transitionName"
    :mode="mode"
    :appear="appear"
    :duration="duration"
    @before-enter="onBeforeEnter"
    @enter="onEnter"
    @after-enter="onAfterEnter"
    @before-leave="onBeforeLeave"
    @leave="onLeave"
    @after-leave="onAfterLeave"
    @enter-cancelled="onEnterCancelled"
    @leave-cancelled="onLeaveCancelled"
  >
    <slot />
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useResponsive } from '@/composables/useResponsive'

const { isMobile } = useResponsive()

const props = defineProps({
  name: {
    type: String,
    default: 'fade'
  },
  mode: {
    type: String,
    default: undefined,
    validator: value => !value || ['in-out', 'out-in'].includes(value)
  },
  appear: {
    type: Boolean,
    default: false
  },
  duration: {
    type: [Number, Object],
    default: undefined
  },
  // Animation presets
  preset: {
    type: String,
    default: 'fade',
    validator: value => [
      'fade', 'slide-up', 'slide-down', 'slide-left', 'slide-right',
      'scale', 'scale-fade', 'flip', 'bounce', 'zoom', 'rotate',
      'slide-fade-up', 'slide-fade-down', 'slide-fade-left', 'slide-fade-right'
    ].includes(value)
  },
  // Performance options
  reduceMotion: {
    type: Boolean,
    default: false
  },
  mobileOptimized: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits([
  'before-enter',
  'enter',
  'after-enter',
  'before-leave',
  'leave',
  'after-leave',
  'enter-cancelled',
  'leave-cancelled'
])

// Computed
const transitionName = computed(() => {
  // Check for reduced motion preference
  if (props.reduceMotion || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    return 'instant'
  }
  
  // Use mobile-optimized animations
  if (props.mobileOptimized && isMobile.value) {
    const mobilePresets = {
      'slide-up': 'slide-up-mobile',
      'slide-down': 'slide-down-mobile',
      'slide-left': 'slide-left-mobile',
      'slide-right': 'slide-right-mobile',
      'scale': 'scale-mobile',
      'bounce': 'fade', // Simplify bounce on mobile
      'flip': 'fade' // Simplify flip on mobile
    }
    
    return mobilePresets[props.preset] || props.preset
  }
  
  return props.name || props.preset
})

// Event handlers
const onBeforeEnter = (el) => {
  emit('before-enter', el)
}

const onEnter = (el, done) => {
  emit('enter', el, done)
}

const onAfterEnter = (el) => {
  emit('after-enter', el)
}

const onBeforeLeave = (el) => {
  emit('before-leave', el)
}

const onLeave = (el, done) => {
  emit('leave', el, done)
}

const onAfterLeave = (el) => {
  emit('after-leave', el)
}

const onEnterCancelled = (el) => {
  emit('enter-cancelled', el)
}

const onLeaveCancelled = (el) => {
  emit('leave-cancelled', el)
}
</script>

<style>
/* Instant transition for reduced motion */
.instant-enter-active,
.instant-leave-active {
  transition: none !important;
}

/* Fade transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Slide transitions */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-left-enter-from,
.slide-left-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-right-enter-from,
.slide-right-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Scale transitions */
.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.scale-fade-enter-active,
.scale-fade-leave-active {
  transition: all 0.3s ease-out;
}

.scale-fade-enter-from,
.scale-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Zoom transitions */
.zoom-enter-active,
.zoom-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.zoom-enter-from,
.zoom-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* Bounce transitions */
.bounce-enter-active {
  animation: bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.bounce-leave-active {
  animation: bounce-out 0.3s ease-in;
}

@keyframes bounce-in {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes bounce-out {
  0% {
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(0.3);
  }
}

/* Flip transitions */
.flip-enter-active,
.flip-leave-active {
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
  transform-style: preserve-3d;
}

.flip-enter-from {
  opacity: 0;
  transform: rotateY(-90deg);
}

.flip-leave-to {
  opacity: 0;
  transform: rotateY(90deg);
}

/* Rotate transitions */
.rotate-enter-active,
.rotate-leave-active {
  transition: all 0.3s ease-out;
}

.rotate-enter-from,
.rotate-leave-to {
  opacity: 0;
  transform: rotate(-10deg) scale(0.9);
}

/* Slide fade combinations */
.slide-fade-up-enter-active,
.slide-fade-up-leave-active {
  transition: all 0.3s ease-out;
}

.slide-fade-up-enter-from,
.slide-fade-up-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.slide-fade-down-enter-active,
.slide-fade-down-leave-active {
  transition: all 0.3s ease-out;
}

.slide-fade-down-enter-from,
.slide-fade-down-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

.slide-fade-left-enter-active,
.slide-fade-left-leave-active {
  transition: all 0.3s ease-out;
}

.slide-fade-left-enter-from,
.slide-fade-left-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-right-enter-active,
.slide-fade-right-leave-active {
  transition: all 0.3s ease-out;
}

.slide-fade-right-enter-from,
.slide-fade-right-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Mobile optimized transitions */
.slide-up-mobile-enter-active,
.slide-up-mobile-leave-active {
  transition: all 0.25s ease-out;
}

.slide-up-mobile-enter-from,
.slide-up-mobile-leave-to {
  opacity: 0;
  transform: translateY(15px);
}

.slide-down-mobile-enter-active,
.slide-down-mobile-leave-active {
  transition: all 0.25s ease-out;
}

.slide-down-mobile-enter-from,
.slide-down-mobile-leave-to {
  opacity: 0;
  transform: translateY(-15px);
}

.slide-left-mobile-enter-active,
.slide-left-mobile-leave-active {
  transition: all 0.25s ease-out;
}

.slide-left-mobile-enter-from,
.slide-left-mobile-leave-to {
  opacity: 0;
  transform: translateX(15px);
}

.slide-right-mobile-enter-active,
.slide-right-mobile-leave-active {
  transition: all 0.25s ease-out;
}

.slide-right-mobile-enter-from,
.slide-right-mobile-leave-to {
  opacity: 0;
  transform: translateX(-15px);
}

.scale-mobile-enter-active,
.scale-mobile-leave-active {
  transition: all 0.25s ease-out;
}

.scale-mobile-enter-from,
.scale-mobile-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* List transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.list-move {
  transition: transform 0.3s ease;
}

/* Stagger animations for multiple items */
.stagger-item {
  transition: all 0.3s ease;
}

.stagger-item:nth-child(1) { transition-delay: 0.1s; }
.stagger-item:nth-child(2) { transition-delay: 0.2s; }
.stagger-item:nth-child(3) { transition-delay: 0.3s; }
.stagger-item:nth-child(4) { transition-delay: 0.4s; }
.stagger-item:nth-child(5) { transition-delay: 0.5s; }
.stagger-item:nth-child(6) { transition-delay: 0.6s; }
.stagger-item:nth-child(7) { transition-delay: 0.7s; }
.stagger-item:nth-child(8) { transition-delay: 0.8s; }
.stagger-item:nth-child(9) { transition-delay: 0.9s; }
.stagger-item:nth-child(10) { transition-delay: 1s; }

/* High performance GPU-accelerated transforms */
.gpu-accelerated {
  will-change: transform, opacity;
  transform: translateZ(0);
}

/* Reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
</style>