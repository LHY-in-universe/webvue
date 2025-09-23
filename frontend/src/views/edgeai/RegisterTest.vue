<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-950">
    <div class="w-full max-w-md bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm border border-slate-200 dark:border-slate-700 p-6 rounded-lg">
      <div class="text-center">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Edge AI Intelligence</h2>
        <p class="text-sm text-slate-600 dark:text-slate-400 mt-2">创建新账户 - 测试页面</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="space-y-6 mt-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">用户名</label>
          <input
            v-model="formData.name"
            type="text"
            placeholder="请输入用户名"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">邮箱</label>
          <input
            v-model="formData.email"
            type="email"
            placeholder="请输入邮箱地址"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">密码</label>
          <input
            v-model="formData.password"
            type="password"
            placeholder="请输入密码（至少6位）"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">确认密码</label>
          <input
            v-model="formData.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full bg-slate-700 hover:bg-slate-600 text-white py-3 px-4 rounded-lg font-medium transition-colors"
        >
          注册账户
        </button>
      </form>

      <div class="mt-6 text-center">
        <button
          @click="goToLogin"
          class="text-blue-600 dark:text-blue-400 hover:underline"
        >
          已有账户？立即登录
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  console.log('Register form submitted:', formData)
  
  try {
    const result = await authStore.register({
      name: formData.name.trim(),
      email: formData.email.trim(),
      password: formData.password
    }, 'edgeai')
    
    if (result.success) {
      router.push('/edgeai/dashboard')
    } else {
      alert('注册失败: ' + result.error)
    }
  } catch (error) {
    console.error('Register error:', error)
    alert('注册失败，请检查网络连接')
  }
}

const goToLogin = () => {
  router.push('/edgeai/login')
}
</script>
