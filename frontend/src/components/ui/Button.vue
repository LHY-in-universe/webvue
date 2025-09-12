<template>
  <component
    :is="tag"
    :type="type"
    :href="href"
    :to="to"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
  >
    <!-- Loading Spinner -->
    <div v-if="loading" :class="['animate-spin', iconSize]">
      <svg fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    
    <!-- Left Icon -->
    <component 
      v-else-if="leftIcon" 
      :is="leftIcon" 
      :class="[iconSize, { 'mr-2': $slots.default }]"
    />
    
    <!-- Button Text/Content -->
    <span v-if="$slots.default && !iconOnly">
      <slot />
    </span>
    
    <!-- Right Icon -->
    <component 
      v-if="rightIcon && !loading" 
      :is="rightIcon" 
      :class="[iconSize, { 'ml-2': $slots.default && !iconOnly }]"
    />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: value => ['primary', 'secondary', 'success', 'warning', 'danger', 'info', 'ghost', 'outline'].includes(value)
  },
  size: {
    type: String, 
    default: 'md',
    validator: value => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  type: {
    type: String,
    default: 'button'
  },
  tag: {
    type: String,
    default: 'button'
  },
  href: String,
  to: [String, Object],
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  block: {
    type: Boolean,
    default: false
  },
  iconOnly: {
    type: Boolean,
    default: false
  },
  leftIcon: [Object, Function, String],
  rightIcon: [Object, Function, String],
  rounded: {
    type: String,
    default: 'md',
    validator: value => ['none', 'sm', 'md', 'lg', 'full'].includes(value)
  }
})

const emit = defineEmits(['click'])

const buttonClasses = computed(() => {
  // Base classes using our CSS system
  let classes = ['btn-base']
  
  // Variant classes
  const variantClass = `btn-${props.variant}`
  classes.push(variantClass)
  
  // Size classes
  const sizes = {
    xs: 'px-2 py-1 text-xs',
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
    xl: 'px-8 py-4 text-xl'
  }
  
  // Icon-only size adjustments
  if (props.iconOnly) {
    const iconOnlySizes = {
      xs: 'p-1',
      sm: 'p-1.5',
      md: 'p-2',
      lg: 'p-3',
      xl: 'p-4'
    }
    classes.push(iconOnlySizes[props.size])
  } else {
    classes.push(sizes[props.size])
  }
  
  // Rounded classes
  const roundedClasses = {
    none: 'rounded-none',
    sm: 'rounded-sm',
    md: 'rounded-lg',
    lg: 'rounded-xl',
    full: 'rounded-full'
  }
  classes.push(roundedClasses[props.rounded])
  
  // Block class
  if (props.block) {
    classes.push('w-full')
  }
  
  // Icon-only specific styling
  if (props.iconOnly) {
    classes.push('aspect-square')
  }
  
  return classes.join(' ')
})

const iconSize = computed(() => {
  const sizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4', 
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-7 h-7'
  }
  return sizes[props.size]
})

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>