<template>
  <div class="switch-toggle-wrapper">
    <div 
      class="switch-toggle" 
      :class="{ 'is-checked': modelValue }"
      @click="handleToggle"
    >
      <!-- Background Track -->
      <div class="switch-track">
        <!-- Left Icon (Light) -->
        <div class="switch-icon left-icon" :class="{ 'active': !modelValue }">
          <SunIcon class="w-4 h-4" />
        </div>
        
        <!-- Right Icon (Dark) -->
        <div class="switch-icon right-icon" :class="{ 'active': modelValue }">
          <MoonIcon class="w-4 h-4" />
        </div>
        
        <!-- Sliding Handle -->
        <div class="switch-handle" :class="{ 'handle-right': modelValue }">
          <div class="handle-inner">
            <!-- Current mode icon in handle -->
            <SunIcon v-if="!modelValue" class="w-3 h-3 text-amber-500" />
            <MoonIcon v-else class="w-3 h-3 text-slate-300" />
          </div>
        </div>
      </div>
      
      <!-- Label Text -->
      <div v-if="showLabel" class="switch-label">
        {{ modelValue ? labelDark : labelLight }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { SunIcon, MoonIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  showLabel: {
    type: Boolean,
    default: true
  },
  labelLight: {
    type: String,
    default: 'Light'
  },
  labelDark: {
    type: String,
    default: 'Dark'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const handleToggle = () => {
  if (props.disabled) return
  
  const newValue = !props.modelValue
  emit('update:modelValue', newValue)
  emit('change', newValue)
}
</script>

<style scoped>
.switch-toggle-wrapper {
  @apply inline-flex items-center select-none;
}

.switch-toggle {
  @apply flex items-center space-x-3 cursor-pointer;
}

.switch-toggle.disabled {
  @apply opacity-50 cursor-not-allowed;
}

/* Switch Track */
.switch-track {
  @apply relative w-16 h-8 bg-gray-200 dark:bg-gray-700 rounded-full;
  @apply border-2 border-gray-300 dark:border-gray-600;
  @apply transition-all duration-300 ease-in-out;
  @apply shadow-inner;
  @apply flex items-center justify-between px-1;
}

.switch-toggle.is-checked .switch-track {
  @apply bg-slate-800 border-slate-700;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Background Icons */
.switch-icon {
  @apply flex items-center justify-center w-6 h-6;
  @apply transition-all duration-300;
  @apply opacity-40 z-10;
}

.switch-icon.active {
  @apply opacity-80 scale-110;
}

.left-icon {
  @apply text-amber-500;
}

.right-icon {
  @apply text-slate-400;
}

.switch-toggle.is-checked .right-icon {
  @apply text-slate-200;
}

/* Sliding Handle */
.switch-handle {
  @apply absolute top-0.5 left-0.5 w-7 h-7 bg-white rounded-full;
  @apply shadow-lg border border-gray-200;
  @apply transition-all duration-300 ease-in-out transform;
  @apply flex items-center justify-center z-20;
}

.switch-handle.handle-right {
  @apply translate-x-8 bg-slate-100 border-slate-300;
}

.handle-inner {
  @apply flex items-center justify-center w-full h-full;
}

/* Hover Effects */
.switch-toggle:hover .switch-track {
  @apply shadow-lg;
}

.switch-toggle:hover .switch-handle {
  @apply scale-105 shadow-xl;
}

/* Focus Effects */
.switch-toggle:focus-within .switch-track {
  @apply ring-2 ring-blue-500 ring-opacity-50;
}

/* Label */
.switch-label {
  @apply text-sm font-medium text-gray-700 dark:text-gray-300;
  @apply transition-colors duration-300;
  @apply min-w-[3rem];
}

/* Glass morphism effect */
.switch-track {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.8);
}

.switch-toggle.is-checked .switch-track {
  background: rgba(30, 41, 59, 0.9);
}

/* Active state glow */
.switch-toggle.is-checked .switch-track {
  box-shadow: 
    inset 0 2px 4px rgba(0, 0, 0, 0.3),
    0 0 12px rgba(59, 130, 246, 0.4);
}

.switch-toggle:not(.is-checked) .switch-track:hover {
  box-shadow: 
    inset 0 2px 4px rgba(0, 0, 0, 0.1),
    0 0 12px rgba(251, 191, 36, 0.3);
}
</style>