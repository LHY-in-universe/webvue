<template>
  <PageLayout
    title="Blockchain Dashboard"
    :icon="CubeIcon"
    icon-color="text-yellow-600"
    :username="authStore.user?.username"
    :is-dark="themeStore.isDark"
    page-title="Blockchain Network Management"
    page-description="Manage distributed blockchain networks and smart contracts"
    center-header
    variant="dashboard"
    @logout="logout"
    @theme-toggle="toggleTheme"
  >

    <!-- Main Services -->
    <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <DashboardCard
          title="Blockchain Explorer"
          description="View and analyze blockchain transactions, blocks, and network statistics"
          :icon="CubeIcon"
          variant="primary"
          interactive
          :features="[
            { label: 'Network Type', value: 'Ethereum Compatible' },
            { label: 'Block Height', value: '18,425,678' },
            { label: 'Transaction Pool', value: '2,456 Pending' },
            { label: 'Network Status', value: 'Healthy' }
          ]"
          action-label="View Blocks"
          action-variant="primary"
          @action="viewBlocks"
        />

        <DashboardCard
          title="Smart Contract Manager"
          description="Deploy, monitor, and interact with smart contracts"
          :icon="DocumentTextIcon"
          variant="warning"
          interactive
          :features="[
            { label: 'Active Contracts', value: '145' },
            { label: 'Solidity Version', value: '0.8.19' },
            { label: 'Gas Optimization', value: 'Enabled' },
            { label: 'Verification', value: 'Automatic' }
          ]"
          action-label="Manage Contracts"
          action-variant="warning"
          @action="manageContracts"
        />
      </div>

      <!-- Network Tools -->
      <div class="grid md:grid-cols-3 gap-6 mt-12 max-w-6xl mx-auto">
        <DashboardCard
          title="Node Management"
          description="Monitor and manage blockchain network nodes"
          :icon="ServerIcon"
          variant="success"
          interactive
          :stats="[
            { label: 'Active Nodes', value: '8' },
            { label: 'Synced Nodes', value: '7' }
          ]"
          action-label="Manage Nodes"
          action-variant="success"
          @action="manageNodes"
        />

        <DashboardCard
          title="Token Analytics"
          description="Track token metrics and trading data"
          :icon="CurrencyDollarIcon"
          variant="info"
          interactive
          :stats="[
            { label: 'Total Supply', value: '1,000,000' },
            { label: 'Circulating', value: '750,000' }
          ]"
          action-label="View Analytics"
          action-variant="primary"
          @action="viewTokenAnalytics"
        />

        <DashboardCard
          title="Consensus Monitor"
          description="Monitor blockchain consensus and validator performance"
          :icon="ShieldCheckIcon"
          variant="danger"
          interactive
          :stats="[
            { label: 'Validators', value: '21' },
            { label: 'Uptime', value: '99.9%' }
          ]"
          action-label="Monitor Consensus"
          action-variant="danger"
          @action="monitorConsensus"
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
  CubeIcon, 
  DocumentTextIcon,
  ServerIcon,
  CurrencyDollarIcon,
  ShieldCheckIcon
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

const viewBlocks = () => {
  router.push('/blockchain/visualization')
}

const manageContracts = () => {
  console.log('Opening Smart Contract Manager...')
}

const manageNodes = () => {
  console.log('Opening Node Management...')
}

const viewTokenAnalytics = () => {
  console.log('Opening Token Analytics...')
}

const monitorConsensus = () => {
  console.log('Opening Consensus Monitor...')
}
</script>