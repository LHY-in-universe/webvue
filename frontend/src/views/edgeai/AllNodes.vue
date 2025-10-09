<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navigation -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            <ServerIcon class="h-8 w-8 text-green-600 mr-3" />
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              Edge Node Management
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <Button
              @click="toggleAutoRefresh"
              variant="outline"
              size="sm"
              :class="{
                'text-green-600 border-green-600 dark:text-green-400 dark:border-green-400': autoRefreshEnabled,
                'text-gray-600 border-gray-300 dark:text-gray-400 dark:border-gray-600': !autoRefreshEnabled
              }"
            >
              {{ autoRefreshEnabled ? 'Auto-refresh ON' : 'Auto-refresh OFF' }}
            </Button>

            <Button
              @click="refreshNodes"
              variant="outline"
              size="sm"
              :leftIcon="ArrowPathIcon"
              :loading="refreshing"
            >
              Refresh
            </Button>
            <Button
              @click="toggleTheme"
              variant="ghost"
              size="sm"
              iconOnly
              :leftIcon="themeStore.isDark ? SunIcon : MoonIcon"
            />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Statistics Overview -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Nodes"
          :value="totalNodes"
          :icon="ServerIcon"
          variant="primary"
          description="All registered nodes"
          animated
        />
        
        <StatCard
          title="Online Nodes"
          :value="onlineNodes"
          :icon="CheckCircleIcon"
          variant="success"
          description="Currently connected"
          animated
        />
        
        <StatCard
          title="Training Nodes"
          :value="trainingNodes"
          :icon="CpuChipIcon"
          variant="info"
          description="Actively training"
          animated
        />
        
        <StatCard
          title="Avg Load"
          :value="averageLoad"
          unit="%"
          :icon="ChartBarIcon"
          variant="warning"
          description="System utilization"
          animated
        />
      </div>

      <!-- Filters and Search -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-8">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0 sm:space-x-4">
          <div class="flex flex-1 items-center space-x-4">
            <div class="relative flex-1 max-w-md">
              <MagnifyingGlassIcon class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                :value="searchQuery"
                @input="onSearchInput"
                @focus="onSearchFocus"
                @blur="onSearchBlur"
                type="text"
                placeholder="Search nodes by name, ID, location, or project..."
                class="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500 text-center placeholder:text-center"
                autocomplete="off"
              />

              <!-- Search Suggestions -->
              <div
                v-if="showSearchSuggestions"
                class="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg z-10 max-h-48 overflow-y-auto"
              >
                <div
                  v-for="suggestion in searchSuggestions"
                  :key="suggestion"
                  @click="selectSuggestion(suggestion)"
                  class="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer text-sm text-gray-900 dark:text-white border-b border-gray-100 dark:border-gray-700 last:border-b-0"
                >
                  {{ suggestion }}
                </div>
              </div>
            </div>
            
            <select
              v-model="statusFilter"
              class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
            >
              <option value="">All Status</option>
              <option value="online">Online</option>
              <option value="training">Training</option>
              <option value="idle">Idle</option>
              <option value="offline">Offline</option>
              <option value="error">Error</option>
            </select>

            <select
              v-model="locationFilter"
              class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
            >
              <option value="">All Locations</option>
              <option v-for="location in uniqueLocations" :key="location" :value="location">
                {{ location }}
              </option>
            </select>

          </div>
          
          <div class="flex items-center space-x-3">
            <Button
              @click="selectAllNodes"
              variant="outline"
              size="sm"
              v-if="filteredNodes.length > 0"
            >
              Select All
            </Button>

            <Button
              @click="clearSelection"
              variant="outline"
              size="sm"
              v-if="selectedNodes.size > 0"
            >
              Clear ({{ selectedNodes.size }})
            </Button>

            <Button
              @click="addNewNode"
              variant="primary"
              size="sm"
              :leftIcon="PlusIcon"
              class="bg-green-600 hover:bg-green-700 focus:ring-green-500"
            >
              Add Node
            </Button>

            <Button
              @click="exportNodes"
              variant="outline"
              size="sm"
              :leftIcon="ArrowDownTrayIcon"
              :loading="exportingNodes"
              :disabled="exportingNodes"
            >
              {{ exportingNodes ? 'Exporting...' : 'Export' }}
            </Button>
          </div>
        </div>
      </div>

      <!-- Nodes Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="node in filteredNodes"
          :key="node.id"
          class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow cursor-pointer relative"
          @click="selectNode(node)"
          :class="{
            'ring-2 ring-green-500 border-green-500': selectedNode?.id === node.id,
            'ring-2 ring-blue-500 border-blue-500': isNodeSelected(node.id)
          }"
        >
          <!-- Selection checkbox -->
          <div class="absolute top-4 right-4">
            <input
              type="checkbox"
              :checked="isNodeSelected(node.id)"
              @click.stop="toggleNodeSelection(node.id)"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
            />
          </div>
          <!-- Node Header -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center space-x-3 flex-1 min-w-0">
              <div class="relative flex-shrink-0">
                <div :class="[
                  'w-3 h-3 rounded-full',
                  getStatusColor(node.status)
                ]"></div>
                <!-- Pulsing indicator for operations -->
                <div
                  v-if="isNodeOperationLoading(node.id, 'connecting') || isNodeOperationLoading(node.id, 'disconnecting')"
                  class="absolute inset-0 w-3 h-3 rounded-full bg-blue-500 animate-ping opacity-75"
                ></div>
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white truncate" :title="node.name">{{ node.name }}</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400 truncate" :title="node.id">{{ node.id }}</p>
              </div>
            </div>
            <span :class="[
              'px-2 py-1 rounded-full text-xs font-medium flex-shrink-0 ml-2',
              getStatusBadgeColor(node.status)
            ]">
              {{ isNodeOperationLoading(node.id, 'connecting') ? 'Connecting...' :
                 isNodeOperationLoading(node.id, 'disconnecting') ? 'Disconnecting...' :
                 node.status }}
            </span>
          </div>

          <!-- Node Metrics -->
          <div class="space-y-3">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600 dark:text-gray-400">CPU Usage:</span>
              <span class="font-medium" :class="{
                'text-red-600 dark:text-red-400': node.cpuUsage > 80,
                'text-yellow-600 dark:text-yellow-400': node.cpuUsage > 60 && node.cpuUsage <= 80,
                'text-green-600 dark:text-green-400': node.cpuUsage <= 60
              }">{{ node.cpuUsage.toFixed(2) }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                class="h-2 rounded-full transition-all duration-300"
                :class="{
                  'bg-red-500': node.cpuUsage > 80,
                  'bg-yellow-500': node.cpuUsage > 60 && node.cpuUsage <= 80,
                  'bg-green-500': node.cpuUsage <= 60
                }"
                :style="{ width: `${node.cpuUsage}%` }"
              ></div>
            </div>

            <div class="flex justify-between text-sm">
              <span class="text-gray-600 dark:text-gray-400">Memory:</span>
              <span class="font-medium" :class="{
                'text-red-600 dark:text-red-400': node.memoryUsage > 80,
                'text-yellow-600 dark:text-yellow-400': node.memoryUsage > 60 && node.memoryUsage <= 80,
                'text-blue-600 dark:text-blue-400': node.memoryUsage <= 60
              }">{{ node.memoryUsage.toFixed(2) }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                class="h-2 rounded-full transition-all duration-300"
                :class="{
                  'bg-red-500': node.memoryUsage > 80,
                  'bg-yellow-500': node.memoryUsage > 60 && node.memoryUsage <= 80,
                  'bg-blue-500': node.memoryUsage <= 60
                }"
                :style="{ width: `${node.memoryUsage}%` }"
              ></div>
            </div>

            <!-- GPU Usage if available -->
            <div v-if="node.gpuUsage > 0" class="flex justify-between text-sm">
              <span class="text-gray-600 dark:text-gray-400">GPU Usage:</span>
              <span class="font-medium" :class="{
                'text-red-600 dark:text-red-400': node.gpuUsage > 80,
                'text-yellow-600 dark:text-yellow-400': node.gpuUsage > 60 && node.gpuUsage <= 80,
                'text-purple-600 dark:text-purple-400': node.gpuUsage <= 60
              }">{{ node.gpuUsage.toFixed(2) }}%</span>
            </div>
            <div v-if="node.gpuUsage > 0" class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                class="h-2 rounded-full transition-all duration-300"
                :class="{
                  'bg-red-500': node.gpuUsage > 80,
                  'bg-yellow-500': node.gpuUsage > 60 && node.gpuUsage <= 80,
                  'bg-purple-500': node.gpuUsage <= 60
                }"
                :style="{ width: `${node.gpuUsage}%` }"
              ></div>
            </div>

            <div class="grid grid-cols-2 gap-4 text-sm pt-2">
              <div>
                <span class="text-gray-600 dark:text-gray-400">Tasks:</span>
                <span class="font-medium ml-1">{{ node.activeTasks }}</span>
              </div>
              <div>
                <span class="text-gray-600 dark:text-gray-400">Uptime:</span>
                <span class="font-medium ml-1">{{ node.uptime }}</span>
              </div>
            </div>

            <div class="text-xs text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-200 dark:border-gray-700">
              <div>Location: {{ node.location }}</div>
              <div>Last seen: {{ node.lastSeen }}</div>
            </div>
          </div>

          <!-- Node Actions -->
          <div class="flex justify-end space-x-2 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <Button
              @click.stop="connectToNode(node)"
              variant="outline"
              size="xs"
              :disabled="isNodeOperationLoading(node.id, 'connecting') || isNodeOperationLoading(node.id, 'disconnecting')"
              :loading="isNodeOperationLoading(node.id, 'connecting') || isNodeOperationLoading(node.id, 'disconnecting')"
            >
              {{ isNodeOperationLoading(node.id, 'connecting') ? 'Connecting...' :
                 isNodeOperationLoading(node.id, 'disconnecting') ? 'Disconnecting...' :
                 (node.status === 'online' || node.status === 'training' || node.status === 'idle') ? 'Disconnect' : 'Connect' }}
            </Button>
            <Button
              @click.stop="showNodeDetails(node)"
              variant="primary"
              size="xs"
            >
              Details
            </Button>
            <Button
              @click.stop="confirmDeleteNode(node)"
              variant="ghost"
              size="xs"
              class="text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-red-900/20"
              :disabled="isNodeOperationLoading(node.id, 'deleting')"
              :loading="isNodeOperationLoading(node.id, 'deleting')"
            >
              <TrashIcon class="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredNodes.length === 0" class="text-center py-12">
        <ServerIcon class="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No nodes found</h3>
        <p class="text-gray-500 dark:text-gray-400 mb-6">
          {{ searchQuery || statusFilter || locationFilter ? 'Try adjusting your filters' : 'Start by adding your first edge node' }}
        </p>
        <Button
          @click="addNewNode"
          variant="primary"
          :leftIcon="PlusIcon"
          class="bg-green-600 hover:bg-green-700 focus:ring-green-500"
        >
          Add First Node
        </Button>
      </div>
    </div>

    <!-- Node Details Modal -->
    <Modal
      :isOpen="showDetailsModal"
      @close="showDetailsModal = false"
      title="Node Details"
      size="xl"
    >
      <div v-if="selectedNode" class="space-y-6">
        <!-- Node Header -->
        <div class="flex items-start justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div class="flex items-center space-x-4">
            <div class="relative">
              <div :class="[
                'w-4 h-4 rounded-full',
                getStatusColor(selectedNode.status)
              ]"></div>
              <div
                v-if="isNodeOperationLoading(selectedNode.id, 'connecting') || isNodeOperationLoading(selectedNode.id, 'disconnecting')"
                class="absolute inset-0 w-4 h-4 rounded-full bg-blue-500 animate-ping opacity-75"
              ></div>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedNode.name }}</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ selectedNode.id }} • {{ selectedNode.location }}</p>
            </div>
          </div>
          <span :class="[
            'px-3 py-1 rounded-full text-sm font-medium',
            getStatusBadgeColor(selectedNode.status)
          ]">
            {{ selectedNode.status }}
          </span>
        </div>

        <!-- Tabs -->
        <div class="border-b border-gray-200 dark:border-gray-700">
          <nav class="-mb-px flex space-x-8">
            <button
              @click="activeDetailsTab = 'overview'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeDetailsTab === 'overview'
                  ? 'border-green-500 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
            >
              Overview
            </button>
            <button
              @click="activeDetailsTab = 'performance'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeDetailsTab === 'performance'
                  ? 'border-green-500 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
            >
              Performance
            </button>
            <button
              @click="activeDetailsTab = 'hardware'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeDetailsTab === 'hardware'
                  ? 'border-green-500 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
            >
              Hardware
            </button>
            <button
              @click="activeDetailsTab = 'activity'"
              :class="[
                'py-2 px-1 border-b-2 font-medium text-sm',
                activeDetailsTab === 'activity'
                  ? 'border-green-500 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
              ]"
            >
              Activity
            </button>
          </nav>
        </div>

        <!-- Tab Content -->
        <div class="min-h-96">
          <!-- Overview Tab -->
          <div v-if="activeDetailsTab === 'overview'" class="space-y-6">
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
                    <span class="capitalize">{{ selectedNode.type }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Location:</span>
                    <span>{{ selectedNode.location }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Project:</span>
                    <span>{{ selectedNode.project }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Last Seen:</span>
                    <span>{{ selectedNode.lastSeen }}</span>
                  </div>
                </div>
              </div>

              <div>
                <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Current Status</h4>
                <div class="space-y-3">
                  <div class="space-y-1">
                    <div class="flex justify-between text-sm">
                      <span class="text-gray-500 dark:text-gray-400">Active Tasks:</span>
                      <span class="font-medium">{{ selectedNode.activeTasks }}</span>
                    </div>
                  </div>

                  <div class="space-y-1">
                    <div class="flex justify-between text-sm">
                      <span class="text-gray-500 dark:text-gray-400">Uptime:</span>
                      <span class="font-medium">{{ selectedNode.uptime }}</span>
                    </div>
                  </div>

                  <div v-if="selectedNode.currentEpoch" class="space-y-1">
                    <div class="flex justify-between text-sm">
                      <span class="text-gray-500 dark:text-gray-400">Training Progress:</span>
                      <span class="font-medium">{{ selectedNode.currentEpoch }}/{{ selectedNode.totalEpochs }}</span>
                    </div>
                    <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        class="bg-blue-500 h-2 rounded-full transition-all duration-300"
                        :style="{ width: `${(selectedNode.currentEpoch / selectedNode.totalEpochs) * 100}%` }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Performance Tab -->
          <div v-if="activeDetailsTab === 'performance'" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <!-- CPU Usage -->
              <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <h5 class="font-medium text-gray-900 dark:text-white mb-2">CPU Usage</h5>
                <div class="text-2xl font-bold" :class="{
                  'text-red-600 dark:text-red-400': selectedNode.cpuUsage > 80,
                  'text-yellow-600 dark:text-yellow-400': selectedNode.cpuUsage > 60 && selectedNode.cpuUsage <= 80,
                  'text-green-600 dark:text-green-400': selectedNode.cpuUsage <= 60
                }">{{ selectedNode.cpuUsage }}%</div>
                <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mt-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="{
                      'bg-red-500': selectedNode.cpuUsage > 80,
                      'bg-yellow-500': selectedNode.cpuUsage > 60 && selectedNode.cpuUsage <= 80,
                      'bg-green-500': selectedNode.cpuUsage <= 60
                    }"
                    :style="{ width: `${selectedNode.cpuUsage}%` }"
                  ></div>
                </div>
              </div>

              <!-- Memory Usage -->
              <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <h5 class="font-medium text-gray-900 dark:text-white mb-2">Memory Usage</h5>
                <div class="text-2xl font-bold" :class="{
                  'text-red-600 dark:text-red-400': selectedNode.memoryUsage > 80,
                  'text-yellow-600 dark:text-yellow-400': selectedNode.memoryUsage > 60 && selectedNode.memoryUsage <= 80,
                  'text-blue-600 dark:text-blue-400': selectedNode.memoryUsage <= 60
                }">{{ selectedNode.memoryUsage }}%</div>
                <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mt-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="{
                      'bg-red-500': selectedNode.memoryUsage > 80,
                      'bg-yellow-500': selectedNode.memoryUsage > 60 && selectedNode.memoryUsage <= 80,
                      'bg-blue-500': selectedNode.memoryUsage <= 60
                    }"
                    :style="{ width: `${selectedNode.memoryUsage}%` }"
                  ></div>
                </div>
              </div>

              <!-- GPU Usage -->
              <div v-if="selectedNode.gpuUsage > 0" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <h5 class="font-medium text-gray-900 dark:text-white mb-2">GPU Usage</h5>
                <div class="text-2xl font-bold" :class="{
                  'text-red-600 dark:text-red-400': selectedNode.gpuUsage > 80,
                  'text-yellow-600 dark:text-yellow-400': selectedNode.gpuUsage > 60 && selectedNode.gpuUsage <= 80,
                  'text-purple-600 dark:text-purple-400': selectedNode.gpuUsage <= 60
                }">{{ selectedNode.gpuUsage }}%</div>
                <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mt-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="{
                      'bg-red-500': selectedNode.gpuUsage > 80,
                      'bg-yellow-500': selectedNode.gpuUsage > 60 && selectedNode.gpuUsage <= 80,
                      'bg-purple-500': selectedNode.gpuUsage <= 60
                    }"
                    :style="{ width: `${selectedNode.gpuUsage}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Hardware Tab -->
          <div v-if="activeDetailsTab === 'hardware'" class="space-y-6">
            <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
              <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Hardware Specifications</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-3">
                  <div>
                    <span class="text-sm text-gray-500 dark:text-gray-400">Processor</span>
                    <div class="font-medium">{{ selectedNode.hardware.cpu }}</div>
                  </div>
                  <div>
                    <span class="text-sm text-gray-500 dark:text-gray-400">Memory</span>
                    <div class="font-medium">{{ selectedNode.hardware.memory }}</div>
                  </div>
                </div>
                <div class="space-y-3">
                  <div>
                    <span class="text-sm text-gray-500 dark:text-gray-400">Storage</span>
                    <div class="font-medium">{{ selectedNode.hardware.storage }}</div>
                  </div>
                  <div>
                    <span class="text-sm text-gray-500 dark:text-gray-400">Graphics</span>
                    <div class="font-medium">{{ selectedNode.hardware.gpu || 'Not available' }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Activity Tab -->
          <div v-if="activeDetailsTab === 'activity'" class="space-y-4">
            <h4 class="text-lg font-medium text-gray-900 dark:text-white">Recent Activity</h4>
            <div class="space-y-3 max-h-80 overflow-y-auto">
              <div
                v-for="activity in selectedNode.recentActivity"
                :key="activity.id"
                class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg"
              >
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <div class="font-medium text-gray-900 dark:text-white">{{ activity.message }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ activity.time }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
          <Button
            @click="connectToNode(selectedNode)"
            variant="outline"
            size="sm"
            :disabled="isNodeOperationLoading(selectedNode.id, 'connecting') || isNodeOperationLoading(selectedNode.id, 'disconnecting')"
            :loading="isNodeOperationLoading(selectedNode.id, 'connecting') || isNodeOperationLoading(selectedNode.id, 'disconnecting')"
          >
            {{ isNodeOperationLoading(selectedNode.id, 'connecting') ? 'Connecting...' :
               isNodeOperationLoading(selectedNode.id, 'disconnecting') ? 'Disconnecting...' :
               (selectedNode.status === 'online' || selectedNode.status === 'training' || selectedNode.status === 'idle') ? 'Disconnect' : 'Connect' }}
          </Button>
          <Button
            @click="showDetailsModal = false"
            variant="primary"
            size="sm"
          >
            Close
          </Button>
        </div>
      </div>
    </Modal>

    <!-- Add Node Modal -->
    <Modal
      :isOpen="showAddNodeModal"
      @close="showAddNodeModal = false"
      title="Add New Node"
      size="md"
    >
      <form @submit.prevent="submitNewNode" class="space-y-4">
        <div>
          <label for="nodeName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Node Name *
          </label>
          <input
            id="nodeName"
            v-model="newNodeData.name"
            type="text"
            required
            placeholder="Enter node name"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>

        <div>
          <label for="nodeLocation" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Location
          </label>
          <input
            id="nodeLocation"
            v-model="newNodeData.location"
            type="text"
            placeholder="Enter node location"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>

        <div>
          <label for="nodeType" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Node Type
          </label>
          <select
            id="nodeType"
            v-model="newNodeData.node_type"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="edge">Edge Node</option>
            <option value="control">Control Node</option>
            <option value="compute">Compute Node</option>
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
            class="bg-green-600 hover:bg-green-700 focus:ring-green-500"
            :loading="addingNode"
            :disabled="addingNode"
          >
            {{ addingNode ? 'Adding...' : 'Add Node' }}
          </Button>
        </div>
      </form>
    </Modal>

    <!-- Floating Batch Actions -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="transform translate-y-full opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform translate-y-full opacity-0"
    >
      <div
        v-if="showBatchActions"
        class="fixed bottom-6 left-1/2 transform -translate-x-1/2 z-50"
      >
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-2xl border border-gray-200 dark:border-gray-700 px-6 py-4">
          <div class="flex items-center space-x-4">
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ selectedNodes.size }} node(s) selected
            </span>

            <div class="flex space-x-2">
              <Button
                @click="batchConnectNodes"
                variant="outline"
                size="sm"
                :loading="batchOperationLoading"
                :disabled="batchOperationLoading"
              >
                Toggle Connection
              </Button>

              <Button
                @click="batchRestartNodes"
                variant="outline"
                size="sm"
                :loading="batchOperationLoading"
                :disabled="batchOperationLoading"
              >
                Restart All
              </Button>

              <Button
                @click="confirmBatchDeleteNodes"
                variant="outline"
                size="sm"
                class="text-red-600 border-red-300 hover:bg-red-50 dark:text-red-400 dark:border-red-600 dark:hover:bg-red-900/20"
                :loading="batchOperationLoading"
                :disabled="batchOperationLoading"
              >
                Delete Selected
              </Button>

              <Button
                @click="clearSelection"
                variant="outline"
                size="sm"
                :disabled="batchOperationLoading"
              >
                Cancel
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Delete Confirmation Modal -->
    <Modal
      :isOpen="showDeleteModal"
      @close="showDeleteModal = false"
      title="Delete Node"
      size="md"
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
              Are you sure you want to delete <strong>{{ nodeToDelete.name }}</strong>? This action cannot be undone.
            </p>
          </div>
        </div>

        <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Node Details:</h4>
          <div class="space-y-1 text-sm text-gray-600 dark:text-gray-300">
            <div><strong>ID:</strong> {{ nodeToDelete.id }}</div>
            <div><strong>Name:</strong> {{ nodeToDelete.name }}</div>
            <div><strong>Type:</strong> {{ nodeToDelete.type }}</div>
            <div><strong>Status:</strong> {{ nodeToDelete.status }}</div>
            <div><strong>Location:</strong> {{ nodeToDelete.location }}</div>
          </div>
        </div>

        <div class="flex justify-end space-x-3 pt-4">
          <Button
            @click="showDeleteModal = false"
            variant="outline"
            size="sm"
          >
            Cancel
          </Button>
          <Button
            @click="deleteNode"
            variant="primary"
            size="sm"
            class="bg-red-600 hover:bg-red-700 focus:ring-red-500"
            :loading="isNodeOperationLoading(nodeToDelete.id, 'deleting')"
            :disabled="isNodeOperationLoading(nodeToDelete.id, 'deleting')"
          >
            {{ isNodeOperationLoading(nodeToDelete.id, 'deleting') ? 'Deleting...' : 'Delete Node' }}
          </Button>
        </div>
      </div>
    </Modal>

    <!-- Batch Delete Confirmation Modal -->
    <Modal
      :isOpen="showBatchDeleteModal"
      @close="showBatchDeleteModal = false"
      title="Delete Multiple Nodes"
      size="md"
    >
      <div class="space-y-4">
        <div class="flex items-center space-x-3 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center">
              <TrashIcon class="w-6 h-6 text-red-600 dark:text-red-400" />
            </div>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-medium text-red-900 dark:text-red-100">Confirm Batch Deletion</h3>
            <p class="text-sm text-red-700 dark:text-red-300 mt-1">
              Are you sure you want to delete <strong>{{ selectedNodes.size }} node(s)</strong>? This action cannot be undone.
            </p>
          </div>
        </div>

        <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Selected Nodes:</h4>
          <div class="space-y-1 text-sm text-gray-600 dark:text-gray-300 max-h-32 overflow-y-auto">
            <div v-for="nodeId in Array.from(selectedNodes)" :key="nodeId" class="flex justify-between">
              <span>{{ nodes.find(n => n.id === nodeId)?.name || nodeId }}</span>
              <span class="text-gray-500">{{ nodes.find(n => n.id === nodeId)?.status || 'Unknown' }}</span>
            </div>
          </div>
        </div>

        <div class="flex justify-end space-x-3 pt-4">
          <Button
            @click="showBatchDeleteModal = false"
            variant="outline"
            size="sm"
          >
            Cancel
          </Button>
          <Button
            @click="batchDeleteNodes"
            variant="primary"
            size="sm"
            class="bg-red-600 hover:bg-red-700 focus:ring-red-500"
            :loading="batchOperationLoading"
            :disabled="batchOperationLoading"
          >
            {{ batchOperationLoading ? 'Deleting...' : `Delete ${selectedNodes.size} Node(s)` }}
          </Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'
