<template>
  <div :class="containerClasses" ref="selectContainer">
    <!-- Label -->
    <label 
      v-if="label"
      :for="inputId" 
      :class="labelClasses"
    >
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>

    <!-- Select Button/Trigger -->
    <button
      :id="inputId"
      ref="selectButton"
      type="button"
      :disabled="disabled"
      :aria-expanded="isOpen"
      :aria-haspopup="true"
      :aria-label="ariaLabel"
      :class="selectButtonClasses"
      @click="toggle"
      @keydown="handleButtonKeydown"
    >
      <!-- Selected Value Display -->
      <div class="flex items-center flex-1 min-w-0">
        <!-- Multiple Selection -->
        <div v-if="multiple && selectedItems.length > 0" class="flex flex-wrap gap-1">
          <span
            v-for="(item, index) in selectedItems.slice(0, maxTags)"
            :key="getItemKey(item)"
            class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
          >
            {{ getItemLabel(item) }}
            <button
              v-if="!disabled && clearable"
              @click.stop="removeItem(item)"
              class="ml-1 hover:text-blue-600 dark:hover:text-blue-400"
            >
              <XMarkIcon class="w-3 h-3" />
            </button>
          </span>
          <span
            v-if="selectedItems.length > maxTags"
            class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400"
          >
            +{{ selectedItems.length - maxTags }} more
          </span>
        </div>

        <!-- Single Selection -->
        <div v-else-if="!multiple && selectedItems.length > 0" class="flex items-center">
          <span v-if="selectedItems[0].icon" class="mr-2">
            <component :is="selectedItems[0].icon" class="w-4 h-4" />
          </span>
          <span class="truncate">{{ getItemLabel(selectedItems[0]) }}</span>
        </div>

        <!-- Placeholder -->
        <span v-else :class="placeholderClasses">
          {{ placeholder }}
        </span>
      </div>

      <!-- Icons -->
      <div class="flex items-center space-x-1">
        <!-- Clear Button -->
        <button
          v-if="clearable && selectedItems.length > 0 && !disabled"
          @click.stop="clear"
          class="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full transition-colors"
          :aria-label="clearLabel"
        >
          <XMarkIcon class="w-4 h-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
        </button>

        <!-- Dropdown Arrow -->
        <ChevronUpDownIcon 
          :class="['w-5 h-5 text-gray-400 transition-transform', isOpen && 'rotate-180']" 
        />
      </div>
    </button>

    <!-- Error Message -->
    <div v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">
      {{ error }}
    </div>

    <!-- Help Text -->
    <div v-if="helpText && !error" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
      {{ helpText }}
    </div>

    <!-- Options Dropdown -->
    <div
      v-if="isOpen"
      ref="dropdown"
      :class="dropdownClasses"
      role="listbox"
      :aria-multiselectable="multiple"
    >
      <!-- Search Input (when searchable) -->
      <div v-if="searchable" class="p-2 border-b border-gray-200 dark:border-gray-700">
        <div class="relative">
          <MagnifyingGlassIcon class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            :placeholder="searchPlaceholder"
            class="w-full pl-10 pr-4 py-2 text-sm bg-gray-50 dark:bg-gray-700 border-0 rounded-lg focus:ring-2 focus:ring-blue-500"
            @keydown="handleSearchKeydown"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="p-4 text-center">
        <div class="animate-spin rounded-full h-6 w-6 border-2 border-blue-500 border-t-transparent mx-auto mb-2"></div>
        <p class="text-sm text-gray-500 dark:text-gray-400">Loading options...</p>
      </div>

      <!-- Options List -->
      <div v-else class="max-h-64 overflow-y-auto">
        <!-- Create New Option (when allowCreate is true and searchQuery exists) -->
        <div
          v-if="allowCreate && searchQuery && !filteredOptions.some(opt => getItemLabel(opt).toLowerCase() === searchQuery.toLowerCase())"
          :class="getOptionClasses(-1)"
          @click="createOption"
          role="option"
        >
          <div class="flex items-center">
            <PlusIcon class="w-4 h-4 text-green-500 mr-2" />
            <span>Create "{{ searchQuery }}"</span>
          </div>
        </div>

        <!-- Option Groups -->
        <template v-if="hasGroups">
          <div
            v-for="(group, groupIndex) in groupedOptions"
            :key="group.label"
            class="py-1"
          >
            <div class="px-4 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              {{ group.label }}
            </div>
            <div
              v-for="(option, optionIndex) in group.options"
              :key="getItemKey(option)"
              :class="getOptionClasses(getGlobalOptionIndex(groupIndex, optionIndex))"
              @click="selectOption(option)"
              @mouseenter="highlightedIndex = getGlobalOptionIndex(groupIndex, optionIndex)"
              role="option"
              :aria-selected="isSelected(option)"
            >
              <slot name="option" :option="option" :selected="isSelected(option)" :highlighted="highlightedIndex === getGlobalOptionIndex(groupIndex, optionIndex)">
                <div class="flex items-center justify-between w-full">
                  <div class="flex items-center">
                    <!-- Checkbox for multiple selection -->
                    <div v-if="multiple" class="mr-3">
                      <div :class="checkboxClasses(option)">
                        <CheckIcon v-if="isSelected(option)" class="w-3 h-3" />
                      </div>
                    </div>

                    <!-- Option Icon -->
                    <span v-if="option.icon" class="mr-3">
                      <component :is="option.icon" class="w-4 h-4" />
                    </span>

                    <!-- Option Content -->
                    <div class="flex-1 min-w-0">
                      <div class="font-medium truncate" v-html="highlightSearch(getItemLabel(option))"></div>
                      <div v-if="option.description" class="text-sm text-gray-500 dark:text-gray-400 truncate">
                        {{ option.description }}
                      </div>
                    </div>
                  </div>

                  <!-- Selected Indicator (single select) -->
                  <CheckIcon 
                    v-if="!multiple && isSelected(option)" 
                    class="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0" 
                  />
                </div>
              </slot>
            </div>
          </div>
        </template>

        <!-- Flat Options List -->
        <template v-else>
          <div
            v-for="(option, index) in filteredOptions"
            :key="getItemKey(option)"
            :class="getOptionClasses(index)"
            @click="selectOption(option)"
            @mouseenter="highlightedIndex = index"
            role="option"
            :aria-selected="isSelected(option)"
          >
            <slot name="option" :option="option" :selected="isSelected(option)" :highlighted="highlightedIndex === index">
              <div class="flex items-center justify-between w-full">
                <div class="flex items-center">
                  <!-- Checkbox for multiple selection -->
                  <div v-if="multiple" class="mr-3">
                    <div :class="checkboxClasses(option)">
                      <CheckIcon v-if="isSelected(option)" class="w-3 h-3" />
                    </div>
                  </div>

                  <!-- Option Icon -->
                  <span v-if="option.icon" class="mr-3">
                    <component :is="option.icon" class="w-4 h-4" />
                  </span>

                  <!-- Option Content -->
                  <div class="flex-1 min-w-0">
                    <div class="font-medium truncate" v-html="highlightSearch(getItemLabel(option))"></div>
                    <div v-if="option.description" class="text-sm text-gray-500 dark:text-gray-400 truncate">
                      {{ option.description }}
                    </div>
                  </div>
                </div>

                <!-- Selected Indicator (single select) -->
                <CheckIcon 
                  v-if="!multiple && isSelected(option)" 
                  class="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0" 
                />
              </div>
            </slot>
          </div>
        </template>

        <!-- No Options Message -->
        <div v-if="filteredOptions.length === 0" class="p-4 text-center text-gray-500 dark:text-gray-400">
          <slot name="no-options" :query="searchQuery">
            <p class="text-sm">{{ searchQuery ? 'No options match your search' : 'No options available' }}</p>
          </slot>
        </div>
      </div>

      <!-- Footer Slot -->
      <div v-if="$slots.footer" class="border-t border-gray-200 dark:border-gray-700 p-2">
        <slot name="footer" :selected="selectedItems" :close="close"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import {
  ChevronUpDownIcon,
  XMarkIcon,
  CheckIcon,
  MagnifyingGlassIcon,
  PlusIcon
} from '@heroicons/vue/24/outline'

