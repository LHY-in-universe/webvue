<template>
  <div class="federated-learning-dashboard min-h-screen bg-gray-50 dark:bg-gray-900" @error="handleRenderError">
    <!-- Navigation Header -->
    <nav class="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                <CpuChipIcon class="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                 Edge AI Training
                </h1>
                <div class="text-sm text-gray-600 dark:text-gray-400">
                  {{ currentProject?.name || 'Real-time Training Dashboard' }}
                </div>
              </div>
            </div>
          </div>
          
          <div class="flex items-center space-x-3">
            <Button 
              @click="openSettingsModal"
              variant="outline"
              size="sm"
              class="flex items-center space-x-2"
            >
              <CogIcon class="w-4 h-4" />
              <span>Settings</span>
            </Button>
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <!-- Training Configuration Header -->
    <div class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="grid grid-cols-2 md:grid-cols-5 gap-6">
          <!-- AI Model -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">AI Model</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ trainingConfig.aiModel }}</div>
          </div>
          
          <!-- Training Strategy -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Training Strategy</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ trainingConfig.strategy }}</div>
          </div>
          
          <!-- Protocol -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Protocol</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ trainingConfig.protocol }}</div>
          </div>
          
          <!-- Target Accuracy -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Target Accuracy</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ trainingConfig.targetAccuracy }}</div>
          </div>
          
          <!-- Estimated Completion -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Estimated Completion</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ trainingConfig.estimatedCompletion }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex-1 flex justify-center items-center">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <span class="text-gray-600 dark:text-gray-400">Loading visualization data...</span>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="flex-1 flex justify-center items-center">
      <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 max-w-md mx-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
              Failed to load visualization data
            </h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </div>
            <div class="mt-3">
              <Button @click="loadVisualizationData" variant="ghost" size="sm" class="text-red-800 dark:text-red-200 hover:bg-red-100 dark:hover:bg-red-800/30">
                Try again
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div v-else class="flex-1 relative">
      <!-- Node Details Panel (Left Side) - Only visible when node selected -->
      <div 
        v-if="selectedNode"
        class="absolute left-0 top-0 z-10 w-64 bg-white dark:bg-gray-900 m-6 mr-0 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 transform overflow-y-auto transition-all duration-700 h-[600px]"
        :class="isClosing ? 'animate-slide-out' : 'animate-slide-in'"
      >
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Node Details</h3>
        
        <!-- Selected Node Details -->
        <div class="space-y-6">
          <!-- Node Header -->
          <div class="flex items-center space-x-3 pb-4 border-b border-gray-200 dark:border-gray-700">
            <div :class="getNodeColorClass(selectedNode.type)" class="w-10 h-10 rounded-full flex items-center justify-center">
              <CpuChipIcon v-if="selectedNode.type === 'training'" class="w-5 h-5 text-white" />
              <ServerIcon v-else-if="selectedNode.type === 'control'" class="w-5 h-5 text-white" />
              <BeakerIcon v-else class="w-5 h-5 text-white" />
            </div>
            <div class="flex-1">
              <h4 class="font-semibold text-gray-900 dark:text-white">{{ selectedNode.name }}</h4>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ selectedNode.id }}</p>
            </div>
            <span 
              :class="getNodeStatusBadgeClass(selectedNode.status)"
              class="px-2 py-1 text-xs font-medium rounded-full"
            >
              {{ selectedNode.status }}
            </span>
          </div>

          <!-- Node Information (matching Node Details List) -->
          <div class="space-y-3">
            <h5 class="text-sm font-medium text-gray-900 dark:text-white">Node Information</h5>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">IP</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.ipAddress }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Role</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.role }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Status</span>
                <span :class="getNodeStatusBadgeClass(selectedNode.status)" class="px-2 py-1 text-xs font-medium rounded-full">
                  {{ selectedNode.status === 'online' ? 'alive' : selectedNode.status }}
                </span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">CPU %</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.resources?.cpu || 0 }}%</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Memory %</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.resources?.memory || 0 }}%</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Disk %</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.diskUsage || 0 }}%</span>
            </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Sent</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ (selectedNode.sent || 0).toFixed(2) }} MB/s</span>
          </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Received</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ (selectedNode.received || 0).toFixed(2) }} MB/s</span>
                </div>
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Heartbeat</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.lastHeartbeat }}</span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="space-y-2 pt-4 border-t border-gray-200 dark:border-gray-700">
            <Button 
              v-if="selectedNode.type === 'training' && selectedNode.status === 'idle'" 
              @click="startNodeTraining(selectedNode)"
              variant="primary"
              size="sm"
              class="w-full flex items-center justify-center space-x-2"
            >
              <PlayIcon class="w-4 h-4" />
              <span>Start Training</span>
            </Button>
            <Button 
              v-if="selectedNode.type === 'training' && selectedNode.status === 'training'" 
              @click="stopNodeTraining(selectedNode)"
              variant="outline"
              size="sm"
              class="w-full flex items-center justify-center space-x-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10h6v4H9z"/>
              </svg>
              <span>Stop Training</span>
            </Button>
            <Button 
              @click="closeNodeDetails"
              variant="ghost"
              size="sm"
              class="w-full"
            >
              Clear Selection
            </Button>
          </div>
        </div>
      </div>
      
      <!-- Main Content Container (Network Visualization + Control Panel) -->
      <div class="flex h-full">
        <!-- Network Visualization Container (fixed position) -->
        <div class="flex-1">
          <!-- Network Visualization -->
          <div class="bg-white dark:bg-gray-900 m-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 h-[900px]">
            <div class="h-full relative">
              <FederatedNetworkVisualization
                ref="networkViz"
                :key="vizKey"
                :nodes="federatedNodes"
                :connections="federatedConnections"
                :training-round="trainingState.currentRound"
                :training-status="trainingState.status"
                :node-animation-states="nodeAnimationStates"
                @node-click="handleNodeClick"
                @connection-click="handleConnectionClick"
              />
            </div>
          </div>
        </div>
        
        <!-- Control Panel (truly fixed position) -->
        <div ref="controlPanelRef" class="w-80 lg:w-96 xl:w-[420px] flex-shrink-0 bg-white dark:bg-gray-900 m-6 ml-0 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 h-[900px] overflow-y-auto">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">Control Panel</h3>
        
        <!-- Quick Actions: Start Training at top -->
        <div class="mb-4">
          <Button 
            v-if="trainingState.status === 'idle' || trainingState.status === 'stopped'"
            @click="startTraining"
            variant="primary"
            size="sm"
            class="w-full flex items-center justify-center space-x-2"
            :disabled="isTrainingStarting"
          >
            <svg v-if="!isTrainingStarting" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h1m4 0h1m-6-8h8a2 2 0 012 2v8a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2z"/>
            </svg>
            <svg v-else class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <span>{{ isTrainingStarting ? 'Starting...' : 'Start Training' }}</span>
          </Button>
        </div>
        
        <!-- Task Management -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Task Management</h4>
          
          <!-- Task List -->
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs text-gray-600 dark:text-gray-400">Active Tasks</span>
              <Button 
                @click="loadTaskList"
                variant="ghost"
                size="sm"
                class="text-xs"
                :disabled="isLoadingTasks"
              >
                <svg v-if="!isLoadingTasks" class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                <svg v-else class="w-3 h-3 mr-1 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                {{ isLoadingTasks ? 'Loading...' : 'Refresh' }}
              </Button>
            </div>
          
            <!-- Task List -->
            <div v-if="taskList.length > 0" class="space-y-3 max-h-72 overflow-y-auto pr-2">
              <div v-for="task in taskList" :key="task" 
                   class="p-3 bg-gray-50 dark:bg-gray-800 rounded text-xs border border-gray-200 dark:border-gray-700">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span class="font-mono text-gray-700 dark:text-gray-300">{{ task.substring(0, 8) }}...</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span class="text-[10px] text-gray-500 dark:text-gray-400">ID: {{ task }}</span>
                    <Button 
                      @click="deleteTask(task)"
                      variant="ghost"
                      size="sm"
                      class="text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 p-1"
                      :disabled="isDeletingTask === task"
                    >
                      <svg v-if="isDeletingTask !== task" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                      </svg>
                      <svg v-else class="w-3 h-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                      </svg>
                    </Button>
            </div>
          </div>
          
                <!-- Task Status Row -->
                <div class="grid grid-cols-2 gap-2 mt-2">
                  <div class="flex items-center justify-between bg-white dark:bg-gray-900 rounded px-2 py-1">
                    <span class="text-gray-500 dark:text-gray-400">Round</span>
                    <span class="font-medium text-gray-900 dark:text-white">
                      {{ (taskStatusMap[task]?.current_round ?? 0) }}/{{ (taskStatusMap[task]?.total_rounds ?? 0) }}
                    </span>
            </div>
                  <div class="flex items-center justify-between bg-white dark:bg-gray-900 rounded px-2 py-1">
                    <span class="text-gray-500 dark:text-gray-400">Loss</span>
                    <span class="font-medium text-red-600 dark:text-red-400">
                      {{ (taskStatusMap[task]?.loss ?? 0).toFixed(4) }}
                    </span>
            </div>
                  <div class="flex items-center justify-between bg-white dark:bg-gray-900 rounded px-2 py-1 col-span-2">
                    <span class="text-gray-500 dark:text-gray-400">Accuracy</span>
                    <span class="font-medium text-green-600 dark:text-green-400">
                      {{ taskStatusMap[task]?.accuracy !== null && taskStatusMap[task]?.accuracy !== undefined
                        ? (taskStatusMap[task].accuracy * 100).toFixed(2) + '%' : 'N/A' }}
                    </span>
          </div>
            </div>
            </div>
          </div>
          
            <div v-else-if="!isLoadingTasks" class="text-xs text-gray-500 dark:text-gray-400 text-center py-2">
              No active tasks
            </div>
          </div>
        </div>

          <!-- Training Controls (hidden, moved to top) -->
          <div v-if="false" class="mb-6">
            <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Training Controls</h4>
            
            <!-- Start Training Button -->
          <Button 
              v-if="trainingState.status === 'idle' || trainingState.status === 'stopped'"
            @click="startTraining"
            variant="primary"
            size="sm"
              class="w-full flex items-center justify-center space-x-2 mb-3"
              :disabled="isTrainingStarting"
            >
              <svg v-if="!isTrainingStarting" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h1m4 0h1m-6-8h8a2 2 0 012 2v8a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2z"/>
              </svg>
              <svg v-else class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              <span>{{ isTrainingStarting ? 'Starting...' : 'Start Training' }}</span>
          </Button>
          
            <!-- Stop Training Button -->
          <Button 
              v-if="trainingState.status === 'training' || trainingState.status === 'running'"
              @click="stopTraining"
            variant="outline"
            size="sm"
              class="w-full flex items-center justify-center space-x-2 mb-3"
              :disabled="isTrainingStopping"
            >
              <svg v-if="!isTrainingStopping" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10h6v4H9z"/>
              </svg>
              <svg v-else class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              <span>{{ isTrainingStopping ? 'Stopping...' : 'Stop Training' }}</span>
          </Button>

            <!-- Current Task ID -->
            <div v-if="currentTaskId" class="text-xs text-gray-500 dark:text-gray-400 mb-3">
              <div class="flex items-center justify-between">
                <span>Task ID:</span>
                <span class="font-mono">{{ currentTaskId.substring(0, 8) }}...</span>
            </div>
            </div>
            
            <!-- Training Metrics -->
            <div v-if="roundMetrics.length > 0 || trainingState.status === 'training'" class="text-xs">
              <h5 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Training Metrics</h5>
              
              <!-- Current Round Info -->
              <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-3">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-gray-600 dark:text-gray-400 font-medium">Current Round</span>
                  <span class="text-lg font-bold text-blue-600 dark:text-blue-400">
                    {{ trainingState.currentRound }}/{{ trainingState.totalRounds }}
                  </span>
            </div>
                <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
                  <div 
                    class="h-2 bg-gradient-to-r from-blue-500 to-green-500 rounded-full transition-all duration-500"
                    :style="{ width: `${(trainingState.currentRound / trainingState.totalRounds) * 100}%` }"
                  ></div>
          </div>
        </div>
              
              <!-- Latest Metrics -->
              <div v-if="roundMetrics.length > 0" class="space-y-2">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-gray-600 dark:text-gray-400 font-medium">Latest Metrics</span>
                    <span class="text-xs text-gray-500 dark:text-gray-400">
                      Round {{ roundMetrics[roundMetrics.length - 1]?.round || 0 }}
                    </span>
    </div>

                  <div class="grid grid-cols-2 gap-3">
                    <!-- Loss -->
            <div class="text-center">
                    <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Loss</div>
                    <div class="text-lg font-bold text-red-600 dark:text-red-400">
                      {{ roundMetrics[roundMetrics.length - 1]?.loss?.toFixed(4) || '0.0000' }}
            </div>
          </div>

                    <!-- Accuracy -->
                    <div class="text-center">
                      <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Accuracy</div>
                      <div class="text-lg font-bold text-green-600 dark:text-green-400">
                        {{ roundMetrics[roundMetrics.length - 1]?.accuracy !== null && roundMetrics[roundMetrics.length - 1]?.accuracy !== undefined 
                          ? (roundMetrics[roundMetrics.length - 1].accuracy * 100).toFixed(2) + '%' 
                          : 'N/A' }}
              </div>
            </div>
            </div>
          </div>

                <!-- Historical Metrics (Last 3 rounds) -->
                <div v-if="roundMetrics.length > 1" class="space-y-1">
                  <div class="text-xs text-gray-500 dark:text-gray-400 font-medium mb-1">Recent Rounds</div>
                  <div v-for="metric in roundMetrics.slice(-3).reverse()" :key="metric.round" 
                       class="flex items-center justify-between py-1 px-2 bg-gray-50 dark:bg-gray-700 rounded text-xs">
                    <span class="text-gray-600 dark:text-gray-400">Round {{ metric.round }}</span>
          <div class="flex items-center space-x-3">
                      <span class="text-red-500 dark:text-red-400">
                        L: {{ metric.loss?.toFixed(3) || '0.000' }}
                      </span>
                      <span class="text-green-500 dark:text-green-400">
                        A: {{ metric.accuracy !== null && metric.accuracy !== undefined 
                          ? (metric.accuracy * 100).toFixed(1) + '%' 
                          : 'N/A' }}
                      </span>
              </div>
            </div>
            </div>
          </div>
              </div>
            </div>
          </div>
        </div>

    <!-- Bottom Dashboard -->
    <div class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
      <!-- Metrics Summary -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <!-- 顶部统计与训练控制按钮已按要求移除 -->

        <!-- Node Details List -->
        <div class="mb-3">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-md font-semibold text-gray-900 dark:text-white">Node Details List</h3>
             <div class="text-sm text-gray-500 dark:text-gray-400">Total: <span class="font-medium text-gray-900 dark:text-white">{{ rayClusterNodes.length }}</span></div>
          </div>

          <!-- Group: Model Nodes -->
          <div class="mb-4">
            <h4 class="text-sm font-medium text-blue-600 dark:text-blue-400 mb-2">Model Nodes ({{ rayGroups.model.length }})</h4>
            <div class="overflow-x-auto bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
              <table class="w-full text-sm">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">IP</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Role</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Status</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">CPU %</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Memory %</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Disk %</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Sent</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Received</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Heartbeat</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="n in rayGroups.model" :key="`model-${n.ip}`" class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700/50">
                    <td class="p-3 text-gray-900 dark:text-white">{{ n.ip }}</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.role }}</td>
                    <td class="p-3"><span :class="getNodeStatusBadgeClass(n.status === 'alive' ? 'online' : 'offline')" class="px-2 py-1 text-xs font-medium rounded-full">{{ n.status }}</span></td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.cpu_usage ?? 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.memory_usage ?? 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.disk_usage ?? 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ (n.sent || 0).toFixed(2) }} MB/s</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ (n.received || 0).toFixed(2) }} MB/s</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ formatHeartbeat(n.heartbeat) }}</td>
                  </tr>
                </tbody>
              </table>
                      </div>
          </div>

          <!-- Group: Data Nodes -->
          <div class="mb-4">
            <h4 class="text-sm font-medium text-green-600 dark:text-green-400 mb-2">Data Nodes ({{ rayGroups.data.length }})</h4>
            <div class="overflow-x-auto bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
              <table class="w-full text-sm">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">IP</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Role</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Status</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">CPU %</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Memory %</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Disk %</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Sent</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Received</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Heartbeat</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="n in rayGroups.data" :key="`data-${n.ip}`" class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700/50">
                    <td class="p-3 text-gray-900 dark:text-white">{{ n.ip }}</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.role }}</td>
                    <td class="p-3"><span :class="getNodeStatusBadgeClass(n.status === 'alive' ? 'online' : 'offline')" class="px-2 py-1 text-xs font-medium rounded-full">{{ n.status }}</span></td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.cpu_usage ?? 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.memory_usage ?? 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.disk_usage ?? 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ (n.sent || 0).toFixed(2) }} MB/s</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ (n.received || 0).toFixed(2) }} MB/s</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ formatHeartbeat(n.heartbeat) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Group: Computer Nodes -->
          <div>
            <h4 class="text-sm font-medium text-purple-600 dark:text-purple-400 mb-2">Computer Nodes ({{ rayGroups.computer.length }})</h4>
            <div class="overflow-x-auto bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
              <table class="w-full text-sm">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">IP</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Role</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Status</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">CPU %</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Memory %</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Disk %</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Sent</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Received</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Heartbeat</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="n in rayGroups.computer" :key="`computer-${n.ip}`" class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700/50">
                    <td class="p-3 text-gray-900 dark:text-white">{{ n.ip }}</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.role }}</td>
                    <td class="p-3"><span :class="getNodeStatusBadgeClass(n.status === 'alive' ? 'online' : 'offline')" class="px-2 py-1 text-xs font-medium rounded-full">{{ n.status }}</span></td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.cpu_usage ?? 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.memory_usage ?? 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ n.disk_usage ?? 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ (n.sent || 0).toFixed(2) }} MB/s</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ (n.received || 0).toFixed(2) }} MB/s</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ formatHeartbeat(n.heartbeat) }}</td>
                  </tr>
                </tbody>
              </table>
                      </div>
                      </div>
                      </div>
                      </div>
                      </div>

    <!-- Node Details Modal -->
    <NodeDetailsModal
      :node="modalSelectedNode"
      :is-visible="isModalVisible"
      :anchor-position="modalAnchorPosition"
      @close="closeNodeModal"
    />

    <!-- Parameters Settings Modal -->
    <div v-if="isSettingsModalVisible" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex min-h-screen items-center justify-center p-4">
        <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="closeSettingsModal"></div>
        
        <div class="relative bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Training Settings</h3>
            <button 
              @click="closeSettingsModal"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
                      </div>
          
          <div class="p-6">
            <form @submit.prevent="saveParameters" class="space-y-6">
              <!-- 训练算法设置 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Training Algorithm (training_alg)</label>
                  <select 
                    v-model="parameters.training_alg"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  >
                    <option value="sft">SFT (Supervised Fine-Tuning)</option>
                    <option value="rlhf">RLHF (Reinforcement Learning from Human Feedback)</option>
                    <option value="dpo">DPO (Direct Preference Optimization)</option>
                    <option value="ppo">PPO (Proximal Policy Optimization)</option>
                  </select>
                      </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Federated Algorithm (fed_alg)</label>
                  <select 
                    v-model="parameters.fed_alg"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  >
                    <option value="fedavg">FedAvg</option>
                    <option value="fedprox">FedProx</option>
                    <option value="fednova">FedNova</option>
                    <option value="scaffold">SCAFFOLD</option>
                    <option value="fedopt">FedOpt</option>
                  </select>
                      </div>
              </div>

              <!-- 安全聚合设置 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Secure Aggregation (secure_aggregation)</label>
                  <select 
                    v-model="parameters.secure_aggregation"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  >
                    <option value="shamir_threshold">Shamir Threshold</option>
                    <option value="paillier">Paillier</option>
                    <option value="secure_aggregation">Secure Aggregation</option>
                    <option value="none">None</option>
                  </select>
                        </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Num Computers (num_computers)</label>
                  <input 
                    v-model.number="parameters.num_computers"
                    type="number"
                    min="1"
                    max="100"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                      </div>
              </div>

              <!-- 阈值和轮次设置 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Threshold (threshold)</label>
                  <input 
                    v-model.number="parameters.threshold"
                    type="number"
                    min="1"
                    :max="parameters.num_computers"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Rounds (num_rounds)</label>
                  <input 
                    v-model.number="parameters.num_rounds"
                    type="number"
                    min="1"
                    max="1000"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>
              </div>

              <!-- 客户端设置 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Num Clients (num_clients)</label>
                  <input 
                    v-model.number="parameters.num_clients"
                    type="number"
                    min="1"
                    max="100"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Sample Clients (sample_clients)</label>
                  <input 
                    v-model.number="parameters.sample_clients"
                    type="number"
                    min="1"
                    :max="parameters.num_clients"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>
              </div>

              <!-- 训练步数和学习率 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Max Steps (max_steps)</label>
                  <input 
                    v-model.number="parameters.max_steps"
                    type="number"
                    min="1"
                    max="10000"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Learning Rate (lr)</label>
                  <input 
                    v-model="parameters.lr"
                    type="text"
                    placeholder="1e-4"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>
              </div>

              <!-- 模型和数据集设置 -->
              <div class="grid grid-cols-1 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Model Path (model_name_or_path)</label>
                  <input 
                    v-model="parameters.model_name_or_path"
                    type="text"
                    placeholder="sshleifer/tiny-gpt2"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Dataset Name (dataset_name)</label>
                  <input 
                    v-model="parameters.dataset_name"
                    type="text"
                    placeholder="vicgalle/alpaca-gpt4"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Dataset Sample (dataset_sample)</label>
                  <input 
                    v-model.number="parameters.dataset_sample"
                    type="number"
                    min="1"
                    max="10000"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>
              </div>

              <!-- 操作按钮 -->
              <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200 dark:border-gray-700">
                      <Button
                  @click="closeSettingsModal"
                  variant="outline"
                  type="button"
                >
                  取消
                      </Button>
                <Button 
                  @click="resetToDefaults"
                  variant="outline"
                  type="button"
                >
                  Reset Defaults
                </Button>
                <Button 
                  type="submit"
                  variant="primary"
                >
                  Save Settings
                </Button>
            </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>  <!-- 关闭 <div v-else class="flex-1 relative"> -->