import { useEdgeAIStore } from '@/stores/edgeai'
import Button from '@/components/ui/Button.vue'
import StatCard from '@/components/ui/StatCard.vue'
import Modal from '@/components/ui/Modal.vue'
import { 
  ServerIcon,
  ArrowLeftIcon,
  SunIcon,
  MoonIcon,
  CheckCircleIcon,
  CpuChipIcon,
  ChartBarIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  ArrowDownTrayIcon,
  ArrowPathIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const themeStore = useThemeStore()
const uiStore = useUIStore()
const edgeaiStore = useEdgeAIStore()

const refreshing = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const locationFilter = ref('')
const selectedNode = ref(null)
const showDetailsModal = ref(false)
const showAddNodeModal = ref(false)
const activeDetailsTab = ref('overview')
const addingNode = ref(false)
const exportingNodes = ref(false)
const nodeOperations = ref({}) // Track loading states for individual nodes
const selectedNodes = ref(new Set()) // Track selected nodes for batch operations
const batchOperationLoading = ref(false)
const showBatchActions = ref(false)
const autoRefreshEnabled = ref(true)
const refreshInterval = ref(null)
const showSearchSuggestions = ref(false)
const searchSuggestions = ref([])
const newNodeData = ref({
  name: '',
  location: '',
  node_type: 'edge'
})

// Delete related state
const showDeleteModal = ref(false)
const showBatchDeleteModal = ref(false)
const nodeToDelete = ref(null)

// Use nodes from EdgeAI store
const nodes = computed(() => edgeaiStore.nodes.map(node => ({
  ...node,
  // Add additional fields for UI that might not be in store
  hardware: node.hardware || {
    cpu: 'Intel Xeon E5-2670 v3',
    memory: '32GB DDR4',
    storage: '1TB SSD',
    gpu: node.gpuUsage > 0 ? 'NVIDIA Tesla V100' : null
  },
  recentActivity: node.recentActivity || [
    { id: 1, message: 'Training task started', time: '2 minutes ago' },
    { id: 2, message: 'Model checkpoint saved', time: '15 minutes ago' },
    { id: 3, message: 'Node connected to network', time: '1 hour ago' }
  ],
  activeTasks: node.activeTasks || (node.status === 'training' ? Math.floor(Math.random() * 5) + 1 : 0),
  uptime: node.uptime || `${Math.floor(Math.random() * 720) + 24}h ${Math.floor(Math.random() * 60)}m`
})))

// Computed properties using store data

// Computed properties
const filteredNodes = computed(() => {
  let filtered = nodes.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(node => 
      node.name.toLowerCase().includes(query) || 
      node.id.toLowerCase().includes(query)
    )
  }

  if (statusFilter.value) {
    filtered = filtered.filter(node => node.status === statusFilter.value)
  }

  if (locationFilter.value) {
    filtered = filtered.filter(node => node.location === locationFilter.value)
  }

  return filtered
})