const { isMobile } = useResponsive()

// Generate unique ID
const generateId = () => `select-${Math.random().toString(36).substr(2, 9)}`

const props = defineProps({
  modelValue: {
    type: [String, Number, Array, Object],
    default: null
  },
  options: {
    type: Array,
    default: () => [],
    required: true
  },
  multiple: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: 'Select an option...'
  },
  searchPlaceholder: {
    type: String,
    default: 'Search options...'
  },
  label: {
    type: String,
    default: ''
  },
  helpText: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  clearable: {
    type: Boolean,
    default: true
  },
  searchable: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  allowCreate: {
    type: Boolean,
    default: false
  },
  maxTags: {
    type: Number,
    default: 3
  },
  valueKey: {
    type: String,
    default: 'value'
  },
  labelKey: {
    type: String,
    default: 'label'
  },
  groupKey: {
    type: String,
    default: 'group'
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
  clearLabel: {
    type: String,
    default: 'Clear selection'
  }
})

const emit = defineEmits([
  'update:modelValue',
  'change',
  'open',
  'close',
  'search',
  'create'
])

// Refs
const selectContainer = ref(null)
const selectButton = ref(null)
const dropdown = ref(null)
const searchInput = ref(null)

// State
const isOpen = ref(false)
const searchQuery = ref('')
const highlightedIndex = ref(-1)
const inputId = generateId()

