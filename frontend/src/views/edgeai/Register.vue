<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-950">
    <Card class="w-full max-w-md bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border border-slate-200 dark:border-slate-700" padding="lg">
      <template #header>
        <div class="text-center">
          <div class="w-16 h-16 bg-slate-100 dark:bg-slate-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <UserPlusIcon class="h-8 w-8 text-slate-600 dark:text-slate-300" />
          </div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Edge AI Intelligence</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">Create New Account</p>
        </div>
      </template>

      <form @submit.prevent="handleRegister" class="space-y-6">
        <Input
          v-model="formData.name"
          label="Username"
          placeholder="Enter username"
          required
          :error="errors.name"
        />
        
        <Input
          v-model="formData.email"
          type="email"
          label="Email"
          placeholder="Enter email address"
          required
          :error="errors.email"
        />
        
        <Input
          v-model="formData.password"
          type="password"
          label="Password"
          placeholder="Enter password (at least 6 characters)"
          required
          :error="errors.password"
        />
        
        <Input
          v-model="formData.confirmPassword"
          type="password"
          label="Confirm Password"
          placeholder="Enter password again"
          required
          :error="errors.confirmPassword"
        />

        <div v-if="errors.general" class="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
          {{ errors.general }}
        </div>

        <Button
          type="submit"
          class="w-full bg-slate-700 hover:bg-slate-600 dark:bg-slate-600 dark:hover:bg-slate-500 text-white py-3 px-4 rounded-lg font-medium transition-colors"
          size="lg"
          :loading="loading"
        >
          Create Account
        </Button>
      </form>

      <!-- Login Link -->
      <div class="mt-6 space-y-3">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200 dark:border-gray-600"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white dark:bg-slate-800 text-gray-500 dark:text-gray-400">Already have an account?</span>
          </div>
        </div>
        
        <Button 
          @click="goToLogin"
          variant="outline" 
          size="lg"
          class="w-full text-blue-600 dark:text-blue-400 border-blue-300 dark:border-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 font-medium transition-all duration-200 hover:scale-[1.02]"
        >
          <span class="flex items-center justify-center space-x-2">
            <span>🔑</span>
            <span>Login Now</span>
          </span>
        </Button>
      </div>

      <template #footer>
        <div class="text-center">
          <Button @click="goBack" variant="ghost" size="sm" class="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100">
            Back to Home
          </Button>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import { UserPlusIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const formData = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  general: ''
})

// 表单验证
const validateForm = () => {
  // 清空之前的错误
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })

  let isValid = true

  // Validate username
  if (!formData.name.trim()) {
    errors.name = 'Username is required'
    isValid = false
  } else if (formData.name.length < 2) {
    errors.name = 'Username must be at least 2 characters'
    isValid = false
  }

  // Validate email
  if (!formData.email.trim()) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }

  // Validate password
  if (!formData.password) {
    errors.password = 'Password is required'
    isValid = false
  } else if (formData.password.length < 6) {
    errors.password = 'Password must be at least 6 characters'
    isValid = false
  }

  // Validate confirm password
  if (!formData.confirmPassword) {
    errors.confirmPassword = 'Please confirm password'
    isValid = false
  } else if (formData.password !== formData.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  return isValid
}

const handleRegister = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true
  
  try {
    const userData = {
      name: formData.name.trim(),
      email: formData.email.trim(),
      password: formData.password
    }
    
    const result = await authStore.register(userData, 'edgeai')
    
    if (result.success) {
      router.push('/edgeai/dashboard')
    } else {
      errors.general = result.error || 'Registration failed, please try again'
    }
  } catch (error) {
    console.error('Register error:', error)
    errors.general = 'Registration failed, please check your network connection'
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/edgeai/login')
}

const goBack = () => {
  router.push('/')
}
</script>
