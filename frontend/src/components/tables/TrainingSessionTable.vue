<template>
  <DataTable
    :data="sessions"
    :columns="columns"
    :loading="loading"
    :show-search="true"
    :searchable="['sessionId', 'modelName', 'status']"
    search-placeholder="Search training sessions..."
    :show-pagination="sessions.length > 8"
    :page-size="8"
    :sortable="true"
    :default-sort="{ key: 'startTime', order: 'desc' }"
    :row-hover="true"
    variant="striped"
    size="sm"
    empty-state-title="No Training Sessions"
    empty-state-description="Start your first training session to see results here."
    :empty-state-action="{
      label: 'Start Training',
      handler: () => $emit('start-training'),
      variant: 'primary'
    }"
    @row-click="handleRowClick"
    @sort="$emit('sort', $event)"
  >
    <template #title>
      <div class="flex items-center">
        <PlayIcon class="w-5 h-5 mr-2 text-green-500" />
        {{ title || 'Training Sessions' }}
        <div v-if="liveCount > 0" class="ml-3 flex items-center">
          <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse mr-1"></div>
          <span class="text-sm text-gray-600 dark:text-gray-400">{{ liveCount }} live</span>
        </div>
      </div>
    </template>

    <template #header>
      <Button
        variant="ghost"
        size="sm"
        :leftIcon="ArrowPathIcon"
        @click="$emit('refresh')"
        :disabled="loading"
      >
        Refresh
      </Button>
    </template>

    <!-- Session ID -->
    <template #cell(sessionId)="{ value, row }">
      <div class="font-mono text-sm">
        <span class="font-medium text-gray-900 dark:text-white">{{ value.slice(0, 8) }}</span>
        <div class="text-xs text-gray-500 dark:text-gray-400">
          {{ row.modelName }}
        </div>
      </div>
    </template>

    <!-- Progress -->
    <template #cell(progress)="{ value, row }">
      <div class="space-y-1">
        <div class="flex items-center justify-between text-xs">
          <span class="text-gray-600 dark:text-gray-400">{{ value }}%</span>
          <span class="text-gray-500 dark:text-gray-500">
            {{ row.currentEpoch }}/{{ row.totalEpochs }}
          </span>
        </div>
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            class="bg-blue-500 h-2 rounded-full transition-all duration-500"
            :style="{ width: `${value}%` }"
          ></div>
        </div>
      </div>
    </template>

    <!-- Accuracy -->
    <template #cell(accuracy)="{ value }">
      <div v-if="value !== null" class="text-center">
        <span :class="[
          'text-sm font-medium',
          value >= 90 ? 'text-green-600' : value >= 80 ? 'text-yellow-600' : 'text-red-600'
        ]">
          {{ value.toFixed(2) }}%
        </span>
      </div>
      <div v-else class="text-center">
        <span class="text-xs text-gray-400">Pending</span>
      </div>
    </template>

    <!-- Loss -->
    <template #cell(loss)="{ value }">
      <div v-if="value !== null" class="text-center">
        <span class="text-sm font-medium text-gray-900 dark:text-white">
          {{ value.toFixed(4) }}
        </span>
      </div>
      <div v-else class="text-center">
        <span class="text-xs text-gray-400">-</span>
      </div>
    </template>

    <!-- Duration -->
    <template #cell(duration)="{ value, row }">
      <div class="flex items-center text-sm">
        <ClockIcon class="w-3 h-3 text-gray-400 mr-1" />
        <span class="text-gray-900 dark:text-white">
          {{ formatDuration(value, row.status) }}
        </span>
      </div>
    </template>

    <!-- Participants -->
    <template #cell(participants)="{ value }">
      <div class="flex items-center justify-center">
        <div class="flex -space-x-1">
          <div
            v-for="i in Math.min(value, 4)"
            :key="i"
            class="w-6 h-6 rounded-full border-2 border-white dark:border-gray-800 flex items-center justify-center text-xs font-medium"
            :class="getParticipantColor(i)"
          >
            {{ i }}
          </div>
          <div
            v-if="value > 4"
            class="w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-600 border-2 border-white dark:border-gray-800 flex items-center justify-center text-xs font-medium text-gray-600 dark:text-gray-300"
          >
            +{{ value - 4 }}
          </div>
        </div>
      </div>
    </template>

    <!-- Status -->
    <template #cell(status)="{ value }">
      <StatusBadge 
        :status="getStatusMapping(value)"
        :label="value"
        variant="filled"
        size="xs"
        :icon="getStatusIcon(value)"
      />
    </template>

    <!-- Actions -->
    <template #cell(actions)="{ row }">
      <div class="flex items-center justify-center space-x-1">
        <Button
          variant="ghost"
          size="xs"
          @click.stop="$emit('view-details', row)"
        >
          View
        </Button>
        <Button
          v-if="canStop(row.status)"
          variant="ghost"
          size="xs"
          @click.stop="$emit('stop-session', row)"
        >
          Stop
        </Button>
        <Button
          v-if="canRestart(row.status)"
          variant="ghost"
          size="xs"
          @click.stop="$emit('restart-session', row)"
        >
          Restart
        </Button>
      </div>
    </template>
  </DataTable>
