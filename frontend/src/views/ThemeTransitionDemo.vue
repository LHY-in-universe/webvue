<template>
  <div class="theme-demo-page">
    <!-- 页面标题 -->
    <div class="demo-header">
      <div class="container mx-auto px-4 py-16">
        <Transition name="title" appear>
          <h1 class="text-4xl font-bold text-center mb-4">
            现代主题切换
          </h1>
        </Transition>
        
        <Transition name="subtitle" appear>
          <p class="text-xl text-center text-gray-600 dark:text-gray-400 mb-8">
            简洁、现代、流畅的主题切换体验
          </p>
        </Transition>
      </div>
    </div>

    <!-- 主要演示区域 -->
    <div class="demo-section">
      <div class="container mx-auto px-4 py-16">
        <div class="max-w-6xl mx-auto">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            
            <!-- 小尺寸开关卡片 -->
            <Card variant="elevated" :hoverable="true">
              <template #header>
                <h3 class="text-lg font-semibold">小尺寸开关</h3>
              </template>
              
              <div class="text-center py-8">
                <p class="text-gray-600 dark:text-gray-400 mb-6">适合导航栏和紧凑空间</p>
                <SimpleThemeToggle size="sm" />
              </div>
              
              <template #footer>
                <div class="flex flex-wrap gap-2">
                  <span class="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full">
                    紧凑设计
                  </span>
                  <span class="px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-xs rounded-full">
                    导航栏适用
                  </span>
                </div>
              </template>
            </Card>

            <!-- 标准开关卡片 -->
            <Card variant="elevated" :hoverable="true">
              <template #header>
                <h3 class="text-lg font-semibold">标准开关</h3>
              </template>
              
              <div class="text-center py-8">
                <p class="text-gray-600 dark:text-gray-400 mb-6">默认尺寸，适合大部分场景</p>
                <SimpleThemeToggle size="md" :show-label="true" />
              </div>
              
              <template #footer>
                <div class="flex flex-wrap gap-2">
                  <span class="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-full">
                    标准尺寸
                  </span>
                  <span class="px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 text-xs rounded-full">
                    带标签
                  </span>
                </div>
              </template>
            </Card>

            <!-- 大尺寸开关卡片 -->
            <Card variant="elevated" :hoverable="true">
              <template #header>
                <h3 class="text-lg font-semibold">大尺寸开关</h3>
              </template>
              
              <div class="text-center py-8">
                <p class="text-gray-600 dark:text-gray-400 mb-6">适合重点展示区域</p>
                <SimpleThemeToggle size="lg" :show-label="true" />
              </div>
              
              <template #footer>
                <div class="flex flex-wrap gap-2">
                  <span class="px-2 py-1 bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200 text-xs rounded-full">
                    大尺寸
                  </span>
                  <span class="px-2 py-1 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 text-xs rounded-full">
                    重点展示
                  </span>
                </div>
              </template>
            </Card>

          </div>
        </div>
      </div>
    </div>

    <!-- 高级动画效果试验区 -->
    <div class="demo-section bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20">
      <div class="container mx-auto px-4 py-16">
        <h2 class="text-3xl font-semibold text-center mb-4">
          🎨 高级动画效果试验区
        </h2>
        <p class="text-center text-gray-600 dark:text-gray-400 mb-12">
          体验各种炫酷的主题切换动画效果
        </p>

        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          <!-- 涟漪效果 -->
          <Card variant="elevated" :hoverable="true">
            <template #header>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                  🌊
                </div>
                <h3 class="text-xl font-semibold">涟漪扩散效果</h3>
              </div>
            </template>
            
            <div class="space-y-4">
              <p class="text-gray-600 dark:text-gray-400">从点击位置向外扩散的圆形涟漪动画</p>
              <div class="text-center py-8">
                <button 
                  @click="triggerRippleTransition"
                  ref="rippleButton"
                  class="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-700"
                >
                  🌊 涟漪切换主题
                </button>
              </div>
            </div>
            
            <template #footer>
              <div class="text-sm text-gray-500 dark:text-gray-400">
                点击按钮体验从点击位置扩散的涟漪动画
              </div>
            </template>
          </Card>

          <!-- 粒子效果 -->
          <Card variant="elevated" :hoverable="true">
            <template #header>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-yellow-100 dark:bg-yellow-900 rounded-lg flex items-center justify-center">
                  ✨
                </div>
                <h3 class="text-xl font-semibold">粒子爆炸效果</h3>
              </div>
            </template>
            
            <div class="space-y-4">
              <p class="text-gray-600 dark:text-gray-400">随机粒子的旋转缩放爆炸动画</p>
              <div class="text-center py-8">
                <button 
                  @click="triggerParticleTransition"
                  class="px-8 py-4 bg-gradient-to-r from-yellow-500 to-orange-600 hover:from-yellow-600 hover:to-orange-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-700"
                >
                  ✨ 粒子切换主题
                </button>
              </div>
            </div>
            
            <template #footer>
              <div class="text-sm text-gray-500 dark:text-gray-400">
                20个随机发光粒子的华丽动画效果
              </div>
            </template>
          </Card>

          <!-- 颜色波浪效果 -->
          <Card variant="elevated" :hoverable="true">
            <template #header>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                  🌈
                </div>
                <h3 class="text-xl font-semibold">颜色波浪效果</h3>
              </div>
            </template>
            
            <div class="space-y-4">
              <p class="text-gray-600 dark:text-gray-400">平滑的颜色波纹从左到右扫过屏幕</p>
              <div class="text-center py-8 space-y-4">
                <button 
                  @click="triggerColorWave('horizontal')"
                  class="block w-full px-8 py-3 bg-gradient-to-r from-green-500 to-teal-600 hover:from-green-600 hover:to-teal-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-700"
                >
                  🌈 横向波浪
                </button>
                <button 
                  @click="triggerColorWave('vertical')"
                  class="block w-full px-8 py-3 bg-gradient-to-r from-teal-500 to-cyan-600 hover:from-teal-600 hover:to-cyan-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-700"
                >
                  🌈 纵向波浪
                </button>
              </div>
            </div>
            
            <template #footer>
              <div class="text-sm text-gray-500 dark:text-gray-400">
                选择横向或纵向的颜色波浪动画
              </div>
            </template>
          </Card>

          <!-- View Transition API 效果 -->
          <Card variant="elevated" :hoverable="true">
            <template #header>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-indigo-100 dark:bg-indigo-900 rounded-lg flex items-center justify-center">
                  🌟
                </div>
                <h3 class="text-xl font-semibold">View Transition API</h3>
              </div>
            </template>
            
            <div class="space-y-4">
              <p class="text-gray-600 dark:text-gray-400">现代浏览器原生支持的圆形扩散切换</p>
              <div class="text-center py-8">
                <SimpleThemeToggle 
                  :show-label="true" 
                  size="md"
                />
              </div>
              <div class="text-xs text-gray-500 dark:text-gray-400 text-center">
                <span class="inline-flex items-center gap-1">
                  <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                  支持 Chrome 111+, Firefox 118+
                </span>
              </div>
            </div>
            
            <template #footer>
              <div class="text-sm text-gray-500 dark:text-gray-400">
                点击位置响应的原生浏览器动画，自动降级兼容
              </div>
            </template>
          </Card>

          <!-- 组合动画效果 -->
          <Card variant="elevated" :hoverable="true">
            <template #header>
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
                  🎆
                </div>
                <h3 class="text-xl font-semibold">终极组合效果</h3>
              </div>
            </template>
            
            <div class="space-y-4">
              <p class="text-gray-600 dark:text-gray-400">所有动画效果的完美组合</p>
              <div class="text-center py-8">
                <button 
                  @click="triggerUltimateTransition"
                  ref="ultimateButton"
                  class="px-8 py-4 bg-gradient-to-r from-purple-500 via-pink-500 to-red-500 hover:from-purple-600 hover:via-pink-600 hover:to-red-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-700 animate-pulse"
                >
                  🎆 终极动画切换
                </button>
              </div>
            </div>
            
            <template #footer>
              <div class="text-sm text-gray-500 dark:text-gray-400">
                涟漪 + 粒子 + 波浪的华丽组合效果
              </div>
            </template>
          </Card>

        </div>
      </div>
    </div>

    <!-- 使用场景演示 -->
    <div class="demo-section bg-gray-50 dark:bg-gray-900">
      <div class="container mx-auto px-4 py-16">
        <h2 class="text-3xl font-semibold text-center mb-12">
          使用场景演示
        </h2>

        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          <!-- 导航栏场景 -->
          <Card variant="elevated" :hoverable="true">
            <template #header>
              <h3 class="text-xl font-semibold">导航栏应用</h3>
            </template>
            
            <div class="space-y-4">
              <p class="text-gray-600 dark:text-gray-400">在导航栏中使用小尺寸开关</p>
              <div class="mock-navbar">
                <div class="navbar-brand">
                  <h4 class="text-lg font-bold">我的应用</h4>
                </div>
                <div class="navbar-controls">
                  <span class="text-sm text-gray-600 dark:text-gray-400 mr-4">切换主题</span>
                  <SimpleThemeToggle size="sm" />
                </div>
              </div>
            </div>
            
            <template #footer>
              <div class="text-sm text-gray-500 dark:text-gray-400">
                适合：顶部导航栏、工具栏、紧凑空间
              </div>
            </template>
          </Card>

          <!-- 设置页面场景 -->
          <Card variant="elevated" :hoverable="true">
            <template #header>
              <h3 class="text-xl font-semibold">设置页面应用</h3>
            </template>
            
            <div class="space-y-4">
              <p class="text-gray-600 dark:text-gray-400">在设置页面中使用带标签的标准开关</p>
              <div class="mock-settings">
                <div class="setting-item">
                  <div class="setting-info">
                    <h4 class="font-medium text-gray-900 dark:text-white">外观模式</h4>
                    <p class="text-sm text-gray-600 dark:text-gray-400">选择浅色或深色主题</p>
                  </div>
                  <SimpleThemeToggle size="md" :show-label="true" />
                </div>
              </div>
            </div>
            
            <template #footer>
              <div class="text-sm text-gray-500 dark:text-gray-400">
                适合：设置页面、偏好设置、配置选项
              </div>
            </template>
          </Card>

          <!-- 重点展示场景 -->
          <div class="lg:col-span-2">
            <Card variant="elevated" :hoverable="true">
              <template #header>
                <h3 class="text-xl font-semibold">重点展示区域</h3>
              </template>
              
              <div class="mock-highlight">
                <div class="text-center py-8">
                  <h4 class="text-2xl font-bold mb-4">个性化体验</h4>
                  <p class="text-gray-600 dark:text-gray-400 mb-8">根据您的偏好选择主题模式</p>
                  <SimpleThemeToggle size="lg" :show-label="true" />
                </div>
              </div>
              
              <template #footer>
                <div class="text-sm text-gray-500 dark:text-gray-400">
                  适合：首页横幅、功能介绍、重要设置项目
                </div>
              </template>
            </Card>
          </div>
          
        </div>
      </div>
    </div>

    <!-- 特性说明 -->
    <div class="demo-section">
      <div class="container mx-auto px-4 py-16">
        <h2 class="text-3xl font-semibold text-center mb-12">
          主要特性
        </h2>
        
        <div class="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">简洁设计</h3>
            <p class="feature-description">现代化的滑动开关设计，简洁优雅</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">流畅动画</h3>
            <p class="feature-description">60fps 流畅动画，GPU 加速优化</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <h3 class="feature-title">全局过渡</h3>
            <p class="feature-description">整个页面的颜色同步平滑切换</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🌟</div>
            <h3 class="feature-title">View Transition API</h3>
            <p class="feature-description">原生浏览器支持的圆形扩散动画</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3 class="feature-title">多尺寸支持</h3>
            <p class="feature-description">小、中、大三种尺寸，适配不同场景</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">♿</div>
            <h3 class="feature-title">无障碍友好</h3>
            <p class="feature-description">支持键盘操作和屏幕阅读器</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <h3 class="feature-title">减少动效</h3>
            <p class="feature-description">自动适配用户的系统偏好设置</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <h3 class="feature-title">兼容降级</h3>
            <p class="feature-description">优雅降级，确保所有浏览器可用</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🎪</div>
            <h3 class="feature-title">华丽组合</h3>
            <p class="feature-description">多种动画效果的完美组合展示</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useThemeStore } from '@/stores/theme'
