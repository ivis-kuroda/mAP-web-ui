<!-- eslint-disable unicorn/prevent-abbreviations -->
<script setup lang="ts">
const { data: navigation } = await useAsyncData('navigation', () => {
  return queryCollectionNavigation('help')
}, {
  transform: data => data.find(item => item.path === '/help')?.children || data || [],
})
const { data: files } = useLazyAsyncData('search', () => {
  return queryCollectionSearchSections('help')
}, {
  server: false,
})
</script>

<template>
  <div>
    <AppHeader :search="false" />

    <UMain>
      <UContainer>
        <UPage>
          <template #left>
            <UPageAside>
              <template #top>
                <UContentSearchButton :collapsed="false" />
              </template>

              <UContentNavigation
                :navigation="navigation"
                highlight
              />
            </UPageAside>
          </template>

          <slot />
        </UPage>
      </UContainer>
    </UMain>

    <AppFooter />

    <ClientOnly>
      <LazyUContentSearch
        :files="files"
        shortcut="meta_k"
        :navigation="navigation"
        :fuse="{ resultLimit: 42 }"
      />
    </ClientOnly>
  </div>
</template>
