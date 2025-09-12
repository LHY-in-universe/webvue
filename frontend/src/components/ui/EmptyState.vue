<template>
  <div :class="containerClasses">
    <!-- Icon -->
    <div 
      v-if="icon || $slots.icon"
      :class="iconContainerClasses"
    >
      <slot name="icon">
        <component 
          :is="icon" 
          :class="iconClasses"
        />
      </slot>
    </div>

    <!-- Title -->
    <h3 
      v-if="title || $slots.title"
      :class="titleClasses"
    >
      <slot name="title">{{ title }}</slot>
    </h3>

    <!-- Description -->
    <p 
      v-if="description || $slots.description"
      :class="descriptionClasses"
    >
      <slot name="description">{{ description }}</slot>
    </p>

    <!-- Action Buttons -->
    <div 
      v-if="$slots.actions || actions?.length || primaryAction"
      class="mt-6"
    >
      <slot name="actions">
        <!-- Primary Action -->
        <Button
          v-if="primaryAction"
          :variant="primaryAction.variant || 'primary'"
          :size="primaryAction.size || 'md'"
          :leftIcon="primaryAction.icon"
          @click="primaryAction.handler"
        >
          {{ primaryAction.label }}
        </Button>

        <!-- Additional Actions -->
        <div v-if="actions?.length" class="mt-3 flex flex-wrap gap-2 justify-center">
          <Button
            v-for="(action, index) in actions"
            :key="index"
            :variant="action.variant || 'secondary'"
            :size="action.size || 'sm'"
            :leftIcon="action.icon"
            @click="action.handler"
          >
            {{ action.label }}
          </Button>
        </div>
      </slot>
    </div>

    <!-- Custom Content -->
    <div v-if="$slots.default" class="mt-6">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Button from './Button.vue'

const props = defineProps({
  title: String,
  description: String,
  icon: [Object, Function, String],
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'info', 'warning', 'error'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  },
  illustration: String, // for custom illustrations
  primaryAction: {
    type: Object,
    default: null
    // { label: string, handler: function, variant?: string, icon?: Component }
  },
  actions: {
    type: Array,
    default: () => []
    // [{ label: string, handler: function, variant?: string, icon?: Component }]
  },
  padding: {
    type: String,
    default: 'normal',
    validator: value => ['none', 'sm', 'normal', 'lg', 'xl'].includes(value)
  }
})

const containerClasses = computed(() => {
  const base = 'text-center flex flex-col items-center justify-center'
  
  const paddings = {
    none: '',
    sm: 'py-4 px-4',
    normal: 'py-8 px-6',
    lg: 'py-12 px-8',
    xl: 'py-16 px-10'
  }
  
  return `${base} ${paddings[props.padding]}`
})

const iconContainerClasses = computed(() => {
  const sizes = {
    sm: 'w-12 h-12',
    md: 'w-16 h-16',
    lg: 'w-20 h-20'
  }
  
  const variants = {
    default: 'bg-gray-100 dark:bg-gray-700',
    info: 'bg-blue-100 dark:bg-blue-900/20',
    warning: 'bg-yellow-100 dark:bg-yellow-900/20',
    error: 'bg-red-100 dark:bg-red-900/20'
  }
  
  return `${sizes[props.size]} ${variants[props.variant]} rounded-full flex items-center justify-center mx-auto mb-4`
})

const iconClasses = computed(() => {
  const sizes = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8', 
    lg: 'w-10 h-10'
  }
  
  const variants = {
    default: 'text-gray-400 dark:text-gray-500',
    info: 'text-blue-600 dark:text-blue-400',
    warning: 'text-yellow-600 dark:text-yellow-400',
    error: 'text-red-600 dark:text-red-400'
  }
  
  return `${sizes[props.size]} ${variants[props.variant]}`
})

const titleClasses = computed(() => {
  const sizes = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl'
  }
  
  return `${sizes[props.size]} font-semibold text-gray-900 dark:text-white mb-2`
})

const descriptionClasses = computed(() => {
  const sizes = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg'
  }
  
  return `${sizes[props.size]} text-gray-600 dark:text-gray-400 max-w-md mx-auto leading-relaxed`
})
</script>