import { useThemeTransition } from '@/composables/useThemeTransition'
import SimpleThemeToggle from '@/components/ui/SimpleThemeToggle.vue'
import Card from '@/components/ui/Card.vue'

const themeStore = useThemeStore()

// 引用按钮元素
const rippleButton = ref(null)
const ultimateButton = ref(null)

// 使用高级主题过渡功能 - 延长动画时间
const {
  transitionTheme,
  createRipple,
  createParticles,
  createColorWave,
  isTransitioning
} = useThemeTransition({
  duration: 1200,  // 增加到 1200ms 为更流畅的动画
  enableRipple: true,
  enableParticles: true,
  enableColorInterpolation: true
})

// 涟漪效果切换
const triggerRippleTransition = async () => {
  if (isTransitioning.value) return
  
  console.log('🌊 触发涟漪效果')
  
  // 使用涟漪动画切换主题
  if (rippleButton.value) {
    await createRipple(rippleButton.value)
  }
  
  // 同时切换主题
  themeStore.toggleTheme()
}

// 粒子效果切换
const triggerParticleTransition = async () => {
  if (isTransitioning.value) return
  
  console.log('✨ 触发粒子效果')
  
  // 创建粒子动画
  await createParticles()
  
  // 同时切换主题
  themeStore.toggleTheme()
}

