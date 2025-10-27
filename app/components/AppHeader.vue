<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const rute = useRoute()

const { setLocale } = useI18n()
const localePath = useLocalePath()
const { currentLocale: locale, locales } = useAvailableLocales()

const items = computed<NavigationMenuItem[]>(() => [
  { label: $t('Home'), to: localePath('/') },
  { label: $t('Services'), to: localePath('/services'), active: rute.path.startsWith('/services') },
  { label: $t('Groups'), to: localePath('/groups'), active: rute.path.startsWith('/groups') },
  { label: $t('User'), to: localePath('/users'), active: rute.path.startsWith('/users') },
  { label: $t('Settings'), to: localePath('/settings') },
])
</script>

<template>
  <UHeader>
    <template #left>
      <NuxtLinkLocale to="/">
        <AppLogo class="w-auto h-6" />
      </NuxtLinkLocale>
    </template>

    <UNavigationMenu :items="items" variant="link" />

    <template #right>
      <UColorModeButton />

      <ULocaleSelect
        v-model="locale" :locales="locales" class="h-8 w-30 my-auto"
        @update:model-value="setLocale($event as AvailableLocaleCode)"
      />

      <UButton
        icon="i-lucide-log-in" color="neutral" variant="ghost" to="/login"
        class="lg:hidden"
      />

      <UButton
        :label="$t('sign-in')" color="neutral" variant="outline" to="/login"
        class="hidden lg:inline-flex"
      />
    </template>

    <template #body>
      <UNavigationMenu :items="items" orientation="vertical" class="-mx-2.5" />

      <USeparator class="my-6" />
      <UButton
        :label="$t('sign-in')" color="neutral" variant="subtle" to="/login"
        block class="mb-3"
      />
    </template>
  </UHeader>
</template>
