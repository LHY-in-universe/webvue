<template>
  <div :class="containerClasses" ref="searchContainer">
    <!-- Search Input -->
    <div :class="inputContainerClasses">
      <!-- Search Icon -->
      <div class="absolute left-3 top-1/2 transform -translate-y-1/2">
        <MagnifyingGlassIcon v-if="!searching" class="w-5 h-5 text-gray-400" />
        <div v-else class="w-5 h-5">
          <div class="animate-spin rounded-full h-4 w-4 border-2 border-blue-500 border-t-transparent"></div>
        </div>
      </div>

      <!-- Input Field -->
      <input
        ref="searchInput"
        v-model="searchQuery"
        :type="inputType"
        :placeholder="placeholder"
        :disabled="disabled || searching"
        :class="inputClasses"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
        @keydown="handleKeydown"
        @keyup="handleKeyup"
        :autocomplete="autocomplete"
        :spellcheck="spellcheck"
      />

      <!-- Clear Button -->
      <button
        v-if="searchQuery && clearable"
        @click="clearSearch"
        class="absolute right-12 top-1/2 transform -translate-y-1/2 p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-colors"
        :aria-label="clearButtonLabel"
      >
        <XMarkIcon class="w-4 h-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
      </button>

      <!-- Search Button -->
      <button
        v-if="showSearchButton"
        @click="performSearch"
        :disabled="disabled || searching || !searchQuery.trim()"
        :class="searchButtonClasses"
      >
        <MagnifyingGlassIcon v-if="!searching" class="w-4 h-4" />
        <div v-else class="w-4 h-4">
          <div class="animate-spin rounded-full h-3 w-3 border-2 border-white border-t-transparent"></div>
        </div>
      </button>
    </div>

    <!-- Advanced Search Toggle -->
    <button
      v-if="allowAdvanced && !isMobile"
      @click="showAdvanced = !showAdvanced"
      :class="advancedToggleClasses"
    >
      <AdjustmentsHorizontalIcon class="w-4 h-4 mr-1" />
      Advanced
      <ChevronDownIcon 
        :class="['w-4 h-4 ml-1 transition-transform', showAdvanced ? 'rotate-180' : '']" 
      />
    </button>

    <!-- Results Dropdown -->
    <div
      v-if="showResults && (results.length > 0 || showNoResults)"
      :class="dropdownClasses"
    >
      <!-- Recent Searches -->
      <div v-if="showRecentSearches && recentSearches.length > 0 && !searchQuery" class="p-2">
        <div class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">Recent Searches</div>
        <button
          v-for="(recent, index) in recentSearches.slice(0, maxRecentSearches)"
          :key="index"
          @click="selectRecentSearch(recent)"
          class="flex items-center w-full px-2 py-1 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
        >
          <ClockIcon class="w-3 h-3 mr-2 text-gray-400" />
          {{ recent }}
        </button>
      </div>

      <!-- Search Results -->
      <div v-if="results.length > 0" class="max-h-64 overflow-y-auto">
        <button
          v-for="(result, index) in results"
          :key="getResultKey(result, index)"
          @click="selectResult(result, index)"
          :class="[
            'w-full px-3 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors',
            highlightedIndex === index && 'bg-blue-50 dark:bg-blue-900/20'
          ]"
        >
          <slot name="result" :result="result" :index="index" :query="searchQuery">
            <div class="flex items-center space-x-2">
              <div v-if="result.icon" class="flex-shrink-0">
                <component :is="result.icon" class="w-4 h-4 text-gray-400" />
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-sm font-medium text-gray-900 dark:text-white truncate">
                  <span v-html="highlightMatch(result.title || result.name || result.label, searchQuery)"></span>
                </div>
                <div v-if="result.description" class="text-xs text-gray-500 dark:text-gray-400 truncate">
                  {{ result.description }}
                </div>
              </div>
              <div v-if="result.category" class="flex-shrink-0">
                <span class="text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-2 py-1 rounded">
                  {{ result.category }}
                </span>
              </div>
            </div>
          </slot>
        </button>
      </div>

      <!-- No Results -->
      <div v-else-if="showNoResults" class="p-4 text-center text-gray-500 dark:text-gray-400">
        <slot name="no-results" :query="searchQuery">
          <MagnifyingGlassIcon class="w-8 h-8 mx-auto mb-2 text-gray-300 dark:text-gray-600" />
          <p class="text-sm">No results found for "{{ searchQuery }}"</p>
        </slot>
      </div>

      <!-- Loading State -->
      <div v-if="searching" class="p-4 text-center">
        <div class="animate-spin rounded-full h-6 w-6 border-2 border-blue-500 border-t-transparent mx-auto mb-2"></div>
        <p class="text-sm text-gray-500 dark:text-gray-400">Searching...</p>
      </div>
    </div>

    <!-- Advanced Search Panel -->
    <div
      v-if="showAdvanced && allowAdvanced"
      :class="advancedPanelClasses"
    >
      <slot name="advanced" :filters="filters" :updateFilters="updateFilters">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Category
            </label>
            <select
              v-model="filters.category"
              class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category.value" :value="category.value">
                {{ category.label }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Date Range
            </label>
            <div class="grid grid-cols-2 gap-2">
              <input
                v-model="filters.dateFrom"
                type="date"
                class="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                v-model="filters.dateTo"
                type="date"
                class="px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import {
  MagnifyingGlassIcon,
  XMarkIcon,
  AdjustmentsHorizontalIcon,
  ChevronDownIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

const { isMobile } = useResponsive()

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Search...'
  },
  results: {
    type: Array,
    default: () => []
  },
  searching: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  clearable: {
    type: Boolean,
    default: true
  },
  showSearchButton: {
    type: Boolean,
    default: false
  },
  allowAdvanced: {
    type: Boolean,
    default: false
  },
  showRecentSearches: {
    type: Boolean,
    default: true
  },
  maxRecentSearches: {
    type: Number,
    default: 5
  },
  debounceMs: {
    type: Number,
    default: 300
  },
  minLength: {
    type: Number,
    default: 1
  },
  maxLength: {
    type: Number,
    default: 100
  },
  inputType: {
    type: String,
    default: 'text'
  },
  autocomplete: {
    type: String,
    default: 'off'
  },
  spellcheck: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  },
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'filled', 'outlined'].includes(value)
  },
  clearButtonLabel: {
    type: String,
    default: 'Clear search'
  },
  categories: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([
  'update:modelValue',
  'search',
  'select',
  'focus',
  'blur',
  'clear',
  'advanced-search'
])