// 颜色波浪效果
const triggerColorWave = async (direction = 'horizontal') => {
  if (isTransitioning.value) return
  
  console.log(`🌈 触发${direction}波浪效果`)
  
  // 创建颜色波浪
  createColorWave(direction)
  
  // 延迟更长时间切换主题，让波浪效果更明显
  setTimeout(() => {
    themeStore.toggleTheme()
  }, 500)
}

// 终极组合效果
const triggerUltimateTransition = async () => {
  if (isTransitioning.value) return
  
  console.log('🎆 触发终极组合效果')
  
  try {
    // 同时触发所有效果
    const effects = []
    
    // 涟漪效果
    if (ultimateButton.value) {
      effects.push(createRipple(ultimateButton.value))
    }
    
    // 粒子效果（延迟更长）
    setTimeout(() => {
      createParticles()
    }, 800)
    
    // 颜色波浪（延迟最长）
    setTimeout(() => {
      createColorWave('horizontal')
    }, 1600)
    
    // 切换主题
    themeStore.toggleTheme()
    
    // 等待所有效果完成
    await Promise.all(effects)
    
    console.log('🎆 终极效果完成')
    
  } catch (error) {
    console.error('终极效果执行出错:', error)
  }
}

// 页面级过渡动画测试
const triggerPageTransition = () => {
  // 添加页面级动画类
  document.documentElement.classList.add('theme-page-transition')
  
  // 批量处理所有卡片动画
  const cards = document.querySelectorAll('.card-elevated')
  cards.forEach((card, index) => {
    setTimeout(() => {
      card.style.transform = 'scale(0.98)'
      card.style.opacity = '0.7'
      
      setTimeout(() => {
        card.style.transform = 'scale(1)'
        card.style.opacity = '1'
      }, 100)
    }, index * 50)
  })
  
  setTimeout(() => {
    document.documentElement.classList.remove('theme-page-transition')
  }, 2500)
}

