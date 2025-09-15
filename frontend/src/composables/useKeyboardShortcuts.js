import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'

export function useKeyboardShortcuts() {
  const router = useRouter()
  const themeStore = useThemeStore()
  const uiStore = useUIStore()

  // Key combination helpers
  const isModifierKey = (event, modifier) => {
    switch (modifier) {
      case 'ctrl': return event.ctrlKey || event.metaKey // Support both Ctrl and Cmd
      case 'alt': return event.altKey
      case 'shift': return event.shiftKey
      case 'meta': return event.metaKey
      default: return false
    }
  }

  const matchesShortcut = (event, shortcut) => {
    const parts = shortcut.toLowerCase().split('+')
    const key = parts[parts.length - 1]
    const modifiers = parts.slice(0, -1)

    // Check if the key matches
    if (event.key.toLowerCase() !== key && event.code.toLowerCase() !== key.toLowerCase()) {
      return false
    }

    // Check if all required modifiers are pressed
    return modifiers.every(modifier => isModifierKey(event, modifier))
  }

  // Default shortcuts configuration
  const shortcuts = {
    // Navigation shortcuts
    'ctrl+1': () => router.push('/edgeai/dashboard'),
    'ctrl+2': () => router.push('/edgeai/all-nodes'),
    'ctrl+3': () => router.push('/edgeai/model-management'),
    'ctrl+4': () => router.push('/edgeai/project-manager'),
    'ctrl+5': () => router.push('/edgeai/task-manager'),
    'ctrl+6': () => router.push('/edgeai/performance-metrics'),
    'ctrl+7': () => router.push('/edgeai/system-logs'),
    
    // P2PAI Navigation shortcuts
    'alt+1': () => router.push('/p2pai/dashboard'),
    'alt+2': () => router.push('/p2pai/model-dashboard'),
    'alt+3': () => router.push('/p2pai/training'),
    'alt+4': () => router.push('/p2pai/nodes'),
    
    // Theme and UI shortcuts
    'ctrl+shift+t': () => themeStore.toggleTheme(),
    'ctrl+shift+d': () => themeStore.setTheme('dark'),
    'ctrl+shift+l': () => themeStore.setTheme('light'),
    
    // Action shortcuts
    'ctrl+r': (event) => {
      event.preventDefault()
      window.location.reload()
    },
    'ctrl+n': () => router.push('/edgeai/create-project'),
    'ctrl+i': () => router.push('/edgeai/import-project'),
    'ctrl+m': () => router.push('/edgeai/model-management'),
    
    // Search and find
    'ctrl+f': (event) => {
      event.preventDefault()
      // Focus search input if it exists
      const searchInput = document.querySelector('input[type="search"], input[placeholder*="search" i], input[placeholder*="Search" i]')
      if (searchInput) {
        searchInput.focus()
        searchInput.select()
      }
    },
    
    // Help and info
    'ctrl+shift+h': () => {
      uiStore.addNotification({
        type: 'info',
        title: 'Keyboard Shortcuts',
        message: 'Press Ctrl+? to see all available shortcuts',
        duration: 5000
      })
    },
    
    'ctrl+shift+?': () => showShortcutsHelp(),
    
    // Quick actions
    'alt+r': () => {
      // Refresh current page data
      const refreshButton = document.querySelector('button[aria-label*="refresh" i], button[title*="refresh" i]')
      if (refreshButton) {
        refreshButton.click()
      }
    },
    
    'escape': () => {
      // Close modals, dropdowns, etc.
      const modal = document.querySelector('[role="dialog"]')
      if (modal) {
        const closeButton = modal.querySelector('button[aria-label*="close" i], button[title*="close" i], .modal-close')
        if (closeButton) {
          closeButton.click()
        }
      }
      
      // Close dropdowns
      const openDropdown = document.querySelector('.dropdown.open, .dropdown-menu.show')
      if (openDropdown) {
        openDropdown.classList.remove('open', 'show')
      }
    },
    
    // Focus management
    'tab': (event) => {
      // Enhanced tab navigation for better accessibility
      const focusableElements = document.querySelectorAll(
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
      
      if (focusableElements.length === 0) return
      
      const currentIndex = Array.from(focusableElements).indexOf(document.activeElement)
      let nextIndex
      
      if (event.shiftKey) {
        nextIndex = currentIndex <= 0 ? focusableElements.length - 1 : currentIndex - 1
      } else {
        nextIndex = currentIndex >= focusableElements.length - 1 ? 0 : currentIndex + 1
      }
      
      focusableElements[nextIndex]?.focus()
    }
  }

  const showShortcutsHelp = () => {
    const shortcutsList = Object.entries(shortcuts)
      .filter(([key]) => !['tab', 'escape'].includes(key))
      .map(([key, action]) => {
        const description = getShortcutDescription(key, action)
        return `${key.toUpperCase()}: ${description}`
      })
      .join('\n')

    uiStore.addNotification({
      type: 'info',
      title: 'Available Keyboard Shortcuts',
      message: shortcutsList,
      duration: 15000
    })
  }

  const getShortcutDescription = (key, action) => {
    const descriptions = {
      'ctrl+1': 'Go to EdgeAI Dashboard',
      'ctrl+2': 'Go to All Nodes',
      'ctrl+3': 'Go to Model Management',
      'ctrl+4': 'Go to Project Manager',
      'ctrl+5': 'Go to Task Manager',
      'ctrl+6': 'Go to Performance Metrics',
      'ctrl+7': 'Go to System Logs',
      'alt+1': 'Go to P2PAI Dashboard',
      'alt+2': 'Go to P2PAI Model Dashboard',
      'alt+3': 'Go to P2PAI Training',
      'alt+4': 'Go to P2PAI Nodes',
      'ctrl+shift+t': 'Toggle Theme',
      'ctrl+shift+d': 'Switch to Dark Theme',
      'ctrl+shift+l': 'Switch to Light Theme',
      'ctrl+r': 'Refresh Page',
      'ctrl+n': 'Create New Project',
      'ctrl+i': 'Import Project',
      'ctrl+m': 'Open Model Management',
      'ctrl+f': 'Focus Search',
      'ctrl+shift+h': 'Show Help',
      'ctrl+shift+?': 'Show All Shortcuts',
      'alt+r': 'Refresh Data'
    }
    
    return descriptions[key] || 'Custom Action'
  }

  // Event handler
  const handleKeyDown = (event) => {
    // Skip if user is typing in an input field
    const isInputFocused = ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName) ||
                          document.activeElement?.contentEditable === 'true'
    
    // Allow certain shortcuts even when input is focused
    const allowedInInput = ['escape', 'ctrl+f', 'ctrl+shift+h', 'ctrl+shift+?', 'ctrl+shift+t']
    
    if (isInputFocused && !allowedInInput.some(shortcut => matchesShortcut(event, shortcut))) {
      return
    }

    // Check each shortcut
    for (const [shortcut, action] of Object.entries(shortcuts)) {
      if (matchesShortcut(event, shortcut)) {
        try {
          action(event)
        } catch (error) {
          console.error(`Error executing shortcut ${shortcut}:`, error)
          uiStore.addNotification({
            type: 'error',
            title: 'Shortcut Error',
            message: `Failed to execute shortcut: ${shortcut}`,
            duration: 3000
          })
        }
        break
      }
    }
  }

  // Add custom shortcut
  const addShortcut = (key, action, description) => {
    shortcuts[key] = action
    if (description) {
      // Store description for help
      shortcuts[key]._description = description
    }
  }

  // Remove shortcut
  const removeShortcut = (key) => {
    delete shortcuts[key]
  }

  // Check if shortcut exists
  const hasShortcut = (key) => {
    return key in shortcuts
  }

  // Get all shortcuts
  const getAllShortcuts = () => {
    return { ...shortcuts }
  }

  // Lifecycle
  onMounted(() => {
    document.addEventListener('keydown', handleKeyDown)
    
    // Show welcome message with shortcut hint
    setTimeout(() => {
      uiStore.addNotification({
        type: 'info',
        title: 'Keyboard Shortcuts Available',
        message: 'Press Ctrl+Shift+? to see all available shortcuts',
        duration: 3000
      })
    }, 2000)
  })

  onUnmounted(() => {
    document.removeEventListener('keydown', handleKeyDown)
  })

  return {
    addShortcut,
    removeShortcut,
    hasShortcut,
    getAllShortcuts,
    showShortcutsHelp
  }
}

