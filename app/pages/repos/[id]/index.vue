<script setup lang="ts">
import { ref } from 'vue'

import { useRoute } from '#imports'

const route = useRoute()
const router = useRouter()

const routeId = computed(() => route.params.id as string)
const mode = computed(() => route.query.mode as string | undefined)

const isAdmin = ref(true) // 仮の管理者判定

const isNew = ref(route.params.id === 'new') // 新規作成モード判定
const isEdit = ref(isNew.value || mode.value === 'edit') // 編集モード判定

// 仮データ（API接続する場合はfetchで置き換え）
const detail = ref({
  serviceName: 'AAA大学リポジトリ',
  serviceUrl: 'https://aaa.repo.nii.ac.jp/',
  entityIds: 'aaa_repo_nii_ac_jp',
  groups: [{}],
  users: [{}],
  suspended: false,
  clientCert: 'client_cert.pem',
  keyFile: 'private_key.pem',
})

// 仮データ（編集時）
// 新規作成時は空で初期化
const form = ref({
  serviceName: isNew.value ? '' : detail.value.serviceName,
  serviceUrl: isNew.value ? '' : detail.value.serviceUrl,
  entityIds: isNew.value ? '' : detail.value.entityIds,
  suspended: isNew.value ? false : detail.value.suspended,
  clientCert: isNew.value ? '' : detail.value.clientCert,
  keyFile: isNew.value ? '' : detail.value.keyFile,
})

// 既存ファイルの有無だけを管理（内容は表示しない）
const existingCertificate = ref<string | null>(null) // ファイル名
const existingPrivateKey = ref<string | null>(null) // ファイル名

const newCertificate = ref<File | null>(null)
const newPrivateKey = ref<File | null>(null)

// 編集時の初期化
onMounted(async () => {
  // const response = await fetch('/api/client-auth/files')
  // const data = awaitresponse.json()
  if (!isNew.value) {
    form.value = detail.value
    existingCertificate.value = 'client_cert.pem'
    // existingPrivateKey.value = 'private_key.pem'
  }

  // existingCertificate.value = 'client_cert.pem'
  // existingPrivateKey.value = 'private_key.pem'
})

// 表示用のファイル情報を計算
const certificateInfo = computed(() => {
  if (newCertificate.value) {
    return {
      name: newCertificate.value.name,
      size: (newCertificate.value.size / 1024).toFixed(1) + ' KB',
      isNew: true,
    }
  }
  if (existingCertificate.value) {
    return {
      name: existingCertificate.value,
      isNew: false,
    }
  }
  return null
})

const privateKeyInfo = computed(() => {
  if (newPrivateKey.value) {
    return {
      name: newPrivateKey.value.name,
      size: (newPrivateKey.value.size / 1024).toFixed(1) + ' KB',
      isNew: true,
    }
  }
  if (existingPrivateKey.value) {
    return {
      name: existingPrivateKey.value,
      isNew: false,
    }
  }
  return null
})

// 保存処理（ダミー）
const onSubmit = () => {
  console.log('送信データ:', form.value)
  // 実際はAPI呼び出し後に詳細へ戻す
  isEdit.value = false
  isNew.value = false
  router.push(`/repos/1`)
}

// キャンセル処理（ダミー）
const onCancel = () => {
  // 実際は詳細画面へ戻す
  router.back()
}

// 削除処理（ダミー）
const onDelete = () => {
  // 実際はAPI呼び出し後に一覧へ戻す
  router.push('/service')
}

const isActive = computed({
  get: () => !form.value.suspended, // 読み取り時の処理
  set: (value) => { form.value.suspended = !value }, // 書き込み時の処理
})

const isOpen = ref(false)

function handleDelete() {
  // ここに削除処理を記述
  console.log('削除しました')
  isOpen.value = false
  onDelete()
}

const repositoryName = computed(() => detail.value.serviceName)
const confirmText = ref('')
const isConfirmed = computed(() => confirmText.value === repositoryName.value)
</script>

