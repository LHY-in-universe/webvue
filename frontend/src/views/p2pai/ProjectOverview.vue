<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Navigation -->
    <nav class="glass-effect shadow-soft border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors micro-bounce"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            
            <div class="w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center mr-3 micro-bounce hover-glow-primary">
              <ChartPieIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gradient text-shadow-soft">
              Project Overview
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <select v-model="selectedTimeRange" class="input-base text-sm w-32">
                <option value="7d">Last 7 days</option>
                <option value="30d">Last 30 days</option>
                <option value="90d">Last 90 days</option>
                <option value="1y">Last year</option>
              </select>
            </div>
            <Button 
              @click="exportReport"
              variant="primary"
              :leftIcon="DocumentArrowDownIcon"
              size="sm"
            >
              Export Report
            </Button>
            <Button 
              @click="toggleTheme" 
              variant="ghost" 
              size="sm"
              iconOnly
              :leftIcon="themeStore.isDark ? SunIcon : MoonIcon"
            />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Page Header -->
      <div class="text-center mb-8 animate-fade-in-up">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Project Analytics Dashboard
        </h2>
        <p class="text-gray-600 dark:text-gray-400">
          Comprehensive overview of your federated learning project performance
        </p>
      </div>

      <!-- Key Performance Indicators -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 stagger-children">
        <StatCard
          title="Total Projects"
          :value="kpis.totalProjects"
          :icon="FolderIcon"
          variant="primary"
          :trend="kpis.projectsTrend"
          trend-label="vs last period"
          description="Active projects"
          animated
        />
        
        <StatCard
          title="Training Sessions"
          :value="kpis.totalSessions"
          :icon="PlayIcon"
          variant="success"
          :trend="kpis.sessionsTrend"
          trend-label="vs last period"
          description="Completed sessions"
          animated
        />
        
        <StatCard
          title="Success Rate"
          :value="kpis.successRate"
          unit="%"
          :precision="1"
          :icon="CheckBadgeIcon"
          variant="info"
          :trend="kpis.successRateTrend"
          trend-label="improvement"
          description="Training success"
          animated
        />

        <StatCard
          title="Total Participants"
          :value="kpis.totalParticipants"
          :icon="UserGroupIcon"
          variant="warning"
          :trend="kpis.participantsTrend"
          trend-label="growth"
          description="Federated nodes"
          animated
        />
      </div>

      <!-- Charts and Analytics -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Training Activity Chart -->
        <Card class="glass-effect">
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <ChartBarIcon class="w-5 h-5 mr-2 text-blue-500" />
                Training Activity
              </h3>
              <div class="flex items-center space-x-2">
                <button
                  v-for="period in ['Daily', 'Weekly', 'Monthly']"
                  :key="period"
                  @click="activityPeriod = period"
                  :class="[
                    'px-3 py-1 text-xs font-medium rounded-md transition-colors',
                    activityPeriod === period
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                      : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                  ]"
                >
                  {{ period }}
                </button>
              </div>
            </div>
            
            <!-- Training Activity Chart -->
            <div class="h-64">
              <Chart
                type="bar"
                :data="trainingActivityData"
                :options="chartOptions.activity"
              />
            </div>
          </div>
        </Card>

        <!-- Model Performance Distribution -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <ChartPieIcon class="w-5 h-5 mr-2 text-green-500" />
              Model Performance Distribution
            </h3>
            
            <!-- Performance bands -->
            <div class="space-y-4">
              <div v-for="band in performanceBands" :key="band.label">
                <div class="flex justify-between items-center mb-1">
                  <span class="text-sm text-gray-600 dark:text-gray-400">{{ band.label }}</span>
                  <span class="text-sm font-medium">{{ band.count }} models</span>
                </div>
                <ProgressBar 
                  :percentage="band.percentage" 
                  :variant="band.variant"
                  :show-percentage="true"
                />
              </div>
            </div>

            <!-- Average metrics -->
            <div class="mt-6 grid grid-cols-2 gap-4">
              <div class="text-center p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                <div class="text-lg font-bold text-green-600">{{ averageMetrics.accuracy.toFixed(1) }}%</div>
                <div class="text-xs text-gray-600 dark:text-gray-400">Avg Accuracy</div>
              </div>
              <div class="text-center p-3 bg-gray-50 dark:bg-slate-700 rounded-lg">
                <div class="text-lg font-bold text-blue-600">{{ averageMetrics.trainingTime.toFixed(1) }}h</div>
                <div class="text-xs text-gray-600 dark:text-gray-400">Avg Training Time</div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Resource Usage and Security -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <!-- Resource Usage -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <CpuChipIcon class="w-5 h-5 mr-2 text-purple-500" />
              Resource Usage
            </h3>
            
            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600 dark:text-gray-400">Compute Hours</span>
                  <span class="font-medium">{{ resourceUsage.computeHours.toFixed(1) }}h</span>
                </div>
                <ProgressBar :percentage="75" variant="primary" size="sm" />
              </div>
              
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600 dark:text-gray-400">Storage Used</span>
                  <span class="font-medium">{{ resourceUsage.storageGB.toFixed(1) }} GB</span>
                </div>
                <ProgressBar :percentage="45" variant="success" size="sm" />
              </div>
              
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600 dark:text-gray-400">Network Transfer</span>
                  <span class="font-medium">{{ resourceUsage.networkTB.toFixed(2) }} TB</span>
                </div>
                <ProgressBar :percentage="60" variant="warning" size="sm" />
              </div>
            </div>

            <div class="mt-6 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <div class="text-sm text-blue-800 dark:text-blue-200">
                <strong>Cost Estimate:</strong> ${{ resourceUsage.estimatedCost.toFixed(2) }}
              </div>
              <div class="text-xs text-blue-600 dark:text-blue-300 mt-1">
                Based on current usage patterns
              </div>
            </div>
          </div>
        </Card>

        <!-- Security Metrics -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <ShieldCheckIcon class="w-5 h-5 mr-2 text-red-500" />
              Security Metrics
            </h3>
            
            <div class="space-y-4">
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">Privacy Preserved Sessions</span>
                <span class="text-sm font-medium text-green-600">{{ securityMetrics.privacyPreserved }}%</span>
              </div>
              
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">Encrypted Connections</span>
                <span class="text-sm font-medium text-green-600">{{ securityMetrics.encryptedConnections }}%</span>
              </div>
              
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">MPC Protocols Used</span>
                <span class="text-sm font-medium text-blue-600">{{ securityMetrics.mpcProtocols }}</span>
              </div>
              
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">Security Incidents</span>
                <span class="text-sm font-medium text-red-600">{{ securityMetrics.securityIncidents }}</span>
              </div>
            </div>

            <div class="mt-6">
              <div class="flex items-center space-x-2 mb-2">
                <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                <span class="text-sm font-medium text-green-600">Security Status: Excellent</span>
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400">
                All security protocols are functioning correctly
              </div>
            </div>
          </div>
        </Card>

        <!-- Recent Activity -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <ClockIcon class="w-5 h-5 mr-2 text-orange-500" />
              Recent Activity
            </h3>
            
            <div class="space-y-3 max-h-64 overflow-y-auto scrollbar-thin">
              <div 
                v-for="activity in recentActivities" 
                :key="activity.id"
                class="flex items-start space-x-3 p-2 hover:bg-gray-50 dark:hover:bg-slate-700 rounded-lg transition-colors"
              >
                <div 
                  :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                    getActivityColor(activity.type)
                  ]"
                >
                  <component :is="getActivityIcon(activity.type)" class="w-4 h-4 text-white" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm text-gray-900 dark:text-white">{{ activity.description }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">
                    {{ formatTimeAgo(activity.timestamp) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Project Comparison -->
      <Card class="glass-effect mb-8">
        <div class="p-6">
          <ProjectTable
            :projects="projectComparison"
            :loading="false"
            @view-details="handleViewDetails"
            @edit-project="handleEditProject"
            @row-click="handleProjectSelect"
            @create-project="handleCreateProject"
          />
        </div>
      </Card>

      <!-- Recommendations -->
      <Card class="glass-effect">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <LightBulbIcon class="w-5 h-5 mr-2 text-yellow-500" />
            AI-Powered Recommendations
          </h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div 
              v-for="recommendation in recommendations" 
              :key="recommendation.id"
              class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-blue-300 dark:hover:border-blue-600 transition-colors"
            >
              <div class="flex items-start space-x-3">
                <div 
                  :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                    recommendation.priority === 'high' ? 'bg-red-100 text-red-600' :
                    recommendation.priority === 'medium' ? 'bg-yellow-100 text-yellow-600' :
                    'bg-green-100 text-green-600'
                  ]"
                >
                  <component :is="recommendation.icon" class="w-4 h-4" />
                </div>
                <div class="flex-1">
                  <h4 class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ recommendation.title }}
                  </h4>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {{ recommendation.description }}
                  </p>
                  <div class="mt-2">
                    <span 
                      :class="[
                        'px-2 py-1 text-xs font-medium rounded-md',
                        recommendation.priority === 'high' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                        recommendation.priority === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                        'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      ]"
                    >
                      {{ recommendation.priority.toUpperCase() }} PRIORITY
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import {
  ArrowLeftIcon,
  ChartPieIcon,
  SunIcon,
  MoonIcon,
  DocumentArrowDownIcon,
  FolderIcon,
  PlayIcon,
  CheckBadgeIcon,
  UserGroupIcon,
  ChartBarIcon,
  CpuChipIcon,
  ShieldCheckIcon,
  ClockIcon,
  PresentationChartLineIcon,
  LightBulbIcon,
  ExclamationTriangleIcon,
  CogIcon,
  RocketLaunchIcon
} from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import Chart from '@/components/ui/Chart.vue'
import ProjectTable from '@/components/tables/ProjectTable.vue'

