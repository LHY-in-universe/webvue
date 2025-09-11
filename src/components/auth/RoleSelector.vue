<template>
  <div :class="containerClasses">
    <div v-if="title || $slots.title" class="text-center mb-8">
      <slot name="title">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {{ title }}
        </h2>
        <p v-if="subtitle" class="text-gray-600 dark:text-gray-400">
          {{ subtitle }}
        </p>
      </slot>
    </div>

    <div :class="gridClasses">
      <div
        v-for="(role, key) in availableRoles"
        :key="key"
        :class="[
          'role-card relative p-6 border-2 rounded-xl transition-all duration-200 cursor-pointer',
          selectedRole === key 
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
            : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-md',
          interactive && 'hover:scale-105'
        ]"
        @click="selectRole(key)"
      >
        <!-- Selection Indicator -->
        <div 
          v-if="selectedRole === key"
          class="absolute top-3 right-3 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center"
        >
          <CheckIcon class="w-4 h-4 text-white" />
        </div>

        <!-- Role Icon -->
        <div v-if="role.icon" class="flex justify-center mb-4">
          <component 
            :is="role.icon" 
            :class="[
              'w-12 h-12',
              selectedRole === key 
                ? 'text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-400'
            ]"
          />
        </div>

        <!-- Role Name -->
        <h3 :class="[
          'text-lg font-semibold text-center mb-2',
          selectedRole === key 
            ? 'text-blue-900 dark:text-blue-100'
            : 'text-gray-900 dark:text-white'
        ]">
          {{ role.name }}
        </h3>

        <!-- Role Description -->
        <p v-if="role.description" :class="[
          'text-sm text-center mb-4',
          selectedRole === key
            ? 'text-blue-700 dark:text-blue-300'
            : 'text-gray-600 dark:text-gray-400'
        ]">
          {{ role.description }}
        </p>

        <!-- Permissions Preview -->
        <div v-if="showPermissions && role.permissions?.length" class="mt-4">
          <h4 class="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2 text-center">
            Key Permissions:
          </h4>
          <div class="flex flex-wrap gap-1 justify-center">
            <span
              v-for="permission in getDisplayPermissions(role.permissions)"
              :key="permission"
              class="px-2 py-1 text-xs rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300"
            >
              {{ formatPermission(permission) }}
            </span>
          </div>
        </div>

        <!-- Role Features -->
        <div v-if="role.features?.length" class="mt-4">
          <ul class="text-xs space-y-1">
            <li
              v-for="feature in role.features.slice(0, maxFeatures)"
              :key="feature"
              :class="[
                'flex items-center',
                selectedRole === key
                  ? 'text-blue-700 dark:text-blue-300'
                  : 'text-gray-600 dark:text-gray-400'
              ]"
            >
              <CheckIcon class="w-3 h-3 mr-1 flex-shrink-0" />
              {{ feature }}
            </li>
            <li v-if="role.features.length > maxFeatures" class="text-gray-500 text-center">
              +{{ role.features.length - maxFeatures }} more
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div v-if="showActions" class="flex justify-center space-x-4 mt-8">
      <Button
        v-if="showCancel"
        variant="ghost"
        @click="$emit('cancel')"
        :disabled="loading"
      >
        {{ cancelText }}
      </Button>
      
      <Button
        variant="primary"
        @click="confirmSelection"
        :disabled="!selectedRole || loading"
        :loading="loading"
      >
        {{ confirmText }}
      </Button>
    </div>

    <!-- Role Details Modal (Optional) -->
    <Modal
      v-if="showDetailsModal"
      v-model:is-open="detailsModalOpen"
      :title="`${currentDetailRole?.name} Details`"
      size="md"
    >
      <div v-if="currentDetailRole" class="p-6">
        <div v-if="currentDetailRole.icon" class="text-center mb-6">
          <component 
            :is="currentDetailRole.icon" 
            class="w-16 h-16 text-blue-600 mx-auto mb-4"
          />
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
            {{ currentDetailRole.name }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400 mt-2">
            {{ currentDetailRole.description }}
          </p>
        </div>

        <div v-if="currentDetailRole.permissions?.length" class="mb-6">
          <h4 class="font-medium text-gray-900 dark:text-white mb-3">
            Permissions:
          </h4>
          <div class="grid grid-cols-1 gap-2">
            <div
              v-for="permission in currentDetailRole.permissions"
              :key="permission"
              class="flex items-center p-2 bg-gray-50 dark:bg-gray-700 rounded-md"
            >
              <CheckIcon class="w-4 h-4 text-green-500 mr-2" />
              <span class="text-sm text-gray-700 dark:text-gray-300">
                {{ formatPermission(permission) }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="currentDetailRole.features?.length">
          <h4 class="font-medium text-gray-900 dark:text-white mb-3">
            Features:
          </h4>
          <ul class="space-y-2">
            <li
              v-for="feature in currentDetailRole.features"
              :key="feature"
              class="flex items-start"
            >
              <CheckIcon class="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
              <span class="text-sm text-gray-700 dark:text-gray-300">{{ feature }}</span>
            </li>
          </ul>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Button from '@/components/ui/Button.vue'
import Modal from '@/components/ui/Modal.vue'
import { CheckIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  roles: {
    type: Object,
    required: true
  },
  modelValue: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: 'Select Your Role'
  },
  subtitle: {
    type: String,
    default: 'Choose the role that best matches your responsibilities'
  },
  columns: {
    type: Number,
    default: 0, // Auto-responsive
    validator: value => value >= 0 && value <= 4
  },
  showPermissions: {
    type: Boolean,
    default: false
  },
  maxPermissions: {
    type: Number,
    default: 3
  },
  maxFeatures: {
    type: Number,
    default: 3
  },
  interactive: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  showCancel: {
    type: Boolean,
    default: false
  },
  confirmText: {
    type: String,
    default: 'Continue'
  },
  cancelText: {
    type: String,
    default: 'Cancel'
  },
  loading: {
    type: Boolean,
    default: false
  },
  showDetailsModal: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel', 'role-selected'])

const selectedRole = ref(props.modelValue)
const detailsModalOpen = ref(false)
const currentDetailRole = ref(null)

const availableRoles = computed(() => props.roles)

const containerClasses = computed(() => {
  return 'max-w-6xl mx-auto'
})

const gridClasses = computed(() => {
  if (props.columns > 0) {
    const cols = Math.min(props.columns, Object.keys(availableRoles.value).length)
    return `grid gap-6 grid-cols-1 md:grid-cols-${cols}`
  }
  
  // Auto-responsive grid based on number of roles
  const roleCount = Object.keys(availableRoles.value).length
  if (roleCount <= 2) return 'grid gap-6 grid-cols-1 md:grid-cols-2'
  if (roleCount <= 3) return 'grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
  return 'grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'
})

const selectRole = (roleKey) => {
  selectedRole.value = roleKey
  emit('update:modelValue', roleKey)
  emit('role-selected', {
    key: roleKey,
    role: availableRoles.value[roleKey]
  })
}

const confirmSelection = () => {
  if (selectedRole.value) {
    emit('confirm', {
      key: selectedRole.value,
      role: availableRoles.value[selectedRole.value]
    })
  }
}

const getDisplayPermissions = (permissions) => {
  return permissions.slice(0, props.maxPermissions)
}

const formatPermission = (permission) => {
  // Convert permission string to readable format
  // e.g., "p2pai:view:dashboard" -> "View Dashboard"
  return permission
    .split(':')
    .slice(-1)[0]
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const showRoleDetails = (roleKey) => {
  currentDetailRole.value = {
    key: roleKey,
    ...availableRoles.value[roleKey]
  }
  detailsModalOpen.value = true
}

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  selectedRole.value = newValue
})
</script>

<style scoped>
.role-card {
  @apply transform transition-all duration-200;
}

.role-card:hover {
  @apply shadow-lg;
}

.role-card.selected {
  @apply ring-2 ring-blue-500 ring-opacity-50;
}
</style>