// Refs
const searchContainer = ref(null)
const searchInput = ref(null)

// State
const searchQuery = ref(props.modelValue)
const showResults = ref(false)
const showAdvanced = ref(false)
const highlightedIndex = ref(-1)
const recentSearches = ref([])
const filters = ref({
  category: '',
  dateFrom: '',
  dateTo: ''
})

// Debounced search
let searchTimeout = null

// Computed
const showNoResults = computed(() => {
  return searchQuery.value.length >= props.minLength && !props.searching && props.results.length === 0
})

const containerClasses = computed(() => {
  return 'relative w-full'
})

const inputContainerClasses = computed(() => {
  return 'relative flex items-center'
})

const inputClasses = computed(() => {
  const baseClasses = 'w-full pl-10 pr-4 py-2 border rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors'
  
  const sizeClasses = {
    sm: 'text-sm py-1.5',
    md: 'text-sm py-2', 
    lg: 'text-base py-3'
  }

  const variantClasses = {
    default: 'border-gray-300 dark:border-gray-600',
    filled: 'border-transparent bg-gray-100 dark:bg-gray-800',
    outlined: 'border-2 border-gray-300 dark:border-gray-600'
  }

  const rightPadding = props.clearable && searchQuery.value ? 'pr-20' : props.showSearchButton ? 'pr-12' : 'pr-4'

  return [
    baseClasses,
    sizeClasses[props.size],
    variantClasses[props.variant],
    rightPadding,
    props.disabled && 'opacity-50 cursor-not-allowed'
  ]
})

const searchButtonClasses = computed(() => {
  return [
    'absolute right-2 top-1/2 transform -translate-y-1/2 px-3 py-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-md transition-colors text-sm font-medium',
    props.disabled && 'cursor-not-allowed'
  ]
})

const advancedToggleClasses = computed(() => {
  return [
    'flex items-center px-3 py-1 mt-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors',
    showAdvanced.value && 'text-blue-600 dark:text-blue-400'
  ]
})

const dropdownClasses = computed(() => {
  return 'absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-50'
})

