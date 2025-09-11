<template>
  <div :class="cardClasses" v-bind="$attrs">
    <div v-if="$slots.header" class="card-header border-b border-gray-200 dark:border-gray-700 px-6 py-4">
      <slot name="header" />
    </div>
    
    <div class="card-body" :class="bodyPadding">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="card-footer border-t border-gray-200 dark:border-gray-700 px-6 py-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'outlined', 'elevated'].includes(value)
  },
  padding: {
    type: String,
    default: 'md',
    validator: value => ['none', 'sm', 'md', 'lg'].includes(value)
  },
  hoverable: {
    type: Boolean,
    default: false
  }
})

const cardClasses = computed(() => {
  const base = 'bg-white dark:bg-gray-800 rounded-lg overflow-hidden'
  
  const variants = {
    default: 'border border-gray-200 dark:border-gray-700',
    outlined: 'border-2 border-gray-200 dark:border-gray-700', 
    elevated: 'shadow-lg border border-gray-200 dark:border-gray-700'
  }
  
  const classes = [base, variants[props.variant]]
  
  if (props.hoverable) {
    classes.push('transition-shadow duration-400 hover:shadow-md cursor-pointer')
  }
  
  return classes.join(' ')
})

const bodyPadding = computed(() => {
  const paddings = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  }
  
  return paddings[props.padding]
})
</script>