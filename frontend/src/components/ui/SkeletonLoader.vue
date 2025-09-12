<template>
  <div :class="containerClasses">
    <!-- Skeleton Types -->
    
    <!-- Text Skeleton -->
    <div v-if="type === 'text'" :class="textClasses">
      <div
        v-for="n in lines"
        :key="n"
        :class="[
          'skeleton-line',
          n === lines && lastLineWidth ? `w-${lastLineWidth}` : 'w-full'
        ]"
        :style="{ animationDelay: `${n * 0.1}s` }"
      ></div>
    </div>

    <!-- Card Skeleton -->
    <div v-else-if="type === 'card'" :class="cardClasses">
      <!-- Card Header -->
      <div v-if="showHeader" class="flex items-center space-x-3 mb-4">
        <div :class="avatarClasses"></div>
        <div class="flex-1 space-y-2">
          <div class="skeleton-line h-4 w-3/4"></div>
          <div class="skeleton-line h-3 w-1/2"></div>
        </div>
      </div>

      <!-- Card Content -->
      <div class="space-y-3">
        <div class="skeleton-line h-4 w-full"></div>
        <div class="skeleton-line h-4 w-full"></div>
        <div class="skeleton-line h-4 w-2/3"></div>
      </div>

      <!-- Card Footer -->
      <div v-if="showFooter" class="flex justify-between items-center mt-4">
        <div class="skeleton-line h-8 w-20 rounded-lg"></div>
        <div class="skeleton-line h-8 w-16 rounded-lg"></div>
      </div>
    </div>

    <!-- Table Skeleton -->
    <div v-else-if="type === 'table'" class="space-y-4">
      <!-- Table Header -->
      <div class="flex space-x-4">
        <div
          v-for="col in columns"
          :key="col"
          :class="[
            'skeleton-line h-10 rounded-lg',
            isMobile ? 'flex-1' : col === 1 ? 'w-1/4' : col === 2 ? 'w-1/3' : col === 3 ? 'w-1/4' : 'w-1/6'
          ]"
        ></div>
      </div>

      <!-- Table Rows -->
      <div
        v-for="row in rows"
        :key="row"
        class="flex space-x-4"
        :style="{ animationDelay: `${row * 0.1}s` }"
      >
        <div
          v-for="col in columns"
          :key="col"
          :class="[
            'skeleton-line h-12 rounded-lg',
            isMobile ? 'flex-1' : col === 1 ? 'w-1/4' : col === 2 ? 'w-1/3' : col === 3 ? 'w-1/4' : 'w-1/6'
          ]"
        ></div>
      </div>
    </div>

    <!-- Chart Skeleton -->
    <div v-else-if="type === 'chart'" :class="chartClasses">
      <!-- Chart Title -->
      <div v-if="showTitle" class="mb-4">
        <div class="skeleton-line h-6 w-1/3"></div>
      </div>

      <!-- Chart Area -->
      <div class="relative">
        <!-- Y-axis -->
        <div class="absolute left-0 top-0 h-full w-8 flex flex-col justify-between py-4">
          <div
            v-for="n in 6"
            :key="n"
            class="skeleton-line h-3 w-6"
            :style="{ animationDelay: `${n * 0.05}s` }"
          ></div>
        </div>

        <!-- Chart Content -->
        <div class="ml-10 relative" :style="{ height: chartHeight }">
          <!-- Chart Bars/Lines -->
          <div
            v-for="n in chartBars"
            :key="n"
            :class="[
              'absolute bottom-0 skeleton-line rounded-t-lg',
              isMobile ? 'w-6' : 'w-8'
            ]"
            :style="{
              left: `${(n - 1) * (isMobile ? 32 : 48)}px`,
              height: `${Math.random() * 60 + 20}%`,
              animationDelay: `${n * 0.1}s`
            }"
          ></div>
        </div>

        <!-- X-axis -->
        <div class="flex justify-between mt-2 ml-10">
          <div
            v-for="n in chartBars"
            :key="n"
            class="skeleton-line h-3 w-8"
            :style="{ animationDelay: `${n * 0.05}s` }"
          ></div>
        </div>
      </div>

      <!-- Legend -->
      <div v-if="showLegend" class="flex justify-center mt-4 space-x-4">
        <div
          v-for="n in 3"
          :key="n"
          class="flex items-center space-x-2"
        >
          <div class="skeleton-line w-4 h-4 rounded"></div>
          <div class="skeleton-line h-3 w-12"></div>
        </div>
      </div>
    </div>

    <!-- List Skeleton -->
    <div v-else-if="type === 'list'" class="space-y-4">
      <div
        v-for="item in items"
        :key="item"
        class="flex items-center space-x-3"
        :style="{ animationDelay: `${item * 0.1}s` }"
      >
        <div v-if="showAvatar" :class="avatarClasses"></div>
        <div class="flex-1 space-y-2">
          <div class="skeleton-line h-4 w-3/4"></div>
          <div class="skeleton-line h-3 w-1/2"></div>
        </div>
        <div v-if="showActions" class="skeleton-line h-8 w-16 rounded-lg"></div>
      </div>
    </div>

    <!-- Custom Skeleton -->
    <div v-else-if="type === 'custom'" class="space-y-4">
      <slot name="skeleton" />
    </div>

    <!-- Default Skeleton -->
    <div v-else class="space-y-3">
      <div class="skeleton-line h-4 w-full"></div>
      <div class="skeleton-line h-4 w-5/6"></div>
      <div class="skeleton-line h-4 w-4/6"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useResponsive } from '@/composables/useResponsive'

