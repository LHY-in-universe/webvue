<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
    <div class="text-center">
      <div class="mb-8">
        <h1 class="text-9xl font-bold text-primary-600 dark:text-primary-400">404</h1>
      </div>
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
          页面未找到
        </h2>
        <p class="text-gray-600 dark:text-gray-400">
          抱歉，您访问的页面不存在或已被移动
        </p>
      </div>
      <div class="space-x-4">
        <Button @click="goHome" variant="primary">
          返回首页
        </Button>
        <Button @click="goBack" variant="secondary">
          返回上页
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  router.back()
}
</script>