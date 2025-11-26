<script setup lang="ts">
import type { FormError } from '@nuxt/ui'

const isCreate = false // 実際はパスを見て編集か作成かで判断
const isEdit = false // 実際はパスを見て編集か作成かで判断
const isDetail = true // 実際はパスを見て編集か作成かで判断
const pageTitle = ref('')
if (isDetail) {
  pageTitle.value = 'グループ詳細'
}
else if (isCreate) {
  pageTitle.value = 'グループ新規作成'
}
else if (isEdit) {
  pageTitle.value = 'グループ編集'
}

const buttonLabel1 = ref('')
if (isCreate) {
  buttonLabel1.value = '作成'
}
else if (isEdit) {
  buttonLabel1.value = '保存'
}
else if (isDetail) {
  buttonLabel1.value = 'グループ編集'
}
const buttonIcon = ref('')
buttonIcon.value = isDetail ? 'i-lucide-edit' : 'i-lucide-save'
const state = reactive({
  groupname: isCreate ? undefined : 'test_group_AAA', // 実際はmAPで取得したものを表示
  groupid: isCreate ? undefined : 'test_group_id', // 実際はmAPで取得したものを表示
})

const validate = (state: any): FormError[] => {
  const errors = []
  if (!state.groupname) errors.push({ name: 'groupname', message: '必須項目です' })
  if (!state.groupid) errors.push({ name: 'groupid', message: '必須項目です' })
  return errors
}

const items1 = ref(['公開', '非公開'])
const items3 = ref(['公開', 'メンバーにのみ公開', '非公開'])
const items4 = ref(['上位グループ名', '下位グループ名'])
const groupitems = ref(['jc_xxx_groups_AAA_parent1', 'jc_xxx_groups_AAA_parent2',
  'jc_xxx_groups_AAA_parent3', 'jc_xxx_groups_BBB']) // 実際はmAPで取得したものを表示
const value1 = ref(isCreate ? undefined : '公開') // 実際はmAPで取得したものを表示
const value3 = ref(isCreate ? undefined : '公開') // 実際はmAPで取得したものを表示
const groupvalue = ref(isCreate
  ? ['']
  : ['jc_xxx_groups_AAA_parent2',
      'jc_xxx_groups_AAA_parent3']) // 実際はmAPで取得したものを表示
const groupvalue2 = ref(isCreate ? undefined : '上位グループ名') // 実際はmAPで取得したものを表示
const conectgroups = ref([''])
const isConected = groupvalue.value != undefined
conectgroups.value = isConected ? groupvalue.value : ['なし']
</script>

<template>
  <UContainer class="max-w-3xl py-8">
    <h2 class="text-2xl font-semibold">
      {{ state.groupname }}
    </h2>
    <UPageCard
      class="mt-6 w-1/2" to="/users" icon="uiw:user"
      :title="$t('group.member-count')" :description="'10人'"
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
              :label="buttonLabel1" class="flex justify-center" color="warning" variant="subtle"
              :icon="buttonIcon" to="/groups/1/edit"
            />
          </div>
        </div>
      </template>
      <div>
        <UForm :validate="validate" :state="state" class="flex flex-col gap-4 w-full">
          <UFormField
            v-if="isDetail" class="w-full" label="管理者"
            :ui="{ label: 'text-lg' }"
          >
            <div class="flex space-x-2">
              <div class="flex flex-col">
                <label>USER_A</label>
                <label>USER_B</label>
                <label>USER_C</label>
              </div>
              <div class="flex mt-auto">
                <ULink to="/users" class="underline">他3名</ULink>
              </div>
            </div>
          </UFormField>
          <UFormField
            name="groupname" class="w-full" label="グループ名" :required="!isDetail"
            :ui="{ label: 'text-lg' }"
          >
            <UInput v-if="!isDetail" id="groupname" v-model="state.groupname" class="w-1/2" />
            <label v-if="isDetail" class="w-full text-left">{{ state.groupname }}</label>
          </UFormField>
          <UFormField
            v-if="isCreate"
            name="groupid" class="w-full" label="グループID" required
            :ui="{ label: 'text-lg' }"
          >
            <UInput id="groupid" v-model="state.groupid" class="w-1/2" />
          </UFormField>
          <UFormField
            v-if="!isCreate" name="groupid" class="w-full" label="グループID"
            :ui="{ label: 'text-lg' }"
          >
            <label class="w-full text-left">{{ state.groupid }}</label>
          </UFormField>
          <UFormField
            class="w-full" label="グループを公開する"
            :ui="{ label: 'text-lg' }"
          >
            <USwitch
              v-if="!isDetail"
              :items="items1"
              :default-value="!isEdit"
              legend=""
              class="flex space-x-4"
            />
            <label v-if="isDetail" class="w-full text-left">{{ value1 }}</label>
          </UFormField>
          <UFormField
            class="w-full" label="グループメンバーを公開する" :required="!isDetail"
            :ui="{ label: 'text-lg' }"
          >
            <URadioGroup
              v-if="!isDetail"
              v-model="value3"
              :items="items3"
              legend=""
              class="flex space-x-4"
            />
            <label v-if="isDetail" for="groupname" class="w-full text-left">{{ value3 }}</label>
          </UFormField>
          <UFormField
            v-if="!isDetail" class="w-full" label="グループの接続先" :ui="{ label: 'text-lg' }"
            description="上位グループ・下位グループのどちらかを選択できます"
          >
            <URadioGroup v-model="groupvalue2" :items="items4" />
            <USelectMenu
              v-model="groupvalue"
              class="min-w-1/2 w-auto max-w-full"
              multiple
              :items="groupitems"
            />
          </UFormField>
          <UFormField
            v-if="isDetail" class="w-full" label="グループの接続先"
            :ui="{ label: 'text-lg' }"
          >
            <div class="flex flex-col">
              <label v-if="isConected" class="w-full text-left font-bold">{{ groupvalue2 }}</label>
              <label
                v-for="(item, index) in conectgroups"
                :key="index"
                class="block w-full text-left"
              >
                {{ item }}
              </label>
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
  </UContainer>
</template>
