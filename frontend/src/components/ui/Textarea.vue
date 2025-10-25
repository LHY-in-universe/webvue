<template>
  <textarea
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    :class="textareaClasses"
    :placeholder="placeholder"
    :disabled="disabled"
    :rows="rows"
    :required="required"
  ></textarea>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
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
  rows: {
    type: Number,
    default: 3
  },
  required: {
    type: Boolean,
    default: false
  },
  error: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'error'].includes(value)
  }
})

defineEmits(['update:modelValue'])

const textareaClasses = computed(() => {
  const base = 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 transition-colors resize-none'
  const variants = {
    default: 'border-gray-300 dark:border-gray-600 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white',
    error: 'border-red-300 dark:border-red-600 focus:ring-red-500 focus:border-red-500 bg-red-50 dark:bg-red-900/10 text-gray-900 dark:text-white'
  }

  const disabledClass = props.disabled ? 'opacity-50 cursor-not-allowed bg-gray-100 dark:bg-gray-700' : ''
  const variantClass = props.error ? variants.error : variants[props.variant]

  return `${base} ${variantClass} ${disabledClass}`
})
</script>

<style scoped>
textarea::placeholder {
  color: rgb(156 163 175);
}

textarea:disabled {
  cursor: not-allowed;
}
</style>
