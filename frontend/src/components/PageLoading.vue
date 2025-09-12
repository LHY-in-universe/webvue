<template>
  <Teleport to="body">
    <div v-if="show" class="page-loading-overlay">
      <div class="page-loading-container">
        <div class="page-loading-content">
          <!-- Animated Logo/Icon -->
          <div class="loading-icon animate-bounce">
            <svg class="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </div>
          
          <!-- Loading Text -->
          <div class="loading-text">
            <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-2">
              {{ title || 'Loading...' }}
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              {{ subtitle || 'Please wait while we load your content' }}
            </p>
          </div>
          
          <!-- Progress Bar -->
          <div class="loading-progress">
            <div class="progress-bar-track">
              <div 
                class="progress-bar-fill"
                :style="{ width: `${progress}%` }"
              ></div>
            </div>
            <span class="text-xs text-gray-500 dark:text-gray-400 mt-1">
              {{ Math.round(progress) }}%
            </span>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Loading...'
  },
  subtitle: {
    type: String,
    default: 'Please wait while we load your content'
  },
  autoProgress: {
    type: Boolean,
    default: true
  }
})

const progress = ref(0)
let progressInterval = null

const startProgress = () => {
  if (!props.autoProgress) return
  
  progress.value = 0
  progressInterval = setInterval(() => {
    if (progress.value < 90) {
      progress.value += Math.random() * 15
    } else if (progress.value < 95) {
      progress.value += Math.random() * 2
    }
  }, 200)
}

const finishProgress = () => {
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }
  progress.value = 100
  
  setTimeout(() => {
    progress.value = 0
  }, 500)
}

watch(() => props.show, (newShow) => {
  if (newShow) {
    startProgress()
  } else {
    finishProgress()
  }
})

onUnmounted(() => {
  if (progressInterval) {
    clearInterval(progressInterval)
  }
})
</script>

<style scoped>
.page-loading-overlay {
  @apply fixed inset-0 z-50 flex items-center justify-center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  animation: fadeIn 0.3s ease-out;
}

.dark .page-loading-overlay {
  background: rgba(17, 24, 39, 0.95);
}

.page-loading-container {
  @apply relative;
}

.page-loading-content {
  @apply flex flex-col items-center text-center;
  animation: slideUp 0.4s ease-out 0.1s both;
}

.loading-icon {
  @apply mb-6;
  animation: bounce 1.5s infinite, glow 2s ease-in-out infinite alternate;
}

.loading-text {
  @apply mb-6;
}

.loading-progress {
  @apply w-64 flex flex-col items-center;
}

.progress-bar-track {
  @apply w-full h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden;
}

.progress-bar-fill {
  @apply h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-full transition-all duration-300 ease-out;
  animation: shimmer 1.5s infinite;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes glow {
  from {
    filter: drop-shadow(0 0 5px rgba(59, 130, 246, 0.3));
  }
  to {
    filter: drop-shadow(0 0 15px rgba(59, 130, 246, 0.6));
  }
}

@keyframes shimmer {
  0% {
    background-position: -200% center;
  }
  100% {
    background-position: 200% center;
  }
}

.progress-bar-fill {
  background-size: 200% 100%;
  background-image: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
}
</style>