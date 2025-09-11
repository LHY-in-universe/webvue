<template>
  <div :class="containerClasses">
    <!-- Navigation -->
    <AppNavbar
      :title="title"
      :icon="icon"
      :icon-color="iconColor"
      :username="username"
      :is-dark="isDark"
      :variant="navVariant"
      :max-width="maxWidth"
      :show-back-button="showBackButton"
      :show-theme-toggle="showThemeToggle"
      :show-logout="showLogout"
      :show-user-info="showUserInfo"
      :logout-text="logoutText"
      @back="$emit('back')"
      @logout="$emit('logout')"
      @theme-toggle="$emit('themeToggle')"
    >
      <!-- Pass through navbar slots -->
      <template v-if="$slots.navIcon" #icon>
        <slot name="navIcon" />
      </template>
      <template v-if="$slots.navTitle" #title>
        <slot name="navTitle" />
      </template>
      <template v-if="$slots.navCenter" #center>
        <slot name="navCenter" />
      </template>
      <template v-if="$slots.navActions" #actions>
        <slot name="navActions" />
      </template>
      <template v-if="$slots.navRight" #right>
        <slot name="navRight" />
      </template>
    </AppNavbar>

    <!-- Main Content -->
    <main :class="contentClasses">
      <!-- Page Header (optional) -->
      <header v-if="$slots.header || pageTitle || pageDescription" class="mb-8">
        <slot name="header">
          <div v-if="centerHeader" class="text-center">
            <h1 v-if="pageTitle" :class="pageTitleClasses">
              {{ pageTitle }}
            </h1>
            <p v-if="pageDescription" :class="pageDescriptionClasses">
              {{ pageDescription }}
            </p>
          </div>
          <div v-else>
            <div class="flex items-center justify-between">
              <div>
                <h1 v-if="pageTitle" :class="pageTitleClasses">
                  {{ pageTitle }}
                </h1>
                <p v-if="pageDescription" :class="pageDescriptionClasses">
                  {{ pageDescription }}
                </p>
              </div>
              <div v-if="$slots.headerActions">
                <slot name="headerActions" />
              </div>
            </div>
          </div>
        </slot>
      </header>

      <!-- Main Content Area -->
      <div :class="mainContentClasses">
        <slot />
      </div>

      <!-- Footer (optional) -->
      <footer v-if="$slots.footer" class="mt-8">
        <slot name="footer" />
      </footer>
    </main>

    <!-- Fixed Elements (optional) -->
    <div v-if="$slots.fixed" class="fixed">
      <slot name="fixed" />
    </div>

    <!-- Modals/Overlays (optional) -->
    <div v-if="$slots.overlays">
      <slot name="overlays" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AppNavbar from '@/components/ui/AppNavbar.vue'

const props = defineProps({
  // Layout props
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'centered', 'wide', 'dashboard'].includes(value)
  },
  background: {
    type: String,
    default: 'default',
    validator: value => ['default', 'slate', 'white', 'transparent'].includes(value)
  },
  maxWidth: {
    type: String,
    default: '7xl',
    validator: value => ['4xl', '6xl', '7xl', 'full'].includes(value)
  },
  padding: {
    type: String,
    default: 'default',
    validator: value => ['none', 'sm', 'default', 'lg'].includes(value)
  },
  
  // Navigation props
  title: String,
  icon: [Object, Function, String],
  iconColor: {
    type: String,
    default: 'text-gray-600 dark:text-gray-300'
  },
  navVariant: {
    type: String,
    default: 'default'
  },
  showBackButton: {
    type: Boolean,
    default: false
  },
  showThemeToggle: {
    type: Boolean,
    default: true
  },
  showLogout: {
    type: Boolean,
    default: true
  },
  showUserInfo: {
    type: Boolean,
    default: true
  },
  logoutText: {
    type: String,
    default: 'Logout'
  },
  username: String,
  isDark: {
    type: Boolean,
    default: false
  },
  
  // Page content props
  pageTitle: String,
  pageDescription: String,
  centerHeader: {
    type: Boolean,
    default: false
  }
})

defineEmits(['back', 'logout', 'themeToggle'])

const containerClasses = computed(() => {
  const backgrounds = {
    default: 'min-h-screen bg-gray-50 dark:bg-gray-900',
    slate: 'min-h-screen bg-slate-50 dark:bg-slate-900',
    white: 'min-h-screen bg-white dark:bg-gray-900',
    transparent: 'min-h-screen'
  }
  return backgrounds[props.background] || backgrounds.default
})

const contentClasses = computed(() => {
  const maxWidths = {
    '4xl': 'max-w-4xl',
    '6xl': 'max-w-6xl',
    '7xl': 'max-w-7xl',
    'full': 'max-w-full'
  }
  
  const paddings = {
    none: '',
    sm: 'px-4 py-4',
    default: 'px-4 sm:px-6 lg:px-8 py-8',
    lg: 'px-6 py-12'
  }
  
  return `${maxWidths[props.maxWidth]} mx-auto ${paddings[props.padding]}`
})

const mainContentClasses = computed(() => {
  const variants = {
    default: '',
    centered: 'flex flex-col items-center',
    wide: 'w-full',
    dashboard: 'space-y-6'
  }
  return variants[props.variant] || variants.default
})

const pageTitleClasses = computed(() => {
  return 'text-3xl font-bold text-gray-900 dark:text-white mb-4'
})

const pageDescriptionClasses = computed(() => {
  return 'text-lg text-gray-600 dark:text-gray-400'
})
</script>

<style scoped>
.fixed {
  z-index: 1000;
}
</style>