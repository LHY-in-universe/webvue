<template>
  <PageLayout
    title="Crypto Services Dashboard"
    :icon="KeyIcon"
    icon-color="text-red-600"
    :username="authStore.user?.username"
    :is-dark="themeStore.isDark"
    page-title="Key Management & Encryption Services"
    page-description="Secure key management and data encryption solutions"
    center-header
    variant="dashboard"
    @logout="logout"
    @theme-toggle="toggleTheme"
  >
    <!-- Service Cards -->
      <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <DashboardCard
          title="Key Manager"
          description="Manage cryptographic keys and certificates with enterprise-grade security"
          :icon="KeyIcon"
          variant="danger"
          interactive
          :features="[
            { label: 'Encryption Standard', value: 'AES-256' },
            { label: 'Key Storage', value: 'Hardware Security Module' },
            { label: 'Access Control', value: 'Role-Based' },
            { label: 'Audit Logging', value: 'Complete' }
          ]"
          action-label="Open Key Manager"
          action-variant="danger"
          @action="openKeyManager"
        />

        <DashboardCard
          title="Encryption Tools"
          description="Advanced encryption and decryption utilities for data protection"
          :icon="ShieldCheckIcon"
          variant="info"
          interactive
          :features="[
            { label: 'Supported Algorithms', value: 'RSA, ECC, AES' },
            { label: 'File Encryption', value: 'Yes' },
            { label: 'Batch Processing', value: 'Supported' },
            { label: 'Hash Functions', value: 'SHA-256, SHA-3' }
          ]"
          action-label="Open Encryption Tools"
          action-variant="primary"
          @action="openEncryptionTools"
        />
      </div>

      <!-- Additional Services -->
      <div class="grid md:grid-cols-3 gap-6 mt-12 max-w-6xl mx-auto">
        <DashboardCard
          title="Certificate Authority"
          description="Issue and manage digital certificates"
          :icon="DocumentCheckIcon"
          variant="success"
          interactive
          action-label="Manage Certificates"
          action-variant="success"
          @action="openCertificateAuthority"
        />

        <DashboardCard
          title="Secure Vault"
          description="Store sensitive data with zero-knowledge encryption"
          :icon="LockClosedIcon"
          variant="warning"
          interactive
          action-label="Access Vault"
          action-variant="warning"
          @action="openSecureVault"
        />

        <DashboardCard
          title="Crypto Analytics"
          description="Monitor cryptographic operations and security metrics"
          :icon="ChartBarIcon"
          variant="primary"
          interactive
          action-label="View Analytics"
          action-variant="primary"
          @action="openAnalytics"
        />
      </div>
  </PageLayout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import PageLayout from '@/components/layout/PageLayout.vue'
import DashboardCard from '@/components/ui/DashboardCard.vue'
import { 
  KeyIcon, 
  ShieldCheckIcon,
  DocumentCheckIcon,
  LockClosedIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const toggleTheme = (event) => {
  themeStore.toggleTheme(event)
}

const logout = () => {
  authStore.logout()
  router.push('/')
}

const openKeyManager = () => {
  console.log('Opening Key Manager...')
}

const openEncryptionTools = () => {
  console.log('Opening Encryption Tools...')
}

const openCertificateAuthority = () => {
  console.log('Opening Certificate Authority...')
}

const openSecureVault = () => {
  console.log('Opening Secure Vault...')
}

const openAnalytics = () => {
  router.push('/crypto/visualization')
}
</script>