const totalNodes = computed(() => nodes.value.length)
const onlineNodes = computed(() => nodes.value.filter(n => n.status === 'online' || n.status === 'training' || n.status === 'idle').length)
const trainingNodes = computed(() => nodes.value.filter(n => n.status === 'training').length)
const averageLoad = computed(() => {
  const activeNodes = nodes.value.filter(n => n.status !== 'offline' && n.status !== 'error')
  if (activeNodes.length === 0) return "0.00"
  const totalLoad = activeNodes.reduce((sum, node) => sum + node.cpuUsage, 0)
  return (totalLoad / activeNodes.length).toFixed(2)
})

const uniqueLocations = computed(() => {
  const locations = nodes.value.map(n => n.location).filter(Boolean)
  return [...new Set(locations)].sort()
})

// Helper functions for node operations
const isNodeOperationLoading = (nodeId, operation) => {
  return nodeOperations.value[nodeId]?.[operation] || false
}

const setNodeOperationLoading = (nodeId, operation, loading) => {
  if (!nodeOperations.value[nodeId]) {
    nodeOperations.value[nodeId] = {}
  }
  nodeOperations.value[nodeId][operation] = loading
}

// Batch operations helpers
const toggleNodeSelection = (nodeId) => {
  if (selectedNodes.value.has(nodeId)) {
    selectedNodes.value.delete(nodeId)
  } else {
    selectedNodes.value.add(nodeId)
  }
  showBatchActions.value = selectedNodes.value.size > 0
}

