<template>
  <div :class="containerClasses" ref="datePickerRef">
    <!-- Label -->
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>

    <!-- Input Field -->
    <div class="relative">
      <input
        :id="inputId"
        ref="inputRef"
        type="text"
        :value="displayValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly || !manualInput"
        :class="inputClasses"
        @click="toggleCalendar"
        @focus="handleFocus"
        @blur="handleBlur"
        @keydown="handleKeydown"
        @input="handleManualInput"
      />
      
      <!-- Calendar Icon -->
      <button
        type="button"
        @click="toggleCalendar"
        :disabled="disabled"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
        :aria-label="showCalendar ? 'Close calendar' : 'Open calendar'"
      >
        <CalendarDaysIcon class="h-5 w-5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300" />
      </button>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">
      {{ error }}
    </div>

    <!-- Help Text -->
    <div v-if="helpText && !error" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
      {{ helpText }}
    </div>

    <!-- Calendar Dropdown -->
    <div
      v-if="showCalendar"
      :class="calendarClasses"
    >
      <!-- Calendar Header -->
      <div class="flex items-center justify-between px-4 py-3 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <!-- Previous Year -->
        <button
          @click="changeYear(-1)"
          class="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors"
          :aria-label="'Previous year'"
        >
          <ChevronDoubleLeftIcon class="w-4 h-4 text-gray-600 dark:text-gray-400" />
        </button>
        
        <!-- Previous Month -->
        <button
          @click="changeMonth(-1)"
          class="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors"
          :aria-label="'Previous month'"
        >
          <ChevronLeftIcon class="w-4 h-4 text-gray-600 dark:text-gray-400" />
        </button>

        <!-- Month/Year Display -->
        <div class="flex items-center space-x-2">
          <button
            @click="showMonthPicker = !showMonthPicker"
            class="font-semibold text-gray-900 dark:text-gray-100 hover:bg-gray-200 dark:hover:bg-gray-700 px-2 py-1 rounded-lg transition-colors"
          >
            {{ monthNames[currentMonth] }}
          </button>
          <button
            @click="showYearPicker = !showYearPicker"
            class="font-semibold text-gray-900 dark:text-gray-100 hover:bg-gray-200 dark:hover:bg-gray-700 px-2 py-1 rounded-lg transition-colors"
          >
            {{ currentYear }}
          </button>
        </div>

        <!-- Next Month -->
        <button
          @click="changeMonth(1)"
          class="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors"
          :aria-label="'Next month'"
        >
          <ChevronRightIcon class="w-4 h-4 text-gray-600 dark:text-gray-400" />
        </button>
        
        <!-- Next Year -->
        <button
          @click="changeYear(1)"
          class="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors"
          :aria-label="'Next year'"
        >
          <ChevronDoubleRightIcon class="w-4 h-4 text-gray-600 dark:text-gray-400" />
        </button>
      </div>

      <!-- Month Picker -->
      <div v-if="showMonthPicker" class="p-4 border-b border-gray-200 dark:border-gray-700">
        <div class="grid grid-cols-3 gap-2">
          <button
            v-for="(month, index) in monthNames"
            :key="month"
            @click="selectMonth(index)"
            :class="[
              'px-3 py-2 text-sm rounded-lg transition-colors',
              currentMonth === index
                ? 'bg-blue-600 text-white'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
            ]"
          >
            {{ month }}
          </button>
        </div>
      </div>

      <!-- Year Picker -->
      <div v-if="showYearPicker" class="p-4 border-b border-gray-200 dark:border-gray-700 max-h-48 overflow-y-auto">
        <div class="grid grid-cols-4 gap-2">
          <button
            v-for="year in yearRange"
            :key="year"
            @click="selectYear(year)"
            :class="[
              'px-2 py-2 text-sm rounded-lg transition-colors',
              currentYear === year
                ? 'bg-blue-600 text-white'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
            ]"
          >
            {{ year }}
          </button>
        </div>
      </div>

      <!-- Time Picker (if includeTime is true) -->
      <div v-if="includeTime && !showMonthPicker && !showYearPicker" class="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center space-x-2">
          <label class="text-sm text-gray-700 dark:text-gray-300">Time:</label>
          <input
            v-model="selectedHour"
            type="number"
            min="0"
            :max="use24Hour ? 23 : 12"
            class="w-16 px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
          <span class="text-gray-500">:</span>
          <input
            v-model="selectedMinute"
            type="number"
            min="0"
            max="59"
            class="w-16 px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          />
          <select
            v-if="!use24Hour"
            v-model="selectedAmPm"
            class="px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            <option value="AM">AM</option>
            <option value="PM">PM</option>
          </select>
        </div>
      </div>

      <!-- Calendar Grid -->
      <div v-if="!showMonthPicker && !showYearPicker" class="p-4">
        <!-- Day Headers -->
        <div class="grid grid-cols-7 mb-2">
          <div
            v-for="day in dayHeaders"
            :key="day"
            class="text-center text-xs font-medium text-gray-500 dark:text-gray-400 py-2"
          >
            {{ day }}
          </div>
        </div>

        <!-- Calendar Days -->
        <div class="grid grid-cols-7 gap-1">
          <button
            v-for="day in calendarDays"
            :key="day.key"
            @click="selectDate(day)"
            :disabled="!day.selectable"
            :class="getDayClasses(day)"
            :aria-label="formatDateForAccessibility(day.date)"
          >
            {{ day.day }}
          </button>
        </div>
      </div>

      <!-- Quick Actions -->
      <div v-if="showQuickActions && !showMonthPicker && !showYearPicker" class="px-4 py-3 bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <div class="flex flex-wrap gap-2">
          <button
            @click="selectToday"
            class="px-3 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-lg hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
          >
            Today
          </button>
          <button
            @click="selectYesterday"
            class="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            Yesterday
          </button>
          <button
            @click="selectTomorrow"
            class="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            Tomorrow
          </button>
          <button
            v-if="selectedDate"
            @click="clearDate"
            class="px-3 py-1 text-xs bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-lg hover:bg-red-200 dark:hover:bg-red-800 transition-colors"
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import {
  CalendarDaysIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ChevronDoubleLeftIcon,
  ChevronDoubleRightIcon
} from '@heroicons/vue/24/outline'

