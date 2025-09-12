import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

// Permission definitions for each module
export const PERMISSIONS = {
  // P2P AI Permissions
  P2PAI: {
    // Dashboard permissions
    VIEW_DASHBOARD: 'p2pai:view:dashboard',
    MANAGE_DASHBOARD: 'p2pai:manage:dashboard',
    
    // Training permissions
    VIEW_TRAINING: 'p2pai:view:training',
    START_TRAINING: 'p2pai:start:training',
    STOP_TRAINING: 'p2pai:stop:training',
    MANAGE_TRAINING: 'p2pai:manage:training',
    
    // Dataset permissions
    VIEW_DATASETS: 'p2pai:view:datasets',
    CREATE_DATASET: 'p2pai:create:dataset',
    UPDATE_DATASET: 'p2pai:update:dataset',
    DELETE_DATASET: 'p2pai:delete:dataset',
    
    // Model permissions
    VIEW_MODELS: 'p2pai:view:models',
    CREATE_MODEL: 'p2pai:create:model',
    UPDATE_MODEL: 'p2pai:update:model',
    DELETE_MODEL: 'p2pai:delete:model',
    DEPLOY_MODEL: 'p2pai:deploy:model',
    
    // Project permissions
    VIEW_PROJECTS: 'p2pai:view:projects',
    CREATE_PROJECT: 'p2pai:create:project',
    UPDATE_PROJECT: 'p2pai:update:project',
    DELETE_PROJECT: 'p2pai:delete:project',
    
    // Monitoring permissions
    VIEW_MONITOR: 'p2pai:view:monitor',
    MANAGE_MONITOR: 'p2pai:manage:monitor',
    
    // Admin permissions
    MANAGE_USERS: 'p2pai:manage:users',
    VIEW_SYSTEM_STATS: 'p2pai:view:system'
  },
  
  // Edge AI Permissions
  EDGEAI: {
    VIEW_DASHBOARD: 'edgeai:view:dashboard',
    MANAGE_DEVICES: 'edgeai:manage:devices',
    DEPLOY_MODELS: 'edgeai:deploy:models',
    VIEW_ANALYTICS: 'edgeai:view:analytics'
  },
  
  // Blockchain Permissions
  BLOCKCHAIN: {
    VIEW_DASHBOARD: 'blockchain:view:dashboard',
    MANAGE_CONTRACTS: 'blockchain:manage:contracts',
    VIEW_TRANSACTIONS: 'blockchain:view:transactions',
    MANAGE_WALLET: 'blockchain:manage:wallet'
  },
  
  // Crypto Permissions
  CRYPTO: {
    VIEW_DASHBOARD: 'crypto:view:dashboard',
    MANAGE_KEYS: 'crypto:manage:keys',
    ENCRYPT_DATA: 'crypto:encrypt:data',
    DECRYPT_DATA: 'crypto:decrypt:data'
  }
}