onMounted(() => {
  console.log('🎨 主题动画演示页加载完成')
  
  // 监听主题变化
  themeStore.$subscribe((mutation, state) => {
    console.log('🔄 主题已切换到:', state.currentTheme)
  })
})
</script>

<style scoped>
/* 页面基础样式 */
.theme-demo-page {
  @apply min-h-screen bg-white dark:bg-gray-950;
  transition: background-color 300ms ease;
}

.demo-header {
  @apply bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800;
}

.demo-section {
  @apply transition-colors duration-300;
}

.container {
  @apply max-w-7xl;
}

/* 演示项目样式 */
.demo-item {
  @apply p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-lg;
  @apply border border-gray-200 dark:border-gray-700;
  @apply transition-all duration-300 hover:shadow-xl;
}

.demo-content {
  @apply text-center;
}

/* 使用场景样式 */
.demo-case {
  @apply bg-white dark:bg-gray-800 rounded-2xl p-8;
  @apply border border-gray-200 dark:border-gray-700;
  @apply shadow-lg transition-all duration-300;
}

.mock-navbar {
  @apply flex items-center justify-between p-4 rounded-lg;
  @apply bg-gray-100 dark:bg-gray-700;
  @apply border border-gray-300 dark:border-gray-600;
}

.navbar-brand {
  @apply text-gray-900 dark:text-white;
}