</template>

<style scoped>
@keyframes slide-in {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slide-out {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(-100%);
    opacity: 0;
  }
}

.animate-slide-in {
  animation: slide-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

.animate-slide-out {
  animation: slide-out 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
}
</style>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEdgeAIStore } from '@/stores/edgeai'
import { useApiOptimization } from '@/composables/useApiOptimization'
import edgeaiService from '@/services/edgeaiService'
import performanceMonitor from '@/utils/performanceMonitor'
import { API_CONFIG } from '@/config/api.js'
import FederatedNetworkVisualization from '@/components/edgeai/FederatedNetworkVisualization.vue'
import NodeDetailsModal from '@/components/edgeai/NodeDetailsModal.vue'
import Button from '@/components/ui/Button.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import { 
  CpuChipIcon,
  ArrowPathIcon,
  ArrowLeftIcon,
  UserPlusIcon,
  ServerIcon,
  PlayIcon,
  CheckCircleIcon,
  BeakerIcon,
  CogIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const route = useRoute()
const edgeaiStore = useEdgeAIStore()
const { cachedApiCall, clearCache } = useApiOptimization()

// Component refs
const networkViz = ref(null)
const vizKey = ref(0)
const controlPanelRef = ref(null)

const scrollControlPanelBottom = () => {
  try {
    const el = controlPanelRef.value
    if (el) {
      el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })
    }
  } catch (e) {
    // ignore
  }
}

