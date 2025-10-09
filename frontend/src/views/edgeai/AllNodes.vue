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
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
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
      </div>

      <!-- Filters and Actions -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-6 shadow-sm">
        <div class="flex items-center gap-4">
          <!-- Status Filter -->
          <div class="flex-shrink-0">
            <select
              v-model="statusFilter"
              class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-gray-400 dark:hover:border-gray-500 min-w-[120px]"
            >
              <option value="">All Status</option>
              <option value="alive">Alive</option>
              <option value="dead">Dead</option>
            </select>
          </div>
          
          <!-- Search Input -->
          <div class="relative flex-1 max-w-md">
            <input
              :value="searchQuery"
              @input="onSearchInput"
              @focus="onSearchFocus"
              @blur="onSearchBlur"
              type="text"
              placeholder=""
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:border-gray-400 dark:hover:border-gray-500"
              autocomplete="off"
            />
          </div>

        </div>
      </div>

      <!-- Nodes Table -->
      <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
        <!-- Table Header -->
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Node Details List</h3>
          <span class="text-sm text-gray-500 dark:text-gray-400">{{ filteredNodes.length }} nodes</span>
        </div>

        <!-- Grouped Tables -->
        <div v-for="group in groupedNodes" :key="group.role" class="border-b border-gray-200 dark:border-gray-700 last:border-b-0">
          <!-- Group Header -->
          <div class="px-6 py-3 bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600">
            <div class="flex items-center justify-between">
              <h4 class="text-sm font-medium text-gray-900 dark:text-white capitalize">
                {{ group.role }} ({{ group.nodes.length }})
              </h4>
              <div class="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
                <span class="flex items-center">
                  <div class="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
                  {{ group.aliveCount }} alive
                </span>
                <span class="flex items-center">
                  <div class="w-2 h-2 bg-gray-400 rounded-full mr-1"></div>
                  {{ group.deadCount }} dead
                </span>
              </div>
            </div>
          </div>

          <!-- Group Table -->
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">IP</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">CPU %</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Memory %</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Disk %</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Sent</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Received</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Heartbeat</th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr
                  v-for="node in group.nodes"
                  :key="node.id"
                  class="hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer"
                  @click="selectNode(node)"
                >
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900 dark:text-white">
                    {{ node.ip || node.id }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'inline-flex px-2 py-1 text-xs font-semibold rounded-full',
                      node.status === 'online' || node.status === 'alive' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
                    ]">
                      {{ node.status === 'alive' ? 'alive' : node.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ node.cpuUsage || 0 }}%
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ node.memoryUsage || 0 }}%
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ node.diskUsage || 0 }}%
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ formatDataRate(node.sent) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {{ formatDataRate(node.received) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {{ formatHeartbeat(node.heartbeat) }}
                  </td>
                </tr>
              </tbody>
            </table>
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
  MagnifyingGlassIcon,
  PlusIcon,
  ArrowDownTrayIcon,
  ArrowPathIcon
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
const autoRefreshEnabled = ref(true)
const refreshInterval = ref(null)
const showSearchSuggestions = ref(false)
const searchSuggestions = ref([])
const newNodeData = ref({
  name: '',
  location: '',
  node_type: 'edge'
})

// Use nodes from EdgeAI store with mock data for demonstration
const nodes = computed(() => {
  // If no real data, use mock data based on the image
  if (edgeaiStore.nodes.length === 0) {
    return [
      // MPC Model Nodes
      {
        id: '43.135.30.207',
        ip: '43.135.30.207',
        name: 'MPC Model Node 1',
        role: 'mpc model node',
        status: 'alive',
        cpuUsage: 0,
        memoryUsage: 36,
        diskUsage: 79.4,
        sent: 9.20,
        received: 4.17,
        heartbeat: Date.now() - 4000,
        location: 'Unknown',
        project: 'Default',
        type: 'edge'
      },
      {
        id: '106.52.36.202',
        ip: '106.52.36.202',
        name: 'MPC Model Node 2',
        role: 'mpc model node',
        status: 'dead',
        cpuUsage: 0,
        memoryUsage: 0,
        diskUsage: 0,
        sent: 0,
        received: 0,
        heartbeat: Date.now() - 4000,
        location: 'Unknown',
        project: 'Default',
        type: 'edge'
      },
      {
        id: '175.178.24.56',
        ip: '175.178.24.56',
        name: 'MPC Model Node 3',
        role: 'mpc model node',
        status: 'dead',
        cpuUsage: 0,
        memoryUsage: 0,
        diskUsage: 0,
        sent: 0,
        received: 0,
        heartbeat: Date.now() - 2000,
        location: 'Unknown',
        project: 'Default',
        type: 'edge'
      },
      // Model Manager Node
      {
        id: '10.0.4.31',
        ip: '10.0.4.31',
        name: 'Model Manager Node',
        role: 'model manager node',
        status: 'alive',
        cpuUsage: 17.3,
        memoryUsage: 7.4,
        diskUsage: 2.8,
        sent: 3.32,
        received: 6.66,
        heartbeat: Date.now() - 5000,
        location: 'Unknown',
        project: 'Default',
        type: 'edge'
      },
      // Edge AI Training Nodes
      {
        id: '114.132.200.147',
        ip: '114.132.200.147',
        name: 'Edge AI Training Node 1',
        role: 'edge AI training node',
        status: 'dead',
        cpuUsage: 0,
        memoryUsage: 0,
        diskUsage: 0,
        sent: 0,
        received: 0,
        heartbeat: Date.now() - 4000,
        location: 'Unknown',
        project: 'Default',
        type: 'edge'
      },
      {
        id: '42.194.177.24',
        ip: '42.194.177.24',
        name: 'Edge AI Training Node 2',
        role: 'edge AI training node',
        status: 'dead',
        cpuUsage: 0,
        memoryUsage: 0,
        diskUsage: 0,
        sent: 0,
        received: 0,
        heartbeat: Date.now() - 2000,
        location: 'Unknown',
        project: 'Default',
        type: 'edge'
      }
    ]
  }
  
  return edgeaiStore.nodes.map(node => ({
    ...node,
    // Add additional fields for UI that might not be in store
    ip: node.ip || node.id,
    role: node.role || 'Unknown',
    cpuUsage: node.cpuUsage || 0,
    memoryUsage: node.memoryUsage || 0,
    diskUsage: node.diskUsage || 0,
    sent: node.sent || 0,
    received: node.received || 0,
    heartbeat: node.heartbeat || Date.now(),
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
  }))
})

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
    filtered = filtered.filter(node => {
      if (statusFilter.value === 'alive') {
        return node.status === 'alive' || node.status === 'online'
      } else if (statusFilter.value === 'dead') {
        return node.status === 'dead' || node.status === 'offline'
      }
      return node.status === statusFilter.value
    })
  }

  if (locationFilter.value) {
    filtered = filtered.filter(node => node.location === locationFilter.value)
  }

  return filtered
})