<template>
  <UContainer class="max-w-3xl py-8">
    <UPageHeader v-if="!isNew" title="AAA大学リポジトリ" />
    <div v-if="!isNew" class="grid grid-cols-2 gap-4 mb-6">
      <UPageCard
        title="グループ数"
        :description="String(detail.groups.length)"
        icon="i-lucide-users"
        orientation="horizontal"
        to="/groups"
      />
      <UPageCard
        title="ユーザー数"
        :description="String(detail.users.length)"
        icon="i-lucide-user"
        to="/users"
      />
    </div>
    <UCard class="mb-6">
      <!-- カードヘッダー -->
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold">
            {{ isNew ? 'リポジトリ作成' : 'リポジトリ詳細' }}
          </h2>
          <UButton
            v-if="isAdmin && !isEdit"
            label="リポジトリ編集"
            icon="i-lucide-edit"
            variant="subtle"
            color="warning"
            @click="isEdit = true"
          />
          <div v-else-if="isEdit" class="flex justify-end gap-3">
            <UButton
              label="キャンセル"
              color="neutral"
              variant="soft"
              @click="isEdit = false"
            />
            <UButton
              type="submit"
              :label="!isNew ? '保存' : '作成'"
              variant="subtle"
              color="info"
              icon="i-lucide-save"
              @click="onSubmit"
            />
          </div>
        </div>
      </template>

      <!-- 本文 -->
      <div class="space-y-6 mt-2">
        <UFormField label="表示名">
          <div v-if="isEdit">
            <UInput v-model="form.serviceName" class="w-1/2" placeholder="例：AAA大学リポジトリ" />
          </div>
          <div v-else>
            {{ detail.serviceName }}
          </div>
        </UFormField>

        <UFormField label="サイトURL">
          <div v-if="isEdit">
            <UInput v-model="form.serviceUrl" class="w-1/2" placeholder="https://..." />
          </div>
          <ULink
            v-else
            :to="detail.serviceUrl"
            target="_blank"
            class="text-blue-600 underline"
          >
            {{ detail.serviceUrl }}
          </ULink>
        </UFormField>

        <UFormField label="稼働状態">
          <!-- <URadioGroup v-if="isEdit" v-model="form.suspended" :items="statusOptions" /> -->
          <USwitch
            v-if="isEdit"
            v-model="isActive"
            :label="isActive ? '稼働中' : '休止中'"
            :ui="{ label: 'block font-normal text-default' }"
          />
          <UBadge
            v-else
            :color="detail.suspended ? 'error' : 'primary'"
            variant="soft"
          >
            {{ detail.suspended ? '休止中' : '稼働中' }}
          </UBadge>
        </UFormField>

        <UFormField v-if="isAdmin" label="SPコネクタID">
          <UInput v-if="isEdit" v-model="form.entityIds" class="w-1/2" />
          <div v-else>
            {{ detail.entityIds }}
          </div>
        </UFormField>

        <UFormField v-if="isAdmin" label="entityID">
          <UInput v-if="isEdit" v-model="form.entityIds" class="w-1/2" />
          <div v-else>
            {{ detail.entityIds }}
          </div>
        </UFormField>

        <UFormField v-if="isAdmin" label="クライアント証明書">
          <div v-if="!isEdit">
            {{ detail.clientCert ? `登録済 (${detail.clientCert})` : '未登録' }}
          </div>

          <UFileUpload v-else v-model="newCertificate" accept=".crt,.pem">
            <template #default="{ open, removeFile }">
              <!-- ファイルあり（既存 or 新規） -->
              <div v-if="certificateInfo" class="flex items-center gap-3 p-3 border rounded-lg" :class="certificateInfo.isNew ? 'bg-info/10 border-info/20' : 'bg-success/10 border-success/20'">
                <UIcon
                  :name="certificateInfo.isNew ? 'i-lucide-file-plus' : 'i-lucide-file-check'"
                  class="size-5"
                  :class="certificateInfo.isNew ? 'text-info' : 'text-success'"
                />
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium truncate">
                    {{ certificateInfo.name }}
                  </p>
                  <p v-if="certificateInfo.isNew" class="text-xs text-muted">
                    {{ certificateInfo.size }}
                  </p>
                </div>
                <UButton
                  v-if="certificateInfo.isNew"
                  icon="i-lucide-x"
                  color="neutral"
                  variant="ghost"
                  size="sm"
                  @click="removeFile()"
                />
                <UButton
                  v-else
                  label="変更"
                  color="neutral"
                  variant="outline"
                  size="sm"
                  @click="open()"
                />
              </div>

              <!-- ファイルなし -->
              <div v-else class="text-center p-6 border-2 border-dashed border-default rounded-lg hover:border-primary/50 transition-colors cursor-pointer" @click="open()">
                <UIcon name="i-lucide-upload" class="size-8 mx-auto text-muted mb-2" />
                <p class="text-sm font-medium">
                  証明書ファイルをアップロード
                </p>
                <p class="text-xs text-muted mt-1">
                  クリックまたはドラッグ＆ドロップ
                </p>
              </div>
            </template>
          </UFileUpload>
        </UFormField>

        <UFormField v-if="isAdmin" label="秘密鍵">
          <div v-if="!isEdit">
            {{ detail.keyFile ? '登録済' : '未登録' }}
          </div>

          <UFileUpload v-else v-model="newPrivateKey" accept=".key,.pem">
            <template #default="{ open, removeFile }">
              <!-- ファイルあり（既存 or 新規） -->
              <div v-if="privateKeyInfo" class="flex items-center gap-3 p-3 border rounded-lg" :class="privateKeyInfo.isNew ? 'bg-info/10 border-info/20' : 'bg-success/10 border-success/20'">
                <UIcon
                  :name="privateKeyInfo.isNew ? 'i-lucide-file-plus' : 'i-lucide-file-check'"
                  class="size-5"
                  :class="privateKeyInfo.isNew ? 'text-info' : 'text-success'"
                />
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium truncate">
                    {{ privateKeyInfo.name }}
                  </p>
                  <p v-if="privateKeyInfo.isNew" class="text-xs text-muted">
                    {{ privateKeyInfo.size }}
                  </p>
                </div>
                <UButton
                  v-if="privateKeyInfo.isNew"
                  icon="i-lucide-x"
                  color="neutral"
                  variant="ghost"
                  size="sm"
                  @click="removeFile()"
                />
                <UButton
                  v-else
                  label="変更"
                  color="neutral"
                  variant="outline"
                  size="sm"
                  @click="open()"
                />
              </div>

              <!-- ファイルなし -->
              <div v-else class="text-center p-6 border-2 border-dashed border-default rounded-lg hover:border-primary/50 transition-colors cursor-pointer" @click="open()">
                <UIcon name="i-lucide-upload" class="size-8 mx-auto text-muted mb-2" />
                <p class="text-sm font-medium">
                  秘密鍵ファイルをアップロード
                </p>
                <p class="text-xs text-muted mt-1">
                  クリックまたはドラッグ＆ドロップ
                </p>
              </div>
            </template>
          </UFileUpload>
        </UFormField>

        <!-- 上書き警告 -->
        <div v-if="isEdit">
          <UAlert
            v-if="(newCertificate && existingCertificate) || (newPrivateKey && existingPrivateKey)"
            icon="i-lucide-alert-triangle"
            color="warning"
            variant="soft"
            title="ファイルを上書きします"
            description="保存すると既存のファイルが新しいファイルで置き換えられます。"
          />
        </div>
      </div>
      <div class="flex justify-center gap-3 pt-4 ">
        <!-- 削除後は一覧画面に遷移する -->
        <UButton
          v-if="isEdit && !isNew"
          label="リポジトリ削除"
          color="error"
          variant="outline"
          @click="isOpen = true"
        />

        <!-- 確認ダイアログ -->
        <UModal
          v-model:open="isOpen"
          title="リポジトリを削除しますか？"
          description="削除したリポジトリは復元できません。"
          :ui="{ footer: 'justify-end' }"
        >
          <template #body>
            <div class="space-y-3">
              <p class="text-sm text-muted">
                削除を確認するには、以下に
                <span class="font-semibold text-highlighted">{{ repositoryName }}</span>
                と入力してください。
              </p>

              <UInput
                v-model="confirmText"
                placeholder="リポジトリ名を入力"
                class="w-full"
                autofocus
                :color="!isConfirmed ? 'error' : 'primary'"
              />
            </div>
          </template>
          <template #footer="{ close }">
            <UButton
              label="キャンセル"
              color="neutral"
              variant="outline"
              @click="close"
            />
            <UButton
              label="削除"
              color="error"
              @click="handleDelete"
            />
          </template>
        </UModal>
      </div>
    </UCard>

    <div v-if="!isNew" class="flex flex-col sm:flex-row items-center justify-between gap-4 p-6 rounded-lg border border-default">
      <div class="text-center sm:text-left">
        <h3 class="text-lg font-semibold text-default mb-1">
          履歴を確認
        </h3>
        <p class="text-sm text-muted">
          このリポジトリに属するユーザーの変更情報やダウンロード履歴を確認できます
        </p>
      </div>

      <UButton
        trailing-icon="i-lucide-arrow-right"
        size="lg"
        color="primary"
        to="/history"
      >
        履歴を見る
      </UButton>
    </div>
  </UContainer>
</template>
