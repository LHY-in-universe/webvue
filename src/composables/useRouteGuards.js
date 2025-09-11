import { useAuthStore } from '@/stores/auth'
import { usePermissions, PERMISSIONS } from '@/composables/usePermissions'
import { $notify } from '@/composables/useNotifications'

// Enhanced route metadata for permission checking
export const enhanceRoutes = (routes) => {
  return routes.map(route => ({
    ...route,
    beforeEnter: createRouteGuard(route.meta || {}),
    meta: {
      ...route.meta,
      // Enhance with default values
      requiresAuth: route.meta?.requiresAuth ?? false,
      permissions: route.meta?.permissions ?? [],
      roles: route.meta?.roles ?? [],
      allowGuest: route.meta?.allowGuest ?? false
    }
  }))
}

// Create a route guard based on route metadata
export const createRouteGuard = (meta) => {
  return async (to, from, next) => {
    const authStore = useAuthStore()
    const { hasAllPermissions, hasAnyRole, initializePermissions } = usePermissions()

    try {
      // Check authentication requirement
      if (meta.requiresAuth && !authStore.isAuthenticated) {
        const module = to.path.split('/')[1]
        $notify.warning('Please log in to access this page')
        next({ name: `${module}Login` })
        return
      }

      // Skip permission checks if guest allowed or no auth required
      if (meta.allowGuest || !meta.requiresAuth) {
        next()
        return
      }

      // Initialize permissions if authenticated
      if (authStore.isAuthenticated && authStore.userType && authStore.currentModule) {
        initializePermissions(authStore.userType, authStore.currentModule)
      }

      // Check required permissions
      if (meta.permissions && meta.permissions.length > 0) {
        if (!hasAllPermissions(meta.permissions)) {
          $notify.error('You do not have permission to access this page')
          next({ name: 'AccessDenied', query: { redirect: to.fullPath } })
          return
        }
      }

      // Check required roles
      if (meta.roles && meta.roles.length > 0) {
        if (!hasAnyRole(meta.roles)) {
          $notify.error('Your role does not have access to this page')
          next({ name: 'AccessDenied', query: { redirect: to.fullPath } })
          return
        }
      }

      // Custom guard function
      if (meta.customGuard && typeof meta.customGuard === 'function') {
        const result = await meta.customGuard(to, from, authStore)
        if (result !== true) {
          if (typeof result === 'string') {
            next({ path: result })
          } else if (typeof result === 'object') {
            next(result)
          } else {
            next(false)
          }
          return
        }
      }

      next()
    } catch (error) {
      console.error('Route guard error:', error)
      $notify.error('An error occurred while checking permissions')
      next({ name: 'Home' })
    }
  }
}

// Global navigation guards
export const setupGlobalGuards = (router) => {
  // Before each route
  router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()
    
    // Update page title
    document.title = to.meta.title || 'FedMPC'
    
    // Loading state management
    if (to.meta.showLoading !== false) {
      // Show loading if navigation takes time
      const loadingTimeout = setTimeout(() => {
        $notify.info('Loading page...', { id: 'page-loading', duration: 0 })
      }, 500)
      
      // Clear loading after navigation
      const clearLoading = () => {
        clearTimeout(loadingTimeout)
        $notify.dismiss('page-loading')
      }
      
      router.afterEach(clearLoading)
      
      // Clear on navigation cancel/error
      setTimeout(clearLoading, 10000) // Max 10s loading
    }

    // Module-specific logic
    const module = to.path.split('/')[1]
    if (module && module !== authStore.currentModule) {
      // Switching modules - might need different auth
      if (to.meta.requiresAuth && !to.meta.allowModuleSwitch) {
        const isAuthenticated = localStorage.getItem(`${module}_auth`)
        if (!isAuthenticated) {
          next(`/${module}/login`)
          return
        }
      }
    }

    next()
  })

  // After each route
  router.afterEach((to, from, failure) => {
    if (failure) {
      console.error('Navigation failed:', failure)
      $notify.error('Navigation failed')
    } else {
      // Track page views, analytics, etc.
      if (to.meta.trackPageView !== false) {
        // Analytics tracking would go here
        console.log('Page view:', to.path)
      }
    }
  })

  // Error handling
  router.onError((error, to, from) => {
    console.error('Router error:', error)
    $notify.error('A navigation error occurred')
    
    // Try to recover
    if (from.name) {
      router.push(from)
    } else {
      router.push({ name: 'Home' })
    }
  })
}

