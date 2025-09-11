<template>
  <div :class="containerClasses">
    <!-- Mobile Header -->
    <div v-if="isMobile" :class="mobileHeaderClasses">
      <div class="flex items-center justify-between">
        <!-- Left side - Menu toggle/back button -->
        <div class="flex items-center space-x-2">
          <button
            v-if="showMenuToggle"
            @click="toggleMobileMenu"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            :aria-label="mobileMenuOpen ? 'Close menu' : 'Open menu'"
          >
            <Bars3Icon v-if="!mobileMenuOpen" class="w-6 h-6 text-gray-600 dark:text-gray-400" />
            <XMarkIcon v-else class="w-6 h-6 text-gray-600 dark:text-gray-400" />
          </button>
          
          <button
            v-if="showBackButton"
            @click="$emit('back')"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            aria-label="Go back"
          >
            <ArrowLeftIcon class="w-6 h-6 text-gray-600 dark:text-gray-400" />
          </button>
          
          <div v-if="title" class="flex items-center space-x-2">
            <component :is="titleIcon" v-if="titleIcon" class="w-5 h-5 text-gray-600 dark:text-gray-400" />
            <h1 class="text-lg font-semibold text-gray-900 dark:text-white truncate">{{ title }}</h1>
          </div>
        </div>
        
        <!-- Right side - Actions -->
        <div class="flex items-center space-x-1">
          <slot name="mobile-actions" />
          <button
            v-if="showMoreActions"
            @click="showActionMenu = !showActionMenu"
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors relative"
            aria-label="More actions"
          >
            <EllipsisVerticalIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
            
            <!-- Action Menu Dropdown -->
            <div
              v-if="showActionMenu"
              class="absolute right-0 top-full mt-1 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50"
              @click.stop
            >
              <slot name="action-menu" />
            </div>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Mobile Menu Overlay -->
    <div
      v-if="isMobile && mobileMenuOpen && showMenuToggle"
      class="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
      @click="closeMobileMenu"
    ></div>
    
    <!-- Mobile Menu Sidebar -->
    <div
      v-if="isMobile && showMenuToggle"
      :class="[
        'fixed left-0 top-0 h-full w-72 bg-white dark:bg-gray-800 shadow-xl z-50 transition-transform duration-300 ease-in-out',
        mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <div class="p-4 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <slot name="menu-header" />
          </div>
          <button
            @click="closeMobileMenu"
            class="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            aria-label="Close menu"
          >
            <XMarkIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </button>
        </div>
      </div>
      
      <div class="p-4 overflow-y-auto h-full pb-20">
        <slot name="mobile-menu" />
      </div>
    </div>
    
    <!-- Main Content Area -->
    <main :class="mainContentClasses">
      <!-- Desktop/Tablet Layout -->
      <div v-if="!isMobile" :class="desktopLayoutClasses">
        <!-- Sidebar -->
        <aside v-if="$slots.sidebar" :class="sidebarClasses">
          <slot name="sidebar" />
        </aside>
        
        <!-- Main Content -->
        <div :class="desktopMainClasses">
          <slot />
        </div>
        
        <!-- Right Panel -->
        <aside v-if="$slots['right-panel']" :class="rightPanelClasses">
          <slot name="right-panel" />
        </aside>
      </div>
      
      <!-- Mobile Layout -->
      <div v-else :class="mobileLayoutClasses">
        <slot />
      </div>
    </main>
    
    <!-- Mobile Bottom Navigation -->
    <nav v-if="isMobile && showBottomNav" :class="bottomNavClasses">
      <slot name="bottom-nav" />
    </nav>
    
    <!-- Floating Action Button (Mobile) -->
    <div v-if="isMobile && showFab" :class="fabClasses">
      <slot name="fab" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import {
  Bars3Icon,
  XMarkIcon,
  ArrowLeftIcon,
  EllipsisVerticalIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  title: String,
  titleIcon: [Object, Function],
  showMenuToggle: {
    type: Boolean,
    default: true
  },
  showBackButton: {
    type: Boolean,
    default: false
  },
  showMoreActions: {
    type: Boolean,
    default: false
  },
  showBottomNav: {
    type: Boolean,
    default: false
  },
  showFab: {
    type: Boolean,
    default: false
  },
  sidebarWidth: {
    type: String,
    default: 'w-64'
  },
  rightPanelWidth: {
    type: String,
    default: 'w-80'
  },
  maxWidth: {
    type: String,
    default: 'max-w-none'
  },
  padding: {
    type: String,
    default: 'auto' // 'auto', 'none', 'sm', 'md', 'lg'
  }
})

