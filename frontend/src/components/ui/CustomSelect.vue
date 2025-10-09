<template>
  <div class="relative" ref="selectContainer">
    <!-- 触发按钮 -->
    <button
      @click="toggleDropdown"
      @keydown.enter.prevent="toggleDropdown"
      @keydown.space.prevent="toggleDropdown"
      @keydown.escape="closeDropdown"
      @keydown.arrow-down.prevent="openDropdown"
      @keydown.arrow-up.prevent="openDropdown"
      :class="[
        'flex items-center justify-between w-full px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200',
        isOpen ? 'ring-2 ring-blue-500 border-blue-500' : ''
      ]"
      :aria-expanded="isOpen"
      :aria-haspopup="true"
      role="combobox"
    >
      <span class="flex items-center">
        <span v-if="selectedOption?.icon" class="mr-2">
          <component :is="selectedOption.icon" class="w-4 h-4" />
        </span>
        {{ selectedOption?.label || placeholder }}
      </span>
      
      <!-- 下拉箭头 -->
      <svg 
        :class="[
          'w-4 h-4 transition-transform duration-200',
          isOpen ? 'rotate-180' : ''
        ]" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- 下拉菜单 -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div
        v-if="isOpen"
        class="absolute z-50 w-full bottom-full mb-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg max-h-60 overflow-auto"
        role="listbox"
      >
        <div class="py-1">
          <button
            v-for="(option, index) in options"
            :key="option.value"
            @click="selectOption(option)"
            @keydown.enter.prevent="selectOption(option)"
            @keydown.space.prevent="selectOption(option)"
            @keydown.arrow-down.prevent="focusNext(index)"
            @keydown.arrow-up.prevent="focusPrevious(index)"
            :class="[
              'flex items-center w-full px-4 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-150',
              selectedOption?.value === option.value ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' : 'text-gray-700 dark:text-gray-300'
            ]"
            :ref="el => optionRefs[index] = el"
            role="option"
            :aria-selected="selectedOption?.value === option.value"
          >
            <span v-if="option.icon" class="mr-3">
              <component :is="option.icon" class="w-4 h-4" />
            </span>
            <span class="flex-1">{{ option.label }}</span>
            <span v-if="selectedOption?.value === option.value" class="ml-2">
              <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
            </span>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  options: {
    type: Array,
    required: true,
    validator: (options) => {
      return options.every(option => 
        typeof option === 'object' && 
        'value' in option && 
        'label' in option
      )
    }
  },
  placeholder: {
    type: String,
    default: '请选择...'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const selectContainer = ref(null)
const isOpen = ref(false)
const optionRefs = ref([])

// 计算当前选中的选项
const selectedOption = computed(() => {
  return props.options.find(option => option.value === props.modelValue) || null
})

// 切换下拉菜单
const toggleDropdown = () => {
  if (props.disabled) return
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    nextTick(() => {
      focusSelectedOption()
    })
  }
}

// 打开下拉菜单
const openDropdown = () => {
  if (props.disabled) return
  isOpen.value = true
  nextTick(() => {
    focusSelectedOption()
  })
}

// 关闭下拉菜单
const closeDropdown = () => {
  isOpen.value = false
}

// 选择选项
const selectOption = (option) => {
  emit('update:modelValue', option.value)
  emit('change', option)
  closeDropdown()
}

// 聚焦到下一个选项
const focusNext = (currentIndex) => {
  const nextIndex = (currentIndex + 1) % props.options.length
  focusOption(nextIndex)
}

// 聚焦到上一个选项
const focusPrevious = (currentIndex) => {
  const prevIndex = currentIndex === 0 ? props.options.length - 1 : currentIndex - 1
  focusOption(prevIndex)
}

// 聚焦到指定选项
const focusOption = (index) => {
  if (optionRefs.value[index]) {
    optionRefs.value[index].focus()
  }
}

// 聚焦到当前选中的选项
const focusSelectedOption = () => {
  const selectedIndex = props.options.findIndex(option => option.value === props.modelValue)
  if (selectedIndex >= 0) {
    focusOption(selectedIndex)
  } else {
    focusOption(0)
  }
}

// 点击外部关闭下拉菜单
const handleClickOutside = (event) => {
  if (selectContainer.value && !selectContainer.value.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