const { isMobile } = useResponsive()

const props = defineProps({
  modelValue: {
    type: [String, Date],
    default: null
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select date...'
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
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  format: {
    type: String,
    default: 'YYYY-MM-DD'
  },
  includeTime: {
    type: Boolean,
    default: false
  },
  use24Hour: {
    type: Boolean,
    default: true
  },
  minDate: {
    type: [String, Date],
    default: null
  },
  maxDate: {
    type: [String, Date],
    default: null
  },
  manualInput: {
    type: Boolean,
    default: false
  },
  showQuickActions: {
    type: Boolean,
    default: true
  },
  size: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  },
  firstDayOfWeek: {
    type: Number,
    default: 0, // 0 = Sunday, 1 = Monday
    validator: value => value >= 0 && value <= 6
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'focus', 'blur', 'open', 'close'])

// Generate unique ID
const generateId = () => `datepicker-${Math.random().toString(36).substr(2, 9)}`

// Refs
const datePickerRef = ref(null)
const inputRef = ref(null)

// State
const showCalendar = ref(false)
const showMonthPicker = ref(false)
const showYearPicker = ref(false)
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())
const selectedDate = ref(null)
const selectedHour = ref(12)
const selectedMinute = ref(0)
const selectedAmPm = ref('AM')
const inputId = generateId()

// Constants
const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

const dayHeaders = computed(() => {
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  // Adjust for first day of week
  const reordered = [...days.slice(props.firstDayOfWeek), ...days.slice(0, props.firstDayOfWeek)]
  return reordered
})

// Computed
const containerClasses = computed(() => 'relative w-full')

const inputClasses = computed(() => {
  const baseClasses = 'block w-full pr-10 border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-3 py-2 text-base',
    lg: 'px-4 py-3 text-lg'
  }
  
  const classes = [baseClasses, sizeClasses[props.size]]
  
  if (props.error) {
    classes.push('border-red-300 focus:border-red-500 focus:ring-red-500')
  }
  
  if (props.disabled) {
    classes.push('bg-gray-50 text-gray-500 cursor-not-allowed dark:bg-gray-600')
  }
  
  return classes.join(' ')
})

const calendarClasses = computed(() => [
  'absolute z-50 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg',
  isMobile.value ? 'w-full' : 'w-80'
])

const displayValue = computed(() => {
  if (!selectedDate.value) return ''
  
  let dateStr = formatDate(selectedDate.value, props.format)
  
  if (props.includeTime) {
    const timeStr = props.use24Hour 
      ? `${String(selectedHour.value).padStart(2, '0')}:${String(selectedMinute.value).padStart(2, '0')}`
      : `${selectedHour.value}:${String(selectedMinute.value).padStart(2, '0')} ${selectedAmPm.value}`
    dateStr += ` ${timeStr}`
  }
  
  return dateStr
})

