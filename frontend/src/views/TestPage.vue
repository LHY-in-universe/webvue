<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">测试页面</h1>
      <p class="text-lg text-gray-600">如果你能看到这个页面，说明Vue路由正常工作！</p>
      <p class="text-sm text-gray-500 mt-4">当前时间: {{ currentTime }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentTime = ref('')

onMounted(() => {
  currentTime.value = new Date().toLocaleString()
  console.log('Test page mounted successfully!')
})
</script>
