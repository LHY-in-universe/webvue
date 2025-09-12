<template>
  <div :class="tableContainerClasses">
    <!-- Table Header -->
    <div v-if="title || $slots.header || showSearch || actions?.length" :class="headerContainerClasses">
      <div :class="headerContentClasses">
        <div v-if="title || $slots.title">
          <slot name="title">
            <h3 :class="titleClasses">{{ title }}</h3>
          </slot>
        </div>
        
        <!-- Search Input -->
        <div v-if="showSearch" :class="searchContainerClasses">
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="searchPlaceholder"
            :class="searchInputClasses"
          />
        </div>
      </div>

      <div v-if="$slots.header || actions?.length" :class="actionContainerClasses">
        <slot name="header" />
        <Button
          v-for="action in actions"
          :key="action.key"
          :variant="action.variant || 'secondary'"
          :size="isMobile ? 'sm' : (action.size || 'sm')"
          :leftIcon="isMobile ? null : action.icon"
          @click="action.handler"
        >
          <span v-if="isMobile" :class="mobileActionClasses">{{ action.label }}</span>
          <span v-else>{{ action.label }}</span>
        </Button>
      </div>
    </div>

    <!-- Mobile/Desktop Toggle -->
    <div v-if="isMobile && allowToggleView" class="mb-4 flex justify-end">
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-600 dark:text-gray-400">View:</span>
        <button
          @click="mobileViewMode = 'table'"
          :class="[
            'px-3 py-1 text-sm rounded-lg transition-colors',
            mobileViewMode === 'table' 
              ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' 
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
        >
          Table
        </button>
        <button
          @click="mobileViewMode = 'cards'"
          :class="[
            'px-3 py-1 text-sm rounded-lg transition-colors',
            mobileViewMode === 'cards' 
              ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' 
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
        >
          Cards
        </button>
      </div>
    </div>

    <!-- Desktop Table View -->
    <div v-if="!isMobile || mobileViewMode === 'table'" :class="scrollableClasses">
      <table class="w-full">
        <!-- Table Head -->
        <thead v-if="!isMobile || showHeaderOnMobile">
          <tr :class="headerRowClasses">
            <th
              v-for="column in visibleColumns"
              :key="column.key"
              :class="[
                headerCellClasses,
                column.align ? `text-${column.align}` : 'text-left',
                column.sortable && 'cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700',
                column.width && `w-${column.width}`,
                isMobile && mobileHeaderClasses
              ]"
              @click="column.sortable ? handleSort(column.key) : null"
            >
              <div class="flex items-center space-x-1">
                <span :class="isMobile ? 'text-xs' : ''">{{ column.title }}</span>
                <div v-if="column.sortable" class="flex flex-col">
                  <ChevronUpIcon 
                    :class="[
                      isMobile ? 'w-2 h-2' : 'w-3 h-3',
                      'transition-colors',
                      sortKey === column.key && sortOrder === 'asc' 
                        ? 'text-blue-600' : 'text-gray-400'
                    ]" 
                  />
                  <ChevronDownIcon 
                    :class="[
                      isMobile ? 'w-2 h-2' : 'w-3 h-3',
                      'transition-colors -mt-1',
                      sortKey === column.key && sortOrder === 'desc' 
                        ? 'text-blue-600' : 'text-gray-400'
                    ]" 
                  />
                </div>
              </div>
            </th>
          </tr>
        </thead>

        <!-- Table Body -->
        <tbody :class="bodyClasses">
          <!-- Loading State -->
          <tr v-if="loading">
            <td :colspan="visibleColumns.length" class="px-4 py-8 text-center">
              <LoadingSpinner size="sm" text="Loading data..." />
            </td>
          </tr>

          <!-- Empty State -->
          <tr v-else-if="!paginatedData.length">
            <td :colspan="visibleColumns.length" class="px-4 py-8">
              <EmptyState
                :icon="emptyStateIcon"
                :title="emptyStateTitle"
                :description="emptyStateDescription"
                size="sm"
                padding="sm"
                :primary-action="emptyStateAction"
              />
            </td>
          </tr>

          <!-- Data Rows -->
          <tr
            v-else
            v-for="(row, rowIndex) in paginatedData"
            :key="getRowKey(row, rowIndex)"
            :class="[
              rowClasses,
              rowHover && 'hover:bg-gray-50 dark:hover:bg-gray-700',
              selectable && 'cursor-pointer',
              selectedRows.includes(getRowKey(row, rowIndex)) && 'bg-blue-50 dark:bg-blue-900/20'
            ]"
            @click="handleRowClick(row, rowIndex)"
          >
            <td
              v-for="column in visibleColumns"
              :key="column.key"
              :class="[
                cellClasses,
                column.align ? `text-${column.align}` : 'text-left'
              ]"
            >
              <slot 
                :name="`cell(${column.key})`" 
                :value="getCellValue(row, column.key)"
                :row="row" 
                :column="column"
                :index="rowIndex"
              >
                <component 
                  v-if="column.component" 
                  :is="column.component" 
                  :value="getCellValue(row, column.key)"
                  :row="row"
                />
                <span v-else-if="column.format">
                  {{ formatCellValue(getCellValue(row, column.key), column.format) }}
                </span>
                <span v-else>
                  {{ getCellValue(row, column.key) }}
                </span>
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mobile Card View -->
    <div v-else-if="isMobile && mobileViewMode === 'cards'" class="space-y-3">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-8">
        <LoadingSpinner size="sm" text="Loading data..." />
      </div>

      <!-- Empty State -->
      <div v-else-if="!paginatedData.length" class="py-8">
        <EmptyState
          :icon="emptyStateIcon"
          :title="emptyStateTitle"
          :description="emptyStateDescription"
          size="sm"
          padding="sm"
          :primary-action="emptyStateAction"
        />
      </div>

      <!-- Data Cards -->
      <div
        v-else
        v-for="(row, rowIndex) in paginatedData"
        :key="getRowKey(row, rowIndex)"
        :class="[
          'bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 shadow-sm',
          selectable && 'cursor-pointer hover:shadow-md transition-shadow',
          selectedRows.includes(getRowKey(row, rowIndex)) && 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20'
        ]"
        @click="handleRowClick(row, rowIndex)"
      >
        <div class="space-y-2">
          <div
            v-for="column in primaryMobileColumns"
            :key="column.key"
            class="flex justify-between items-start"
          >
            <span class="text-sm font-medium text-gray-600 dark:text-gray-400 flex-shrink-0 w-1/3">
              {{ column.title }}:
            </span>
            <div class="flex-1 text-right">
              <slot 
                :name="`cell(${column.key})`" 
                :value="getCellValue(row, column.key)"
                :row="row" 
                :column="column"
                :index="rowIndex"
              >
                <component 
                  v-if="column.component" 
                  :is="column.component" 
                  :value="getCellValue(row, column.key)"
                  :row="row"
                />
                <span v-else-if="column.format" class="text-sm text-gray-900 dark:text-white">
                  {{ formatCellValue(getCellValue(row, column.key), column.format) }}
                </span>
                <span v-else class="text-sm text-gray-900 dark:text-white">
                  {{ getCellValue(row, column.key) }}
                </span>
              </slot>
            </div>
          </div>
          
          <!-- Show more details button for additional columns -->
          <div v-if="secondaryMobileColumns.length > 0" class="pt-2 border-t border-gray-100 dark:border-gray-700">
            <button
              @click="toggleCardExpanded(getRowKey(row, rowIndex))"
              class="text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
            >
              {{ expandedCards.includes(getRowKey(row, rowIndex)) ? 'Show Less' : 'Show More' }}
            </button>
            
            <div v-if="expandedCards.includes(getRowKey(row, rowIndex))" class="mt-2 space-y-1">
              <div
                v-for="column in secondaryMobileColumns"
                :key="column.key"
                class="flex justify-between items-start text-xs"
              >
                <span class="text-gray-500 dark:text-gray-400 w-1/3">
                  {{ column.title }}:
                </span>
                <div class="flex-1 text-right">
                  <slot 
                    :name="`cell(${column.key})`" 
                    :value="getCellValue(row, column.key)"
                    :row="row" 
                    :column="column"
                    :index="rowIndex"
                  >
                    <span class="text-gray-600 dark:text-gray-300">
                      {{ getCellValue(row, column.key) }}
                    </span>
                  </slot>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Table Footer -->
    <div v-if="showPagination || $slots.footer" class="mt-4 flex items-center justify-between">
      <div v-if="$slots.footer">
        <slot name="footer" />
      </div>
      
      <!-- Pagination -->
      <div v-if="showPagination && totalPages > 1" class="flex items-center space-x-2">
        <span class="text-sm text-gray-600 dark:text-gray-400">
          Showing {{ startIndex + 1 }} to {{ Math.min(endIndex, filteredData.length) }} 
          of {{ filteredData.length }} results
        </span>
        
        <div class="flex items-center space-x-1">
          <Button
            variant="ghost"
            size="sm"
            :disabled="currentPage === 1"
            @click="currentPage = 1"
          >
            First
          </Button>
          
          <Button
            variant="ghost"
            size="sm"
            :disabled="currentPage === 1"
            @click="currentPage--"
          >
            Previous
          </Button>
          
          <span class="text-sm text-gray-600 dark:text-gray-400 px-2">
            Page {{ currentPage }} of {{ totalPages }}
          </span>
          
          <Button
            variant="ghost"
            size="sm"
            :disabled="currentPage === totalPages"
            @click="currentPage++"
          >
            Next
          </Button>
          
          <Button
            variant="ghost"
            size="sm"
            :disabled="currentPage === totalPages"
            @click="currentPage = totalPages"
          >
            Last
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import Button from './Button.vue'
import LoadingSpinner from './LoadingSpinner.vue'
import EmptyState from './EmptyState.vue'
import {
  MagnifyingGlassIcon,
  ChevronUpIcon,
  ChevronDownIcon,
  TableCellsIcon
} from '@heroicons/vue/24/outline'

