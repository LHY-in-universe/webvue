<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Navigation -->
    <nav class="glass-effect shadow-soft border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center mr-3 micro-bounce hover-glow-primary">
              <CpuChipIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gradient text-shadow-soft">
              {{ userTypeText === 'Client' ? 'Client Control Panel' : 'Server Control Panel' }}
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Welcome, {{ authStore.user?.username }}
            </span>
            
            <!-- Offline/Online Status -->
            <div v-if="isOffline" class="flex items-center space-x-2 text-sm text-yellow-600 dark:text-yellow-400">
              <div class="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
              <span>Offline Mode</span>
              <span v-if="queuedRequests > 0">({{ queuedRequests }} queued)</span>
            </div>
            
            <!-- Refresh Button -->
            <Button 
              @click="refreshData" 
              variant="ghost" 
              size="sm"
              :disabled="loading"
              :leftIcon="loading ? undefined : ChartBarIcon"
            >
              <LoadingSpinner v-if="loading" size="sm" />
              <span v-else>Refresh</span>
            </Button>
            
            <SimpleThemeToggle size="sm" />
            <Button @click="logout" variant="ghost" size="sm">
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Error State -->
    <div v-if="error && !loading" class="max-w-4xl mx-auto px-6 py-4">
      <Card class="bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800">
        <div class="p-4 flex items-center space-x-3">
          <div class="flex-shrink-0">
            <svg class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
              Failed to load dashboard data
            </h3>
            <p class="mt-1 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </p>
          </div>
          <Button @click="refreshData" variant="secondary" size="sm">
            Retry
          </Button>
        </div>
      </Card>
    </div>

    <div class="max-w-4xl mx-auto px-6 py-8">
      <!-- Client Dashboard -->
      <div v-if="authStore.userType === 'client'">
        <!-- Welcome Section -->
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Welcome Back!
          </h2>
        </div>

        <!-- Project Creation Section -->
        <div class="grid md:grid-cols-3 gap-6 mb-8">
          <!-- Local Training Project Creation -->
          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="createLocalProject">
            <div class="text-center p-6 flex flex-col h-full">
              <div class="w-14 h-14 bg-gray-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <ShieldCheckIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4 min-h-[3.5rem] flex items-center justify-center">Local Model Training</h3>
              
              <div class="text-gray-600 dark:text-gray-400 font-medium text-sm mt-auto">
                Start Local Training →
              </div>
            </div>
          </Card>

          <!-- Federated Learning Project Creation -->
          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="createFederatedProject">
            <div class="text-center p-6 flex flex-col h-full">
              <div class="w-14 h-14 bg-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <UsersIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4 min-h-[3.5rem] flex items-center justify-center">Federated Learning Training</h3>
              
              <div class="text-blue-600 font-medium text-sm mt-auto">
                Start Federated Learning →
              </div>
            </div>
          </Card>

          <!-- MPC Training Project Creation -->
          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="createMPCProject">
            <div class="text-center p-6 flex flex-col h-full">
              <div class="w-14 h-14 bg-green-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <LockClosedIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4 min-h-[3.5rem] flex items-center justify-center">MPC Training</h3>
              
              <div class="text-green-600 font-medium text-sm mt-auto">
                Start MPC Training →
              </div>
            </div>
          </Card>
        </div>

        <!-- Management Centers -->
        <div class="grid md:grid-cols-2 gap-6 mb-8">
          <!-- Dataset Management -->
          <Card class="cursor-pointer hover:shadow-lg transition-shadow" @click="openDatasetCenter">
            <div class="text-center p-6">
              <div class="w-14 h-14 bg-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <CircleStackIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Dataset Management Center</h3>
              <div class="text-blue-600 font-medium text-sm">
                Enter Dataset Center →
              </div>
            </div>
          </Card>

          <!-- Model Management -->
          <Card class="cursor-pointer hover:shadow-lg transition-shadow" @click="openModelCenter">
            <div class="text-center p-6">
              <div class="w-14 h-14 bg-green-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <CubeIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Model Management Center</h3>
              <div class="text-green-600 font-medium text-sm">
                Enter Model Center →
              </div>
            </div>
          </Card>
        </div>

        <!-- Training Status Overview -->
        <Card class="mb-8">
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Training Status Overview</h3>
          </template>
          <div class="grid md:grid-cols-2 gap-6">
            <div class="text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-slate-700 p-3 rounded-lg transition-colors" 
                 @click="viewCompletedTraining">
              <div class="text-2xl font-bold text-gray-700 dark:text-gray-300">{{ completedTraining }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Completed Training</div>
            </div>
            <div class="text-center cursor-pointer hover:bg-gray-50 dark:hover:bg-slate-700 p-3 rounded-lg transition-colors"
                 @click="viewOngoingTraining">
              <div class="text-2xl font-bold text-gray-700 dark:text-gray-300">{{ ongoingTraining }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Ongoing Training</div>
            </div>
          </div>
        </Card>

        <!-- My Projects - Following EdgeAI Design -->
        <div class="mb-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-semibold text-gray-900 dark:text-white">My Projects</h2>
            
            <div class="flex items-center space-x-4">
              <!-- Search Box -->
              <div class="relative">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search projects..."
                  class="w-64 pl-4 pr-10 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <MagnifyingGlassIcon class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              </div>
              
              <!-- Status Filter -->
              <select
                v-model="statusFilter"
                class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Statuses</option>
                <option value="Training">Training</option>
                <option value="Completed">Completed</option>
                <option value="Idle">Idle</option>
                <option value="Error">Error</option>
              </select>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div 
              v-for="project in filteredProjects" 
              :key="project.id"
              @click="openProjectVisualization(project)"
              class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 cursor-pointer hover:shadow-lg transition-all duration-200"
            >
              <!-- Status Indicator and Title -->
              <div class="flex items-start justify-between mb-3">
                <div class="flex items-center">
                  <div 
                    :class="getStatusDotColor(project.status)"
                    class="w-3 h-3 rounded-full mr-3"
                  ></div>
                  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    {{ project.name }}
                  </h3>
                </div>
              </div>
              
              <!-- Training Algorithms Badges -->
              <div class="flex flex-wrap gap-2 mb-3">
                <span class="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 rounded-full">
                  {{ project.training_alg }}
                </span>
                <span v-if="project.fed_alg" class="px-2 py-1 text-xs font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-300 rounded-full">
                  {{ project.fed_alg }}
                </span>
                <span v-if="project.type === 'federated' && project.num_clients" class="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 rounded-full">
                  {{ project.num_clients }} Clients
                </span>
                <span v-if="project.type === 'mpc' && project.threshold" class="px-2 py-1 text-xs font-medium bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300 rounded-full">
                  {{ project.threshold }}/{{ project.num_computers }} Threshold
                </span>
              </div>
              
              <!-- Model and Dataset Info -->
              <div class="space-y-1 mb-3 text-sm">
                <div class="flex items-center text-gray-600 dark:text-gray-400">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                  </svg>
                  <span class="truncate">{{ project.model_name_or_path }}</span>
                </div>
                <div class="flex items-center text-gray-600 dark:text-gray-400">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                  </svg>
                  <span class="truncate">{{ project.dataset_name }}</span>
                </div>
              </div>
              
              <!-- Training Parameters -->
              <div class="grid grid-cols-3 gap-2 mb-3 text-xs">
                <div class="text-center p-2 bg-gray-50 dark:bg-gray-700/50 rounded">
                  <div class="text-gray-500 dark:text-gray-400">Batch</div>
                  <div class="font-semibold text-gray-900 dark:text-white">{{ project.batch_size }}</div>
                </div>
                <div class="text-center p-2 bg-gray-50 dark:bg-gray-700/50 rounded">
                  <div class="text-gray-500 dark:text-gray-400">LR</div>
                  <div class="font-semibold text-gray-900 dark:text-white">{{ project.lr }}</div>
                </div>
                <div class="text-center p-2 bg-gray-50 dark:bg-gray-700/50 rounded">
                  <div class="text-gray-500 dark:text-gray-400">Epochs</div>
                  <div class="font-semibold text-gray-900 dark:text-white">{{ project.total_epochs }}</div>
                </div>
              </div>
              
              <!-- Training Progress -->
              <div class="flex justify-between text-sm mb-2">
                <span class="text-gray-500 dark:text-gray-400">Progress:</span>
                <span class="font-semibold text-gray-900 dark:text-white">{{ project.progress }}%</span>
              </div>
              
              <!-- Progress Bar -->
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-2">
                <div 
                  class="bg-green-500 h-2 rounded-full transition-all duration-300"
                  :style="{ width: project.progress + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Server Dashboard -->
      <div v-else-if="authStore.userType === 'server'">
        <!-- Server Welcome Section -->
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Server Management Center
          </h2>
        </div>

        <!-- Server Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8 stagger-children">
          <StatCard
            title="Ray Clusters"
            :value="rayClusters"
            :icon="ServerIcon"
            variant="primary"
            clickable
            animated
            @click="navigateToRays"
          />
          
          <StatCard
            title="Server Projects"
            :value="serverProjects"
            :icon="CpuChipIcon"
            variant="success"
            clickable
            animated
            @click="navigateToProjects"
          />
          
          <StatCard
            title="Training Requests"
            :value="trainingRequests"
            :icon="ClockIcon"
            variant="warning"
            clickable
            animated
            @click="navigateToRequests"
          />
          
          <StatCard
            title="Server Models"
            :value="serverModels"
            :icon="ChartBarIcon"
            variant="info"
            clickable
            animated
            @click="navigateToModels"
          />
        </div>

        <!-- Quick Navigation -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="navigateToRays">
            <div class="text-center p-6 flex flex-col h-full">
              <div class="w-14 h-14 bg-blue-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <ServerIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Ray Cluster Management</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400 flex-grow">
                Create and manage Ray clusters, invite clients to join
              </p>
            </div>
          </Card>

          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="navigateToProjects">
            <div class="text-center p-6 flex flex-col h-full">
              <div class="w-14 h-14 bg-purple-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <CpuChipIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Server Projects</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400 flex-grow">
                Manage FL/MPC federated training projects
              </p>
            </div>
          </Card>

          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="navigateToRequests">
            <div class="text-center p-6 flex flex-col h-full">
              <div class="w-14 h-14 bg-orange-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <ClockIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Training Requests</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400 flex-grow">
                Handle client training requests
              </p>
            </div>
          </Card>

          <Card class="cursor-pointer hover:shadow-lg transition-all hover:scale-[1.02]" @click="navigateToModels">
            <div class="text-center p-6 flex flex-col h-full">
              <div class="w-14 h-14 bg-green-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <ChartBarIcon class="w-7 h-7 text-white" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Server Models</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400 flex-grow">
                Manage trained models
              </p>
            </div>
          </Card>
        </div>

        <!-- Global Training Control -->
        <Card class="mb-8">
          <template #header>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Global Training Control</h3>
          </template>
          
          <div class="space-y-4">
            <Button 
              @click="startGlobalTraining" 
              variant="primary" 
              size="lg" 
              block
              :loading="globalTrainingActive"
              :disabled="globalTrainingActive"
            >
              {{ globalTrainingActive ? 'Training in Progress...' : 'Start Global Training' }}
            </Button>
            
            <div v-if="globalTrainingActive" class="space-y-4">
              <div class="text-center py-2 text-gray-600 dark:text-gray-400">
                <p>Training Round: {{ trainingRounds }} / 10</p>
                <p>Current Accuracy: {{ accuracy.toFixed(2) }}%</p>
              </div>
              
              <ProgressBar
                :percentage="(trainingRounds / 10) * 100"
                label="Training Progress"
                variant="success"
                :animated="true"
                :info="`Round ${trainingRounds} of 10`"
              />
            </div>
          </div>
        </Card>

        <!-- Client Management & System Logs -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <template #header>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Connected Clients</h3>
            </template>
            
            <div class="space-y-3">
              <div v-for="client in clientList" :key="client.id" class="flex items-center justify-between p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                <div>
                  <div class="font-medium text-gray-900 dark:text-white">{{ client.name }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">{{ client.ip }}</div>
                </div>
                <div class="text-right">
                  <div class="text-sm font-medium" :class="client.status === 'online' ? 'text-green-600' : 'text-gray-400'">
                    {{ client.status }}
                  </div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">{{ client.lastSeen }}</div>
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <template #header>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">System Logs</h3>
            </template>
            
            <div class="space-y-3">
              <div v-for="log in systemLogs" :key="log.id" class="text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-900 dark:text-white">{{ log.message }}</span>
                  <span class="text-gray-500 dark:text-gray-400">{{ log.time }}</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>

    <!-- Training Details Modal -->
    <Modal
      v-model:isOpen="showTrainingModal"
      title="Training Details"
      :icon="ChartBarIcon"
      size="lg"
      @confirm="handleTrainingAction"
      @cancel="closeTrainingModal"
    >
      <div class="space-y-6">
        <!-- Training Summary -->
        <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-3">Training Summary</h4>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Model Type</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ selectedTraining?.name || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Training Type</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ selectedTraining?.trainingType || 'N/A' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Accuracy</p>
              <p class="font-medium text-gray-900 dark:text-white">
                {{ selectedTraining?.accuracy ? `${selectedTraining.accuracy.toFixed(2)}%` : 'N/A' }}
              </p>
            </div>
            <div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Date</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ selectedTraining?.date || 'N/A' }}</p>
            </div>
          </div>
        </div>

        <!-- Training Progress (if applicable) -->
        <div v-if="selectedTraining?.progress">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-3">Training Progress</h4>
          <ProgressBar
            :percentage="selectedTraining.progress"
            label="Completion Rate"
            variant="success"
            :animated="true"
          />
        </div>

        <!-- Loading State -->
        <div v-if="modalLoading" class="flex justify-center py-8">
          <LoadingSpinner 
            size="lg" 
            text="Loading training details..." 
            color="primary"
          />
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button @click="closeTrainingModal" variant="ghost">
            Close
          </Button>
          <Button @click="handleTrainingAction" variant="primary">
            View Full Report
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUIStore } from '@/stores/ui'
import { useP2PAIStore } from '@/stores/p2pai'
import { useApiOptimization } from '@/composables/useApiOptimization.js'
import { useErrorBoundary } from '@/composables/useErrorBoundary'
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts'
import { useOfflineMode } from '@/composables/useOfflineMode'
import p2paiService from '@/services/p2paiService.js'
import performanceMonitor from '@/utils/performanceMonitor.js'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import { 
  CpuChipIcon, 
  ClockIcon,
  ChartBarIcon,
  ShieldCheckIcon,
  UsersIcon,
  CircleStackIcon,
  CubeIcon,
  ServerIcon,
  LockClosedIcon,
  MagnifyingGlassIcon,
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const uiStore = useUIStore()
const p2paiStore = useP2PAIStore()
const { cachedApiCall, clearCache } = useApiOptimization()
const { hasError, retry, captureError } = useErrorBoundary()
const { enableShortcuts, disableShortcuts } = useKeyboardShortcuts()
const { 
  isOffline, 
  queuedRequests, 
  hasOfflineData, 
  offlineAwareFetch 
} = useOfflineMode()

// API loading state
const loading = ref(true)
const error = ref(null)


// Common data
const trainingRounds = ref(0)
const accuracy = ref(0)

// Modal data
const showTrainingModal = ref(false)
const selectedTraining = ref(null)
const modalLoading = ref(false)

// Client-specific data
const completedTraining = ref(3)
const ongoingTraining = ref(1)


// Server-specific data
const globalTrainingActive = ref(false)
// Server Dashboard - Old Stats (deprecated)
const connectedClients = ref(4)
const activeTrainingSessions = ref(2)
const pendingRequests = ref(1)
const systemUptime = ref(48.73)

// Server Dashboard - New Stats
const rayClusters = ref(0)
const serverProjects = ref(0)
const trainingRequests = ref(0)
const serverModels = ref(0)

// Enhanced API data loading function
const loadDashboardData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('P2PAIDashboard')
  loading.value = true
  error.value = null
  
  try {
    // 🔧 Using frontend hardcoded data
    console.warn('⚠️ Using hardcoded project data for frontend demo')

    // Hardcoded data already set in ref initialization
    // projects.value = HARDCODED_PROJECTS

    // Update statistics (based on hardcoded projects)
    completedTraining.value = HARDCODED_PROJECTS.filter(p => p.status === 'Completed').length
    ongoingTraining.value = HARDCODED_PROJECTS.filter(p => p.status === 'Training').length
    
    // Update Server-side statistics
    if (authStore.userType === 'server') {
      rayClusters.value = HARDCODED_SERVER_RAYS.length
      serverProjects.value = HARDCODED_SERVER_PROJECTS.length
      trainingRequests.value = HARDCODED_TRAINING_REQUESTS.filter(r => r.status === 'pending').length
      serverModels.value = HARDCODED_SERVER_MODELS.length
      console.log('✅ Server data statistics updated')
    }
    
    loading.value = false
    pageMonitor.end()
    console.log('✅ Hardcoded project data loaded successfully')
    return
    
    // Below is the actual API call code (currently disabled)
    const [projectStats, nodeStats, trainingData, modelStats, datasetStats] = await Promise.all([
      cachedApiCall('project-stats', () => p2paiService.projects.getProjectStats(), 2 * 60 * 1000),
      cachedApiCall('node-stats', () => p2paiService.nodes.getNodeStats(), 1 * 60 * 1000),
      cachedApiCall('training-sessions', () => p2paiService.training.getTrainingSessions({ limit: 10 }), 30 * 1000),
      cachedApiCall('model-stats', () => p2paiService.models.getModelStats(), 5 * 60 * 1000),
      cachedApiCall('dataset-stats', () => p2paiService.datasets.getDatasetStats(), 5 * 60 * 1000)
    ])
    
    // Update project data with real API data
    if (projectStats.data?.projects) {
      projects.value = projectStats.data.projects.map(project => ({
        ...project,
        lastUpdated: formatTime(project.last_updated)
      }))
    }
    
    // Update dashboard statistics
    completedTraining.value = trainingData.data?.completed_sessions || 0
    ongoingTraining.value = trainingData.data?.active_sessions || 0
    connectedClients.value = nodeStats.data?.connected_nodes || 0
    activeTrainingSessions.value = trainingData.data?.active_sessions || 0
    pendingRequests.value = trainingData.data?.pending_requests || 0
    systemUptime.value = nodeStats.data?.uptime_hours || 0
    
    // Sync with main P2PAI store
    await p2paiStore.loadRealData()
    
    console.log('📊 Dashboard data loaded successfully')
    pageMonitor.end()
  } catch (err) {
    console.error('❌ Failed to load dashboard data:', err)
    error.value = err.message || 'Failed to load dashboard data'
    captureError(err, null, 'Dashboard data loading failed')
    pageMonitor.end()
  } finally {
    loading.value = false
  }
}