// Loading and error states
const loading = ref(false)
const error = ref(null)
const renderError = ref(null)
const refreshInterval = ref(null)
const refreshErrorCount = ref(0)
const MAX_REFRESH_ERRORS = 3

// Global error handler for component rendering errors
const handleRenderError = (err, context) => {
  console.error('Visualization render error:', err, 'Context:', context)
  renderError.value = {
    message: err.message || 'Rendering error occurred',
    stack: err.stack,
    context
  }
}

// Training Configuration (will be loaded from API)
const trainingConfig = ref({
  aiModel: 'Loading...',
  strategy: 'Loading...',
  protocol: 'Loading...',
  targetAccuracy: 'Loading...',
  estimatedCompletion: 'Loading...'
})

// Training State
const trainingState = ref({
  status: 'idle', // idle, training, completed
  currentRound: 0,
  totalRounds: 100,
  startTime: null,
  endTime: null
})

// 后端训练接口配置与状态
// 在开发环境通过Vite代理到 http://12.148.158.61:6677，避免CORS
const TRAIN_API_BASE = '/edge-train'
const trainingTaskId = ref(null)
const monitorTimer = ref(null)
const roundMetrics = ref([]) // { round, loss, accuracy }

// 训练控制状态
const isTrainingStarting = ref(false)
const isTrainingStopping = ref(false)
const currentTaskId = ref(null)

