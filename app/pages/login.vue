<script setup lang="ts">
definePageMeta({
  layout: 'auth',
})
</script>

<template>
  <UPage>
    <UPageSection
      :title="$t('login-title')"
      :ui="{ body: 'flex justify-center items-center' }"
    >
      <template #body>
        <EmbeddedDs />
      </template>
    </UPageSection>
  </UPage>
</template>
