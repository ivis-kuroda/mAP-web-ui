<script setup lang="ts">
const isAuthenticated = true

onMounted(() => {
  if (isAuthenticated) {
    navigateTo('/help/user/create-users')
  }
  else {
    navigateTo('/login')
  }
})
</script>
