<script setup lang="ts">
import { description, name as title } from '@@/package.json'

const route = useRoute()

let next = route.query.next
if (Array.isArray(next)) {
  next = next[0]
}
</script>

<template>
  <UPage>
    <UPageSection
      :title="title"
      :description="description"
      :ui="{ body: 'flex justify-center items-center' }"
    >
      <template #body>
        <EmbeddedDs :next="next as string" />
      </template>
    </UPageSection>
  </UPage>
</template>