const yearRange = computed(() => {
  const currentYear = new Date().getFullYear()
  const startYear = currentYear - 50
  const endYear = currentYear + 50
  const years = []
  for (let year = startYear; year <= endYear; year++) {
    years.push(year)
  }
  return years
})

const calendarDays = computed(() => {
  const days = []
  const firstDay = new Date(currentYear.value, currentMonth.value, 1)
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)
  
  // Adjust first day based on firstDayOfWeek setting
  let startDay = firstDay.getDay() - props.firstDayOfWeek
  if (startDay < 0) startDay += 7
  
  // Add previous month's trailing days
  const prevMonth = new Date(currentYear.value, currentMonth.value, 0)
  for (let i = startDay - 1; i >= 0; i--) {
    const date = new Date(currentYear.value, currentMonth.value - 1, prevMonth.getDate() - i)
    days.push({
      key: `prev-${prevMonth.getDate() - i}`,
      day: prevMonth.getDate() - i,
      date: date,
      isCurrentMonth: false,
      isToday: isToday(date),
      isSelected: isSelected(date),
      selectable: isSelectableDate(date)
    })
  }
  
  // Add current month's days
  for (let day = 1; day <= lastDay.getDate(); day++) {
    const date = new Date(currentYear.value, currentMonth.value, day)
    days.push({
      key: `current-${day}`,
      day: day,
      date: date,
      isCurrentMonth: true,
      isToday: isToday(date),
      isSelected: isSelected(date),
      selectable: isSelectableDate(date)
    })
  }
  
  // Add next month's leading days
  const remainingCells = 42 - days.length // 6 rows × 7 days
  for (let day = 1; day <= remainingCells; day++) {
    const date = new Date(currentYear.value, currentMonth.value + 1, day)
    days.push({
      key: `next-${day}`,
      day: day,
      date: date,
      isCurrentMonth: false,
      isToday: isToday(date),
      isSelected: isSelected(date),
      selectable: isSelectableDate(date)
    })
  }
  
  return days
})

// Methods
const toggleCalendar = () => {
  if (props.disabled) return
  showCalendar.value = !showCalendar.value
  showMonthPicker.value = false
  showYearPicker.value = false
  emit(showCalendar.value ? 'open' : 'close')
}

const handleFocus = (event) => {
  emit('focus', event)
}

const handleBlur = (event) => {
  emit('blur', event)
}

const handleKeydown = (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault()
    toggleCalendar()
  } else if (event.key === 'Escape') {
    showCalendar.value = false
    emit('close')
  }
}

const handleManualInput = (event) => {
  if (!props.manualInput) return
  
  const value = event.target.value
  const parsedDate = parseDate(value)
  
  if (parsedDate && isSelectableDate(parsedDate)) {
    selectedDate.value = parsedDate
    currentMonth.value = parsedDate.getMonth()
    currentYear.value = parsedDate.getFullYear()
    updateModelValue()
  }
}

const selectDate = (day) => {
  if (!day.selectable) return
  
  selectedDate.value = new Date(day.date)
  
  if (props.includeTime) {
    selectedDate.value.setHours(
      props.use24Hour ? selectedHour.value : 
      selectedAmPm.value === 'PM' ? (selectedHour.value === 12 ? 12 : selectedHour.value + 12) :
      (selectedHour.value === 12 ? 0 : selectedHour.value)
    )
    selectedDate.value.setMinutes(selectedMinute.value)
  }
  
  updateModelValue()
  
  if (!props.includeTime) {
    showCalendar.value = false
    emit('close')
  }
}

const selectMonth = (month) => {
  currentMonth.value = month
  showMonthPicker.value = false
}

const selectYear = (year) => {
  currentYear.value = year
  showYearPicker.value = false
}

const changeMonth = (delta) => {
  const newDate = new Date(currentYear.value, currentMonth.value + delta, 1)
  currentMonth.value = newDate.getMonth()
  currentYear.value = newDate.getFullYear()
}

const changeYear = (delta) => {
  currentYear.value += delta
}

const selectToday = () => {
  const today = new Date()
  selectedDate.value = today
  currentMonth.value = today.getMonth()
  currentYear.value = today.getFullYear()
  updateModelValue()
  if (!props.includeTime) {
    showCalendar.value = false
    emit('close')
  }
}

