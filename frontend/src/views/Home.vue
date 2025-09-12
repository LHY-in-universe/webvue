<template>
  <div class="home-container">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-soft border-b border-gray-200 dark:border-gray-700">
      <div class="container-app">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <h1 class="text-heading-2 font-bold text-gray-900 dark:text-white">
                OpenTMP 
              </h1>
            </div>
          </div>
          
          <div class="flex items-center space-x-6">
            <!-- 现代主题开关 -->
            <SimpleThemeToggle 
              :show-label="true"
              size="md"
            />
            
            <!-- Demo Toast Button -->
            <Button @click="showDemoToast" variant="outline" size="sm">
              Demo
            </Button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="bg-slate-900 dark:bg-slate-950 text-white relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-slate-800/50 to-slate-900/50"></div>
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10">
        <div class="text-center">
          <h1 class="text-4xl md:text-6xl font-bold mb-6 tracking-tight text-white">
            OpenTMP LLM Engine
          </h1>
          <p class="text-xl md:text-2xl text-slate-300 mb-8 font-normal">
            Secure and Efficient Distributed Machine Learning Solutions
          </p>

        </div>
      </div>
    </div>

    <!-- Modules Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">


      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- P2P AI Module -->
        <ModuleCard
          title="P2P AI Intelligence"

          :icon="CpuChipIcon"
          module-id="p2pai"
          variant="primary"
          @click="handleModuleClick"
        />

        <!-- EdgeAI Module -->
        <ModuleCard
          title="Edge AI Intelligence"

          :icon="ComputerDesktopIcon"
          module-id="edgeai"
          variant="success"
          @click="handleModuleClick"
        />

      </div>

      <!-- Feature Highlights -->
      <div class="mt-20">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="w-12 h-12 bg-slate-100 dark:bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-4">
              <ShieldCheckIcon class="h-6 w-6 text-slate-600 dark:text-slate-300" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Secure & Reliable</h3>
            <p class="text-gray-600 dark:text-gray-400"></p>
          </div>
          
          <div class="text-center">
            <div class="w-12 h-12 bg-slate-100 dark:bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-4">
              <BoltIcon class="h-6 w-6 text-slate-600 dark:text-slate-300" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">High Performance</h3>
            <p class="text-gray-600 dark:text-gray-400"></p>
          </div>
          
          <div class="text-center">
            <div class="w-12 h-12 bg-slate-100 dark:bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-4">
              <GlobeAltIcon class="h-6 w-6 text-slate-600 dark:text-slate-300" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Easy to Scale</h3>
            <p class="text-gray-600 dark:text-gray-400"></p>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-slate-900 dark:bg-slate-950 text-white border-t border-slate-800 dark:border-slate-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="text-center">
          <h3 class="text-xl font-semibold mb-2 text-white"> OpenTMP LLM Engine</h3>
          <p class="text-slate-400 mb-6">
            
          </p>
          <div class="flex justify-center space-x-6 text-sm text-slate-400">
            <span>© OpenTMP</span>
            <span>•</span>
            <span>Modern Architecture</span>
            <span>•</span>
            <span>Open Source Friendly</span>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import ModuleCard from '@/components/ui/ModuleCard.vue'
import { 
  CpuChipIcon,
  ComputerDesktopIcon,
  CubeIcon,
  KeyIcon,
  ShieldCheckIcon,
  BoltIcon,
  GlobeAltIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()

// Reactive stores
const themeStore = ref(null)
const uiStore = ref(null)
const isDark = ref(false)

onMounted(async () => {
  try {
    // 动态导入stores
    const { useThemeStore } = await import('@/stores/theme')
    const { useUIStore } = await import('@/stores/ui')
    
    themeStore.value = useThemeStore()
    uiStore.value = useUIStore()
    
    // 初始化主题状态
    isDark.value = themeStore.value?.isDark || false
  } catch (error) {
    console.warn('Store initialization failed:', error)
  }
})

// Theme is now handled by UnifiedThemeToggle component

const showDemoToast = () => {
  if (uiStore.value?.addNotification) {
    const toastTypes = ['success', 'error', 'warning', 'info']
    const randomType = toastTypes[Math.floor(Math.random() * toastTypes.length)]
    
    const messages = {
      success: 'Operation completed successfully!',
      error: 'An error occurred',
      warning: 'Please note this warning',
      info: 'This is an information tip'
    }
    
    uiStore.value.addNotification({
      type: randomType,
      title: `${randomType.toUpperCase()} Demo`,
      message: messages[randomType],
      actions: [
        {
          label: 'View Details',
          handler: () => console.log('Action clicked')
        }
      ]
    })
  } else {
    console.log('Demo toast clicked (stores not loaded)')
  }
}

const selectModule = (module) => {
  // Clear any previous session data
  localStorage.removeItem('userType')
  localStorage.removeItem('userData')
  
  // Set current module
  localStorage.setItem('currentModule', module)
  
  // Show loading notification
  if (uiStore.value?.notifyInfo) {
    uiStore.value.notifyInfo(
      `Entering ${module.toUpperCase()} module...`,
      'Module Switch'
    )
  } else {
    console.log(`Entering ${module.toUpperCase()} module...`)
  }
  
  // Navigate to module login
  setTimeout(() => {
    router.push(`/${module}/login`)
  }, 500)
}

const handleModuleClick = (event) => {
  selectModule(event.moduleId)
}
</script>