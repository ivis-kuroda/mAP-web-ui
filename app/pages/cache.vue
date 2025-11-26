<script setup lang="ts">
import type { TableColumn, TableRow } from '@nuxt/ui'

import { UButton, UCheckbox, UIcon, ULink } from '#components'

const localePath = useLocalePath()
const { repositories } = useDataStore()
const data = ref<Repository[]>(repositories)
const lastUpdated = ref<string | null>('2025-11-07T00:00:00Z')
const lastUpdatedError = ref<string | null>(null)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const isLoading = ref(false)

// 更新進行状況の管理
const updateProgress = ref(0)
const updateTotal = ref(0)
const completedRepositories = ref<Repository[]>([])

const columnNameMap = {
  displayName: $t('repository.name-column'),
  url: $t('repository.url-column'),
  entityIds: $t('sp-connecter-column'),
} as const

type RepositoryTableColumn = TableColumn<Repository>
const columns = computed<RepositoryTableColumn[]>(() => [
  {
    id: 'select',
    header: ({ table }) =>
      h(UCheckbox, {
        'modelValue': table.getIsSomePageRowsSelected()
          ? 'indeterminate'
          : table.getIsAllPageRowsSelected(),
        'onUpdate:modelValue': value => table.toggleAllPageRowsSelected(!!value),
        'aria-label': 'Select all',
      }),
    cell: ({ row }) =>
      h(UCheckbox, {
        'modelValue': row.getIsSelected(),
        'onUpdate:modelValue': value => row.toggleSelected(!!value),
        'aria-label': 'Select row',
      }),
    enableHiding: false,
  },
  {
    accessorKey: 'id',
    header: ({ column }) => sortableHeader(column, '#'),
  },
  {
    accessorKey: 'displayName',
    header: ({ column }) => sortableHeader(column, columnNameMap.displayName),
    cell: ({ row }) => {
      const name: string = row.original.displayName
      return h(ULink, {
        to: localePath(`/repos/${row.original.id}`),
        class: 'font-bold hover:underline inline-flex items-center',
      }, [
        h('span', name),
      ])
    },
    enableHiding: false,
  },
  {
    accessorKey: 'url',
    header: ({ column }) => sortableHeader(column, columnNameMap.url),
    cell: ({ row }) => {
      const url = row.original.url
      return h(ULink, {
        to: url,
        target: '_blank',
        class: 'hover:underline inline-flex items-center gap-1',
      }, [
        h('span', url),
        h(UIcon, { name: 'i-lucide-external-link', class: 'size-4 shrink-0' }),
      ])
    },
    meta: {},
  },
])

const table = useTemplateRef('table')
const columnVisibility = ref({ id: false })

type Column = Parameters<
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  Extract<RepositoryTableColumn['header'], (...arguments_: any) => any>
>[0]['column']

function sortableHeader(column: Column, label: string) {
  const sortDirection = column.getIsSorted()
  return h(UButton, {
    color: sortDirection ? 'primary' : 'neutral',
    variant: 'ghost',
    size: 'xs',
    label,
    class: 'font-medium cursor-pointer',
    onClick() {
      if (sortDirection === 'asc') column.toggleSorting(true)
      else if (sortDirection === 'desc') column.clearSorting()
      else column.toggleSorting(false)
    },
  })
}

const sorting = ref([{ id: 'id', desc: false }])
const isTableView = ref(true)

const page = ref(1)
const pageSize = ref(20)
const pageOptions = ref([20, 50, 100])

const globalFilter = ref('')
const filteredData = computed(() => {
  if (!globalFilter.value) return data.value
  const f = globalFilter.value.toLowerCase()
  return data.value.filter(
    item =>
      item.displayName.toLowerCase().includes(f)
      || item.url.toLowerCase().includes(f)
      || item.entityIds.toLowerCase().includes(f),
  )
})
const pagedData = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