const router = useRouter()
const themeStore = useThemeStore()

// State
const selectedTimeRange = ref('30d')
const activityPeriod = ref('Daily')

// KPIs
const kpis = ref({
  totalProjects: 12,
  projectsTrend: 8.5,
  totalSessions: 245,
  sessionsTrend: 15.2,
  successRate: 94.2,
  successRateTrend: 2.8,
  totalParticipants: 156,
  participantsTrend: 12.3
})

// Chart.js data configuration
const trainingActivityData = computed(() => ({
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  datasets: [
    {
      label: 'Training Sessions',
      data: [12, 21, 16, 24, 26, 9, 7],
      backgroundColor: 'rgba(59, 130, 246, 0.8)',
      borderColor: 'rgba(59, 130, 246, 1)',
      borderWidth: 2,
      borderRadius: 4
    },
    {
      label: 'Completed Sessions',
      data: [10, 19, 14, 22, 24, 8, 6],
      backgroundColor: 'rgba(16, 185, 129, 0.8)',
      borderColor: 'rgba(16, 185, 129, 1)',
      borderWidth: 2,
      borderRadius: 4
    }
  ]
}))

const chartOptions = ref({
  activity: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          color: '#6b7280'
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#6b7280'
        }
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        },
        ticks: {
          color: '#6b7280'
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  }
})