// Responsive composable
const { isMobile, isTablet, getResponsiveClasses, containerPadding } = useResponsive()

const props = defineProps({
  title: String,
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  columns: {
    type: Array,
    required: true,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'striped', 'bordered', 'minimal'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  },
  // Search functionality
  showSearch: {
    type: Boolean,
    default: false
  },
  searchPlaceholder: {
    type: String,
    default: 'Search...'
  },
  searchable: {
    type: Array,
    default: () => []
  },
  // Sorting
  sortable: {
    type: Boolean,
    default: true
  },
  defaultSort: {
    type: Object,
    default: null
  },
  // Pagination
  showPagination: {
    type: Boolean,
    default: false
  },
  pageSize: {
    type: Number,
    default: 10
  },
  // Selection
  selectable: {
    type: Boolean,
    default: false
  },
  rowKey: {
    type: String,
    default: 'id'
  },
  // Styling
  rowHover: {
    type: Boolean,
    default: true
  },
  responsive: {
    type: Boolean,
    default: true
  },
  // Actions
  actions: {
    type: Array,
    default: () => []
  },
  // Empty state
  emptyStateTitle: {
    type: String,
    default: 'No Data Available'
  },
  emptyStateDescription: {
    type: String,
    default: 'There is no data to display.'
  },
  emptyStateIcon: {
    type: [Object, Function],
    default: () => TableCellsIcon
  },
  emptyStateAction: {
    type: Object,
    default: null
  },
  // Mobile-specific options
  allowToggleView: {
    type: Boolean,
    default: true
  },
  showHeaderOnMobile: {
    type: Boolean,
    default: false
  },
  mobileColumnsLimit: {
    type: Number,
    default: 3
  }
})

