<template>
  <InfoCard
    :title="title"
    :subtitle="subtitle"
    :icon="icon"
    :status="status"
    :badge="badge"
    :badgeVariant="badgeVariant"
    :interactive="true"
    :elevated="elevated"
    :timestamp="timestamp"
    @click="toggleExpanded"
  >
    <!-- Preview Content -->
    <div class="space-y-3">
      <div v-if="preview" class="text-body text-gray-700 dark:text-gray-300">
        {{ preview }}
      </div>
      
      <!-- Quick Stats -->
      <div v-if="quickStats && quickStats.length" class="flex flex-wrap gap-4">
        <div 
          v-for="(stat, index) in quickStats" 
          :key="index"
          class="flex items-center space-x-2"
        >
          <div class="w-2 h-2 bg-primary-500 rounded-full"></div>
          <span class="text-body-sm text-gray-600 dark:text-gray-400">
            <strong class="text-gray-900 dark:text-white">{{ stat.value }}</strong>
            {{ stat.label }}
          </span>
        </div>
      </div>
      
      <!-- Expandable Indicator -->
      <div class="flex items-center justify-between mt-4">
        <span class="text-body-sm text-primary-600 dark:text-primary-400 font-medium">
          {{ expanded ? '点击收起' : '点击查看详情' }}
        </span>
        <ChevronDownIcon 
          :class="[
            'w-5 h-5 text-primary-600 dark:text-primary-400 transition-transform duration-200',
            { 'transform rotate-180': expanded }
          ]"
        />
      </div>
    </div>
    
    <!-- Expanded Content -->
    <div 
      v-if="expanded"
      class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700 animate-fade-in"
    >
      <!-- Detail Sections -->
      <div v-if="details && details.length" class="space-y-6">
        <div v-for="(section, index) in details" :key="index">
          <h4 class="text-heading-3 text-gray-900 dark:text-white mb-3">
            {{ section.title }}
          </h4>
          
          <!-- Key-Value Pairs -->
          <div v-if="section.type === 'keyValue'" class="space-y-2">
            <div 
              v-for="(item, itemIndex) in section.data" 
              :key="itemIndex"
              class="flex justify-between py-2"
            >
              <span class="text-body-sm text-gray-600 dark:text-gray-400">
                {{ item.key }}
              </span>
              <span class="text-body-sm font-medium text-gray-900 dark:text-white">
                {{ item.value }}
              </span>
            </div>
          </div>
          
          <!-- List -->
          <div v-else-if="section.type === 'list'" class="space-y-2">
            <div 
              v-for="(item, itemIndex) in section.data" 
              :key="itemIndex"
              class="flex items-start space-x-3"
            >
              <div class="flex-shrink-0 w-1.5 h-1.5 bg-primary-500 rounded-full mt-2"></div>
              <span class="text-body-sm text-gray-700 dark:text-gray-300">
                {{ item }}
              </span>
            </div>
          </div>
          
          <!-- Text -->
          <div v-else-if="section.type === 'text'" class="text-body text-gray-700 dark:text-gray-300">
            {{ section.data }}
          </div>
          
          <!-- Custom Content Slot -->
          <div v-else-if="section.type === 'custom'">
            <slot :name="section.slot" :data="section.data" />
          </div>
        </div>
      </div>
      
      <!-- Custom Expanded Content -->
      <div v-if="$slots.expanded">
        <slot name="expanded" />
      </div>
      
      <!-- Action Buttons -->
      <div v-if="actions && actions.length" class="flex flex-wrap gap-3 mt-6">
        <button
          v-for="(action, index) in actions"
          :key="index"
          :class="[
            'btn-base px-4 py-2',
            action.variant === 'primary' ? 'btn-primary' :
            action.variant === 'secondary' ? 'btn-secondary' :
            action.variant === 'success' ? 'btn-success' :
            action.variant === 'warning' ? 'btn-warning' :
            action.variant === 'danger' ? 'btn-danger' :
            'btn-ghost'
          ]"
          @click.stop="handleActionClick(action)"
        >
          <component v-if="action.icon" :is="action.icon" class="w-4 h-4 mr-2" />
          {{ action.label }}
        </button>
      </div>
    </div>
  </InfoCard>
</template>

<script setup>
import { ref } from 'vue'
import InfoCard from './InfoCard.vue'
import { ChevronDownIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  title: String,
  subtitle: String,
  icon: [Object, Function, String],
  status: {
    type: String,
    validator: value => ['success', 'warning', 'danger', 'info'].includes(value)
  },
  badge: String,
  badgeVariant: {
    type: String,
    default: 'primary'
  },
  elevated: {
    type: Boolean,
    default: true
  },
  timestamp: [String, Date, Number],
  preview: String,
  quickStats: Array,
  details: Array,
  actions: Array,
  defaultExpanded: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['expand', 'collapse', 'action'])

const expanded = ref(props.defaultExpanded)

const toggleExpanded = () => {
  expanded.value = !expanded.value
  emit(expanded.value ? 'expand' : 'collapse')
}

const handleActionClick = (action) => {
  emit('action', action)
  if (action.handler) {
    action.handler()
  }
}
</script>