// 任务管理状态
const taskList = ref([])
const isLoadingTasks = ref(false)
const isDeletingTask = ref(null)
// 每个任务的监控状态缓存 { [taskId]: { current_round, total_rounds, loss, accuracy } }
const taskStatusMap = ref({})

// Current project (will be loaded from API)
const currentProject = ref({
  name: 'Loading...',
  status: 'loading'
})

// All Available Federated Learning Nodes (will be loaded from API)
const allFederatedNodes = ref([])

// 原始 Ray 集群节点（直接用于节点明细列表表格展示）
const rayClusterNodes = ref([])

// 按角色分组（model/data/computer）
const rayGroups = computed(() => {
  const groups = { model: [], data: [], computer: [] }
  rayClusterNodes.value.forEach(n => {
    const role = String(n.role || '').toLowerCase()
    if (role.includes('model')) groups.model.push(n)
    else if (role.includes('data')) groups.data.push(n)
    else groups.computer.push(n)
  })
  return groups
})

// Node filtering and pagination state (simplified for dynamic training)
const currentPage = ref(0)
const maxDisplayedNodes = 15
const nodeFilter = ref('training') // 固定显示训练中的节点

// Sorting state
const sortConfig = ref({
  key: 'name',
  direction: 'asc' // 'asc' or 'desc'
})

// 节点动画状态管理
const nodeAnimationStates = ref(new Map())

// 所有训练完成标志
const allTrainingCompleted = ref(false)

// 节点淡出动画控制
const triggerNodeFadeOut = (nodeId) => {
  nodeAnimationStates.value.set(nodeId, {
    fading: true,
    fadeStartTime: Date.now()
  })
  
  // 3秒后完全移除节点动画状态
  setTimeout(() => {
    nodeAnimationStates.value.delete(nodeId)
  }, 3000)
}

// 替换训练完成的节点
const replaceCompletedNode = () => {
  const idleNodes = allFederatedNodes.value.filter(n => 
    n.type === 'training' && n.status === 'idle'
  )
  
  if (idleNodes.length > 0) {
    // 选择优先级最高的空闲节点
    idleNodes.sort((a, b) => b.priority - a.priority)
    const newTrainingNode = idleNodes[0]
    
    newTrainingNode.status = 'training'
    newTrainingNode.trainingProgress = Math.floor(Math.random() * 10) // 从0-10%开始
    
    console.log(`Node ${newTrainingNode.name} started training to replace completed node`)
    return true
  }
  return false
}

// 检查所有训练是否完成
const checkAllTrainingCompleted = () => {
  const allTrainingNodes = allFederatedNodes.value.filter(n => n.type === 'training')
  const completedNodes = allTrainingNodes.filter(n => n.status === 'completed')
  const idleNodes = allTrainingNodes.filter(n => n.status === 'idle')
  
  // 如果所有节点都完成训练且没有空闲节点可以替换
  if (completedNodes.length === allTrainingNodes.length || 
      (completedNodes.length > 0 && idleNodes.length === 0)) {
    if (!allTrainingCompleted.value) {
      allTrainingCompleted.value = true
      triggerCelebrationAnimation()
    }
    return true
  }
  return false
}

// 触发庆祝动画
const triggerCelebrationAnimation = () => {
  console.log('🎉 All training completed! Showing celebration animation...')
  
  // 这里可以添加更复杂的庆祝动画逻辑
  // 例如：烟花效果、进度条完成动画、成功提示等
  trainingState.value.status = 'completed'
  trainingState.value.endTime = Date.now()
  
  // 显示完成通知（在实际应用中可以是模态框或toast）
  setTimeout(() => {
    alert('🎉 联邦学习训练已全部完成！所有节点已完成训练任务。')
  }, 1000)
}

// Load visualization data from API
const loadVisualizationData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('EdgeAIVisualization')
  loading.value = true
  error.value = null
  
  try {
    const projectId = route.params.projectId
    
    // Load project details, training config, and nodes in parallel
    const [projectResult, configResult, nodesResult] = await Promise.all([
      projectId ? cachedApiCall(`edgeai-project-${projectId}`, 
        () => edgeaiService.projects.getProject(projectId), 
        2 * 60 * 1000
      ) : null,
      cachedApiCall('edgeai-training-config', 
        () => edgeaiService.training.getTrainingConfig(projectId), 
        5 * 60 * 1000
      ),
      cachedApiCall('edgeai-visualization-nodes', 
        () => edgeaiService.nodes.getVisualizationNodes(projectId), 
        30 * 1000 // Cache for 30 seconds for real-time updates
      )
    ])

    // Update project details
    if (projectResult) {
      currentProject.value = {
        name: projectResult.name || 'EdgeAI Training Session',
        status: projectResult.status || 'active'
      }
    } else {
      currentProject.value = {
        name: 'EdgeAI Training Session',
        status: 'active'
      }
    }

    // Update training configuration
    if (configResult) {
      const config = configResult.config || configResult
      trainingConfig.value = {
        aiModel: config.ai_model || 'Unknown Model',
        strategy: config.strategy || 'Unknown Strategy',
        protocol: config.protocol || 'fedavg',
        targetAccuracy: config.target_accuracy || '≥90%',
        estimatedCompletion: config.estimated_completion || 'Unknown'
      }
    }

    // Update nodes data（严格使用后端返回的数据，不生成任何假数据）
    const nodesList = nodesResult?.nodes || nodesResult || []

    const mappedNodes = Array.isArray(nodesList)
      ? nodesList
          .filter(node => node && node.id)
        .map(node => ({
          id: node.id,
          name: node.name || `Node ${node.id}`,
            type: node.type || node.node_type || 'training',
          status: node.status || 'idle',
          role: node.role || 'Participant',
          user: node.user || 'System',
            ipAddress: node.ip_address || node.ip || 'Unknown',
            connectedNodes: node.connected_nodes || node.connectedNodes || '0',
            trainingProgress: node.training_progress || node.progress || 0,
          resources: {
              cpu: node.resources?.cpu ?? node.cpu ?? 0,
              memory: node.resources?.memory ?? node.memory ?? '0.0',
              gpu: node.resources?.gpu ?? node.gpu ?? 0
            },
            lastHeartbeat: node.last_heartbeat || node.last_seen || 'Unknown',
          priority: node.priority || 1
        }))
      : []

    allFederatedNodes.value = mappedNodes

    console.log('Loaded nodes data:', allFederatedNodes.value.length, 'total nodes')
    console.log('Control nodes:', allFederatedNodes.value.filter(n => ['model', 'control'].includes(n.type)).length)
    console.log('Training nodes:', allFederatedNodes.value.filter(n => n.type === 'training').length)

    pageMonitor.end({ success: true, nodeCount: allFederatedNodes.value.length })
  } catch (err) {
    console.error('Failed to load visualization data:', err)
    error.value = err.message || 'Failed to load visualization data'
    pageMonitor.end({ success: false, error: err.message })
  } finally {
    loading.value = false
  }
}

// Setup auto-refresh for real-time updates
const setupAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  refreshInterval.value = setInterval(() => {
    if (!loading.value) {
      loadNodesData()
    }
  }, 5 * 1000) // 每5秒刷新一次
}

