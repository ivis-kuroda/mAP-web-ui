<template>
  <UApp :toaster="{ position: 'top-center' }">
    <AppHeader :search="false" :profile="false" />

    <UMain>
      <UContainer>
        <slot />
      </UContainer>
    </UMain>

    <AppFooter :links="false" />
  </UApp>
</template>