// EdgeAI specific shortcuts
export function useEdgeAIShortcuts() {
  const router = useRouter()
  const uiStore = useUIStore()
  
  const edgeAIShortcuts = {
    // Quick navigation within EdgeAI
    'g d': () => router.push('/edgeai/dashboard'),
    'g n': () => router.push('/edgeai/all-nodes'),
    'g m': () => router.push('/edgeai/model-management'),
    'g p': () => router.push('/edgeai/project-manager'),
    'g t': () => router.push('/edgeai/task-manager'),
    'g v': () => router.push('/edgeai/visualization'),
    
    // Quick actions
    'c p': () => router.push('/edgeai/create-project'),
    'i p': () => router.push('/edgeai/import-project'),
    
    // Data refresh
    'r r': () => {
      const refreshButtons = document.querySelectorAll('button[aria-label*="refresh" i], button[title*="refresh" i]')
      refreshButtons.forEach(button => button.click())
    },
    
    // Export actions
    'e l': () => {
      const exportButton = document.querySelector('button[aria-label*="export" i], button[title*="export" i]')
      if (exportButton) {
        exportButton.click()
      }
    }
  }

  let keySequence = ''
  let sequenceTimeout = null

  const handleSequenceKeyDown = (event) => {
    // Only handle letter keys for sequences
    if (event.ctrlKey || event.altKey || event.metaKey || event.shiftKey) {
      return
    }

    if (event.key.length === 1 && /[a-z]/i.test(event.key)) {
      keySequence += event.key.toLowerCase()
      
      // Clear previous timeout
      if (sequenceTimeout) {
        clearTimeout(sequenceTimeout)
      }
      
      // Check for matching shortcuts
      const matchingShortcut = Object.keys(edgeAIShortcuts).find(shortcut => 
        shortcut.replace(/\s+/g, '') === keySequence
      )
      
      if (matchingShortcut) {
        event.preventDefault()
        edgeAIShortcuts[matchingShortcut]()
        keySequence = ''
      } else {
        // Set timeout to clear sequence
        sequenceTimeout = setTimeout(() => {
          keySequence = ''
        }, 1000)
      }
    } else {
      // Non-letter key resets sequence
      keySequence = ''
    }
  }

  onMounted(() => {
    document.addEventListener('keydown', handleSequenceKeyDown)
  })

  onUnmounted(() => {
    document.removeEventListener('keydown', handleSequenceKeyDown)
    if (sequenceTimeout) {
      clearTimeout(sequenceTimeout)
    }
  })

  return {
    edgeAIShortcuts
  }
}