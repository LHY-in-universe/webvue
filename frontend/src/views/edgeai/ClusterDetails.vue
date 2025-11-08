<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <Button 
              @click="$router.back()" 
              variant="ghost" 
              size="sm" 
              class="mr-4"
            >
              ← Back
            </Button>
            <ServerStackIcon class="h-8 w-8 text-blue-600 mr-3" />
            <div>
              <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                {{ cluster?.name || 'Cluster Details' }}
              </h1>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Cluster ID: {{ clusterId }}
              </p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600 dark:text-gray-400">Loading cluster details...</span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-8">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
              Failed to load cluster details
            </h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </div>
            <div class="mt-3">
              <Button @click="loadClusterDetails" variant="ghost" size="sm" class="text-red-800 dark:text-red-200 hover:bg-red-100 dark:hover:bg-red-800/30">
                Try again
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Cluster Details -->
      <template v-else-if="cluster">
        <!-- Header Section -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-8">
          <div class="flex items-start justify-between mb-6">
            <div class="flex items-center">
              <div 
                :class="getStatusDotColor(cluster.status)"
                class="w-4 h-4 rounded-full mr-4"
              ></div>
              <div>
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
                  {{ cluster.name }}
                </h1>
                <p class="text-gray-600 dark:text-gray-400 mt-1">
                  {{ cluster.description || 'No description available' }}
                </p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <span :class="getStatusBadgeColor(cluster.status)" class="px-3 py-1 rounded-full text-sm font-medium">
                {{ cluster.status }}
              </span>
              <span :class="getTypeBadgeColor(cluster.type)" class="px-3 py-1 rounded-full text-sm font-medium">
                {{ cluster.type }}
              </span>
            </div>
          </div>

          <!-- Cluster Control Buttons -->
          <div class="flex justify-between items-center mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
            <!-- Left side: Cluster Operations -->
            <div class="flex items-center space-x-3">
              <Button
                @click="handleStartCluster"
                :loading="startingCluster"
                variant="primary"
                size="sm"
              >
                <PlayCircleIcon class="w-4 h-4 mr-2" />
                Start Cluster
              </Button>

              <Button
                @click="handleStopCluster"
                :loading="stoppingCluster"
                variant="outline"
                size="sm"
                class="border-orange-300 text-orange-700 hover:bg-orange-50 dark:border-orange-700 dark:text-orange-400 dark:hover:bg-orange-900/20"
              >
                <StopCircleIcon class="w-4 h-4 mr-2" />
                Stop Cluster
              </Button>

              <Button
                @click="handleRestartCluster"
                :loading="restartingCluster"
                variant="outline"
                size="sm"
                class="border-blue-300 text-blue-700 hover:bg-blue-50 dark:border-blue-700 dark:text-blue-400 dark:hover:bg-blue-900/20"
              >
                <ArrowPathIcon class="w-4 h-4 mr-2" />
                Restart Cluster
              </Button>
            </div>

            <!-- Right side: Delete Cluster -->
            <Button
              @click="deleteCluster"
              :loading="deleting"
              variant="outline"
              size="sm"
              class="border-red-300 text-red-700 hover:bg-red-50 dark:border-red-700 dark:text-red-400 dark:hover:bg-red-900/20"
            >
              <TrashIcon class="w-4 h-4 mr-2" />
              Delete Cluster
            </Button>
          </div>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Nodes"
            :value="cluster.nodeCount || 0"
            :icon="ServerIcon"
            variant="primary"
            description="Cluster nodes"
          />
          <StatCard
            title="CPU Cores"
            :value="cluster.cpuCores || 0"
            :icon="CpuChipIcon"
            variant="info"
            description="Total CPU cores"
          />
          <StatCard
            title="Memory"
            :value="cluster.memory || 0"
            unit="GB"
            :icon="MemoryIcon"
            variant="warning"
            description="Total memory"
          />
          <StatCard
            title="GPU Count"
            :value="cluster.gpuCount || 0"
            :icon="CpuChipIcon"
            variant="success"
            description="GPU devices"
          />
        </div>

        <!-- Main Content -->
        <div class="space-y-8">
            <!-- Cluster Information -->
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Cluster Information</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Cluster ID</label>
                  <p class="text-gray-900 dark:text-white font-mono text-sm">{{ cluster.id }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Type</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.type }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Status</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.status }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Created</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.created }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Last Updated</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.lastUpdated }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-600 dark:text-gray-400">Active Projects</label>
                  <p class="text-gray-900 dark:text-white">{{ cluster.activeProjects || 0 }}</p>
                </div>
              </div>
            </div>

            <!-- Performance Metrics -->
            <div v-if="cluster.metrics" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Performance Metrics</h2>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="text-center">
                  <div class="text-3xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                    {{ (cluster.metrics.cpuUsage || 0).toFixed(1) }}%
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">CPU Usage</div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-2">
                    <div 
                      class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${cluster.metrics.cpuUsage || 0}%` }"
                    ></div>
                  </div>
                </div>
                <div class="text-center">
                  <div class="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">
                    {{ (cluster.metrics.memoryUsage || 0).toFixed(1) }}%
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">Memory Usage</div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-2">
                    <div 
                      class="bg-green-600 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${cluster.metrics.memoryUsage || 0}%` }"
                    ></div>
                  </div>
                </div>
                <div class="text-center">
                  <div class="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-2">
                    {{ (cluster.metrics.gpuUsage || 0).toFixed(1) }}%
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">GPU Usage</div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-2">
                    <div 
                      class="bg-purple-600 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${cluster.metrics.gpuUsage || 0}%` }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Cluster Nodes Section -->
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Cluster Nodes</h2>
                <div class="flex space-x-3">
                  <Button
                    @click="refreshNodes"
                    variant="outline"
                    size="sm"
                    :leftIcon="ArrowPathIcon"
                    :loading="nodesLoading"
                  >
                    Refresh
                  </Button>
                  <Button
                    @click="showAddNodeModal = true"
                    variant="primary"
                    size="sm"
                    :leftIcon="PlusIcon"
                    class="bg-blue-600 hover:bg-blue-700"
                  >
                    Add Node
                  </Button>
                </div>
              </div>

              <!-- Node Type Tabs -->
              <div class="mb-6">
                <div class="border-b border-gray-200 dark:border-gray-700">
                  <nav class="-mb-px flex space-x-8">
                    <button
                      v-for="nodeType in nodeTypes"
                      :key="nodeType.key"
                      @click="selectedNodeType = nodeType.key"
                      :class="[
                        'py-2 px-1 border-b-2 font-medium text-sm',
                        selectedNodeType === nodeType.key
                          ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                      ]"
                    >
                      {{ nodeType.label }} ({{ getNodesByType(nodeType.key).length }})
                    </button>
                  </nav>
                </div>
              </div>

              <!-- Loading State -->
              <div v-if="nodesLoading" class="flex justify-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>

              <!-- Empty State -->
              <div v-else-if="clusterNodes.length === 0" class="text-center py-8">
                <ServerIcon class="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No nodes found</h3>
                <p class="text-gray-600 dark:text-gray-400 mb-4">This cluster doesn't have any nodes yet.</p>
                <Button @click="showAddNodeModal = true" class="bg-blue-600 hover:bg-blue-700 text-white">
                  <PlusIcon class="w-4 h-4 mr-2" />
                  Add Node
                </Button>
              </div>

              <!-- Nodes Grid -->
              <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div
                  v-for="node in getNodesByType(selectedNodeType)" 
                  :key="node.id"
                  class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600"
                >
                  <div class="flex items-start justify-between mb-3">
                    <div class="flex items-center">
                      <div 
                        :class="getNodeStatusColor(node.status)"
                        class="w-3 h-3 rounded-full mr-3"
                      ></div>
                      <div>
                        <h3 class="font-medium text-gray-900 dark:text-white">{{ node.name }}</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400">{{ node.node_type || 'worker' }} • {{ node.status }}</p>
                      </div>
                    </div>
                    <span :class="getNodeTypeBadgeColor(node.node_type)" class="px-2 py-1 rounded-full text-xs font-medium">
                      {{ node.node_type || 'worker' }}
                    </span>
                  </div>
                  
                  <div class="space-y-2 text-sm">
                    <div class="flex justify-between">
                      <span class="text-gray-600 dark:text-gray-400">IP Address:</span>
                      <span class="font-mono text-gray-900 dark:text-white">{{ node.location }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-600 dark:text-gray-400">CPU Usage:</span>
                      <span class="text-gray-900 dark:text-white">{{ node.cpu_usage.toFixed(1) }}%</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-600 dark:text-gray-400">Memory:</span>
                      <span class="text-gray-900 dark:text-white">{{ node.memory_usage.toFixed(1) }}%</span>
                    </div>
                  </div>

                  <div class="flex justify-end space-x-2 mt-4">
                    <Button
                      @click="viewNodeDetails(node)"
                      variant="outline"
                      size="xs"
                    >
                      Details
                    </Button>
                    <Button
                      @click="removeNode(node)"
                      variant="ghost"
                      size="xs"
                      class="text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-red-900/20"
                    >
                      <TrashIcon class="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
        </div>
      </template>
    </div>

    <!-- Add Node Modal -->
    <Modal
      :isOpen="showAddNodeModal"
      @close="showAddNodeModal = false"
      title="Add Node to Cluster"
      size="md"
    >
      <form @submit.prevent="submitNewNode" class="space-y-4">
        <div>
          <label for="nodeIp" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            IPv4 Address *
          </label>
          <input
            id="nodeIp"
            v-model="newNodeData.ip"
            type="text"
            required
            placeholder="192.168.1.100"
            pattern="^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            Enter a unique IPv4 address. Make sure this IP is not already used by another node.
          </p>
        </div>

        <div>
          <label for="nodeName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Node Name
          </label>
          <input
            id="nodeName"
            v-model="newNodeData.name"
            type="text"
            placeholder="Enter node name (optional)"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div>
          <label for="nodeType" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Node Type *
          </label>
          <select
            id="nodeType"
            v-model="newNodeData.node_type"
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="center">Center Node</option>
            <option value="mpc">MPC Node</option>
            <option value="training">Training Node</option>
          </select>
        </div>

        <div class="flex justify-end space-x-3 pt-4">
          <Button
            type="button"
            @click="showAddNodeModal = false"
            variant="outline"
            size="sm"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            variant="primary"
            size="sm"
            class="bg-blue-600 hover:bg-blue-700 focus:ring-blue-500"
            :loading="addingNode"
            :disabled="addingNode"
          >
            {{ addingNode ? 'Adding...' : 'Add Node' }}
          </Button>
        </div>
      </form>
    </Modal>

    <!-- Node Details Modal -->
    <Modal
      :isOpen="showNodeDetailsModal"
      @close="showNodeDetailsModal = false"
      title="Node Details"
      size="lg"
    >
      <div v-if="selectedNode" class="space-y-6">
        <!-- Node Header -->
        <div class="flex items-start justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div class="flex items-center space-x-4">
            <div class="relative">
              <div :class="[
                'w-4 h-4 rounded-full',
                getNodeStatusColor(selectedNode.status)
              ]"></div>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedNode.name }}</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ selectedNode.node_type || 'worker' }} • {{ selectedNode.status }}</p>
            </div>
          </div>
          <span :class="getNodeTypeBadgeColor(selectedNode.node_type)" class="px-3 py-1 rounded-full text-sm font-medium">
            {{ selectedNode.node_type || 'worker' }}
          </span>
        </div>

        <!-- Node Information -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Basic Information</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Node ID:</span>
                <span class="font-mono">{{ selectedNode.id }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Name:</span>
                <span>{{ selectedNode.name }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Type:</span>
                <span class="capitalize">{{ selectedNode.node_type || 'worker' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">IP Address:</span>
                <span class="font-mono">{{ selectedNode.location }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Status:</span>
                <span class="capitalize">{{ selectedNode.status }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Last Seen:</span>
                <span>{{ new Date(selectedNode.last_seen).toLocaleString() }}</span>
              </div>
            </div>
          </div>

          <div>
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Resource Usage</h4>
            <div class="space-y-3">
              <div class="space-y-1">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500 dark:text-gray-400">CPU Usage:</span>
                  <span class="font-medium">{{ selectedNode.cpu_usage.toFixed(1) }}%</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="{
                      'bg-red-500': selectedNode.cpu_usage > 80,
                      'bg-yellow-500': selectedNode.cpu_usage > 60 && selectedNode.cpu_usage <= 80,
                      'bg-green-500': selectedNode.cpu_usage <= 60
                    }"
                    :style="{ width: `${selectedNode.cpu_usage}%` }"
                  ></div>
                </div>
              </div>

              <div class="space-y-1">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500 dark:text-gray-400">Memory Usage:</span>
                  <span class="font-medium">{{ selectedNode.memory_usage.toFixed(1) }}%</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="{
                      'bg-red-500': selectedNode.memory_usage > 80,
                      'bg-yellow-500': selectedNode.memory_usage > 60 && selectedNode.memory_usage <= 80,
                      'bg-blue-500': selectedNode.memory_usage <= 60
                    }"
                    :style="{ width: `${selectedNode.memory_usage}%` }"
                  ></div>
                </div>
              </div>

              <div v-if="selectedNode.gpu_usage > 0" class="space-y-1">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500 dark:text-gray-400">GPU Usage:</span>
                  <span class="font-medium">{{ selectedNode.gpu_usage.toFixed(1) }}%</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="{
                      'bg-red-500': selectedNode.gpu_usage > 80,
                      'bg-yellow-500': selectedNode.gpu_usage > 60 && selectedNode.gpu_usage <= 80,
                      'bg-purple-500': selectedNode.gpu_usage <= 60
                    }"
                    :style="{ width: `${selectedNode.gpu_usage}%` }"
                  ></div>
                </div>
              </div>

              <div class="space-y-1">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500 dark:text-gray-400">Active Tasks:</span>
                  <span class="font-medium">{{ selectedNode.active_tasks || 0 }}</span>
                </div>
              </div>

              <div class="space-y-1">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500 dark:text-gray-400">Uptime:</span>
                  <span class="font-medium">{{ selectedNode.uptime || '0h 0m' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
          <Button
            @click="removeNode(selectedNode)"
            variant="outline"
            size="sm"
            class="text-red-600 border-red-300 hover:bg-red-50 dark:text-red-400 dark:border-red-700 dark:hover:bg-red-900/20"
          >
            <TrashIcon class="w-4 h-4 mr-2" />
            Remove Node
          </Button>
          <Button
            @click="showNodeDetailsModal = false"
            variant="primary"
            size="sm"
          >
            Close
          </Button>
        </div>
      </div>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal
      :isOpen="showDeleteModal"
      @close="cancelDelete"
      title="Delete Node"
      size="md"
      :hideFooter="true"
    >
      <div v-if="nodeToDelete" class="space-y-4">
        <div class="flex items-center space-x-3 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center">
              <TrashIcon class="w-6 h-6 text-red-600 dark:text-red-400" />
            </div>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-medium text-red-900 dark:text-red-100">Confirm Node Deletion</h3>
            <p class="text-sm text-red-700 dark:text-red-300 mt-1">
              Are you sure you want to delete <strong>{{ nodeToDelete.name }}</strong>?
            </p>
          </div>
        </div>

        <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Node Details:</h4>
          <div class="space-y-1 text-sm text-gray-600 dark:text-gray-300">
            <div><strong>Name:</strong> {{ nodeToDelete.name }}</div>
            <div><strong>Type:</strong> {{ nodeToDelete.type }}</div>
            <div><strong>Status:</strong> {{ nodeToDelete.status }}</div>
            <div><strong>IP Address:</strong> {{ nodeToDelete.location }}</div>
          </div>
        </div>

        <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-3">
          <p class="text-sm text-yellow-800 dark:text-yellow-200">
            ⚠️ This action cannot be undone. The node will be permanently removed from the cluster.
          </p>
        </div>

        <div class="flex justify-end space-x-3 pt-4">
          <Button
            @click="cancelDelete"
            variant="outline"
            size="sm"
          >
            Cancel
          </Button>
          <Button
            @click="confirmDelete"
            variant="primary"
            size="sm"
            class="bg-red-600 hover:bg-red-700 focus:ring-red-500"
            :loading="deleting"
            :disabled="deleting"
          >
            {{ deleting ? 'Deleting...' : 'Delete Node' }}
          </Button>
        </div>
      </div>
    </Modal>

    <!-- Stop Cluster Confirmation Modal -->
    <Modal
      :isOpen="showStopConfirmModal"
      @close="cancelStopCluster"
      title="Stop Cluster"
      size="md"
      :hideFooter="true"
    >
      <div class="space-y-4">
        <div class="flex items-center space-x-3 p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-800">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-orange-100 dark:bg-orange-900 rounded-full flex items-center justify-center">
              <StopCircleIcon class="w-6 h-6 text-orange-600 dark:text-orange-400" />
            </div>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-medium text-orange-900 dark:text-orange-100">Confirm Cluster Stop</h3>
            <p class="text-sm text-orange-700 dark:text-orange-300 mt-1">
              Are you sure you want to stop <strong>{{ cluster?.name }}</strong>?
            </p>
          </div>
        </div>

        <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-3">
          <p class="text-sm text-yellow-800 dark:text-yellow-200">
            ⚠️ This will stop all running tasks on this cluster.
          </p>
        </div>

        <div class="flex justify-end space-x-3 pt-4">
          <Button
            @click="cancelStopCluster"
            variant="outline"
            size="sm"
          >
            Cancel
          </Button>
          <Button
            @click="confirmStopCluster"
            variant="primary"
            size="sm"
            class="bg-orange-600 hover:bg-orange-700 focus:ring-orange-500"
            :loading="stoppingCluster"
            :disabled="stoppingCluster"
          >
            {{ stoppingCluster ? 'Stopping...' : 'Stop Cluster' }}
          </Button>
        </div>
      </div>
    </Modal>

    <!-- Restart Cluster Confirmation Modal -->
    <Modal
      :isOpen="showRestartConfirmModal"
      @close="cancelRestartCluster"
      title="Restart Cluster"
      size="md"
      :hideFooter="true"
    >
      <div class="space-y-4">
        <div class="flex items-center space-x-3 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
              <ArrowPathIcon class="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-medium text-blue-900 dark:text-blue-100">Confirm Cluster Restart</h3>
            <p class="text-sm text-blue-700 dark:text-blue-300 mt-1">
              Are you sure you want to restart <strong>{{ cluster?.name }}</strong>?
            </p>
          </div>
        </div>

        <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-3">
          <p class="text-sm text-yellow-800 dark:text-yellow-200">
            ⚠️ This will stop and then start the cluster. All running tasks will be interrupted.
          </p>
        </div>

        <div class="flex justify-end space-x-3 pt-4">
          <Button
            @click="cancelRestartCluster"
            variant="outline"
            size="sm"
          >
            Cancel
          </Button>
          <Button
            @click="confirmRestartCluster"
            variant="primary"
            size="sm"
            class="bg-blue-600 hover:bg-blue-700 focus:ring-blue-500"
            :loading="restartingCluster"
            :disabled="restartingCluster"
          >
            {{ restartingCluster ? 'Restarting...' : 'Restart Cluster' }}
          </Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApiOptimization } from '@/composables/useApiOptimization'
import { useNotifications } from '@/composables/useNotifications'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import Button from '@/components/ui/Button.vue'
import StatCard from '@/components/ui/StatCard.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import Modal from '@/components/ui/Modal.vue'
import {
  ServerStackIcon,
  ServerIcon,
  CpuChipIcon,
  ArrowPathIcon,
  PlusIcon,
  TrashIcon,
  PlayCircleIcon,
  StopCircleIcon
} from '@heroicons/vue/24/outline'

// Memory icon (using CpuChipIcon as fallback)
const MemoryIcon = CpuChipIcon

const route = useRoute()
const router = useRouter()
const { cachedApiCall, clearCache } = useApiOptimization()
const { success, error: showError, confirm } = useNotifications()

// Get cluster ID from route params
const clusterId = computed(() => route.params.id)

// Reactive data
const loading = ref(false)
const nodesLoading = ref(false)
const deleting = ref(false)
const error = ref(null)
const cluster = ref(null)
const clusterNodes = ref([])
const refreshInterval = ref(null)

// Cluster operation states
const startingCluster = ref(false)
const stoppingCluster = ref(false)
const restartingCluster = ref(false)
const showStopConfirmModal = ref(false)
const showRestartConfirmModal = ref(false)

// Node management
const showAddNodeModal = ref(false)
const showNodeDetailsModal = ref(false)
const selectedNode = ref(null)
const addingNode = ref(false)
const selectedNodeType = ref('all')
const newNodeData = ref({
  ip: '',
  name: '',
  node_type: 'center'
})

// Node types configuration
const nodeTypes = ref([
  { key: 'all', label: 'All Nodes' },
  { key: 'center', label: 'Center' },
  { key: 'mpc', label: 'MPC' },
  { key: 'training', label: 'Training' }
])


// Utility functions
const getStatusDotColor = (status) => {
  const colors = {
    Active: 'bg-green-500',
    Inactive: 'bg-gray-500',
    Error: 'bg-red-500',
    Maintenance: 'bg-yellow-500'
  }
  return colors[status] || 'bg-gray-500'
}

const getStatusBadgeColor = (status) => {
  const colors = {
    Active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    Inactive: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    Error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    Maintenance: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
  }
  return colors[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

const getTypeBadgeColor = (type) => {
  const colors = {
    Training: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    Inference: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    Hybrid: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200'
  }
  return colors[type] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

// Node status color function
const getNodeStatusColor = (status) => {
  const colors = {
    online: 'bg-green-500',
    idle: 'bg-gray-500',
    training: 'bg-blue-500',
    offline: 'bg-gray-400',
    error: 'bg-red-500',
    Active: 'bg-green-500',
    Inactive: 'bg-gray-500',
    Error: 'bg-red-500',
    Maintenance: 'bg-yellow-500'
  }
  return colors[status] || 'bg-gray-500'
}


// Load cluster details
const loadClusterDetails = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('EdgeAIClusterDetails')
  loading.value = true
  error.value = null
  
  console.log('🔄 Loading cluster details for ID:', clusterId.value)
  
  // Validate cluster ID
  if (!clusterId.value || clusterId.value === 'undefined' || clusterId.value === undefined) {
    console.error('❌ Invalid cluster ID:', clusterId.value)
    error.value = 'Invalid cluster ID. Please check the URL and try again.'
    loading.value = false
    return
  }
  
  try {
    // Load cluster details
    const clusterResult = await cachedApiCall(`edgeai-cluster-${clusterId.value}`, 
      () => edgeaiService.clusters.getCluster(clusterId.value), 
      2 * 60 * 1000 // Cache for 2 minutes
    )
    
    console.log('📊 Cluster result:', clusterResult)

    if (clusterResult) {
      cluster.value = {
        id: clusterResult.id,
        name: clusterResult.name,
        description: clusterResult.description || 'No description available',
        type: clusterResult.type || 'Hybrid',
        status: clusterResult.status || 'Active',
        nodeCount: clusterResult.node_count || 0,
        cpuCores: clusterResult.cpu_cores || 0,
        memory: clusterResult.memory || 0,
        gpuCount: clusterResult.gpu_count || 0,
        activeProjects: clusterResult.active_projects || 0,
        activeProjectNames: clusterResult.active_project_names || [],
        metrics: clusterResult.metrics || null,
        created: clusterResult.created_time ? new Date(clusterResult.created_time).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
        lastUpdated: clusterResult.last_updated_time ? new Date(clusterResult.last_updated_time).toISOString().split('T')[0] : new Date().toISOString().split('T')[0]
      }
      console.log('📋 Mapped cluster:', cluster.value)
    } else {
      throw new Error('Cluster not found')
    }

    // Load cluster nodes
    await loadClusterNodes()

    pageMonitor.end({ success: true, clusterId: clusterId.value })
  } catch (err) {
    console.error('Failed to load cluster details:', err)
    error.value = err.message || 'Failed to load cluster details'
    pageMonitor.end({ success: false, error: err.message })
  } finally {
    loading.value = false
  }
}

// Load cluster nodes
const loadClusterNodes = async () => {
  nodesLoading.value = true
  
  try {
    const nodesResult = await cachedApiCall(`edgeai-cluster-nodes-${clusterId.value}`, 
      () => edgeaiService.nodes.getClusterNodes(clusterId.value), 
      1 * 60 * 1000 // Cache for 1 minute
    )
    
    if (nodesResult && Array.isArray(nodesResult)) {
      clusterNodes.value = nodesResult.map(node => ({
        id: node.id,
        name: node.name,
        node_type: node.node_type || 'worker',
        // 映射后端的state字段到前端的status字段
        status: node.status || node.state || 'idle',
        location: node.location || 'Unknown',
        cpu_usage: node.cpu_usage || 0,
        memory_usage: node.memory_usage || 0,
        gpu_usage: node.gpu_usage || 0,
        progress: node.progress || 0,
        last_seen: node.last_seen || new Date().toISOString(),
        project: node.project || 'No Project',
        uptime: node.uptime || '0h 0m',
        active_tasks: node.active_tasks || 0
      }))
    } else {
      clusterNodes.value = []
    }
  } catch (err) {
    console.error('Failed to load cluster nodes:', err)
    clusterNodes.value = []
  } finally {
    nodesLoading.value = false
  }
}

// Setup auto-refresh
const setupAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }

  refreshInterval.value = setInterval(async () => {
    if (!loading.value) {
      await loadClusterDetails()
    }
  }, 30 * 1000) // Refresh every 30 seconds
}


// Node-related functions
const refreshNodes = async () => {
  clearCache(`edgeai-cluster-nodes-${clusterId.value}`)
  await loadClusterNodes()
}

const submitNewNode = async () => {
  if (!newNodeData.value.ip.trim()) {
    showError('IPv4 address is required')
    return
  }

  // Validate IPv4 format with proper range checking
  const ipRegex = /^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$/
  if (!ipRegex.test(newNodeData.value.ip)) {
    showError('Please enter a valid IPv4 address (e.g., 192.168.1.100)')
    return
  }

  // Validate each octet is between 0-255
  const octets = newNodeData.value.ip.trim().split('.')
  const invalidOctet = octets.find(octet => {
    const num = parseInt(octet, 10)
    return isNaN(num) || num < 0 || num > 255
  })

  if (invalidOctet !== undefined) {
    showError('Each part of the IP address must be between 0 and 255')
    return
  }

  addingNode.value = true

  try {
    const result = await edgeaiService.nodes.createNodeInCluster(clusterId.value, {
      ip: newNodeData.value.ip.trim(),
      name: newNodeData.value.name.trim() || undefined,
      node_type: newNodeData.value.node_type
    })

    if (result) {
      // Reset form and close modal
      newNodeData.value = { ip: '', name: '', node_type: 'center' }
      showAddNodeModal.value = false

      // Clear cache and refresh node data
      clearCache(`edgeai-cluster-nodes-${clusterId.value}`)
      await loadClusterNodes()

      success('Node added successfully!')
    } else {
      showError('Failed to add node')
    }
  } catch (err) {
    console.error('Failed to add node:', err)

    // 处理不同的错误类型
    let errorMessage = 'Unknown error'

    if (err.response?.data?.detail) {
      // 后端返回的具体错误信息
      errorMessage = err.response.data.detail
    } else if (err.response?.status === 400) {
      errorMessage = 'Invalid request. Please check your input.'
    } else if (err.response?.status === 409) {
      errorMessage = 'Node with this IP address already exists.'
    } else if (err.message) {
      errorMessage = err.message
    }

    showError(`Failed to add node: ${errorMessage}`)
  } finally {
    addingNode.value = false
  }
}

const viewNodeDetails = (node) => {
  selectedNode.value = node
  showNodeDetailsModal.value = true
}

// 删除确认对话框状态
const showDeleteModal = ref(false)
const nodeToDelete = ref(null)

const removeNode = (node) => {
  console.log('🗑️ Preparing to delete node:', node)
  nodeToDelete.value = node
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (!nodeToDelete.value) return

  deleting.value = true
  try {
    console.log('🗑️ Deleting node:', nodeToDelete.value.id)
    await edgeaiService.nodes.deleteNode(nodeToDelete.value.id)
    await loadClusterNodes()
    success('Node removed successfully!')
    showDeleteModal.value = false
    nodeToDelete.value = null
  } catch (err) {
    console.error('Failed to remove node:', err)

    // 检查是否是404错误（节点已不存在）
    if (err.code === 'NOT_FOUND' || err.status === 404) {
      showError('This node no longer exists. Refreshing the list...')
      // 节点已经不存在，刷新列表并关闭对话框
      await loadClusterNodes()
      showDeleteModal.value = false
      nodeToDelete.value = null
    } else {
      showError(`Failed to remove node: ${err.error || err.message || 'Unknown error'}`)
    }
  } finally {
    deleting.value = false
  }
}

const cancelDelete = () => {
  showDeleteModal.value = false
  nodeToDelete.value = null
}

// Helper functions for node management
const getNodesByType = (type) => {
  if (type === 'all') {
    return clusterNodes.value
  }
  return clusterNodes.value.filter(node => node.node_type === type)
}

const getNodeTypeBadgeColor = (nodeType) => {
  const colors = {
    center: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    mpc: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    training: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    worker: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
  }
  return colors[nodeType] || colors.worker
}

// Delete cluster function
const deleteCluster = async () => {
  if (!confirm(`Are you sure you want to delete cluster "${cluster.value?.name}"? This action cannot be undone.`)) {
    return
  }

  deleting.value = true
  error.value = null

  try {
    console.log('🗑️ Deleting cluster:', clusterId.value)
    const result = await edgeaiService.clusters.deleteCluster(clusterId.value)

    // Show success message
    console.log('✅ Cluster deleted successfully:', result)

    // Clear cache to ensure fresh data on next load
    clearCache(`edgeai-cluster-${clusterId.value}`)
    clearCache('edgeai-clusters')

    // Redirect to cluster management page
    router.push('/edgeai/cluster-management')
  } catch (err) {
    console.error('❌ Failed to delete cluster:', err)
    error.value = err.message || 'Failed to delete cluster'

    // Show user-friendly error message
    showError(`Failed to delete cluster: ${err.message || 'Unknown error'}`)
  } finally {
    deleting.value = false
  }
}

// Cluster control functions
const handleStartCluster = async () => {
  startingCluster.value = true

  try {
    console.log('🚀 Starting cluster:', clusterId.value)
    const result = await edgeaiService.clusters.startCluster(clusterId.value)

    console.log('✅ Cluster started successfully:', result)
    success(`Cluster "${cluster.value?.name}" started successfully!`)

    // Clear cache and refresh cluster data
    clearCache(`edgeai-cluster-${clusterId.value}`)
    clearCache(`edgeai-cluster-nodes-${clusterId.value}`)
    await loadClusterDetails()
  } catch (err) {
    console.error('❌ Failed to start cluster:', err)
    showError(`Failed to start cluster: ${err.response?.data?.detail || err.message || 'Unknown error'}`)
  } finally {
    startingCluster.value = false
  }
}

const handleStopCluster = () => {
  showStopConfirmModal.value = true
}

const confirmStopCluster = async () => {
  stoppingCluster.value = true
  showStopConfirmModal.value = false

  try {
    console.log('⏸️ Stopping cluster:', clusterId.value)
    const result = await edgeaiService.clusters.stopCluster(clusterId.value)

    console.log('✅ Cluster stopped successfully:', result)
    success(`Cluster "${cluster.value?.name}" stopped successfully!`)

    // Clear cache and refresh cluster data
    clearCache(`edgeai-cluster-${clusterId.value}`)
    clearCache(`edgeai-cluster-nodes-${clusterId.value}`)
    await loadClusterDetails()
  } catch (err) {
    console.error('❌ Failed to stop cluster:', err)
    showError(`Failed to stop cluster: ${err.response?.data?.detail || err.message || 'Unknown error'}`)
  } finally {
    stoppingCluster.value = false
  }
}

const cancelStopCluster = () => {
  showStopConfirmModal.value = false
}

const handleRestartCluster = () => {
  showRestartConfirmModal.value = true
}

const confirmRestartCluster = async () => {
  restartingCluster.value = true
  showRestartConfirmModal.value = false

  try {
    console.log('🔄 Restarting cluster:', clusterId.value)
    const result = await edgeaiService.clusters.restartCluster(clusterId.value)

    console.log('✅ Cluster restarted successfully:', result)
    success(`Cluster "${cluster.value?.name}" restarted successfully!`)

    // Clear cache and refresh cluster data
    clearCache(`edgeai-cluster-${clusterId.value}`)
    clearCache(`edgeai-cluster-nodes-${clusterId.value}`)
    await loadClusterDetails()
  } catch (err) {
    console.error('❌ Failed to restart cluster:', err)
    showError(`Failed to restart cluster: ${err.response?.data?.detail || err.message || 'Unknown error'}`)
  } finally {
    restartingCluster.value = false
  }
}

const cancelRestartCluster = () => {
  showRestartConfirmModal.value = false
}


// Component lifecycle
onMounted(async () => {
  // Wait for route params to be resolved
  await new Promise(resolve => setTimeout(resolve, 0))
  
  // Double check that clusterId is valid before loading
  if (clusterId.value && clusterId.value !== 'undefined') {
    await loadClusterDetails()
    setupAutoRefresh()
  } else {
    console.error('❌ Cluster ID not available on mount:', clusterId.value)
    error.value = 'Invalid cluster ID. Please check the URL and try again.'
  }
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  clearCache()
})
</script>