// Load only nodes data for real-time updates
const loadNodesData = async () => {
  try {
    // 从训练服务获取 Ray 集群节点状态
    const resp = await fetch(`${TRAIN_API_BASE}/monitorRayCluster/node`, { headers: { accept: 'application/json' } })
    if (!resp.ok) throw new Error(`Ray cluster monitor failed: ${resp.status}`)
    const nodes = await resp.json()

    if (Array.isArray(nodes)) {
      rayClusterNodes.value = nodes
      vizKey.value++
      const mapped = nodes
        .filter(n => n && (n.ip || n.id))
        .map(n => {
          const role = (n.role || '').toLowerCase()
          const type = role.includes('model') ? 'model' : 'training'
          const statusMap = { alive: 'online', dead: 'offline' }
          const status = statusMap[(n.status || '').toLowerCase()] || (n.status || 'idle')
          return {
            id: n.ip || n.id,
            name: `${role || 'node'} ${n.ip || ''}`.trim(),
            type,
            status,
            role: n.role || undefined,
            user: undefined,
            ipAddress: n.ip || 'Unknown',
            connectedNodes: undefined,
            trainingProgress: 0,
        resources: {
              cpu: Number(n.cpu_usage ?? 0),
              memory: String(n.memory_usage ?? '0.0'),
              gpu: 0
            },
            lastHeartbeat: formatHeartbeat(n.heartbeat),
            priority: 1
          }
        })
      allFederatedNodes.value = mapped
    }
    // 成功后重置错误计数
    if (refreshErrorCount.value !== 0) refreshErrorCount.value = 0
  } catch (err) {
    console.error('Failed to refresh nodes data (ray cluster):', err)
    refreshErrorCount.value += 1
    if (refreshErrorCount.value >= MAX_REFRESH_ERRORS) {
      if (refreshInterval.value) {
        clearInterval(refreshInterval.value)
        refreshInterval.value = null
      }
      if (refreshErrorCount.value === MAX_REFRESH_ERRORS) {
        alert('Ray 集群监控接口连续失败，已暂停自动刷新。请检查训练服务/代理配置。')
      }
    }
  }
}

// 将心跳时间戳转为相对时间字符串
const formatHeartbeat = (ts) => {
  if (!ts) return '-'
  try {
    const now = Date.now()
    const diffSec = Math.max(0, Math.floor((now - Number(ts)) / 1000))
    if (diffSec < 60) return `${diffSec} seconds ago`
    const diffMin = Math.floor(diffSec / 60)
    if (diffMin < 60) return `${diffMin} minutes ago`
    const diffHour = Math.floor(diffMin / 60)
    return `${diffHour} hours ago`
  } catch (e) {
    return '-'
  }
}

// Computed property for displayed nodes - 直接使用 Ray 集群节点数据
const displayedNodes = computed(() => {
  // 直接使用 Ray 集群节点数据，确保与 Node Details List 对应
  const mapped = rayClusterNodes.value.map(n => {
    const role = String(n.role || '').toLowerCase()
    let type = 'training'
    if (role.includes('model')) type = 'model'
    else if (role.includes('data')) type = 'training'
    else type = 'training'
    
    return {
      id: n.ip,
      name: `${n.role} ${n.ip}`,
      type: type,
      status: n.status === 'alive' ? 'online' : 'offline',
      role: n.role,
      ipAddress: n.ip,
      resources: {
        cpu: n.cpu_usage || 0,
        memory: String(n.memory_usage || 0),
        gpu: 0
      },
      lastHeartbeat: formatHeartbeat(n.heartbeat),
      priority: 1,
      // 添加 Node Details List 中需要的字段
      diskUsage: Number(n.disk_usage ?? 0),
      sent: Number(n.sent ?? 0),
      received: Number(n.received ?? 0)
    }
  })
  
  console.log('displayedNodes computed:', {
    rayClusterNodesCount: rayClusterNodes.value.length,
    mappedCount: mapped.length,
    nodes: mapped.map(n => ({ id: n.id, name: n.name, type: n.type }))
  })
  
  return mapped
})

// Update federatedNodes to use displayedNodes
const federatedNodes = displayedNodes

// 传输状态管理
const transmissionStates = ref(new Map())

// Dynamic connections based on currently displayed nodes
const federatedConnections = computed(() => {
  const connections = []
  const displayedTrainingNodes = federatedNodes.value.filter(n => n.type === 'training')
  const controlNodes = federatedNodes.value.filter(n => ['model', 'control'].includes(n.type))
  
  // 仅当后端返回了控制/模型节点时，按轮询方式连接到训练节点
  if (controlNodes.length > 0) {
  displayedTrainingNodes.forEach((trainingNode, index) => {
      const controlNodeId = controlNodes[index % controlNodes.length].id
    const connectionId = `${controlNodeId}-${trainingNode.id}`
    const transmissionState = transmissionStates.value.get(connectionId)
    
    connections.push({
      id: connectionId,
      from: controlNodeId,
      to: trainingNode.id,
      type: 'control',
      active: trainingNode.status === 'training',
      transmitting: transmissionState?.transmitting || false,
      direction: transmissionState?.direction || 'downstream',
      lastTransmission: transmissionState?.lastTransmission || 0,
      bandwidth: 0
    })
  })
  }
  
  return connections
})

// 传输控制函数
const triggerTransmission = (connectionId, direction, duration = 2000) => {
  transmissionStates.value.set(connectionId, {
    transmitting: true,
    direction: direction,
    lastTransmission: Date.now()
  })
  
  // 设置传输结束定时器
  setTimeout(() => {
    const state = transmissionStates.value.get(connectionId)
    if (state) {
      state.transmitting = false
      transmissionStates.value.set(connectionId, state)
    }
  }, duration)
}

// 随机方向选择
const getRandomDirection = () => {
  const directions = ['upstream', 'downstream', 'bidirectional']
  return directions[Math.floor(Math.random() * directions.length)]
}

// Pagination computed properties
const totalPages = computed(() => {
  const filteredEdgeNodes = allFederatedNodes.value.filter(n => {
    if (n.type !== 'training') return false
    if (nodeFilter.value === 'all') return true
    return n.status === nodeFilter.value
  })
  return Math.ceil(filteredEdgeNodes.length / maxDisplayedNodes)
})

const canGoNext = computed(() => currentPage.value < totalPages.value - 1)
const canGoPrevious = computed(() => currentPage.value > 0)

// Computed properties for federated learning
const totalFederatedNodes = computed(() => allFederatedNodes.value.length)
const controlNodes = computed(() => federatedNodes.value.filter(n => ['model', 'control'].includes(n.type)))
const edgeNodes = computed(() => federatedNodes.value.filter(n => n.type === 'training'))
const controlNodesCount = computed(() => controlNodes.value.length)
const edgeNodesCount = computed(() => edgeNodes.value.length)
const maxControlNodes = computed(() => 15)
const maxEdgeNodes = computed(() => 15)

const onlineNodes = computed(() => {
  return allFederatedNodes.value.filter(n => n.status === 'online' || n.status === 'training' || n.status === 'completed').length
})

const trainingNodes = computed(() => {
  return allFederatedNodes.value.filter(n => n.status === 'training').length
})

const dataTransferRate = computed(() => '1.5MB/s')

const averageProgress = computed(() => {
  const trainingNodes = allFederatedNodes.value.filter(n => n.type === 'training')
  if (trainingNodes.length === 0) return 0
  const total = trainingNodes.reduce((sum, node) => sum + (node.trainingProgress || 0), 0)
  return Math.round(total / trainingNodes.length)
})

const networkLatency = computed(() => 18)
const systemHealth = computed(() => 'Good')

// Methods
const goBack = () => {
  router.push('/edgeai/dashboard')
}

// Training control methods
const inviteUser = () => {
  console.log('Inviting user...')
  // In real app, this would open a user invitation modal
}

// Node filtering and pagination methods
const setNodeFilter = (filter) => {
  nodeFilter.value = filter
  currentPage.value = 0 // Reset to first page when filter changes
}

const nextPage = () => {
  if (canGoNext.value) {
    currentPage.value++
  }
}

const previousPage = () => {
  if (canGoPrevious.value) {
    currentPage.value--
  }
}

const addNode = () => {
  // Add a new training node to the pool
  const newNodeId = `training-${String(allFederatedNodes.value.filter(n => n.type === 'training').length + 1).padStart(2, '0')}`
  const newNode = {
    id: newNodeId,
    name: `Training Node ${String(allFederatedNodes.value.filter(n => n.type === 'training').length + 1).padStart(2, '0')}`,
    type: 'training',
    status: 'idle',
    trainingProgress: 0,
    resources: {
      cpu: Math.floor(Math.random() * 30) + 20,
      memory: (Math.random() * 1.5 + 0.5).toFixed(1),
      gpu: Math.floor(Math.random() * 30) + 30
    },
    lastHeartbeat: 'Just connected',
    priority: Math.floor(Math.random() * 5)
  }
  allFederatedNodes.value.push(newNode)
  console.log('New node added:', newNode)
}

