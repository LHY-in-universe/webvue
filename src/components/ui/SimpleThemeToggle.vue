<template>
  <button
    @click="toggleTheme($event)"
    :disabled="themeStore.isTransitioning"
    class="simple-theme-toggle"
    :class="{ 'transitioning': themeStore.isTransitioning }"
    type="button"
    :aria-label="`切换到${themeStore.isDark ? '浅色' : '深色'}模式`"
    title="切换主题"
  >
    <Transition name="icon-flip" mode="out-in">
      <component 
        :is="themeStore.isDark ? MoonIcon : SunIcon" 
        :key="themeStore.isDark ? 'moon' : 'sun'"
        class="theme-icon"
      />
    </Transition>
  </button>
</template>

<script setup>
import { useThemeStore } from '@/stores/theme'
import { SunIcon, MoonIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: value => ['sm', 'md', 'lg'].includes(value)
  }
})

// 使用统一的主题管理
const themeStore = useThemeStore()

// 主题切换函数 - 使用统一的 themeStore
const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}
</script>

<style scoped>
/* 基础按钮样式 */
.simple-theme-toggle {
  @apply relative inline-flex items-center justify-center;
  @apply p-2 rounded-lg transition-all duration-500 ease-out;
  @apply text-gray-600 dark:text-gray-400;
  @apply hover:text-gray-900 dark:hover:text-gray-100;
  @apply hover:bg-gray-100 dark:hover:bg-gray-800;
  @apply focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
}

/* 尺寸变体 */
.simple-theme-toggle.size-sm .theme-icon {
  @apply w-4 h-4;
}

.simple-theme-toggle.size-md .theme-icon {
  @apply w-5 h-5;
}

.simple-theme-toggle.size-lg .theme-icon {
  @apply w-6 h-6;
}

/* 图标样式 */
.theme-icon {
  @apply w-5 h-5 transition-transform duration-500;
}

/* 过渡状态 */
.simple-theme-toggle.transitioning {
  @apply pointer-events-none;
}

/* 悬停效果 */
.simple-theme-toggle:hover .theme-icon {
  @apply scale-110;
}

/* 激活状态 */
.simple-theme-toggle:active .theme-icon {
  @apply scale-95;
}

/* 图标翻转动画 */
.icon-flip-enter-active,
.icon-flip-leave-active {
  transition: all 0.8s ease-out;
}

.icon-flip-enter-from {
  opacity: 0;
  transform: rotateY(90deg) scale(0.8);
}

.icon-flip-leave-to {
  opacity: 0;
  transform: rotateY(-90deg) scale(0.8);
}

/* 深色模式特殊样式 */
[data-bs-theme="dark"] .simple-theme-toggle {
  @apply text-yellow-400;
}

[data-bs-theme="light"] .simple-theme-toggle {
  @apply text-orange-500;
}

/* GPU 加速优化 */
.theme-icon {
  transform: translateZ(0);
  will-change: transform;
  backface-visibility: hidden;
}
</style>