const displayInfo = computed(() => {
  const total = filteredData.value.length

  if (total === 0) {
    return '0件を表示（全0件）'
  }

  const start = (page.value - 1) * pageSize.value + 1
  const end = Math.min(page.value * pageSize.value, total)

  return $t('table.display-info-text', { start, end, total })
})

const rowSelection = ref<Record<string, boolean>>({})
const selectedRepositories = computed(() => {
  const selectedIds = new Set(Object.entries(rowSelection.value)
    .filter(([, isSelected]) => isSelected)
    .map(([id]) => id))

  return data.value.filter((repositories, index) => selectedIds.has(index.toString()))
})

function onSelect(first: Event | TableRow<Repository>, second: Event | TableRow<Repository>) {
  const row = 'original' in first ? first : second as TableRow<Repository>
  row.toggleSelected(!row.getIsSelected())
}

// 更新処理のシミュレーション関数
async function updateRepositories(repos: Repository[]) {
  isLoading.value = true
  updateTotal.value = repos.length
  updateProgress.value = 0
  completedRepositories.value = []

  for (const [index, repo] of repos.entries()) {
    // 実際の更新処理をここに記述
    await new Promise(resolve => setTimeout(resolve, 3000)) // シミュレーション

    updateProgress.value = index + 1
    completedRepositories.value.push(repo)
  }

  isLoading.value = false
}

async function updateSelected() {
  await updateRepositories(selectedRepositories.value)
}

async function updateAll() {
  await updateRepositories(data.value)
}

// 完了リポジトリのアコーディオンアイテム（単一アイテム）
const completedAccordionItems = computed(() => {
  if (completedRepositories.value.length === 0) return []

  return [{
    label: `更新完了 (${completedRepositories.value.length}件)`,
    icon: 'i-lucide-check-circle',
  }]
})

// 進行率の計算
const progressPercentage = computed(() => {
  if (updateTotal.value === 0) return 0
  return Math.round((updateProgress.value / updateTotal.value) * 100)
})
</script>

