<template>
  <UApp :toaster="{ position: 'top-center' }">
    <AppHeader />

    <UMain>
      <UContainer>
        <UPage>
          <template #left>
            <AppSideMenu />
          </template>

          <UPageBody>
            <slot />
          </UPageBody>
        </UPage>
      </UContainer>
    </UMain>

    <AppFooter />
  </UApp>
</template>