// Performance bands
const performanceBands = ref([
  { label: 'Excellent (>90%)', count: 8, percentage: 67, variant: 'success' },
  { label: 'Good (80-90%)', count: 3, percentage: 25, variant: 'info' },
  { label: 'Fair (70-80%)', count: 1, percentage: 8, variant: 'warning' },
  { label: 'Poor (<70%)', count: 0, percentage: 0, variant: 'danger' }
])

// Average metrics
const averageMetrics = ref({
  accuracy: 89.4,
  trainingTime: 4.2
})

// Resource usage
const resourceUsage = ref({
  computeHours: 342.5,
  storageGB: 125.8,
  networkTB: 2.34,
  estimatedCost: 1247.50
})

// Security metrics
const securityMetrics = ref({
  privacyPreserved: 100,
  encryptedConnections: 100,
  mpcProtocols: 3,
  securityIncidents: 0
})

// Recent activities
const recentActivities = ref([
  {
    id: 1,
    type: 'training',
    description: 'Federated training session completed for Image Classifier',
    timestamp: Date.now() - 1800000
  },
  {
    id: 2,
    type: 'model',
    description: 'New model "BERT Sentiment" deployed to production',
    timestamp: Date.now() - 3600000
  },
  {
    id: 3,
    type: 'security',
    description: 'MPC protocol security audit passed',
    timestamp: Date.now() - 7200000
  },
  {
    id: 4,
    type: 'dataset',
    description: 'Dataset "Customer Reviews" updated with 10k new samples',
    timestamp: Date.now() - 10800000
  },
  {
    id: 5,
    type: 'participant',
    description: '3 new participants joined federated network',
    timestamp: Date.now() - 14400000
  }
])