<template>
  <UContainer class="max-w-3xl py-8">
    <UCard>
      <template #header>
        <h2 class="text-2xl font-semibold">
          {{ $t('cache.title') }}
        </h2>
      </template>
      <div v-if="!isLoading" class="flex flex-col items-center space-y-6">
        <!-- 更新中は最終更新日時を非表示 -->
        <!-- エラー時 -->
        <div v-if="lastUpdatedError">
          <UAlert
            color="error"
            variant="soft"
            icon="i-lucide-circle-x"
            :title="$t('cache.last-updated-error-title')"
            :ui="{
              root: 'items-center',
              title: 'text-2xl',
              icon: 'size-6',
            }"
          />
        </div>
        <!-- 正常時 -->
        <UFormField
          v-else-if="!isLoading"
          :label="$t('cache.last-updated-date', { lastUpdated: formatDate(lastUpdated) })"
          :ui="{ label: 'text-2xl' }"
        />
      </div>
      <!-- 更新中の表示 -->
      <div v-if="isLoading" class="mt-4 space-y-4">
        <div class="space-y-4">
          <!-- 進行状況テキスト -->
          <div class="text-center">
            <p class="text-lg font-semibold">
              {{ $t('cache.updating') }}
            </p>
            <p class="text-2xl font-bold text-primary mt-2">
              {{ updateProgress }} / {{ updateTotal }} 件
            </p>
          </div>

          <!-- プログレスバー -->
          <UProgress
            :model-value="progressPercentage"
            :max="100"
            size="lg"
            color="primary"
            status
          />

          <!-- 完了したリポジトリのアコーディオン -->
          <div v-if="completedRepositories.length > 0">
            <UAccordion
              :items="completedAccordionItems"
              :ui="{
                item: 'border border-default rounded-lg overflow-hidden bg-default',
                trigger: 'hover:bg-accented/50 transition-colors',
              }"
            >
              <template #body>
                <!-- 5件分の高さ（各アイテム約68px）でスクロール -->
                <div class="max-h-[340px] overflow-y-auto">
                  <div class="divide-y divide-default">
                    <div
                      v-for="(repo, index) in completedRepositories"
                      :key="repo.id"
                      class="flex items-center gap-3 p-3 hover:bg-accented/30 transition-colors"
                    >
                      <UBadge
                        color="success"
                        variant="soft"
                        size="sm"
                        class="shrink-0 font-mono"
                      >
                        {{ index + 1 }}
                      </UBadge>
                      <UIcon name="i-lucide-check-circle-2" class="size-5 text-success shrink-0" />
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium truncate">
                          {{ repo.displayName }}
                        </p>
                        <p class="text-xs text-muted truncate">
                          {{ repo.url }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
            </UAccordion>
          </div>
        </div>
      </div>
    </UCard>

    <!-- 通常表示 -->
    <div v-if="!isLoading">
      <div class="flex justify-end space-x-2 mt-4">
        <UModal
          :title="$t('cache.update-confirmation-title',
                     { count: selectedRepositories.length })"
        >
          <UButton
            :label="$t('cache.updateSelectedRepositories')"
            color="neutral"
            variant="soft"
            :disabled="selectedRepositories.length === 0"
          />
          <template #body>
            <div class="flex flex-col justify-between items-center mt-4">
              <div class="gap-4 text-center">
                <div v-for="repos in selectedRepositories" :key="repos.id" class="mb-2">
                  <p>
                    {{ repos.displayName }}
                  </p>
                </div>
              </div>
            </div>
          </template>
          <template #footer>
            <div class="mt-4 ml-auto space-x-4">
              <UButton :label="$t('modal.cancel-button')" color="neutral" variant="soft" />
              <UButton
                :label="$t('modal.update-button')"
                color="success"
                @click="updateSelected"
              />
            </div>
          </template>
        </UModal>

        <UModal title="全リポジトリの更新を行いますか？">
          <UButton :label="$t('cache.updateAllRepositories')" color="neutral" variant="soft" />
          <template #footer>
            <div class="ml-auto space-x-4">
              <UButton :label="$t('modal.cancel-button')" color="neutral" variant="soft" />
              <UButton
                :label="$t('modal.update-button')"
                color="success"
                @click="updateAll"
              />
            </div>
          </template>
        </UModal>
      </div>

      <div class="flex justify-between mt-8">
        <UInput
          v-model="globalFilter"
          class="max-w-sm"
          placeholder="検索"
          icon="i-lucide-search"
        />

        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-600">表示件数:</span>
          <USelect
            v-model="pageSize"
            :items="pageOptions"
            class="w-24"
          />
        </div>
      </div>

      <div v-if="isTableView">
        <UTable
          ref="table"
          v-model:column-visibility="columnVisibility"
          v-model:sorting="sorting"
          v-model:global-filter="globalFilter"
          v-model:row-selection="rowSelection"
          :data="pagedData"
          :columns="columns"
          @select="onSelect"
        />

        <div class="flex items-center mt-4">
          <div class="flex-1 text-gray-500 text-sm">
            {{ displayInfo }}
          </div>

          <div class="flex-1 flex justify-center">
            <UPagination
              v-model:page="page"
              :items-per-page="pageSize"
              :total="filteredData.length"
            />
          </div>

          <div class="flex-1" />
        </div>
      </div>
    </div>
    <!-- デバッグ用スイッチ（本番では削除） -->
    <USwitch v-model="isLoading" class="mt-10" label="test用" />
    <UButton
      size="xs"
      color="neutral"
      variant="outline"
      label="最終更新日時取得エラー"
      @click="lastUpdatedError = '接続に失敗しました'; lastUpdated = null"
    />
    <UButton
      size="xs"
      color="primary"
      variant="outline"
      label="最終更新日時取得成功"
      @click="lastUpdatedError = null; lastUpdated = '2025-11-07T00:00:00Z'"
    />
  </UContainer>
</template>