const selectYesterday = () => {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  selectedDate.value = yesterday
  currentMonth.value = yesterday.getMonth()
  currentYear.value = yesterday.getFullYear()
  updateModelValue()
  if (!props.includeTime) {
    showCalendar.value = false
    emit('close')
  }
}

const selectTomorrow = () => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  selectedDate.value = tomorrow
  currentMonth.value = tomorrow.getMonth()
  currentYear.value = tomorrow.getFullYear()
  updateModelValue()
  if (!props.includeTime) {
    showCalendar.value = false
    emit('close')
  }
}

const clearDate = () => {
  selectedDate.value = null
  updateModelValue()
  showCalendar.value = false
  emit('close')
}

const updateModelValue = () => {
  const value = selectedDate.value
  emit('update:modelValue', value)
  emit('change', value)
}

// Helper functions
const isToday = (date) => {
  const today = new Date()
  return date.toDateString() === today.toDateString()
}

const isSelected = (date) => {
  if (!selectedDate.value) return false
  return date.toDateString() === selectedDate.value.toDateString()
}

const isSelectableDate = (date) => {
  if (props.minDate) {
    const minDate = new Date(props.minDate)
    if (date < minDate) return false
  }
  
  if (props.maxDate) {
    const maxDate = new Date(props.maxDate)
    if (date > maxDate) return false
  }
  
  return true
}

const getDayClasses = (day) => {
  const baseClasses = 'w-8 h-8 text-sm rounded-lg transition-colors'
  const classes = [baseClasses]
  
  if (!day.selectable) {
    classes.push('text-gray-300 dark:text-gray-600 cursor-not-allowed')
  } else if (day.isSelected) {
    classes.push('bg-blue-600 text-white')
  } else if (day.isToday) {
    classes.push('bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200')
  } else if (day.isCurrentMonth) {
    classes.push('text-gray-900 dark:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700')
  } else {
    classes.push('text-gray-400 dark:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700')
  }
  
  return classes.join(' ')
}

const formatDate = (date, format) => {
  if (!date) return ''
  
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
}

const parseDate = (dateString) => {
  // Simple date parsing - can be enhanced for more formats
  const date = new Date(dateString)
  return isNaN(date.getTime()) ? null : date
}

const formatDateForAccessibility = (date) => {
  return date.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

// Click outside handler
const handleClickOutside = (event) => {
  if (datePickerRef.value && !datePickerRef.value.contains(event.target)) {
    showCalendar.value = false
    showMonthPicker.value = false
    showYearPicker.value = false
    emit('close')
  }
}

// Initialize selectedDate from modelValue
const initializeDate = () => {
  if (props.modelValue) {
    const date = new Date(props.modelValue)
    if (!isNaN(date.getTime())) {
      selectedDate.value = date
      currentMonth.value = date.getMonth()
      currentYear.value = date.getFullYear()
      
      if (props.includeTime) {
        selectedHour.value = props.use24Hour ? date.getHours() : 
          date.getHours() === 0 ? 12 : 
          date.getHours() > 12 ? date.getHours() - 12 : date.getHours()
        selectedMinute.value = date.getMinutes()
        selectedAmPm.value = date.getHours() >= 12 ? 'PM' : 'AM'
      }
    }
  }
}

// Watch for external changes
watch(() => props.modelValue, initializeDate)

// Watch time changes
watch([selectedHour, selectedMinute, selectedAmPm], () => {
  if (selectedDate.value && props.includeTime) {
    const newDate = new Date(selectedDate.value)
    const hour = props.use24Hour ? selectedHour.value :
      selectedAmPm.value === 'PM' ? (selectedHour.value === 12 ? 12 : selectedHour.value + 12) :
      (selectedHour.value === 12 ? 0 : selectedHour.value)
    
    newDate.setHours(hour, selectedMinute.value)
    selectedDate.value = newDate
    updateModelValue()
  }
})

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  initializeDate()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Expose methods
defineExpose({
  focus: () => inputRef.value?.focus(),
  blur: () => inputRef.value?.blur(),
  open: () => { showCalendar.value = true },
  close: () => { showCalendar.value = false },
  selectToday,
  clearDate
})
</script>

<style scoped>
/* Custom scrollbar for year picker */
.max-h-48::-webkit-scrollbar {
  width: 6px;
}

.max-h-48::-webkit-scrollbar-track {
  background: transparent;
}

.max-h-48::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.4);
  border-radius: 3px;
}

.max-h-48::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.6);
}
</style>