<script setup lang="ts">
const columns = [
  {
    label: 'Resources',
    children: [
      { label: 'Services', to: '/services' },
      { label: 'Groups', to: '/groups' },
      { label: 'Users', to: '/users' },
    ],
  },
  {
    label: 'Other',
    children: [
      { label: 'Settings', to: '/settings' },
    ],
  },
]
</script>

<template>
  <USeparator
    icon="i-simple-icons-nuxtdotjs" class="h-px"
  />

  <UFooter :ui="{ top: 'border-b border-default' }">
    <template #top>
      <UContainer>
        <UFooterColumns :columns="columns" />
      </UContainer>
    </template>

    <template #left>
      <p class="text-muted text-sm">
        &copy; {{ new Date().getFullYear() }} National Institute of Informatics
      </p>
    </template>

    <template #right>
      <UColorModeButton />
    </template>
  </UFooter>
</template>