const emit = defineEmits(['sort', 'row-click', 'selection-change'])

// Reactive data
// Mobile state
const mobileViewMode = ref('table')
const expandedCards = ref([])
const searchQuery = ref('')
const sortKey = ref(props.defaultSort?.key || '')
const sortOrder = ref(props.defaultSort?.order || 'asc')
const currentPage = ref(1)
const selectedRows = ref([])

// Computed properties
const visibleColumns = computed(() => {
  return props.columns.filter(column => !column.hidden)
})

const filteredData = computed(() => {
  if (!searchQuery.value || !props.searchable.length) {
    return props.data
  }

  const query = searchQuery.value.toLowerCase()
  return props.data.filter(row => {
    return props.searchable.some(field => {
      const value = getCellValue(row, field)
      return String(value).toLowerCase().includes(query)
    })
  })
})

const sortedData = computed(() => {
  if (!sortKey.value) return filteredData.value

  return [...filteredData.value].sort((a, b) => {
    const aVal = getCellValue(a, sortKey.value)
    const bVal = getCellValue(b, sortKey.value)

    let comparison = 0
    if (aVal > bVal) comparison = 1
    if (aVal < bVal) comparison = -1

    return sortOrder.value === 'desc' ? -comparison : comparison
  })
})

const totalPages = computed(() => {
  if (!props.showPagination) return 1
  return Math.ceil(filteredData.value.length / props.pageSize)
})

const startIndex = computed(() => {
  return (currentPage.value - 1) * props.pageSize
})

const endIndex = computed(() => {
  return startIndex.value + props.pageSize
})

const paginatedData = computed(() => {
  if (!props.showPagination) return sortedData.value
  return sortedData.value.slice(startIndex.value, endIndex.value)
})

// Styling classes
const tableContainerClasses = computed(() => {
  const base = 'data-table'
  return `${base} ${props.responsive ? 'overflow-hidden' : ''}`
})

const scrollableClasses = computed(() => {
  return props.responsive ? 'overflow-x-auto' : ''
})

const headerRowClasses = computed(() => {
  const variants = {
    default: 'border-b border-gray-200 dark:border-gray-700',
    striped: 'border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800',
    bordered: 'border border-gray-200 dark:border-gray-700',
    minimal: 'border-b border-gray-100 dark:border-gray-800'
  }
  return variants[props.variant] || variants.default
})

const headerCellClasses = computed(() => {
  const sizes = {
    sm: 'px-3 py-2 text-xs',
    md: 'px-4 py-3 text-sm',
    lg: 'px-6 py-4 text-base'
  }
  
  return `${sizes[props.size]} font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider`
})

