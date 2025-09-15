<template>
  <div class="federated-learning-dashboard min-h-screen bg-gray-50 dark:bg-gray-900">
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

          <!-- Basic Information -->
          <div class="space-y-3">
            <h5 class="text-sm font-medium text-gray-900 dark:text-white">Basic Information</h5>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Type</span>
                <span class="font-medium text-gray-900 dark:text-white capitalize">{{ selectedNode.type }}</span>
              </div>
              <div v-if="selectedNode.role" class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Role</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.role }}</span>
              </div>
              <div v-if="selectedNode.user" class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Responsible User</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.user }}</span>
              </div>
              <div v-if="selectedNode.ipAddress" class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">IP Address</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.ipAddress }}</span>
              </div>
              <div v-if="selectedNode.lastHeartbeat" class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Last Heartbeat</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.lastHeartbeat }}</span>
              </div>
            </div>
          </div>

          <!-- Training Progress (for training nodes) -->
          <div v-if="selectedNode.type === 'training'" class="space-y-3">
            <h5 class="text-sm font-medium text-gray-900 dark:text-white">Training Progress</h5>
            <div class="space-y-3">
              <div>
                <div class="flex justify-between mb-2">
                  <span class="text-sm text-gray-500 dark:text-gray-400">Progress</span>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedNode.trainingProgress || 0 }}%</span>
                </div>
                <div class="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-full">
                  <div 
                    class="h-2 bg-gradient-to-r from-blue-500 to-green-500 rounded-full transition-all duration-500"
                    :style="{ width: `${selectedNode.trainingProgress || 0}%` }"
                  ></div>
                </div>
              </div>
              <div v-if="selectedNode.priority !== undefined" class="flex justify-between">
                <span class="text-sm text-gray-500 dark:text-gray-400">Priority Level</span>
                <span class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedNode.priority }}/10</span>
              </div>
            </div>
          </div>

          <!-- Connection Info (for control nodes) -->
          <div v-if="selectedNode.type === 'control' || selectedNode.type === 'model'" class="space-y-3">
            <h5 class="text-sm font-medium text-gray-900 dark:text-white">Connection Information</h5>
            <div class="space-y-2 text-sm">
              <div v-if="selectedNode.connectedNodes" class="flex justify-between">
                <span class="text-gray-500 dark:text-gray-400">Connected Nodes</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ selectedNode.connectedNodes }}</span>
              </div>
            </div>
          </div>

          <!-- System Resources (for training nodes) -->
          <div v-if="selectedNode.type === 'training' && selectedNode.resources" class="space-y-3">
            <h5 class="text-sm font-medium text-gray-900 dark:text-white">System Resources</h5>
            <div class="space-y-3">
              <!-- CPU -->
              <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                <div class="flex justify-between mb-2">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">CPU Usage</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.resources.cpu }}%</span>
                </div>
                <div class="w-full h-1.5 bg-gray-200 dark:bg-gray-600 rounded-full">
                  <div 
                    class="h-1.5 bg-blue-500 rounded-full transition-all duration-300"
                    :style="{ width: `${selectedNode.resources.cpu}%` }"
                  ></div>
                </div>
              </div>

              <!-- Memory -->
              <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                <div class="flex justify-between mb-2">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Memory Usage</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.resources.memory }}GB</span>
                </div>
                <div class="w-full h-1.5 bg-gray-200 dark:bg-gray-600 rounded-full">
                  <div 
                    class="h-1.5 bg-green-500 rounded-full transition-all duration-300"
                    :style="{ width: `${Math.min(100, parseFloat(selectedNode.resources.memory) * 40)}%` }"
                  ></div>
                </div>
              </div>

              <!-- GPU -->
              <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                <div class="flex justify-between mb-2">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">GPU Usage</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.resources.gpu }}%</span>
                </div>
                <div class="w-full h-1.5 bg-gray-200 dark:bg-gray-600 rounded-full">
                  <div 
                    class="h-1.5 bg-purple-500 rounded-full transition-all duration-300"
                    :style="{ width: `${selectedNode.resources.gpu}%` }"
                  ></div>
                </div>
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
        <div class="w-64 flex-shrink-0 bg-white dark:bg-gray-900 m-6 ml-0 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 h-[900px] overflow-y-auto">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">Control Panel</h3>
        
        <!-- Training Progress -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Training Progress</h4>
          
          <!-- Overall Progress -->
          <div class="mb-4">
            <div class="flex items-center justify-between text-sm mb-2">
              <span class="text-gray-600 dark:text-gray-400">Overall Progress</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ averageProgress }}%</span>
            </div>
            <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full">
              <div 
                class="h-3 bg-gradient-to-r from-blue-500 to-green-500 rounded-full transition-all duration-500"
                :style="{ width: `${averageProgress}%` }"
              ></div>
            </div>
          </div>
          
          <!-- Training Rounds Progress -->
          <div class="mb-4">
            <div class="flex items-center justify-between text-sm mb-2">
              <span class="text-gray-600 dark:text-gray-400">Training Rounds</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ trainingState.currentRound }}/{{ trainingState.totalRounds }}</span>
            </div>
            <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full">
              <div 
                class="h-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full transition-all duration-500"
                :style="{ width: `${(trainingState.currentRound / trainingState.totalRounds) * 100}%` }"
              ></div>
            </div>
          </div>
          
          <!-- Active Training Nodes -->
          <div class="mb-4">
            <div class="flex items-center justify-between text-sm mb-2">
              <span class="text-gray-600 dark:text-gray-400">Active Training Nodes</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ trainingNodes }}/{{ maxDisplayedNodes }}</span>
            </div>
            <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full">
              <div 
                class="h-3 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full transition-all duration-500"
                :style="{ width: `${(trainingNodes / maxDisplayedNodes) * 100}%` }"
              ></div>
            </div>
          </div>
          
          <!-- Training Status -->
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Status</span>
            <span 
              class="px-2 py-1 text-xs font-medium rounded-full"
              :class="getTrainingStatusBadgeClass(trainingState.status)"
            >
              {{ getTrainingStatusText(trainingState.status) }}
            </span>
          </div>
        </div>

        <!-- Essential Training Controls -->
        <div class="space-y-3 mb-8">
          <Button 
            @click="startTraining"
            variant="primary"
            size="sm"
            class="w-full flex items-center justify-center space-x-2"
            :disabled="trainingState.status === 'training'"
          >
            <PlayIcon class="w-4 h-4" />
            <span>{{ trainingState.status === 'training' ? 'Training...' : 'Start Training' }}</span>
          </Button>
          
          <Button 
            @click="completeTraining"
            variant="outline"
            size="sm"
            class="w-full flex items-center justify-center space-x-2"
            :disabled="trainingState.status !== 'training'"
          >
            <CheckCircleIcon class="w-4 h-4" />
            <span>Complete Training</span>
          </Button>
        </div>
        
        <!-- Real-time Status -->
        <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-4">Real-time Status</h4>
          
          <div class="space-y-4">
            <!-- Online Nodes -->
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ onlineNodes }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Online Nodes</div>
            </div>
            
            <!-- Training Nodes -->
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ trainingNodes }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Training</div>
            </div>
            
            <!-- Data Transfer -->
            <div class="text-center">
              <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ dataTransferRate }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Data Transfer</div>
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
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
          <!-- Total Nodes -->
          <div class="flex items-center space-x-3">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                <ServerIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
              </div>
            </div>
            <div>
              <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ totalFederatedNodes }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Total Nodes</div>
            </div>
          </div>

          <!-- Average Progress -->
          <div class="flex items-center space-x-3">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                <BeakerIcon class="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
            </div>
            <div>
              <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ averageProgress }}%</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Average Progress</div>
            </div>
          </div>

          <!-- Network Latency -->
          <div class="flex items-center space-x-3">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 dark:bg-yellow-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/>
                </svg>
              </div>
            </div>
            <div>
              <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ networkLatency }}ms</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Network Latency</div>
            </div>
          </div>

          <!-- System Health -->
          <div class="flex items-center space-x-3">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
            </div>
            <div>
              <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ systemHealth }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">System Health</div>
            </div>
          </div>
        </div>

        <!-- Additional Training Controls -->
        <div class="mb-4">
          <h3 class="text-md font-semibold text-gray-900 dark:text-white mb-3">Training Controls</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
            <Button 
              @click="inviteUser"
              variant="outline"
              size="sm"
              class="flex items-center justify-center space-x-2"
            >
              <UserPlusIcon class="w-4 h-4" />
              <span>Invite User</span>
            </Button>
            
            <Button 
              @click="addNode"
              variant="outline"
              size="sm"
              class="flex items-center justify-center space-x-2"
            >
              <ServerIcon class="w-4 h-4" />
              <span>Add Node</span>
            </Button>
            
            <Button 
              @click="resetView"
              variant="outline"
              size="sm"
              class="flex items-center justify-center space-x-2"
            >
              <ArrowPathIcon class="w-4 h-4" />
              <span>Reset View</span>
            </Button>
            
            <Button 
              @click="testDataTransmission"
              variant="outline"
              size="sm"
              class="flex items-center justify-center space-x-2"
            >
              <CogIcon class="w-4 h-4" />
              <span>Test Data Flow</span>
            </Button>
          </div>
        </div>

        <!-- Node Details List -->
        <div class="mb-3">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-md font-semibold text-gray-900 dark:text-white">Node Details List</h3>
            <div class="text-sm text-gray-500 dark:text-gray-400">
              Control Nodes: <span class="font-medium text-green-600">{{ controlNodesCount }}</span> • 
              Edge Nodes: <span class="font-medium text-blue-600">{{ edgeNodesCount }}</span> • 
              Total: <span class="font-medium text-gray-900 dark:text-white">{{ totalFederatedNodes }}</span>
            </div>
          </div>

          <!-- Control Nodes Table -->
          <div class="mb-3">
            <h4 class="text-sm font-medium text-green-600 dark:text-green-400 mb-2">
              Control Nodes (Max {{ maxControlNodes }})
            </h4>
            <div class="overflow-x-auto bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
              <table class="w-full text-sm">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Node Name</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Role</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Status</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Responsible User</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">IP Address</th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Connected Nodes</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="node in controlNodes" 
                    :key="node.id"
                    class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700/50"
                  >
                    <td class="p-3">
                      <div class="flex items-center space-x-3">
                        <div :class="getNodeColorClass(node.type)" class="w-3 h-3 rounded-full"></div>
                        <span class="font-medium text-gray-900 dark:text-white">{{ node.name }}</span>
                      </div>
                    </td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ node.role }}</td>
                    <td class="p-3">
                      <span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                        {{ node.status }}
                      </span>
                    </td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ node.user }}</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ node.ipAddress }}</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ node.connectedNodes }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Edge/Training Nodes Table -->
          <div>
            <h4 class="text-sm font-medium text-blue-600 dark:text-blue-400 mb-2">
              Edge Nodes ({{ allFederatedNodes.filter(n => n.type === 'training').length }} total)
            </h4>
            <div class="overflow-x-auto bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
              <table class="w-full text-sm">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th 
                      @click="sortNodes('name')"
                      class="text-left p-3 font-medium text-gray-900 dark:text-white cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    >
                      <div class="flex items-center space-x-1">
                        <span>Node Name</span>
                        <span class="text-xs">{{ getSortIcon('name') }}</span>
                      </div>
                    </th>
                    <th 
                      @click="sortNodes('status')"
                      class="text-left p-3 font-medium text-gray-900 dark:text-white cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    >
                      <div class="flex items-center space-x-1">
                        <span>Status</span>
                        <span class="text-xs">{{ getSortIcon('status') }}</span>
                      </div>
                    </th>
                    <th 
                      @click="sortNodes('trainingProgress')"
                      class="text-left p-3 font-medium text-gray-900 dark:text-white cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    >
                      <div class="flex items-center space-x-1">
                        <span>Training Progress</span>
                        <span class="text-xs">{{ getSortIcon('trainingProgress') }}</span>
                      </div>
                    </th>
                    <th 
                      @click="sortNodes('cpu')"
                      class="text-left p-3 font-medium text-gray-900 dark:text-white cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    >
                      <div class="flex items-center space-x-1">
                        <span>CPU</span>
                        <span class="text-xs">{{ getSortIcon('cpu') }}</span>
                      </div>
                    </th>
                    <th 
                      @click="sortNodes('memory')"
                      class="text-left p-3 font-medium text-gray-900 dark:text-white cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    >
                      <div class="flex items-center space-x-1">
                        <span>Memory</span>
                        <span class="text-xs">{{ getSortIcon('memory') }}</span>
                      </div>
                    </th>
                    <th 
                      @click="sortNodes('gpu')"
                      class="text-left p-3 font-medium text-gray-900 dark:text-white cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    >
                      <div class="flex items-center space-x-1">
                        <span>GPU</span>
                        <span class="text-xs">{{ getSortIcon('gpu') }}</span>
                      </div>
                    </th>
                    <th 
                      @click="sortNodes('lastHeartbeat')"
                      class="text-left p-3 font-medium text-gray-900 dark:text-white cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    >
                      <div class="flex items-center space-x-1">
                        <span>Last Heartbeat</span>
                        <span class="text-xs">{{ getSortIcon('lastHeartbeat') }}</span>
                      </div>
                    </th>
                    <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="node in sortedTrainingNodes" 
                    :key="node.id"
                    class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700/50"
                  >
                    <td class="p-3">
                      <div class="flex items-center space-x-3">
                        <div :class="getNodeColorClass(node.type)" class="w-3 h-3 rounded-full"></div>
                        <span class="font-medium text-gray-900 dark:text-white">{{ node.name }}</span>
                      </div>
                    </td>
                    <td class="p-3">
                      <span 
                        :class="getNodeStatusBadgeClass(node.status)"
                        class="px-2 py-1 text-xs font-medium rounded-full"
                      >
                        {{ node.status }}
                      </span>
                    </td>
                    <td class="p-3">
                      <div class="flex items-center space-x-2">
                        <div class="w-16 h-2 bg-gray-200 dark:bg-gray-600 rounded-full">
                          <div 
                            class="h-2 bg-blue-600 rounded-full transition-all duration-500"
                            :style="{ width: `${node.trainingProgress || 0}%` }"
                          ></div>
                        </div>
                        <span class="text-sm font-medium text-gray-900 dark:text-white">{{ node.trainingProgress || 0 }}%</span>
                      </div>
                    </td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ node.resources?.cpu || 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ node.resources?.memory || 0 }}GB</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ node.resources?.gpu || 0 }}%</td>
                    <td class="p-3 text-gray-600 dark:text-gray-400">{{ node.lastHeartbeat || '-' }}</td>
                    <td class="p-3">
                      <Button 
                        @click="viewNodeDetails(node)" 
                        variant="ghost" 
                        size="xs"
                      >
                        View Details
                      </Button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
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
import FederatedNetworkVisualization from '@/components/edgeai/FederatedNetworkVisualization.vue'
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