const startTraining = async () => {
  if (trainingState.value.status === 'training' || isTrainingStarting.value) return
  
  isTrainingStarting.value = true
  try {
    // 从参数生成后端训练payload
    const payload = { parameters: { ...parameters.value } }
    console.log('🚀 发送训练请求到:', `${TRAIN_API_BASE}/train`, 'payload:', payload)
    // 发送开始训练请求
    const resp = await fetch(`${TRAIN_API_BASE}/train`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'accept': 'application/json' },
      body: JSON.stringify(payload)
    })
    if (!resp.ok) {
      let errorMessage = `Start training failed: ${resp.status}`
      try {
        const errorData = await resp.json()
        errorMessage += ` - ${errorData.message || errorData.error || 'Unknown error'}`
        console.error('❌ 训练启动失败详情:', errorData)
      } catch (e) {
        console.error('❌ 无法解析错误响应:', e)
      }
      throw new Error(errorMessage)
    }
    const data = await resp.json()
    console.log('✅ 训练启动响应:', data)
    trainingTaskId.value = data?.task_id || data?.id || data?.taskId
    currentTaskId.value = trainingTaskId.value
    if (!trainingTaskId.value) {
      throw new Error(`No task_id returned from training service`)
    }
    console.log('📝 保存的 task_id:', trainingTaskId.value)
    // 更新UI状态
    trainingState.value.status = 'training'
    trainingState.value.startTime = Date.now()
    trainingState.value.currentRound = 0
    roundMetrics.value = []
    // 启动轮询监控
    startMonitor()
  } catch (e) {
    console.error('Start training error:', e)
    let errorMsg = '启动训练失败：'
    
    if (e.message.includes('409')) {
      errorMsg += '检测到已有训练任务在运行中。\n\n建议：\n1. 等待当前训练完成\n2. 或联系管理员停止现有训练任务'
    } else if (e.message.includes('400')) {
      errorMsg += '请求参数错误，请检查参数设置。'
    } else if (e.message.includes('500')) {
      errorMsg += '服务器内部错误，请稍后重试。'
    } else if (e.message.includes('Failed to fetch')) {
      errorMsg += '无法连接到训练服务，请检查网络连接和服务状态。'
    } else {
      errorMsg += e.message || '未知错误，请稍后重试。'
    }
    
    alert(errorMsg)
  } finally {
    isTrainingStarting.value = false
  }
}

const completeTraining = () => {
  if (trainingState.value.status === 'training') {
    trainingState.value.status = 'completed'
    trainingState.value.endTime = Date.now()
    
    // Mark all training nodes as completed
    allFederatedNodes.value.forEach(node => {
      if (node.type === 'training') {
        node.status = 'completed'
        node.trainingProgress = 100
      }
    })
    
    console.log('Training completed')
  }
}

const stopTraining = async () => {
  if (trainingState.value.status !== 'training' && trainingState.value.status !== 'running' || isTrainingStopping.value) return
  
  isTrainingStopping.value = true
  try {
    // 停止监控
    stopMonitor()
    
    // 更新状态
    trainingState.value.status = 'stopped'
    trainingState.value.endTime = Date.now()
    
    // 重置任务ID
    currentTaskId.value = null
    trainingTaskId.value = null
    
    console.log('Training stopped')
  } catch (e) {
    console.error('Stop training error:', e)
  } finally {
    isTrainingStopping.value = false
  }
}

// 轮询监控训练进度
const startMonitor = () => {
  stopMonitor()
  if (!trainingTaskId.value) return
  monitorTimer.value = setInterval(async () => {
    try {
      console.log('🔍 轮询监控 task_id:', trainingTaskId.value)
      const resp = await fetch(`${TRAIN_API_BASE}/monitor/${trainingTaskId.value}`, {
        method: 'GET',
        headers: { 'accept': 'application/json' }
      })
      if (!resp.ok) {
        let errorMessage = `Monitor failed: ${resp.status}`
        try {
          const errorData = await resp.json()
          errorMessage += ` - ${errorData.message || errorData.error || 'Unknown error'}`
          console.error('❌ 监控失败详情:', errorData)
        } catch (e) {
          console.error('❌ 无法解析监控错误响应:', e)
        }
        throw new Error(errorMessage)
      }
      const data = await resp.json()
      console.log('📊 监控响应:', data)
      // 解析后端返回结构
      const current = Number(data.current_round ?? data.round ?? trainingState.value.currentRound)
      const total = Number(data.total_rounds ?? trainingState.value.totalRounds)
      const loss = data.loss
      const accuracy = data.accuracy
      console.log('📈 解析数据 - current:', current, 'total:', total, 'loss:', loss, 'accuracy:', accuracy)
      trainingState.value.currentRound = current
      if (Number.isFinite(total) && total > 0) trainingState.value.totalRounds = total
      if (Number.isFinite(current)) {
        const last = roundMetrics.value[roundMetrics.value.length - 1]
        if (!last || last.round !== current) {
          roundMetrics.value.push({ round: current, loss, accuracy })
          console.log('➕ 新增轮次指标:', { round: current, loss, accuracy })
        } else {
          last.loss = loss; last.accuracy = accuracy
          console.log('🔄 更新轮次指标:', { round: current, loss, accuracy })
        }
      }
      if (total && current >= total) {
        trainingState.value.status = 'completed'
        console.log('🏁 训练完成!')
        stopMonitor()
      }
    } catch (e) {
      console.error('Monitor error:', e)
      // 如果是404错误，说明任务不存在，停止监控
      if (e.message.includes('404')) {
        console.log('🛑 训练任务不存在，停止监控')
        stopMonitor()
        trainingState.value.status = 'stopped'
      } else if (e.message.includes('Failed to fetch')) {
        console.log('🌐 网络连接问题，继续尝试监控...')
      } else {
        console.log('⚠️ 监控错误，继续尝试...')
      }
    }
  }, 2000)
}

const stopMonitor = () => {
  if (monitorTimer.value) {
    clearInterval(monitorTimer.value)
    monitorTimer.value = null
  }
}

// 任务管理方法
const loadTaskList = async () => {
  isLoadingTasks.value = true
  try {
    console.log('📋 加载任务列表...')
    const resp = await fetch(`${TRAIN_API_BASE}/tasksList`, {
      method: 'GET',
      headers: { 'accept': 'application/json' }
    })
    if (!resp.ok) {
      let errorMessage = `Load tasks failed: ${resp.status}`
      try {
        const errorData = await resp.json()
        errorMessage += ` - ${errorData.message || errorData.error || 'Unknown error'}`
        console.error('❌ 加载任务失败详情:', errorData)
      } catch (e) {
        console.error('❌ 无法解析错误响应:', e)
      }
      throw new Error(errorMessage)
    }
    const data = await resp.json()
    console.log('✅ 任务列表响应:', data)
    const newTaskList = data.tasks || []
    console.log('📋 更新任务列表:', { 
      oldCount: taskList.value.length, 
      newCount: newTaskList.length, 
      tasks: newTaskList 
    })
    taskList.value = newTaskList

    // 并行查询每个任务的状态
    await refreshAllTaskStatuses()
    // 加载后滚动到底部，便于查看最新任务
    setTimeout(scrollControlPanelBottom, 0)
  } catch (e) {
    console.error('Load task list error:', e)
    alert(`加载任务列表失败：${e.message}`)
  } finally {
    isLoadingTasks.value = false
  }
}

const refreshAllTaskStatuses = async () => {
  if (!Array.isArray(taskList.value) || taskList.value.length === 0) {
    taskStatusMap.value = {}
    return
  }
  console.log('🔎 并行查询任务状态...', taskList.value)
  const entries = await Promise.all(taskList.value.map(async (taskId) => {
    try {
      const resp = await fetch(`${TRAIN_API_BASE}/monitor/${taskId}`, {
        method: 'GET', headers: { accept: 'application/json' }
      })
      if (!resp.ok) throw new Error(`status ${resp.status}`)
      const status = await resp.json()
      return [taskId, {
        current_round: Number(status.current_round ?? 0),
        total_rounds: Number(status.total_rounds ?? 0),
        loss: typeof status.loss === 'number' ? status.loss : 0,
        accuracy: status.accuracy
      }]
    } catch (err) {
      console.warn('获取任务状态失败:', taskId, err.message)
      return [taskId, { current_round: 0, total_rounds: 0, loss: 0, accuracy: null }]
    }
  }))
  taskStatusMap.value = Object.fromEntries(entries)
  console.log('📦 任务状态缓存:', taskStatusMap.value)
}