const bodyClasses = computed(() => {
  const variants = {
    default: 'divide-y divide-gray-200 dark:divide-gray-700',
    striped: 'divide-y divide-gray-200 dark:divide-gray-700',
    bordered: 'border border-gray-200 dark:border-gray-700',
    minimal: 'divide-y divide-gray-100 dark:divide-gray-800'
  }
  return variants[props.variant] || variants.default
})

const rowClasses = computed(() => {
  const base = 'transition-colors'
  if (props.variant === 'striped') {
    return `${base} even:bg-gray-50 even:dark:bg-gray-800/50`
  }
  return base
})

const cellClasses = computed(() => {
  const sizes = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-3 text-sm',
    lg: 'px-6 py-4 text-base'
  }
  
  return `${sizes[props.size]} text-gray-900 dark:text-white`
})

// Mobile-specific computed properties
const headerContainerClasses = computed(() => {
  return getResponsiveClasses({
    xs: 'mb-4 flex flex-col space-y-3',
    md: 'mb-4 flex items-center justify-between'
  })
})

const headerContentClasses = computed(() => {
  return getResponsiveClasses({
    xs: 'flex flex-col space-y-3',
    md: 'flex items-center space-x-4'
  })
})

const titleClasses = computed(() => {
  return getResponsiveClasses({
    xs: 'text-lg font-semibold text-gray-900 dark:text-white',
    md: 'text-lg font-semibold text-gray-900 dark:text-white'
  })
})

const searchContainerClasses = computed(() => {
  return getResponsiveClasses({
    xs: 'relative w-full',
    md: 'relative'
  })
})

const searchInputClasses = computed(() => {
  return getResponsiveClasses({
    xs: 'pl-10 pr-4 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent w-full',
    md: 'pl-10 pr-4 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent'
  })
})

const actionContainerClasses = computed(() => {
  return getResponsiveClasses({
    xs: 'flex items-center space-x-1 justify-center',
    md: 'flex items-center space-x-2'
  })
})

const mobileActionClasses = computed(() => {
  return 'text-xs'
})

const mobileHeaderClasses = computed(() => {
  return 'px-2 py-1'
})

const primaryMobileColumns = computed(() => {
  return visibleColumns.value.slice(0, props.mobileColumnsLimit)
})

const secondaryMobileColumns = computed(() => {
  return visibleColumns.value.slice(props.mobileColumnsLimit)
})

// Methods
const getCellValue = (row, key) => {
  return key.split('.').reduce((obj, k) => obj?.[k], row)
}

const getRowKey = (row, index) => {
  return props.rowKey ? getCellValue(row, props.rowKey) : index
}

const formatCellValue = (value, format) => {
  switch (format) {
    case 'date':
      return new Date(value).toLocaleDateString()
    case 'datetime':
      return new Date(value).toLocaleString()
    case 'currency':
      return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
    case 'number':
      return new Intl.NumberFormat().format(value)
    case 'percentage':
      return `${(value * 100).toFixed(1)}%`
    default:
      return value
  }
}

const handleSort = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  
  emit('sort', { key: sortKey.value, order: sortOrder.value })
}

const handleRowClick = (row, index) => {
  if (props.selectable) {
    const key = getRowKey(row, index)
    const selectedIndex = selectedRows.value.indexOf(key)
    
    if (selectedIndex > -1) {
      selectedRows.value.splice(selectedIndex, 1)
    } else {
      selectedRows.value.push(key)
    }
    
    emit('selection-change', selectedRows.value)
  }
  
  emit('row-click', row, index)
}

// Mobile-specific methods
const toggleCardExpanded = (rowKey) => {
  const index = expandedCards.value.indexOf(rowKey)
  if (index > -1) {
    expandedCards.value.splice(index, 1)
  } else {
    expandedCards.value.push(rowKey)
  }
}

// Watch for mobile view mode changes to reset expanded cards
watch(mobileViewMode, () => {
  expandedCards.value = []
})

// Watch for search query changes to reset pagination
watch(searchQuery, () => {
  currentPage.value = 1
})
</script>

<style scoped>
.data-table {
  @apply w-full;
}

/* Responsive table improvements */
@media (max-width: 640px) {
  .data-table table,
  .data-table thead,
  .data-table tbody,
  .data-table th,
  .data-table td,
  .data-table tr {
    @apply block;
  }

  .data-table thead tr {
    @apply absolute -top-full -left-full;
  }

  .data-table tr {
    @apply border border-gray-200 dark:border-gray-700 mb-2 rounded-lg p-4;
  }

  .data-table td {
    @apply border-none relative pl-12 py-2;
  }

  .data-table td:before {
    content: attr(data-label);
    @apply absolute left-2 top-2 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase;
  }
}
</style>