import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useDark, useToggle } from '@vueuse/core'

export const useThemeStore = defineStore('theme', () => {
  // 使用 @vueuse/core 的标准实现
  const isDark = useDark({
    selector: 'html',
    attribute: 'data-bs-theme',
    valueDark: 'dark',
    valueLight: 'light'
  })
  
  const autoTheme = ref(false)
  const systemPrefersDark = ref(false)

  // Getters - 保持兼容性
  const getTheme = computed(() => {
    return isDark.value ? 'dark' : 'light'
  })

  const currentTheme = computed(() => {
    return isDark.value ? 'dark' : 'light'
  })

  // 动画状态
  const isTransitioning = ref(false)

  // Actions - 统一主题切换方法 - 使用View Transition API
  const toggleTheme = async (event) => {
    if (isTransitioning.value) return
    
    isTransitioning.value = true
    
    try {
      // 获取点击位置 (支持事件对象或元素)
      let x = window.innerWidth / 2
      let y = window.innerHeight / 2
      
      if (event) {
        // 如果是事件对象
        if (event.clientX !== undefined && event.clientY !== undefined) {
          x = event.clientX
          y = event.clientY
        }
        // 如果是DOM元素，获取其中心位置
        else if (event.getBoundingClientRect) {
          const rect = event.getBoundingClientRect()
          x = rect.left + rect.width / 2
          y = rect.top + rect.height / 2
        }
        // 如果是包含target的事件
        else if (event.target && event.target.getBoundingClientRect) {
          const rect = event.target.getBoundingClientRect()
          x = rect.left + rect.width / 2
          y = rect.top + rect.height / 2
        }
      }
      
      // 计算扩散半径 - 到屏幕角落的最大距离
      const endRadius = Math.hypot(
        Math.max(x, window.innerWidth - x),
        Math.max(y, window.innerHeight - y)
      )
      
      console.log(`🌟 统一主题切换: 位置(${x}, ${y}), 半径${Math.round(endRadius)}px`)
      
      // 兼容性处理 - 检查 View Transition API 支持
      if (!document.startViewTransition) {
        console.log('📱 View Transition API 不支持，使用即时切换')
        isDark.value = !isDark.value
        return
      }
      
      // 创建 View Transition - 统一实现
      const transition = document.startViewTransition(async () => {
        isDark.value = !isDark.value
      })
      
      // 等待过渡准备就绪并执行圆形展开动画
      transition.ready.then(() => {
        // 创建圆形剪裁路径 - 从点击位置展开
        const clipPath = [
          `circle(0px at ${x}px ${y}px)`,
          `circle(${endRadius}px at ${x}px ${y}px)`
        ]
        
        // 应用动画到正确的伪元素
        document.documentElement.animate(
          {
            clipPath: isDark.value ? clipPath.slice().reverse() : clipPath,
          },
          {
            duration: 800,
            easing: "ease-in-out",
            pseudoElement: isDark.value 
              ? "::view-transition-old(root)" 
              : "::view-transition-new(root)",
          }
        )
        
        console.log('🎨 圆形展开动画启动 - 主题:', isDark.value ? 'dark' : 'light')
      })
      
      // 等待动画完成
      await transition.finished
      console.log('✅ 统一主题切换完成')
      
    } catch (error) {
      console.error('❌ 主题切换失败:', error)
      // 降级处理：确保主题状态正确切换
      isDark.value = !isDark.value
    } finally {
      // 重置过渡状态
      setTimeout(() => {
        isTransitioning.value = false
      }, 50)
    }
  }

  const setTheme = (theme) => {
    isDark.value = theme === 'dark'
  }

  const setAutoTheme = (auto = true) => {
    // @vueuse/core 自动处理系统主题
    autoTheme.value = auto
  }

  const updateSystemPreference = () => {
    systemPrefersDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }

  const initializeTheme = () => {
    // @vueuse/core 自动处理初始化和本地存储
    updateSystemPreference()
    return () => {} // 空的清理函数
  }

  return {
    // State
    isDark,
    autoTheme,
    systemPrefersDark,
    isTransitioning,
    
    // Getters  
    getTheme,
    currentTheme,
    
    // Actions
    toggleTheme,
    setTheme,
    setAutoTheme,
    updateSystemPreference,
    initializeTheme
  }
})