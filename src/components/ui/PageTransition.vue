<template>
  <TransitionGroup
    :name="computedTransitionName"
    :mode="mode"
    :duration="duration"
    tag="div"
    class="page-transition-container"
    @before-enter="onBeforeEnter"
    @enter="onEnter"
    @after-enter="onAfterEnter"
    @before-leave="onBeforeLeave"
    @leave="onLeave"
    @after-leave="onAfterLeave"
  >
    <slot />
  </TransitionGroup>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const props = defineProps({
  name: {
    type: String,
    default: 'page'
  },
  mode: {
    type: String,
    default: 'out-in'
  },
  duration: {
    type: [Number, Object],
    default: { enter: 500, leave: 300 }
  },
  effect: {
    type: String,
    default: 'slide',
    validator: (value) => ['slide', 'fade', 'scale', 'rotate', 'flip'].includes(value)
  },
  direction: {
    type: String,
    default: 'auto',
    validator: (value) => ['auto', 'forward', 'backward', 'up', 'down', 'left', 'right'].includes(value)
  },
  enableRouteTransitions: {
    type: Boolean,
    default: true
  },
  staggerChildren: {
    type: Boolean,
    default: false
  },
  staggerDelay: {
    type: Number,
    default: 50
  }
})

const emit = defineEmits([
  'before-enter',
  'enter', 
  'after-enter',
  'before-leave',
  'leave',
  'after-leave',
  'transition-start',
  'transition-end'
])

const router = useRouter()
const route = useRoute()

const transitionDirection = ref('forward')
const isTransitioning = ref(false)

const computedTransitionName = computed(() => {
  const dir = props.direction === 'auto' ? transitionDirection.value : props.direction
  return `${props.name}-${props.effect}-${dir}`
})

// Route-based transition direction detection
const detectTransitionDirection = (to, from) => {
  if (!props.enableRouteTransitions) return 'forward'
  
  // Define route hierarchy for automatic direction detection
  const routeHierarchy = {
    '/': 0,
    '/home': 0,
    '/login': 1,
    '/dashboard': 2,
    '/projects': 3,
    '/project': 4,
    '/settings': 5
  }
  
  const toDepth = routeHierarchy[to.path] ?? 999
  const fromDepth = routeHierarchy[from.path] ?? 999
  
  return toDepth > fromDepth ? 'forward' : 'backward'
}

// Transition event handlers
const onBeforeEnter = (el) => {
  isTransitioning.value = true
  emit('transition-start')
  
  if (props.staggerChildren) {
    const children = el.querySelectorAll('[data-stagger]')
    children.forEach((child, index) => {
      child.style.transitionDelay = `${index * props.staggerDelay}ms`
    })
  }
  
  emit('before-enter', el)
}

const onEnter = (el, done) => {
  emit('enter', el, done)
}

const onAfterEnter = (el) => {
  isTransitioning.value = false
  emit('transition-end')
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

// Setup route change detection
let removeRouterGuard = null

onMounted(() => {
  if (props.enableRouteTransitions) {
    removeRouterGuard = router.beforeEach((to, from) => {
      transitionDirection.value = detectTransitionDirection(to, from)
    })
  }
})

onUnmounted(() => {
  if (removeRouterGuard) {
    removeRouterGuard()
  }
})

defineExpose({
  isTransitioning,
  transitionDirection
})
</script>

<style scoped>
.page-transition-container {
  position: relative;
  width: 100%;
  height: 100%;
}

/* Slide transitions */
.page-slide-forward-enter-active,
.page-slide-forward-leave-active,
.page-slide-backward-enter-active,
.page-slide-backward-leave-active {
  transition: all 0.4s cubic-bezier(0.55, 0, 0.1, 1);
}

.page-slide-forward-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.page-slide-forward-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}

.page-slide-backward-enter-from {
  opacity: 0;
  transform: translateX(-100%);
}

.page-slide-backward-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

/* Fade transitions */
.page-fade-forward-enter-active,
.page-fade-forward-leave-active,
.page-fade-backward-enter-active,
.page-fade-backward-leave-active {
  transition: all 0.3s ease;
}

.page-fade-forward-enter-from,
.page-fade-forward-leave-to,
.page-fade-backward-enter-from,
.page-fade-backward-leave-to {
  opacity: 0;
}

/* Scale transitions */
.page-scale-forward-enter-active,
.page-scale-forward-leave-active,
.page-scale-backward-enter-active,
.page-scale-backward-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.page-scale-forward-enter-from {
  opacity: 0;
  transform: scale(1.1);
}

.page-scale-forward-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.page-scale-backward-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

.page-scale-backward-leave-to {
  opacity: 0;
  transform: scale(1.1);
}

/* Rotate transitions */
.page-rotate-forward-enter-active,
.page-rotate-forward-leave-active,
.page-rotate-backward-enter-active,
.page-rotate-backward-leave-active {
  transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.page-rotate-forward-enter-from {
  opacity: 0;
  transform: rotateY(-90deg) scale(0.8);
}

.page-rotate-forward-leave-to {
  opacity: 0;
  transform: rotateY(90deg) scale(0.8);
}

.page-rotate-backward-enter-from {
  opacity: 0;
  transform: rotateY(90deg) scale(0.8);
}

.page-rotate-backward-leave-to {
  opacity: 0;
  transform: rotateY(-90deg) scale(0.8);
}

/* Flip transitions */
.page-flip-forward-enter-active,
.page-flip-forward-leave-active,
.page-flip-backward-enter-active,
.page-flip-backward-leave-active {
  transition: all 0.6s cubic-bezier(0.23, 1, 0.320, 1);
  transform-style: preserve-3d;
  perspective: 1000px;
}

.page-flip-forward-enter-from {
  opacity: 0;
  transform: rotateX(-90deg);
}

.page-flip-forward-leave-to {
  opacity: 0;
  transform: rotateX(90deg);
}

.page-flip-backward-enter-from {
  opacity: 0;
  transform: rotateX(90deg);
}

.page-flip-backward-leave-to {
  opacity: 0;
  transform: rotateX(-90deg);
}

/* Vertical directions */
.page-slide-up-enter-active,
.page-slide-up-leave-active {
  transition: all 0.4s cubic-bezier(0.55, 0, 0.1, 1);
}

.page-slide-up-enter-from {
  opacity: 0;
  transform: translateY(100%);
}

.page-slide-up-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}

.page-slide-down-enter-active,
.page-slide-down-leave-active {
  transition: all 0.4s cubic-bezier(0.55, 0, 0.1, 1);
}

.page-slide-down-enter-from {
  opacity: 0;
  transform: translateY(-100%);
}

.page-slide-down-leave-to {
  opacity: 0;
  transform: translateY(100%);
}

/* Stagger animations */
[data-stagger] {
  transition: all 0.3s ease;
}

/* Mobile optimizations */
@media (max-width: 768px) {
  .page-transition-container {
    will-change: transform, opacity;
  }
  
  /* Reduce motion for better performance on mobile */
  .page-slide-forward-enter-active,
  .page-slide-forward-leave-active,
  .page-slide-backward-enter-active,
  .page-slide-backward-leave-active {
    transition-duration: 0.25s;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .page-transition-container * {
    transition-duration: 0.1s !important;
    animation-duration: 0.1s !important;
  }
}
</style>