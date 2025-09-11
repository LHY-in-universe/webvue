<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-900 dark:bg-slate-950">
    <Card class="w-full max-w-md bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border border-slate-200 dark:border-slate-700" padding="lg">
      <template #header>
        <div class="text-center">
          <div class="w-16 h-16 bg-slate-100 dark:bg-slate-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <KeyIcon class="h-8 w-8 text-slate-600 dark:text-slate-300" />
          </div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Cryptographic Security</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">Login to Cryptographic Security Platform</p>
        </div>
      </template>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <Input
          v-model="credentials.username"
          label="Username"
          placeholder="Enter username or try: crypto_demo"
          required
        />
        
        <Input
          v-model="credentials.password"
          type="password"
          label="Password"
          placeholder="Enter password or try: demo123"
          required
        />
        
        <div class="text-xs text-gray-500 dark:text-gray-400 text-center">
          Demo credentials: <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded">crypto_demo</code> / <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded">demo123</code>
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

      <!-- Quick Login -->
      <div class="mt-6 space-y-3">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200 dark:border-gray-600"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white dark:bg-slate-800 text-gray-500 dark:text-gray-400">Demo Login</span>
          </div>
        </div>
        
        <Button 
          @click="quickLogin"
          variant="outline" 
          size="lg"
          :loading="quickLoading"
          class="w-full text-purple-600 dark:text-purple-400 border-purple-300 dark:border-purple-600 hover:bg-purple-50 dark:hover:bg-purple-900/20 font-medium transition-all duration-200 hover:scale-[1.02]"
        >
          <span class="flex items-center justify-center space-x-2">
            <span>🔐</span>
            <span>Quick Demo Login</span>
          </span>
        </Button>
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
import { KeyIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const quickLoading = ref(false)
const credentials = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  loading.value = true
  
  try {
    const result = await authStore.login(credentials.value, 'crypto')
    if (result.success) {
      router.push('/crypto/dashboard')
    }
  } catch (error) {
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}

const quickLogin = async () => {
  quickLoading.value = true
  
  try {
    const demoCredentials = {
      username: 'crypto_demo',
      password: 'demo123'
    }
    
    const result = await authStore.quickLogin(demoCredentials, 'crypto')
    if (result.success) {
      router.push('/crypto/dashboard')
    }
  } catch (error) {
    console.error('Quick login error:', error)
  } finally {
    quickLoading.value = false
  }
}

const goBack = () => {
  router.push('/')
}
</script>