const { isMobile, getResponsiveValue } = useResponsive()

const props = defineProps({
  type: {
    type: String,
    default: 'text',
    validator: value => ['text', 'card', 'table', 'chart', 'list', 'custom'].includes(value)
  },
  lines: {
    type: Number,
    default: 3
  },
  rows: {
    type: Number,
    default: 5
  },
  columns: {
    type: Number,
    default: 4
  },
  items: {
    type: Number,
    default: 5
  },
  chartBars: {
    type: Number,
    default: 7
  },
  animated: {
    type: Boolean,
    default: true
  },
  speed: {
    type: String,
    default: 'normal', // slow, normal, fast
    validator: value => ['slow', 'normal', 'fast'].includes(value)
  },
  variant: {
    type: String,
    default: 'default', // default, wave, pulse
    validator: value => ['default', 'wave', 'pulse'].includes(value)
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  showFooter: {
    type: Boolean,
    default: true
  },
  showTitle: {
    type: Boolean,
    default: true
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  showAvatar: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  lastLineWidth: {
    type: String,
    default: '2/3'
  },
  height: {
    type: String,
    default: 'auto'
  }
})

// Computed classes
const containerClasses = computed(() => {
  const base = 'skeleton-container animate-pulse'
  const height = props.height !== 'auto' ? `h-${props.height}` : ''
  const speed = {
    slow: 'skeleton-slow',
    normal: 'skeleton-normal', 
    fast: 'skeleton-fast'
  }[props.speed]
  
  return [base, height, speed, props.animated ? 'animate-pulse' : '']
})

const textClasses = computed(() => {
  return getResponsiveValue({
    xs: 'space-y-2',
    md: 'space-y-3'
  })
})

const cardClasses = computed(() => {
  return getResponsiveValue({
    xs: 'p-3 border border-gray-200 dark:border-gray-700 rounded-lg',
    md: 'p-6 border border-gray-200 dark:border-gray-700 rounded-lg'
  })
})

const chartClasses = computed(() => {
  return getResponsiveValue({
    xs: 'p-3',
    md: 'p-4'
  })
})

const chartHeight = computed(() => {
  return getResponsiveValue({
    xs: '200px',
    md: '300px'
  })
})

const avatarClasses = computed(() => {
  return getResponsiveValue({
    xs: 'skeleton-line w-10 h-10 rounded-full flex-shrink-0',
    md: 'skeleton-line w-12 h-12 rounded-full flex-shrink-0'
  })
})
</script>

<style scoped>
.skeleton-line {
  @apply bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 dark:from-gray-700 dark:via-gray-600 dark:to-gray-700 rounded;
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
}

.skeleton-container.skeleton-slow .skeleton-line {
  animation-duration: 2.5s;
}

.skeleton-container.skeleton-fast .skeleton-line {
  animation-duration: 1s;
}

/* Wave animation */
.skeleton-container .skeleton-line {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  ), #f3f4f6;
  background-size: 200% 100%;
}

.dark .skeleton-container .skeleton-line {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  ), #374151;
  background-size: 200% 100%;
}

@keyframes skeleton-loading {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* Pulse variant */
.skeleton-container.skeleton-pulse .skeleton-line {
  animation: skeleton-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes skeleton-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Remove default animate-pulse when using custom animations */
.skeleton-container.skeleton-slow,
.skeleton-container.skeleton-fast,
.skeleton-container.skeleton-pulse {
  animation: none;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .skeleton-line {
    min-height: 16px;
  }
}

@media (min-width: 641px) {
  .skeleton-line {
    min-height: 20px;
  }
}
</style>