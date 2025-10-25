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
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
          <!-- Training Mode -->
          <div class="text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Training Mode</div>
            <div class="text-sm font-semibold text-gray-900 dark:text-white truncate">{{ trainingConfig.mode }}</div>
          </div>
          
          <!-- AI Model -->
          <div class="text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">AI Model</div>
            <div class="text-sm font-semibold text-gray-900 dark:text-white truncate">{{ trainingConfig.aiModel }}</div>
          </div>
          
          <!-- Training Algorithm -->
          <div class="text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Training Alg</div>
            <div class="text-sm font-semibold text-blue-600 dark:text-blue-400 truncate">{{ trainingConfig.trainingAlg || 'N/A' }}</div>
          </div>
          
          <!-- Federated Algorithm -->
          <div class="text-center" v-if="trainingConfig.fedAlg">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Fed Alg</div>
            <div class="text-sm font-semibold text-purple-600 dark:text-purple-400 truncate">{{ trainingConfig.fedAlg }}</div>
          </div>
          
          <!-- Dataset -->
          <div class="text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Dataset</div>
            <div class="text-sm font-semibold text-gray-900 dark:text-white truncate">{{ trainingConfig.dataset || 'N/A' }}</div>
          </div>
          
          <!-- Batch Size -->
          <div class="text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Batch Size</div>
            <div class="text-sm font-semibold text-gray-900 dark:text-white">{{ trainingConfig.batchSize || 'N/A' }}</div>
          </div>
          
          <!-- Learning Rate -->
          <div class="text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Learning Rate</div>
            <div class="text-sm font-semibold text-gray-900 dark:text-white">{{ trainingConfig.lr || 'N/A' }}</div>
          </div>
          
          <!-- Status -->
          <div class="text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Status</div>
            <div class="text-sm font-semibold text-green-600 dark:text-green-400">{{ projectStatus }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex-1 flex justify-center items-center">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <span class="text-gray-600 dark:text-gray-400">Loading project visualization...</span>
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
              Failed to load project visualization
            </h3>
            <div class="mt-2 text-sm text-red-700 dark:text-red-300">
              {{ error }}
            </div>
            <div class="mt-3">
              <Button @click="loadProjectVisualizationData" variant="ghost" size="sm" class="text-red-800 dark:text-red-200 hover:bg-red-100 dark:hover:bg-red-800/30">
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
        v-if="selectedNode && showNodeDetails"
        class="absolute left-0 top-0 z-10 w-64 bg-white dark:bg-gray-900 m-6 mr-0 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 transform overflow-y-auto custom-scrollbar transition-all duration-700 h-[600px]"
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
                <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.resources?.cpu ? selectedNode.resources.cpu.toFixed(2) : '---' }}%</span>
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
                <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.resources?.memory ? selectedNode.resources.memory.toFixed(2) : '---' }}%</span>
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
                <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.resources.gpu.toFixed(2) }}%</span>
              </div>
              <div class="w-full h-1.5 bg-gray-200 dark:bg-gray-600 rounded-full">
                <div 
                  class="h-1.5 bg-purple-500 rounded-full transition-all duration-300"
                  :style="{ width: `${selectedNode.resources.gpu}%` }"
                ></div>
              </div>
            </div>

            <!-- Training Information (for control nodes) -->
            <div v-if="selectedNode.type === 'control'" class="space-y-4">
              <h5 class="text-sm font-medium text-gray-900 dark:text-white">Training Information</h5>
              
              <!-- Training Progress -->
              <div>
                <div class="flex justify-between mb-2">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Training Progress</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.trainingProgress ? selectedNode.trainingProgress.toFixed(2) : '---' }}%</span>
                </div>
                <div v-if="selectedNode.trainingProgress" class="w-full h-1.5 bg-gray-200 dark:bg-gray-600 rounded-full">
                  <div 
                    class="h-1.5 bg-gradient-to-r from-blue-500 to-green-500 rounded-full transition-all duration-300"
                    :style="{ width: `${selectedNode.trainingProgress}%` }"
                  ></div>
                </div>
              </div>

              <!-- Training Rounds -->
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Current Round</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.currentRound || '---' }}/{{ selectedNode.totalRounds || '---' }}</span>
                </div>
              </div>

              <!-- Model Accuracy -->
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Model Accuracy</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.modelAccuracy ? selectedNode.modelAccuracy.toFixed(2) : '---' }}%</span>
                </div>
              </div>

              <!-- Connected Nodes -->
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Connected Nodes</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.connectedNodes || '---' }}</span>
                </div>
              </div>

              <!-- Network Latency -->
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Network Latency</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.networkLatency || '---' }}ms</span>
                </div>
              </div>

              <!-- Data Processed -->
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Data Processed</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.dataProcessed || '---' }}</span>
                </div>
              </div>

              <!-- Model Size -->
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Model Size</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.modelSize || '---' }}</span>
                </div>
              </div>

              <!-- Last Update -->
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-xs font-medium text-gray-600 dark:text-gray-300">Last Update</span>
                  <span class="text-xs font-bold text-gray-900 dark:text-white">{{ selectedNode.lastUpdate || '---' }}</span>
                </div>
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
              
              <!-- 4 independent charts -->
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

          <!-- Network Visualization (for federated and MPC) - Designed following EdgeAI pattern -->
          <div v-else class="bg-white dark:bg-gray-900 m-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 h-[700px]">
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
        <div class="w-64 flex-shrink-0 bg-white dark:bg-gray-900 m-6 ml-0 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 h-[700px] overflow-y-auto custom-scrollbar">
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

    <!-- Bottom Dashboard - Only shown for distributed training -->
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

          <!-- Display different tables based on project type -->
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

          <!-- Federated learning node table -->
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

      <!-- Complete Configuration Information Panel -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <svg class="w-5 h-5 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Complete Configuration
              </h3>
              <button 
                @click="showConfigPanel = !showConfigPanel"
                class="text-sm text-blue-600 hover:text-blue-700"
              >
                {{ showConfigPanel ? 'Collapse' : 'Expand' }}
              </button>
            </div>
            
            <div v-if="showConfigPanel" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <!-- Training Configuration -->
              <div class="space-y-3">
                <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 pb-2">
                  Training Configuration
                </h4>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Training Algorithm:</span>
                    <span class="font-medium text-blue-600 dark:text-blue-400">{{ trainingConfig.trainingAlg || 'N/A' }}</span>
                  </div>
                  <div v-if="trainingConfig.fedAlg" class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Federated Algorithm:</span>
                    <span class="font-medium text-purple-600 dark:text-purple-400">{{ trainingConfig.fedAlg }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Secure Aggregation:</span>
                    <span class="font-medium">{{ projectType === 'mpc' ? 'Yes' : 'No' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Total Rounds:</span>
                    <span class="font-medium">{{ trainingState.totalRounds }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Batch Size:</span>
                    <span class="font-medium">{{ trainingConfig.batchSize }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Learning Rate:</span>
                    <span class="font-medium">{{ trainingConfig.lr }}</span>
                  </div>
                </div>
              </div>

              <!-- Node Configuration -->
              <div class="space-y-3">
                <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 pb-2">
                  Node Configuration
                </h4>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Project Type:</span>
                    <span class="font-medium">{{ trainingConfig.mode }}</span>
                  </div>
                  <div v-if="projectType === 'local'" class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Compute Nodes:</span>
                    <span class="font-medium">1</span>
                  </div>
                  <div v-if="projectType === 'federated'">
                    <div class="flex justify-between mb-2">
                      <span class="text-gray-500 dark:text-gray-400">Total Clients:</span>
                      <span class="font-medium">5</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-500 dark:text-gray-400">Sample Clients:</span>
                      <span class="font-medium">3</span>
                    </div>
                  </div>
                  <div v-if="projectType === 'mpc'">
                    <div class="flex justify-between mb-2">
                      <span class="text-gray-500 dark:text-gray-400">Parties:</span>
                      <span class="font-medium">3</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-500 dark:text-gray-400">Threshold:</span>
                      <span class="font-medium">2</span>
                    </div>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Visible Nodes:</span>
                    <span class="font-medium">{{ visibleNodes.length }}</span>
                  </div>
                </div>
              </div>

              <!-- Model and Dataset -->
              <div class="space-y-3">
                <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 pb-2">
                  Model and Dataset
                </h4>
                <div class="space-y-2 text-sm">
                  <div>
                    <span class="text-gray-500 dark:text-gray-400 block mb-1">Model:</span>
                    <span class="font-medium block truncate">{{ trainingConfig.aiModel }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500 dark:text-gray-400 block mb-1">Dataset:</span>
                    <span class="font-medium block truncate">{{ trainingConfig.dataset }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Sampling Strategy:</span>
                    <span class="font-medium">{{ projectType === 'mpc' ? 'Secure' : 'Full' }}</span>
                  </div>
                </div>
              </div>

              <!-- Performance Metrics -->
              <div class="space-y-3">
                <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 pb-2">
                  Performance Metrics
                </h4>
                <div class="space-y-2 text-sm">
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Status:</span>
                    <span class="font-medium text-green-600 dark:text-green-400">{{ projectStatus }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Progress:</span>
                    <span class="font-medium">{{ trainingState.currentRound }}/{{ trainingState.totalRounds }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Loss:</span>
                    <span class="font-medium text-red-600">{{ projectType === 'local' ? '0.234' : projectType === 'federated' ? '0.189' : '0.146' }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-500 dark:text-gray-400">Accuracy:</span>
                    <span class="font-medium text-blue-600">{{ projectType === 'local' ? '85.2%' : projectType === 'federated' ? '89.5%' : '91.8%' }}</span>
                  </div>
                  <div>
                    <span class="text-gray-500 dark:text-gray-400 block mb-1">Task ID:</span>
                    <span class="font-medium text-xs block truncate">{{ projectType }}_task_00{{ projectId }}</span>
                  </div>
                </div>
              </div>
            </div>
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
import { useP2PAIStore } from '@/stores/p2pai'
import { useApiOptimization } from '@/composables/useApiOptimization'
import edgeaiService from '@/services/edgeaiService'
import p2paiService from '@/services/p2paiService'
import performanceMonitor from '@/utils/performanceMonitor'
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
const p2paiStore = useP2PAIStore()
const { cachedApiCall, clearCache } = useApiOptimization()

// Loading and error states
const loading = ref(false)
const error = ref(null)
const refreshInterval = ref(null)

// Project state
const projectId = ref(route.params.projectId || 'default')
const selectedNode = ref(null)
const showNodeDetails = ref(false)
const isClosing = ref(false)
const isTraining = ref(false)
const showConfigPanel = ref(true)

// Training state with initial progress
const trainingState = ref({
  currentRound: 15,
  totalRounds: 100,
  status: 'idle'
})

const nodeAnimationStates = ref({})

// Local training data (will be loaded from API)
const localTrainingData = ref({
  rounds: [],
  accuracy: [],
  loss: [],
  cpu: [],
  gpu: [],
  memory: []
})

// Network data for visualization
const networkData = ref({
  nodes: [],
  links: [],
  summary: {
    totalNodes: 0,
    trainingNodes: 0,
    totalModels: 0,
    activeModels: 0
  }
})

// Project display information (use ref instead of computed for dynamic updates)
const projectDisplayName = ref('P2P AI Project')
const projectSubtitle = ref('Real-time Training Dashboard')

// 🔧 P2P AI Hardcoded Project Data - FRONTEND DEMO/FALLBACK DATA
// 📁 File Location: /frontend/src/views/p2pai/ProjectVisualization.vue
//
// ⚠️ WARNING: This is hardcoded demo data for visualization purposes only
//
// Purpose:
// 1. Provides demo data when backend API is unavailable
// 2. Allows frontend testing without backend dependency
// 3. Shows example data structure for project visualization
//
// TODO: In production, all data should come from p2paiService API
// These hardcoded projects (ID 1, 2, 3) should only be used for:
// - Development/testing environments
// - Demo presentations
// - Fallback when API fails
const P2PAI_HARDCODED_PROJECTS = {
  1: {
    id: 1,
    name: '[Frontend Demo] Local Training - Image Classification',
    description: '⚠️ Frontend demo data - Local training project using single machine for image classification model training',
    type: 'local',
    status: 'training',
    progress: 65,
    epochs: 100,
    created_time: new Date('2024-01-15'),
    model_name_or_path: 'resnet50',
    dataset_name: 'CIFAR-10'
  },
  2: {
    id: 2,
    name: '[Frontend Demo] Federated Learning - Medical Diagnosis',
    description: '⚠️ Frontend demo data - Federated learning project with multiple hospitals collaboratively training disease diagnosis model',
    type: 'federated',
    status: 'training',
    progress: 75,
    epochs: 50,
    created_time: new Date('2024-01-20'),
    model_name_or_path: 'efficientnet-b0',
    dataset_name: 'Medical-Images'
  },
  3: {
    id: 3,
    name: '[Frontend Demo] MPC - Financial Data Analysis',
    description: '⚠️ Frontend demo data - Multi-party computation project with multiple financial institutions jointly analyzing data',
    type: 'mpc',
    status: 'completed',
    progress: 100,
    epochs: 30,
    created_time: new Date('2024-01-25'),
    model_name_or_path: 'mlp-classifier',
    dataset_name: 'Financial-Records'
  }
}

// Computed properties
const projectType = computed(() => {
  // First check if it's a P2P AI hardcoded project
  const projectIdNum = parseInt(projectId.value)
  if (P2PAI_HARDCODED_PROJECTS[projectIdNum]) {
    return P2PAI_HARDCODED_PROJECTS[projectIdNum].type
  }
  
  // Otherwise infer from ID string
  if (projectId.value.includes('local')) return 'local'
  if (projectId.value.includes('federated')) return 'federated'
  if (projectId.value.includes('mpc')) return 'mpc'
  return 'local'
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
  // Try to get actual model info from hardcoded projects
  const projectIdNum = parseInt(projectId.value)
  const project = P2PAI_HARDCODED_PROJECTS[projectIdNum]
  
  const configs = {
    local: {
      mode: 'Local Training',
      aiModel: project ? project.model_name_or_path : 'ResNet-50',
      privacy: 'Full Visibility',
      trainingAlg: project ? project.training_alg : 'Adam',
      fedAlg: null,
      dataset: project ? project.dataset_name : 'CIFAR-10',
      batchSize: project ? project.batch_size : 32,
      lr: project ? project.lr : 0.001,
    },
    federated: {
      mode: 'Federated Learning',
      aiModel: project ? project.model_name_or_path : 'Neural Network',
      privacy: 'Partial Privacy',
      trainingAlg: project ? project.training_alg : 'Adam',
      fedAlg: project ? project.fed_alg : 'FedAvg',
      dataset: project ? project.dataset_name : 'Medical-Images',
      batchSize: project ? project.batch_size : 16,
      lr: project ? project.lr : 0.0005,
    },
    mpc: {
      mode: 'MPC Training',
      aiModel: project ? project.model_name_or_path : 'Encrypted Model',
      privacy: 'Cryptographic',
      trainingAlg: project ? project.training_alg : 'SecureAgg',
      fedAlg: project ? project.fed_alg : 'SecureFedAvg',
      dataset: project ? project.dataset_name : 'Financial-Records',
      batchSize: project ? project.batch_size : 64,
      lr: project ? project.lr : 0.0001,
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
        resources: { cpu: 45, memory: 70, gpu: 65 },
        isOwn: false,
        trainingProgress: overallProgress.value,
        currentRound: trainingState.value.currentRound,
        totalRounds: trainingState.value.totalRounds,
        modelAccuracy: 87.5,
        lastUpdate: 'Just now',
        networkLatency: 12,
        connectedNodes: 9,
        dataProcessed: '2.3GB',
        modelSize: '45.2MB'
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
        status: 'idle',
        resources: { cpu: 90, memory: 85 },
        isOwn: false,
        progress: 0
      },
      { 
        id: 'edge-006', 
        name: 'Tablet E', 
        type: 'edge',
        status: 'training',
        resources: { cpu: 55, memory: 40 },
        isOwn: false,
        progress: 45
      },
      { 
        id: 'edge-007', 
        name: 'Smart Phone F', 
        type: 'edge',
        status: 'training',
        resources: { cpu: 40, memory: 25 },
        isOwn: false,
        progress: 78
      },
      { 
        id: 'edge-008', 
        name: 'Server Node G', 
        type: 'edge',
        status: 'training',
        resources: { cpu: 95, memory: 90 },
        isOwn: false,
        progress: 92
      },
      { 
        id: 'edge-009', 
        name: 'Edge Box H', 
        type: 'edge',
        status: 'idle',
        resources: { cpu: 60, memory: 50 },
        isOwn: false,
        progress: 0
      },
      { 
        id: 'edge-010', 
        name: 'Mini PC I', 
        type: 'edge',
        status: 'training',
        resources: { cpu: 70, memory: 65 },
        isOwn: false,
        progress: 34
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
    // Note: In MPC mode, other parties are hidden and shown as hidden placeholders
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

// Computed properties for bottom dashboard
const totalNodes = computed(() => {
  if (projectType.value === 'mpc') {
    return 5 // MPC: 1 visible node + 4 hidden parties
  } else if (projectType.value === 'federated') {
    return visibleNodes.value.length // Federated learning shows all visible nodes
  }
  return 1 // Local training
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

// 🔧 Helper function to generate mock node data
const generateMockNodesForProject = (project) => {
  const nodes = []
  
  if (project.type === 'local') {
    // Local training has only one node
    nodes.push({
      id: 'local-001',
      name: 'Local Node',
      label: 'Local Node',
      type: 'training',
      status: project.status === 'training' ? 'training' : 'idle',
      progress: project.progress,
      cpu: 'Intel i7',
      gpu: 'NVIDIA RTX 3080',
      memory: '32GB',
      ip: '127.0.0.1',
      x: 400,
      y: 300,
      resources: {
        cpu: 75,
        memory: 68,
        gpu: 85
      },
      trainingProgress: project.progress
    })
  } else if (project.type === 'federated') {
    // Federated learning has multiple nodes
    const nodeCount = 5
    for (let i = 0; i < nodeCount; i++) {
      nodes.push({
        id: `node-${String(i + 1).padStart(3, '0')}`,
        name: i === 0 ? 'Control Node' : `Training Node ${i}`,
        label: i === 0 ? 'Control Node' : `Node ${i}`,
        type: i === 0 ? 'control' : 'training',
        status: project.status === 'training' ? 'training' : 'idle',
        progress: project.progress,
        cpu: `CPU ${i + 1}`,
        gpu: i === 0 ? 'None' : `GPU ${i}`,
        memory: `${16 + i * 8}GB`,
        ip: `192.168.1.${100 + i}`,
        x: 200 + (i % 3) * 250,
        y: 200 + Math.floor(i / 3) * 200,
        resources: {
          cpu: 60 + Math.random() * 30,
          memory: 50 + Math.random() * 40,
          gpu: i === 0 ? null : 70 + Math.random() * 25
        },
        trainingProgress: project.progress
      })
    }
  } else if (project.type === 'mpc') {
    // MPC has multiple parties
    const nodeCount = 3
    for (let i = 0; i < nodeCount; i++) {
      nodes.push({
        id: `mpc-node-${i + 1}`,
        name: `MPC Party ${i + 1}`,
        label: `Party ${i + 1}`,
        type: 'mpc',
        status: project.status === 'completed' ? 'idle' : 'computing',
        progress: project.progress,
        cpu: 'Encrypted',
        gpu: 'N/A',
        memory: 'Protected',
        ip: 'Hidden',
        x: 300 + i * 200,
        y: 300,
        resources: null, // MPC does not display resource details
        trainingProgress: project.progress
      })
    }
  }
  
  return nodes
}

// Load project visualization data from EdgeAI API or P2P AI hardcoded data
const loadProjectVisualizationData = async () => {
  const pageMonitor = performanceMonitor.monitorPageLoad('P2PAIProjectVisualization')
  loading.value = true
  error.value = null

  try {
    const projectIdValue = projectId.value
    
    // Check if it's a P2P AI hardcoded project (ID 1, 2, 3)
    const projectIdNum = parseInt(projectIdValue)
    if (P2PAI_HARDCODED_PROJECTS[projectIdNum]) {
      console.warn('⚠️ Using P2P AI hardcoded project data')
      const project = P2PAI_HARDCODED_PROJECTS[projectIdNum]
      
      // Set project basic info
      projectDisplayName.value = project.name
      projectSubtitle.value = project.description
      
      // Generate mock node data based on project type
      const nodes = generateMockNodesForProject(project)
      networkData.value = {
        nodes: nodes,
        links: [],
        summary: {
          totalNodes: nodes.length,
          trainingNodes: nodes.filter(n => n.status === 'training').length,
          totalModels: 1,
          activeModels: project.status === 'training' ? 1 : 0
        }
      }
      
      // Set training state
      trainingState.value = {
        status: project.status,
        currentRound: Math.floor((project.progress / 100) * project.epochs),
        totalRounds: project.epochs,
        startTime: project.created_time,
        endTime: project.status === 'completed' ? new Date() : null
      }
      isTraining.value = project.status === 'training'
      
      console.log('✅ P2P AI project data loaded:', project)
      pageMonitor.end({ success: true, projectType: project.type })
      loading.value = false
      return
    }

    // Otherwise, try to load data from P2P AI API (fallback to EdgeAI API if needed)
    console.log('Trying to load project data from P2P AI API...')
    const visualizationData = await cachedApiCall(
      `p2pai-visualization-${projectIdValue}`,
      () => p2paiService.projects?.getProjectVisualization?.(projectIdValue) || edgeaiService.projects.getProjectVisualization(projectIdValue),
      30 * 1000 // Cache for 30 seconds for real-time updates
    )

    console.log('Visualization Data:', visualizationData)

    // Update project info with database data
    if (visualizationData.project) {
      // The project name should now have (db) suffix
      projectDisplayName.value = visualizationData.project.name
      projectSubtitle.value = visualizationData.project.description
    }

    // Update node data with real database nodes
    if (visualizationData.nodes && visualizationData.nodes.length > 0) {
      // Transform database nodes to visualization format
      const nodeVisualizationData = visualizationData.nodes.map((node, index) => ({
        id: node.id,
        name: node.name, // This should have (db) suffix
        label: node.name,
        type: node.role || 'worker',
        status: node.state, // Should be 'training' for most nodes
        progress: node.progress || 0,
        cpu: node.cpu || 'Unknown',
        gpu: node.gpu || 'None',
        memory: node.memory || 'Unknown',
        ip: node.path_ipv4 || '',
        x: 100 + (index % 3) * 200, // Simple layout
        y: 100 + Math.floor(index / 3) * 150
      }))

      // Update network data for visualization
      networkData.value = {
        nodes: nodeVisualizationData,
        links: [], // Could be enhanced with actual relationships
        summary: {
          totalNodes: visualizationData.summary.total_nodes,
          trainingNodes: visualizationData.summary.training_nodes,
          totalModels: visualizationData.summary.total_models,
          activeModels: visualizationData.summary.active_models
        }
      }

      console.log('Updated network data with database nodes:', networkData.value)
    }

    // Update model data
    if (visualizationData.models && visualizationData.models.length > 0) {
      console.log('Models from database:', visualizationData.models)
      // Models data can be used for additional displays if needed
    }

    // Set training state based on project status
    if (visualizationData.project) {
      trainingState.value = {
        status: visualizationData.project.status || 'idle',
        currentRound: Math.floor(visualizationData.project.progress || 0),
        totalRounds: visualizationData.project.epochs || 100,
        startTime: visualizationData.project.created_time,
        endTime: null
      }
      isTraining.value = visualizationData.project.status === 'training' || visualizationData.project.status === 'active'
    }

    pageMonitor.end({ success: true, projectType: projectType.value })
  } catch (err) {
    console.error('Failed to load EdgeAI project visualization data:', err)
    error.value = err.message || 'Failed to load project visualization data'
    pageMonitor.end({ success: false, error: err.message })
  } finally {
    loading.value = false
  }
}

// Setup auto-refresh for real-time training updates
const setupAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  
  refreshInterval.value = setInterval(() => {
    if (!loading.value && isTraining.value) {
      // Only refresh training data during training
      loadTrainingData()
    }
  }, 10 * 1000) // Refresh every 10 seconds during training
}

// Load only training data for real-time updates
const loadTrainingData = async () => {
  try {
    const projectIdValue = projectId.value
    const trainingResult = await p2paiService.training.getTrainingMetrics(projectIdValue)
    
    if (trainingResult) {
      localTrainingData.value = {
        rounds: trainingResult.rounds || localTrainingData.value.rounds,
        accuracy: trainingResult.accuracy || localTrainingData.value.accuracy,
        loss: trainingResult.loss || localTrainingData.value.loss,
        cpu: trainingResult.cpu_usage || localTrainingData.value.cpu,
        gpu: trainingResult.gpu_usage || localTrainingData.value.gpu,
        memory: trainingResult.memory_usage || localTrainingData.value.memory
      }
    }
  } catch (err) {
    console.error('Failed to refresh training data:', err)
  }
}

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
  if (projectType.value === 'federated' && (node.id === 'local-001' || node.type === 'control')) return true
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

// Additional methods - Required for bottom panel
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
onMounted(async () => {
  // Initialize P2P AI project visualization with real data
  console.log('Loading project visualization for:', projectId.value, 'Type:', projectType.value)
  
  // Load initial data
  await loadProjectVisualizationData()
  
  // Setup auto-refresh for real-time updates
  setupAutoRefresh()
  
  // Connect to P2P AI store WebSocket for real-time updates
  p2paiStore.connectWebSocket()
})

onUnmounted(() => {
  // Clean up resources
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
  
  // Clear API cache
  clearCache()
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

/* Custom Scrollbar Styles */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9; /* Light mode track background */
}

.dark .custom-scrollbar::-webkit-scrollbar-track {
  background: #1f2937; /* Dark mode track background */
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1; /* Light mode thumb */
  border-radius: 3px;
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #374151; /* Dark mode thumb */
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8; /* Light mode thumb hover */
}

.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #4b5563; /* Dark mode thumb hover */
}

/* Firefox scrollbar */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9; /* Light mode: thumb track */
}

.dark .custom-scrollbar {
  scrollbar-color: #374151 #1f2937; /* Dark mode: thumb track */
}
</style>