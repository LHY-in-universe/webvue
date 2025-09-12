<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-16">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <CpuChipIcon class="h-16 w-16 text-primary-600 mx-auto mb-6" />
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          选择用户类型
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-400">
          请选择您在P2P AI训练平台中的角色
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Client Type -->
        <Card 
          hoverable
          variant="elevated"
          class="cursor-pointer transform transition-all duration-200 hover:scale-105"
          @click="selectUserType('client')"
        >
          <div class="text-center p-8">
            <div class="w-20 h-20 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mx-auto mb-6">
              <UserIcon class="h-10 w-10 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 class="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
              客户端
            </h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              作为数据提供方参与联邦学习训练，保护数据隐私的同时贡献计算资源
            </p>
            <Button variant="primary" size="lg" block>
              选择客户端
            </Button>
          </div>
        </Card>

        <!-- Server Type -->
        <Card 
          hoverable
          variant="elevated"
          class="cursor-pointer transform transition-all duration-200 hover:scale-105"
          @click="selectUserType('server')"
        >
          <div class="text-center p-8">
            <div class="w-20 h-20 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mx-auto mb-6">
              <ServerIcon class="h-10 w-10 text-green-600 dark:text-green-400" />
            </div>
            <h3 class="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
              服务器
            </h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              作为协调方管理联邦学习过程，聚合模型参数并协调多方训练
            </p>
            <Button variant="success" size="lg" block>
              选择服务器
            </Button>
          </div>
        </Card>
      </div>

      <div class="text-center mt-8">
        <Button @click="goBack" variant="ghost">
          返回登录
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import { CpuChipIcon, UserIcon, ServerIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const selectUserType = (type) => {
  authStore.setUserType(type)
  router.push('/p2pai/dashboard')
}

const goBack = () => {
  router.push('/p2pai/login')
}
</script>