// Loading and error states
const loading = ref(false)
const error = ref(null)
const refreshInterval = ref(null)

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

// Current project (will be loaded from API)
const currentProject = ref({
  name: 'Loading...',
  status: 'loading'
})

// All Available Federated Learning Nodes (will be loaded from API)
const allFederatedNodes = ref([])

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
      trainingConfig.value = {
        aiModel: configResult.ai_model || 'Unknown Model',
        strategy: configResult.strategy || 'Unknown Strategy', 
        protocol: configResult.protocol || 'fedavg',
        targetAccuracy: configResult.target_accuracy || '≥90%',
        estimatedCompletion: configResult.estimated_completion || 'Unknown'
      }
    }

    // Update nodes data
    if (nodesResult && Array.isArray(nodesResult)) {
      allFederatedNodes.value = nodesResult.map(node => ({
        id: node.id,
        name: node.name || `Node ${node.id}`,
        type: node.type || 'training',
        status: node.status || 'idle',
        role: node.role || 'Participant',
        user: node.user || 'System',
        ipAddress: node.ip_address || 'Unknown',
        connectedNodes: node.connected_nodes || '0 nodes',
        trainingProgress: node.training_progress || 0,
        resources: {
          cpu: node.resources?.cpu || 0,
          memory: node.resources?.memory || '0.0',
          gpu: node.resources?.gpu || 0
        },
        lastHeartbeat: node.last_heartbeat || 'Unknown',
        priority: node.priority || 1
      }))
    }

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
      // Only refresh nodes data for real-time updates
      loadNodesData()
    }
  }, 15 * 1000) // Refresh every 15 seconds
}