// Role-based permission mapping
export const ROLES = {
  P2PAI: {
    ADMIN: {
      name: 'Administrator',
      permissions: [
        PERMISSIONS.P2PAI.VIEW_DASHBOARD,
        PERMISSIONS.P2PAI.MANAGE_DASHBOARD,
        PERMISSIONS.P2PAI.VIEW_TRAINING,
        PERMISSIONS.P2PAI.START_TRAINING,
        PERMISSIONS.P2PAI.STOP_TRAINING,
        PERMISSIONS.P2PAI.MANAGE_TRAINING,
        PERMISSIONS.P2PAI.VIEW_DATASETS,
        PERMISSIONS.P2PAI.CREATE_DATASET,
        PERMISSIONS.P2PAI.UPDATE_DATASET,
        PERMISSIONS.P2PAI.DELETE_DATASET,
        PERMISSIONS.P2PAI.VIEW_MODELS,
        PERMISSIONS.P2PAI.CREATE_MODEL,
        PERMISSIONS.P2PAI.UPDATE_MODEL,
        PERMISSIONS.P2PAI.DELETE_MODEL,
        PERMISSIONS.P2PAI.DEPLOY_MODEL,
        PERMISSIONS.P2PAI.VIEW_PROJECTS,
        PERMISSIONS.P2PAI.CREATE_PROJECT,
        PERMISSIONS.P2PAI.UPDATE_PROJECT,
        PERMISSIONS.P2PAI.DELETE_PROJECT,
        PERMISSIONS.P2PAI.VIEW_MONITOR,
        PERMISSIONS.P2PAI.MANAGE_MONITOR,
        PERMISSIONS.P2PAI.MANAGE_USERS,
        PERMISSIONS.P2PAI.VIEW_SYSTEM_STATS
      ]
    },
    RESEARCHER: {
      name: 'Researcher',
      permissions: [
        PERMISSIONS.P2PAI.VIEW_DASHBOARD,
        PERMISSIONS.P2PAI.VIEW_TRAINING,
        PERMISSIONS.P2PAI.START_TRAINING,
        PERMISSIONS.P2PAI.STOP_TRAINING,
        PERMISSIONS.P2PAI.VIEW_DATASETS,
        PERMISSIONS.P2PAI.CREATE_DATASET,
        PERMISSIONS.P2PAI.UPDATE_DATASET,
        PERMISSIONS.P2PAI.VIEW_MODELS,
        PERMISSIONS.P2PAI.CREATE_MODEL,
        PERMISSIONS.P2PAI.UPDATE_MODEL,
        PERMISSIONS.P2PAI.VIEW_PROJECTS,
        PERMISSIONS.P2PAI.CREATE_PROJECT,
        PERMISSIONS.P2PAI.UPDATE_PROJECT,
        PERMISSIONS.P2PAI.VIEW_MONITOR
      ]
    },
    DATA_PROVIDER: {
      name: 'Data Provider',
      permissions: [
        PERMISSIONS.P2PAI.VIEW_DASHBOARD,
        PERMISSIONS.P2PAI.VIEW_DATASETS,
        PERMISSIONS.P2PAI.CREATE_DATASET,
        PERMISSIONS.P2PAI.UPDATE_DATASET,
        PERMISSIONS.P2PAI.VIEW_PROJECTS,
        PERMISSIONS.P2PAI.VIEW_MONITOR
      ]
    },
    VIEWER: {
      name: 'Viewer',
      permissions: [
        PERMISSIONS.P2PAI.VIEW_DASHBOARD,
        PERMISSIONS.P2PAI.VIEW_TRAINING,
        PERMISSIONS.P2PAI.VIEW_DATASETS,
        PERMISSIONS.P2PAI.VIEW_MODELS,
        PERMISSIONS.P2PAI.VIEW_PROJECTS,
        PERMISSIONS.P2PAI.VIEW_MONITOR
      ]
    }
  },
  
  EDGEAI: {
    ADMIN: {
      name: 'Administrator',
      permissions: Object.values(PERMISSIONS.EDGEAI)
    },
    OPERATOR: {
      name: 'Operator',
      permissions: [
        PERMISSIONS.EDGEAI.VIEW_DASHBOARD,
        PERMISSIONS.EDGEAI.MANAGE_DEVICES,
        PERMISSIONS.EDGEAI.DEPLOY_MODELS
      ]
    },
    VIEWER: {
      name: 'Viewer',
      permissions: [
        PERMISSIONS.EDGEAI.VIEW_DASHBOARD,
        PERMISSIONS.EDGEAI.VIEW_ANALYTICS
      ]
    }
  },
  
  BLOCKCHAIN: {
    ADMIN: {
      name: 'Administrator',
      permissions: Object.values(PERMISSIONS.BLOCKCHAIN)
    },
    DEVELOPER: {
      name: 'Developer',
      permissions: [
        PERMISSIONS.BLOCKCHAIN.VIEW_DASHBOARD,
        PERMISSIONS.BLOCKCHAIN.MANAGE_CONTRACTS,
        PERMISSIONS.BLOCKCHAIN.VIEW_TRANSACTIONS
      ]
    },
    VIEWER: {
      name: 'Viewer',
      permissions: [
        PERMISSIONS.BLOCKCHAIN.VIEW_DASHBOARD,
        PERMISSIONS.BLOCKCHAIN.VIEW_TRANSACTIONS
      ]
    }
  },
  
  CRYPTO: {
    ADMIN: {
      name: 'Administrator',
      permissions: Object.values(PERMISSIONS.CRYPTO)
    },
    OPERATOR: {
      name: 'Operator',
      permissions: [
        PERMISSIONS.CRYPTO.VIEW_DASHBOARD,
        PERMISSIONS.CRYPTO.ENCRYPT_DATA,
        PERMISSIONS.CRYPTO.DECRYPT_DATA
      ]
    },
    VIEWER: {
      name: 'Viewer',
      permissions: [
        PERMISSIONS.CRYPTO.VIEW_DASHBOARD
      ]
    }
  }
}