const deleteTask = async (taskId) => {
  if (isDeletingTask.value) return
  
  isDeletingTask.value = taskId
  try {
    console.log('🗑️ 删除任务:', taskId)
    const resp = await fetch(`${TRAIN_API_BASE}/tasks/${taskId}`, {
      method: 'DELETE',
      headers: { 'accept': 'application/json' }
    })
    if (!resp.ok) {
      let errorMessage = `Delete task failed: ${resp.status}`
      try {
        const errorData = await resp.json()
        errorMessage += ` - ${errorData.message || errorData.error || 'Unknown error'}`
        console.error('❌ 删除任务失败详情:', errorData)
      } catch (e) {
        console.error('❌ 无法解析错误响应:', e)
      }
      throw new Error(errorMessage)
    }
    const data = await resp.json()
    console.log('✅ 删除任务响应:', data)
    console.log('🗑️ 删除详情:', {
      taskId: taskId,
      status: data.status,
      terminated: data.terminated,
      reason: data.detail?.reason
    })
    
    // 从列表中移除已删除的任务
    taskList.value = taskList.value.filter(task => task !== taskId)
    delete taskStatusMap.value[taskId]
    
    // 如果删除的是当前训练任务，停止监控
    if (taskId === trainingTaskId.value) {
      stopMonitor()
      trainingState.value.status = 'stopped'
      currentTaskId.value = null
      trainingTaskId.value = null
    }
    
    // 延迟1秒后重新加载任务列表并刷新状态，确保后端状态同步
    setTimeout(async () => {
      console.log('🔄 删除后重新加载任务列表...')
      await loadTaskList()
    }, 1000)
    
    alert(`任务 ${taskId.substring(0, 8)}... 已成功删除`)
  } catch (e) {
    console.error('Delete task error:', e)
    alert(`删除任务失败：${e.message}`)
  } finally {
    isDeletingTask.value = null
  }
}

const resetView = () => {
  if (networkViz.value) {
    networkViz.value.resetView()
  }
}

const testDataTransmission = () => {
  // 手动触发所有连接的数据传输测试
  federatedConnections.value.forEach((connection, index) => {
    setTimeout(() => {
      const directions = ['upstream', 'downstream', 'bidirectional']
      const randomDirection = directions[index % directions.length]
      triggerTransmission(connection.id, randomDirection, 3000)
      console.log(`Testing data flow: ${connection.from} -> ${connection.to} (${randomDirection})`)
    }, index * 500) // 每个连接延迟500ms，避免同时触发
  })
}

// 数据传输模拟
const simulateDataTransmission = () => {
  if (trainingState.value.status === 'training') {
    federatedConnections.value.forEach(connection => {
      const trainingNode = allFederatedNodes.value.find(n => n.id === connection.to)
      
      if (trainingNode && trainingNode.status === 'training') {
        // 随机触发不同类型的数据传输
        const random = Math.random()
        
        if (random < 0.15) {
          // 15% 概率：参数下发 (模型节点 → 训练节点)
          triggerTransmission(connection.id, 'downstream', 1800)
        } else if (random < 0.25) {
          // 10% 概率：梯度上传 (训练节点 → 模型节点)
          triggerTransmission(connection.id, 'upstream', 2200) 
        } else if (random < 0.30) {
          // 5% 概率：双向同步
          triggerTransmission(connection.id, 'bidirectional', 2500)
        }
      }
    })
  }
}

// Simulation methods
const simulateTraining = () => {
  if (trainingState.value.status === 'training') {
    const completedInThisRound = []
    
    // Increment training round periodically
    if (Math.random() < 0.1) { // 10% chance to increment round
      trainingState.value.currentRound = Math.min(
        trainingState.value.totalRounds, 
        trainingState.value.currentRound + 1
      )
    }
    
    // Update training progress for all training nodes
    allFederatedNodes.value.forEach(node => {
      if (node.type === 'training' && node.status === 'training') {
        const increment = Math.random() * 3 + 0.5 // 0.5-3.5% increment
        node.trainingProgress = Math.min(100, (node.trainingProgress || 0) + increment)
        
        // Update resources simulation
        if (node.resources) {
          node.resources.cpu = Math.max(50, Math.min(100, node.resources.cpu + (Math.random() - 0.5) * 10))
          node.resources.gpu = Math.max(60, Math.min(100, node.resources.gpu + (Math.random() - 0.5) * 8))
        }
        
        // Update heartbeat
        const heartbeats = ['1 sec ago', '2 sec ago', '3 sec ago', '4 sec ago', '5 sec ago']
        node.lastHeartbeat = heartbeats[Math.floor(Math.random() * heartbeats.length)]
        
        // Mark as completed if progress reaches 100%
        if (node.trainingProgress >= 100) {
          node.status = 'completed'
          node.trainingProgress = 100
          completedInThisRound.push(node.id)
          
          // 触发淡出动画
          triggerNodeFadeOut(node.id)
          console.log(`Node ${node.name} completed training, starting fade-out animation`)
        }
      }
    })
    
    // 处理完成的节点，尝试替换为新的训练节点
    completedInThisRound.forEach(completedNodeId => {
      setTimeout(() => {
        const replaced = replaceCompletedNode()
        if (!replaced) {
          console.log('No idle nodes available for replacement')
        }
      }, 1500) // 1.5秒后尝试替换，让用户看到淡出效果
    })
    
    // Simulate data transmission
    simulateDataTransmission()
    
    // Randomly start training on some idle nodes (reduced probability)
    const idleNodes = allFederatedNodes.value.filter(n => n.type === 'training' && n.status === 'idle')
    if (idleNodes.length > 0 && Math.random() < 0.05) { // 降低概率，避免太频繁
      const randomNode = idleNodes[Math.floor(Math.random() * idleNodes.length)]
      randomNode.status = 'training'
      randomNode.trainingProgress = Math.floor(Math.random() * 5) // 从0-5%开始
      console.log(`Node ${randomNode.name} started training`)
    }
    
    // 检查是否所有训练都已完成
    if (!checkAllTrainingCompleted()) {
      // Continue simulation only if not all training is completed
      setTimeout(simulateTraining, 2000) // Update every 2 seconds
    }
  }
}

// 节点详细信息面板状态
const selectedNode = ref(null)
const isClosing = ref(false)

// 模态框状态
const isModalVisible = ref(false)
const modalSelectedNode = ref(null)
const modalAnchorPosition = ref({ x: 0, y: 0 })

// 参数设置模态框状态
const isSettingsModalVisible = ref(false)

// 训练参数配置
const parameters = ref({
  training_alg: 'sft',
  fed_alg: 'fedavg',
  secure_aggregation: 'shamir_threshold',
  num_computers: 3,
  threshold: 2,
  num_rounds: 10,
  num_clients: 2,
  sample_clients: 2,
  max_steps: 100,
  lr: '1e-4',
  model_name_or_path: 'sshleifer/tiny-gpt2',
  dataset_name: 'vicgalle/alpaca-gpt4',
  dataset_sample: 50
})

// 默认参数配置
const defaultParameters = {
  training_alg: 'sft',
  fed_alg: 'fedavg',
  secure_aggregation: 'shamir_threshold',
  num_computers: 3,
  threshold: 2,
  num_rounds: 10,
  num_clients: 2,
  sample_clients: 2,
  max_steps: 100,
  lr: '1e-4',
  model_name_or_path: 'sshleifer/tiny-gpt2',
  dataset_name: 'vicgalle/alpaca-gpt4',
  dataset_sample: 50
}

// Event handlers
const handleNodeClick = (node) => {
  if (!node || !node.id) {
    console.error('Invalid node data received for update:', node)
    return
  }
  console.log('Node clicked - Type:', node.type, 'Name:', node.name, 'ID:', node.id)
  selectedNode.value = node
  isClosing.value = false
  // No longer using modal, details shown in left panel
}

