<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900">
    <!-- Navigation -->
    <nav class="glass-effect shadow-soft border-b border-slate-200 dark:border-slate-700">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <button 
              @click="goBack" 
              class="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors micro-bounce"
            >
              <ArrowLeftIcon class="w-5 h-5" />
            </button>
            
            <div class="w-8 h-8 bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center mr-3 micro-bounce hover-glow-primary">
              <UsersIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gradient text-shadow-soft">
              Federated Learning Training
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Node: {{ nodeId }}
            </span>
            <SimpleThemeToggle size="sm" />
          </div>
        </div>
      </div>
    </nav>

    <div class="max-w-6xl mx-auto px-6 py-8">
      <!-- Page Header -->
      <div class="text-center mb-8 animate-fade-in-up">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Federated Training Session
        </h2>
        <p class="text-gray-600 dark:text-gray-400">
          Participate in collaborative model training while preserving data privacy
        </p>
      </div>

      <!-- Training Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 stagger-children">
        <StatCard
          title="Training Status"
          :value="trainingStatus"
          :icon="statusIcon"
          :variant="statusVariant"
          description="Current session status"
          clickable
          animated
          @click="viewStatusDetails"
        />
        
        <StatCard
          title="Current Round"
          :value="currentRound"
          unit="/ 100"
          :icon="ArrowPathIcon"
          variant="primary"
          :progress="roundProgress"
          description="Training progress"
          animated
        />
        
        <StatCard
          title="Connected Nodes"
          :value="connectedNodes"
          :icon="ServerIcon"
          variant="success"
          :trend="nodesTrend"
          trend-label="vs last round"
          description="Active participants"
          animated
        />
      </div>

      <!-- Training Configuration -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Model Configuration -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <CpuChipIcon class="w-5 h-5 mr-2 text-blue-500" />
              Model Configuration
            </h3>
            
            <div class="space-y-4">
              <!-- Training Algorithm -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Training Algorithm
                </label>
                <select v-model="config.training_alg" class="input-base">
                  <option value="sft">Supervised Fine-Tuning (SFT)</option>
                  <option value="rlhf">Reinforcement Learning from Human Feedback (RLHF)</option>
                  <option value="dpo">Direct Preference Optimization (DPO)</option>
                </select>
              </div>

              <!-- Federated Algorithm -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Federated Algorithm
                </label>
                <select v-model="config.fed_alg" class="input-base">
                  <option value="fedavg">FedAvg</option>
                  <option value="fedprox">FedProx</option>
                  <option value="scaffold">SCAFFOLD</option>
                </select>
              </div>

              <!-- Model Path -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Model Name or Path
                </label>
                <input 
                  v-model="config.model_name_or_path" 
                  type="text" 
                  class="input-base"
                  placeholder="sshleifer/tiny-gpt2"
                />
              </div>

              <!-- Dataset -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Dataset Name
                </label>
                <input 
                  v-model="config.dataset_name" 
                  type="text" 
                  class="input-base"
                  placeholder="vicgalle/alpaca-gpt4"
                />
              </div>

              <!-- Learning Rate -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Learning Rate: {{ config.lr }}
                </label>
                <input 
                  v-model="config.lr" 
                  type="text" 
                  class="input-base"
                  placeholder="1e-4"
                />
              </div>

              <!-- Max Steps -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Max Steps
                </label>
                <input 
                  v-model="config.max_steps" 
                  type="number" 
                  min="1" 
                  max="10000"
                  class="input-base"
                />
              </div>

              <!-- Dataset Sample -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Dataset Sample Size
                </label>
                <input 
                  v-model="config.dataset_sample" 
                  type="number" 
                  min="1" 
                  max="1000"
                  class="input-base"
                />
              </div>
            </div>
          </div>
        </Card>

        <!-- Federated Learning Configuration -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <UsersIcon class="w-5 h-5 mr-2 text-green-500" />
              Federated Learning Configuration
            </h3>
            
            <div class="space-y-4">
              <!-- Number of Computers -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Number of Computers
                </label>
                <input 
                  v-model="config.num_computers" 
                  type="number" 
                  min="1" 
                  max="20"
                  class="input-base"
                />
              </div>

              <!-- Number of Rounds -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Number of Rounds
                </label>
                <input 
                  v-model="config.num_rounds" 
                  type="number" 
                  min="1" 
                  max="100"
                  class="input-base"
                />
              </div>

              <!-- Number of Clients -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Number of Clients
                </label>
                <input 
                  v-model="config.num_clients" 
                  type="number" 
                  min="1" 
                  max="50"
                  class="input-base"
                />
              </div>

              <!-- Sample Clients -->
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Sample Clients per Round
                </label>
                <input 
                  v-model="config.sample_clients" 
                  type="number" 
                  min="1" 
                  :max="config.num_clients"
                  class="input-base"
                />
              </div>
            </div>
          </div>
        </Card>

      </div>

      <!-- Control Panel -->
      <div class="mb-8">
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">Control Panel</h3>
            
            <div class="space-y-4">
              <!-- Training Status Button -->
              <div class="mb-4">
                <!-- 当有活跃任务时显示 Training 状态 -->
                <Button 
                  v-if="hasActiveTasks"
                  variant="outline"
                  size="sm"
                  class="w-full flex items-center justify-center space-x-2 border-blue-200 bg-white hover:bg-gray-50"
                  disabled
                >
                  <svg class="w-4 h-4 animate-spin text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                  </svg>
                  <span class="text-blue-600">Training</span>
                </Button>
                
                <!-- 当没有活跃任务时显示 Start Training 按钮 -->
                <Button 
                  v-else-if="trainingStatus === 'Ready' || trainingStatus === 'Stopped'"
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
              <div v-if="taskList.length > 0" class="mb-6">
                <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Task Management</h4>
                
                <!-- Task List -->
                <div class="mb-4">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-sm text-gray-900 dark:text-white">Active Tasks</span>
                    <Button 
                      @click="loadTaskList"
                      variant="ghost"
                      size="sm"
                      class="text-xs text-gray-500 hover:text-gray-700"
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
                         class="p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
                      <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center space-x-3">
                          <div class="flex items-center space-x-2">
                            <div :class="isTaskRunning(task) ? 'bg-green-500' : 'bg-gray-400'" class="w-2 h-2 rounded-full"></div>
                            <span class="text-xs font-medium" :class="isTaskRunning(task) ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'">
                              {{ isTaskRunning(task) ? 'Running' : 'Stopped' }}
                            </span>
                          </div>
                          <div class="flex items-center space-x-2">
                            <div class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs">
                              <span class="font-mono text-gray-600 dark:text-gray-300">{{ task.substring(0, 8) }}...</span>
                            </div>
                            <Button 
                              @click="copyTaskId(task)"
                              variant="ghost"
                              size="sm"
                              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 p-1"
                              title="复制任务ID"
                            >
                              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                              </svg>
                            </Button>
                          </div>
                        </div>
                        <Button 
                          @click="deleteTask(task)"
                          variant="ghost"
                          size="sm"
                          class="text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 p-1"
                          :disabled="isDeletingTask === task"
                          title="删除任务"
                        >
                          <svg v-if="isDeletingTask !== task" class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                          </svg>
                          <svg v-else class="w-3 h-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                          </svg>
                        </Button>
                      </div>
                      
                      <!-- Progress Bar -->
                      <div class="mb-3">
                        <div class="flex items-center justify-between mb-1">
                          <span class="text-xs text-gray-600 dark:text-gray-400">Training Progress</span>
                          <span class="text-xs font-medium text-gray-900 dark:text-white">
                            {{ getTaskProgressPercentage(task) }}%
                          </span>
                        </div>
                        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div 
                            class="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500 ease-out"
                            :style="{ width: getTaskProgressPercentage(task) + '%' }"
                          ></div>
                        </div>
                        <div class="flex items-center justify-between mt-1">
                          <span class="text-xs text-gray-500 dark:text-gray-400">
                            Round {{ (taskStatusMap[task]?.current_round ?? 0) }}/{{ (taskStatusMap[task]?.total_rounds ?? 0) }}
                          </span>
                          <span class="text-xs text-gray-500 dark:text-gray-400">
                            {{ getTaskProgressPercentage(task) }}% Complete
                          </span>
                        </div>
                      </div>

                      <!-- Task Status Row -->
                      <div class="grid grid-cols-2 gap-2">
                        <div class="flex items-center justify-between bg-gray-50 dark:bg-gray-700 rounded px-2 py-1">
                          <span class="text-xs text-gray-600 dark:text-gray-400">Loss</span>
                          <span class="text-xs font-medium text-red-600 dark:text-red-400">
                            {{ (taskStatusMap[task]?.loss ?? 0).toFixed(4) }}
                          </span>
                        </div>
                        <div class="flex items-center justify-between bg-gray-50 dark:bg-gray-700 rounded px-2 py-1">
                          <span class="text-xs text-gray-600 dark:text-gray-400">Accuracy</span>
                          <span class="text-xs font-medium text-green-600 dark:text-green-400">
                            {{ taskStatusMap[task]?.accuracy !== null && taskStatusMap[task]?.accuracy !== undefined
                              ? (taskStatusMap[task].accuracy * 100).toFixed(6) + '%' : 'N/A' }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
            </div>
          </div>
        </Card>
      </div>


      <!-- Network Status -->
      <div class="space-y-6">
        <!-- Connected Nodes Section -->
        <div class="space-y-6">
          <!-- Loading State -->
          <div v-if="networkLoading" class="text-center py-8">
            <div class="inline-flex items-center px-4 py-2 text-sm text-gray-600 dark:text-gray-400">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              Loading network nodes...
            </div>
          </div>
          
          <!-- Error State -->
          <div v-else-if="networkError" class="text-center py-8">
            <div class="text-red-600 dark:text-red-400 mb-2">
              <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
              {{ networkError }}
            </div>
            <button @click="loadNetworkNodes" class="text-blue-600 dark:text-blue-400 hover:underline">
              Retry
            </button>
          </div>
          
          <!-- Node Details List -->
          <div v-else class="space-y-6">

            <!-- Model Manager Nodes -->
            <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
              <div class="px-6 py-4 bg-green-50 dark:bg-green-900/20 border-b border-gray-200 dark:border-gray-700">
                <h3 class="text-lg font-semibold text-green-600 dark:text-green-400">
                  Model Manager Nodes ({{ managerNodes.length }})
                </h3>
              </div>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead class="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">IP</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Role</th>
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
                    <tr v-if="managerNodes.length === 0">
                      <td colspan="9" class="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                        No Model Manager Nodes found
                      </td>
                    </tr>
                    <tr
                      v-for="node in managerNodes"
                      :key="node.id"
                      class="hover:bg-gray-50 dark:hover:bg-gray-700"
                    >
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900 dark:text-white">
                        {{ node.ip }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {{ node.role }}
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

            <!-- Training Nodes -->
            <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
              <div class="px-6 py-4 bg-purple-50 dark:bg-purple-900/20 border-b border-gray-200 dark:border-gray-700">
                <h3 class="text-lg font-semibold text-purple-600 dark:text-purple-400">
                  Training Nodes ({{ trainingNodes.length }})
                </h3>
              </div>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead class="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">IP</th>
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Role</th>
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
                    <tr v-if="trainingNodes.length === 0">
                      <td colspan="9" class="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                        No Training Nodes found
                      </td>
                    </tr>
                    <tr
                      v-for="node in trainingNodes"
                      :key="node.id"
                      class="hover:bg-gray-50 dark:hover:bg-gray-700"
                    >
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900 dark:text-white">
                        {{ node.ip }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {{ node.role === 'edge AI training node' ? 'Training Nodes' : node.role }}
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
        </div>

      </div>
    </div>

    <!-- Training Details Modal -->
    <Modal
      :isOpen="showTrainingModal"
      @close="showTrainingModal = false"
      title="Training Session Details"
      size="lg"
    >
      <div class="space-y-4">
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Session Information</h4>
          <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
            <p>Session ID: {{ sessionId }}</p>
            <p>Started: {{ formatDateTime(sessionStartTime) }}</p>
            <p>Duration: {{ formatDuration(trainingDuration) }}</p>
          </div>
        </div>
        
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Performance Metrics</h4>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p class="text-gray-600 dark:text-gray-400">Current Accuracy:</p>
              <p class="font-medium text-green-600">{{ currentAccuracy.toFixed(2) }}%</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Best Accuracy:</p>
              <p class="font-medium text-green-600">{{ bestAccuracy.toFixed(2) }}%</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Current Loss:</p>
              <p class="font-medium text-red-600">{{ currentLoss.toFixed(4) }}</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Best Loss:</p>
              <p class="font-medium text-red-600">{{ bestLoss.toFixed(4) }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button @click="showTrainingModal = false" variant="secondary">
            Close
          </Button>
          <Button @click="exportTrainingLog" variant="primary">
            Export Log
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useApiOptimization } from '@/composables/useApiOptimization.js'
import p2paiService from '@/services/p2paiService.js'
import performanceMonitor from '@/utils/performanceMonitor.js'
import { API_ENDPOINTS, buildApiUrl } from '@/config/api.js'
import {
  ArrowLeftIcon,
  UsersIcon,
  CpuChipIcon,
  PlayIcon,
  StopIcon,
  PauseIcon,
  ChartBarIcon,
  GlobeAltIcon,
  ArrowPathIcon,
  ServerIcon
} from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import StatCard from '@/components/ui/StatCard.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'
import Modal from '@/components/ui/Modal.vue'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'

const router = useRouter()
const themeStore = useThemeStore()
const { cachedApiCall } = useApiOptimization()

// API loading state
const apiLoading = ref(false)
const apiError = ref(null)

// Training state
const isTraining = ref(false)
const isPaused = ref(false)
const trainingStatus = ref('Ready')
const currentRound = ref(0)
const trainingDuration = ref(0)
const sessionId = ref(null)
const sessionStartTime = ref(null)
const federatedWebSocket = ref(null)

// 后端训练接口配置与状态
// 使用API配置文件中的端点
const TRAIN_API_BASE = API_ENDPOINTS.P2P_AI.TRAINING
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

// Training configuration
const config = ref({
  training_alg: 'sft',
  fed_alg: 'fedavg',
  num_computers: 3,
  num_rounds: 10,
  num_clients: 2,
  sample_clients: 2,
  max_steps: 100,
  lr: '1e-4',
  model_name_or_path: 'sshleifer/tiny-gpt2',
  dataset_name: 'vicgalle/alpaca-gpt4',
  dataset_sample: 50
})

// Metrics
const currentAccuracy = ref(0)
const currentLoss = ref(0)
const bestAccuracy = ref(0)
const bestLoss = ref(Infinity)
const connectedNodes = ref(8)
const nodesTrend = ref(12.5)

// Network stats
const messagesSent = ref(0)
const messagesReceived = ref(0)
const networkLatency = ref(0)
const dataTransferred = ref(0)

// UI state
const showTrainingModal = ref(false)
const nodeId = ref('Node-001')

// Computed properties
const statusIcon = computed(() => {
  switch (trainingStatus.value) {
    case 'Training': return PlayIcon
    case 'Paused': return PauseIcon
    case 'Completed': return CheckCircleIcon
    case 'Error': return XCircleIcon
    default: return CpuChipIcon
  }
})

const statusVariant = computed(() => {
  switch (trainingStatus.value) {
    case 'Training': return 'success'
    case 'Paused': return 'warning'
    case 'Completed': return 'info'
    case 'Error': return 'danger'
    default: return 'default'
  }
})

const roundProgress = computed(() => {
  return (currentRound.value / 100) * 100
})

const overallProgress = computed(() => {
  return roundProgress.value * 0.6 + (currentAccuracy.value / 100) * 40
})

const canStartTraining = computed(() => {
  return !isTraining.value && connectedNodes.value >= 2
})

// 检查是否有活跃任务
const hasActiveTasks = computed(() => {
  return taskList.value.length > 0 && taskList.value.some(taskId => isTaskRunning(taskId))
})

const networkNodes = ref([])
const networkLoading = ref(false)
const networkError = ref(null)

// Computed properties for node categorization
const mpcNodes = computed(() => 
  networkNodes.value.filter(node => node.role === 'mpc model node')
)

const managerNodes = computed(() => 
  networkNodes.value.filter(node => node.role === 'model manager node')
)

const trainingNodes = computed(() => 
  networkNodes.value.filter(node => node.role === 'edge AI training node')
)

const totalNodes = computed(() => networkNodes.value.length)

// Methods
const goBack = () => {
  router.push('/p2pai/dashboard')
}

// 格式化heartbeat时间显示
const formatHeartbeat = (timestamp) => {
  if (!timestamp) return 'N/A'
  
  const now = Date.now()
  const diff = now - timestamp
  
  if (diff < 1000) {
    return '-1s ago'
  } else if (diff < 60000) {
    return `-${Math.floor(diff / 1000)}s ago`
  } else if (diff < 3600000) {
    return `-${Math.floor(diff / 60000)}m ago`
  } else {
    return `-${Math.floor(diff / 3600000)}h ago`
  }
}

// Load network nodes data from API
const loadNetworkNodes = async () => {
  try {
    networkLoading.value = true
    networkError.value = null
    
    const rayClusterUrl = buildApiUrl(API_ENDPOINTS.P2P_AI.TRAINING.RAY_CLUSTER)
    const response = await fetch(rayClusterUrl, {
      method: 'GET',
      headers: {
        'accept': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    // Transform API data to match our UI structure
    networkNodes.value = data.map((node, index) => ({
      id: `node-${index + 1}`,
      name: `Node-${String(index + 1).padStart(3, '0')}`,
      ip: node.ip,
      role: node.role,
      status: node.status === 'alive' ? 'online' : 'offline',
      cpuUsage: node.cpu_usage,
      memoryUsage: node.memory_usage,
      diskUsage: node.disk_usage,
      sent: node.sent,
      received: node.received,
      heartbeat: formatHeartbeat(node.heartbeat)
    }))
    
    // Calculate communication stats
    messagesSent.value = data.reduce((sum, node) => sum + (node.sent || 0), 0)
    messagesReceived.value = data.reduce((sum, node) => sum + (node.received || 0), 0)
    dataTransferred.value = (messagesSent.value + messagesReceived.value) * 1024 // Convert to bytes
    
    // Calculate average latency (simulated)
    const aliveNodes = data.filter(node => node.status === 'alive')
    networkLatency.value = aliveNodes.length > 0 ? Math.floor(Math.random() * 50) + 20 : 0
    
    // Update connected nodes count
    connectedNodes.value = networkNodes.value.filter(n => n.status === 'online' || n.status === 'training').length
    
    console.log('✅ Network nodes loaded successfully:', networkNodes.value)
  } catch (err) {
    console.error('❌ Failed to load network nodes:', err)
    networkError.value = err.message || 'Failed to load network data'
    
    // Fallback to mock data
    networkNodes.value = [
      { id: 'node-1', name: 'Node-001', status: 'training', ip: '10.0.4.31', role: 'model manager node' },
      { id: 'node-2', name: 'Node-002', status: 'online', ip: '43.135.30.207', role: 'mpc model node' },
      { id: 'node-3', name: 'Node-003', status: 'training', ip: '106.52.36.202', role: 'mpc model node' },
      { id: 'node-4', name: 'Node-004', status: 'online', ip: '114.132.200.147', role: 'edge AI training node' },
      { id: 'node-5', name: 'Node-005', status: 'offline', ip: '175.178.24.56', role: 'mpc model node' },
      { id: 'node-6', name: 'Node-006', status: 'online', ip: '42.194.177.24', role: 'edge AI training node' }
    ]
    messagesSent.value = 1247
    messagesReceived.value = 1189
    networkLatency.value = 45
    dataTransferred.value = 2048576
    connectedNodes.value = 4
  } finally {
    networkLoading.value = false
  }
}

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const startTraining = async () => {
  if (trainingStatus.value === 'Training' || isTrainingStarting.value) return
  
  isTrainingStarting.value = true
  try {
    // 从参数生成后端训练payload
    const payload = { parameters: { ...config.value } }
    console.log('🚀 发送训练请求到:', `${TRAIN_API_BASE}/train`, 'payload:', payload)
    // 发送开始训练请求
    const trainUrl = buildApiUrl(API_ENDPOINTS.P2P_AI.TRAINING.TRAIN)
    const resp = await fetch(trainUrl, {
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
    trainingStatus.value = 'Training'
    isTraining.value = true
    sessionStartTime.value = Date.now()
    currentRound.value = 0
    roundMetrics.value = []
    // 启动轮询监控
    startMonitor()
    // 自动刷新任务列表以显示新任务
    setTimeout(() => {
      loadTaskList()
      console.log('🔄 训练启动后自动刷新任务列表')
    }, 1000) // 延迟1秒确保后端任务已创建
    
    // 再次延迟刷新，确保任务完全创建
    setTimeout(() => {
      loadTaskList()
      console.log('🔄 训练启动后第二次刷新任务列表')
    }, 3000) // 延迟3秒再次刷新
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

const stopTraining = async () => {
  if (!sessionId.value) {
    // Local stop for simulation mode
    isTraining.value = false
    isPaused.value = false
    trainingStatus.value = 'Ready'
    return
  }
  
  try {
    console.log('🛑 Stopping federated training session:', sessionId.value)
    
    const response = await p2paiService.training.stopTraining(sessionId.value)
    
    if (response.success) {
      isTraining.value = false
      isPaused.value = false
      trainingStatus.value = 'Stopped'
      
      // Close WebSocket connection
      if (federatedWebSocket.value) {
        federatedWebSocket.value.close()
        federatedWebSocket.value = null
      }
      
      console.log('✅ Federated training stopped successfully')
    }
  } catch (err) {
    console.error('❌ Failed to stop federated training:', err)
    // Still update local state even if API call fails
    isTraining.value = false
    isPaused.value = false
    trainingStatus.value = 'Error'
  }
}

const pauseTraining = () => {
  isPaused.value = !isPaused.value
  trainingStatus.value = isPaused.value ? 'Paused' : 'Training'
}

const viewStatusDetails = () => {
  showTrainingModal.value = true
}

const onModelChange = () => {
  console.log('Configuration changed:', config.value)
}

const exportTrainingLog = () => {
  // Implementation for exporting training logs
  console.log('Exporting training log...')
}

const formatDuration = (ms) => {
  const seconds = Math.floor(ms / 1000) % 60
  const minutes = Math.floor(ms / (1000 * 60)) % 60
  const hours = Math.floor(ms / (1000 * 60 * 60))
  
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

const formatDateTime = (date) => {
  return date.toLocaleString()
}

const formatDataSize = (bytes) => {
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  
  return `${size.toFixed(2)} ${units[unitIndex]}`
}

const formatDataRate = (bytes) => {
  if (!bytes || bytes === 0) return '0.00 KB/s'
  const units = ['B/s', 'KB/s', 'MB/s', 'GB/s']
  let size = bytes
  let unitIndex = 0
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  
  return `${size.toFixed(2)} ${units[unitIndex]}`
}

const formatHeartbeat = (timestamp) => {
  if (!timestamp) return 'Never'
  const now = Date.now()
  const diff = now - timestamp
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  
  if (hours > 0) return `${hours}h ago`
  if (minutes > 0) return `${minutes}m ago`
  return `${seconds}s ago`
}

// 轮询监控训练进度
const startMonitor = () => {
  stopMonitor()
  if (!trainingTaskId.value) return
  monitorTimer.value = setInterval(async () => {
    try {
      console.log('🔍 轮询监控 task_id:', trainingTaskId.value)
      const monitorUrl = buildApiUrl(API_ENDPOINTS.P2P_AI.TRAINING.MONITOR, { taskId: trainingTaskId.value })
      const resp = await fetch(monitorUrl, {
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
      const current = Number(data.current_round ?? data.round ?? currentRound.value)
      const total = Number(data.total_rounds ?? 100)
      const loss = data.loss
      const accuracy = data.accuracy
      console.log('📈 解析数据 - current:', current, 'total:', total, 'loss:', loss, 'accuracy:', accuracy)
      currentRound.value = current
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
        trainingStatus.value = 'Completed'
        console.log('🏁 训练完成!')
        stopMonitor()
      }
    } catch (e) {
      console.error('Monitor error:', e)
      // 如果是404错误，说明任务不存在，停止监控
      if (e.message.includes('404')) {
        console.log('🛑 训练任务不存在，停止监控')
        stopMonitor()
        trainingStatus.value = 'Stopped'
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
    const tasksListUrl = buildApiUrl(API_ENDPOINTS.P2P_AI.TRAINING.TASKS_LIST)
    const resp = await fetch(tasksListUrl, {
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
    // 兼容新旧两种返回：
    // 旧：{ tasks: [id1, id2] }
    // 新：{ "<taskId>": "running", ... }
    let newTaskList = []
    if (Array.isArray(data?.tasks)) {
      newTaskList = data.tasks
    } else if (data && typeof data === 'object') {
      newTaskList = Object.keys(data)
      // 将已有状态预置到缓存（若后续监控接口不可用时也能展示占位）
      for (const [taskId, statusText] of Object.entries(data)) {
        if (!taskStatusMap.value[taskId]) {
          taskStatusMap.value[taskId] = { current_round: 0, total_rounds: 0, loss: 0, accuracy: null, statusText }
        } else {
          taskStatusMap.value[taskId].statusText = statusText
        }
      }
    } else if (Array.isArray(data)) {
      newTaskList = data
    } else {
      newTaskList = []
    }
    // 只保留 running 的任务
    const runningTasks = newTaskList.filter(id => isTaskRunning(id))
    console.log('📋 更新任务列表:', { 
      oldCount: taskList.value.length, 
      newCount: newTaskList.length,
      runningCount: runningTasks.length,
      allTasks: newTaskList,
      runningTasks: runningTasks
    })
    taskList.value = runningTasks

    // 并行查询每个任务的状态
    await refreshAllTaskStatuses()
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
      const monitorUrl = buildApiUrl(API_ENDPOINTS.P2P_AI.TRAINING.MONITOR, { taskId })
      const resp = await fetch(monitorUrl, {
        method: 'GET', headers: { accept: 'application/json' }
      })
      if (!resp.ok) throw new Error(`status ${resp.status}`)
      const status = await resp.json()
      const prev = taskStatusMap.value?.[taskId] || {}
      return [taskId, {
        // 保留由 tasksList 写入的状态文本（running/deleted等）
        statusText: prev.statusText,
        current_round: Number(status.current_round ?? 0),
        total_rounds: Number(status.total_rounds ?? 0),
        loss: typeof status.loss === 'number' ? status.loss : 0,
        accuracy: status.accuracy
      }]
    } catch (err) {
      console.warn('获取任务状态失败:', taskId, err.message)
      const prev = taskStatusMap.value?.[taskId] || {}
      return [taskId, { statusText: prev.statusText, current_round: 0, total_rounds: 0, loss: 0, accuracy: null }]
    }
  }))
  taskStatusMap.value = Object.fromEntries(entries)
  console.log('📦 任务状态缓存:', taskStatusMap.value)
}

// 判定任务是否 running（基于 tasksList 返回的状态文本缓存）
const isTaskRunning = (taskId) => {
  try {
    const statusText = taskStatusMap.value?.[taskId]?.statusText
    return String(statusText || '').toLowerCase() === 'running'
  } catch (e) {
    return false
  }
}

// 计算任务进度百分比
const getTaskProgressPercentage = (taskId) => {
  const taskStatus = taskStatusMap.value[taskId]
  if (!taskStatus) return 0
  
  const currentRound = Number(taskStatus.current_round || 0)
  const totalRounds = Number(taskStatus.total_rounds || 0)
  
  if (totalRounds <= 0) return 0
  
  const percentage = Math.min(100, Math.max(0, (currentRound / totalRounds) * 100))
  return Math.round(percentage)
}

// 复制任务ID到剪贴板
const copyTaskId = async (taskId) => {
  try {
    await navigator.clipboard.writeText(taskId)
    // 可以添加一个简单的提示，比如 toast 通知
    console.log('任务ID已复制到剪贴板:', taskId)
    // 这里可以添加一个 toast 通知组件
    alert(`任务ID已复制: ${taskId}`)
  } catch (err) {
    console.error('复制失败:', err)
    // 降级方案：使用传统的复制方法
    const textArea = document.createElement('textarea')
    textArea.value = taskId
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    alert(`任务ID已复制: ${taskId}`)
  }
}

const deleteTask = async (taskId) => {
  if (isDeletingTask.value) return
  
  isDeletingTask.value = taskId
  try {
    console.log('🗑️ 删除任务:', taskId)
    const deleteUrl = buildApiUrl(API_ENDPOINTS.P2P_AI.TRAINING.TASK_DELETE, { taskId })
    const resp = await fetch(deleteUrl, {
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
      trainingStatus.value = 'Stopped'
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

// Setup WebSocket connection for real-time federated updates
const setupFederatedWebSocket = (sessionId) => {
  if (federatedWebSocket.value) {
    federatedWebSocket.value.close()
  }
  
  try {
    federatedWebSocket.value = p2paiService.training.createTrainingWebSocket(sessionId, {
      onOpen: () => {
        console.log('📡 Federated WebSocket connected')
      },
      onMessage: (data) => {
        console.log('📨 Federated update received:', data)
        updateFederatedMetrics(data)
      },
      onError: (error) => {
        console.error('❌ Federated WebSocket error:', error)
      },
      onClose: () => {
        console.log('🔌 Federated WebSocket closed')
        if (isTraining.value) {
          // Try to reconnect after 3 seconds
          setTimeout(() => setupFederatedWebSocket(sessionId), 3000)
        }
      }
    })
  } catch (err) {
    console.error('Failed to setup federated WebSocket:', err)
  }
}

// Update federated metrics from WebSocket data
const updateFederatedMetrics = (data) => {
  if (data.type === 'federated_round') {
    currentRound.value = data.round || currentRound.value
    currentAccuracy.value = data.accuracy || currentAccuracy.value
    currentLoss.value = data.loss || currentLoss.value
    connectedNodes.value = data.connected_nodes || connectedNodes.value
    
    if (data.accuracy > bestAccuracy.value) {
      bestAccuracy.value = data.accuracy
    }
    if (data.loss < bestLoss.value) {
      bestLoss.value = data.loss
    }
    
    // Update node information
    if (data.nodes) {
      networkNodes.value = data.nodes.map(node => ({
        id: node.id,
        name: node.name,
        status: node.status
      }))
    }
  } else if (data.type === 'federated_completed') {
    trainingStatus.value = 'Completed'
    isTraining.value = false
    isPaused.value = false
  } else if (data.type === 'federated_error') {
    trainingStatus.value = 'Error'
    apiError.value = data.message || 'Federated training error occurred'
    isTraining.value = false
    isPaused.value = false
  }
}

// Load connected nodes data
const loadNodesData = async () => {
  try {
    const nodesResponse = await cachedApiCall(
      'federated-nodes',
      () => p2paiService.nodes.getNodes({ type: 'federated' }),
      30 * 1000 // 30 second cache
    )
    
    if (nodesResponse.data?.nodes) {
      networkNodes.value = nodesResponse.data.nodes.map(node => ({
        id: node.id,
        name: node.name,
        status: node.status || 'offline'
      }))
      connectedNodes.value = networkNodes.value.filter(n => n.status === 'online' || n.status === 'training').length
    }
  } catch (err) {
    console.warn('Failed to load nodes data:', err)
  }
}

// Lifecycle
onMounted(async () => {
  console.log('🌐 Federated Training component mounted')
  
  // Initialize default values
  currentAccuracy.value = 0
  currentLoss.value = 2.5
  bestLoss.value = 2.5
  
  // Load initial nodes data
  await loadNodesData()
  
  // Load network nodes data
  await loadNetworkNodes()
  
  // Load task list
  await loadTaskList()
  
  // 启动定期刷新节点数据
  startNodeRefreshTimer()
})

// 添加节点数据定期刷新
let nodeRefreshTimer = null

const startNodeRefreshTimer = () => {
  if (nodeRefreshTimer) {
    clearInterval(nodeRefreshTimer)
  }
  
  // 每5秒刷新一次节点数据
  nodeRefreshTimer = setInterval(async () => {
    try {
      await loadNetworkNodes()
    } catch (error) {
      console.error('❌ 定期刷新节点数据失败:', error)
    }
  }, 5000)
}

const stopNodeRefreshTimer = () => {
  if (nodeRefreshTimer) {
    clearInterval(nodeRefreshTimer)
    nodeRefreshTimer = null
  }
}

onUnmounted(() => {
  console.log('🧹 Cleaning up Federated Training component')
  
  // Close WebSocket connection
  if (federatedWebSocket.value) {
    federatedWebSocket.value.close()
    federatedWebSocket.value = null
  }
  
  // Stop monitoring
  stopMonitor()
  
  // Stop node refresh timer
  stopNodeRefreshTimer()
  
  // Stop training if active
  if (isTraining.value) {
    stopTraining()
  }
})
</script>

<style scoped>
input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
}
</style>