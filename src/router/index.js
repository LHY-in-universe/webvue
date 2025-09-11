import { createRouter, createWebHistory } from 'vue-router'

// Lazy load views for better performance
const Home = () => import('@/views/Home.vue')
const ThemeTransitionDemo = () => import('@/views/ThemeTransitionDemo.vue')

// P2P AI Module Routes
const P2PAI = {
  Login: () => import('@/views/p2pai/Login.vue'),
  UserTypeSelect: () => import('@/views/p2pai/UserTypeSelect.vue'),
  Dashboard: () => import('@/views/p2pai/Dashboard.vue'),
  FederatedTraining: () => import('@/views/p2pai/FederatedTraining.vue'),
  LocalTraining: () => import('@/views/p2pai/LocalTraining.vue'),
  MPCTraining: () => import('@/views/p2pai/MPCTraining.vue'),
  DatasetDashboard: () => import('@/views/p2pai/DatasetDashboard.vue'),
  ModelDashboard: () => import('@/views/p2pai/ModelDashboard.vue'),
  TrainingMonitor: () => import('@/views/p2pai/TrainingMonitor.vue'),
  ProjectOverview: () => import('@/views/p2pai/ProjectOverview.vue'),
  ProjectVisualization: () => import('@/views/p2pai/ProjectVisualization.vue'),
}

// EdgeAI Module Routes  
const EdgeAI = {
  Login: () => import('@/views/edgeai/Login.vue'),
  Dashboard: () => import('@/views/edgeai/Dashboard.vue'),
  AllNodes: () => import('@/views/edgeai/AllNodes.vue'),
  CreateProject: () => import('@/views/edgeai/CreateProject.vue'),
  ProjectManager: () => import('@/views/edgeai/ProjectManager.vue'),
  Visualization: () => import('@/views/edgeai/Visualization.vue'),
  ImportProject: () => import('@/views/edgeai/ImportProject.vue'),
  TaskManager: () => import('@/views/edgeai/TaskManager.vue'),
  PerformanceMetrics: () => import('@/views/edgeai/PerformanceMetrics.vue'),
  SystemLogs: () => import('@/views/edgeai/SystemLogs.vue'),
  ModelManagement: () => import('@/views/edgeai/ModelManagement.vue'),
  ModelDetails: () => import('@/views/edgeai/ModelDetails.vue'),
}

// Blockchain Module Routes
const Blockchain = {
  Login: () => import('@/views/blockchain/Login.vue'),
  Dashboard: () => import('@/views/blockchain/Dashboard.vue'),
}

