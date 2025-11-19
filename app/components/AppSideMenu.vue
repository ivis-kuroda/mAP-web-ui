<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const route = useRoute()
const localePath = useLocalePath()

const items = computed<NavigationMenuItem[]>(() => [
  {
    label: $t('Management'), type: 'label',
  },
  {
    label: $t('repositories'),
    icon: 'i-lucide-folder',
    to: localePath('/repos'),
    active: route.path.startsWith(localePath('/repos')),
  },
  {
    label: $t('groups'),
    icon: 'i-lucide-users',
    to: localePath('/groups'),
    active: route.path.startsWith(localePath('/groups')),
  },
  {
    label: $t('users'),
    icon: 'i-lucide-user',
    to: localePath('/users'),
    active: route.path.startsWith(localePath('/users')),
  },
  {
    label: $t('Others'),
    type: 'label',
  },
  {
    label: $t('history'),
    icon: 'i-lucide-clock',
    to: localePath('/history'),
    active: route.path.startsWith(localePath('/history')),
  },
  {
    label: $t('cache-groups-menu'),
    icon: 'i-lucide-database',
    to: localePath('/cache'),
    active: route.path.startsWith(localePath('/cache')),
  },
])
</script>

<template>
  <UPageAside>
    <template #top>
      <UBadge variant="subtle" color="error">
        {{ $t('user.role.admin') }}
      </UBadge>
    </template>

    <UNavigationMenu :items="items" orientation="vertical" />
  </UPageAside>
</template>
