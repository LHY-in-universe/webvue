<template>
  <div :class="fieldContainerClasses">
    <!-- Label -->
    <label 
      v-if="label || $slots.label" 
      :for="fieldId"
      :class="labelClasses"
    >
      <slot name="label">
        {{ label }}
        <span v-if="required" class="text-red-500 ml-1">*</span>
      </slot>
    </label>
    
    <!-- Help Text (before input) -->
    <p v-if="helpText && helpPosition === 'top'" :class="helpTextClasses">
      {{ helpText }}
    </p>

    <!-- Input Container -->
    <div class="relative">
      <!-- Left Icon -->
      <div v-if="leftIcon" :class="leftIconClasses">
        <component :is="leftIcon" class="h-5 w-5" />
      </div>

      <!-- Main Input Field -->
      <input
        v-if="type !== 'textarea' && type !== 'select'"
        :id="fieldId"
        v-model="inputValue"
        :type="type"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :class="inputClasses"
        v-bind="$attrs"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      />

      <!-- Textarea -->
      <textarea
        v-else-if="type === 'textarea'"
        :id="fieldId"
        v-model="inputValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :rows="rows"
        :class="inputClasses"
        v-bind="$attrs"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      ></textarea>

      <!-- Select -->
      <select
        v-else-if="type === 'select'"
        :id="fieldId"
        v-model="inputValue"
        :disabled="disabled"
        :required="required"
        :class="inputClasses"
        v-bind="$attrs"
        @change="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option 
          v-for="option in options" 
          :key="option.value || option" 
          :value="option.value || option"
        >
          {{ option.label || option }}
        </option>
      </select>

      <!-- Right Icon / Loading -->
      <div v-if="rightIcon || loading" :class="rightIconClasses">
        <LoadingSpinner v-if="loading" size="sm" />
        <component v-else-if="rightIcon" :is="rightIcon" class="h-5 w-5" />
      </div>
    </div>

    <!-- Help Text (after input) -->
    <p v-if="helpText && helpPosition === 'bottom'" :class="helpTextClasses">
      {{ helpText }}
    </p>

    <!-- Error Message -->
    <p v-if="errorMessage" :class="errorClasses">
      {{ errorMessage }}
    </p>

    <!-- Success Message -->
    <p v-if="successMessage" :class="successClasses">
      {{ successMessage }}
    </p>
  </div>
</template>

<script setup>
import { computed, ref, useAttrs } from 'vue'
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue'

const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean],
    default: ''
  },
  type: {
    type: String,
    default: 'text',
    validator: value => [
      'text', 'email', 'password', 'number', 'tel', 'url', 'search',
      'textarea', 'select', 'date', 'time', 'datetime-local'
    ].includes(value)
  },
  label: String,
  placeholder: String,
  helpText: String,
  helpPosition: {
    type: String,
    default: 'bottom',
    validator: value => ['top', 'bottom'].includes(value)
  },
  errorMessage: String,
  successMessage: String,
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'outlined', 'filled'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  },
  leftIcon: [Object, Function, String],
  rightIcon: [Object, Function, String],
  options: Array, // for select type: [{ label, value }] or ['option1', 'option2']
  rows: {
    type: Number,
    default: 3
  }
})

const emit = defineEmits(['update:modelValue', 'input', 'focus', 'blur'])

// Disable attribute inheritance to prevent duplicate attributes
defineOptions({
  inheritAttrs: false
})

const attrs = useAttrs()
const fieldId = computed(() => attrs.id || `field-${Math.random().toString(36).substr(2, 9)}`)
const isFocused = ref(false)

const inputValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const fieldContainerClasses = computed(() => {
  return 'space-y-2'
})

const labelClasses = computed(() => {
  const base = 'block text-sm font-medium'
  const colors = props.errorMessage 
    ? 'text-red-700 dark:text-red-400'
    : 'text-gray-700 dark:text-gray-300'
  return `${base} ${colors}`
})

const inputClasses = computed(() => {
  const base = 'block w-full rounded-md border-0 shadow-sm ring-1 ring-inset focus:ring-2 focus:ring-inset transition-colors'
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-3 py-2 text-sm', 
    lg: 'px-4 py-3 text-base'
  }
  
  const variants = {
    default: 'bg-white dark:bg-gray-900',
    outlined: 'bg-transparent',
    filled: 'bg-gray-50 dark:bg-gray-800'
  }
  
  // State-based styling
  let stateClasses = ''
  if (props.errorMessage) {
    stateClasses = 'ring-red-300 dark:ring-red-600 focus:ring-red-500 text-red-900 dark:text-red-100 placeholder:text-red-400'
  } else if (props.successMessage) {
    stateClasses = 'ring-green-300 dark:ring-green-600 focus:ring-green-500'
  } else if (props.disabled) {
    stateClasses = 'ring-gray-200 dark:ring-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-500 dark:text-gray-400'
  } else {
    stateClasses = 'ring-gray-300 dark:ring-gray-600 focus:ring-blue-500 dark:focus:ring-blue-400 text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500'
  }
  
  // Icon padding
  const leftPadding = props.leftIcon ? 'pl-10' : ''
  const rightPadding = props.rightIcon || props.loading ? 'pr-10' : ''
  
  return [
    base,
    sizes[props.size],
    variants[props.variant],
    stateClasses,
    leftPadding,
    rightPadding
  ].join(' ')
})

const leftIconClasses = computed(() => {
  return 'absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-gray-400 dark:text-gray-500'
})

const rightIconClasses = computed(() => {
  return 'absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-gray-400 dark:text-gray-500'
})

const helpTextClasses = computed(() => {
  return 'text-sm text-gray-600 dark:text-gray-400'
})

const errorClasses = computed(() => {
  return 'text-sm text-red-600 dark:text-red-400'
})

const successClasses = computed(() => {
  return 'text-sm text-green-600 dark:text-green-400'
})

const handleInput = (event) => {
  emit('input', event)
}

const handleFocus = (event) => {
  isFocused.value = true
  emit('focus', event)
}

const handleBlur = (event) => {
  isFocused.value = false
  emit('blur', event)
}
</script>
</template>