// Load only nodes data for real-time updates
const loadNodesData = async () => {
  try {
    const projectId = route.params.projectId
    const nodesResult = await edgeaiService.nodes.getVisualizationNodes(projectId)
    
    if (nodesResult && Array.isArray(nodesResult)) {
      // Update existing nodes or add new ones
      const updatedNodes = nodesResult.map(node => ({
        id: node.id,
        name: node.name || `Node ${node.id}`,
        type: node.type || 'training',
        status: node.status || 'idle',
        role: node.role || 'Participant',
        user: node.user || 'System',
        ipAddress: node.ip_address || 'Unknown',
        connectedNodes: node.connected_nodes || '0 nodes',
        trainingProgress: node.training_progress || 0,
        resources: {
          cpu: node.resources?.cpu || 0,
          memory: node.resources?.memory || '0.0',
          gpu: node.resources?.gpu || 0
        },
        lastHeartbeat: node.last_heartbeat || 'Unknown',
        priority: node.priority || 1
      }))
      
      allFederatedNodes.value = updatedNodes
    }
  } catch (err) {
    console.error('Failed to refresh nodes data:', err)
  }
}

// Computed property for displayed nodes - 只显示训练中的节点
const displayedNodes = computed(() => {
  // Get control nodes (always show)
  const controlNodes = allFederatedNodes.value.filter(n => ['model', 'control'].includes(n.type))
  
  // 只显示正在训练的节点，加上正在消散的节点
  const activeTrainingNodes = allFederatedNodes.value.filter(n => 
    n.type === 'training' && 
    (n.status === 'training' || nodeAnimationStates.value.get(n.id)?.fading)
  )
  
  // 按优先级和CPU使用率排序
  activeTrainingNodes.sort((a, b) => {
    if (b.priority !== a.priority) return b.priority - a.priority
    return b.resources.cpu - a.resources.cpu
  })
  
  // 限制最多15个训练节点
  const limitedTrainingNodes = activeTrainingNodes.slice(0, 15)
  
  return [...controlNodes, ...limitedTrainingNodes]
})

