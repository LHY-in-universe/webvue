<template>
  <Modal
    :is-open="isOpen"
    :size="size"
    :persistent="persistent"
    hide-footer
    @close="handleClose"
    @update:is-open="$emit('update:isOpen', $event)"
  >
    <template #title>
      <div class="flex items-center">
        <component 
          :is="typeConfig.icon" 
          :class="typeConfig.iconClass"
          class="w-6 h-6 mr-3"
        />
        {{ title || typeConfig.defaultTitle }}
      </div>
    </template>

    <div class="p-6">
      <!-- Icon and Message -->
      <div class="flex items-start">
        <div :class="['flex-shrink-0 mx-auto flex items-center justify-center h-12 w-12 rounded-full', typeConfig.bgClass]">
          <component 
            :is="typeConfig.icon" 
            :class="typeConfig.iconClass"
            class="h-6 w-6"
          />
        </div>
        <div class="ml-4 flex-1">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
            {{ title || typeConfig.defaultTitle }}
          </h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            <p>{{ message || typeConfig.defaultMessage }}</p>
            
            <!-- Additional Details -->
            <div v-if="details" class="mt-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-md">
              <p class="text-xs text-gray-700 dark:text-gray-300">{{ details }}</p>
            </div>

            <!-- Input Field (for rename/input confirmations) -->
            <div v-if="requiresInput" class="mt-4">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {{ inputLabel || 'Type to confirm:' }}
              </label>
              <input
                ref="inputRef"
                v-model="inputValue"
                type="text"
                :placeholder="inputPlaceholder"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                @keyup.enter="handleConfirm"
              />
              <p v-if="inputError" class="mt-1 text-sm text-red-600">{{ inputError }}</p>
            </div>

            <!-- Checkbox confirmation -->
            <div v-if="requiresCheckbox" class="mt-4">
              <label class="flex items-center">
                <input
                  v-model="checkboxValue"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">
                  {{ checkboxLabel || 'I understand the consequences' }}
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Custom Footer -->
    <div class="bg-gray-50 dark:bg-gray-700 px-6 py-4 flex justify-end space-x-3">
      <Button
        variant="ghost"
        @click="handleClose"
        :disabled="loading"
      >
        {{ cancelText || 'Cancel' }}
      </Button>
      
      <Button
        :variant="typeConfig.buttonVariant"
        @click="handleConfirm"
        :loading="loading"
        :disabled="!canConfirm"
      >
        {{ confirmText || typeConfig.defaultConfirmText }}
      </Button>
    </div>
  </Modal>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import Modal from './Modal.vue'
import Button from './Button.vue'
import {
  ExclamationTriangleIcon,
  TrashIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
  CheckCircleIcon,
  QuestionMarkCircleIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'warning',
    validator: value => ['warning', 'danger', 'info', 'success', 'question', 'delete'].includes(value)
  },
  title: String,
  message: String,
  details: String,
  confirmText: String,
  cancelText: String,
  size: {
    type: String,
    default: 'sm'
  },
  persistent: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  // Input confirmation
  requiresInput: {
    type: Boolean,
    default: false
  },
  inputLabel: String,
  inputPlaceholder: String,
  inputValidation: {
    type: [String, RegExp, Function],
    default: null
  },
  inputRequired: {
    type: String,
    default: '' // Value that must be entered to confirm
  },
  // Checkbox confirmation
  requiresCheckbox: {
    type: Boolean,
    default: false
  },
  checkboxLabel: String
})

const emit = defineEmits(['confirm', 'cancel', 'close', 'update:isOpen'])

const inputRef = ref(null)
const inputValue = ref('')
const inputError = ref('')
const checkboxValue = ref(false)

