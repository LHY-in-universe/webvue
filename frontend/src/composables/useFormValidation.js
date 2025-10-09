/**
 * Form validation composable with decimal precision support
 */
import { ref, computed } from 'vue'
import {
  createPercentageValidator,
  createPositiveNumberValidator,
  validateNumericRange,
  parseNumericInput
} from '@/utils/numberUtils'

export function useFormValidation() {
  const errors = ref({})
  const touched = ref({})

  /**
   * Clear all validation errors
   */
  const clearErrors = () => {
    errors.value = {}
    touched.value = {}
  }

  /**
   * Clear error for a specific field
   * @param {string} field - Field name
   */
  const clearFieldError = (field) => {
    delete errors.value[field]
    delete touched.value[field]
  }

  /**
   * Mark a field as touched
   * @param {string} field - Field name
   */
  const touchField = (field) => {
    touched.value[field] = true
  }

  /**
   * Validate a single field
   * @param {string} field - Field name
   * @param {*} value - Field value
   * @param {Function|Array} validator - Validator function or array of validators
   */
  const validateField = (field, value, validator) => {
    touchField(field)

    if (Array.isArray(validator)) {
      // Multiple validators
      for (const val of validator) {
        const error = val(value)
        if (error) {
          errors.value[field] = error
          return false
        }
      }
      clearFieldError(field)
      return true
    } else if (typeof validator === 'function') {
      // Single validator
      const error = validator(value)
      if (error) {
        errors.value[field] = error
        return false
      }
      clearFieldError(field)
      return true
    }

    return true
  }

  /**
   * Validate multiple fields at once
   * @param {Object} data - Data object with field values
   * @param {Object} validators - Object with field validators
   */
  const validateForm = (data, validators) => {
    let isValid = true

    for (const [field, validator] of Object.entries(validators)) {
      const fieldValid = validateField(field, data[field], validator)
      if (!fieldValid) {
        isValid = false
      }
    }

    return isValid
  }

  /**
   * Get validation state for a field
   * @param {string} field - Field name
   */
  const getFieldState = (field) => {
    const hasError = errors.value[field]
    const isTouched = touched.value[field]

    return {
      hasError: !!hasError,
      isTouched: !!isTouched,
      error: hasError || null,
      isValid: !hasError && isTouched
    }
  }

  // Computed properties
  const hasErrors = computed(() => Object.keys(errors.value).length > 0)
  const isFormValid = computed(() => !hasErrors.value && Object.keys(touched.value).length > 0)

  // Common validators for EdgeAI forms
  const validators = {
    required: (fieldName = 'Field') => (value) => {
      if (!value || (typeof value === 'string' && value.trim() === '')) {
        return `${fieldName} is required`
      }
      return null
    },

    percentage: createPercentageValidator,
    positiveNumber: createPositiveNumberValidator,

    nodeIp: (value) => {
      if (!value) return 'IP address is required'
      const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
      if (!ipRegex.test(value)) {
        return 'Please enter a valid IP address'
      }
      return null
    },

    learningRate: (value) => {
      const num = parseFloat(value)
      if (isNaN(num)) {
        return 'Learning rate must be a number'
      }
      if (num <= 0 || num > 1) {
        return 'Learning rate must be between 0 and 1'
      }
      return null
    },

    epochs: (value) => {
      const num = parseInt(value)
      if (isNaN(num) || num < 1 || num > 10000) {
        return 'Epochs must be between 1 and 10,000'
      }
      return null
    },

    batchSize: (value) => {
      const num = parseInt(value)
      if (isNaN(num) || num < 1 || num > 1024) {
        return 'Batch size must be between 1 and 1,024'
      }
      return null
    },

    projectName: (value) => {
      if (!value || value.trim().length === 0) {
        return 'Project name is required'
      }
      if (value.length > 200) {
        return 'Project name cannot exceed 200 characters'
      }
      return null
    },

    nodeName: (value) => {
      if (!value || value.trim().length === 0) {
        return 'Node name is required'
      }
      if (value.length > 200) {
        return 'Node name cannot exceed 200 characters'
      }
      return null
    },

    fileSize: (value) => {
      const num = parseFloat(value)
      if (isNaN(num) || num < 0) {
        return 'File size must be a positive number'
      }
      if (num > 10000) { // 10GB limit
        return 'File size cannot exceed 10GB'
      }
      return null
    }
  }

  /**
   * Create a validation handler for form inputs
   * @param {string} field - Field name
   * @param {Function|Array} validator - Validator function(s)
   */
  const createValidationHandler = (field, validator) => {
    return (value) => {
      return validateField(field, value, validator)
    }
  }

  /**
   * Create input handler with decimal precision and validation
   * @param {string} field - Field name
   * @param {Function} setter - Function to set the value
   * @param {Function|Array} validator - Validator function(s)
   * @param {number} decimals - Number of decimal places
   */
  const createNumericInputHandler = (field, setter, validator, decimals = 2) => {
    return (event) => {
      const rawValue = event.target.value
      const numericValue = parseNumericInput(rawValue, decimals)

      setter(numericValue)
      validateField(field, numericValue, validator)
    }
  }

  return {
    errors,
    touched,
    hasErrors,
    isFormValid,
    clearErrors,
    clearFieldError,
    touchField,
    validateField,
    validateForm,
    getFieldState,
    validators,
    createValidationHandler,
    createNumericInputHandler
  }
}

export default useFormValidation