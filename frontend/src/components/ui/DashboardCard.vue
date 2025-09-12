<template>
  <Card 
    :class="[
      'dashboard-card transition-all duration-400',
      interactive && 'cursor-pointer hover:shadow-xl hover:scale-[1.02] group',
      variant !== 'default' && variantClasses
    ]"
    :hoverable="interactive"
    :variant="cardVariant"
    @click="handleClick"
  >
    <div class="p-6">
      <!-- Header Section -->
      <div class="flex items-start justify-between mb-4">
        <div class="flex items-center space-x-3">
          <!-- Icon Container -->
          <div 
            v-if="icon || $slots.icon"
            :class="[
              'flex items-center justify-center rounded-xl transition-colors',
              iconSize === 'sm' ? 'w-10 h-10' : iconSize === 'lg' ? 'w-16 h-16' : 'w-12 h-12',
              iconClasses,
              interactive && 'group-hover:scale-110 transition-transform'
            ]"
          >
            <slot name="icon">
              <component 
                :is="icon" 
                :class="[
                  iconSize === 'sm' ? 'w-5 h-5' : iconSize === 'lg' ? 'w-8 h-8' : 'w-6 h-6',
                  iconColorClasses
                ]"
              />
            </slot>
          </div>
          
          <!-- Title & Description -->
          <div class="min-w-0 flex-1">
            <h3 
              v-if="title" 
              :class="[
                'font-semibold truncate',
                titleSize === 'sm' ? 'text-lg' : titleSize === 'lg' ? 'text-2xl' : 'text-xl',
                'text-gray-900 dark:text-white'
              ]"
            >
              {{ title }}
            </h3>
            <p 
              v-if="description || $slots.description" 
              class="text-gray-600 dark:text-gray-300 mt-1"
              :class="descriptionSize === 'sm' ? 'text-sm' : 'text-base'"
            >
              <slot name="description">{{ description }}</slot>
            </p>
          </div>
        </div>
        
        <!-- Badge -->
        <div v-if="badge" :class="badgeClasses">
          {{ badge }}
        </div>
      </div>

      <!-- Stats Section (for dashboard metrics) -->
      <div v-if="stats && stats.length" class="mb-6">
        <div :class="statsGridClasses">
          <div 
            v-for="(stat, index) in stats" 
            :key="index"
            class="text-center p-3 bg-gray-50 dark:bg-slate-700/50 rounded-lg"
          >
            <div class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ stat.value }}
            </div>
            <div class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              {{ stat.label }}
            </div>
          </div>
        </div>
      </div>

      <!-- Feature List -->
      <div v-if="features && features.length" class="mb-6">
        <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
          <div class="text-sm text-gray-700 dark:text-gray-300 space-y-2">
            <div 
              v-for="(feature, index) in features" 
              :key="index"
              class="flex items-center justify-between"
            >
              <span>{{ feature.label }}:</span>
              <span class="font-medium text-gray-600 dark:text-gray-300">{{ feature.value }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Slot -->
      <div v-if="$slots.default" class="mb-6">
        <slot />
      </div>

      <!-- Action Buttons -->
      <div v-if="actions && actions.length || $slots.actions" class="flex flex-wrap gap-3">
        <slot name="actions">
          <Button
            v-for="(action, index) in actions"
            :key="index"
            :variant="action.variant || 'primary'"
            :size="action.size || 'md'"
            :leftIcon="action.icon"
            :block="action.block"
            @click.stop="handleActionClick(action)"
          >
            {{ action.label }}
          </Button>
        </slot>
      </div>

      <!-- Single Action Button (for simple cases) -->
      <div v-if="actionLabel && !actions?.length && !$slots.actions" class="mt-6">
        <Button
          :variant="actionVariant"
          :size="actionSize"
          :leftIcon="actionIcon"
          :block="actionBlock"
          @click.stop="handleAction"
        >
          {{ actionLabel }}
        </Button>
      </div>
    </div>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import Card from './Card.vue'
import Button from './Button.vue'

const props = defineProps({
  // Basic properties
  title: String,
  description: String,
  icon: [Object, Function, String],
  badge: String,
  
  // Sizing
  iconSize: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  },
  titleSize: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  },
  descriptionSize: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md'].includes(value)
  },
  
  // Styling
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  
  // Interactivity
  interactive: {
    type: Boolean,
    default: false
  },
  
  // Data
  stats: Array, // [{ label: string, value: string|number }]
  features: Array, // [{ label: string, value: string }]
  actions: Array, // [{ label: string, variant?: string, icon?: Component, handler?: Function }]
  
  // Single action (simpler interface)
  actionLabel: String,
  actionVariant: {
    type: String,
    default: 'primary'
  },
  actionSize: {
    type: String,
    default: 'md'
  },
  actionIcon: [Object, Function, String],
  actionBlock: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['click', 'action'])

const variantClasses = computed(() => {
  const variants = {
    primary: 'border-blue-200 dark:border-blue-800 bg-blue-50/50 dark:bg-blue-900/10',
    success: 'border-green-200 dark:border-green-800 bg-green-50/50 dark:bg-green-900/10',
    warning: 'border-yellow-200 dark:border-yellow-800 bg-yellow-50/50 dark:bg-yellow-900/10',
    danger: 'border-red-200 dark:border-red-800 bg-red-50/50 dark:bg-red-900/10',
    info: 'border-cyan-200 dark:border-cyan-800 bg-cyan-50/50 dark:bg-cyan-900/10'
  }
  return variants[props.variant] || ''
})

const cardVariant = computed(() => {
  return props.variant === 'default' ? 'elevated' : 'default'
})

const iconClasses = computed(() => {
  const variants = {
    default: 'bg-slate-100 dark:bg-slate-700',
    primary: 'bg-blue-100 dark:bg-blue-800/50',
    success: 'bg-green-100 dark:bg-green-800/50',
    warning: 'bg-yellow-100 dark:bg-yellow-800/50',
    danger: 'bg-red-100 dark:bg-red-800/50',
    info: 'bg-cyan-100 dark:bg-cyan-800/50'
  }
  return variants[props.variant] || variants.default
})

const iconColorClasses = computed(() => {
  const variants = {
    default: 'text-slate-600 dark:text-slate-300',
    primary: 'text-blue-600 dark:text-blue-300',
    success: 'text-green-600 dark:text-green-300',
    warning: 'text-yellow-600 dark:text-yellow-300',
    danger: 'text-red-600 dark:text-red-300',
    info: 'text-cyan-600 dark:text-cyan-300'
  }
  return variants[props.variant] || variants.default
})

const badgeClasses = computed(() => {
  return 'px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 text-xs font-medium rounded-md'
})

const statsGridClasses = computed(() => {
  if (!props.stats) return ''
  const count = props.stats.length
  if (count <= 2) return 'grid grid-cols-2 gap-4'
  if (count <= 4) return 'grid grid-cols-2 md:grid-cols-4 gap-4'
  return 'grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4'
})

const handleClick = (event) => {
  if (props.interactive) {
    emit('click', event)
  }
}

const handleAction = () => {
  emit('action', { type: 'single' })
}

const handleActionClick = (action) => {
  if (action.handler) {
    action.handler()
  }
  emit('action', action)
}
</script>

<style scoped>
.dashboard-card {
  @apply transition-all duration-300;
}

.dashboard-card:hover {
  @apply shadow-lg;
}
</style>