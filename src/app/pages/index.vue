<script setup lang="ts">
import { description, name as title } from '@@/package.json'
</script>

<template>
  <div>
    <UPageHero
      :title="title"
      :description="description"
    />
  </div>
</template>