// Enhanced refresh dashboard data
const refreshData = async () => {
  // Clear all caches for fresh data
  clearCache('project-stats')
  clearCache('node-stats')
  clearCache('training-sessions')
  clearCache('model-stats')
  clearCache('dataset-stats')
  
  await loadDashboardData()
  
  uiStore.addNotification({
    type: 'success',
    title: 'Dashboard Refreshed',
    message: 'All data has been updated',
    duration: 2000
  })
}

// Format time helper for real timestamps
const formatTime = (timestamp) => {
  if (!timestamp) return 'Unknown'
  
  const now = new Date()
  const time = new Date(timestamp)
  const diffInMinutes = Math.floor((now - time) / (1000 * 60))
  
  if (diffInMinutes < 1) return 'Just now'
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`
  
  const hours = Math.floor(diffInMinutes / 60)
  if (hours < 24) return `${hours}h ago`
  
  const days = Math.floor(hours / 24)
  return `${days}d ago`
}

// Project search and filtering - Following EdgeAI functionality
const searchQuery = ref('')
const statusFilter = ref('')

// 🔧 FRONTEND HARDCODED DATA
// 📁 File Location: /frontend/src/views/p2pai/Dashboard.vue
// ⚠️ This is hardcoded example project data for frontend demo only
// 📋 Database table: client_projects (id, user_id, type, name, description, training_alg, fed_alg, secure_aggregation, 
//              total_epochs, num_rounds, batch_size, lr, num_computers, threshold, num_clients, sample_clients, 
//              max_steps, model_name_or_path, dataset_name, dataset_sample, status, progress, loss, accuracy, 
//              task_id, created_time, updated_time)
const HARDCODED_PROJECTS = [
  {
    id: 1,
    type: 'local',
    name: '[Frontend Demo] Local Training - Image Classification',
    description: '⚠️ Frontend demo data - Local training project using single machine for image classification model',
    training_alg: 'Adam',
    fed_alg: null,
    secure_aggregation: false,
    total_epochs: 100,
    num_rounds: null,
    batch_size: 32,
    lr: 0.001,
    num_computers: 1,
    threshold: null,
    num_clients: null,
    sample_clients: null,
    max_steps: 10000,
    model_name_or_path: 'resnet50',
    dataset_name: 'CIFAR-10',
    dataset_sample: 'full',
    status: 'Training',
    progress: 65.00,
    loss: 0.234567,
    accuracy: 0.8520,
    task_id: 'local_task_001',
    created_time: new Date('2024-01-15'),
    updated_time: new Date(),
    // 前端显示字段
    nodes: 1,
    created: '2024-01-15',
    lastUpdated: '2m ago',
    trainingType: 'Local Training'
  },
  {
    id: 2,
    type: 'federated',
    name: '[Frontend Demo] Federated Learning - Medical Diagnosis',
    description: '⚠️ Frontend demo data - Federated learning project with multiple hospitals collaborating on disease diagnosis model',
    training_alg: 'Adam',
    fed_alg: 'FedAvg',
    secure_aggregation: true,
    total_epochs: 100,
    num_rounds: 20,
    batch_size: 16,
    lr: 0.0005,
    num_computers: null,
    threshold: null,
    num_clients: 5,
    sample_clients: 3,
    max_steps: 5000,
    model_name_or_path: 'efficientnet-b0',
    dataset_name: 'Medical-Images',
    dataset_sample: 'iid',
    status: 'Training',
    progress: 75.00,
    loss: 0.189234,
    accuracy: 0.8950,
    task_id: 'fl_task_002',
    created_time: new Date('2024-01-20'),
    updated_time: new Date(),
    // 前端显示字段
    nodes: 5,
    created: '2024-01-20',
    lastUpdated: '5m ago',
    trainingType: 'Federated Learning'
  },
  {
    id: 3,
    type: 'mpc',
    name: '[Frontend Demo] MPC - Financial Data Analysis',
    description: '⚠️ Frontend demo data - Multi-party computation project with financial institutions jointly analyzing data',
    training_alg: 'SecureAgg',
    fed_alg: 'SecureFedAvg',
    secure_aggregation: true,
    total_epochs: 1000,
    num_rounds: 100,
    batch_size: 64,
    lr: 0.0001,
    num_computers: 3,
    threshold: 2,
    num_clients: null,
    sample_clients: null,
    max_steps: 3000,
    model_name_or_path: 'mlp-classifier',
    dataset_name: 'Financial-Records',
    dataset_sample: 'secure',
    status: 'Completed',
    progress: 100.00,
    loss: 0.145678,
    accuracy: 0.9180,
    task_id: 'mpc_task_003',
    created_time: new Date('2024-01-25'),
    updated_time: new Date('2024-02-01'),
    // 前端显示字段
    nodes: 3,
    created: '2024-01-25',
    lastUpdated: '3d ago',
    trainingType: 'MPC'
  }
]

// ===== Server-side Hardcoded Data =====
// service_rays (id, name, description, service_user_id, client_user_id)
const HARDCODED_SERVER_RAYS = [
  {
    id: 1,
    name: 'Ray Cluster Alpha',
    description: 'Primary training cluster for large-scale federated learning tasks',
    service_user_id: 1,
    status: 'running',
    created_time: new Date('2024-01-15'),
    updated_time: new Date('2024-02-10'),
    clients: [
      { id: 1, name: 'Client-001', ipv4: '192.168.1.101', status: 'connected' },
      { id: 2, name: 'Client-002', ipv4: '192.168.1.102', status: 'connected' },
      { id: 3, name: 'Client-003', ipv4: '192.168.1.103', status: 'connected' }
    ],
    project_count: 2
  },
  {
    id: 2,
    name: 'Ray Cluster Beta',
    description: 'Dedicated MPC cluster providing high-security training environment',
    service_user_id: 1,
    status: 'idle',
    created_time: new Date('2024-01-20'),
    updated_time: new Date('2024-02-08'),
    clients: [
      { id: 4, name: 'Client-004', ipv4: '192.168.1.104', status: 'connected' },
      { id: 5, name: 'Client-005', ipv4: '192.168.1.105', status: 'idle' }
    ],
    project_count: 1
  },
  {
    id: 3,
    name: 'Ray Cluster Gamma',
    description: 'Test cluster for experimental training tasks',
    service_user_id: 1,
    status: 'initializing',
    created_time: new Date('2024-02-05'),
    updated_time: new Date('2024-02-10'),
    clients: [],
    project_count: 0
  }
]

// service_projects (id, user_id, ray_id, type, name, description, training_alg, fed_alg, 
//                  secure_aggregation, total_epochs, num_rounds, batch_size, lr, 
//                  num_computers, threshold, num_clients, sample_clients, max_steps, 
//                  model_name_or_path, status, progress, task_id, created_time, updated_time)
const HARDCODED_SERVER_PROJECTS = [
  {
    id: 1,
    user_id: 1,
    ray_id: 1,
    ray_name: 'Ray Cluster Alpha',
    type: 'federated',
    name: 'FL Medical Image Classification',
    description: 'Federated learning-based medical image classification project with patient privacy protection',
    training_alg: 'FedAvg',
    fed_alg: 'FedAvg',
    secure_aggregation: true,
    total_epochs: 50,
    num_rounds: 100,
    batch_size: 32,
    lr: 0.001000,
    num_computers: 3,
    threshold: 2,
    num_clients: 3,
    sample_clients: 3,
    max_steps: 5000,
    model_name_or_path: 'resnet50',
    status: 'training',
    progress: 45.50,
    task_id: 'server_fl_task_001',
    created_time: new Date('2024-01-20'),
    updated_time: new Date('2024-02-10')
  },
  {
    id: 2,
    user_id: 1,
    ray_id: 1,
    ray_name: 'Ray Cluster Alpha',
    type: 'federated',
    name: 'FL Financial Risk Control Model',
    description: 'Multi-bank collaborative risk assessment model training',
    training_alg: 'FedProx',
    fed_alg: 'FedProx',
    secure_aggregation: true,
    total_epochs: 30,
    num_rounds: 50,
    batch_size: 64,
    lr: 0.000500,
    num_computers: 3,
    threshold: 2,
    num_clients: 3,
    sample_clients: 2,
    max_steps: 3000,
    model_name_or_path: 'xgboost',
    status: 'completed',
    progress: 100.00,
    task_id: 'server_fl_task_002',
    created_time: new Date('2024-01-15'),
    updated_time: new Date('2024-02-05')
  },
  {
    id: 3,
    user_id: 1,
    ray_id: 2,
    ray_name: 'Ray Cluster Beta',
    type: 'mpc',
    name: 'MPC Encrypted Data Analysis',
    description: 'Sensitive data analysis using multi-party secure computation',
    training_alg: 'SecureAgg',
    fed_alg: null,
    secure_aggregation: true,
    total_epochs: 20,
    num_rounds: 30,
    batch_size: 16,
    lr: 0.000100,
    num_computers: 2,
    threshold: 2,
    num_clients: 2,
    sample_clients: 2,
    max_steps: 2000,
    model_name_or_path: 'mlp_classifier',
    status: 'pending',
    progress: 0.00,
    task_id: 'server_mpc_task_001',
    created_time: new Date('2024-02-08'),
    updated_time: new Date('2024-02-08')
  }
]

// service_models (id, name, description, user_id, project_id, file_path, version, size, 
//                class_config, status, progress, loss, accuracy, created_time, updated_time)
const HARDCODED_SERVER_MODELS = [
  {
    id: 1,
    name: 'FL Medical Image Classification Model',
    description: 'Federated learning trained ResNet50 medical image classification model',
    user_id: 1,
    project_id: 2,
    project_name: 'FL Financial Risk Control Model',
    file_path: '/models/fl_medical_resnet50_v1.pth',
    version: 'v1.0.0',
    size: 102428800, // approx 102MB
    class_config: JSON.stringify({
      model_type: 'ResNet50',
      num_classes: 10,
      input_shape: [3, 224, 224],
      optimizer: 'Adam'
    }),
    status: 'completed',
    progress: 100.00,
    loss: 0.234567,
    accuracy: 0.9156,
    created_time: new Date('2024-02-05'),
    updated_time: new Date('2024-02-05')
  },
  {
    id: 2,
    name: 'FL Financial Risk Control Model',
    description: 'XGBoost risk assessment model',
    user_id: 1,
    project_id: 2,
    project_name: 'FL Financial Risk Control Model',
    file_path: '/models/fl_finance_xgb_v2.model',
    version: 'v2.1.0',
    size: 51200000, // approx 51MB
    class_config: JSON.stringify({
      model_type: 'XGBoost',
      max_depth: 6,
      n_estimators: 100,
      learning_rate: 0.05
    }),
    status: 'completed',
    progress: 100.00,
    loss: 0.156789,
    accuracy: 0.9423,
    created_time: new Date('2024-02-05'),
    updated_time: new Date('2024-02-05')
  },
  {
    id: 3,
    name: 'MPC Encrypted Analysis Model',
    description: 'MLP classifier for encrypted data analysis',
    user_id: 1,
    project_id: 3,
    project_name: 'MPC Encrypted Data Analysis',
    file_path: '/models/mpc_mlp_classifier_v1.pkl',
    version: 'v1.0.0',
    size: 25600000, // approx 26MB
    class_config: JSON.stringify({
      model_type: 'MLP',
      hidden_layers: [128, 64, 32],
      activation: 'relu',
      dropout: 0.3
    }),
    status: 'training',
    progress: 35.00,
    loss: 0.456789,
    accuracy: 0.8234,
    created_time: new Date('2024-02-08'),
    updated_time: new Date('2024-02-10')
  }
]

// Training request data
const HARDCODED_TRAINING_REQUESTS = [
  {
    id: 1,
    client_id: 4,
    client_name: 'Client-004',
    client_ip: '192.168.1.104',
    type: 'federated',
    project_name: 'FL Text Sentiment Analysis',
    description: 'BERT-based multilingual sentiment analysis model training',
    requested_config: {
      training_alg: 'FedAvg',
      num_rounds: 80,
      batch_size: 32,
      lr: 0.0001,
      num_clients: 4,
      model_name_or_path: 'bert-base-multilingual'
    },
    status: 'pending',
    created_time: new Date('2024-02-10'),
    updated_time: new Date('2024-02-10')
  },
  {
    id: 2,
    client_id: 5,
    client_name: 'Client-005',
    client_ip: '192.168.1.105',
    type: 'mpc',
    project_name: 'MPC Joint Statistical Analysis',
    description: 'Multi-party secure computation joint statistical analysis',
    requested_config: {
      training_alg: 'SecureAgg',
      num_rounds: 20,
      threshold: 3,
      num_clients: 3,
      model_name_or_path: 'linear_regression'
    },
    status: 'pending',
    created_time: new Date('2024-02-09'),
    updated_time: new Date('2024-02-09')
  },
  {
    id: 3,
    client_id: 6,
    client_name: 'Client-006',
    client_ip: '192.168.1.106',
    type: 'federated',
    project_name: 'FL Recommendation System',
    description: 'Federated learning recommendation system training',
    requested_config: {
      training_alg: 'FedProx',
      num_rounds: 60,
      batch_size: 128,
      lr: 0.001,
      num_clients: 5,
      model_name_or_path: 'ncf_model'
    },
    status: 'approved',
    ray_id: 1,
    created_time: new Date('2024-02-08'),
    updated_time: new Date('2024-02-09')
  }
]

// Project data - using hardcoded data
const projects = ref(HARDCODED_PROJECTS)

// Computed property - Following EdgeAI filtering logic
const filteredProjects = computed(() => {
  let filtered = projects.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(project => 
      project.name.toLowerCase().includes(query) ||
      project.description.toLowerCase().includes(query)
    )
  }

  // Filter by status
  if (statusFilter.value) {
    filtered = filtered.filter(project => project.status === statusFilter.value)
  }

  return filtered
})

// Status dot color - Following EdgeAI logic
const getStatusDotColor = (status) => {
  const colors = {
    'Training': 'bg-blue-500',
    'Completed': 'bg-green-500', 
    'Idle': 'bg-gray-500',
    'Error': 'bg-red-500'
  }
  return colors[status] || 'bg-gray-500'
}

const clientList = ref([
  {
    id: 'client_001',
    name: 'Client-001',
    ip: '192.168.1.101',
    status: 'online',
    lastSeen: '2 mins ago'
  },
  {
    id: 'client_002', 
    name: 'Client-002',
    ip: '192.168.1.102',
    status: 'online',
    lastSeen: '5 mins ago'
  },
  {
    id: 'client_003',
    name: 'Client-003',
    ip: '192.168.1.103',
    status: 'offline',
    lastSeen: '1 hour ago'
  },
  {
    id: 'client_004',
    name: 'Client-004',
    ip: '192.168.1.104',
    status: 'online',
    lastSeen: '1 min ago'
  }
])

const systemLogs = ref([
  { id: 1, message: 'Global training session started', time: 'just now' },
  { id: 2, message: 'Client-004 joined training session', time: '2 minutes ago' },
  { id: 3, message: 'Model parameters updated', time: '5 minutes ago' },
  { id: 4, message: 'Training round 8 completed', time: '8 minutes ago' }
])

const userTypeText = computed(() => {
  return authStore.userType === 'server' ? 'Server' : 'Client'
})

// Project Creation Methods
const createLocalProject = () => {
  router.push('/p2pai/local-training')
}

const createFederatedProject = () => {
  router.push('/p2pai/federated-training')
}

const createMPCProject = () => {
  router.push('/p2pai/mpc-training')
}

const openDatasetCenter = () => {
  router.push('/p2pai/datasets')
}

const openModelCenter = () => {
  router.push('/p2pai/models')
}


const openProjectVisualization = (project) => {
  // 如果传入的是字符串（旧的调用方式），则直接使用
  if (typeof project === 'string') {
    router.push(`/p2pai/visualization/${project}`)
  } else {
    // 如果是本地训练项目，使用新的本地训练可视化界面
    if (project.type === 'local') {
      router.push(`/p2pai/local-visualization/${project.id}`)
    } else {
      // 联邦学习和MPC使用原有的可视化界面
      router.push(`/p2pai/visualization/${project.id}`)
    }
  }
}

const viewCompletedTraining = () => {
  console.log('Viewing completed training details')
  // TODO: Show completed training modal
}

const viewOngoingTraining = () => {
  console.log('Viewing ongoing training details')
  // TODO: Show ongoing training modal  
}


// Server methods
const startGlobalTraining = () => {
  globalTrainingActive.value = true
  console.log('Starting global training')
  
  // Simulate training progress
  const interval = setInterval(() => {
    trainingRounds.value++
    accuracy.value = parseFloat(Math.min(95, accuracy.value + Math.random() * 3).toFixed(2))
    
    if (trainingRounds.value >= 10) {
      globalTrainingActive.value = false
      clearInterval(interval)
      
      // Add completion log
      systemLogs.value.unshift({
        id: Date.now(),
        message: 'Global training completed successfully',
        time: 'just now'
      })
    }
  }, 3000)
}

const viewClientDetails = () => {
  router.push('/p2pai/monitor')
}

const viewTrainingDetails = () => {
  router.push('/p2pai/monitor')
}

const viewPendingRequests = () => {
  router.push('/p2pai/models')
}

const viewSystemStatus = () => {
  router.push('/p2pai/monitor')
}

// Server Dashboard - New Navigation Methods
const navigateToRays = () => {
  router.push('/p2pai/server/rays')
}

const navigateToProjects = () => {
  router.push('/p2pai/server/projects')
}

const navigateToRequests = () => {
  router.push('/p2pai/server/requests')
}

const navigateToModels = () => {
  router.push('/p2pai/server/models')
}

// Modal methods
const closeTrainingModal = () => {
  showTrainingModal.value = false
  selectedTraining.value = null
  modalLoading.value = false
}

const handleTrainingAction = () => {
  console.log('Handling training action for:', selectedTraining.value?.id)
  // TODO: Navigate to full training report
  closeTrainingModal()
}

const logout = () => {
  authStore.logout()
  router.push('/')
}

// Auto-refresh interval
let refreshInterval = null

onMounted(async () => {
  console.group('🚀 P2P AI Dashboard mounted')
  console.log('Loading dashboard data...')
  
  // Enable modern functionality
  enableShortcuts()
  
  // Initialize with some demo data for backwards compatibility
  accuracy.value = parseFloat((75 + Math.random() * 10).toFixed(2))
  
  // Handle role from URL parameters
  const role = route.query.role
  if (role && (role === 'client' || role === 'server')) {
    authStore.setUserType(role)
  }
  
  // Load initial data from API
  await loadDashboardData()
  
  // Set up auto-refresh every 30 seconds
  refreshInterval = setInterval(() => {
    if (!loading.value) {
      refreshData()
    }
  }, 30000)
  
  // Show welcome notification
  uiStore.addNotification({
    type: 'info',
    title: 'P2PAI Dashboard',
    message: 'Dashboard loaded with enhanced features',
    duration: 3000
  })
  
  console.log('Dashboard initialized with auto-refresh and modern features')
  console.groupEnd()
})

onUnmounted(() => {
  console.log('🧹 Cleaning up P2P AI Dashboard')
  
  // Disable modern functionality
  disableShortcuts()
  
  // Clear refresh interval
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  
  console.log('P2P AI Dashboard unmounted')
})
</script>