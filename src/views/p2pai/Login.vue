<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-950">
    <Card class="w-full max-w-md bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border border-slate-200 dark:border-slate-700" padding="lg">
      <template #header>
        <div class="text-center">
          <div class="w-16 h-16 bg-slate-100 dark:bg-slate-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <CpuChipIcon class="h-8 w-8 text-slate-600 dark:text-slate-300" />
          </div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">P2P AI Intelligence</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-2"></p>
        </div>
      </template>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- User Type Selection -->
        <div class="space-y-3">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">
            Select User Type <span class="text-red-500">*</span>
          </label>
          <div class="grid grid-cols-1 gap-3">
            <!-- Client Option -->
            <div 
              @click="selectUserType('client')" 
              :class="[
                'p-4 border rounded-lg cursor-pointer transition-all duration-200',
                selectedUserType === 'client' 
                  ? 'border-slate-500 bg-slate-50 dark:bg-slate-700/50 dark:border-slate-400' 
                  : 'border-gray-200 dark:border-gray-600 hover:border-slate-300 dark:hover:border-slate-500'
              ]"
            >
              <div class="flex items-center space-x-3">
                <div :class="[
                  'w-4 h-4 rounded-full border-2 transition-colors',
                  selectedUserType === 'client' 
                    ? 'border-slate-500 bg-slate-500' 
                    : 'border-gray-300 dark:border-gray-500'
                ]">
                  <div v-if="selectedUserType === 'client'" class="w-full h-full rounded-full bg-white scale-50"></div>
                </div>
                <div>
                  <div class="font-medium text-gray-900 dark:text-white">
                    Client
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">
                    Training participant client node
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Server Option -->
            <div 
              @click="selectUserType('server')" 
              :class="[
                'p-4 border rounded-lg cursor-pointer transition-all duration-200',
                selectedUserType === 'server' 
                  ? 'border-slate-500 bg-slate-50 dark:bg-slate-700/50 dark:border-slate-400' 
                  : 'border-gray-200 dark:border-gray-600 hover:border-slate-300 dark:hover:border-slate-500'
              ]"
            >
              <div class="flex items-center space-x-3">
                <div :class="[
                  'w-4 h-4 rounded-full border-2 transition-colors',
                  selectedUserType === 'server' 
                    ? 'border-slate-500 bg-slate-500' 
                    : 'border-gray-300 dark:border-gray-500'
                ]">
                  <div v-if="selectedUserType === 'server'" class="w-full h-full rounded-full bg-white scale-50"></div>
                </div>
                <div>
                  <div class="font-medium text-gray-900 dark:text-white">
                    Model Server
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">
                    Training coordinator server node
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="errors.userType" class="text-red-500 text-sm">
            {{ errors.userType }}
          </div>
        </div>

        <Input
          v-model="credentials.username"
          :label="'Username'"
          :placeholder="'Enter username'"
          required
          :error="errors.username"
        />
        
        <Input
          v-model="credentials.password"
          type="password"
          :label="'Password'"
          :placeholder="'Enter password'"
          required
          :error="errors.password"
        />

        <!-- General Error Display -->
        <div v-if="errors.general" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
                Login Error
              </h3>
              <div class="mt-2 text-sm text-red-700 dark:text-red-300">
                {{ errors.general }}
              </div>
            </div>
          </div>
        </div>

        <Button
          type="submit"
          class="w-full bg-slate-700 hover:bg-slate-600 dark:bg-slate-600 dark:hover:bg-slate-500 text-white py-3 px-4 rounded-lg font-medium transition-colors"
          size="lg"
          :loading="loading"
        >
          Login
        </Button>
      </form>

      <!-- Quick Login Options -->
      <div class="mt-6 space-y-3">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200 dark:border-gray-600"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white dark:bg-slate-800 text-gray-500 dark:text-gray-400">Demo Login</span>
          </div>
        </div>
        
        <div class="grid grid-cols-1 gap-3">
          <Button 
            @click="quickLoginAsClient"
            variant="outline" 
            size="lg"
            :loading="quickLoading === 'client'"
            class="text-orange-600 dark:text-orange-400 border-orange-300 dark:border-orange-600 hover:bg-orange-50 dark:hover:bg-orange-900/20 font-medium transition-all duration-200 hover:scale-[1.02]"
          >
            <span class="flex items-center justify-center space-x-2">
              <span>👥</span>
              <span>Client Quick Demo</span>
            </span>
          </Button>
          
          <Button 
            @click="quickLoginAsServer"
            variant="outline" 
            size="lg"
            :loading="quickLoading === 'server'"
            class="text-indigo-600 dark:text-indigo-400 border-indigo-300 dark:border-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 font-medium transition-all duration-200 hover:scale-[1.02]"
          >
            <span class="flex items-center justify-center space-x-2">
              <span>🖥️</span>
              <span>Server Quick Demo</span>
            </span>
          </Button>
        </div>
      </div>

      <template #footer>
        <div class="text-center">
          <Button @click="goBack" variant="ghost" size="sm" class="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100">
            Back
          </Button>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import { CpuChipIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const quickLoading = ref('')
const selectedUserType = ref('')
const credentials = ref({
  username: '',
  password: ''
})
const errors = ref({})

const selectUserType = (type) => {
  selectedUserType.value = type
  errors.value.userType = '' // Clear error when selection is made
}

const handleLogin = async () => {
  loading.value = true
  errors.value = {}
  
  // Validate user type selection
  if (!selectedUserType.value) {
    errors.value.userType = 'Please select user type'
    loading.value = false
    return
  }
  
  try {
    const result = await authStore.login(credentials.value, 'p2pai')
    if (result.success) {
      // Set user type in auth store
      authStore.setUserType(selectedUserType.value)
      
      // Navigate to appropriate dashboard based on user type
      if (selectedUserType.value === 'client') {
        router.push('/p2pai/dashboard?role=client')
      } else if (selectedUserType.value === 'server') {
        router.push('/p2pai/dashboard?role=server')
      }
    } else {
      errors.value.general = result.error || 'Login failed'
    }
  } catch (error) {
    errors.value.general = 'An error occurred during login'
  } finally {
    loading.value = false
  }
}

const quickLoginAsClient = async () => {
  console.log('Quick login as client clicked')
  quickLoading.value = 'client'
  selectedUserType.value = 'client'
  
  try {
    const demoCredentials = {
      username: 'client_demo',
      password: 'demo123'
    }
    
    const result = await authStore.quickLogin(demoCredentials, 'p2pai')
    if (result.success) {
      authStore.setUserType('client')
      console.log('Quick login successful, navigating to dashboard...')
      await router.push('/p2pai/dashboard?role=client')
    }
    
  } catch (error) {
    console.error('Quick login error:', error)
    errors.value.general = 'An error occurred during quick login'
  } finally {
    quickLoading.value = ''
  }
}

const quickLoginAsServer = async () => {
  console.log('Quick login as server clicked')
  quickLoading.value = 'server'
  selectedUserType.value = 'server'
  
  try {
    const demoCredentials = {
      username: 'server_demo',
      password: 'demo123'
    }
    
    const result = await authStore.quickLogin(demoCredentials, 'p2pai')
    if (result.success) {
      authStore.setUserType('server')
      console.log('Quick server login successful, navigating to dashboard...')
      await router.push('/p2pai/dashboard?role=server')
    }
    
  } catch (error) {
    console.error('Server quick login error:', error)
    errors.value.general = 'An error occurred during quick login'
  } finally {
    quickLoading.value = ''
  }
}

const goBack = () => {
  router.push('/')
}
</script>