const selectAllNodes = () => {
  filteredNodes.value.forEach(node => selectedNodes.value.add(node.id))
  showBatchActions.value = true
}

const clearSelection = () => {
  selectedNodes.value.clear()
  showBatchActions.value = false
}

const isNodeSelected = (nodeId) => {
  return selectedNodes.value.has(nodeId)
}

// Batch operations
const batchConnectNodes = async () => {
  batchOperationLoading.value = true
  const selectedNodeIds = Array.from(selectedNodes.value)
  let successCount = 0
  let errorCount = 0

  try {
    for (const nodeId of selectedNodeIds) {
      const node = nodes.value.find(n => n.id === nodeId)
      if (!node) continue

      const isConnecting = node.status === 'offline' || node.status === 'error'

      try {
        let result
        if (isConnecting) {
          result = await edgeaiStore.connectToNode(nodeId)
        } else {
          result = await edgeaiStore.disconnectFromNode(nodeId)
        }

        if (result.success) {
          successCount++
        } else {
          errorCount++
        }
      } catch {
        errorCount++
      }
    }

    if (successCount > 0) {
      uiStore.addNotification({
        type: 'success',
        title: 'Batch Operation Completed',
        message: `Successfully processed ${successCount} node(s)${errorCount > 0 ? `, ${errorCount} failed` : ''}`
      })
    }

    if (errorCount > 0 && successCount === 0) {
      uiStore.addNotification({
        type: 'error',
        title: 'Batch Operation Failed',
        message: `Failed to process ${errorCount} node(s)`
      })
    }

    clearSelection()
  } finally {
    batchOperationLoading.value = false
  }
}

