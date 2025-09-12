<template>
  <!-- Modal Overlay -->
  <Teleport to="body">
    <Transition name="modal-overlay">
      <div 
        v-if="isOpen"
        class="modal-overlay fixed inset-0 z-50 flex items-center justify-center p-4"
        :class="overlayClasses"
        @click="handleOverlayClick"
      >
        <!-- Modal Container -->
        <Transition name="modal-content">
          <div 
            v-if="isOpen"
            :class="[
              'modal-container glass-effect rounded-2xl shadow-strong max-h-[90vh] overflow-hidden animate-scale-in-bounce',
              sizeClasses
            ]"
            @click.stop
            role="dialog"
            :aria-labelledby="titleId"
            aria-modal="true"
          >
            <!-- Header -->
            <div 
              v-if="!hideHeader"
              class="modal-header px-6 py-4 border-b border-gray-200 dark:border-slate-700"
              :class="headerClasses"
            >
              <div class="flex items-center justify-between">
                <!-- Title -->
                <div class="flex items-center space-x-3">
                  <component 
                    :is="icon" 
                    v-if="icon" 
                    class="w-6 h-6 text-gray-600 dark:text-gray-300"
                  />
                  <h3 
                    :id="titleId"
                    class="text-lg font-semibold text-gradient text-shadow-soft"
                  >
                    <slot name="title">{{ title }}</slot>
                  </h3>
                </div>
                
                <!-- Close Button -->
                <button
                  v-if="!hideCloseButton"
                  @click="close"
                  class="modal-close-btn p-2 rounded-lg micro-bounce interactive-focus hover:bg-gray-100 dark:hover:bg-slate-700 transition-colors"
                  :aria-label="closeButtonLabel"
                >
                  <XMarkIcon class="w-5 h-5 text-gray-500 dark:text-gray-400" />
                </button>
              </div>
              
              <!-- Subtitle -->
              <p 
                v-if="subtitle"
                class="mt-2 text-sm text-gray-600 dark:text-gray-400"
              >
                {{ subtitle }}
              </p>
            </div>
            
            <!-- Body -->
            <div 
              class="modal-body"
              :class="bodyClasses"
            >
              <div class="overflow-y-auto max-h-full">
                <slot>
                  <div class="p-6">
                    <p class="text-gray-600 dark:text-gray-300">{{ content }}</p>
                  </div>
                </slot>
              </div>
            </div>
            
            <!-- Footer -->
            <div 
              v-if="!hideFooter || $slots.footer"
              class="modal-footer px-6 py-4 bg-gray-50 dark:bg-slate-700/50 border-t border-gray-200 dark:border-slate-700"
            >
              <slot name="footer">
                <div class="flex justify-end space-x-3">
                  <Button
                    v-if="showCancelButton"
                    @click="cancel"
                    variant="ghost"
                    :loading="loading"
                  >
                    {{ cancelButtonText }}
                  </Button>
                  <Button
                    v-if="showConfirmButton"
                    @click="confirm"
                    :variant="confirmButtonVariant"
                    :loading="loading"
                  >
                    {{ confirmButtonText }}
                  </Button>
                </div>
              </slot>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import Button from './Button.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  content: {
    type: String,
    default: ''
  },
  icon: {
    type: [Object, String, Function],
    default: null
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  persistent: {
    type: Boolean,
    default: false
  },
  hideHeader: {
    type: Boolean,
    default: false
  },
  hideFooter: {
    type: Boolean,
    default: false
  },
  hideCloseButton: {
    type: Boolean,
    default: false
  },
  closeOnEscape: {
    type: Boolean,
    default: true
  },
  showCancelButton: {
    type: Boolean,
    default: true
  },
  showConfirmButton: {
    type: Boolean,
    default: true
  },
  cancelButtonText: {
    type: String,
    default: 'Cancel'
  },
  confirmButtonText: {
    type: String,
    default: 'Confirm'
  },
  confirmButtonVariant: {
    type: String,
    default: 'primary'
  },
  closeButtonLabel: {
    type: String,
    default: 'Close modal'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'cancel', 'confirm', 'update:isOpen'])

// Responsive functionality
const { isMobile, getModalSize, getResponsiveValue } = useResponsive()

const titleId = computed(() => `modal-title-${Math.random().toString(36).substr(2, 9)}`)

const overlayClasses = computed(() => {
  return 'bg-black/50 backdrop-blur-sm'
})

const sizeClasses = computed(() => {
  // Auto-adjust size for mobile
  const actualSize = isMobile.value ? getModalSize(props.size) : props.size
  
  const sizes = {
    xs: getResponsiveValue({ xs: 'w-full max-w-xs mx-2', md: 'w-full max-w-sm' }),
    sm: getResponsiveValue({ xs: 'w-full max-w-sm mx-2', md: 'w-full max-w-md' }),
    md: getResponsiveValue({ xs: 'w-full max-w-md mx-2', md: 'w-full max-w-lg' }),
    lg: getResponsiveValue({ xs: 'w-full mx-2', md: 'w-full max-w-2xl' }),
    xl: getResponsiveValue({ xs: 'w-full mx-2', md: 'w-full max-w-4xl' }),
    full: getResponsiveValue({ xs: 'w-full mx-2', md: 'w-full max-w-none m-4' })
  }
  return sizes[actualSize] || sizes.md
})

const headerClasses = computed(() => {
  return 'bg-white dark:bg-slate-800'
})

const bodyClasses = computed(() => {
  return 'bg-white dark:bg-slate-800'
})

const handleOverlayClick = () => {
  if (!props.persistent) {
    close()
  }
}

const close = () => {
  emit('update:isOpen', false)
  emit('close')
}

const cancel = () => {
  emit('cancel')
  if (!props.persistent) {
    close()
  }
}

const confirm = () => {
  emit('confirm')
}

const handleEscape = (event) => {
  if (event.key === 'Escape' && props.closeOnEscape && props.isOpen && !props.persistent) {
    close()
  }
}

// Lock body scroll when modal is open
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onMounted(() => {
  if (props.closeOnEscape) {
    document.addEventListener('keydown', handleEscape)
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* Overlay transitions */
.modal-overlay-enter-active,
.modal-overlay-leave-active {
  transition: all 0.3s ease;
}

.modal-overlay-enter-from,
.modal-overlay-leave-to {
  opacity: 0;
}

.modal-overlay-enter-to,
.modal-overlay-leave-from {
  opacity: 1;
}

/* Content transitions */
.modal-content-enter-active {
  transition: all 0.3s ease;
}

.modal-content-leave-active {
  transition: all 0.2s ease;
}

.modal-content-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(-10px);
}

.modal-content-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}

.modal-content-enter-to,
.modal-content-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* Enhanced styles */
.modal-container {
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-close-btn {
  @apply focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2;
}
</style>