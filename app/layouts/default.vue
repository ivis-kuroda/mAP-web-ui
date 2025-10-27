<script setup lang="ts">
const toaster = { position: 'top-right' } as const
</script>

<template>
  <UApp :toaster="toaster">
    <AppHeader />

    <UMain>
      <slot />
    </UMain>

    <AppFooter />
  </UApp>
</template>
