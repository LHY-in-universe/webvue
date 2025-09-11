<template>
  <form 
    :class="formClasses"
    @submit="handleSubmit"
    v-bind="$attrs"
  >
    <!-- Form Header -->
    <div v-if="$slots.header || title || description" class="mb-6">
      <slot name="header">
        <div class="text-center" v-if="centered">
          <h2 v-if="title" class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            {{ title }}
          </h2>
          <p v-if="description" class="text-gray-600 dark:text-gray-400">
            {{ description }}
          </p>
        </div>
        <div v-else>
          <h2 v-if="title" class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            {{ title }}
          </h2>
          <p v-if="description" class="text-gray-600 dark:text-gray-400">
            {{ description }}
          </p>
        </div>
      </slot>
    </div>

    <!-- Form Content -->
    <div :class="contentClasses">
      <slot />
    </div>

    <!-- Form Actions -->
    <div v-if="$slots.actions || showDefaultActions" :class="actionsClasses">
      <slot name="actions">
        <div class="flex items-center justify-end space-x-3">
          <Button
            v-if="showCancel"
            type="button"
            variant="ghost"
            @click="handleCancel"
            :disabled="loading"
          >
            {{ cancelText }}
          </Button>
          <Button
            type="submit"
            :variant="submitVariant"
            :loading="loading"
            :disabled="disabled || loading"
          >
            {{ loading ? loadingText : submitText }}
          </Button>
        </div>
      </slot>
    </div>

    <!-- Form Footer -->
    <div v-if="$slots.footer" class="mt-6">
      <slot name="footer" />
    </div>
  </form>
</template>

<script setup>
import { computed } from 'vue'
import Button from '@/components/ui/Button.vue'

const props = defineProps({
  title: String,
  description: String,
  centered: {
    type: Boolean,
    default: false
  },
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'card', 'modal'].includes(value)
  },
  layout: {
    type: String,
    default: 'vertical',
    validator: value => ['vertical', 'horizontal', 'grid'].includes(value)
  },
  columns: {
    type: Number,
    default: 1
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  showDefaultActions: {
    type: Boolean,
    default: true
  },
  showCancel: {
    type: Boolean,
    default: false
  },
  submitText: {
    type: String,
    default: 'Submit'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  loadingText: {
    type: String,
    default: 'Submitting...'
  },
  submitVariant: {
    type: String,
    default: 'primary'
  },
  spacing: {
    type: String,
    default: 'normal',
    validator: value => ['tight', 'normal', 'loose'].includes(value)
  }
})

const emit = defineEmits(['submit', 'cancel'])

// Disable attribute inheritance for form element
defineOptions({
  inheritAttrs: false
})

const formClasses = computed(() => {
  const variants = {
    default: '',
    card: 'bg-white dark:bg-gray-800 p-6 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700',
    modal: 'bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg'
  }
  
  const spacing = {
    tight: 'space-y-4',
    normal: 'space-y-6', 
    loose: 'space-y-8'
  }
  
  return [
    variants[props.variant],
    spacing[props.spacing]
  ].join(' ').trim()
})

const contentClasses = computed(() => {
  const layouts = {
    vertical: 'space-y-4',
    horizontal: 'space-y-4 md:space-y-0 md:space-x-4 md:flex md:items-end',
    grid: `grid gap-4 ${props.columns > 1 ? `grid-cols-1 md:grid-cols-${Math.min(props.columns, 3)}` : ''}`
  }
  
  return layouts[props.layout] || layouts.vertical
})

const actionsClasses = computed(() => {
  const variants = {
    default: 'mt-6 pt-4 border-t border-gray-200 dark:border-gray-700',
    card: 'mt-6 pt-4 border-t border-gray-200 dark:border-gray-700',
    modal: 'mt-6'
  }
  
  return variants[props.variant] || variants.default
})

const handleSubmit = (event) => {
  event.preventDefault()
  if (!props.loading && !props.disabled) {
    emit('submit', event)
  }
}

const handleCancel = () => {
  emit('cancel')
}
</script>
</template>