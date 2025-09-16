<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="isVisible"
        class="modal-overlay"
        @click.self="closeModal"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/50 dark:bg-black/70 backdrop-blur-sm"></div>

        <!-- Modal Content -->
        <div class="modal-content" :style="{
          left: modalPosition.x,
          top: modalPosition.y,
          transform: modalPosition.transform,
          width: modalPosition.width || 'auto',
          height: modalPosition.height || 'auto'
        }">
          <!-- Header -->
          <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center space-x-4">
              <!-- Status Indicator -->
              <div class="relative">
                <div
                  :class="getStatusColor(node?.status)"
                  class="w-4 h-4 rounded-full"
                >
                  <div
                    v-if="node?.status === 'training'"
                    class="absolute inset-0 rounded-full animate-ping opacity-20"
                    :class="getStatusColor(node?.status)"
                  ></div>
                </div>
              </div>

              <!-- Node Info -->
              <div>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">
                  {{ node?.name || 'Unknown Node' }}
                </h2>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ node?.id }} • {{ node?.type || 'training' }}
                </p>
              </div>
            </div>

            <!-- Close Button -->
            <button
              @click="closeModal"
              class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            >
              <XMarkIcon class="w-6 h-6" />
            </button>
          </div>

          <!-- Content -->
          <div class="p-6 overflow-y-auto max-h-[calc(90vh-100px)]">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <!-- Basic Information -->
              <div class="space-y-4">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Basic Information</h3>

                <!-- Info Grid -->
                <div class="space-y-3">
                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400">Status:</span>
                    <span
                      :class="getStatusTextColor(node?.status)"
                      class="font-medium capitalize"
                    >
                      {{ node?.status || 'unknown' }}
                    </span>
                  </div>

                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400">Role:</span>
                    <span class="text-gray-900 dark:text-white font-medium">
                      {{ node?.role || 'Participant' }}
                    </span>
                  </div>

                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400">IP Address:</span>
                    <span class="text-gray-900 dark:text-white font-mono text-sm">
                      {{ node?.ipAddress || 'Unknown' }}
                    </span>
                  </div>

                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400">Connected Nodes:</span>
                    <span class="text-gray-900 dark:text-white font-medium">
                      {{ node?.connectedNodes || '0 nodes' }}
                    </span>
                  </div>

                  <div class="flex justify-between">
                    <span class="text-gray-600 dark:text-gray-400">Last Heartbeat:</span>
                    <span class="text-gray-900 dark:text-white">
                      {{ node?.lastHeartbeat || 'Unknown' }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Performance Metrics -->
              <div class="space-y-4">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Performance Metrics</h3>

                <!-- CPU Usage -->
                <div class="space-y-2">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-600 dark:text-gray-400">CPU Usage</span>
                    <span class="text-gray-900 dark:text-white font-medium">{{ node?.resources?.cpu || 0 }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      class="bg-blue-500 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${node?.resources?.cpu || 0}%` }"
                    ></div>
                  </div>
                </div>

                <!-- Memory Usage -->
                <div class="space-y-2">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-600 dark:text-gray-400">Memory Usage</span>
                    <span class="text-gray-900 dark:text-white font-medium">{{ node?.resources?.memory || '0.0' }}GB</span>
                  </div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      class="bg-green-500 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${getMemoryPercentage()}%` }"
                    ></div>
                  </div>
                </div>

                <!-- GPU Usage -->
                <div class="space-y-2">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-600 dark:text-gray-400">GPU Usage</span>
                    <span class="text-gray-900 dark:text-white font-medium">{{ node?.resources?.gpu || 0 }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      class="bg-purple-500 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${node?.resources?.gpu || 0}%` }"
                    ></div>
                  </div>
                </div>
              </div>

              <!-- Training Information -->
              <div v-if="node?.type === 'training'" class="lg:col-span-2 space-y-4">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Training Information</h3>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <!-- Training Progress -->
                  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                    <div class="text-center">
                      <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">
                        {{ Math.round(node?.trainingProgress || 0) }}%
                      </div>
                      <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">Training Progress</div>
                      <div class="mt-2">
                        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div
                            class="bg-blue-500 h-2 rounded-full transition-all duration-300"
                            :style="{ width: `${node?.trainingProgress || 0}%` }"
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Priority -->
                  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                    <div class="text-center">
                      <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">
                        {{ node?.priority || 0 }}
                      </div>
                      <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">Priority Level</div>
                    </div>
                  </div>

                  <!-- User -->
                  <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                    <div class="text-center">
                      <div class="text-lg font-medium text-gray-900 dark:text-white">
                        {{ node?.user || 'System' }}
                      </div>
                      <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">Assigned User</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer Actions -->
          <div class="flex items-center justify-end space-x-3 p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
            <button
              @click="closeModal"
              class="px-4 py-2 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
            >
              Close
            </button>

            <button
              v-if="node?.status === 'training'"
              class="px-4 py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
            >
              Stop Training
            </button>

            <button
              v-else-if="node?.status === 'idle'"
              class="px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
            >
              Start Training
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, watch, onMounted, onUnmounted } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  node: {
    type: Object,
    default: () => null
  },
  isVisible: {
    type: Boolean,
    default: false
  },
  anchorPosition: {
    type: Object,
    default: () => ({ x: 0, y: 0 })
  }
})

const emit = defineEmits(['close', 'action'])

// Status color helpers
const getStatusColor = (status) => {
  const colors = {
    training: 'bg-blue-500',
    idle: 'bg-gray-400',
    online: 'bg-green-500',
    offline: 'bg-red-500',
    error: 'bg-red-500',
    completed: 'bg-green-500'
  }
  return colors[status] || 'bg-gray-400'
}

