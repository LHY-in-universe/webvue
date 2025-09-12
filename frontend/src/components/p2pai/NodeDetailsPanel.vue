<template>
  <div
    v-if="isVisible"
    class="node-details-overlay"
    @click="handleOverlayClick"
  >
    <div
      class="node-details-panel"
      :class="{ 'show': isVisible }"
      @click.stop
    >
      <!-- 头部 -->
      <div class="panel-header">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div 
              class="w-12 h-12 rounded-xl flex items-center justify-center"
              :style="{ backgroundColor: node.color + '20', border: `2px solid ${node.strokeColor}` }"
            >
              <!-- 节点类型图标 -->
              <ServerIcon v-if="node.type === 'control'" class="w-6 h-6" :style="{ color: node.strokeColor }" />
              <CpuChipIcon v-else class="w-6 h-6" :style="{ color: node.strokeColor }" />
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ node.name }}
              </h3>
              <div class="flex items-center space-x-2 mt-1">
                <span class="text-sm text-gray-600 dark:text-gray-400">
                  {{ node.type === 'control' ? 'Control Node' : 'Edge Node' }}
                </span>
                <div 
                  :class="[
                    'w-2 h-2 rounded-full',
                    getStatusIndicatorColor(node.status)
                  ]"
                ></div>
                <span :class="getStatusTextColor(node.status)" class="text-sm font-medium">
                  {{ getStatusText(node.status) }}
                </span>
              </div>
            </div>
          </div>
          
          <Button
            @click="$emit('close')"
            variant="ghost"
            size="sm"
            class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
          >
            <XMarkIcon class="w-5 h-5" />
          </Button>
        </div>
      </div>
      
      <!-- 内容区域 -->
      <div class="panel-content">
        <!-- 基本信息 -->
        <div class="info-section">
          <h4 class="section-title">Basic Information</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">Node ID</span>
              <span class="info-value">{{ node.id }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">IP Address</span>
              <span class="info-value font-mono">{{ node.ip }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">User</span>
              <span class="info-value">{{ node.user || 'N/A' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Node Type</span>
              <span class="info-value">
                {{ node.type === 'control' ? 
                    (node.subType === 'master' ? 'Master Node' : 'Participant Node') : 
                    (node.isOwn ? 'Local Node' : 'Remote Node') 
                }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- 训练信息（仅边缘节点且正在训练时显示） -->
        <div v-if="node.type === 'edge' && node.status === 'training'" class="info-section">
          <h4 class="section-title">Training Status</h4>
          <div class="training-info">
            <div class="training-progress-item">
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Training Progress</span>
                <span class="text-sm font-semibold text-blue-600 dark:text-blue-400">
                  {{ Math.round(node.progress || 0) }}%
                </span>
              </div>
              <ProgressBar 
                :percentage="node.progress || 0"
                variant="primary"
                size="sm"
                :animated="true"
              />
            </div>
            
            <div class="training-metrics">
              <div class="metric-item">
                <span class="metric-label">Current Accuracy</span>
                <span class="metric-value text-green-600 dark:text-green-400">
                  {{ node.accuracy ? node.accuracy.toFixed(2) : 'N/A' }}%
                </span>
              </div>
              <div class="metric-item" v-if="node.loss">
                <span class="metric-label">Loss Value</span>
                <span class="metric-value text-orange-600 dark:text-orange-400">
                  {{ node.loss.toFixed(4) }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 资源使用情况 -->
        <div v-if="node.resources" class="info-section">
          <h4 class="section-title">Resource Usage</h4>
          <div class="resource-grid">
            <div class="resource-item">
              <div class="flex items-center justify-between mb-2">
                <span class="resource-label">
                  <CpuChipIcon class="w-4 h-4 mr-1" />
                  CPU
                </span>
                <span class="resource-value">{{ node.resources.cpu }}%</span>
              </div>
              <ProgressBar 
                :percentage="node.resources.cpu"
                :variant="getResourceVariant(node.resources.cpu)"
                size="sm"
              />
            </div>
            
            <div class="resource-item">
              <div class="flex items-center justify-between mb-2">
                <span class="resource-label">
                  <RectangleStackIcon class="w-4 h-4 mr-1" />
                  Memory
                </span>
                <span class="resource-value">{{ node.resources.memory }}%</span>
              </div>
              <ProgressBar 
                :percentage="node.resources.memory"
                :variant="getResourceVariant(node.resources.memory)"
                size="sm"
              />
            </div>
            
            <div class="resource-item">
              <div class="flex items-center justify-between mb-2">
                <span class="resource-label">
                  <CommandLineIcon class="w-4 h-4 mr-1" />
                  GPU
                </span>
                <span class="resource-value">{{ node.resources.gpu }}%</span>
              </div>
              <ProgressBar 
                :percentage="node.resources.gpu"
                :variant="getResourceVariant(node.resources.gpu)"
                size="sm"
              />
            </div>
          </div>
        </div>
        
        <!-- 连接状态 -->
        <div class="info-section">
          <h4 class="section-title">Connection Status</h4>
          <div class="connection-info">
            <div class="connection-item">
              <span class="connection-label">Network Latency</span>
              <span class="connection-value">
                {{ generateRandomLatency() }}ms
              </span>
            </div>
            <div class="connection-item">
              <span class="connection-label">Connection Quality</span>
              <span class="connection-value">
                <span :class="getConnectionQualityColor()">
                  {{ getConnectionQuality() }}
                </span>
              </span>
            </div>
            <div class="connection-item">
              <span class="connection-label">Uptime</span>
              <span class="connection-value">
                {{ formatUptime() }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- 操作按钮（仅本人节点） -->
        <div v-if="node.isOwn" class="info-section">
          <h4 class="section-title">Actions</h4>
          <div class="action-buttons">
            <Button
              v-if="node.status === 'training'"
              @click="pauseTraining"
              variant="warning"
              size="sm"
              class="action-button"
            >
              <PauseIcon class="w-4 h-4 mr-2" />
              Pause Training
            </Button>
            
            <Button
              v-if="node.status !== 'training'"
              @click="resumeTraining"
              variant="primary"
              size="sm"
              class="action-button"
            >
              <PlayIcon class="w-4 h-4 mr-2" />
              Resume Training
            </Button>
            
            <Button
              @click="viewLogs"
              variant="outline"
              size="sm"
              class="action-button"
            >
              <DocumentTextIcon class="w-4 h-4 mr-2" />
              View Logs
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  XMarkIcon,
  ServerIcon,
  CpuChipIcon,
  RectangleStackIcon,
  CommandLineIcon,
  PauseIcon,
  PlayIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'

import Button from '@/components/ui/Button.vue'
import ProgressBar from '@/components/ui/ProgressBar.vue'

const props = defineProps({
  node: {
    type: Object,
    required: true
  },
  isVisible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

// 计算属性
const getStatusIndicatorColor = (status) => {
  const colors = {
    active: 'bg-green-500',
    training: 'bg-blue-500 animate-pulse',
    offline: 'bg-gray-400',
    completed: 'bg-green-600',
    error: 'bg-red-500'
  }
  return colors[status] || 'bg-gray-400'
}

const getStatusTextColor = (status) => {
  const colors = {
    active: 'text-green-600 dark:text-green-400',
    training: 'text-blue-600 dark:text-blue-400',
    offline: 'text-gray-500 dark:text-gray-400',
    completed: 'text-green-600 dark:text-green-400',
    error: 'text-red-600 dark:text-red-400'
  }
  return colors[status] || 'text-gray-500'
}

const getStatusText = (status) => {
  const texts = {
    active: 'Active',
    training: 'Training',
    offline: 'Offline',
    completed: 'Completed',
    error: 'Error'
  }
  return texts[status] || 'Unknown'
}

const getResourceVariant = (percentage) => {
  if (percentage >= 90) return 'danger'
  if (percentage >= 70) return 'warning'
  if (percentage >= 40) return 'primary'
  return 'success'
}

const getConnectionQuality = () => {
  const qualities = ['Excellent', 'Good', 'Average']
  return qualities[Math.floor(Math.random() * qualities.length)]
}

const getConnectionQualityColor = () => {
  const colors = ['text-green-600 dark:text-green-400', 'text-blue-600 dark:text-blue-400', 'text-orange-600 dark:text-orange-400']
  return colors[Math.floor(Math.random() * colors.length)]
}

// 方法
const generateRandomLatency = () => {
  return Math.floor(Math.random() * 100) + 10
}

const formatUptime = () => {
  const hours = Math.floor(Math.random() * 24) + 1
  const minutes = Math.floor(Math.random() * 60)
  return `${hours}h ${minutes}m`
}

const handleOverlayClick = () => {
  emit('close')
}

const pauseTraining = () => {
  console.log('Pausing training for node:', props.node.id)
  // Pause training logic
}

const resumeTraining = () => {
  console.log('Resuming training for node:', props.node.id)
  // Resume training logic
}

const viewLogs = () => {
  console.log('Viewing logs for node:', props.node.id)
  // View logs logic
}
</script>

<style scoped>
.node-details-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  backdrop-filter: blur(4px);
  min-height: 100vh;
  min-width: 100vw;
}

.node-details-panel {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(229, 231, 235, 0.3);
  border-radius: 20px;
  width: 100%;
  max-width: 500px;
  max-height: 85vh;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
  transform: scale(0.95) translateY(30px);
  opacity: 0;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.node-details-panel.show {
  transform: scale(1) translateY(0);
  opacity: 1;
}

:root.dark .node-details-panel {
  background: rgba(15, 23, 42, 0.98) !important;
  border-color: rgba(148, 163, 184, 0.2) !important;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4) !important;
}

.panel-header {
  padding: 28px;
  border-bottom: 1px solid rgba(229, 231, 235, 0.3);
  background: rgba(248, 250, 252, 0.5);
}

:root.dark .panel-header {
  border-bottom-color: rgba(148, 163, 184, 0.2) !important;
  background: rgba(30, 41, 59, 0.5) !important;
}

.panel-content {
  padding: 0 28px 28px;
  max-height: calc(85vh - 140px);
  overflow-y: auto;
}

.info-section {
  margin-bottom: 28px;
}

.section-title {
  font-size: 13px;
  font-weight: 700;
  color: rgb(100, 116, 139);
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding-left: 2px;
}

:root.dark .section-title {
  color: rgb(148, 163, 184) !important;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.info-item {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(226, 232, 240, 0.4);
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
}

.info-item:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(99, 102, 241, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

:root.dark .info-item {
  background: rgba(30, 41, 59, 0.7) !important;
  border-color: rgba(100, 116, 139, 0.3) !important;
}

:root.dark .info-item:hover {
  background: rgba(30, 41, 59, 0.9) !important;
  border-color: rgba(99, 102, 241, 0.4) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

.info-label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: rgb(107, 114, 128);
  margin-bottom: 4px;
}

:root.dark .info-label {
  color: rgb(156, 163, 175) !important;
}

.info-value {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: rgb(17, 24, 39);
}

:root.dark .info-value {
  color: rgb(243, 244, 246) !important;
}

.training-info {
  space-y: 16px;
}

.training-progress-item {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(99, 102, 241, 0.2);
  margin-bottom: 20px;
  backdrop-filter: blur(8px);
}

:root.dark .training-progress-item {
  background: rgba(30, 41, 59, 0.8) !important;
  border-color: rgba(99, 102, 241, 0.3) !important;
}

.training-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.metric-item {
  text-align: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  border: 1px solid rgba(226, 232, 240, 0.4);
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
}

.metric-item:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(16, 185, 129, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

:root.dark .metric-item {
  background: rgba(30, 41, 59, 0.7) !important;
  border-color: rgba(100, 116, 139, 0.3) !important;
}

:root.dark .metric-item:hover {
  background: rgba(30, 41, 59, 0.9) !important;
  border-color: rgba(16, 185, 129, 0.4) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

.metric-label {
  display: block;
  font-size: 12px;
  color: rgb(107, 114, 128);
  margin-bottom: 4px;
}

:root.dark .metric-label {
  color: rgb(156, 163, 175) !important;
}

.metric-value {
  display: block;
  font-size: 16px;
  font-weight: 700;
}

.resource-grid {
  space-y: 12px;
}

.resource-item {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(226, 232, 240, 0.4);
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
  margin-bottom: 12px;
}

.resource-item:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

:root.dark .resource-item {
  background: rgba(30, 41, 59, 0.7) !important;
  border-color: rgba(100, 116, 139, 0.3) !important;
}

:root.dark .resource-item:hover {
  background: rgba(30, 41, 59, 0.9) !important;
  border-color: rgba(139, 92, 246, 0.4) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

.resource-label {
  display: flex;
  align-items: center;
  font-size: 13px;
  font-weight: 500;
  color: rgb(75, 85, 99);
}

:root.dark .resource-label {
  color: rgb(156, 163, 175) !important;
}

.resource-value {
  font-size: 13px;
  font-weight: 600;
  color: rgb(17, 24, 39);
}

:root.dark .resource-value {
  color: rgb(243, 244, 246) !important;
}

.connection-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.connection-item {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  padding: 16px;
  border: 1px solid rgba(226, 232, 240, 0.4);
  text-align: center;
  backdrop-filter: blur(8px);
  transition: all 0.2s ease;
}

.connection-item:hover {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

:root.dark .connection-item {
  background: rgba(30, 41, 59, 0.7) !important;
  border-color: rgba(100, 116, 139, 0.3) !important;
}

:root.dark .connection-item:hover {
  background: rgba(30, 41, 59, 0.9) !important;
  border-color: rgba(59, 130, 246, 0.4) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

.connection-label {
  display: block;
  font-size: 12px;
  color: rgb(107, 114, 128);
  margin-bottom: 4px;
}

:root.dark .connection-label {
  color: rgb(156, 163, 175) !important;
}

.connection-value {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: rgb(17, 24, 39);
}

:root.dark .connection-value {
  color: rgb(243, 244, 246) !important;
}

.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.action-button {
  justify-self: stretch;
}

/* 滚动条样式 */
.panel-content::-webkit-scrollbar {
  width: 4px;
}

.panel-content::-webkit-scrollbar-track {
  background: rgba(248, 250, 252, 0.5);
  border-radius: 2px;
}

:root.dark .panel-content::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.5) !important;
}

.panel-content::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.4);
  border-radius: 2px;
  transition: background 0.2s ease;
}

:root.dark .panel-content::-webkit-scrollbar-thumb {
  background: rgba(100, 116, 139, 0.6) !important;
}

.panel-content::-webkit-scrollbar-thumb:hover {
  background: rgba(99, 102, 241, 0.6);
}

:root.dark .panel-content::-webkit-scrollbar-thumb:hover {
  background: rgba(99, 102, 241, 0.7) !important;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .node-details-panel {
    margin: 10px;
    max-width: none;
  }
  
  .info-grid,
  .training-metrics,
  .connection-info {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
  }
}
</style>