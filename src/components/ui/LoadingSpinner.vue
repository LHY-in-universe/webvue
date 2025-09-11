<template>
  <div 
    class="loading-spinner"
    :class="containerClasses"
  >
    <!-- Spinner Container -->
    <div class="flex items-center justify-center">
      <!-- Ring Spinner (default) -->
      <div 
        v-if="variant === 'border' || variant === 'ring'"
        :class="[
          'animate-spin rounded-full border-solid',
          sizeClasses,
          colorClasses
        ]"
      >
        <!-- Optional center dot -->
        <div v-if="variant === 'dot'" class="absolute inset-2 bg-current rounded-full opacity-25"></div>
      </div>

      <!-- Dots Spinner -->
      <div v-else-if="variant === 'dots'" class="flex space-x-1">
        <div
          v-for="i in 3"
          :key="i"
          :class="[
            'rounded-full animate-bounce',
            dotSizeClasses,
            dotColorClasses
          ]"
          :style="{ animationDelay: `${(i - 1) * 0.2}s` }"
        ></div>
      </div>

      <!-- Pulse Spinner -->
      <div v-else-if="variant === 'pulse'" :class="pulseSizeClasses">
        <div :class="[
          'rounded-full animate-pulse-custom',
          pulseSizeClasses,
          pulseColorClasses
        ]"></div>
      </div>

      <!-- Bars Spinner -->
      <div v-else-if="variant === 'bars'" class="flex space-x-1 items-end">
        <div
          v-for="i in 4"
          :key="i"
          :class="[
            'rounded-sm animate-wave',
            barSizeClasses,
            barColorClasses
          ]"
          :style="{ animationDelay: `${(i - 1) * 0.15}s` }"
        ></div>
      </div>

      <!-- Grid Spinner -->
      <div v-else-if="variant === 'grid'" :class="gridContainerClasses">
        <div
          v-for="i in 9"
          :key="i"
          :class="[
            'rounded-sm animate-pulse-custom',
            gridItemClasses,
            gridColorClasses
          ]"
          :style="{ animationDelay: `${((i - 1) % 3) * 0.1 + Math.floor((i - 1) / 3) * 0.05}s` }"
        ></div>
      </div>

      <!-- Heart Spinner -->
      <div v-else-if="variant === 'heart'">
        <svg
          :class="[
            'animate-pulse-custom',
            heartSizeClasses,
            heartColorClasses
          ]"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
        </svg>
      </div>

      <!-- Custom Spinner Slot -->
      <div v-else-if="variant === 'custom'">
        <slot name="spinner">
          <!-- Fallback to ring -->
          <div :class="[
            'animate-spin rounded-full border-solid',
            sizeClasses,
            colorClasses
          ]"></div>
        </slot>
      </div>
    </div>
    
    <!-- Loading Text -->
    <div v-if="text || $slots.default" class="ml-3 flex items-center">
      <slot>
        <p :class="textClasses">{{ text }}</p>
      </slot>
    </div>

    <!-- Progress Bar -->
    <div v-if="showProgress && progress !== null" class="w-full mt-3">
      <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-1">
        <span>{{ progressText }}</span>
        <span>{{ Math.round(progress) }}%</span>
      </div>
      <div :class="progressBarClasses">
        <div
          :class="[
            'h-full rounded-full transition-all duration-300',
            progressColorClasses
          ]"
          :style="{ width: `${progress}%` }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'warning', 'danger', 'white'].includes(value)
  },
  variant: {
    type: String,
    default: 'border',
    validator: (value) => ['border', 'ring', 'dot', 'pulse', 'dots', 'bars', 'grid', 'heart', 'custom'].includes(value)
  },
  text: {
    type: String,
    default: ''
  },
  overlay: {
    type: Boolean,
    default: false
  },
  fullPage: {
    type: Boolean,
    default: false
  },
  showProgress: {
    type: Boolean,
    default: false
  },
  progress: {
    type: Number,
    default: null,
    validator: value => value === null || (value >= 0 && value <= 100)
  },
  progressText: {
    type: String,
    default: 'Loading'
  }
})

const sizeClasses = computed(() => {
  const sizes = {
    xs: 'w-4 h-4 border-2',
    sm: 'w-5 h-5 border-2',
    md: 'w-6 h-6 border-2',
    lg: 'w-8 h-8 border-2',
    xl: 'w-12 h-12 border-4'
  }
  return sizes[props.size]
})

const colorClasses = computed(() => {
  const colors = {
    primary: 'border-blue-600 border-r-transparent dark:border-blue-400',
    secondary: 'border-gray-600 border-r-transparent dark:border-gray-300',
    success: 'border-green-600 border-r-transparent dark:border-green-400',
    warning: 'border-yellow-600 border-r-transparent dark:border-yellow-400',
    danger: 'border-red-600 border-r-transparent dark:border-red-400',
    white: 'border-white border-r-transparent'
  }
  return colors[props.color]
})

const textClasses = computed(() => {
  const sizes = {
    xs: 'text-xs',
    sm: 'text-sm',
    md: 'text-sm',
    lg: 'text-base',
    xl: 'text-lg'
  }
  return `${sizes[props.size]} text-gray-600 dark:text-gray-300 font-medium`
})

const containerClasses = computed(() => {
  const classes = ['flex items-center']
  
  if (props.fullPage) {
    classes.push('fixed inset-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm justify-center')
  } else if (props.overlay) {
    classes.push('absolute inset-0 z-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm justify-center')
  }
  
  return classes
})

