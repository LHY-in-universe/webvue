<template>
  <div class="performance-settings space-y-6">
    <div class="space-y-4">
      <!-- Monitoring Toggle -->
      <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
        <div>
          <h3 class="text-sm font-medium text-gray-900 dark:text-white">
            Performance Monitoring
          </h3>
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
            Enable real-time performance tracking
          </p>
        </div>
        <SwitchToggle 
          v-model="settings.enabled"
          @change="handleSettingChange('enabled', $event)"
        />
      </div>

      <!-- Sampling Rate -->
      <div class="space-y-2">
        <label class="text-sm font-medium text-gray-900 dark:text-white">
          Sampling Interval (ms)
        </label>
        <div class="flex items-center space-x-4">
          <input
            v-model.number="settings.samplingInterval"
            type="range"
            min="100"
            max="5000"
            step="100"
            class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            @input="handleSettingChange('samplingInterval', $event.target.value)"
          />
          <span class="text-sm text-gray-600 dark:text-gray-400 min-w-0 w-16 text-right">
            {{ settings.samplingInterval }}ms
          </span>
        </div>
        <p class="text-xs text-gray-500 dark:text-gray-400">
          Lower values provide more detailed monitoring but may impact performance
        </p>
      </div>

      <!-- Memory Tracking -->
      <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
        <div>
          <h3 class="text-sm font-medium text-gray-900 dark:text-white">
            Memory Tracking
          </h3>
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
            Track memory usage patterns
          </p>
        </div>
        <SwitchToggle 
          v-model="settings.trackMemory"
          @change="handleSettingChange('trackMemory', $event)"
        />
      </div>

      <!-- Component Tracking -->
      <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
        <div>
          <h3 class="text-sm font-medium text-gray-900 dark:text-white">
            Component Tracking
          </h3>
          <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
            Monitor individual component performance
          </p>
        </div>
        <SwitchToggle 
          v-model="settings.trackComponents"
          @change="handleSettingChange('trackComponents', $event)"
        />
      </div>

      <!-- Data Retention -->
      <div class="space-y-2">
        <label class="text-sm font-medium text-gray-900 dark:text-white">
          Data Retention (minutes)
        </label>
        <select
          v-model="settings.dataRetention"
          class="w-full p-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          @change="handleSettingChange('dataRetention', $event.target.value)"
        >
          <option value="5">5 minutes</option>
          <option value="10">10 minutes</option>
          <option value="30">30 minutes</option>
          <option value="60">1 hour</option>
          <option value="180">3 hours</option>
          <option value="360">6 hours</option>
        </select>
        <p class="text-xs text-gray-500 dark:text-gray-400">
          Longer retention requires more memory
        </p>
      </div>

      <!-- Performance Thresholds -->
      <div class="space-y-4">
        <h3 class="text-sm font-medium text-gray-900 dark:text-white">
          Performance Thresholds
        </h3>
        
        <!-- Render Time Warning -->
        <div class="space-y-2">
          <label class="text-xs text-gray-600 dark:text-gray-400">
            Slow Render Warning (ms)
          </label>
          <input
            v-model.number="settings.thresholds.slowRender"
            type="number"
            min="1"
            max="1000"
            class="w-full p-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            @input="handleThresholdChange('slowRender', $event.target.value)"
          />
        </div>

        <!-- Memory Usage Warning -->
        <div class="space-y-2">
          <label class="text-xs text-gray-600 dark:text-gray-400">
            High Memory Usage (MB)
          </label>
          <input
            v-model.number="settings.thresholds.highMemory"
            type="number"
            min="10"
            max="1000"
            class="w-full p-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            @input="handleThresholdChange('highMemory', $event.target.value)"
          />
        </div>
      </div>

      <!-- Notification Settings -->
      <div class="space-y-4">
        <h3 class="text-sm font-medium text-gray-900 dark:text-white">
          Notifications
        </h3>
        
        <div class="flex items-center justify-between">
          <span class="text-xs text-gray-600 dark:text-gray-400">
            Show performance alerts
          </span>
          <SwitchToggle 
            v-model="settings.notifications.enabled"
            size="sm"
            @change="handleNotificationChange('enabled', $event)"
          />
        </div>
        
        <div class="flex items-center justify-between">
          <span class="text-xs text-gray-600 dark:text-gray-400">
            Console logging
          </span>
          <SwitchToggle 
            v-model="settings.notifications.console"
            size="sm"
            @change="handleNotificationChange('console', $event)"
          />
        </div>
      </div>

      <!-- Advanced Settings -->
      <details class="group">
        <summary class="flex items-center justify-between p-3 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50 rounded-lg">
          <span class="text-sm font-medium text-gray-900 dark:text-white">
            Advanced Settings
          </span>
          <ChevronDownIcon class="w-4 h-4 text-gray-500 group-open:rotate-180 transition-transform" />
        </summary>
        
        <div class="mt-4 space-y-4 pl-4">
          <!-- Max Data Points -->
          <div class="space-y-2">
            <label class="text-xs text-gray-600 dark:text-gray-400">
              Max Data Points
            </label>
            <input
              v-model.number="settings.maxDataPoints"
              type="number"
              min="100"
              max="10000"
              class="w-full p-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              @input="handleSettingChange('maxDataPoints', $event.target.value)"
            />
          </div>

          <!-- Debug Mode -->
          <div class="flex items-center justify-between">
            <span class="text-xs text-gray-600 dark:text-gray-400">
              Debug mode
            </span>
            <SwitchToggle 
              v-model="settings.debug"
              size="sm"
              @change="handleSettingChange('debug', $event)"
            />
          </div>
        </div>
      </details>
    </div>

    <!-- Action Buttons -->
    <div class="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
      <Button
        variant="ghost"
        size="sm"
        @click="resetToDefaults"
      >
        Reset to Defaults
      </Button>
      
      <div class="flex items-center space-x-2">
        <Button
          variant="ghost"
          size="sm"
          @click="$emit('close')"
        >
          Cancel
        </Button>
        <Button
          variant="primary"
          size="sm"
          @click="saveSettings"
        >
          Save Changes
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Button from '@/components/ui/Button.vue'
import SwitchToggle from '@/components/ui/SwitchToggle.vue'
import { ChevronDownIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  config: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update-config', 'close'])

// Default settings
const defaultSettings = {
  enabled: true,
  samplingInterval: 1000,
  trackMemory: true,
  trackComponents: true,
  dataRetention: 30,
  maxDataPoints: 1000,
  debug: false,
  thresholds: {
    slowRender: 16,
    highMemory: 100
  },
  notifications: {
    enabled: true,
    console: false
  }
}

// Local settings state
const settings = ref({ ...defaultSettings, ...props.config })

// Watch for external config changes
watch(() => props.config, (newConfig) => {
  settings.value = { ...defaultSettings, ...newConfig }
}, { deep: true })

// Methods
const handleSettingChange = (key, value) => {
  settings.value[key] = typeof value === 'string' ? Number(value) || value : value
  emit('update-config', { ...settings.value })
}

const handleThresholdChange = (key, value) => {
  settings.value.thresholds[key] = Number(value) || 0
  emit('update-config', { ...settings.value })
}

const handleNotificationChange = (key, value) => {
  settings.value.notifications[key] = value
  emit('update-config', { ...settings.value })
}

const resetToDefaults = () => {
  settings.value = { ...defaultSettings }
  emit('update-config', { ...settings.value })
}

const saveSettings = () => {
  emit('update-config', { ...settings.value })
  emit('close')
}

// Computed validation
const isValid = computed(() => {
  return settings.value.samplingInterval >= 100 &&
         settings.value.dataRetention > 0 &&
         settings.value.thresholds.slowRender > 0 &&
         settings.value.thresholds.highMemory > 0
})
</script>

<style scoped>
/* Custom range slider styles */
input[type="range"]::-webkit-slider-thumb {
  @apply appearance-none w-4 h-4 bg-blue-500 rounded-full cursor-pointer;
}

input[type="range"]::-moz-range-thumb {
  @apply w-4 h-4 bg-blue-500 rounded-full cursor-pointer border-0;
}

/* Custom details/summary styles */
details > summary {
  list-style: none;
}

details > summary::-webkit-details-marker {
  display: none;
}

/* Focus states */
input:focus,
select:focus {
  @apply outline-none;
}

/* Smooth transitions */
.transition-transform {
  transition: transform 0.2s ease-in-out;
}
</style>