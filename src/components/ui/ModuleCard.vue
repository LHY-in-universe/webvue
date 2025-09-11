<template>
  <div 
    :class="[
      'bg-white/80 dark:bg-slate-800/50 backdrop-blur-sm rounded-xl border border-gray-200 dark:border-slate-700/50',
      'shadow-lg hover:shadow-xl transition-all duration-300 p-8 cursor-pointer hover:scale-[1.02] group',
      variantClasses
    ]"
    @click="handleClick"
  >
    <!-- Icon -->
    <div class="flex justify-center mb-6">
      <div 
        :class="[
          'w-16 h-16 rounded-2xl flex items-center justify-center transition-colors',
          'group-hover:scale-110 group-hover:bg-slate-200 dark:group-hover:bg-slate-600/50',
          iconClasses
        ]"
      >
        <slot name="icon">
          <component 
            :is="icon" 
            class="w-8 h-8 text-slate-600 dark:text-slate-300"
          />
        </slot>
      </div>
    </div>
    
    <!-- Content -->
    <div class="text-center">
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-3">
        {{ title }}
      </h3>
      <p class="text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
        {{ description }}
      </p>
      
      <!-- Features (optional) -->
      <div v-if="features && features.length" class="mb-6">
        <div class="bg-gray-50 dark:bg-slate-700/50 rounded-lg p-4">
          <div class="space-y-2">
            <div 
              v-for="(feature, index) in features" 
              :key="index"
              class="flex items-center justify-between text-sm"
            >
              <span class="text-gray-600 dark:text-gray-400">{{ feature.label }}:</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ feature.value }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Stats (optional) -->
      <div v-if="stats && stats.length" class="grid grid-cols-2 gap-4 mb-6">
        <div 
          v-for="(stat, index) in stats" 
          :key="index"
          class="text-center p-3 bg-gray-50 dark:bg-slate-700/50 rounded-lg"
        >
          <div class="text-lg font-bold text-gray-900 dark:text-white">{{ stat.value }}</div>
          <div class="text-xs text-gray-600 dark:text-gray-400">{{ stat.label }}</div>
        </div>
      </div>
      
      <!-- Action Button -->
      <button 
        :class="[
          'w-full py-3 px-4 rounded-lg font-medium transition-colors',
          buttonClasses
        ]"
      >
        {{ buttonText || 'Enter Module' }}
      </button>
    </div>
    
    <!-- Badge (optional) -->
    <div 
      v-if="badge" 
      class="absolute top-4 right-4 px-2 py-1 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs font-medium rounded-md"
    >
      {{ badge }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  icon: [Object, Function, String],
  buttonText: String,
  badge: String,
  features: Array, // [{ label: string, value: string }]
  stats: Array, // [{ label: string, value: string|number }]
  variant: {
    type: String,
    default: 'default',
    validator: value => ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  moduleId: String // for identification
})

const emit = defineEmits(['click'])

const variantClasses = computed(() => {
  const variants = {
    default: 'hover:border-slate-300 dark:hover:border-slate-600',
    primary: 'hover:border-blue-300 dark:hover:border-blue-700 hover:bg-blue-50/30 dark:hover:bg-blue-900/10',
    success: 'hover:border-green-300 dark:hover:border-green-700 hover:bg-green-50/30 dark:hover:bg-green-900/10',
    warning: 'hover:border-yellow-300 dark:hover:border-yellow-700 hover:bg-yellow-50/30 dark:hover:bg-yellow-900/10',
    danger: 'hover:border-red-300 dark:hover:border-red-700 hover:bg-red-50/30 dark:hover:bg-red-900/10',
    info: 'hover:border-cyan-300 dark:hover:border-cyan-700 hover:bg-cyan-50/30 dark:hover:bg-cyan-900/10'
  }
  return variants[props.variant] || variants.default
})

const iconClasses = computed(() => {
  const variants = {
    default: 'bg-slate-100 dark:bg-slate-700/50',
    primary: 'bg-blue-100 dark:bg-blue-800/50',
    success: 'bg-green-100 dark:bg-green-800/50',
    warning: 'bg-yellow-100 dark:bg-yellow-800/50',
    danger: 'bg-red-100 dark:bg-red-800/50',
    info: 'bg-cyan-100 dark:bg-cyan-800/50'
  }
  return variants[props.variant] || variants.default
})

const buttonClasses = computed(() => {
  const variants = {
    default: 'bg-slate-700 hover:bg-slate-600 dark:bg-slate-600 dark:hover:bg-slate-500 text-white',
    primary: 'bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600 text-white',
    success: 'bg-green-600 hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-600 text-white',
    warning: 'bg-yellow-600 hover:bg-yellow-700 dark:bg-yellow-700 dark:hover:bg-yellow-600 text-white',
    danger: 'bg-red-600 hover:bg-red-700 dark:bg-red-700 dark:hover:bg-red-600 text-white',
    info: 'bg-cyan-600 hover:bg-cyan-700 dark:bg-cyan-700 dark:hover:bg-cyan-600 text-white'
  }
  return variants[props.variant] || variants.default
})

const handleClick = () => {
  emit('click', {
    moduleId: props.moduleId,
    title: props.title
  })
}
</script>

<style scoped>
.group:hover .group-hover\:scale-110 {
  transform: scale(1.1);
}
</style>