// Permission-enhanced route definitions
export const createPermissionRoutes = () => {
  return {
    // P2P AI Routes with permissions
    p2pai: [
      {
        path: '/p2pai/dashboard',
        name: 'P2PAIDashboard',
        component: () => import('@/views/p2pai/Dashboard.vue'),
        meta: {
          title: 'P2P AI - Dashboard',
          requiresAuth: true,
          permissions: [PERMISSIONS.P2PAI.VIEW_DASHBOARD],
          trackPageView: true
        }
      },
      {
        path: '/p2pai/training/federated',
        name: 'P2PAIFederatedTraining',
        component: () => import('@/views/p2pai/FederatedTraining.vue'),
        meta: {
          title: 'P2P AI - Federated Training',
          requiresAuth: true,
          permissions: [PERMISSIONS.P2PAI.VIEW_TRAINING, PERMISSIONS.P2PAI.START_TRAINING],
          roles: ['ADMIN', 'RESEARCHER']
        }
      },
      {
        path: '/p2pai/datasets',
        name: 'P2PAIDatasets',
        component: () => import('@/views/p2pai/DatasetDashboard.vue'),
        meta: {
          title: 'P2P AI - Dataset Management',
          requiresAuth: true,
          permissions: [PERMISSIONS.P2PAI.VIEW_DATASETS],
          customGuard: async (to, from, authStore) => {
            // Custom logic for dataset access
            if (authStore.userType === 'VIEWER' && !authStore.user?.hasDatasetAccess) {
              return { name: 'P2PAIDashboard', query: { message: 'dataset_access_required' } }
            }
            return true
          }
        }
      },
      {
        path: '/p2pai/models',
        name: 'P2PAIModels',
        component: () => import('@/views/p2pai/ModelDashboard.vue'),
        meta: {
          title: 'P2P AI - Model Management',
          requiresAuth: true,
          permissions: [PERMISSIONS.P2PAI.VIEW_MODELS]
        }
      },
      {
        path: '/p2pai/monitor',
        name: 'P2PAIMonitor',
        component: () => import('@/views/p2pai/TrainingMonitor.vue'),
        meta: {
          title: 'P2P AI - Training Monitor',
          requiresAuth: true,
          permissions: [PERMISSIONS.P2PAI.VIEW_MONITOR],
          refreshInterval: 5000 // Auto-refresh every 5s
        }
      },
      {
        path: '/p2pai/overview',
        name: 'P2PAIOverview',
        component: () => import('@/views/p2pai/ProjectOverview.vue'),
        meta: {
          title: 'P2P AI - Project Overview',
          requiresAuth: true,
          permissions: [PERMISSIONS.P2PAI.VIEW_PROJECTS]
        }
      },
      {
        path: '/p2pai/admin',
        name: 'P2PAIAdmin',
        component: () => import('@/views/p2pai/AdminDashboard.vue'),
        meta: {
          title: 'P2P AI - Administration',
          requiresAuth: true,
          roles: ['ADMIN'],
          permissions: [PERMISSIONS.P2PAI.MANAGE_USERS, PERMISSIONS.P2PAI.VIEW_SYSTEM_STATS]
        }
      }
    ]
  }
}

// Route helper functions
export const useRouteHelpers = () => {
  const authStore = useAuthStore()
  const { canNavigateTo, hasPermission } = usePermissions()

  // Check if current user can access a route
  const canAccessRoute = (routeName, params = {}) => {
    try {
      const resolved = router.resolve({ name: routeName, params })
      const meta = resolved.meta || {}
      
      if (meta.requiresAuth && !authStore.isAuthenticated) {
        return false
      }
      
      if (meta.permissions && !hasAllPermissions(meta.permissions)) {
        return false
      }
      
      if (meta.roles && !hasAnyRole(meta.roles)) {
        return false
      }
      
      return true
    } catch {
      return false
    }
  }

  // Get available routes for current user
  const getAvailableRoutes = (routes) => {
    return routes.filter(route => {
      const routeName = route.name || route.path
      return canAccessRoute(routeName)
    })
  }

  // Navigate with permission check
  const navigateWithPermissionCheck = (to, options = {}) => {
    const { fallback = '/', showError = true } = options
    
    if (canAccessRoute(to.name || to)) {
      router.push(to)
    } else {
      if (showError) {
        $notify.error('You do not have permission to access that page')
      }
      router.push(fallback)
    }
  }

  return {
    canAccessRoute,
    getAvailableRoutes,
    navigateWithPermissionCheck
  }
}

// Breadcrumb helpers
export const useBreadcrumbs = () => {
  const generateBreadcrumbs = (route) => {
    const breadcrumbs = []
    const pathSegments = route.path.split('/').filter(Boolean)
    
    let currentPath = ''
    pathSegments.forEach((segment, index) => {
      currentPath += `/${segment}`
      
      // Try to resolve route for breadcrumb
      try {
        const resolved = router.resolve(currentPath)
        if (resolved.name) {
          breadcrumbs.push({
            name: resolved.meta?.breadcrumbTitle || resolved.meta?.title || segment,
            path: currentPath,
            active: index === pathSegments.length - 1
          })
        }
      } catch {
        // Fallback breadcrumb
        breadcrumbs.push({
          name: segment.charAt(0).toUpperCase() + segment.slice(1),
          path: currentPath,
          active: index === pathSegments.length - 1
        })
      }
    })
    
    return breadcrumbs
  }

  return { generateBreadcrumbs }
}