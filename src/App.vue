<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useAuthStore } from './stores/auth'
import { useThemeStore } from './stores/theme'
import { useUIStore } from './stores/ui'
import Toast from './components/ui/Toast.vue'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const uiStore = useUIStore()

let themeCleanup = null

onMounted(() => {
  try {
    // Initialize all stores
    authStore.initializeAuth()
    themeCleanup = themeStore.initializeTheme() // Store cleanup function
    uiStore.initializeUI()
    
    console.log('App and stores initialized successfully')
  } catch (error) {
    console.warn('Store initialization failed:', error)
  }
})

onUnmounted(() => {
  // Cleanup theme listener
  if (themeCleanup) {
    themeCleanup()
  }
  console.log('App unmounted')
})
</script>

<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-700">
    <RouterView />
    
    <!-- Global Toast Notifications -->
    <Toast />
  </div>
</template>

<style>
/* Global styles are in main.css */
</style>
