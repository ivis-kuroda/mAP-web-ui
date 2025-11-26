<script setup lang="ts">
import type { FormError } from '@nuxt/ui'

const route = useRoute()
const { users, repositories, groups } = useDataStore()

const userId = route.params.id as string
const user = users.find(u => u.id === userId)

const isCreate = false
const isEdit = false
const isDetail = true
const pageTitle = ref('')
if (isDetail) {
  pageTitle.value = 'ユーザー詳細'
}
else if (isCreate) {
  pageTitle.value = 'ユーザー追加'
}
else if (isEdit) {
  pageTitle.value = 'ユーザー編集'
}

const buttonLabel1 = ref('')
if (isCreate) {
  buttonLabel1.value = '作成'
}
else if (isEdit) {
  buttonLabel1.value = '保存'
}
else if (isDetail) {
  buttonLabel1.value = '編集'
}

const buttonIcon = ref('')
buttonIcon.value = isDetail ? 'i-lucide-edit' : 'i-lucide-save'

interface UserFormState {
  eppn?: string
  userId?: string
  userName?: string
  email?: string
}

const state = reactive<UserFormState>({
  eppn: isCreate ? undefined : user?.eppn,
  userId: isCreate ? undefined : user?.id,
  userName: isCreate ? undefined : user?.displayName,
  email: isCreate ? undefined : user?.email,
})

const validate = (state: UserFormState): FormError[] => {
  const errors = []
  if (!state.eppn) errors.push({ name: 'eppn', message: '必須項目です' })
  return errors
}

const langSelect = ref(['日本語', '英語'])
const repositoryNames = ref(repositories.map(repo => repo.displayName))
const affiliatedRepoNames = repositories[0]?.displayName
const groupNames = groups.map(group => group!.displayName)
const affiliatedGroupNames = [
  groups[3]!.displayName, groups[4]!.displayName, groups[5]!.displayName,
]
const lang = ref(isCreate ? undefined : '日本語')
const groupvalue = ref(isCreate
  ? ['']
  : ['jc_aaa_groups_AAA_parent2',
      'jc_aaa_groups_AAA_parent3'])
const conectgroups = ref([''])
const isConected = groupvalue.value != undefined
conectgroups.value = isConected ? groupvalue.value : ['なし']
</script>

<template>
  <div class="max-w-200 m-auto p-6">
    <UPageHeader
      v-if="!isCreate"
      :title="state.userName" :ui="{ root: 'pt-0' }"
      :headline="$t('users')"
    />
    <UCard class="mt-6">
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-semibold">
            {{ pageTitle }}
          </h2>
          <div class="flex space-x-4 justify-end">
            <UButton v-if="!isDetail" label="キャンセル" color="neutral" variant="soft" />
            <UButton
              v-if="!isDetail"
              :label="buttonLabel1" class="flex justify-center" color="info" variant="subtle"
              :icon="buttonIcon" to="/users"
            />
            <UButton
              v-if="isDetail"
              :label="buttonLabel1" class="flex justify-center" color="warning" variant="subtle"
              :icon="buttonIcon" :to="`/users/${userId}/edit`"
            />
          </div>
        </div>
      </template>
      <div>
        <UForm :validate="validate" :state="state" class="flex flex-col gap-4 w-full">
          <UFormField
            name="eppn" class="w-full" label="ePPN" :required="!isDetail"
            :ui="{ label: 'text-lg' }"
          >
            <UInput v-if="!isDetail" id="eppn" v-model="state.eppn" class="w-2/3" />
            <label v-if="isDetail" class="w-full text-left">{{ state.eppn }}</label>
          </UFormField>
          <UFormField
            name="userId" class="w-full" label="ユーザーID"
            :ui="{ label: 'text-lg' }"
          >
            <UInput v-if="!isDetail" id="userId" v-model="state.userId" class="w-2/3" />
            <label v-if="isDetail" class="w-full text-left">{{ state.userId }}</label>
          </UFormField>
          <UFormField
            name="userName" class="w-full" label="ユーザー名"
            :ui="{ label: 'text-lg' }"
          >
            <UInput v-if="!isDetail" id="userName" v-model="state.userName" class="w-2/3" />
            <label v-if="isDetail" class="w-full text-left">{{ state.userName }}</label>
          </UFormField>
          <UFormField
            name="email" class="w-full" label="メールアドレス"
            :ui="{ label: 'text-lg' }"
          >
            <UInput v-if="!isDetail" id="email" v-model="state.email" class="w-2/3" />
            <label v-if="isDetail" class="w-full text-left">{{ state.email }}</label>
          </UFormField>
          <UFormField
            class="w-full" label="優先言語"
            :ui="{ label: 'text-lg' }"
          >
            <USelectMenu
              v-if="!isDetail"
              :items="langSelect"
              :default-value="'日本語'"
              legend=""
              class="flex space-x-4 w-36"
            />
            <label v-if="isDetail" class="w-full text-left">{{ lang }}</label>
          </UFormField>
          <UFormField
            class="w-full" label="所属リポジトリ"
            :ui="{ label: 'text-lg' }"
          >
            <USelectMenu
              v-if="!isDetail"
              :items="repositoryNames"
              class="flex space-x-4 w-2/3"
              multiple
            />
            <label v-if="isDetail" for="groupname" class="w-full text-left">
              <span>{{ affiliatedRepoNames }}</span>
              <UBadge variant="subtle" class="mx-2">{{ $t('user.role.repo_admin') }}</UBadge>
            </label>
          </UFormField>
          <UFormField
            class="w-full" label="所属グループ" :required="!isDetail"
            :ui="{ label: 'text-lg' }"
          >
            <USelectMenu
              v-if="!isDetail"
              :items="groupNames"
              legend=""
              class="flex space-x-4 w-2/3"
            />
            <div v-if="isDetail" class="flex grid-cols-2 gap-10">
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
      </div>
      <div v-if="isEdit" class="flex justify-center gap-3 mt-10">
        <UModal title="グループを削除しますか？" description="削除したグループは復元できません">
          <UButton
            color="error"
            label="グループ削除"
            variant="outline"
          />
          <template #body>
            <div class="flex justify-right gap-4">
              <UButton label="キャンセル" color="neutral" variant="soft" />
              <UButton label="削除" color="error" />
            </div>
          </template>
        </UModal>
      </div>
    </UCard>
    <UPageCard v-if="!isCreate" variant="ghost">
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
