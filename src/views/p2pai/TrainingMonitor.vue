<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Navigation -->
    <nav class="glass-effect shadow-soft border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            
            <div class="w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center mr-3">
              <ChartBarIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Training Monitor
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span class="text-sm text-gray-600 dark:text-gray-400">Live</span>
            </div>
            <Button 
              @click="toggleTheme" 
              variant="ghost" 
              size="sm"
            >
              Theme
            </Button>
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Page Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Training Monitor
          </h2>
          <p class="text-gray-600 dark:text-gray-400">
            Real-time monitoring of all training sessions
          </p>
        </div>
      </div>

      <!-- Training Overview Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Active Sessions"
          :value="3"
          :icon="PlayIcon"
          variant="success"
          description="Currently training"
        />
        
        <StatCard
          title="Completed Today"
          :value="12"
          :icon="CheckCircleIcon"
          variant="info"
          description="Successfully finished"
        />
        
        <StatCard
          title="Total GPU Hours"
          :value="48.5"
          unit="h"
          :precision="1"
          :icon="CpuChipIcon"
          variant="warning"
          description="Resource usage"
        />

        <StatCard
          title="Average Accuracy"
          :value="89.2"
          unit="%"
          :precision="1"
          :icon="TrophyIcon"
          variant="primary"
          description="Session performance"
        />
      </div>

      <!-- Active Training Sessions -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Live Training Sessions -->
        <Card class="glass-effect">
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <PlayIcon class="w-5 h-5 mr-2 text-green-500" />
                Active Training Sessions
              </h3>
              <Button
                @click="refreshSessions"
                variant="ghost"
                size="sm"
              >
                Refresh
              </Button>
            </div>
            
            <div class="space-y-4">
              <div class="text-center py-8">
                <PlayIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
                <p class="text-gray-500 dark:text-gray-400">No active training sessions</p>
              </div>
            </div>
          </div>
        </Card>

        <!-- System Resources -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <ServerIcon class="w-5 h-5 mr-2 text-blue-500" />
              System Resources
            </h3>
            
            <div class="space-y-6">
              <!-- GPU Utilization -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">GPU Utilization</span>
                  <span class="text-sm text-gray-600 dark:text-gray-400">75%</span>
                </div>
                <ProgressBar :percentage="75" variant="success" />
              </div>
              
              <!-- CPU Usage -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">CPU Usage</span>
                  <span class="text-sm text-gray-600 dark:text-gray-400">45%</span>
                </div>
                <ProgressBar :percentage="45" variant="info" />
              </div>
              
              <!-- Memory Usage -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Memory Usage</span>
                  <span class="text-sm text-gray-600 dark:text-gray-400">68%</span>
                </div>
                <ProgressBar :percentage="68" variant="warning" />
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Performance Charts -->
      <Card class="glass-effect">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <ChartBarIcon class="w-5 h-5 mr-2 text-indigo-500" />
            Performance Analytics
          </h3>
          
          <!-- Chart placeholder -->
          <div class="h-64 bg-gray-50 dark:bg-slate-700 rounded-lg flex items-center justify-center">
            <div class="text-center">
              <ChartBarIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p class="text-gray-500 dark:text-gray-400">Training performance charts</p>
              <p class="text-xs text-gray-400 mt-1">Real-time analytics coming soon</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import {
  ArrowLeftIcon,
  ChartBarIcon,
  PlayIcon,
  CheckCircleIcon,
  CpuChipIcon,
  TrophyIcon,
  ServerIcon
} from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'

const router = useRouter()
const themeStore = useThemeStore()

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const refreshSessions = () => {
  console.log('Refreshing sessions...')
}
</script>

<style scoped>
.glass-effect {
  @apply bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm;
}
</style>