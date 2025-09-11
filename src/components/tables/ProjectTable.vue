<template>
  <DataTable
    :data="projects"
    :columns="columns"
    :loading="loading"
    :show-search="true"
    :searchable="['name', 'type', 'status']"
    search-placeholder="Search projects..."
    :show-pagination="projects.length > 10"
    :page-size="10"
    :sortable="true"
    :default-sort="{ key: 'createdAt', order: 'desc' }"
    :row-hover="true"
    variant="default"
    size="md"
    empty-state-title="No Projects Found"
    empty-state-description="Create your first project to get started with federated learning."
    :empty-state-action="{
      label: 'Create Project',
      handler: () => $emit('create-project'),
      variant: 'primary'
    }"
    @row-click="handleRowClick"
    @sort="$emit('sort', $event)"
  >
    <template #title>
      <div class="flex items-center">
        <PresentationChartLineIcon class="w-5 h-5 mr-2 text-indigo-500" />
        {{ title || 'Project Performance Comparison' }}
      </div>
    </template>

    <!-- Project Name and Details -->
    <template #cell(name)="{ row }">
      <div>
        <div class="text-sm font-medium text-gray-900 dark:text-white">
          {{ row.name }}
        </div>
        <div class="text-xs text-gray-500 dark:text-gray-400">
          Created {{ formatDate(row.createdAt) }}
        </div>
      </div>
    </template>

    <!-- Project Type Badge -->
    <template #cell(type)="{ value }">
      <StatusBadge 
        :status="getProjectTypeStatus(value)"
        :label="value"
        variant="subtle"
        size="sm"
      />
    </template>

    <!-- Participants Count -->
    <template #cell(participants)="{ value }">
      <div class="flex items-center">
        <UsersIcon class="w-4 h-4 text-gray-400 mr-1" />
        <span class="text-sm font-medium text-gray-900 dark:text-white">{{ value }}</span>
      </div>
    </template>

    <!-- Accuracy with Progress -->
    <template #cell(accuracy)="{ value }">
      <div class="flex items-center space-x-2">
        <span class="text-sm font-medium text-green-600">
          {{ value.toFixed(1) }}%
        </span>
        <div class="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            class="bg-green-500 h-2 rounded-full transition-all duration-300"
            :style="{ width: `${value}%` }"
          ></div>
        </div>
      </div>
    </template>

    <!-- Training Time with Icon -->
    <template #cell(trainingTime)="{ value }">
      <div class="flex items-center">
        <ClockIcon class="w-4 h-4 text-gray-400 mr-1" />
        <span class="text-sm text-gray-900 dark:text-white">{{ value }}h</span>
      </div>
    </template>

    <!-- Status Badge -->
    <template #cell(status)="{ value }">
      <StatusBadge 
        :status="getStatusMapping(value)"
        :label="value"
        variant="filled"
        size="sm"
      />
    </template>

    <!-- Actions -->
    <template #cell(actions)="{ row }">
      <div class="flex items-center space-x-2">
        <Button
          variant="ghost"
          size="xs"
          @click.stop="$emit('view-details', row)"
        >
          View
        </Button>
        <Button
          variant="ghost"
          size="xs"
          @click.stop="$emit('edit-project', row)"
        >
          Edit
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
  PresentationChartLineIcon,
  UsersIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  projects: {
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

const emit = defineEmits(['create-project', 'view-details', 'edit-project', 'row-click', 'sort'])

const columns = computed(() => {
  const baseColumns = [
    {
      key: 'name',
      title: 'Project',
      sortable: true,
      width: '1/4'
    },
    {
      key: 'type',
      title: 'Type',
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
      key: 'accuracy',
      title: 'Accuracy',
      sortable: true,
      align: 'center'
    },
    {
      key: 'trainingTime',
      title: 'Training Time',
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

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = now - date
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`
  return `${Math.floor(diffDays / 365)} years ago`
}

const getProjectTypeStatus = (type) => {
  const typeMapping = {
    'Federated Learning': 'info',
    'MPC Training': 'success',
    'Edge AI': 'warning',
    'Blockchain': 'pending'
  }
  return typeMapping[type] || 'info'
}

const getStatusMapping = (status) => {
  const statusMapping = {
    'Completed': 'completed',
    'Running': 'running',
    'Failed': 'failed',
    'Pending': 'pending',
    'Active': 'active',
    'Inactive': 'inactive'
  }
  return statusMapping[status] || 'pending'
}

const handleRowClick = (row) => {
  emit('row-click', row)
}
</script>