const closeNodeDetails = () => {
  isClosing.value = true
  // 等待淡出动画完成后再隐藏面板
  setTimeout(() => {
    selectedNode.value = null
    isClosing.value = false
  }, 800) // 与动画时长保持一致
}

// 模态框控制函数
const openNodeModal = (node, anchorPosition = null) => {
  modalSelectedNode.value = node
  if (anchorPosition) {
    modalAnchorPosition.value = anchorPosition
  }
  isModalVisible.value = true
}

const closeNodeModal = () => {
  isModalVisible.value = false
  setTimeout(() => {
    modalSelectedNode.value = null
  }, 300)
}

// 处理表格中的详情按钮点击
const handleTableNodeDetails = (node) => {
  openNodeModal(node)
}

// All hover functionality removed

const handleConnectionClick = (connection) => {
  console.log('Connection clicked:', connection)
}

const viewNodeDetails = (node, event) => {
  // 获取整个表格行的位置（而不是按钮位置）
  const rowElement = event.target.closest('tr')
  if (!rowElement) {
    console.warn('Could not find table row element')
    // 回退到按钮位置
    const buttonRect = event.target.getBoundingClientRect()
    const anchorPosition = {
      x: buttonRect.left + buttonRect.width / 2,
      y: buttonRect.top + buttonRect.height / 2
    }
    openNodeModal(node, anchorPosition)
    return
  }

  // 计算行的中心位置
  const rowRect = rowElement.getBoundingClientRect()
  const anchorPosition = {
    x: rowRect.left + rowRect.width / 2,
    y: rowRect.top + rowRect.height / 2
  }

  // 使用模态框替代侧边面板
  openNodeModal(node, anchorPosition)
  console.log('Opening node details modal:', node, 'at row center position:', anchorPosition, 'row rect:', rowRect)
}

const startNodeTraining = (node) => {
  if (node.status === 'idle') {
    node.status = 'training'
    node.trainingProgress = Math.floor(Math.random() * 5) // Start from 0-5%
    console.log(`Started training for node: ${node.name}`)
  }
}

const stopNodeTraining = (node) => {
  if (node.status === 'training') {
    node.status = 'idle'
    node.trainingProgress = Math.floor(node.trainingProgress || 0) // Keep current progress
    console.log(`Stopped training for node: ${node.name}`)
  }
}

// 参数设置相关方法
const openSettingsModal = () => {
  isSettingsModalVisible.value = true
  loadParametersFromStorage()
}

const closeSettingsModal = () => {
  isSettingsModalVisible.value = false
}

const loadParametersFromStorage = () => {
  try {
    const savedParameters = localStorage.getItem('edgeai-training-parameters')
    if (savedParameters) {
      const parsed = JSON.parse(savedParameters)
      parameters.value = { ...defaultParameters, ...parsed }
    }
  } catch (error) {
    console.error('Failed to load parameters from storage:', error)
    parameters.value = { ...defaultParameters }
  }
}

const saveParameters = () => {
  try {
    // 验证参数
    if (parameters.value.threshold > parameters.value.num_computers) {
      alert('阈值不能大于计算机数量')
      return
    }
    
    if (parameters.value.sample_clients > parameters.value.num_clients) {
      alert('采样客户端数量不能大于客户端总数')
      return
    }

    // 保存到localStorage
    localStorage.setItem('edgeai-training-parameters', JSON.stringify(parameters.value))
    
    // 更新训练配置显示
    updateTrainingConfigDisplay()
    
    // 关闭模态框
    closeSettingsModal()
    
    console.log('Parameters saved:', parameters.value)
    
    // 显示成功消息
    alert('参数设置已保存！')
  } catch (error) {
    console.error('Failed to save parameters:', error)
    alert('保存参数时出错，请重试')
  }
}

const resetToDefaults = () => {
  if (confirm('确定要重置为默认参数吗？这将覆盖当前的所有设置。')) {
    parameters.value = { ...defaultParameters }
  }
}

const updateTrainingConfigDisplay = () => {
  // 更新训练配置显示，让用户看到参数变化
  trainingConfig.value = {
    aiModel: parameters.value.model_name_or_path,
    strategy: parameters.value.training_alg.toUpperCase(),
    protocol: parameters.value.fed_alg,
    targetAccuracy: `≥90%`,
    estimatedCompletion: `${parameters.value.num_rounds} rounds`
  }
  // 同步训练轮次到控制面板
  const parsedRounds = Number(parameters.value.num_rounds)
  trainingState.value.totalRounds = Number.isFinite(parsedRounds) && parsedRounds > 0 ? parsedRounds : 100
}

// Helper methods
const getNodeColorClass = (type) => {
  const classes = {
    model: 'bg-blue-500',
    control: 'bg-red-500',
    training: 'bg-green-500'
  }
  return classes[type] || 'bg-gray-500'
}

const getNodeStatusBadgeClass = (status) => {
  const classes = {
    online: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    training: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    completed: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    offline: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getTrainingStatusBadgeClass = (status) => {
  const classes = {
    idle: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300',
    training: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    completed: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getTrainingStatusText = (status) => {
  const texts = {
    idle: 'Ready',
    training: 'Training',
    completed: 'Completed'
  }
  return texts[status] || 'Unknown'
}

// Sorting functions
const sortNodes = (key) => {
  if (sortConfig.value.key === key) {
    // Toggle direction if same key
    sortConfig.value.direction = sortConfig.value.direction === 'asc' ? 'desc' : 'asc'
  } else {
    // Set new key with ascending direction
    sortConfig.value.key = key
    sortConfig.value.direction = 'asc'
  }
}

const getSortIcon = (key) => {
  if (sortConfig.value.key !== key) {
    return '⇅' // No sort - elegant double arrow
  }
  return sortConfig.value.direction === 'asc' ? '▲' : '▼' // Modern triangular arrows
}

// Sorted training nodes for table display
const sortedTrainingNodes = computed(() => {
  const nodes = allFederatedNodes.value.filter(n => n.type === 'training')
  
  return nodes.sort((a, b) => {
    const { key, direction } = sortConfig.value
    let aValue, bValue
    
    switch (key) {
      case 'name':
        aValue = a.name || a.id
        bValue = b.name || b.id
        break
      case 'status':
        aValue = a.status
        bValue = b.status
        break
      case 'trainingProgress':
        aValue = a.trainingProgress || 0
        bValue = b.trainingProgress || 0
        break
      case 'cpu':
        aValue = a.resources?.cpu || 0
        bValue = b.resources?.cpu || 0
        break
      case 'memory':
        aValue = parseFloat(a.resources?.memory || 0)
        bValue = parseFloat(b.resources?.memory || 0)
        break
      case 'gpu':
        aValue = a.resources?.gpu || 0
        bValue = b.resources?.gpu || 0
        break
      case 'lastHeartbeat':
        aValue = a.lastHeartbeat || ''
        bValue = b.lastHeartbeat || ''
        break
      default:
        aValue = a.name || a.id
        bValue = b.name || b.id
    }
    
    // Handle string comparison
    if (typeof aValue === 'string' && typeof bValue === 'string') {
      const comparison = aValue.localeCompare(bValue)
      return direction === 'asc' ? comparison : -comparison
    }
    
    // Handle numeric comparison
    if (direction === 'asc') {
      return aValue - bValue
    } else {
      return bValue - aValue
    }
  })
})

onMounted(async () => {
  // Initialize EdgeAI visualization with real data
  console.log('EdgeAI Visualization Dashboard mounted')
  
  // Load initial data
  await loadVisualizationData()
  
  // 首次拉取 Ray 集群节点
  await loadNodesData()
  
  // Load parameters from storage
  loadParametersFromStorage()
  
  // Update training config display with loaded parameters
  updateTrainingConfigDisplay()
  
  // Load task list
  await loadTaskList()
  
  // Setup auto-refresh for real-time updates
  setupAutoRefresh()
  
  // Connect to EdgeAI store WebSocket for real-time updates
  // This will gracefully handle connection failures and switch to offline mode
  try {
    edgeaiStore.connectWebSocket()
  } catch (error) {
    console.warn('WebSocket connection failed, continuing in offline mode:', error)
  }
})

onUnmounted(() => {
  // Clean up resources
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  stopMonitor()
  
  // Clear API cache
  clearCache()
  
  // Clean up any running training simulations
  if (trainingState.value.status === 'training') {
    trainingState.value.status = 'idle'
  }
})
</script>