const batchRestartNodes = async () => {
  batchOperationLoading.value = true
  const selectedNodeIds = Array.from(selectedNodes.value)
  let successCount = 0
  let errorCount = 0

  try {
    for (const nodeId of selectedNodeIds) {
      try {
        const result = await edgeaiStore.restartNode(nodeId)
        if (result.success) {
          successCount++
        } else {
          errorCount++
        }
      } catch {
        errorCount++
      }
    }

    uiStore.addNotification({
      type: successCount > 0 ? 'success' : 'error',
      title: 'Batch Restart Completed',
      message: `Successfully restarted ${successCount} node(s)${errorCount > 0 ? `, ${errorCount} failed` : ''}`
    })

    clearSelection()
  } finally {
    batchOperationLoading.value = false
  }
}

// Delete node methods
const confirmDeleteNode = (node) => {
  nodeToDelete.value = node
  showDeleteModal.value = true
}

const deleteNode = async () => {
  if (!nodeToDelete.value) return

  setNodeOperationLoading(nodeToDelete.value.id, 'deleting', true)

  try {
    const result = await edgeaiStore.deleteNode(nodeToDelete.value.id)

    if (result.success) {
      uiStore.addNotification({
        type: 'success',
        title: 'Node Deleted',
        message: `Successfully deleted node: ${nodeToDelete.value.name}`
      })

      showDeleteModal.value = false
      nodeToDelete.value = null

      // Refresh node data
      await refreshNodes()
    } else {
      uiStore.addNotification({
        type: 'error',
        title: 'Delete Failed',
        message: result.error || `Failed to delete node: ${nodeToDelete.value.name}`
      })
    }
  } catch (error) {
    console.error('Error deleting node:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Delete Error',
      message: `Error deleting node: ${error.message || 'Unknown error occurred'}`
    })
  } finally {
    setNodeOperationLoading(nodeToDelete.value.id, 'deleting', false)
  }
}