// Dots spinner classes
const dotSizeClasses = computed(() => {
  const sizes = {
    xs: 'w-1.5 h-1.5',
    sm: 'w-2 h-2',
    md: 'w-2.5 h-2.5',
    lg: 'w-3 h-3',
    xl: 'w-4 h-4'
  }
  return sizes[props.size]
})

const dotColorClasses = computed(() => {
  const colors = {
    primary: 'bg-blue-600 dark:bg-blue-400',
    secondary: 'bg-gray-600 dark:bg-gray-300',
    success: 'bg-green-600 dark:bg-green-400',
    warning: 'bg-yellow-600 dark:bg-yellow-400',
    danger: 'bg-red-600 dark:bg-red-400',
    white: 'bg-white'
  }
  return colors[props.color]
})

// Pulse spinner classes
const pulseSizeClasses = computed(() => {
  const sizes = {
    xs: 'w-4 h-4',
    sm: 'w-5 h-5',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  }
  return sizes[props.size]
})

const pulseColorClasses = computed(() => {
  const colors = {
    primary: 'bg-blue-600 dark:bg-blue-400',
    secondary: 'bg-gray-600 dark:bg-gray-300',
    success: 'bg-green-600 dark:bg-green-400',
    warning: 'bg-yellow-600 dark:bg-yellow-400',
    danger: 'bg-red-600 dark:bg-red-400',
    white: 'bg-white'
  }
  return colors[props.color]
})

// Bars spinner classes
const barSizeClasses = computed(() => {
  const sizes = {
    xs: 'w-1 h-3',
    sm: 'w-1.5 h-4',
    md: 'w-2 h-6',
    lg: 'w-3 h-8',
    xl: 'w-4 h-12'
  }
  return sizes[props.size]
})

const barColorClasses = computed(() => {
  const colors = {
    primary: 'bg-blue-600 dark:bg-blue-400',
    secondary: 'bg-gray-600 dark:bg-gray-300',
    success: 'bg-green-600 dark:bg-green-400',
    warning: 'bg-yellow-600 dark:bg-yellow-400',
    danger: 'bg-red-600 dark:bg-red-400',
    white: 'bg-white'
  }
  return colors[props.color]
})

// Grid spinner classes
const gridContainerClasses = computed(() => 'grid grid-cols-3 gap-1')

const gridItemClasses = computed(() => {
  const sizes = {
    xs: 'w-1 h-1',
    sm: 'w-1.5 h-1.5',
    md: 'w-2 h-2',
    lg: 'w-2.5 h-2.5',
    xl: 'w-3 h-3'
  }
  return sizes[props.size]
})

const gridColorClasses = computed(() => {
  const colors = {
    primary: 'bg-blue-600 dark:bg-blue-400',
    secondary: 'bg-gray-600 dark:bg-gray-300',
    success: 'bg-green-600 dark:bg-green-400',
    warning: 'bg-yellow-600 dark:bg-yellow-400',
    danger: 'bg-red-600 dark:bg-red-400',
    white: 'bg-white'
  }
  return colors[props.color]
})

// Heart spinner classes
const heartSizeClasses = computed(() => {
  const sizes = {
    xs: 'w-4 h-4',
    sm: 'w-5 h-5',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  }
  return sizes[props.size]
})

const heartColorClasses = computed(() => {
  const colors = {
    primary: 'text-blue-600 dark:text-blue-400',
    secondary: 'text-gray-600 dark:text-gray-300',
    success: 'text-green-600 dark:text-green-400',
    warning: 'text-yellow-600 dark:text-yellow-400',
    danger: 'text-red-600 dark:text-red-400',
    white: 'text-white'
  }
  return colors[props.color]
})

// Progress bar classes
const progressBarClasses = computed(() => [
  'w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden'
])

const progressColorClasses = computed(() => {
  const colors = {
    primary: 'bg-blue-600 dark:bg-blue-400',
    secondary: 'bg-gray-600 dark:bg-gray-300',
    success: 'bg-green-600 dark:bg-green-400',
    warning: 'bg-yellow-600 dark:bg-yellow-400',
    danger: 'bg-red-600 dark:bg-red-400',
    white: 'bg-white'
  }
  return colors[props.color]
})
</script>

<style scoped>
.loading-spinner {
  @apply select-none;
}

/* Custom pulse animation for pulse variant */
@keyframes pulse-custom {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse-custom {
  animation: pulse-custom 1.5s ease-in-out infinite;
}

/* Wave animation for bars */
@keyframes wave {
  0%, 40%, 100% {
    transform: scaleY(0.4);
  }
  20% {
    transform: scaleY(1);
  }
}

.animate-wave {
  animation: wave 1.2s infinite ease-in-out;
}

/* Enhanced bounce for dots */
@keyframes dots-bounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.6;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

/* Grid fade animation */
@keyframes grid-fade {
  0%, 70%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  35% {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-grid-fade {
  animation: grid-fade 1.5s infinite ease-in-out;
}

/* Smooth transitions for progress */
.progress-transition {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
  .animate-spin,
  .animate-pulse,
  .animate-pulse-custom,
  .animate-bounce,
  .animate-wave,
  .animate-grid-fade {
    animation: none;
  }
  
  /* Show static state for reduced motion */
  .loading-spinner * {
    animation: none !important;
    transform: none !important;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .loading-spinner {
    filter: contrast(1.2);
  }
}

/* Print styles */
@media print {
  .loading-spinner {
    display: none;
  }
}
</style>