const advancedPanelClasses = computed(() => {
  return 'mt-2 p-4 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg'
})

// Methods
const handleInput = () => {
  emit('update:modelValue', searchQuery.value)
  
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  if (searchQuery.value.length >= props.minLength) {
    showResults.value = true
    searchTimeout = setTimeout(() => {
      performSearch()
    }, props.debounceMs)
  } else {
    showResults.value = false
  }
}

const handleFocus = () => {
  showResults.value = true
  emit('focus')
}

const handleBlur = () => {
  // Delay hiding results to allow clicking on them
  setTimeout(() => {
    showResults.value = false
    highlightedIndex.value = -1
  }, 200)
  emit('blur')
}

const handleKeydown = (event) => {
  if (!showResults.value) return
  
  const resultsCount = props.results.length
  
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      highlightedIndex.value = Math.min(highlightedIndex.value + 1, resultsCount - 1)
      break
    case 'ArrowUp':
      event.preventDefault()
      highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1)
      break
    case 'Enter':
      event.preventDefault()
      if (highlightedIndex.value >= 0 && highlightedIndex.value < resultsCount) {
        selectResult(props.results[highlightedIndex.value], highlightedIndex.value)
      } else {
        performSearch()
      }
      break
    case 'Escape':
      showResults.value = false
      highlightedIndex.value = -1
      searchInput.value.blur()
      break
  }
}

const handleKeyup = (event) => {
  if (event.key === 'Enter' && !showResults.value) {
    performSearch()
  }
}

const performSearch = () => {
  if (!searchQuery.value.trim() || searchQuery.value.length < props.minLength) return
  
  // Add to recent searches
  if (props.showRecentSearches && !recentSearches.value.includes(searchQuery.value)) {
    recentSearches.value.unshift(searchQuery.value)
    recentSearches.value = recentSearches.value.slice(0, props.maxRecentSearches)
    saveRecentSearches()
  }
  
  const searchData = {
    query: searchQuery.value,
    filters: { ...filters.value }
  }
  
  emit('search', searchData)
  
  if (showAdvanced.value) {
    emit('advanced-search', searchData)
  }
}

const selectResult = (result, index) => {
  emit('select', { result, index })
  showResults.value = false
  highlightedIndex.value = -1
}

const selectRecentSearch = (query) => {
  searchQuery.value = query
  emit('update:modelValue', query)
  performSearch()
}

const clearSearch = () => {
  searchQuery.value = ''
  emit('update:modelValue', '')
  emit('clear')
  showResults.value = false
  nextTick(() => {
    searchInput.value.focus()
  })
}

const updateFilters = (newFilters) => {
  filters.value = { ...filters.value, ...newFilters }
}

const getResultKey = (result, index) => {
  return result.id || result.key || index
}

const highlightMatch = (text, query) => {
  if (!query || !text) return text
  
  const regex = new RegExp(`(${query})`, 'gi')
  return text.replace(regex, '<mark class="bg-yellow-200 dark:bg-yellow-800">$1</mark>')
}

const saveRecentSearches = () => {
  try {
    localStorage.setItem('searchbox_recent_searches', JSON.stringify(recentSearches.value))
  } catch (error) {
    console.warn('Could not save recent searches:', error)
  }
}

const loadRecentSearches = () => {
  try {
    const saved = localStorage.getItem('searchbox_recent_searches')
    if (saved) {
      recentSearches.value = JSON.parse(saved)
    }
  } catch (error) {
    console.warn('Could not load recent searches:', error)
  }
}

// Handle clicks outside
const handleClickOutside = (event) => {
  if (searchContainer.value && !searchContainer.value.contains(event.target)) {
    showResults.value = false
    showAdvanced.value = false
  }
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  searchQuery.value = newValue
})

watch(() => props.results, () => {
  highlightedIndex.value = -1
})

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  if (props.showRecentSearches) {
    loadRecentSearches()
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
})
</script>

<style scoped>
/* Custom scrollbar for results */
.max-h-64::-webkit-scrollbar {
  width: 6px;
}

.max-h-64::-webkit-scrollbar-track {
  background: transparent;
}

.max-h-64::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.4);
  border-radius: 3px;
}

.max-h-64::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.6);
}

/* Highlight mark styles */
:deep(mark) {
  @apply bg-yellow-200 dark:bg-yellow-800 text-inherit;
}
</style>