.navbar-controls {
  @apply flex items-center;
}

.mock-settings {
  @apply space-y-4;
}

.setting-item {
  @apply flex items-center justify-between p-6 rounded-lg;
  @apply bg-gray-50 dark:bg-gray-700;
  @apply border border-gray-200 dark:border-gray-600;
}

.setting-info {
  @apply flex-1;
}

.mock-highlight {
  @apply p-12 rounded-xl;
  @apply bg-gradient-to-br from-blue-50 to-indigo-50;
  @apply dark:from-gray-800 dark:to-gray-700;
  @apply border border-gray-200 dark:border-gray-600;
}

/* 特性卡片样式 */
.feature-card {
  @apply text-center p-6 rounded-xl;
  @apply bg-white dark:bg-gray-800;
  @apply border border-gray-200 dark:border-gray-700;
  @apply shadow-md hover:shadow-lg transition-all duration-300;
}

.feature-icon {
  @apply text-4xl mb-4;
}

.feature-title {
  @apply text-lg font-semibold mb-2;
  @apply text-gray-900 dark:text-white;
}

.feature-description {
  @apply text-gray-600 dark:text-gray-400 text-sm;
}

/* Vue 过渡动画 */
.title-enter-active,
.subtitle-enter-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.title-enter-from {
  opacity: 0;
  transform: translateY(-30px) scale(0.95);
}

.subtitle-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .demo-item {
    @apply p-6;
  }
  
  .demo-case {
    @apply p-6;
  }
  
  .mock-navbar {
    @apply flex-col space-y-4;
  }
  
  .navbar-controls {
    @apply w-full justify-center;
  }
  
  .setting-item {
    @apply flex-col space-y-4 text-center;
  }
  
  .mock-highlight {
    @apply p-8;
  }
  
  .feature-card {
    @apply p-4;
  }
}

/* 高级动画效果样式 - 延长动画时间 */
.theme-page-transition {
  transition: all 2000ms cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.theme-page-transition * {
  transition: all 2000ms cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 动画按钮增强 */
button:active {
  transform: scale(0.98) !important;
}

/* 卡片动画 - 延长动画时间 */
.card-elevated {
  transition: all 800ms cubic-bezier(0.4, 0, 0.2, 1);
}

.card-elevated:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 渐变背景动画 - 延长动画时间 */
.demo-section {
  background-attachment: fixed;
  transition: background 1500ms ease;
}

/* 按钮脉冲动画增强 */
@keyframes enhanced-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

.animate-pulse {
  animation: enhanced-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* 页面进入动画 */
@keyframes pageEnter {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.theme-demo-page {
  animation: pageEnter 800ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* 按钮悬停光晕效果 */
button {
  position: relative;
  overflow: hidden;
}

button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 1200ms;
}

button:hover::before {
  left: 100%;
}

/* 打印样式 */
@media print {
  .demo-header {
    @apply bg-white text-black;
  }
  
  .demo-item,
  .demo-case,
  .feature-card {
    @apply bg-white border border-gray-300 shadow-none;
  }
  
  button {
    display: none;
  }
}
</style>