const getStatusTextColor = (status) => {
  const colors = {
    training: 'text-blue-600 dark:text-blue-400',
    idle: 'text-gray-600 dark:text-gray-400',
    online: 'text-green-600 dark:text-green-400',
    offline: 'text-red-600 dark:text-red-400',
    error: 'text-red-600 dark:text-red-400',
    completed: 'text-green-600 dark:text-green-400'
  }
  return colors[status] || 'text-gray-600 dark:text-gray-400'
}

// Memory percentage calculation (assume max 8GB for visualization)
const getMemoryPercentage = () => {
  const memory = parseFloat(props.node?.resources?.memory || 0)
  return Math.min((memory / 8) * 100, 100)
}

// Modal positioning computation
const modalPosition = computed(() => {
  if (!props.anchorPosition || !props.isVisible) {
    return { x: '50%', y: '50%', transform: 'translate(-50%, -50%)' }
  }

  const { x, y } = props.anchorPosition
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight

  console.log('🎯 Modal positioning - Anchor:', { x, y }, 'Viewport:', { viewportWidth, viewportHeight })

  // Check for mobile/small screens
  if (viewportWidth <= 768) {
    console.log('📱 Mobile positioning applied')
    // Mobile: use simplified positioning
    return {
      x: '0.5rem',
      y: '2.5rem',
      transform: 'none'
    }
  }

  // Desktop positioning logic with dynamic size calculations
  // Base modal dimensions based on content and viewport
  const maxModalWidth = Math.min(896, viewportWidth - 64) // 896px or viewport minus 64px padding
  const modalWidth = Math.max(512, Math.min(maxModalWidth, viewportWidth * 0.8)) // Between 512px and 80% viewport

  // Height calculation based on content type and viewport
  const baseHeight = props.node?.type === 'training' ? 650 : 550 // Training nodes need more space
  const modalHeight = Math.min(baseHeight, viewportHeight * 0.85, viewportHeight - 80) // Ensure 80px total padding

  // Calculate optimal position relative to row center
  let modalX = x - modalWidth / 2
  let modalY = y - modalHeight / 2

  // Enhanced boundary detection and adjustment
  const padding = 16
  const originalModalX = modalX
  const originalModalY = modalY

  // Horizontal boundary adjustment
  if (modalX < padding) {
    modalX = padding
  } else if (modalX + modalWidth > viewportWidth - padding) {
    modalX = viewportWidth - modalWidth - padding
  }

  // Vertical boundary adjustment with smart offset
  if (modalY < padding) {
    modalY = padding
  } else if (modalY + modalHeight > viewportHeight - padding) {
    modalY = viewportHeight - modalHeight - padding
  }

  // Log positioning calculation for debugging
  console.log('📏 Modal calculations:', {
    modalSize: { width: modalWidth, height: modalHeight },
    original: { x: originalModalX, y: originalModalY },
    adjusted: { x: modalX, y: modalY },
    boundaries: {
      left: modalX >= padding,
      right: modalX + modalWidth <= viewportWidth - padding,
      top: modalY >= padding,
      bottom: modalY + modalHeight <= viewportHeight - padding
    }
  })

  return {
    x: `${Math.round(modalX)}px`,
    y: `${Math.round(modalY)}px`,
    width: `${Math.round(modalWidth)}px`,
    height: `${Math.round(modalHeight)}px`,
    transform: 'none'
  }
})

// Modal actions
const closeModal = () => {
  console.log('🚪 Closing modal')
  emit('close')
}

// Debug modal visibility
watch(() => props.isVisible, (newValue) => {
  console.log('👁️  Modal visibility changed:', newValue)
  if (newValue) {
    console.log('📍 Modal should be displayed in screen center')
    // Log viewport dimensions for debugging
    console.log('📐 Viewport dimensions:', {
      width: window.innerWidth,
      height: window.innerHeight
    })
  }
})

// Keyboard event handling
const handleKeydown = (event) => {
  if (event.key === 'Escape' && props.isVisible) {
    closeModal()
  }
}

// Lifecycle
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Modal overlay - support for dynamic positioning */
.modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  z-index: 9999 !important;
  padding: 1rem !important;
  box-sizing: border-box !important;
}

/* Modal content container */
.modal-content {
  position: absolute !important;
  background: white;
  border-radius: 1rem !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
  max-width: 56rem !important; /* max-w-4xl */
  width: auto !important;
  min-width: 32rem !important; /* min-w-lg */
  max-height: 90vh !important;
  overflow: hidden !important;
  z-index: 10000 !important;
  transition: all 0.3s ease !important;
}

/* Dark mode for modal content */
.modal-content {
  @apply bg-white dark:bg-gray-900;
}

/* Modal transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease !important;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0 !important;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9) translateY(-20px) !important;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease !important;
}

/* Focus management */
.modal-content:focus {
  outline: none !important;
}

/* Scrollbar styling */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  @apply bg-gray-100 dark:bg-gray-800;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  @apply bg-gray-300 dark:bg-gray-600 rounded-full;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-400 dark:bg-gray-500;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 0.5rem !important;
  }

  .modal-content {
    min-width: 20rem !important; /* min-w-80 */
    max-width: calc(100vw - 1rem) !important;
    max-height: 95vh !important;
    left: 0.5rem !important;
    right: 0.5rem !important;
    top: 2.5rem !important;
    transform: none !important;
    width: calc(100vw - 1rem) !important;
  }
}

/* Ensure backdrop is behind content */
.modal-overlay > div:first-child {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  z-index: 9998 !important;
}

/* Additional viewport-based positioning */
.modal-overlay {
  min-height: 100vh !important;
  min-width: 100vw !important;
}
</style>