<template>
  <nav :class="navClasses">
    <div :class="containerClasses">
      <div class="flex justify-between h-16">
        <!-- Left Side -->
        <div class="flex items-center">
          <!-- Back Button (optional) -->
          <button 
            v-if="showBackButton"
            @click="handleBack"
            :class="backButtonClasses"
          >
            <ArrowLeftIcon class="w-5 h-5" />
          </button>
          
          <!-- Icon -->
          <div 
            v-if="icon || $slots.icon"
            :class="iconContainerClasses"
          >
            <slot name="icon">
              <component 
                :is="icon" 
                :class="iconClasses"
              />
            </slot>
          </div>
          
          <!-- Title -->
          <h1 :class="titleClasses">
            <slot name="title">{{ title }}</slot>
          </h1>
        </div>
        
        <!-- Center Content (optional) -->
        <div v-if="$slots.center" class="flex items-center">
          <slot name="center" />
        </div>
        
        <!-- Right Side -->
        <div class="flex items-center space-x-4">
          <!-- User Info (optional) -->
          <span 
            v-if="showUserInfo && username" 
            class="text-sm text-gray-600 dark:text-gray-400 hidden md:block"
          >
            Welcome, {{ username }}
          </span>
          
          <!-- Custom Actions Slot -->
          <slot name="actions" />
          
          <!-- Theme Toggle -->
          <Button 
            v-if="showThemeToggle"
            @click="toggleTheme" 
            variant="ghost" 
            size="sm"
            iconOnly
            :leftIcon="isDark ? SunIcon : MoonIcon"
          />
          
          <!-- Logout Button -->
          <Button 
            v-if="showLogout"
            @click="handleLogout" 
            variant="ghost" 
            size="sm"
          >
            {{ logoutText }}
          </Button>
          
          <!-- Custom Right Content -->
          <slot name="right" />
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useAuthStore } from '@/stores/auth'
import Button from './Button.vue'
import { ArrowLeftIcon, SunIcon, MoonIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  title: String,
  icon: [Object, Function, String],
  iconColor: {
    type: String,
    default: 'text-gray-600 dark:text-gray-300'
  },
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'glass', 'minimal'].includes(value)
  },
  maxWidth: {
    type: String,
    default: '7xl',
    validator: value => ['4xl', '6xl', '7xl', 'full'].includes(value)
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
  }
})

const emit = defineEmits(['back', 'logout', 'themeToggle'])

const router = useRouter()
const themeStore = useThemeStore()
const authStore = useAuthStore()

const navClasses = computed(() => {
  const variants = {
    default: 'bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700',
    glass: 'glass-effect shadow-soft border-b border-slate-200 dark:border-slate-700',
    minimal: 'bg-transparent border-b border-gray-200 dark:border-gray-700'
  }
  return variants[props.variant] || variants.default
})

const containerClasses = computed(() => {
  const maxWidths = {
    '4xl': 'max-w-4xl',
    '6xl': 'max-w-6xl', 
    '7xl': 'max-w-7xl',
    'full': 'max-w-full'
  }
  return `${maxWidths[props.maxWidth]} mx-auto px-4 sm:px-6 lg:px-8`
})

const backButtonClasses = computed(() => {
  return 'mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors micro-bounce'
})

const iconContainerClasses = computed(() => {
  const base = 'flex items-center justify-center mr-3'
  if (props.variant === 'glass') {
    return `${base} w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-lg micro-bounce hover-glow-primary`
  }
  return base
})

const iconClasses = computed(() => {
  const size = props.variant === 'glass' ? 'h-5 w-5' : 'h-8 w-8'
  return `${size} ${props.iconColor}`
})

const titleClasses = computed(() => {
  const base = 'font-semibold'
  if (props.variant === 'glass') {
    return `${base} text-xl text-gradient text-shadow-soft`
  }
  return `${base} text-xl text-gray-900 dark:text-white`
})

const handleBack = () => {
  emit('back')
  if (!props.showBackButton) return
  router.back()
}

const handleLogout = () => {
  emit('logout')
  if (authStore?.logout) {
    authStore.logout()
  }
  router.push('/')
}

const toggleTheme = (event) => {
  emit('themeToggle', event)
  if (themeStore?.toggleTheme) {
    themeStore.toggleTheme(event)
  }
}
</script>

<style scoped>
.text-gradient {
  @apply bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent;
}

.text-shadow-soft {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.glass-effect {
  @apply backdrop-blur-sm bg-white/80 dark:bg-slate-800/80;
}

.shadow-soft {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.micro-bounce:hover {
  transform: scale(1.05);
}

.hover-glow-primary:hover {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}
</style>