const confirmBatchDeleteNodes = () => {
  if (selectedNodes.value.size === 0) return
  showBatchDeleteModal.value = true
}

const batchDeleteNodes = async () => {
  if (selectedNodes.value.size === 0) return

  batchOperationLoading.value = true
  const selectedNodeIds = Array.from(selectedNodes.value)

  try {
    const result = await edgeaiStore.batchDeleteNodes(selectedNodeIds)

    if (result.success) {
      uiStore.addNotification({
        type: 'success',
        title: 'Batch Delete Completed',
        message: result.message || `Successfully deleted ${selectedNodeIds.length} node(s)`
      })

      showBatchDeleteModal.value = false
      clearSelection()

      // Refresh node data
      await refreshNodes()
    } else {
      uiStore.addNotification({
        type: 'error',
        title: 'Batch Delete Failed',
        message: result.error || `Failed to delete ${selectedNodeIds.length} node(s)`
      })
    }
  } catch (error) {
    console.error('Error batch deleting nodes:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Batch Delete Error',
      message: `Error deleting nodes: ${error.message || 'Unknown error occurred'}`
    })
  } finally {
    batchOperationLoading.value = false
  }
}

// Auto-refresh functionality
const startAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }

  if (autoRefreshEnabled.value) {
    refreshInterval.value = setInterval(async () => {
      if (!refreshing.value && !batchOperationLoading.value) {
        await refreshNodes()
      }
    }, 5000) // Refresh every 5 seconds
  }
}

const stopAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
    refreshInterval.value = null
  }
}

const toggleAutoRefresh = () => {
  autoRefreshEnabled.value = !autoRefreshEnabled.value
  if (autoRefreshEnabled.value) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}

// Search suggestions
const generateSearchSuggestions = (query) => {
  if (!query || query.length < 2) {
    searchSuggestions.value = []
    showSearchSuggestions.value = false
    return
  }

  const lowercaseQuery = query.toLowerCase()
  const suggestions = new Set()

  // Add node names
  nodes.value.forEach(node => {
    if (node.name.toLowerCase().includes(lowercaseQuery)) {
      suggestions.add(node.name)
    }
    if (node.id.toLowerCase().includes(lowercaseQuery)) {
      suggestions.add(node.id)
    }
    if (node.location.toLowerCase().includes(lowercaseQuery)) {
      suggestions.add(node.location)
    }
    if (node.project.toLowerCase().includes(lowercaseQuery)) {
      suggestions.add(node.project)
    }
  })

  searchSuggestions.value = Array.from(suggestions).slice(0, 5)
  showSearchSuggestions.value = searchSuggestions.value.length > 0
}

const selectSuggestion = (suggestion) => {
  searchQuery.value = suggestion
  showSearchSuggestions.value = false
}

const onSearchInput = (event) => {
  const query = event.target.value
  searchQuery.value = query
  generateSearchSuggestions(query)
}

