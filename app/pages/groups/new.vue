<script setup lang="ts">
import type { FormError } from '@nuxt/ui'

const isCreate = true // 実際はパスを見て編集か作成かで判断
const isEdit = false // 実際はパスを見て編集か作成かで判断
const isDetail = false // 実際はパスを見て編集か作成かで判断
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
  if (!state.groupname) errors.push({ name: 'groupname', message: '入力規則に合致しません' })
  if (!state.groupid) errors.push({ name: 'groupid', message: '入力規則に合致しません' })
  return errors
}

const items1 = ref(['公開', '非公開'])
const items3 = ref(['公開', 'メンバーにのみ公開', '非公開'])
const items4 = ref(['上位グループ名', '下位グループ名', '接続しない'])
const groupitems = ref(['jc_xxx_groups_AAA_parent1', 'jc_xxx_groups_AAA_parent2',
  'jc_xxx_groups_AAA_parent3', 'jc_xxx_groups_BBB']) // 実際はmAPで取得したものを表示
const value1 = ref(isCreate ? undefined : '公開') // 実際はmAPで取得したものを表示
const value3 = ref(isCreate ? '非公開' : '公開') // 実際はmAPで取得したものを表示
const groupvalue = ref(isCreate
  ? ['']
  : ['jc_xxx_groups_AAA_parent2',
      'jc_xxx_groups_AAA_parent3']) // 実際はmAPで取得したものを表示
const groupvalue2 = ref(isCreate ? '接続しない' : '上位グループ名') // 実際はmAPで取得したものを表示
const parentgroups = ref([''])
const chaildgroups = ref([''])
if (groupvalue.value != undefined) {
  if (groupvalue2.value == '上位グループ名') {
    parentgroups.value = groupvalue.value
    chaildgroups.value = ['なし']
  }
  else if (groupvalue2.value == '下位グループ名') {
    parentgroups.value = ['なし']
    chaildgroups.value = groupvalue.value
  }
}
const validateGroup = ref(undefined)
if (!isDetail) {
  validateGroup.value = '1文字以上50文字以内'
}
</script>

<template>
  <UContainer class="max-w-3xl py-8">
    <UCard class="mt-6">
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-semibold">
            {{ pageTitle }}
          </h2>
          <div class="flex space-x-4 justify-end">
            <UButton
              v-if="!isDetail" label="キャンセル" color="neutral" variant="soft"
              to="/groups"
            />
            <UButton
              :label="buttonLabel1" class="flex justify-center" color="info" variant="subtle"
              :icon="buttonIcon" to="/groups/1"
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
            <div class="flex flex-col">
              <label class="w-full">USER_A</label>
              <label class="w-full">USER_B</label>
            </div>
          </UFormField>
          <UFormField
            name="groupname" class="w-full" label="グループ名" :required="!isDetail"
            :description="validateGroup"
            :ui="{ label: 'text-lg' }"
          >
            <UInput v-if="!isDetail" id="groupname" v-model="state.groupname" class="w-1/2" />
            <label v-if="isDetail" class="w-full text-left">{{ state.groupname }}</label>
          </UFormField>
          <UFormField
            v-if="isCreate"
            name="groupid" class="w-full" label="グループID" required
            :ui="{ label: 'text-lg' }"
            description="半角英数字と記号(.-_)、4文字以上50文字以内"
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
              legend=""
              :default-value="isEdit"
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
            description="上位グループ・下位グループのどちらかを選択できます" required
          >
            <URadioGroup v-model="groupvalue2" :items="items4" />
            <USelectMenu
              v-model="groupvalue"
              :disabled="groupvalue2 === '接続しない'"
              class="min-w-1/2 w-auto max-w-full"
              multiple
              :items="groupitems"
            />
          </UFormField>
          <UFormField v-if="isDetail" class="w-full" label="グループの接続先">
            <div class="flex flex-col">
              <label class="w-full text-left font-bold text-lg">{{ groupvalue2 }}</label>
              <label
                v-for="(item, index) in parentgroups"
                :key="index"
                class="block w-full text-left"
              >
                {{ item }}
              </label>
              <label
                v-for="(item, index) in chaildgroups"
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
            <div class="flex justify-center gap-4">
              <UButton label="キャンセル" color="neutral" variant="soft" />
              <UButton label="削除" color="error" variant="outline" />
            </div>
          </template>
        </UModal>
      </div>
    </UCard>
  </UContainer>
</template>