// Project comparison
const projectComparison = ref([
  {
    id: 1,
    name: 'Image Classification FL',
    type: 'Federated',
    participants: 12,
    accuracy: 94.2,
    trainingTime: 3.5,
    status: 'completed',
    createdAt: new Date('2024-01-15')
  },
  {
    id: 2,
    name: 'Privacy-Preserving NLP',
    type: 'MPC',
    participants: 5,
    accuracy: 91.8,
    trainingTime: 6.2,
    status: 'active',
    createdAt: new Date('2024-02-01')
  },
  {
    id: 3,
    name: 'Local CNN Training',
    type: 'Local',
    participants: 1,
    accuracy: 87.3,
    trainingTime: 2.1,
    status: 'completed',
    createdAt: new Date('2024-02-10')
  },
  {
    id: 4,
    name: 'Collaborative Learning',
    type: 'Federated',
    participants: 8,
    accuracy: 89.6,
    trainingTime: 4.8,
    status: 'training',
    createdAt: new Date('2024-02-15')
  }
])

// AI Recommendations
const recommendations = ref([
  {
    id: 1,
    title: 'Optimize Training Schedule',
    description: 'Schedule training during off-peak hours to reduce costs by 23%',
    priority: 'high',
    icon: ClockIcon
  },
  {
    id: 2,
    title: 'Increase Federated Participants',
    description: 'Add 2-3 more participants to improve model generalization',
    priority: 'medium',
    icon: UserGroupIcon
  },
  {
    id: 3,
    title: 'Enable Auto-scaling',
    description: 'Configure auto-scaling to handle variable workloads efficiently',
    priority: 'low',
    icon: CogIcon
  },
  {
    id: 4,
    title: 'Upgrade Security Protocols',
    description: 'Consider upgrading to latest MPC protocol for enhanced privacy',
    priority: 'medium',
    icon: ShieldCheckIcon
  }
])

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const exportReport = () => {
  console.log('Exporting project report...')
  // Simulate report generation
}

const getActivityColor = (type) => {
  const colors = {
    training: 'bg-blue-500',
    model: 'bg-green-500',
    security: 'bg-red-500',
    dataset: 'bg-purple-500',
    participant: 'bg-orange-500'
  }
  return colors[type] || 'bg-gray-500'
}

const getActivityIcon = (type) => {
  const icons = {
    training: PlayIcon,
    model: CpuChipIcon,
    security: ShieldCheckIcon,
    dataset: FolderIcon,
    participant: UserGroupIcon
  }
  return icons[type] || ClockIcon
}


const formatTimeAgo = (timestamp) => {
  const diff = Date.now() - timestamp
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days}d ago`
  if (hours > 0) return `${hours}h ago`
  return `${minutes}m ago`
}

const formatDate = (date) => {
  return date.toLocaleDateString()
}

// Project table event handlers
const handleViewDetails = (project) => {
  router.push(`/p2pai/projects/${project.id}`)
}

const handleEditProject = (project) => {
  router.push(`/p2pai/projects/${project.id}/edit`)
}

const handleProjectSelect = (project) => {
  console.log('Project selected:', project)
}

const handleCreateProject = () => {
  router.push('/p2pai/projects/create')
}

// Lifecycle
onMounted(() => {
  // Initialize component
})
</script>

<style scoped>
/* Custom scrollbar styles */
.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.dark .scrollbar-thin::-webkit-scrollbar-track {
  background: #1e293b;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.dark .scrollbar-thin::-webkit-scrollbar-thumb {
  background: #475569;
}

/* Chart hover effects */
.h-full > div:hover {
  transform: scale(1.05);
}
</style>