<template>
  <div class="p2pai-project-visualization min-h-screen bg-gray-50 dark:bg-gray-900">
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
              <div :class="projectIconClass" class="w-8 h-8 rounded-lg flex items-center justify-center">
                <component :is="projectIcon" class="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                  {{ projectDisplayName }}
                </h1>
                <div class="text-sm text-gray-600 dark:text-gray-400">
                  {{ projectSubtitle }}
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
          <!-- Training Mode -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Training Mode</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ trainingConfig.mode }}</div>
          </div>
          
          <!-- AI Model -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">AI Model</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ trainingConfig.aiModel }}</div>
          </div>
          
          <!-- Privacy Level -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Privacy Level</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ trainingConfig.privacy }}</div>
          </div>
          
          <!-- Visible Nodes -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Visible Nodes</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ visibleNodesCount }}</div>
          </div>
          
          <!-- Status -->
          <div class="text-center">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-1">Status</div>
            <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ projectStatus }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 relative">
      <!-- Node Details Panel (Left Side) - Only visible when node selected -->
      <div 
        v-if="selectedNode && showNodeDetails"
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
              <LockClosedIcon v-else class="w-5 h-5 text-white" />
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

          <!-- Node Performance Metrics (only if visible) -->
          <div v-if="canShowNodeMetrics(selectedNode)" class="space-y-4">
            <h5 class="text-sm font-medium text-gray-900 dark:text-white">Performance Metrics</h5>
            
            <!-- CPU Usage -->
            <div>
              <div class="flex justify-between mb-2">
                <span class="text-xs font-medium text-gray-600 dark:text-gray-300">CPU Usage</span>
                <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.resources?.cpu || '---' }}%</span>
              </div>
              <div v-if="selectedNode.resources?.cpu" class="w-full h-1.5 bg-gray-200 dark:bg-gray-600 rounded-full">
                <div 
                  class="h-1.5 bg-blue-500 rounded-full transition-all duration-300"
                  :style="{ width: `${selectedNode.resources.cpu}%` }"
                ></div>
              </div>
            </div>

            <!-- Memory Usage -->
            <div>
              <div class="flex justify-between mb-2">
                <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Memory Usage</span>
                <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.resources?.memory || '---' }}%</span>
              </div>
              <div v-if="selectedNode.resources?.memory" class="w-full h-1.5 bg-gray-200 dark:bg-gray-600 rounded-full">
                <div 
                  class="h-1.5 bg-green-500 rounded-full transition-all duration-300"
                  :style="{ width: `${selectedNode.resources.memory}%` }"
                ></div>
              </div>
            </div>

            <!-- GPU Usage (if available) -->
            <div v-if="selectedNode.resources?.gpu">
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

          <!-- Privacy Notice -->
          <div v-else class="text-center py-4">
            <LockClosedIcon class="w-8 h-8 text-gray-400 mx-auto mb-2" />
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Node details protected by privacy settings
            </p>
          </div>

          <!-- Action Buttons -->
          <div class="space-y-2 pt-4 border-t border-gray-200 dark:border-gray-700">
            <Button 
              v-if="canControlNode(selectedNode)" 
              @click="handleNodeAction(selectedNode)"
              variant="primary"
              size="sm"
              class="w-full flex items-center justify-center space-x-2"
            >
              <PlayIcon v-if="selectedNode.status === 'idle'" class="w-4 h-4" />
              <StopIcon v-else class="w-4 h-4" />
              <span>{{ selectedNode.status === 'idle' ? 'Start Training' : 'Stop Training' }}</span>
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
      
      <!-- Main Content Container -->
      <div class="flex h-full">
        <!-- Visualization Container -->
        <div class="flex-1">
          <!-- Local Training Chart View -->
          <div v-if="projectType === 'local'" class="bg-white dark:bg-gray-900 m-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 h-[900px]">
            <div class="h-full p-6">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
                Local Training Metrics
              </h3>
              
              <!-- 4个独立的图表 -->
              <div class="grid grid-cols-2 gap-4 h-5/6">
                <!-- Training Accuracy Chart -->
                <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                  <h4 class="text-md font-medium text-gray-900 dark:text-white mb-3">Training Accuracy</h4>
                  <div class="h-40">
                    <LocalTrainingChart 
                      :training-data="{ rounds: localTrainingData.rounds, accuracy: localTrainingData.accuracy }"
                      :is-training="isTraining"
                      chart-type="accuracy"
                      class="h-full"
                    />
                  </div>
                </div>
                
                <!-- Loss Chart -->
                <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                  <h4 class="text-md font-medium text-gray-900 dark:text-white mb-3">Training Loss</h4>
                  <div class="h-40">
                    <LocalTrainingChart 
                      :training-data="{ rounds: localTrainingData.rounds, loss: localTrainingData.loss }"
                      :is-training="isTraining"
                      chart-type="loss"
                      class="h-full"
                    />
                  </div>
                </div>
                
                <!-- CPU Usage Chart -->
                <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                  <h4 class="text-md font-medium text-gray-900 dark:text-white mb-3">CPU Usage</h4>
                  <div class="h-40">
                    <LocalTrainingChart 
                      :training-data="{ rounds: localTrainingData.rounds, cpu: localTrainingData.cpu }"
                      :is-training="isTraining"
                      chart-type="cpu"
                      class="h-full"
                    />
                  </div>
                </div>
                
                <!-- Memory Usage Chart -->
                <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
                  <h4 class="text-md font-medium text-gray-900 dark:text-white mb-3">Memory Usage</h4>
                  <div class="h-40">
                    <LocalTrainingChart 
                      :training-data="{ rounds: localTrainingData.rounds, memory: localTrainingData.memory }"
                      :is-training="isTraining"
                      chart-type="memory"
                      class="h-full"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Network Visualization (for federated and MPC) - 完全按照EdgeAI设计 -->
          <div v-else class="bg-white dark:bg-gray-900 m-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 h-[900px]">
            <div class="h-full relative">
              <NetworkVisualization
                ref="networkViz"
                :nodes="visibleNodes"
                :connections="visibleConnections"
                :training-active="isTraining"
                :project-type="projectType"
                @node-click="handleNodeClick"
                @node-hover="handleNodeHover"
              />
            </div>
          </div>
        </div>
        
        <!-- Control Panel (Right Side) -->
        <div class="w-64 flex-shrink-0 bg-white dark:bg-gray-900 m-6 ml-0 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 h-[900px] overflow-y-auto">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">Control Panel</h3>
        
        <!-- Training Progress -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Training Progress</h4>
          
          <!-- Overall Progress -->
          <div class="mb-4">
            <div class="flex items-center justify-between text-sm mb-2">
              <span class="text-gray-600 dark:text-gray-400">Overall Progress</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ overallProgress }}%</span>
            </div>
            <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full">
              <div 
                class="h-3 bg-gradient-to-r from-blue-500 to-green-500 rounded-full transition-all duration-500"
                :style="{ width: `${overallProgress}%` }"
              ></div>
            </div>
          </div>
          
          <!-- Training Rounds Progress -->
          <div v-if="projectType !== 'local'" class="mb-4">
            <div class="flex items-center justify-between text-sm mb-2">
              <span class="text-gray-600 dark:text-gray-400">Training Rounds</span>
              <span class="font-medium text-gray-900 dark:text-white">{{ trainingState.currentRound }}/{{ trainingState.totalRounds }}</span>
            </div>
            <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full">
              <div 
                class="h-3 bg-blue-500 rounded-full transition-all duration-500"
                :style="{ width: `${(trainingState.currentRound / trainingState.totalRounds) * 100}%` }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Network Statistics -->
        <div class="mb-6">
          <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Network Statistics</h4>
          <div class="space-y-4">
            <!-- Total Nodes -->
            <div class="flex items-center space-x-3">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                  <CpuChipIcon class="w-5 h-5 text-green-600 dark:text-green-400" />
                </div>
              </div>
              <div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ totalVisibleNodes }}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">Visible Nodes</div>
              </div>
            </div>

            <!-- Model Accuracy -->
            <div class="flex items-center space-x-3">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                  <BeakerIcon class="w-5 h-5 text-blue-600 dark:text-blue-400" />
                </div>
              </div>
              <div>
                <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ modelAccuracy }}%</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">Model Accuracy</div>
              </div>
            </div>

            <!-- Privacy Level -->
            <div class="flex items-center space-x-3">
              <div class="flex-shrink-0">
                <div :class="privacyLevelIconClass" class="w-8 h-8 rounded-lg flex items-center justify-center">
                  <component :is="privacyIcon" class="w-5 h-5" :class="privacyIconColor" />
                </div>
              </div>
              <div>
                <div class="text-lg font-bold text-gray-900 dark:text-white">{{ trainingConfig.privacy }}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">Privacy Level</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Training Controls -->
        <div class="mb-4">
          <h3 class="text-md font-semibold text-gray-900 dark:text-white mb-3">Training Controls</h3>
          <div class="grid grid-cols-2 gap-2">
            <Button 
              v-if="!isTraining"
              @click="startTraining"
              variant="primary"
              size="sm"
              class="flex items-center justify-center space-x-2"
            >
              <PlayIcon class="w-4 h-4" />
              <span>Start</span>
            </Button>
            <Button 
              v-else
              @click="stopTraining"
              variant="danger"
              size="sm"
              class="flex items-center justify-center space-x-2"
            >
              <StopIcon class="w-4 h-4" />
              <span>Stop</span>
            </Button>
            
            <Button 
              @click="resetView"
              variant="outline"
              size="sm"
              class="flex items-center justify-center space-x-2"
            >
              <ArrowPathIcon class="w-4 h-4" />
              <span>Reset</span>
            </Button>
          </div>
        </div>

        <!-- Privacy Information -->
        <div class="mb-3">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-md font-semibold text-gray-900 dark:text-white">Privacy Info</h3>
          </div>
          <div class="text-xs text-gray-600 dark:text-gray-400 space-y-1">
            <div v-for="info in privacyInfo" :key="info" class="flex items-center space-x-2">
              <div class="w-1 h-1 bg-gray-400 rounded-full flex-shrink-0"></div>
              <span>{{ info }}</span>
            </div>
          </div>
        </div>
        </div>
      </div>
    </div>

    <!-- Bottom Dashboard - 只在分布式训练时显示 -->
    <div v-if="projectType !== 'local'" class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
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
              <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ totalNodes }}</div>
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
              <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ overallProgress }}%</div>
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

          <!-- Privacy Level -->
          <div class="flex items-center space-x-3">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
                <LockClosedIcon class="w-5 h-5 text-purple-600 dark:text-purple-400" />
              </div>
            </div>
            <div>
              <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ privacyLevel }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">Privacy Level</div>
            </div>
          </div>
        </div>

        <!-- Training Controls -->
        <div class="mb-4">
          <h3 class="text-md font-semibold text-gray-900 dark:text-white mb-3">Training Controls</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
            <Button 
              @click="startTraining"
              variant="primary"
              size="sm"
              class="flex items-center justify-center space-x-2"
              :disabled="trainingState.status === 'training'"
            >
              <PlayIcon class="w-4 h-4" />
              <span>{{ trainingState.status === 'training' ? 'Training...' : 'Start Training' }}</span>
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
              @click="togglePrivacyMode"
              variant="outline"
              size="sm"
              class="flex items-center justify-center space-x-2"
            >
              <EyeSlashIcon v-if="projectType === 'mpc'" class="w-4 h-4" />
              <EyeIcon v-else class="w-4 h-4" />
              <span>{{ projectType === 'mpc' ? 'Max Privacy' : 'Standard' }}</span>
            </Button>
            
            <Button 
              @click="exportData"
              variant="outline"
              size="sm"
              class="flex items-center justify-center space-x-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <span>Export</span>
            </Button>
          </div>
        </div>

        <!-- Node Details List -->
        <div class="mb-3">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-md font-semibold text-gray-900 dark:text-white">Node Details</h3>
            <div class="text-sm text-gray-500 dark:text-gray-400">
              <span v-if="projectType === 'mpc'">
                Visible: <span class="font-medium text-purple-600">{{ visibleNodes.length }}</span> • 
                Privacy: <span class="font-medium text-purple-600">Maximum</span>
              </span>
              <span v-else>
                Control: <span class="font-medium text-green-600">{{ controlNodesCount }}</span> • 
                Training: <span class="font-medium text-blue-600">{{ trainingNodesCount }}</span> • 
                Total: <span class="font-medium text-gray-900 dark:text-white">{{ totalNodes }}</span>
              </span>
            </div>
          </div>

          <!-- 根据项目类型显示不同的表格 -->
          <div v-if="projectType === 'mpc'" class="overflow-x-auto bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
            <table class="w-full text-sm">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Node Type</th>
                  <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Status</th>
                  <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Privacy Level</th>
                  <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Data Protection</th>
                </tr>
              </thead>
              <tbody>
                <tr class="border-b border-gray-100 dark:border-gray-800">
                  <td class="p-3">
                    <div class="flex items-center space-x-3">
                      <div class="w-3 h-3 bg-purple-500 rounded-full"></div>
                      <span class="font-medium text-gray-900 dark:text-white">Local Node</span>
                    </div>
                  </td>
                  <td class="p-3">
                    <span class="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                      Active
                    </span>
                  </td>
                  <td class="p-3 text-purple-600 dark:text-purple-400 font-medium">Maximum</td>
                  <td class="p-3 text-gray-600 dark:text-gray-400">All data encrypted</td>
                </tr>
                <tr class="border-b border-gray-100 dark:border-gray-800">
                  <td class="p-3">
                    <div class="flex items-center space-x-3">
                      <div class="w-3 h-3 bg-gray-400 rounded-full"></div>
                      <span class="font-medium text-gray-900 dark:text-white">Remote Parties</span>
                    </div>
                  </td>
                  <td class="p-3">
                    <span class="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300">
                      Hidden
                    </span>
                  </td>
                  <td class="p-3 text-purple-600 dark:text-purple-400 font-medium">Maximum</td>
                  <td class="p-3 text-gray-600 dark:text-gray-400">Identity protected</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 联邦学习节点表格 -->
          <div v-else class="overflow-x-auto bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
            <table class="w-full text-sm">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Node Name</th>
                  <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Type</th>
                  <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Status</th>
                  <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Progress</th>
                  <th class="text-left p-3 font-medium text-gray-900 dark:text-white">Last Update</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="node in visibleNodes.slice(0, 5)" 
                  :key="node.id"
                  class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700/50"
                  @click="handleNodeClick(node)"
                >
                  <td class="p-3">
                    <div class="flex items-center space-x-3">
                      <div :class="getNodeColorClass(node.type)" class="w-3 h-3 rounded-full"></div>
                      <span class="font-medium text-gray-900 dark:text-white">{{ node.name || node.id }}</span>
                    </div>
                  </td>
                  <td class="p-3 text-gray-600 dark:text-gray-400 capitalize">{{ node.type }}</td>
                  <td class="p-3">
                    <span 
                      :class="getNodeStatusBadgeClass(node.status)"
                      class="px-2 py-1 text-xs font-medium rounded-full"
                    >
                      {{ node.status }}
                    </span>
                  </td>
                  <td class="p-3">
                    <div v-if="node.type === 'training'" class="flex items-center space-x-2">
                      <div class="w-16 h-2 bg-gray-200 dark:bg-gray-600 rounded-full">
                        <div 
                          class="h-2 bg-blue-600 rounded-full transition-all duration-500"
                          :style="{ width: `${node.trainingProgress || 0}%` }"
                        ></div>
                      </div>
                      <span class="text-sm font-medium text-gray-900 dark:text-white">{{ node.trainingProgress || 0 }}%</span>
                    </div>
                    <span v-else class="text-gray-400">-</span>
                  </td>
                  <td class="p-3 text-gray-600 dark:text-gray-400">{{ node.lastHeartbeat || 'Just now' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import {
  ArrowLeftIcon,
  CpuChipIcon,
  ServerIcon,
  LockClosedIcon,
  UsersIcon,
  ShieldCheckIcon,
  PlayIcon,
  StopIcon,
  ArrowPathIcon,
  BeakerIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/vue/24/outline'

import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import Button from '@/components/ui/Button.vue'
import NetworkVisualization from '@/components/p2pai/NetworkVisualization.vue'
import LocalTrainingChart from '@/components/p2pai/LocalTrainingChart.vue'

const router = useRouter()
const route = useRoute()
const themeStore = useThemeStore()

// Project state
const projectId = ref(route.params.projectId || 'default')
const selectedNode = ref(null)
const showNodeDetails = ref(false)
const isClosing = ref(false)
const isTraining = ref(false)

// Training state with initial progress
const trainingState = ref({
  currentRound: 15,
  totalRounds: 100,
  status: 'idle'
})

const nodeAnimationStates = ref({})

// Local training data with initial mock data
const localTrainingData = ref({
  rounds: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  accuracy: [65.2, 68.5, 71.3, 74.1, 76.8, 79.2, 81.5, 83.7, 85.1, 86.4],
  loss: [2.1, 1.9, 1.7, 1.5, 1.3, 1.1, 0.9, 0.8, 0.7, 0.6],
  cpu: [72, 75, 78, 74, 76, 79, 77, 73, 75, 78],
  gpu: [85, 82, 87, 84, 86, 88, 85, 83, 86, 89],
  memory: [68, 71, 69, 72, 70, 74, 73, 71, 75, 72]
})

// Computed properties
const projectType = computed(() => {
  if (projectId.value.includes('local')) return 'local'
  if (projectId.value.includes('federated')) return 'federated'
  if (projectId.value.includes('mpc')) return 'mpc'
  return 'local'
})

const projectDisplayName = computed(() => {
  const names = {
    local: 'Local Training Project',
    federated: 'Federated Learning Project',
    mpc: 'MPC Privacy Training'
  }
  return names[projectType.value] || 'P2P AI Project'
})

const projectSubtitle = computed(() => {
  const subtitles = {
    local: 'Complete data visibility and control',
    federated: 'Collaborative learning with privacy protection',
    mpc: 'Maximum privacy with cryptographic protection'
  }
  return subtitles[projectType.value] || 'Real-time Training Dashboard'
})

const projectIcon = computed(() => {
  const icons = {
    local: ShieldCheckIcon,
    federated: UsersIcon,
    mpc: LockClosedIcon
  }
  return icons[projectType.value] || CpuChipIcon
})

const projectIconClass = computed(() => {
  const classes = {
    local: 'bg-gray-600',
    federated: 'bg-blue-600',
    mpc: 'bg-green-600'
  }
  return classes[projectType.value] || 'bg-blue-600'
})

const trainingConfig = computed(() => {
  const configs = {
    local: {
      mode: 'Local Training',
      aiModel: 'ResNet-50',
      privacy: 'Full Visibility',
    },
    federated: {
      mode: 'Federated Learning',
      aiModel: 'Neural Network',
      privacy: 'Partial Privacy',
    },
    mpc: {
      mode: 'MPC Training',
      aiModel: 'Encrypted Model',
      privacy: 'Cryptographic',
    }
  }
  return configs[projectType.value] || configs.local
})

const visibleNodesCount = computed(() => {
  const counts = {
    local: '1 (Local Only)',
    federated: `${visibleNodes.value.length} (${visibleNodes.value.filter(n => n.type === 'edge').length} Edge + ${visibleNodes.value.filter(n => n.type === 'control').length} Server)`,
    mpc: '1 (Others Hidden)'
  }
  return counts[projectType.value] || '1'
})

const projectStatus = computed(() => {
  return isTraining.value ? 'Training' : 'Ready'
})

const overallProgress = computed(() => {
  if (projectType.value === 'local') {
    return localTrainingData.value.accuracy.length > 0 
      ? Math.round(localTrainingData.value.accuracy[localTrainingData.value.accuracy.length - 1]) 
      : 0
  }
  return Math.round((trainingState.value.currentRound / trainingState.value.totalRounds) * 100)
})

const totalVisibleNodes = computed(() => {
  return visibleNodes.value.length
})

const modelAccuracy = computed(() => {
  if (projectType.value === 'local') {
    return localTrainingData.value.accuracy.length > 0 
      ? localTrainingData.value.accuracy[localTrainingData.value.accuracy.length - 1].toFixed(1)
      : '0.0'
  }
  return '87.5' // Mock federated/MPC accuracy
})

const privacyIcon = computed(() => {
  const icons = {
    local: EyeIcon,
    federated: ShieldCheckIcon,
    mpc: LockClosedIcon
  }
  return icons[projectType.value] || EyeIcon
})

const privacyIconColor = computed(() => {
  const colors = {
    local: 'text-green-600 dark:text-green-400',
    federated: 'text-yellow-600 dark:text-yellow-400',
    mpc: 'text-purple-600 dark:text-purple-400'
  }
  return colors[projectType.value] || 'text-green-600'
})

const privacyLevelIconClass = computed(() => {
  const classes = {
    local: 'bg-green-100 dark:bg-green-900',
    federated: 'bg-yellow-100 dark:bg-yellow-900',
    mpc: 'bg-purple-100 dark:bg-purple-900'
  }
  return classes[projectType.value] || 'bg-green-100'
})

const privacyInfo = computed(() => {
  const info = {
    local: [
      'All training data visible',
      'Complete resource monitoring',
      'Full control over training'
    ],
    federated: [
      'Your data stays local',
      'Only global model shared',
      'Other nodes hidden'
    ],
    mpc: [
      'All data encrypted',
      'Minimal information sharing',
      'Maximum privacy protection'
    ]
  }
  return info[projectType.value] || info.local
})

const visibleNodes = computed(() => {
  if (projectType.value === 'local') {
    return [
      { 
        id: 'local-001', 
        name: 'Your Device', 
        type: 'edge',
        status: isTraining.value ? 'training' : 'idle',
        resources: { cpu: 75, memory: 60, gpu: 80 },
        color: '#3b82f6',
        strokeColor: '#1d4ed8',
        isOwn: true,
        progress: isTraining.value ? overallProgress.value : 0
      }
    ]
  } else if (projectType.value === 'federated') {
    return [
      { 
        id: 'local-001', 
        name: 'Your Device', 
        type: 'edge',
        status: isTraining.value ? 'training' : 'idle',
        resources: { cpu: 75, memory: 60, gpu: 80 },
        isOwn: true,
        progress: isTraining.value ? overallProgress.value : 0
      },
      { 
        id: 'server-001', 
        name: 'Central Server', 
        type: 'control',
        subType: 'master',
        status: 'active',
        resources: { cpu: 45, memory: 70 },
        isOwn: false
      },
      { 
        id: 'edge-002', 
        name: 'Mobile Device A', 
        type: 'edge',
        status: 'training',
        resources: { cpu: 65, memory: 45 },
        isOwn: false,
        progress: 67
      },
      { 
        id: 'edge-003', 
        name: 'Laptop B', 
        type: 'edge',
        status: 'idle',
        resources: { cpu: 85, memory: 70 },
        isOwn: false,
        progress: 0
      },
      { 
        id: 'edge-004', 
        name: 'IoT Device C', 
        type: 'edge',
        status: 'training',
        resources: { cpu: 45, memory: 30 },
        isOwn: false,
        progress: 23
      },
      { 
        id: 'edge-005', 
        name: 'Workstation D', 
        type: 'edge',
        status: 'offline',
        resources: { cpu: 0, memory: 0 },
        isOwn: false,
        progress: 0
      }
    ]
  } else { // MPC
    return [
      { 
        id: 'local-001', 
        name: 'Your Device', 
        type: 'edge',
        status: 'computing',
        resources: { cpu: 85 },
        isOwn: true,
        progress: isTraining.value ? overallProgress.value : 0
      }
    ]
    // 注意：MPC模式下其他参与方是隐藏的，由隐藏占位符显示
  }
})

const visibleConnections = computed(() => {
  if (projectType.value === 'federated') {
    return [
      { 
        from: 'local-001', 
        to: 'server-001', 
        type: 'federated',
        active: isTraining.value
      },
      { 
        from: 'edge-002', 
        to: 'server-001', 
        type: 'federated',
        active: true
      },
      { 
        from: 'edge-003', 
        to: 'server-001', 
        type: 'federated',
        active: false
      },
      { 
        from: 'edge-004', 
        to: 'server-001', 
        type: 'federated',
        active: true
      },
      { 
        from: 'edge-005', 
        to: 'server-001', 
        type: 'federated',
        active: false
      }
    ]
  }
  return []
})

// 新增的底部面板所需的计算属性
const totalNodes = computed(() => {
  if (projectType.value === 'mpc') {
    return 5 // MPC：1个可见节点 + 4个隐藏参与方
  } else if (projectType.value === 'federated') {
    return visibleNodes.value.length // 联邦学习显示所有可见节点
  }
  return 1 // 本地训练
})

const controlNodesCount = computed(() => {
  return visibleNodes.value.filter(n => n.type === 'control').length
})

const trainingNodesCount = computed(() => {
  return visibleNodes.value.filter(n => n.type === 'training').length
})

const networkLatency = computed(() => {
  const latencies = {
    local: 0,
    federated: 45,
    mpc: 12 // Lower latency for MPC due to minimal data sharing
  }
  return latencies[projectType.value] || 0
})

const privacyLevel = computed(() => {
  const levels = {
    local: 'Standard',
    federated: 'Medium',
    mpc: 'Maximum'
  }
  return levels[projectType.value] || 'Standard'
})

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

const getNodeColorClass = (type) => {
  const classes = {
    training: 'bg-blue-500',
    control: 'bg-green-500',
    mpc: 'bg-purple-500'
  }
  return classes[type] || 'bg-gray-500'
}

const getNodeStatusBadgeClass = (status) => {
  const classes = {
    idle: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300',
    training: 'bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-300',
    active: 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-300',
    computing: 'bg-purple-100 text-purple-800 dark:bg-purple-800 dark:text-purple-300'
  }
  return classes[status] || classes.idle
}

const canShowNodeMetrics = (node) => {
  if (projectType.value === 'local') return true
  if (projectType.value === 'federated' && node.id === 'local-001') return true
  if (projectType.value === 'mpc') return false // Very limited for MPC
  return false
}

const canControlNode = (node) => {
  return node.id === 'local-001' // Can only control your own node
}

const handleNodeClick = (node) => {
  selectedNode.value = node
  showNodeDetails.value = true
  isClosing.value = false
}

const handleConnectionClick = (connection) => {
  console.log('Connection clicked:', connection)
}

const handleNodeHover = (node) => {
  console.log('Node hovered:', node)
}

const closeNodeDetails = () => {
  isClosing.value = true
  setTimeout(() => {
    showNodeDetails.value = false
    selectedNode.value = null
    isClosing.value = false
  }, 300)
}

const handleNodeAction = (node) => {
  if (node.status === 'idle') {
    startTraining()
  } else {
    stopTraining()
  }
}

const startTraining = () => {
  isTraining.value = true
  trainingState.value.status = 'training'
  
  if (projectType.value === 'local') {
    // Start local training simulation
    startLocalTrainingSimulation()
  } else {
    // Start federated/MPC training simulation
    startDistributedTrainingSimulation()
  }
}

const stopTraining = () => {
  isTraining.value = false
  trainingState.value.status = 'idle'
}

const resetView = () => {
  // Reset view state
  selectedNode.value = null
  showNodeDetails.value = false
  
  // Reset training data for local training
  if (projectType.value === 'local') {
    localTrainingData.value = {
      rounds: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      accuracy: [65.2, 68.5, 71.3, 74.1, 76.8, 79.2, 81.5, 83.7, 85.1, 86.4],
      loss: [2.1, 1.9, 1.7, 1.5, 1.3, 1.1, 0.9, 0.8, 0.7, 0.6],
      cpu: [72, 75, 78, 74, 76, 79, 77, 73, 75, 78],
      gpu: [85, 82, 87, 84, 86, 88, 85, 83, 86, 89],
      memory: [68, 71, 69, 72, 70, 74, 73, 71, 75, 72]
    }
  }
}

// 新增方法 - 底部面板所需
const togglePrivacyMode = () => {
  console.log('Toggle privacy mode for', projectType.value)
}

const exportData = () => {
  console.log('Export data for', projectType.value)
}

const startLocalTrainingSimulation = () => {
  const interval = setInterval(() => {
    if (!isTraining.value) {
      clearInterval(interval)
      return
    }
    
    const round = localTrainingData.value.rounds.length + 1
    localTrainingData.value.rounds.push(round)
    
    // Simulate improving accuracy
    const accuracy = Math.min(95, 60 + round * 0.3 + Math.random() * 5)
    localTrainingData.value.accuracy.push(accuracy)
    
    // Simulate decreasing loss
    const loss = Math.max(0.1, 2.5 * Math.exp(-round * 0.05) + Math.random() * 0.1)
    localTrainingData.value.loss.push(loss)
    
    // Simulate resource usage
    const cpu = 70 + Math.random() * 20
    const gpu = 80 + Math.random() * 15
    const memory = 60 + Math.random() * 25
    
    localTrainingData.value.cpu.push(cpu)
    localTrainingData.value.gpu.push(gpu)
    localTrainingData.value.memory.push(memory)
    
    // Keep only last 50 data points
    if (localTrainingData.value.rounds.length > 50) {
      Object.keys(localTrainingData.value).forEach(key => {
        localTrainingData.value[key].shift()
      })
    }
  }, 1000)
}

const startDistributedTrainingSimulation = () => {
  const interval = setInterval(() => {
    if (!isTraining.value) {
      clearInterval(interval)
      return
    }
    
    trainingState.value.currentRound = Math.min(
      trainingState.value.totalRounds,
      trainingState.value.currentRound + 1
    )
    
    if (trainingState.value.currentRound >= trainingState.value.totalRounds) {
      stopTraining()
    }
  }, 2000)
}

// Lifecycle
onMounted(() => {
  // Initialize based on project type
  console.log('Loading project visualization for:', projectId.value, 'Type:', projectType.value)
})
</script>

<style scoped>
.p2pai-project-visualization {
  min-height: 100vh;
}

/* Animation classes */
.animate-slide-in {
  animation: slideIn 0.7s ease-out forwards;
}

.animate-slide-out {
  animation: slideOut 0.3s ease-in forwards;
}

@keyframes slideIn {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(-100%);
    opacity: 0;
  }
}
</style>