const onSearchFocus = () => {
  if (searchQuery.value) {
    generateSearchSuggestions(searchQuery.value)
  }
}

const onSearchBlur = () => {
  // Delay hiding suggestions to allow for clicks
  setTimeout(() => {
    showSearchSuggestions.value = false
  }, 200)
}

// Methods
const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const goBack = () => {
  router.push('/edgeai/dashboard')
}

const refreshNodes = async () => {
  refreshing.value = true
  
  try {
    const result = await edgeaiStore.refreshData()
    
    if (result.success) {
      uiStore.addNotification({
        type: 'success',
        title: 'Nodes Refreshed',
        message: 'Node status has been updated successfully.'
      })
    } else {
      uiStore.addNotification({
        type: 'error',
        title: 'Refresh Failed',
        message: result.error || 'Failed to refresh node data.'
      })
    }
  } finally {
    refreshing.value = false
  }
}

const selectNode = (node) => {
  selectedNode.value = node
}

const showNodeDetails = (node) => {
  selectedNode.value = node
  showDetailsModal.value = true
}

const addNewNode = () => {
  showAddNodeModal.value = true
}

const submitNewNode = async () => {
  if (!newNodeData.value.name.trim()) {
    uiStore.addNotification({
      type: 'error',
      title: 'Validation Error',
      message: 'Node name is required.'
    })
    return
  }

  addingNode.value = true

  try {
    const result = await edgeaiStore.addNode({
      name: newNodeData.value.name.trim(),
      location: newNodeData.value.location.trim() || 'Unknown',
      node_type: newNodeData.value.node_type
    })

    if (result.success) {
      uiStore.addNotification({
        type: 'success',
        title: 'Node Added',
        message: `Successfully added node: ${newNodeData.value.name}`
      })

      // Reset form and close modal
      newNodeData.value = { name: '', location: '', node_type: 'edge' }
      showAddNodeModal.value = false

      // Refresh node data
      await refreshNodes()
    } else {
      uiStore.addNotification({
        type: 'error',
        title: 'Add Node Failed',
        message: result.error || 'Failed to add new node.'
      })
    }
  } catch (error) {
    console.error('Error adding node:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Add Node Error',
      message: `Error adding node: ${error.message || 'Unknown error occurred'}`
    })
  } finally {
    addingNode.value = false
  }
}

const connectToNode = async (node) => {
  const isConnecting = node.status === 'offline' || node.status === 'error'
  const operation = isConnecting ? 'connecting' : 'disconnecting'

  setNodeOperationLoading(node.id, operation, true)

  try {
    let result
    if (isConnecting) {
      result = await edgeaiStore.connectToNode(node.id)
    } else {
      result = await edgeaiStore.disconnectFromNode(node.id)
    }

    if (result.success) {
      uiStore.addNotification({
        type: 'success',
        title: isConnecting ? 'Node Connected' : 'Node Disconnected',
        message: `Successfully ${isConnecting ? 'connected to' : 'disconnected from'} ${node.name}`
      })
    } else {
      uiStore.addNotification({
        type: 'error',
        title: 'Connection Failed',
        message: result.error || `Failed to ${isConnecting ? 'connect to' : 'disconnect from'} ${node.name}`
      })
    }
  } catch (error) {
    console.error('Connection error:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Connection Error',
      message: `Error ${isConnecting ? 'connecting to' : 'disconnecting from'} ${node.name}: ${error.message || 'Unknown error'}`
    })
  } finally {
    setNodeOperationLoading(node.id, operation, false)
  }
}

const exportNodes = async () => {
  exportingNodes.value = true

  try {
    const result = await edgeaiStore.exportNodes({
      status: statusFilter.value,
      location: locationFilter.value,
      search: searchQuery.value
    })

    if (result.success) {
      uiStore.addNotification({
        type: 'success',
        title: 'Export Completed',
        message: result.message || 'Node data has been exported successfully.'
      })
    } else {
      uiStore.addNotification({
        type: 'error',
        title: 'Export Failed',
        message: result.error || 'Failed to export node data.'
      })
    }
  } catch (error) {
    console.error('Error exporting nodes:', error)
    uiStore.addNotification({
      type: 'error',
      title: 'Export Error',
      message: `Error exporting nodes: ${error.message || 'Unknown error occurred'}`
    })
  } finally {
    exportingNodes.value = false
  }
}

const getStatusColor = (status) => {
  const colors = {
    online: 'bg-green-500',
    training: 'bg-blue-500',
    idle: 'bg-gray-500',
    offline: 'bg-gray-400',
    error: 'bg-red-500'
  }
  return colors[status] || 'bg-gray-400'
}

const getStatusBadgeColor = (status) => {
  const colors = {
    online: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    training: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    idle: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    offline: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const getStatusTextColor = (status) => {
  const colors = {
    online: 'text-green-600 dark:text-green-400',
    training: 'text-blue-600 dark:text-blue-400',
    idle: 'text-gray-600 dark:text-gray-400',
    offline: 'text-gray-500 dark:text-gray-500',
    error: 'text-red-600 dark:text-red-400'
  }
  return colors[status] || 'text-gray-600'
}

// Lifecycle
onMounted(async () => {
  await edgeaiStore.initializeStore()
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
  edgeaiStore.cleanup()
})
</script>