<script setup lang="ts">
import type { FooterColumn } from '@nuxt/ui'

const { links = true } = defineProps<{ links?: boolean }>()

const localePath = useLocalePath()

const columns = computed<FooterColumn[]>(() => [
  {
    label: $t('Management'),
    children: [
      { label: $t('repositories'), to: localePath('/repos') },
      { label: $t('groups'), to: localePath('/groups') },
      { label: $t('users'), to: localePath('/users') },
    ],
  },
  {
    label: $t('Others'),
    children: [
      { label: $t('history'), to: localePath('/history') },
      { label: $t('cache-groups-menu'), to: localePath('/cache') },
    ],
  },
])
</script>

<template>
  <USeparator icon="i-simple-icons-nuxtdotjs" class="h-px" />

  <UFooter :ui="{ top: 'border-b border-default' }">
    <template v-if="links" #top>
      <UContainer>
        <UPage>
          <template #left>
            <UPageAside />
          </template>

          <UPageBody class="pb-0 px-10">
            <UFooterColumns :columns="columns" :ui="{ root: 'xl:grid-cols-2' }" />
          </UPageBody>
        </UPage>
      </UContainer>
    </template>

    <template #left>
      <p class="text-muted text-sm">
        &copy; {{ new Date().getFullYear() }} National Institute of Informatics
      </p>
    </template>

    <template #right>
      <ULink to="" class="text-sm hover:underline inline-flex items-center gap-0.5">
        {{ $t('privacy-policy') }}
        <UIcon name="i-lucide-external-link" class="size-3.5 shrink-0" /></ULink>
      |
      <ULink to="" class="text-sm hover:underline inline-flex items-center gap-0.5">
        {{ $t('terms-of-use') }}
        <UIcon name="i-lucide-external-link" class="size-3.5 shrink-0" /></ULink>
    </template>
  </UFooter>
</template>