// Crypto Module Routes
const Crypto = {
  Login: () => import('@/views/crypto/Login.vue'),
  Dashboard: () => import('@/views/crypto/Dashboard.vue'),
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'FedMPC - 联邦多方计算平台' }
  },
  {
    path: '/theme-demo',
    name: 'ThemeTransitionDemo',
    component: ThemeTransitionDemo,
    meta: { title: 'Vue Native Theme Transitions Demo' }
  },
  
  
  // P2P AI Routes
  {
    path: '/p2pai/login',
    name: 'P2PAILogin',
    component: P2PAI.Login,
    meta: { title: 'P2P AI - 登录' }
  },
  {
    path: '/p2pai/user-type-select',
    name: 'P2PAIUserSelect', 
    component: P2PAI.UserTypeSelect,
    meta: { title: 'P2P AI - 用户类型选择' }
  },
  {
    path: '/p2pai/dashboard',
    name: 'P2PAIDashboard',
    component: P2PAI.Dashboard,
    meta: { 
      title: 'P2P AI - Dashboard',
      requiresAuth: true
    }
  },
  {
    path: '/p2pai/federated-training',
    name: 'P2PAIFederatedTraining',
    component: P2PAI.FederatedTraining,
    meta: {
      title: 'P2P AI - Federated Training',
      requiresAuth: true
    }
  },
  {
    path: '/p2pai/local-training',
    name: 'P2PAILocalTraining',
    component: P2PAI.LocalTraining,
    meta: {
      title: 'P2P AI - Local Training',
      requiresAuth: true
    }
  },
  {
    path: '/p2pai/mpc-training',
    name: 'P2PAIMPCTraining',
    component: P2PAI.MPCTraining,
    meta: {
      title: 'P2P AI - MPC Training',
      requiresAuth: true
    }
  },
  {
    path: '/p2pai/datasets',
    name: 'P2PAIDatasetDashboard',
    component: P2PAI.DatasetDashboard,
    meta: {
      title: 'P2P AI - Dataset Management',
      requiresAuth: true
    }
  },
  {
    path: '/p2pai/models',
    name: 'P2PAIModelDashboard',
    component: P2PAI.ModelDashboard,
    meta: {
      title: 'P2P AI - Model Management',
      requiresAuth: true
    }
  },
  {
    path: '/p2pai/monitor',
    name: 'P2PAITrainingMonitor',
    component: P2PAI.TrainingMonitor,
    meta: {
      title: 'P2P AI - Training Monitor',
      requiresAuth: true
    }
  },
  {
    path: '/p2pai/overview',
    name: 'P2PAIProjectOverview',
    component: P2PAI.ProjectOverview,
    meta: {
      title: 'P2P AI - Project Overview',
      requiresAuth: true
    }
  },
  {
    path: '/p2pai/visualization/:projectId?',
    name: 'P2PAIProjectVisualization',
    component: P2PAI.ProjectVisualization,
    meta: {
      title: 'P2P AI - Project Visualization',
      requiresAuth: true
    }
  },

  // EdgeAI Routes
  {
    path: '/edgeai/login',
    name: 'EdgeAILogin',
    component: EdgeAI.Login,
    meta: { title: 'Edge AI - 登录' }
  },
  {
    path: '/edgeai/dashboard',
    name: 'EdgeAIDashboard', 
    component: EdgeAI.Dashboard,
    meta: {
      title: 'Edge AI - 仪表板',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/all-nodes',
    name: 'EdgeAIAllNodes',
    component: EdgeAI.AllNodes,
    meta: {
      title: 'Edge AI - 节点管理',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/create-project',
    name: 'EdgeAICreateProject',
    component: EdgeAI.CreateProject,
    meta: {
      title: 'Edge AI - 创建项目',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/project-manager',
    name: 'EdgeAIProjectManager',
    component: EdgeAI.ProjectManager,
    meta: {
      title: 'Edge AI - 项目管理',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/visualization/:projectId?',
    name: 'EdgeAIVisualization',
    component: EdgeAI.Visualization,
    meta: {
      title: 'Edge AI - 项目可视化',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/import-project',
    name: 'EdgeAIImportProject',
    component: EdgeAI.ImportProject,
    meta: {
      title: 'Edge AI - 导入项目',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/task-manager',
    name: 'EdgeAITaskManager',
    component: EdgeAI.TaskManager,
    meta: {
      title: 'Edge AI - 任务管理',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/performance-metrics',
    name: 'EdgeAIPerformanceMetrics',
    component: EdgeAI.PerformanceMetrics,
    meta: {
      title: 'Edge AI - 性能指标',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/system-logs',
    name: 'EdgeAISystemLogs',
    component: EdgeAI.SystemLogs,
    meta: {
      title: 'Edge AI - System Logs',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/model-management',
    name: 'EdgeAIModelManagement',
    component: EdgeAI.ModelManagement,
    meta: {
      title: 'Edge AI - Model Management',
      requiresAuth: true
    }
  },
  {
    path: '/edgeai/model-details/:id',
    name: 'EdgeAIModelDetails',
    component: EdgeAI.ModelDetails,
    meta: {
      title: 'Edge AI - Model Details',
      requiresAuth: true
    }
  },

  // Blockchain Routes
  {
    path: '/blockchain/login',
    name: 'BlockchainLogin',
    component: Blockchain.Login,
    meta: { title: '区块链 - 登录' }
  },
  {
    path: '/blockchain/dashboard',
    name: 'BlockchainDashboard',
    component: Blockchain.Dashboard,
    meta: {
      title: '区块链 - 仪表板',
      requiresAuth: true
    }
  },

  // Crypto Routes
  {
    path: '/crypto/login',
    name: 'CryptoLogin',
    component: Crypto.Login,
    meta: { title: '加密 - 登录' }
  },
  {
    path: '/crypto/dashboard',
    name: 'CryptoDashboard',
    component: Crypto.Dashboard,
    meta: {
      title: '加密 - 仪表板',
      requiresAuth: true
    }
  },

  // 404 fallback
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  // Update page title
  document.title = to.meta.title || 'FedMPC'
  
  // Auth guard - simplified for now
  if (to.meta.requiresAuth) {
    const isAuthenticated = localStorage.getItem('isAuthenticated')
    if (!isAuthenticated) {
      // Redirect to appropriate login based on module
      const module = to.path.split('/')[1]
      next(`/${module}/login`)
      return
    }
  }
  
  next()
})

export default router