<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Navigation Header -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Left Side -->
          <div class="flex items-center">
            <button 
              @click="$emit('go-back')" 
              class="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            
            <div class="flex items-center space-x-3">
              <div 
                class="w-8 h-8 rounded-lg flex items-center justify-center"
                :class="iconBgClass"
              >
                <component :is="icon" class="h-5 w-5" :class="iconClass" />
              </div>
              <div>
                <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                  {{ title }}
                </h1>
                <div v-if="subtitle" class="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                  <span>{{ subtitle }}</span>
                  <div 
                    v-if="status"
                    class="flex items-center space-x-1"
                  >
                    <div 
                      class="w-2 h-2 rounded-full"
                      :class="getStatusColor(status)"
                    ></div>
                    <span class="capitalize">{{ status }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Right Side Controls -->
          <div class="flex items-center space-x-3">
            <!-- Custom Header Actions Slot -->
            <slot name="header-actions" />
            
            <!-- Keyboard Shortcuts Help -->
            <Button 
              v-if="showShortcuts"
              @click="$emit('show-shortcuts')" 
              variant="ghost" 
              size="sm"
              title="Keyboard Shortcuts (H)"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </Button>
            
            <!-- Fullscreen Toggle -->
            <Button 
              v-if="enableFullscreen"
              @click="toggleFullscreen" 
              variant="ghost" 
              size="sm"
              :title="isFullscreen ? 'Exit Fullscreen (F11)' : 'Enter Fullscreen (F11)'"
            >
              <svg v-if="!isFullscreen" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 9V4.5M9 9H4.5M9 9L3.5 3.5M15 9V4.5M15 9h4.5M15 9l5.5-5.5M9 15v4.5M9 15H4.5M9 15l-5.5 5.5M15 15v4.5m0-4.5h4.5m-4.5 0l5.5 5.5"></path>
              </svg>
            </Button>
            
            <!-- Theme Toggle -->
            <SimpleThemeToggle v-if="showThemeToggle" size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <div 
      class="visualization-content"
      :class="{
        'max-w-7xl mx-auto px-6 py-8': !isFullscreen,
        'px-2 py-2': isFullscreen
      }"
    >
      <!-- Project/Context Info Header -->
      <div v-if="showInfoHeader && !isFullscreen" class="mb-8">
        <Card class="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm border border-gray-200 dark:border-gray-700">
          <div class="p-6">
            <slot name="info-header" />
          </div>
        </Card>
      </div>
      
      <!-- Control Panel -->
      <div v-if="showControls && !isFullscreen" class="mb-6">
        <Card class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
          <div class="p-6">
            <slot name="controls" />
          </div>
        </Card>
      </div>
      
      <!-- Main Visualization Content -->
      <div class="visualization-main">
        <slot name="main-content" />
      </div>
      
      <!-- Additional Sections -->
      <div v-if="!isFullscreen" class="additional-sections space-y-8 mt-8">
        <slot name="additional-content" />
      </div>
    </div>
    
    <!-- Floating Action Button (FAB) -->
    <Transition name="fab">
      <div
        v-if="showFab"
        class="fixed bottom-6 right-6 z-50"
      >
        <Button
          @click="$emit('fab-click')"
          class="w-14 h-14 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          :class="fabClass"
        >
          <component :is="fabIcon" class="w-6 h-6" />
        </Button>
      </div>
    </Transition>
    
    <!-- Keyboard Shortcuts Modal -->
    <Transition name="modal">
      <div
        v-if="showShortcutsModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="$emit('hide-shortcuts')"
      >
        <Card class="w-full max-w-md mx-4">
          <template #header>
            <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Keyboard Shortcuts</h3>
              <Button @click="$emit('hide-shortcuts')" variant="ghost" size="sm">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </Button>
            </div>
          </template>
          <div class="p-6">
            <slot name="shortcuts" />
          </div>
        </Card>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: String,
  status: String,
  icon: {
    type: [String, Object, Function],
    required: true
  },
  variant: {
    type: String,
    default: 'primary',
    validator: value => ['primary', 'secondary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  showInfoHeader: {
    type: Boolean,
    default: true
  },
  showControls: {
    type: Boolean,
    default: true
  },
  showShortcuts: {
    type: Boolean,
    default: true
  },
  showShortcutsModal: {
    type: Boolean,
    default: false
  },
  showThemeToggle: {
    type: Boolean,
    default: true
  },
  enableFullscreen: {
    type: Boolean,
    default: true
  },
  showFab: {
    type: Boolean,
    default: false
  },
  fabIcon: [String, Object, Function],
  fabVariant: {
    type: String,
    default: 'primary'
  }
})

const emit = defineEmits([
  'go-back', 
  'show-shortcuts', 
  'hide-shortcuts', 
  'fab-click',
  'fullscreen-change'
])

const themeStore = useThemeStore()
const isFullscreen = ref(false)

// Computed classes based on variant
const iconBgClass = computed(() => {
  const variants = {
    primary: 'bg-blue-100 dark:bg-blue-900',
    secondary: 'bg-gray-100 dark:bg-gray-700',
    success: 'bg-green-100 dark:bg-green-900',
    warning: 'bg-yellow-100 dark:bg-yellow-900',
    danger: 'bg-red-100 dark:bg-red-900',
    info: 'bg-cyan-100 dark:bg-cyan-900'
  }
  return variants[props.variant]
})

const iconClass = computed(() => {
  const variants = {
    primary: 'text-blue-600 dark:text-blue-400',
    secondary: 'text-gray-600 dark:text-gray-400',
    success: 'text-green-600 dark:text-green-400',
    warning: 'text-yellow-600 dark:text-yellow-400',
    danger: 'text-red-600 dark:text-red-400',
    info: 'text-cyan-600 dark:text-cyan-400'
  }
  return variants[props.variant]
})

const fabClass = computed(() => {
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-600 hover:bg-gray-700 text-white',
    success: 'bg-green-600 hover:bg-green-700 text-white',
    warning: 'bg-yellow-600 hover:bg-yellow-700 text-white',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    info: 'bg-cyan-600 hover:bg-cyan-700 text-white'
  }
  return variants[props.fabVariant]
})

// Status color helper
const getStatusColor = (status) => {
  const colors = {
    online: 'bg-green-500',
    offline: 'bg-gray-400',
    training: 'bg-blue-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500',
    paused: 'bg-yellow-500',
    completed: 'bg-green-500'
  }
  return colors[status] || 'bg-gray-400'
}

// Fullscreen functionality
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    document.exitFullscreen()
    isFullscreen.value = false
  }
  emit('fullscreen-change', isFullscreen.value)
}

// Keyboard shortcuts
const handleKeydown = (event) => {
  // F11 for fullscreen
  if (event.key === 'F11' && props.enableFullscreen) {
    event.preventDefault()
    toggleFullscreen()
  }
  
  // H for help
  if (event.key === 'h' || event.key === 'H') {
    if (props.showShortcuts && !props.showShortcutsModal) {
      emit('show-shortcuts')
    }
  }
  
  // ESC to close modals
  if (event.key === 'Escape') {
    if (props.showShortcutsModal) {
      emit('hide-shortcuts')
    }
  }
}

// Fullscreen change listener
const handleFullscreenChange = () => {
  isFullscreen.value = !!document.fullscreenElement
  emit('fullscreen-change', isFullscreen.value)
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('fullscreenchange', handleFullscreenChange)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
})
</script>

<style scoped>
.visualization-content {
  transition: all 0.3s ease;
}

/* Transition styles */
.fab-enter-active,
.fab-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fab-enter-from,
.fab-leave-to {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.95) translateY(-20px);
}
</style>