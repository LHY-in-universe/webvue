<template>
  <div v-if="hasAccess">
    <slot />
  </div>
  
  <!-- Fallback content when no access -->
  <div v-else-if="$slots.fallback || fallback">
    <slot name="fallback">
      <div v-if="fallback" :class="fallbackClasses">
        <div class="text-center p-6">
          <component :is="fallbackIcon" class="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
            {{ fallbackTitle }}
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
            {{ fallbackMessage }}
          </p>
          <Button 
            v-if="showFallbackAction && fallbackAction"
            :variant="fallbackActionVariant"
            :size="fallbackActionSize"
            @click="fallbackAction.handler"
          >
            {{ fallbackAction.label }}
          </Button>
        </div>
      </div>
    </slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePermissions } from '@/composables/usePermissions'
import Button from '@/components/ui/Button.vue'
import { 
  LockClosedIcon,
  ExclamationTriangleIcon,
  ShieldExclamationIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  // Permission-based access
  permissions: {
    type: Array,
    default: () => []
  },
  requireAllPermissions: {
    type: Boolean,
    default: true
  },
  
  // Role-based access
  roles: {
    type: Array,
    default: () => []
  },
  requireAllRoles: {
    type: Boolean,
    default: false
  },
  
  // Custom access function
  customCheck: {
    type: Function,
    default: null
  },
  
  // Fallback options
  fallback: {
    type: Boolean,
    default: false
  },
  fallbackTitle: {
    type: String,
    default: 'Access Restricted'
  },
  fallbackMessage: {
    type: String,
    default: 'You do not have permission to view this content.'
  },
  fallbackIcon: {
    type: [Object, Function],
    default: () => LockClosedIcon
  },
  fallbackVariant: {
    type: String,
    default: 'warning',
    validator: value => ['info', 'warning', 'error'].includes(value)
  },
  showFallbackAction: {
    type: Boolean,
    default: false
  },
  fallbackAction: {
    type: Object,
    default: null
    // { label: string, handler: function, variant?: string, size?: string }
  },
  fallbackActionVariant: {
    type: String,
    default: 'primary'
  },
  fallbackActionSize: {
    type: String,
    default: 'sm'
  }
})

const { 
  hasPermission, 
  hasAnyPermission, 
  hasAllPermissions,
  hasRole,
  hasAnyRole
} = usePermissions()

const hasAccess = computed(() => {
  // Custom check takes precedence
  if (props.customCheck) {
    return props.customCheck()
  }
  
  let permissionCheck = true
  let roleCheck = true
  
  // Check permissions
  if (props.permissions.length > 0) {
    if (props.requireAllPermissions) {
      permissionCheck = hasAllPermissions(props.permissions)
    } else {
      permissionCheck = hasAnyPermission(props.permissions)
    }
  }
  
  // Check roles
  if (props.roles.length > 0) {
    if (props.requireAllRoles) {
      roleCheck = props.roles.every(role => hasRole(role))
    } else {
      roleCheck = hasAnyRole(props.roles)
    }
  }
  
  return permissionCheck && roleCheck
})

const fallbackClasses = computed(() => {
  const variants = {
    info: 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg',
    warning: 'bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg',
    error: 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg'
  }
  
  return variants[props.fallbackVariant] || variants.warning
})
</script>