const typeConfig = computed(() => {
  const configs = {
    warning: {
      icon: ExclamationTriangleIcon,
      iconClass: 'text-yellow-600',
      bgClass: 'bg-yellow-100',
      buttonVariant: 'warning',
      defaultTitle: 'Warning',
      defaultMessage: 'This action may have consequences. Do you want to continue?',
      defaultConfirmText: 'Continue'
    },
    danger: {
      icon: ExclamationCircleIcon,
      iconClass: 'text-red-600',
      bgClass: 'bg-red-100',
      buttonVariant: 'danger',
      defaultTitle: 'Dangerous Action',
      defaultMessage: 'This action cannot be undone. Are you sure?',
      defaultConfirmText: 'Yes, Continue'
    },
    delete: {
      icon: TrashIcon,
      iconClass: 'text-red-600',
      bgClass: 'bg-red-100',
      buttonVariant: 'danger',
      defaultTitle: 'Delete Confirmation',
      defaultMessage: 'This item will be permanently deleted. This action cannot be undone.',
      defaultConfirmText: 'Delete'
    },
    info: {
      icon: InformationCircleIcon,
      iconClass: 'text-blue-600',
      bgClass: 'bg-blue-100',
      buttonVariant: 'primary',
      defaultTitle: 'Information',
      defaultMessage: 'Please confirm this action.',
      defaultConfirmText: 'OK'
    },
    success: {
      icon: CheckCircleIcon,
      iconClass: 'text-green-600',
      bgClass: 'bg-green-100',
      buttonVariant: 'success',
      defaultTitle: 'Success',
      defaultMessage: 'The action was completed successfully.',
      defaultConfirmText: 'OK'
    },
    question: {
      icon: QuestionMarkCircleIcon,
      iconClass: 'text-gray-600',
      bgClass: 'bg-gray-100',
      buttonVariant: 'primary',
      defaultTitle: 'Confirmation',
      defaultMessage: 'Do you want to proceed with this action?',
      defaultConfirmText: 'Yes'
    }
  }
  
  return configs[props.type] || configs.question
})

const canConfirm = computed(() => {
  if (props.loading) return false
  
  if (props.requiresInput) {
    if (props.inputRequired && inputValue.value !== props.inputRequired) {
      return false
    }
    if (props.inputValidation) {
      if (typeof props.inputValidation === 'string') {
        return inputValue.value === props.inputValidation
      }
      if (props.inputValidation instanceof RegExp) {
        return props.inputValidation.test(inputValue.value)
      }
      if (typeof props.inputValidation === 'function') {
        return props.inputValidation(inputValue.value)
      }
    }
    return inputValue.value.trim().length > 0
  }
  
  if (props.requiresCheckbox) {
    return checkboxValue.value
  }
  
  return true
})

const validateInput = () => {
  inputError.value = ''
  
  if (props.requiresInput) {
    if (props.inputRequired && inputValue.value !== props.inputRequired) {
      inputError.value = `Please type "${props.inputRequired}" to confirm`
      return false
    }
    
    if (props.inputValidation) {
      if (typeof props.inputValidation === 'string') {
        if (inputValue.value !== props.inputValidation) {
          inputError.value = `Input must match "${props.inputValidation}"`
          return false
        }
      } else if (props.inputValidation instanceof RegExp) {
        if (!props.inputValidation.test(inputValue.value)) {
          inputError.value = 'Input format is invalid'
          return false
        }
      } else if (typeof props.inputValidation === 'function') {
        const result = props.inputValidation(inputValue.value)
        if (result !== true) {
          inputError.value = typeof result === 'string' ? result : 'Input is invalid'
          return false
        }
      }
    }
    
    if (!inputValue.value.trim()) {
      inputError.value = 'This field is required'
      return false
    }
  }
  
  return true
})

const handleConfirm = () => {
  if (!validateInput() || !canConfirm.value) return
  
  emit('confirm', {
    inputValue: inputValue.value,
    checkboxValue: checkboxValue.value
  })
}

const handleClose = () => {
  emit('cancel')
  emit('close')
  reset()
}

const reset = () => {
  inputValue.value = ''
  inputError.value = ''
  checkboxValue.value = false
}

// Focus input when modal opens
watch(() => props.isOpen, async (isOpen) => {
  if (isOpen && props.requiresInput) {
    await nextTick()
    inputRef.value?.focus()
  }
  if (!isOpen) {
    reset()
  }
})

// Watch input value for validation
watch(inputValue, () => {
  if (inputError.value) {
    validateInput()
  }
})
</script>