// Computed
const selectedItems = computed(() => {
  if (props.modelValue === null || props.modelValue === undefined) {
    return []
  }
  
  if (props.multiple) {
    const values = Array.isArray(props.modelValue) ? props.modelValue : [props.modelValue]
    return props.options.filter(option => 
      values.some(value => getItemValue(option) === value)
    )
  } else {
    const selectedOption = props.options.find(option => 
      getItemValue(option) === props.modelValue
    )
    return selectedOption ? [selectedOption] : []
  }
})

const filteredOptions = computed(() => {
  if (!searchQuery.value) return props.options
  
  const query = searchQuery.value.toLowerCase()
  return props.options.filter(option => 
    getItemLabel(option).toLowerCase().includes(query) ||
    (option.description && option.description.toLowerCase().includes(query))
  )
})

const hasGroups = computed(() => {
  return props.options.some(option => option[props.groupKey])
})

const groupedOptions = computed(() => {
  if (!hasGroups.value) return []
  
  const groups = {}
  filteredOptions.value.forEach(option => {
    const groupName = option[props.groupKey] || 'Other'
    if (!groups[groupName]) {
      groups[groupName] = { label: groupName, options: [] }
    }
    groups[groupName].options.push(option)
  })
  
  return Object.values(groups)
})

const ariaLabel = computed(() => {
  if (props.label) return props.label
  if (props.multiple) return 'Multiple selection dropdown'
  return 'Single selection dropdown'
})

// Classes
const containerClasses = computed(() => 'relative w-full')

const labelClasses = computed(() => 
  'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1'
)

const selectButtonClasses = computed(() => {
  const baseClasses = 'relative w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg pl-3 pr-10 py-2 text-left cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors'
  
  const sizeClasses = {
    sm: 'py-1.5 text-sm',
    md: 'py-2 text-sm',
    lg: 'py-3 text-base'
  }
  
  const variantClasses = {
    default: 'border-gray-300 dark:border-gray-600',
    filled: 'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700',
    outlined: 'border-2 border-gray-300 dark:border-gray-600'
  }
  
  const stateClasses = {
    disabled: 'opacity-50 cursor-not-allowed bg-gray-50 dark:bg-gray-800',
    error: 'border-red-300 dark:border-red-600',
    open: 'ring-2 ring-blue-500 border-blue-500'
  }
  
  return [
    baseClasses,
    sizeClasses[props.size],
    variantClasses[props.variant],
    props.disabled && stateClasses.disabled,
    props.error && stateClasses.error,
    isOpen.value && !props.error && stateClasses.open
  ]
})

const placeholderClasses = computed(() => 
  'text-gray-500 dark:text-gray-400'
)

const dropdownClasses = computed(() => {
  const baseClasses = 'absolute z-50 mt-1 bg-white dark:bg-gray-800 shadow-lg max-h-80 rounded-lg py-1 text-base ring-1 ring-black ring-opacity-5 focus:outline-none border border-gray-200 dark:border-gray-700'
  
  return [
    baseClasses,
    'w-full' // Always full width for now, could be configurable
  ]
})

const checkboxClasses = (option) => [
  'w-4 h-4 border border-gray-300 dark:border-gray-600 rounded flex items-center justify-center',
  isSelected(option) 
    ? 'bg-blue-600 border-blue-600 text-white' 
    : 'bg-white dark:bg-gray-700'
]

const getOptionClasses = (index) => [
  'cursor-pointer select-none relative py-2 pl-4 pr-9 hover:bg-gray-100 dark:hover:bg-gray-700',
  highlightedIndex.value === index && 'bg-blue-50 dark:bg-blue-900/20'
]

// Methods
const getItemValue = (item) => {
  return typeof item === 'object' ? item[props.valueKey] : item
}

const getItemLabel = (item) => {
  return typeof item === 'object' ? item[props.labelKey] || item[props.valueKey] : item
}

const getItemKey = (item) => {
  return getItemValue(item)
}