const totalNodes = computed(() => nodes.value.length)
const onlineNodes = computed(() => nodes.value.filter(n => n.status === 'alive' || n.status === 'online').length)

const uniqueLocations = computed(() => {
  const locations = nodes.value.map(n => n.location).filter(Boolean)
  return [...new Set(locations)].sort()
})

// 按角色分组节点
const groupedNodes = computed(() => {
  const groups = {}
  
  filteredNodes.value.forEach(node => {
    const role = node.role || 'Unknown'
    if (!groups[role]) {
      groups[role] = {
        role: role,
        nodes: [],
        aliveCount: 0,
        deadCount: 0
      }
    }
    
    groups[role].nodes.push(node)
    if (node.status === 'alive' || node.status === 'online') {
      groups[role].aliveCount++
    } else {
      groups[role].deadCount++
    }
  })
  
  // 按角色名称排序
  return Object.values(groups).sort((a, b) => a.role.localeCompare(b.role))
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



// Auto-refresh functionality
const startAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }

  if (autoRefreshEnabled.value) {
    refreshInterval.value = setInterval(async () => {
      if (!refreshing.value) {
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

// 格式化数据速率
const formatDataRate = (value) => {
  if (!value || value === 0) return '0.00 KB/s'
  return `${value.toFixed(2)} KB/s`
}

// 格式化心跳时间
const formatHeartbeat = (heartbeat) => {
  if (!heartbeat) return 'Unknown'
  
  const now = Date.now()
  const diff = now - heartbeat
  const seconds = Math.floor(diff / 1000)
  
  if (seconds < 60) {
    return `${seconds} seconds ago`
  } else if (seconds < 3600) {
    const minutes = Math.floor(seconds / 60)
    return `${minutes} minutes ago`
  } else {
    const hours = Math.floor(seconds / 3600)
    return `${hours} hours ago`
  }
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