// Global permission state
const userPermissions = ref(new Set())
const userRole = ref(null)

export const usePermissions = () => {
  const authStore = useAuthStore()
  const router = useRouter()

  // Initialize permissions based on user role and module
  const initializePermissions = (role, module) => {
    userRole.value = role
    const moduleRoles = ROLES[module?.toUpperCase()]
    
    if (moduleRoles && moduleRoles[role?.toUpperCase()]) {
      const rolePermissions = moduleRoles[role.toUpperCase()].permissions
      userPermissions.value = new Set(rolePermissions)
    } else {
      // Default to viewer permissions if role not found
      const viewerRole = moduleRoles?.VIEWER
      if (viewerRole) {
        userPermissions.value = new Set(viewerRole.permissions)
      } else {
        userPermissions.value = new Set()
      }
    }
  }

  // Check if user has specific permission
  const hasPermission = (permission) => {
    return userPermissions.value.has(permission)
  }

  // Check if user has any of the provided permissions
  const hasAnyPermission = (permissions) => {
    return permissions.some(permission => userPermissions.value.has(permission))
  }

  // Check if user has all of the provided permissions
  const hasAllPermissions = (permissions) => {
    return permissions.every(permission => userPermissions.value.has(permission))
  }

  // Check if user has specific role
  const hasRole = (role) => {
    return userRole.value?.toUpperCase() === role?.toUpperCase()
  }

  // Check if user has any of the provided roles
  const hasAnyRole = (roles) => {
    return roles.some(role => hasRole(role))
  }

  // Route guard for permissions
  const requiresPermission = (permission) => {
    return (to, from, next) => {
      if (hasPermission(permission)) {
        next()
      } else {
        // Redirect to access denied or dashboard
        next({ name: 'AccessDenied' })
      }
    }
  }

  // Route guard for roles
  const requiresRole = (role) => {
    return (to, from, next) => {
      if (hasRole(role)) {
        next()
      } else {
        next({ name: 'AccessDenied' })
      }
    }
  }

  // Get permissions for current module
  const getCurrentModulePermissions = computed(() => {
    const module = authStore.getCurrentModule?.toUpperCase()
    return PERMISSIONS[module] || {}
  })

  // Get roles for current module
  const getCurrentModuleRoles = computed(() => {
    const module = authStore.getCurrentModule?.toUpperCase()
    return ROLES[module] || {}
  })

  // Get current user role info
  const getCurrentRoleInfo = computed(() => {
    const module = authStore.getCurrentModule?.toUpperCase()
    const moduleRoles = ROLES[module]
    if (moduleRoles && userRole.value) {
      return moduleRoles[userRole.value.toUpperCase()]
    }
    return null
  })

  // Navigation helpers with permission checks
  const canNavigateTo = (routeName) => {
    const route = router.resolve({ name: routeName })
    const requiredPermissions = route.meta?.permissions || []
    const requiredRoles = route.meta?.roles || []
    
    if (requiredPermissions.length > 0) {
      return hasAllPermissions(requiredPermissions)
    }
    
    if (requiredRoles.length > 0) {
      return hasAnyRole(requiredRoles)
    }
    
    return true
  }

  // Safe navigation with permission check
  const navigateIfAllowed = (routeName, fallback = null) => {
    if (canNavigateTo(routeName)) {
      router.push({ name: routeName })
    } else if (fallback) {
      router.push(fallback)
    }
  }

  // Get filtered menu items based on permissions
  const getFilteredMenuItems = (menuItems) => {
    return menuItems.filter(item => {
      if (item.permissions) {
        return hasAllPermissions(item.permissions)
      }
      if (item.roles) {
        return hasAnyRole(item.roles)
      }
      if (item.routeName) {
        return canNavigateTo(item.routeName)
      }
      return true
    })
  }

  // Debug helpers
  const getAllPermissions = () => Array.from(userPermissions.value)
  const getRole = () => userRole.value

  return {
    // Initialization
    initializePermissions,
    
    // Permission checks
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    
    // Role checks
    hasRole,
    hasAnyRole,
    
    // Route guards
    requiresPermission,
    requiresRole,
    
    // Navigation helpers
    canNavigateTo,
    navigateIfAllowed,
    getFilteredMenuItems,
    
    // Computed properties
    getCurrentModulePermissions,
    getCurrentModuleRoles,
    getCurrentRoleInfo,
    
    // Debug helpers
    getAllPermissions,
    getRole,
    
    // State
    userPermissions: userPermissions.value,
    userRole
  }
}