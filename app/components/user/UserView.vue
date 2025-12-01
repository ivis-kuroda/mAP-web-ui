<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const localePath = useLocalePath()

const { users } = useDataStore()
const userId = route.params.id as string
const user = users.find(u => u.id === userId)

const { mode } = defineProps<{ mode: 'add' | 'edit' | 'detail' }>()

if (!user && mode !== 'add') {
  throw createError({
    statusCode: 404, statusMessage: `User not found: ${route.path}`, fatal: true,
  })
}

const titleMap = {
  add: $t('user.view.title-add'),
  edit: $t('user.view.title-edit'),
  detail: $t('user.view.title-detail'),
}
const pageTitle = ref(titleMap[mode])

const mainActionMap = {
  add: {
    // Add button
    label: $t('button.add'),
    icon: 'i-lucide-plus',
    onClick: () => {
      router.push(localePath('/users'))
    },
  },
  edit: {
    // Save button
    label: $t('button.save'),
    icon: 'i-lucide-save',
    onClick: () => {
      router.push(localePath(`/users/${userId}`))
    },
  },
  detail: {
    // Edit button
    label: $t('button.edit'),
    icon: 'i-lucide-edit',
    to: localePath(`/users/${userId}/edit`),
  },
}

interface UserFormState {
  eppn?: string
  userId?: string
  userName?: string
  email?: string
  repositories?: { id: string, displayName: string, role: string }[]
}

const userData = reactive<UserFormState>(
  mode === 'add'
    ? {}
    : {
        eppn: user?.eppn,
        userId: user?.id,
        userName: user?.displayName,
        email: user?.email,
      },
)
</script>

<template>
  <div class="max-w-200 m-auto p-6">
    <UPageHeader
      v-if="['edit', 'detail'].includes(mode)"
      :title="user!.displayName" :ui="{ root: 'pt-0' }"
      :headline="$t('users')"
    />
    <UCard class="mt-6">
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-semibold">
            {{ pageTitle }}
          </h2>
          <div v-if="mode=== 'detail'" class="flex">
            <UButton
              :label="mainActionMap.detail.label" color="warning" variant="subtle"
              :icon="mainActionMap.detail.icon" :to="mainActionMap.detail.to"
              class="flex justify-center"
            />
          </div>
          <div v-else class="flex space-x-4">
            <UButton
              :label="$t('button.cancel')"
              color="neutral" variant="soft"
              :to="mode==='add' ? localePath('/users') : localePath(`/users/${userId}`)"
            />
            <UButton
              :label="mainActionMap[mode].label" color="info" variant="subtle"
              :icon="mainActionMap[mode].icon" class="flex justify-center"
              @click="mainActionMap[mode].onClick"
            />
          </div>
        </div>
      </template>

      <UserForm :state="{ mode, ...userData }" />
    </UCard>
    <UPageCard v-if="['edit', 'detail'].includes(mode)" variant="ghost">
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-semibold">
            {{ $t('history') }}
          </h2>
        </div>
      </template>
      <template #body>
        <UChangelogVersions
          :ui="{
            container: 'gap-y-8 sm:gap-y-8 lg:gap-y-8', indicator: 'start-25',
          }"
        >
          <UChangelogVersion
            date="2025/11/5"
            :ui="{ container: 'pl-36', description: 'mt-0', indicator: 'w-25' }"
          >
            <template #date>
              2025/11/5
            </template>
            <template #description>
              <NuxtLinkLocale to="/users/1" class="font-bold hover:underline">
                青山太郎
              </NuxtLinkLocale>
              により作成
            </template>
          </UChangelogVersion>
          <UChangelogVersion
            date="2025/11/5"
            :ui="{ container: 'pl-36', description: 'mt-0', indicator: 'w-25' }"
          >
            <template #date>
              2025/11/5
            </template>
            <template #description>
              <NuxtLinkLocale to="/users/1" class="font-bold hover:underline">
                青山太郎
              </NuxtLinkLocale>
              により編集
            </template>
          </UChangelogVersion>
          <UChangelogVersion
            date="2025/11/5"
            :ui="{ container: 'pl-36', description: 'mt-0', indicator: 'w-25' }"
          >
            <template #date>
              2025/11/5
            </template>
            <template #description>
              システム管理者により編集
            </template>
          </UChangelogVersion>
          <UChangelogVersion
            date="2025/11/5"
            :ui="{ container: 'pl-36', description: 'mt-0', indicator: 'w-25' }"
          >
            <template #date>
              2025/11/5
            </template>
            <template #description>
              <NuxtLinkLocale to="/users/1" class="font-bold hover:underline">
                青山太郎
              </NuxtLinkLocale>
              により
              <NuxtLinkLocale to="/history" class="font-bold hover:underline">
                ダウンロード
              </NuxtLinkLocale>
            </template>
          </UChangelogVersion>
        </UChangelogVersions>
      </template>
    </UPageCard>
  </div>
</template>
