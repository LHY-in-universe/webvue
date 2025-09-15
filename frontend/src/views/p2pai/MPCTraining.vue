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
              <LockClosedIcon class="h-5 w-5 text-slate-600 dark:text-slate-300" />
            </div>
            <h1 class="text-xl font-semibold text-gradient text-shadow-soft">
              Multi-Party Computation Training
            </h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Party: {{ partyId }}
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
          Secure Multi-Party Training
        </h2>
        <p class="text-gray-600 dark:text-gray-400">
          Train models collaboratively with cryptographic privacy guarantees
        </p>
      </div>
      <!-- Security Status Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 stagger-children">
        <StatCard
          title="Protocol Status"
          :value="protocolStatus"
          :icon="statusIcon"
          :variant="statusVariant"
          description="MPC protocol state"
          clickable
          animated
          @click="viewProtocolDetails"
        />
        <StatCard
          title="Connected Parties"
          :value="connectedParties"
          unit="/ 3"
          :icon="UsersIcon"
          variant="primary"
          :progress="partyProgress"
          description="Active participants"
          animated
        />
        <StatCard
          title="Privacy Level"
          :value="privacyLevel"
          :icon="ShieldCheckIcon"
          variant="success"
          description="Data protection"
          animated
        />
        <StatCard
          title="Computation Round"
          :value="currentRound"
          unit="/ 100"
          :icon="ArrowPathIcon"
          variant="info"
          :progress="roundProgress"
          description="Training progress"
          animated
        />
      </div>
      <!-- MPC Configuration -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Security Configuration -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <LockClosedIcon class="w-5 h-5 mr-2 text-red-500" />
              Security Configuration
            </h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  MPC Protocol
                </label>
                <select 
                  v-model="selectedProtocol" 
                  class="input-base"
                  @change="onProtocolChange"
                  :disabled="isTraining"
                >
                  <option value="shamir">Shamir Secret Sharing</option>
                  <option value="bgw">BGW Protocol</option>
                  <option value="spdz">SPDZ Protocol</option>
                  <option value="aby">ABY Framework</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Security Parameter (bits): {{ securityBits }}
                </label>
                <input 
                  v-model="securityBits" 
                  type="range" 
                  min="64" 
                  max="256" 
                  step="32"
                  class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
                  :disabled="isTraining"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Threshold (t of n)
                </label>
                <div class="grid grid-cols-2 gap-4">
                  <input 
                    v-model="threshold" 
                    type="number" 
                    min="1" 
                    :max="totalParties - 1"
                    class="input-base"
                    :disabled="isTraining"
                  />
                  <input 
                    v-model="totalParties" 
                    type="number" 
                    min="3" 
                    max="10"
                    class="input-base"
                    :disabled="isTraining"
                  />
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <div class="flex items-center">
                  <input 
                    id="homomorphic" 
                    v-model="useHomomorphic" 
                    type="checkbox"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    :disabled="isTraining"
                  />
                  <label for="homomorphic" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                    Homomorphic Encryption
                  </label>
                </div>
                <div class="flex items-center">
                  <input 
                    id="differential-privacy" 
                    v-model="useDifferentialPrivacy" 
                    type="checkbox"
                    class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    :disabled="isTraining"
                  />
                  <label for="differential-privacy" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                    Differential Privacy
                  </label>
                </div>
              </div>
            </div>
          </div>
        </Card>
        <!-- Training Configuration -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <CpuChipIcon class="w-5 h-5 mr-2 text-blue-500" />
              Training Configuration
            </h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Model Type
                </label>
                <select 
                  v-model="selectedModel" 
                  class="input-base"
                  :disabled="isTraining"
                >
                  <option value="linear">Linear Regression</option>
                  <option value="logistic">Logistic Regression</option>
                  <option value="neural">Neural Network</option>
                  <option value="tree">Decision Tree</option>
                </select>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Learning Rate
                  </label>
                  <input 
                    v-model="learningRate" 
                    type="number" 
                    step="0.001" 
                    min="0.001" 
                    max="1"
                    class="input-base"
                    :disabled="isTraining"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Batch Size
                  </label>
                  <input 
                    v-model="batchSize" 
                    type="number" 
                    min="16" 
                    max="256" 
                    step="16"
                    class="input-base"
                    :disabled="isTraining"
                  />
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Max Rounds
                  </label>
                  <input 
                    v-model="maxRounds" 
                    type="number" 
                    min="10" 
                    max="1000"
                    class="input-base"
                    :disabled="isTraining"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Convergence Threshold
                  </label>
                  <input 
                    v-model="convergenceThreshold" 
                    type="number" 
                    step="0.0001" 
                    min="0.0001"
                    class="input-base"
                    :disabled="isTraining"
                  />
                </div>
              </div>
              <!-- Privacy Parameters -->
              <div v-if="useDifferentialPrivacy" class="border-t border-gray-200 dark:border-gray-700 pt-4">
                <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Differential Privacy Parameters
                </h4>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                      Epsilon (ε)
                    </label>
                    <input 
                      v-model="epsilon" 
                      type="number" 
                      step="0.1" 
                      min="0.1" 
                      max="10"
                      class="input-base text-sm"
                      :disabled="isTraining"
                    />
                  </div>
                  <div>
                    <label class="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                      Delta (δ)
                    </label>
                    <input 
                      v-model="delta" 
                      type="number" 
                      step="0.00001" 
                      min="0.00001" 
                      max="0.01"
                      class="input-base text-sm"
                      :disabled="isTraining"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
      <!-- Training Controls and Status -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Training Controls -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <PlayIcon class="w-5 h-5 mr-2 text-green-500" />
              MPC Training Controls
            </h3>
            <div class="space-y-4">
              <!-- Party Connection Status -->
              <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4 mb-4">
                <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Party Status</h4>
                <div class="space-y-2">
                  <div 
                    v-for="party in parties" 
                    :key="party.id"
                    class="flex items-center justify-between"
                  >
                    <div class="flex items-center">
                      <div :class="[
                        'w-3 h-3 rounded-full mr-3',
                        party.connected ? 'bg-green-500' : 'bg-red-500'
                      ]"></div>
                      <span class="text-sm">{{ party.name }}</span>
                    </div>
                    <span class="text-xs text-gray-500 capitalize">
                      {{ party.connected ? 'Connected' : 'Offline' }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="flex space-x-3">
                <Button 
                  v-if="!isTraining" 
                  @click="startMPCTraining"
                  variant="primary"
                  :leftIcon="PlayIcon"
                  class="flex-1"
                  :disabled="!canStartTraining"
                >
                  Start MPC Training
                </Button>
                <Button 
                  v-else
                  @click="stopTraining"
                  variant="danger"
                  :leftIcon="StopIcon"
                  class="flex-1"
                >
                  Stop Training
                </Button>
                <Button 
                  v-if="isTraining"
                  @click="pauseTraining"
                  variant="warning"
                  :leftIcon="PauseIcon"
                  :disabled="isPaused"
                >
                  {{ isPaused ? 'Paused' : 'Pause' }}
                </Button>
              </div>
              <!-- Training Progress -->
              <div class="space-y-3">
                <ProgressBar 
                  :percentage="overallProgress"
                  variant="success"
                  :animated="isTraining"
                  :show-percentage="true"
                />
                <p class="text-xs text-gray-500 dark:text-gray-400 text-center">
                  Overall MPC Training Progress
                </p>
                <ProgressBar 
                  :percentage="protocolProgress"
                  variant="primary"
                  :animated="isTraining"
                  :show-percentage="true"
                  size="sm"
                />
                <p class="text-xs text-gray-500 dark:text-gray-400 text-center">
                  Current Protocol Round
                </p>
              </div>
              <!-- Training Stats -->
              <div class="bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
                <div class="text-sm text-gray-700 dark:text-gray-300 space-y-2">
                  <div class="flex justify-between">
                    <span>Training Time:</span>
                    <span class="font-medium">{{ formatDuration(trainingDuration) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Communication Rounds:</span>
                    <span class="font-medium">{{ communicationRounds.toLocaleString() }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Data Transferred:</span>
                    <span class="font-medium">{{ formatDataSize(dataTransferred) }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Privacy Guarantee:</span>
                    <span class="font-medium text-green-600">{{ privacyLevel }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>
        <!-- Security Metrics -->
        <Card class="glass-effect">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <ShieldCheckIcon class="w-5 h-5 mr-2 text-green-500" />
              Security Metrics
            </h3>
            <div class="space-y-4">
              <!-- Security Level Indicators -->
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <div class="text-sm text-green-600 dark:text-green-400">Data Privacy</div>
                  <div class="text-xl font-bold text-green-700 dark:text-green-300">100%</div>
                </div>
                <div class="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <div class="text-sm text-blue-600 dark:text-blue-400">Protocol Security</div>
                  <div class="text-xl font-bold text-blue-700 dark:text-blue-300">{{ securityBits }}-bit</div>
                </div>
                <div class="text-center p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                  <div class="text-sm text-purple-600 dark:text-purple-400">Communication</div>
                  <div class="text-xl font-bold text-purple-700 dark:text-purple-300">Encrypted</div>
                </div>
                <div class="text-center p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                  <div class="text-sm text-orange-600 dark:text-orange-400">Verification</div>
                  <div class="text-xl font-bold text-orange-700 dark:text-orange-300">Active</div>
                </div>
              </div>
              <!-- Protocol Performance -->
              <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
                <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Protocol Performance</h4>
                <div class="space-y-3">
                  <div>
                    <div class="flex justify-between text-xs mb-1">
                      <span class="text-gray-600 dark:text-gray-400">Computation Load:</span>
                      <span>{{ computationLoad }}%</span>
                    </div>
                    <ProgressBar :percentage="computationLoad" variant="info" size="sm" />
                  </div>
                  <div>
                    <div class="flex justify-between text-xs mb-1">
                      <span class="text-gray-600 dark:text-gray-400">Network Load:</span>
                      <span>{{ networkLoad }}%</span>
                    </div>
                    <ProgressBar :percentage="networkLoad" variant="warning" size="sm" />
                  </div>
                  <div>
                    <div class="flex justify-between text-xs mb-1">
                      <span class="text-gray-600 dark:text-gray-400">Memory Usage:</span>
                      <span>{{ memoryUsage }}%</span>
                    </div>
                    <ProgressBar :percentage="memoryUsage" variant="success" size="sm" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
      <!-- Training Results -->
      <Card class="glass-effect">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <ChartBarIcon class="w-5 h-5 mr-2 text-purple-500" />
            Training Results
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Model Performance -->
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">Model Performance</h4>
              <div class="space-y-4">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Current Accuracy:</span>
                  <span class="text-lg font-semibold text-green-600">{{ currentAccuracy.toFixed(2) }}%</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Current Loss:</span>
                  <span class="text-lg font-semibold text-red-600">{{ currentLoss.toFixed(4) }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Convergence Rate:</span>
                  <span class="text-lg font-semibold text-blue-600">{{ convergenceRate.toFixed(3) }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Training Rounds:</span>
                  <span class="text-lg font-semibold text-purple-600">{{ currentRound }} / {{ maxRounds }}</span>
                </div>
              </div>
            </div>
            <!-- Privacy Analysis -->
            <div>
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">Privacy Analysis</h4>
              <div class="space-y-4">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Privacy Budget (ε):</span>
                  <span class="text-lg font-semibold text-orange-600">
                    {{ useDifferentialPrivacy ? epsilon : 'N/A' }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Secret Shares:</span>
                  <span class="text-lg font-semibold text-cyan-600">{{ threshold }} of {{ totalParties }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Adversary Resistance:</span>
                  <span class="text-lg font-semibold text-red-600">{{ threshold - 1 }} parties</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Protocol Type:</span>
                  <span class="text-lg font-semibold text-indigo-600">{{ selectedProtocol.toUpperCase() }}</span>
                </div>
              </div>
            </div>
          </div>
          <!-- Chart Placeholder -->
          <div class="mt-6 h-64 bg-gray-50 dark:bg-slate-700 rounded-lg flex items-center justify-center">
            <div class="text-center">
              <ChartBarIcon class="w-12 h-12 text-gray-400 mx-auto mb-2" />
              <p class="text-gray-500 dark:text-gray-400">MPC Training Convergence Chart</p>
              <p class="text-xs text-gray-400 mt-1">Privacy-preserving visualization coming soon</p>
            </div>
          </div>
        </div>
      </Card>
      </div>
      <!-- Enhanced Progress Demonstrations -->
      <Card v-if="isTraining" class="glass-effect mt-8">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <ArrowPathIcon class="w-5 h-5 mr-2 text-blue-500" />
            Advanced Training Progress
          </h3>
          <div class="space-y-6">
            <!-- Enhanced Overall Progress with Buffer -->
            <div>
              <ProgressBar 
                :value="currentRound"
                :max="maxRounds"
                :bufferValue="currentRound + 5"
                label="Training Progress with Buffer"
                variant="primary"
                :animated="true"
                :striped="true"
                :showValue="true"
                :showInnerLabel="true"
                unit=" rounds"
                :status="isTraining ? 'Training in progress...' : 'Ready to start'"
                info="Buffer shows lookahead computation"
              />
            </div>
            <!-- Segmented Progress for Phases -->
            <div>
              <ProgressBar 
                :percentage="Math.min(100, (currentRound / maxRounds) * 100)"
                label="Training Phases"
                variant="success"
                :segments="4"
                :animated="true"
                size="lg"
                info="Phase 1: Setup | Phase 2: Training | Phase 3: Validation | Phase 4: Aggregation"
              />
            </div>
            <!-- Multiple Value Progress -->
            <div>
              <ProgressBar 
                label="Resource Utilization"
                :multipleValues="[
                  { label: 'CPU Usage', value: computationLoad, color: 'primary' },
                  { label: 'Network I/O', value: networkLoad, color: 'warning' },
                  { label: 'Memory', value: memoryUsage, color: 'success' },
                  { label: 'Privacy Budget', value: Math.min(100, (epsilon / 10) * 100), color: 'danger' }
                ]"
                unit="%"
                :max="100"
              />
            </div>
            <!-- Step-based Progress -->
            <div>
              <ProgressBar 
                :value="currentRound"
                :max="maxRounds"
                :steps="[
                  { value: 10, label: 'Initial Setup', icon: 'play' },
                  { value: 25, label: 'Key Exchange', icon: 'key' },
                  { value: 50, label: 'Training Phase', icon: 'cpu' },
                  { value: 75, label: 'Validation', icon: 'check' },
                  { value: 100, label: 'Complete', icon: 'flag' }
                ]"
                label="MPC Protocol Steps"
                variant="info"
                :showValue="true"
                unit=" rounds"
              />
            </div>
          </div>
        </div>
      </Card>
    </div>
    <!-- Protocol Details Modal -->
    <Modal
      :isOpen="showProtocolModal"
      @close="showProtocolModal = false"
      title="MPC Protocol Details"
      size="lg"
    >
      <div class="space-y-4">
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Protocol Configuration</h4>
          <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
            <p>Protocol: {{ selectedProtocol.toUpperCase() }}</p>
            <p>Security Parameter: {{ securityBits }} bits</p>
            <p>Threshold Scheme: {{ threshold }} of {{ totalParties }}</p>
            <p>Homomorphic Encryption: {{ useHomomorphic ? 'Enabled' : 'Disabled' }}</p>
            <p>Differential Privacy: {{ useDifferentialPrivacy ? 'Enabled' : 'Disabled' }}</p>
          </div>
        </div>
        <div>
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Communication Statistics</h4>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p class="text-gray-600 dark:text-gray-400">Total Rounds:</p>
              <p class="font-medium">{{ communicationRounds.toLocaleString() }}</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Data Transferred:</p>
              <p class="font-medium">{{ formatDataSize(dataTransferred) }}</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Average Latency:</p>
              <p class="font-medium">{{ averageLatency }}ms</p>
            </div>
            <div>
              <p class="text-gray-600 dark:text-gray-400">Throughput:</p>
              <p class="font-medium">{{ throughput }} ops/sec</p>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button @click="showProtocolModal = false" variant="secondary">
            Close
          </Button>
          <Button @click="exportProtocolLog" variant="primary">
            Export Protocol Log
          </Button>
        </div>
      </template>
    </Modal>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useApiOptimization } from '@/composables/useApiOptimization.js'
import p2paiService from '@/services/p2paiService.js'
import performanceMonitor from '@/utils/performanceMonitor.js'
import {
  ArrowLeftIcon,
  LockClosedIcon,
  UsersIcon,
  ShieldCheckIcon,
  CpuChipIcon,
  PlayIcon,
  StopIcon,
  PauseIcon,
  ChartBarIcon,
  ArrowPathIcon
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
const isTraining = ref(false)
const isPaused = ref(false)
const protocolStatus = ref('Ready')
const currentRound = ref(0)
const trainingDuration = ref(0)
const partyId = ref('Party-A')
const sessionId = ref(null)
const mpcWebSocket = ref(null)
const selectedProtocol = ref('shamir')
const securityBits = ref(128)
const threshold = ref(2)
const totalParties = ref(3)
const useHomomorphic = ref(true)
const useDifferentialPrivacy = ref(false)
const privacyLevel = ref('Cryptographic')
const selectedModel = ref('logistic')
const learningRate = ref(0.01)
const batchSize = ref(64)
const maxRounds = ref(100)
const convergenceThreshold = ref(0.001)
const epsilon = ref(1.0)
const delta = ref(0.00001)
const currentAccuracy = ref(0)
const currentLoss = ref(0)
const convergenceRate = ref(0)
const communicationRounds = ref(0)
const dataTransferred = ref(0)
const averageLatency = ref(0)
const throughput = ref(0)
const computationLoad = ref(0)
const networkLoad = ref(0)
const memoryUsage = ref(0)
const showProtocolModal = ref(false)
const parties = ref([
  { id: 'A', name: 'Party A (You)', connected: true },
  { id: 'B', name: 'Party B', connected: true },
  { id: 'C', name: 'Party C', connected: false }
])
const statusIcon = computed(() => {
  switch (protocolStatus.value) {
    case 'Training': return PlayIcon
    case 'Paused': return PauseIcon
    case 'Completed': return CheckCircleIcon
    case 'Error': return XCircleIcon
    default: return LockClosedIcon
  }
})
const statusVariant = computed(() => {
  switch (protocolStatus.value) {
    case 'Training': return 'success'
    case 'Paused': return 'warning'
    case 'Completed': return 'info'
    case 'Error': return 'danger'
    default: return 'default'
  }
})
const connectedParties = computed(() => {
  return parties.value.filter(p => p.connected).length
})
const partyProgress = computed(() => {
  return (connectedParties.value / totalParties.value) * 100
})
const roundProgress = computed(() => {
  return (currentRound.value / maxRounds.value) * 100
})
const overallProgress = computed(() => {
  return roundProgress.value * 0.8 + (currentAccuracy.value / 100) * 20
})
const protocolProgress = computed(() => {
  return Math.min(100, (communicationRounds.value % 100))
})
const canStartTraining = computed(() => {
  return !isTraining.value && connectedParties.value >= threshold.value
})
const goBack = () => {
  router.push('/p2pai/dashboard')
}
const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}
const onProtocolChange = () => {
  console.log('Protocol changed to:', selectedProtocol.value)
}
const startMPCTraining = async () => {
  if (!canStartTraining.value) return
  
  apiLoading.value = true
  apiError.value = null
  
  try {
    // Prepare MPC training configuration
    const mpcConfig = {
      protocol: selectedProtocol.value,
      security_parameters: {
        security_bits: securityBits.value,
        threshold: threshold.value,
        total_parties: totalParties.value,
        use_homomorphic: useHomomorphic.value,
        use_differential_privacy: useDifferentialPrivacy.value
      },
      model_config: {
        model_type: selectedModel.value,
        learning_rate: learningRate.value,
        batch_size: batchSize.value,
        max_rounds: maxRounds.value,
        convergence_threshold: convergenceThreshold.value
      },
      privacy_config: useDifferentialPrivacy.value ? {
        epsilon: epsilon.value,
        delta: delta.value
      } : null
    }
    
    console.log('🔒 Starting MPC training with config:', mpcConfig)
    
    // Start MPC training via API
    const response = await p2paiService.training.startMPCTraining(mpcConfig)
    
    if (response.success) {
      // Update state with real session data
      sessionId.value = response.data.session_id
      isTraining.value = true
      protocolStatus.value = 'Training'
      currentRound.value = 0
      communicationRounds.value = 0
      
      // Setup WebSocket connection for real-time updates
      setupMPCWebSocket(sessionId.value)
      
      console.log('✅ MPC training started successfully:', response.data)
    } else {
      throw new Error(response.error || 'Failed to start MPC training')
    }
  } catch (err) {
    console.error('❌ Failed to start MPC training:', err)
    apiError.value = err.message || 'Failed to start MPC training'
    protocolStatus.value = 'Error'
  } finally {
    apiLoading.value = false
  }
}
const stopTraining = async () => {
  if (!sessionId.value) {
    // Local stop for simulation mode
    isTraining.value = false
    isPaused.value = false
    protocolStatus.value = 'Ready'
    return
  }
  
  try {
    console.log('🛑 Stopping MPC training session:', sessionId.value)
    
    const response = await p2paiService.training.stopTraining(sessionId.value)
    
    if (response.success) {
      isTraining.value = false
      isPaused.value = false
      protocolStatus.value = 'Stopped'
      
      // Close WebSocket connection
      if (mpcWebSocket.value) {
        mpcWebSocket.value.close()
        mpcWebSocket.value = null
      }
      
      console.log('✅ MPC training stopped successfully')
    }
  } catch (err) {
    console.error('❌ Failed to stop MPC training:', err)
    // Still update local state even if API call fails
    isTraining.value = false
    isPaused.value = false
    protocolStatus.value = 'Error'
  }
}
const pauseTraining = () => {
  isPaused.value = !isPaused.value
  protocolStatus.value = isPaused.value ? 'Paused' : 'Training'
}
const viewProtocolDetails = () => {
  showProtocolModal.value = true
}
const exportProtocolLog = () => {
  console.log('Exporting MPC protocol log...')
}
const formatDuration = (ms) => {
  const seconds = Math.floor(ms / 1000) % 60
  const minutes = Math.floor(ms / (1000 * 60)) % 60
  const hours = Math.floor(ms / (1000 * 60 * 60))
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
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
// Setup WebSocket connection for real-time MPC updates
const setupMPCWebSocket = (sessionId) => {
  if (mpcWebSocket.value) {
    mpcWebSocket.value.close()
  }
  
  try {
    mpcWebSocket.value = p2paiService.training.createTrainingWebSocket(sessionId, {
      onOpen: () => {
        console.log('📡 MPC WebSocket connected')
      },
      onMessage: (data) => {
        console.log('📨 MPC update received:', data)
        updateMPCMetrics(data)
      },
      onError: (error) => {
        console.error('❌ MPC WebSocket error:', error)
      },
      onClose: () => {
        console.log('🔌 MPC WebSocket closed')
        if (isTraining.value) {
          // Try to reconnect after 3 seconds
          setTimeout(() => setupMPCWebSocket(sessionId), 3000)
        }
      }
    })
  } catch (err) {
    console.error('Failed to setup MPC WebSocket:', err)
  }
}

// Update MPC metrics from WebSocket data
const updateMPCMetrics = (data) => {
  if (data.type === 'mpc_round') {
    currentRound.value = data.round || currentRound.value
    currentAccuracy.value = data.accuracy || currentAccuracy.value
    currentLoss.value = data.loss || currentLoss.value
    convergenceRate.value = data.convergence_rate || convergenceRate.value
    communicationRounds.value = data.communication_rounds || communicationRounds.value
    dataTransferred.value = data.data_transferred || dataTransferred.value
    
    // Update system resources
    computationLoad.value = data.computation_load || computationLoad.value
    networkLoad.value = data.network_load || networkLoad.value
    memoryUsage.value = data.memory_usage || memoryUsage.value
    averageLatency.value = data.average_latency || averageLatency.value
    throughput.value = data.throughput || throughput.value
    
    // Update party status
    if (data.parties) {
      parties.value = data.parties.map(party => ({
        id: party.id,
        name: party.name,
        connected: party.connected || false
      }))
    }
  } else if (data.type === 'mpc_completed') {
    protocolStatus.value = 'Completed'
    isTraining.value = false
    isPaused.value = false
  } else if (data.type === 'mpc_error') {
    protocolStatus.value = 'Error'
    apiError.value = data.message || 'MPC training error occurred'
    isTraining.value = false
    isPaused.value = false
  }
}

// Load parties data
const loadPartiesData = async () => {
  try {
    const partiesResponse = await cachedApiCall(
      'mpc-parties',
      () => p2paiService.nodes.getNodes({ type: 'mpc' }),
      30 * 1000 // 30 second cache
    )
    
    if (partiesResponse.data?.nodes) {
      parties.value = partiesResponse.data.nodes.slice(0, totalParties.value).map(node => ({
        id: node.id,
        name: node.name || `Party-${node.id}`,
        connected: node.status === 'online' || node.status === 'training'
      }))
    }
  } catch (err) {
    console.warn('Failed to load parties data:', err)
  }
}

onMounted(async () => {
  console.log('🔒 MPC Training component mounted')
  
  currentAccuracy.value = 0
  currentLoss.value = 2.0
  convergenceRate.value = 1.0
  
  // Load initial parties data
  await loadPartiesData()
})
onUnmounted(() => {
  console.log('🧹 Cleaning up MPC Training component')
  
  // Close WebSocket connection
  if (mpcWebSocket.value) {
    mpcWebSocket.value.close()
    mpcWebSocket.value = null
  }
  
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
  background: #dc2626;
  cursor: pointer;
}
input[type="range"]::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #dc2626;
  cursor: pointer;
  border: none;
}
</style>