// Update federatedNodes to use displayedNodes
const federatedNodes = displayedNodes

// 传输状态管理
const transmissionStates = ref(new Map())

// Dynamic connections based on currently displayed nodes
const federatedConnections = computed(() => {
  const connections = []
  const displayedTrainingNodes = federatedNodes.value.filter(n => n.type === 'training')
  const controlNodeIds = ['model-1', 'model-2', 'backup-control']
  
  // Create connections from each control node to visible training nodes
  displayedTrainingNodes.forEach((trainingNode, index) => {
    const controlNodeId = controlNodeIds[index % controlNodeIds.length]
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

const startTraining = () => {
  if (trainingState.value.status !== 'training') {
    trainingState.value.status = 'training'
    trainingState.value.startTime = Date.now()
    trainingState.value.currentRound = 1
    
    // Start simulating training progress
    simulateTraining()
    console.log('Training started')
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

// Event handlers
const handleNodeClick = (node) => {
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

// All hover functionality removed

const handleConnectionClick = (connection) => {
  console.log('Connection clicked:', connection)
}

const viewNodeDetails = (node) => {
  selectedNode.value = node
  console.log('Viewing node details:', node)
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
  
  // Setup auto-refresh for real-time updates
  setupAutoRefresh()
  
  // Connect to EdgeAI store WebSocket for real-time updates
  edgeaiStore.connectWebSocket()
})

onUnmounted(() => {
  // Clean up resources
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  
  // Clear API cache
  clearCache()
  
  // Clean up any running training simulations
  if (trainingState.value.status === 'training') {
    trainingState.value.status = 'idle'
  }
})
</script>