const isSelected = (option) => {
  if (props.multiple) {
    return Array.isArray(props.modelValue) && 
           props.modelValue.includes(getItemValue(option))
  }
  return props.modelValue === getItemValue(option)
}

const toggle = () => {
  if (props.disabled) return
  isOpen.value ? close() : open()
}

const open = () => {
  if (props.disabled) return
  isOpen.value = true
  highlightedIndex.value = -1
  emit('open')
  
  nextTick(() => {
    if (props.searchable && searchInput.value) {
      searchInput.value.focus()
    }
  })
}

const close = () => {
  isOpen.value = false
  searchQuery.value = ''
  highlightedIndex.value = -1
  emit('close')
}

const selectOption = (option) => {
  if (props.multiple) {
    const currentValue = Array.isArray(props.modelValue) ? [...props.modelValue] : []
    const optionValue = getItemValue(option)
    
    if (currentValue.includes(optionValue)) {
      // Remove if already selected
      const newValue = currentValue.filter(v => v !== optionValue)
      emit('update:modelValue', newValue)
      emit('change', newValue)
    } else {
      // Add to selection
      const newValue = [...currentValue, optionValue]
      emit('update:modelValue', newValue)
      emit('change', newValue)
    }
  } else {
    const newValue = getItemValue(option)
    emit('update:modelValue', newValue)
    emit('change', newValue)
    close()
  }
}

const removeItem = (item) => {
  if (!props.multiple || props.disabled) return
  
  const currentValue = Array.isArray(props.modelValue) ? [...props.modelValue] : []
  const newValue = currentValue.filter(v => v !== getItemValue(item))
  emit('update:modelValue', newValue)
  emit('change', newValue)
}

const clear = () => {
  if (props.disabled) return
  
  const newValue = props.multiple ? [] : null
  emit('update:modelValue', newValue)
  emit('change', newValue)
}

const createOption = () => {
  if (!props.allowCreate || !searchQuery.value.trim()) return
  
  const newOption = {
    [props.valueKey]: searchQuery.value,
    [props.labelKey]: searchQuery.value
  }
  
  emit('create', newOption)
  searchQuery.value = ''
}

const getGlobalOptionIndex = (groupIndex, optionIndex) => {
  let globalIndex = 0
  for (let i = 0; i < groupIndex; i++) {
    globalIndex += groupedOptions.value[i].options.length
  }
  return globalIndex + optionIndex
}

const highlightSearch = (text) => {
  if (!searchQuery.value) return text
  
  const regex = new RegExp(`(${searchQuery.value})`, 'gi')
  return text.replace(regex, '<mark class="bg-yellow-200 dark:bg-yellow-800">$1</mark>')
}

// Keyboard navigation
const handleButtonKeydown = (event) => {
  switch (event.key) {
    case 'Enter':
    case ' ':
      event.preventDefault()
      toggle()
      break
    case 'ArrowDown':
      event.preventDefault()
      if (!isOpen.value) {
        open()
      } else {
        highlightedIndex.value = Math.min(highlightedIndex.value + 1, filteredOptions.value.length - 1)
      }
      break
    case 'ArrowUp':
      event.preventDefault()
      if (isOpen.value) {
        highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1)
      }
      break
    case 'Escape':
      close()
      break
  }
}

const handleSearchKeydown = (event) => {
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      highlightedIndex.value = Math.min(highlightedIndex.value + 1, filteredOptions.value.length - 1)
      break
    case 'ArrowUp':
      event.preventDefault()
      highlightedIndex.value = Math.max(highlightedIndex.value - 1, -1)
      break
    case 'Enter':
      event.preventDefault()
      if (highlightedIndex.value >= 0) {
        selectOption(filteredOptions.value[highlightedIndex.value])
      }
      break
    case 'Escape':
      close()
      selectButton.value?.focus()
      break
  }
}

// Click outside handler
const handleClickOutside = (event) => {
  if (selectContainer.value && !selectContainer.value.contains(event.target)) {
    close()
  }
}

// Watch for search changes
watch(searchQuery, (newQuery) => {
  emit('search', newQuery)
  highlightedIndex.value = -1
})

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Custom scrollbar for dropdown */
.max-h-80::-webkit-scrollbar {
  width: 6px;
}

.max-h-80::-webkit-scrollbar-track {
  background: transparent;
}

.max-h-80::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.4);
  border-radius: 3px;
}

.max-h-80::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.6);
}

/* Highlight mark styles */
:deep(mark) {
  @apply bg-yellow-200 dark:bg-yellow-800 text-inherit;
}
</style>