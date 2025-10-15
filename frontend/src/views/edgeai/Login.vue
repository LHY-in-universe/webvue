<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-950">
    <!-- Notification Manager -->
    <NotificationManager />
    
    <Card class="w-full max-w-md bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border border-slate-200 dark:border-slate-700" padding="lg">
      <template #header>
        <div class="text-center">
          <div class="w-16 h-16 bg-slate-100 dark:bg-slate-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <ComputerDesktopIcon class="h-8 w-8 text-slate-600 dark:text-slate-300" />
          </div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Edge AI Intelligence</h2>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">
            {{ isLogin ? 'Login to Edge AI Intelligence Platform' : 'Create your Edge AI account' }}
          </p>
        </div>
      </template>

      <!-- Tab Navigation -->
      <div class="mb-6">
        <div class="flex bg-gray-100 dark:bg-slate-700 rounded-lg p-1">
          <button
            @click="isLogin = true"
            :class="[
              'flex-1 py-2 text-sm font-medium rounded-md transition-colors',
              isLogin
                ? 'bg-white dark:bg-slate-600 text-gray-900 dark:text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
            ]"
          >
            Login
          </button>
          <button
            @click="isLogin = false"
            :class="[
              'flex-1 py-2 text-sm font-medium rounded-md transition-colors',
              !isLogin
                ? 'bg-white dark:bg-slate-600 text-gray-900 dark:text-white shadow-sm'
                : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
            ]"
          >
            Register
          </button>
        </div>
      </div>

      <!-- Login Form -->
      <form v-if="isLogin" @submit.prevent="handleLogin" class="space-y-6">
        <Input
          v-model="loginCredentials.username"
          label="Username/Email"
          placeholder="Enter username or email"
          required
        />

        <Input
          v-model="loginCredentials.password"
          type="password"
          label="Password"
          placeholder="Enter password"
          required
        />

        <div class="text-xs text-gray-500 dark:text-gray-400 text-center">
          Demo credentials: <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded">edgeai_demo</code> / <code class="bg-gray-100 dark:bg-gray-800 px-1 rounded">demo123</code>
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

      <!-- Register Form -->
      <form v-else @submit.prevent="handleRegister" class="space-y-4">
        <Input
          v-model="registerCredentials.name"
          label="Full Name"
          placeholder="Enter your full name"
          required
        />

        <Input
          v-model="registerCredentials.email"
          type="email"
          label="Email"
          placeholder="Enter email address"
          required
          :error="emailError"
        />

        <Input
          v-model="registerCredentials.username"
          label="Username (Optional)"
          placeholder="Enter username, leave empty to use email prefix"
        />

        <Input
          v-model="registerCredentials.password"
          type="password"
          label="Password"
          placeholder="Enter password (at least 6 characters)"
          required
          :error="passwordError"
        />

        <Input
          v-model="registerCredentials.confirmPassword"
          type="password"
          label="Confirm Password"
          placeholder="Enter password again"
          required
          :error="confirmPasswordError"
        />

        <Button
          type="submit"
          class="w-full bg-slate-700 hover:bg-slate-600 dark:bg-slate-600 dark:hover:bg-slate-500 text-white py-3 px-4 rounded-lg font-medium transition-colors"
          size="lg"
          :loading="loading"
          :disabled="!isRegisterValid"
        >
          Register Account
        </Button>
      </form>

      <!-- Quick Login (only show on login tab) -->
      <div v-if="isLogin" class="mt-6 space-y-3">
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
          class="w-full text-green-600 dark:text-green-400 border-green-300 dark:border-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 font-medium transition-all duration-200 hover:scale-[1.02]"
        >
          <span class="flex items-center justify-center space-x-2">
            <span>🚀</span>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import Card from '@/components/ui/Card.vue'
import NotificationManager from '@/components/ui/NotificationManager.vue'
import { ComputerDesktopIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

// State
const isLogin = ref(true)
const loading = ref(false)
const quickLoading = ref(false)

// Login credentials
const loginCredentials = ref({
  username: '',
  password: ''
})

// Register credentials
const registerCredentials = ref({
  name: '',
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

// Validation for registration
const emailError = computed(() => {
  if (!registerCredentials.value.email) return ''
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(registerCredentials.value.email) ? '' : 'Please enter a valid email address'
})

const passwordError = computed(() => {
  if (!registerCredentials.value.password) return ''
  return registerCredentials.value.password.length >= 6 ? '' : 'Password must be at least 6 characters long'
})

const confirmPasswordError = computed(() => {
  if (!registerCredentials.value.confirmPassword) return ''
  return registerCredentials.value.password === registerCredentials.value.confirmPassword ? '' : 'Passwords do not match'
})

const isRegisterValid = computed(() => {
  return registerCredentials.value.name &&
         registerCredentials.value.email &&
         registerCredentials.value.password &&
         registerCredentials.value.confirmPassword &&
         !emailError.value &&
         !passwordError.value &&
         !confirmPasswordError.value
})

// Login handler
const handleLogin = async () => {
  loading.value = true

  try {
    const result = await authStore.login(loginCredentials.value, 'edgeai')
    if (result.success) {
      // 登录成功，通知系统会自动显示成功消息
      router.push('/edgeai/dashboard')
    } else {
      // 登录失败，显示具体错误信息
      console.error('Login failed:', result.error)
    }
  } catch (error) {
    console.error('Login error:', error)
    // 网络错误或其他异常
    const { useNotifications } = await import('@/composables/useNotifications')
    const notifications = useNotifications()
    notifications.error('网络连接失败，请检查网络设置')
  } finally {
    loading.value = false
  }
}

// Register handler
const handleRegister = async () => {
  if (!isRegisterValid.value) return

  loading.value = true

  try {
    const result = await authStore.register(registerCredentials.value, 'edgeai')
    if (result.success) {
      // 注册成功，通知系统会自动显示成功消息
      router.push('/edgeai/dashboard')
    } else {
      // 注册失败，显示具体错误信息
      console.error('Register failed:', result.error)
    }
  } catch (error) {
    console.error('Register error:', error)
    // 网络错误或其他异常
    const { useNotifications } = await import('@/composables/useNotifications')
    const notifications = useNotifications()
    notifications.error('网络连接失败，请检查网络设置')
  } finally {
    loading.value = false
  }
}

// Quick login (demo)
const quickLogin = async () => {
  quickLoading.value = true

  try {
    const demoCredentials = {
      username: 'edgeai_demo',
      password: 'demo123'
    }

    // Use quick login method for faster response
    const result = await authStore.quickLogin(demoCredentials, 'edgeai')
    if (result.success) {
      router.push('/edgeai/dashboard')
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