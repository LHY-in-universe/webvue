<template>
  <div class="input-wrapper">
    <!-- Label -->
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <!-- Input Container -->
    <div class="relative">
      <!-- Prefix Icon -->
      <div v-if="prefixIcon || $slots.prefix" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <slot name="prefix">
          <component v-if="prefixIcon" :is="prefixIcon" class="h-5 w-5 text-gray-400" />
        </slot>
      </div>

      <!-- Input Element -->
      <input
        :id="inputId"
        ref="inputRef"
        :type="currentType"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :value="inputValue"
        :class="inputClasses"
        :autocomplete="autocomplete"
        :spellcheck="spellcheck"
        :min="min"
        :max="max"
        :step="step"
        :minlength="minlength"
        :maxlength="maxlength"
        :pattern="pattern"
        @input="handleInput"
        @change="handleChange"
        @focus="handleFocus"
        @blur="handleBlur"
        @keydown="handleKeydown"
        @paste="handlePaste"
      />
      
      <!-- Password Toggle -->
      <button
        v-if="type === 'password' && togglePassword"
        type="button"
        @click="togglePasswordVisibility"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
        :aria-label="showPassword ? 'Hide password' : 'Show password'"
      >
        <EyeIcon v-if="showPassword" class="h-5 w-5 text-gray-400 hover:text-gray-600" />
        <EyeSlashIcon v-else class="h-5 w-5 text-gray-400 hover:text-gray-600" />
      </button>

      <!-- Clear Button -->
      <button
        v-else-if="clearable && inputValue && !disabled && !readonly"
        type="button"
        @click="clear"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
        :aria-label="clearLabel"
      >
        <XMarkIcon class="h-5 w-5 text-gray-400 hover:text-gray-600" />
      </button>

      <!-- Suffix Icon -->
      <div v-else-if="suffixIcon || $slots.suffix" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <slot name="suffix">
          <component v-if="suffixIcon" :is="suffixIcon" class="h-5 w-5 text-gray-400" />
        </slot>
      </div>

      <!-- Loading Spinner -->
      <div v-else-if="loading" class="absolute inset-y-0 right-0 pr-3 flex items-center">
        <div class="animate-spin rounded-full h-4 w-4 border-2 border-blue-500 border-t-transparent"></div>
      </div>

      <!-- Error Icon (fallback) -->
      <div v-else-if="error" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <ExclamationTriangleIcon class="h-5 w-5 text-red-500" />
      </div>
    </div>
    
    <!-- Character Counter -->
    <div v-if="showCounter && maxlength" class="mt-1 text-xs text-right text-gray-500">
      {{ inputValue.length }} / {{ maxlength }}
    </div>

    <!-- Error Message -->
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">
      {{ error }}
    </p>
    
    <!-- Help Text -->
    <p v-else-if="help" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
      {{ help }}
    </p>
  </div>
</template>

<script setup>
import { computed, ref, watch, nextTick, onMounted } from 'vue'
import { useResponsive } from '@/composables/useResponsive'
import {
  EyeIcon,
  EyeSlashIcon,
  XMarkIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const { isMobile } = useResponsive()

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
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
  error: {
    type: String,
    default: ''
  },
  help: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  },
  // Enhanced props
  clearable: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  togglePassword: {
    type: Boolean,
    default: true
  },
  showCounter: {
    type: Boolean,
    default: false
  },
  clearLabel: {
    type: String,
    default: 'Clear input'
  },
  // HTML attributes
  autocomplete: String,
  spellcheck: Boolean,
  min: [String, Number],
  max: [String, Number],
  step: [String, Number],
  minlength: [String, Number],
  maxlength: [String, Number],
  pattern: String,
  // Icons
  prefixIcon: [Object, Function, String],
  suffixIcon: [Object, Function, String]
})

const emit = defineEmits(['update:modelValue', 'input', 'change', 'focus', 'blur', 'keydown', 'paste', 'clear'])

// Refs
const inputRef = ref(null)
const inputId = ref(`input-${Math.random().toString(36).substr(2, 9)}`)

// State
const inputValue = ref(props.modelValue?.toString() || '')
const showPassword = ref(false)
const isFocused = ref(false)

// Computed
const currentType = computed(() => {
  if (props.type === 'password' && showPassword.value) {
    return 'text'
  }
  return props.type
})

const inputClasses = computed(() => {
  const base = 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white'
  
  const sizes = {
    sm: 'py-1.5 text-sm',
    md: 'py-2 text-base', 
    lg: 'py-3 text-lg'
  }
  
  const classes = [base, sizes[props.size]]
  
  // Padding adjustments for icons
  const leftPadding = props.prefixIcon || props.$slots?.prefix ? 'pl-10' : 'px-3'
  const rightPadding = (
    props.suffixIcon || 
    props.$slots?.suffix || 
    (props.type === 'password' && props.togglePassword) || 
    props.clearable || 
    props.loading ||
    props.error
  ) ? 'pr-10' : 'px-3'
  
  // Apply padding - use left/right specific if needed, otherwise default px
  if (leftPadding !== 'px-3' || rightPadding !== 'px-3') {
    if (leftPadding !== 'px-3') classes.push(leftPadding)
    if (rightPadding !== 'px-3') classes.push(rightPadding)
    // Add base horizontal padding if not using icons
    if (leftPadding === 'px-3' && rightPadding === 'px-3') {
      classes.push('px-3')
    }
  } else {
    classes.push('px-3')
  }
  
  if (props.error) {
    classes.push('border-red-300 focus:border-red-500 focus:ring-red-500')
  }
  
  if (props.disabled) {
    classes.push('bg-gray-50 text-gray-500 cursor-not-allowed dark:bg-gray-600')
  }
  
  if (props.readonly) {
    classes.push('bg-gray-50 dark:bg-gray-800')
  }
  
  return classes.join(' ')
})

// Methods
const handleInput = (event) => {
  inputValue.value = event.target.value
  emit('update:modelValue', getValue())
  emit('input', event)
}

const handleChange = (event) => {
  emit('change', event)
}

const handleFocus = (event) => {
  isFocused.value = true
  emit('focus', event)
}

const handleBlur = (event) => {
  isFocused.value = false
  emit('blur', event)
}

const handleKeydown = (event) => {
  emit('keydown', event)
}

const handlePaste = (event) => {
  emit('paste', event)
}

const clear = () => {
  inputValue.value = ''
  emit('update:modelValue', getValue())
  emit('clear')
  nextTick(() => {
    inputRef.value?.focus()
  })
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const getValue = () => {
  if (props.type === 'number') {
    const num = parseFloat(inputValue.value)
    return isNaN(num) ? null : num
  }
  return inputValue.value
}

const focus = () => {
  inputRef.value?.focus()
}

const blur = () => {
  inputRef.value?.blur()
}

const select = () => {
  inputRef.value?.select()
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  inputValue.value = newValue?.toString() || ''
})

// Expose methods
defineExpose({
  focus,
  blur,
  select,
  clear,
  inputRef
})

onMounted(() => {
  inputValue.value = props.modelValue?.toString() || ''
})
</script>