</template>

<script setup>
import { computed } from 'vue'
import DataTable from '@/components/ui/DataTable.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Button from '@/components/ui/Button.vue'
import {
  PlayIcon,
  ClockIcon,
  ArrowPathIcon,
  StopIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  PauseCircleIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  sessions: {
    type: Array,
    required: true,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  title: String,
  showActions: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['start-training', 'view-details', 'stop-session', 'restart-session', 'row-click', 'sort', 'refresh'])

const liveCount = computed(() => {
  return props.sessions.filter(session => 
    session.status === 'Running' || session.status === 'Training'
  ).length
})

const columns = computed(() => {
  const baseColumns = [
    {
      key: 'sessionId',
      title: 'Session',
      sortable: true,
      width: '1/6'
    },
    {
      key: 'progress',
      title: 'Progress',
      sortable: true,
      align: 'center'
    },
    {
      key: 'accuracy',
      title: 'Accuracy',
      sortable: true,
      align: 'center'
    },
    {
      key: 'loss',
      title: 'Loss',
      sortable: true,
      align: 'center'
    },
    {
      key: 'duration',
      title: 'Duration',
      sortable: true,
      align: 'center'
    },
    {
      key: 'participants',
      title: 'Participants',
      sortable: true,
      align: 'center'
    },
    {
      key: 'status',
      title: 'Status',
      sortable: true,
      align: 'center'
    }
  ]

  if (props.showActions) {
    baseColumns.push({
      key: 'actions',
      title: 'Actions',
      sortable: false,
      align: 'center',
      width: '1/8'
    })
  }

  return baseColumns
})

const formatDuration = (duration, status) => {
  if (status === 'Running' && !duration) return 'Live'
  if (!duration) return '-'
  
  const hours = Math.floor(duration / 3600)
  const minutes = Math.floor((duration % 3600) / 60)
  
  if (hours > 0) return `${hours}h ${minutes}m`
  return `${minutes}m`
}

const getParticipantColor = (index) => {
  const colors = [
    'bg-blue-500 text-white',
    'bg-green-500 text-white',
    'bg-yellow-500 text-white',
    'bg-purple-500 text-white'
  ]
  return colors[(index - 1) % colors.length]
}

const getStatusMapping = (status) => {
  const statusMapping = {
    'Running': 'running',
    'Training': 'running',
    'Completed': 'completed',
    'Failed': 'failed',
    'Stopped': 'inactive',
    'Pending': 'pending',
    'Paused': 'warning'
  }
  return statusMapping[status] || 'pending'
}

const getStatusIcon = (status) => {
  const iconMapping = {
    'Running': PlayIcon,
    'Training': PlayIcon,
    'Completed': CheckCircleIcon,
    'Failed': ExclamationCircleIcon,
    'Stopped': StopIcon,
    'Pending': ClockIcon,
    'Paused': PauseCircleIcon
  }
  return iconMapping[status] || ClockIcon
}

const canStop = (status) => {
  return ['Running', 'Training'].includes(status)
}

const canRestart = (status) => {
  return ['Failed', 'Stopped', 'Completed'].includes(status)
}

const handleRowClick = (row) => {
  emit('row-click', row)
}
</script>