const emit = defineEmits(['back', 'menu-toggle'])

// Responsive functionality
const { isMobile, isTablet, containerPadding, getResponsiveValue } = useResponsive()

// Mobile state
const mobileMenuOpen = ref(false)
const showActionMenu = ref(false)

// Computed classes
const containerClasses = computed(() => {
  const base = 'min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col'
  return base
})

const mobileHeaderClasses = computed(() => {
  return [
    'sticky top-0 z-30 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700',
    'px-4 py-3 shadow-sm'
  ]
})

const mainContentClasses = computed(() => {
  const base = 'flex-1 relative'
  const paddingClass = props.padding === 'auto' ? containerPadding.value : 
    props.padding === 'none' ? '' :
    `p-${props.padding}`
  
  return [base, paddingClass]
})

const desktopLayoutClasses = computed(() => {
  return 'flex h-full'
})

const sidebarClasses = computed(() => {
  return [
    props.sidebarWidth,
    'flex-shrink-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700',
    'overflow-y-auto'
  ]
})

const desktopMainClasses = computed(() => {
  const base = 'flex-1 overflow-x-hidden'
  const maxWidthClass = props.maxWidth
  return [base, maxWidthClass]
})

const rightPanelClasses = computed(() => {
  return [
    props.rightPanelWidth,
    'flex-shrink-0 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700',
    'overflow-y-auto'
  ]
})

const mobileLayoutClasses = computed(() => {
  const base = 'flex flex-col min-h-0'
  const bottomPadding = props.showBottomNav ? 'pb-16' : ''
  return [base, bottomPadding]
})

const bottomNavClasses = computed(() => {
  return [
    'fixed bottom-0 left-0 right-0 z-30',
    'bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700',
    'px-4 py-2 shadow-lg'
  ]
})

const fabClasses = computed(() => {
  return [
    'fixed bottom-4 right-4 z-30',
    props.showBottomNav && 'bottom-20'
  ]
})

// Methods
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
  emit('menu-toggle', mobileMenuOpen.value)
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
  emit('menu-toggle', false)
}

// Handle escape key
const handleEscape = (event) => {
  if (event.key === 'Escape') {
    if (showActionMenu.value) {
      showActionMenu.value = false
    } else if (mobileMenuOpen.value) {
      closeMobileMenu()
    }
  }
}

// Close action menu when clicking outside
const handleClickOutside = (event) => {
  if (showActionMenu.value && !event.target.closest('[aria-label="More actions"]')) {
    showActionMenu.value = false
  }
}

// Watch for mobile changes to close menu
watch(isMobile, (newValue) => {
  if (!newValue && mobileMenuOpen.value) {
    closeMobileMenu()
  }
})

// Lifecycle
onMounted(() => {
  document.addEventListener('keydown', handleEscape)
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Prevent body scroll when mobile menu is open */
.mobile-menu-open {
  overflow: hidden;
}

/* Custom scrollbar for sidebar */
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.4);
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.6);
}

/* Mobile-specific optimizations */
@media (max-width: 768px) {
  /* Ensure touch targets are at least 44px */
  button {
    min-height: 44px;
    min-width: 44px;
  }
  
  /* Optimize tap highlights */
  button, a {
    -webkit-tap-highlight-color: rgba(59, 130, 246, 0.1);
  }
}

/* Prevent zoom on double tap */
@media (max-width: 768px) {
  * {
    touch-action: manipulation;
  }
}

/* Safe area handling for iOS */
@supports (padding: max(0px)) {
  .mobile-header {
    padding-top: max(12px, env(safe-area-inset-top));
  }
  
  .bottom-nav {
    padding-bottom: max(8px, env(safe-area-inset-bottom));
  }
  
  .fab {
    bottom: max(16px, calc(env(safe-area-inset-bottom) + 16px));
    right: max(16px, env(safe-area-inset-right));
  }
}
</style>