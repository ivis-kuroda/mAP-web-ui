<script setup lang="ts">
import type { FormError } from '@nuxt/ui'

const localePath = useLocalePath()
const { repositories, groups } = useDataStore()

interface UserFormState {
  mode: 'add' | 'edit' | 'detail'
  eppn?: string
  userId?: string
  userName?: string
  email?: string
}
const { state } = defineProps<{ state: UserFormState }>()

const validate = (state: UserFormState): FormError[] => {
  const errors = []
  if (!state.eppn) errors.push({ name: 'eppn', message: $t('form.error.required') })
  return errors
}

const langSelect = computed(() => [$t('language.japanese'), $t('language.english')])
const repositoryNames = ref(repositories.map(repo => repo.displayName))
const affiliatedRepoNames = repositories[0]?.displayName
const userRoles = ref([
  $t('user.role.admin'), $t('user.role.repo_admin'), $t('user.role.community_admin'),
  $t('user.role.contributor'), $t('user.role.general'),
])
const groupNames = groups.map(group => group!.displayName)
const affiliatedGroupNames = [
  groups[3]!.displayName, groups[4]!.displayName, groups[5]!.displayName,
]
const lang = $t('language.japanese')
</script>

<template>
  <UForm :validate="validate" :state="state" class="flex flex-col gap-4 w-full">
    <UFormField
      name="eppn" label="ePPN"
      :required="['add', 'edit'].includes(state.mode)"
      class="w-full" :ui="{ label: 'text-lg' }"
    >
      <p v-if="state.mode === 'detail'" class="w-full text-left">
        {{ state.eppn }}
      </p>
      <UInput v-else id="eppn" v-state.model="state.eppn" class="w-2/3" />
    </UFormField>
    <UFormField
      name="userId" :label="$t('user.view.user-id-label')"
      class="w-full" :ui="{ label: 'text-lg' }"
    >
      <UInput v-if="state.mode === 'add'" id="userId" v-state.model="state.userId" class="w-2/3" />
      <p v-else class="w-full text-left">
        {{ state.userId }}
      </p>
    </UFormField>
    <UFormField
      name="userName" :label="$t('user.view.user-name-label')"
      class="w-full" :ui="{ label: 'text-lg' }"
    >
      <p v-if="state.mode === 'detail'" class="w-full text-left">
        {{ state.userName }}
      </p>
      <UInput v-else id="userName" v-state.model="state.userName" class="w-2/3" />
    </UFormField>
    <UFormField
      name="email" :label="$t('user.view.email-label')"
      class="w-full" :ui="{ label: 'text-lg' }"
    >
      <p v-if="state.mode === 'detail'" class="w-full text-left">
        {{ state.email }}
      </p>
      <UInput v-else id="email" v-state.model="state.email" class="w-2/3" />
    </UFormField>
    <UFormField
      :label="$t('user.view.preferred-language-label')"
      class="w-full" :ui="{ label: 'text-lg' }"
    >
      <p v-if="state.mode === 'detail'" class="w-full text-left">
        {{ lang }}
      </p>
      <USelectMenu v-else :items="langSelect" class="flex space-x-4 w-36" />
    </UFormField>
    <UFormField
      :label="$t('user.view.repositories-label')"
      :required="['add', 'edit'].includes(state.mode)"
      class="w-2/3" :ui="{ label: 'text-lg' }"
    >
      <template v-if="['add', 'edit'].includes(state.mode)" #hint>
        <UIcon name="i-lucide-plus" />
      </template>
      <div class="flex">
        <USelectMenu
          v-if="['add', 'edit'].includes(state.mode)"
          :placeholder="$t('repositories')"
          :items="repositoryNames"
          multiple
          class="flex space-x-4 w-2/3 mr-2.5"
        />
        <USelectMenu
          v-if="['add', 'edit'].includes(state.mode)"
          :placeholder="$t('user.role-filter')"
          :items="userRoles"
          class="flex space-x-4 w-1/3"
        />
      </div>
      <p v-if="state.mode === 'detail'" for="groupname" class="w-full text-left">
        <span>{{ affiliatedRepoNames }}</span>
        <UBadge variant="subtle" class="mx-2">
          {{ $t('user.role.repo_admin') }}
        </UBadge>
      </p>
    </UFormField>
    <UFormField
      :label="$t('user.view.groups-label')"
      :required="['add', 'edit'].includes(state.mode)"
      class="w-full" :ui="{ label: 'text-lg' }"
    >
      <USelectMenu
        v-if="['add', 'edit'].includes(state.mode)"
        :placeholder="$t('groups')"
        :items="groupNames"
        class="flex space-x-4 w-2/3"
        multiple
      />
      <div v-if="state.mode === 'detail'" class="flex grid-cols-2 gap-10">
        <div class="w-full">
          <p
            v-for="value in affiliatedGroupNames" :key="value"
            for="groupname" class="w-full text-left"
          >
            {{ value }}
          </p>
        </div>
        <div class="flex items-end w-full justify-end pr-20">
          <NuxtLinkLocale to="/groups" class="inline-flex hover:underline">
            一覧へ
            <UIcon
              name="i-lucide-chevron-right"
              class="size-5 shrink-0 inline-flex"
            />
          </NuxtLinkLocale>
        </div>
      </div>
    </UFormField>
  </UForm>
  <div v-if="state.mode === 'edit'" class="flex justify-center gap-3 mt-10">
    <UModal
      :title="$t('user.modal.delete-user-title')"
      :description="$t('user.modal.delete-user-description')"
      :ui="{ footer: 'justify-end' }"
    >
      <UButton
        :label="$t('user.delete-button')"
        color="error"
        variant="outline"
      />
      <template #footer="{ close }">
        <div class="flex gap-2">
          <UButton :label="$t('button.cancel')" color="neutral" variant="soft" @click="close" />
          <UButton :label="$t('button.delete')" color="error" :to="localePath('/users')" />
        </div>
      </template>
    </UModal>
  </div>
</template>
