/**
 * Number utilities for ensuring consistent decimal precision throughout the application
 */

/**
 * Format a number to exactly 2 decimal places
 * @param {number|string} value - The value to format
 * @param {number} decimals - Number of decimal places (default: 2)
 * @returns {number} - The formatted number as a float
 */
export function formatToDecimal(value, decimals = 2) {
  if (value === null || value === undefined || value === '') {
    return 0.00;
  }

  const num = parseFloat(value);
  if (isNaN(num)) {
    return 0.00;
  }

  return parseFloat(num.toFixed(decimals));
}

/**
 * Format a percentage value (0-100) to 2 decimal places
 * @param {number|string} value - The percentage value
 * @returns {number} - The formatted percentage
 */
export function formatPercentage(value) {
  const num = formatToDecimal(value, 2);
  // Ensure percentage is within valid range
  return Math.max(0.00, Math.min(100.00, num));
}

/**
 * Format a file size in MB to 2 decimal places
 * @param {number|string} value - The file size in MB
 * @returns {number} - The formatted file size
 */
export function formatFileSize(value) {
  const num = formatToDecimal(value, 2);
  // Ensure file size is not negative
  return Math.max(0.00, num);
}

/**
 * Format a data transfer amount (sent/received) to 2 decimal places
 * @param {number|string} value - The data transfer amount
 * @returns {number} - The formatted transfer amount
 */
export function formatDataTransfer(value) {
  const num = formatToDecimal(value, 2);
  // Ensure transfer amount is not negative
  return Math.max(0.00, num);
}

/**
 * Format a loss value to 2 decimal places
 * @param {number|string} value - The loss value
 * @returns {number} - The formatted loss value
 */
export function formatLoss(value) {
  const num = formatToDecimal(value, 2);
  // Loss values should not be negative
  return Math.max(0.00, num);
}

/**
 * Format an accuracy value (0-100) to 2 decimal places
 * @param {number|string} value - The accuracy value
 * @returns {number} - The formatted accuracy value
 */
export function formatAccuracy(value) {
  return formatPercentage(value);
}

/**
 * Pre-process form data to ensure all numeric fields have proper decimal precision
 * @param {Object} data - The form data object
 * @param {Object} fieldMappings - Mapping of fields to their formatting functions
 * @returns {Object} - The processed data object
 */
export function preprocessFormData(data, fieldMappings = {}) {
  const processed = { ...data };

  // Default field mappings
  const defaultMappings = {
    progress: formatPercentage,
    cpu_usage: formatPercentage,
    memory_usage: formatPercentage,
    disk_usage: formatPercentage,
    sent: formatDataTransfer,
    received: formatDataTransfer,
    size: formatFileSize,
    loss: formatLoss,
    accuracy: formatAccuracy,
    // Add more mappings as needed
  };

  const mappings = { ...defaultMappings, ...fieldMappings };

  // Process each field
  for (const [field, formatter] of Object.entries(mappings)) {
    if (processed.hasOwnProperty(field)) {
      processed[field] = formatter(processed[field]);
    }
  }

  return processed;
}

/**
 * Validate that a numeric value is within the expected range
 * @param {number} value - The value to validate
 * @param {number} min - Minimum allowed value
 * @param {number} max - Maximum allowed value
 * @returns {boolean} - Whether the value is valid
 */
export function validateNumericRange(value, min = 0, max = 100) {
  const num = parseFloat(value);
  return !isNaN(num) && num >= min && num <= max;
}

/**
 * Create a validation function for percentage values (0-100)
 * @param {string} fieldName - Name of the field for error messages
 * @returns {Function} - Validation function
 */
export function createPercentageValidator(fieldName = 'Value') {
  return (value) => {
    if (!validateNumericRange(value, 0, 100)) {
      return `${fieldName} must be between 0.00 and 100.00`;
    }
    return null; // No error
  };
}

/**
 * Create a validation function for positive numeric values
 * @param {string} fieldName - Name of the field for error messages
 * @param {number} maxValue - Maximum allowed value (optional)
 * @returns {Function} - Validation function
 */
export function createPositiveNumberValidator(fieldName = 'Value', maxValue = Infinity) {
  return (value) => {
    const num = parseFloat(value);
    if (isNaN(num) || num < 0) {
      return `${fieldName} must be a positive number`;
    }
    if (num > maxValue) {
      return `${fieldName} cannot exceed ${maxValue}`;
    }
    return null; // No error
  };
}

/**
 * Format display values with proper decimal places and units
 * @param {number} value - The numeric value
 * @param {string} unit - The unit to append (e.g., '%', 'MB', etc.)
 * @param {number} decimals - Number of decimal places
 * @returns {string} - Formatted display string
 */
export function formatDisplayValue(value, unit = '', decimals = 2) {
  const formatted = formatToDecimal(value, decimals);
  return unit ? `${formatted}${unit}` : formatted.toString();
}

/**
 * Parse and clean numeric input from form fields
 * @param {string|number} value - The input value
 * @param {number} decimals - Number of decimal places to preserve
 * @returns {number} - The cleaned numeric value
 */
export function parseNumericInput(value, decimals = 2) {
  if (typeof value === 'string') {
    // Remove any non-numeric characters except decimal point and minus sign
    const cleaned = value.replace(/[^0-9.-]/g, '');
    return formatToDecimal(cleaned, decimals);
  }
  return formatToDecimal(value, decimals);
}

export default {
  formatToDecimal,
  formatPercentage,
  formatFileSize,
  formatDataTransfer,
  formatLoss,
  formatAccuracy,
  preprocessFormData,
  validateNumericRange,
  createPercentageValidator,
  createPositiveNumberValidator,
  formatDisplayValue,
  parseNumericInput
};