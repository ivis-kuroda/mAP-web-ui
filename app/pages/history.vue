<script setup lang="ts">
import type { CalendarDate } from '@internationalized/date'
import type { DropdownMenuItem, TabsItem } from '@nuxt/ui'

const UButton = resolveComponent('UButton')
const UBadge = resolveComponent('UBadge')
const UIcon = resolveComponent('UIcon')

const { users, repositories, groups } = useDataStore()

// ダウンロード履歴の型
type DownloadHistory = {
  id: string
  originalDownloadId: string | null
  downloadedAt: string
  downloaderName: string
  userCount: number
  groupCount: number
  isDisabled: boolean
  status: 'completed' | 'processing' | 'failed' | 'canceled'
  downloadType: 'initial' | 'redownload'
  redownloadCount: number
  children?: DownloadHistory[] // 再ダウンロード履歴
  _matchedFields?: string[] // マッチしたフィールドを追跡
}

type SortField = 'downloadedAt' | 'downloaderName' | 'userCount' | 'groupCount' | 'status'
type SortOrder = 'asc' | 'desc'

// サンプルデータ（階層構造）- 多めに追加
const downloadHistories = ref<DownloadHistory[]>([
  {
    id: '1',
    originalDownloadId: null,
    downloadedAt: '2024-03-15T14:30:00',
    downloaderName: '山田太郎',
    userCount: 150,
    groupCount: 4,
    isDisabled: false,
    status: 'completed',
    downloadType: 'initial',
    redownloadCount: 0,
    children: [
      {
        id: '2',
        originalDownloadId: '1',
        downloadedAt: '2024-03-16T10:15:00',
        downloaderName: '山田太郎',
        userCount: 150,
        groupCount: 4,
        status: 'completed',
        downloadType: 'redownload',
        redownloadCount: 1,
        isDisabled: false,
      },
      {
        id: '3',
        originalDownloadId: '1',
        downloadedAt: '2024-03-17T16:45:00',
        downloaderName: '佐藤花子',
        userCount: 150,
        groupCount: 4,
        status: 'completed',
        downloadType: 'redownload',
        redownloadCount: 2,
        isDisabled: false,
      },
      {
        id: '8',
        originalDownloadId: '1',
        downloadedAt: '2024-03-18T11:20:00',
        downloaderName: '田中美咲',
        userCount: 150,
        groupCount: 4,
        status: 'completed',
        downloadType: 'redownload',
        redownloadCount: 3,
        isDisabled: false,
      },
      {
        id: '9',
        originalDownloadId: '1',
        downloadedAt: '2024-03-19T15:30:00',
        downloaderName: '鈴木一郎',
        userCount: 150,
        groupCount: 4,
        status: 'completed',
        downloadType: 'redownload',
        redownloadCount: 4,
        isDisabled: false,
      },
    ],
  },
  {
    id: '4',
    originalDownloadId: null,
    downloadedAt: '2024-03-14T10:15:00',
    downloaderName: '佐藤花子',
    userCount: 200,
    groupCount: 6,
    status: 'canceled',
    downloadType: 'initial',
    redownloadCount: 0,
    isDisabled: false,
  },
  {
    id: '5',
    originalDownloadId: null,
    downloadedAt: '2024-03-13T16:45:00',
    downloaderName: '鈴木一郎',
    userCount: 180,
    groupCount: 2,
    status: 'completed',
    downloadType: 'initial',
    redownloadCount: 0,
    isDisabled: false,
    children: [
      {
        id: '6',
        originalDownloadId: '5',
        downloadedAt: '2024-03-14T09:20:00',
        downloaderName: '鈴木一郎',
        userCount: 180,
        groupCount: 2,
        status: 'completed',
        downloadType: 'redownload',
        redownloadCount: 1,
        isDisabled: false,
      },
    ],
  },
  {
    id: '7',
    originalDownloadId: null,
    downloadedAt: '2024-03-12T09:20:00',
    downloaderName: '田中美咲',
    userCount: 165,
    groupCount: 8,
    status: 'completed',
    downloadType: 'initial',
    redownloadCount: 0,
    isDisabled: false,
  },
  {
    id: '10',
    originalDownloadId: null,
    downloadedAt: '2024-03-11T14:30:00',
    downloaderName: '高橋誠',
    userCount: 190,
    groupCount: 5,
    status: 'failed',
    downloadType: 'initial',
    redownloadCount: 0,
    isDisabled: false,
  },
  {
    id: '11',
    originalDownloadId: null,
    downloadedAt: '2024-03-10T10:15:00',
    downloaderName: '伊藤舞',
    userCount: 210,
    groupCount: 7,
    status: 'completed',
    downloadType: 'initial',
    redownloadCount: 0,
    isDisabled: false,
  },
  {
    id: '12',
    originalDownloadId: null,
    downloadedAt: '2024-03-09T16:45:00',
    downloaderName: '渡辺健太',
    userCount: 175,
    groupCount: 3,
    status: 'completed',
    downloadType: 'initial',
    redownloadCount: 0,
    isDisabled: false,
  },
  {
    id: '13',
    originalDownloadId: null,
    downloadedAt: '2024-03-08T09:20:00',
    downloaderName: '中村優子',
    userCount: 195,
    groupCount: 4,
    status: 'completed',
    downloadType: 'initial',
    redownloadCount: 0,
    isDisabled: true,
  },
  {
    id: '14',
    originalDownloadId: null,
    downloadedAt: '2024-03-07T14:30:00',
    downloaderName: '小林修',
    userCount: 185,
    groupCount: 6,
    status: 'completed',
    downloadType: 'initial',
    redownloadCount: 0,
    isDisabled: true,
  },
])

const isAdmin = ref(true)

// タブのアイテム
const tabItems: TabsItem[] = [
  {
    label: 'ダウンロード履歴',
    icon: 'i-lucide-download',
    slot: 'download',
  },
  {
    label: 'アップロード履歴',
    icon: 'i-lucide-upload',
    slot: 'upload',
  },
]

// 検索フィルター
const searchQuery = ref('')
const dateFrom = ref('')
const dateTo = ref('')

const dateRange = ref<{ start?: CalendarDate, end?: CalendarDate }>({})

const formattedDateRange = computed(() => {
  if (!dateRange.value.start && !dateRange.value.end) return ''

  const format = (d?: CalendarDate) =>
    d
      ? `${d.year}/${String(d.month).padStart(2, '0')}/${String(d.day).padStart(2, '0')}`
      : ''

  if (dateRange.value.start && dateRange.value.end) {
    return `${format(dateRange.value.start)} ~ ${format(dateRange.value.end)}`
  }

  return format(dateRange.value.start) || format(dateRange.value.end)
})

function resetDateRange() {
  dateRange.value = {}
}

const userNames = ref(users.map(user => user.displayName))
const userGroupNames = ref(groups.map(group => group.displayName))
const repositoryNames = ref(repositories.map(repo => repo.displayName))

// ソート設定
const sortField = ref<SortField>('downloadedAt')
const sortOrder = ref<SortOrder>('desc')

// ページネーション設定
const currentPage = ref(1)
const itemsPerPage = ref(10)

// 表示件数オプション
const itemsPerPageOptions = [
  { label: '10件', value: 10 },
  { label: '20件', value: 20 },
  { label: '50件', value: 50 },
  { label: '100件', value: 100 },
]

// 展開状態の管理
const expandedRows = ref<Set<string>>(new Set())

function toggleExpand(id: string) {
  if (expandedRows.value.has(id)) {
    expandedRows.value.delete(id)
  }
  else {
    expandedRows.value.add(id)
  }
}

// 検索にマッチしたグループを自動展開
watch([searchQuery, dateRange], () => {
  if (searchQuery.value || dateRange.value.start || dateRange.value.end) {
    const matched = new Set<string>()
    for (const parent of downloadHistories.value) {
      if (parent.children) {
        const hasMatchedChild = parent.children.some((child) => {
          const query = searchQuery.value.toLowerCase()
          const nameMatch = child.downloaderName.toLowerCase().includes(query)
          const dateMatch = formatDateForSearch(child.downloadedAt).toLowerCase().includes(query)
          const dateRangeMatch = isDateInRange(child.downloadedAt)

          return (nameMatch || dateMatch) && dateRangeMatch
        })

        if (hasMatchedChild) {
          matched.add(parent.id)
        }
      }
    }
    expandedRows.value = matched
  }
})

// ページ変更時にページトップにスクロール
watch(currentPage, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

// ソートを切り替え
function toggleSort(field: SortField) {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  }
  else {
    sortField.value = field
    sortOrder.value = 'desc'
  }
}

// ソートアイコンを取得
function getSortIcon(field: SortField) {
  if (sortField.value !== field) return 'i-lucide-arrow-up-down'
  return sortOrder.value === 'asc' ? 'i-lucide-arrow-up' : 'i-lucide-arrow-down'
}

// データをソート
function sortData(data: DownloadHistory[]): DownloadHistory[] {
  const sorted = [...data].sort((a, b) => {
    let comparison = 0

    switch (sortField.value) {
      case 'downloadedAt': {
        comparison = new Date(a.downloadedAt).getTime() - new Date(b.downloadedAt).getTime()
        break
      }
      // case 'downloaderName': {
      //   comparison = a.downloaderName.localeCompare(b.downloaderName, 'ja')
      //   break
      // }
      // case 'userCount': {
      //   comparison = a.userCount - b.userCount
      //   break
      // }
      // case 'groupCount': {
      //   comparison = a.groupCount - b.groupCount
      //   break
      // }
      // case 'status': {
      //   const statusOrder = ['completed', 'processing', 'failed', 'canceled']
      //   comparison = statusOrder.indexOf(a.status) - statusOrder.indexOf(b.status)
      //   break
      // }
    }

    return sortOrder.value === 'asc' ? comparison : -comparison
  })

  return sorted.map((parent) => {
    if (parent.children && parent.children.length > 0) {
      return {
        ...parent,
        children: sortData(parent.children),
      }
    }
    return parent
  })
}

// 日時を比較用の文字列に変換
function formatDateForSearch(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 日時の範囲チェック
function isDateInRange(dateString: string): boolean {
  if (!dateRange.value.start && !dateRange.value.end) return true

  const date = new Date(dateString)
  const from = dateRange.value.start ? new Date(dateRange.value.start) : null
  const to = dateRange.value.end ? new Date(dateRange.value.end) : null
  if (from && date < from) return false
  if (to) {
    const toEnd = new Date(to)
    toEnd.setHours(23, 59, 59, 999)
    if (date > toEnd) return false
  }

  return true
}

// 項目が検索条件にマッチするかチェック
function checkMatch(item: DownloadHistory): string[] {
  const matched: string[] = []
  const query = searchQuery.value.toLowerCase()

  if (!query && !dateRange.value.start && !dateRange.value.end) {
    return matched
  }

  if (query && item.downloaderName.toLowerCase().includes(query)) {
    matched.push('name')
  }

  if (query && formatDateForSearch(item.downloadedAt).toLowerCase().includes(query)) {
    matched.push('date')
  }

  if ((dateRange.value.start || dateRange.value.end) && isDateInRange(item.downloadedAt) && !matched.includes('date')) {
    matched.push('date')
  }

  return matched
}

// フィルタリング & ソート（ページネーション前）
const filteredAndSortedData = computed(() => {
  const isSearching = searchQuery.value || dateRange.value.start || dateRange.value.end

  let result = downloadHistories.value.map((parent) => {
    const childrenWithMatch = parent.children?.map(child => ({
      ...child,
      _matchedFields: checkMatch(child),
    })) || []

    // 検索中だけ、ヒットした子だけ残す
    const filteredChildren = isSearching
      ? childrenWithMatch.filter(child => child._matchedFields?.length > 0)
      : childrenWithMatch

    return {
      ...parent,
      _matchedFields: checkMatch(parent),
      children: filteredChildren,
    }
  })

  // 検索中のみ、親単位のフィルタも実行
  if (isSearching) {
    result = result.filter((parent) => {
      const parentMatched = parent._matchedFields?.length > 0
      const childMatched = parent.children?.length > 0
      return parentMatched || childMatched
    })
  }

  return sortData(result)
})

// ページネーション適用後のデータ
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredAndSortedData.value.slice(start, end)
})

// 総件数
const totalItems = computed(() => filteredAndSortedData.value.length)

// 総ページ数
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))

// マッチした件数をカウント
const matchedCount = computed(() => {
  let count = 0
  for (const parent of filteredAndSortedData.value) {
    if (parent._matchedFields && parent._matchedFields.length > 0) {
      count++
    }
    if (parent.children) {
      for (const child of parent.children) {
        if (child._matchedFields && child._matchedFields.length > 0) {
          count++
        }
      }
    }
  }
  return count
})

// フィルターをリセット
function resetFilters() {
  searchQuery.value = ''
  resetDateRange()
  currentPage.value = 1
}

// フィルターが適用されているか
const hasActiveFilters = computed(() => {
  return !!(searchQuery.value || dateRange.value.start || dateRange.value.end)
})

// 表示件数変更時はページを1に戻す
watch(itemsPerPage, () => {
  currentPage.value = 1
})

// フィルター変更時もページを1に戻す
watch([searchQuery, dateRange], () => {
  currentPage.value = 1
})

const toast = useToast()

function handleRedownload(history: DownloadHistory) {
  toast.add({
    title: '再ダウンロード開始',
    description: `${history.userCount}人分のユーザーデータをダウンロードしています`,
    color: 'info',
  })
}

// 統計情報
const totalDownloads = computed(() => downloadHistories.value.length)
const initialDownloads = computed(() => downloadHistories.value.filter(h => h.downloadType === 'initial').length)
const redownloadCount = computed(() => {
  let count = 0
  for (const h of downloadHistories.value) {
    if (h.downloadType === 'redownload') count++
    if (h.children && Array.isArray(h.children)) {
      count += h.children.filter(child => child.downloadType === 'redownload').length
    }
  }
  return count
})
// アップロード履歴のサンプルデータ

const totalUploads = computed(() => 10) // 仮の値
const successCount = computed(() => 8) // 仮の値
const failureCount = computed(() => 2) // 仮の値
const latestUploadDate = computed(() => {
  if (downloadHistories.value.length === 0) {
    return '-'
  }

  const latest = downloadHistories.value.reduce((previous, current) => {
    return new Date(current.downloadedAt) > new Date(previous.downloadedAt) ? current : previous
  })

  const date = new Date(latest.downloadedAt)
  return date.toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
})

const totalUsers = computed(() => {
  // 重複を除いた総ユーザー数を計算
  const uniqueSnapshots = new Set(downloadHistories.value.map(h => h.dataSnapshotDate))
  return downloadHistories.value
    .filter(h => h.downloadType === 'initial')
    .reduce((sum, h) => sum + h.userCount, 0)
})

// ステータス設定
const statusConfig = {
  completed: { label: '完了', color: 'success' as const },
  processing: { label: '処理中', color: 'info' as const },
  failed: { label: '失敗', color: 'error' as const },
  canceled: { label: 'キャンセル', color: 'warning' as const },
}

// アクションメニューの項目
function getDropdownActions(history: DownloadHistory, type: string): DropdownMenuItem[] {
  const actions: DropdownMenuItem[] = []
  if (type === 'upload') {
    actions.push({
      label: '詳細を表示',
      icon: 'i-lucide-arrow-right',
      to: `/upload/1`,
    })
  }
  actions.push(
    {
      label: '履歴IDをコピー',
      icon: 'i-lucide-clipboard-copy',
    },
    {
      label: '履歴を非公開',
      icon: 'i-lucide-eye-off',
    },
  )
  return actions
}
function generateRandomChecksum() {
  const chars = '0123456789abcdef'
  let checksum = ''
  for (let index = 0; index < 8; index++) {
    checksum += chars[Math.floor(Math.random() * chars.length)]
  }
  return checksum
}
</script>

<template>
  <div class="min-h-screen bg-default">
    <!-- ヘッダー -->
    <div class="bg-elevated border-b border-default mb-6">
      <div class="container mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-highlighted">
              履歴
            </h1>
            <p class="mt-1 text-sm text-muted">
              ユーザー一覧の履歴を確認・管理できます
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- タブ切り替え -->
    <!-- <UTabs
      :items="tabItems"
      class="w-full"
      variant="pill"
      :ui="{
        root: 'gap-0',
        list: 'bg-transparent! p-0! gap-0 border-none! mb-0!',
        trigger: 'rounded-t-lg rounded-b-none! border! border-b-0! border-gray-300 bg-gray-100! data-[state=active]:bg-white! data-[state=active]:border-gray-300! data-[state=active]:z-10 data-[state=active]:text-gray-900! data-[state=inactive]:border-gray-200 hover:data-[state=inactive]:bg-gray-200! px-6',
        indicator: 'hidden!',
        content: 'border! border-gray-300 rounded-b-lg rounded-tr-lg bg-white! p-4! -mt-px',
      }"
    > -->
    <UTabs
      :items="tabItems" class="w-full" variant="link"
      :ui="{
        trigger: 'min-w-50',
      }"
    >
      <template #download>
        <div class="container mx-auto px-6 py-6">
          <!-- 統計カード -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <UCard variant="outline">
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-lg bg-primary/10">
                  <UIcon name="i-lucide-download" class="size-6 text-primary" />
                </div>
                <div>
                  <p class="text-sm text-muted">
                    総ダウンロード数
                  </p>
                  <p class="text-2xl font-bold text-highlighted">
                    {{ totalDownloads }}
                  </p>
                </div>
              </div>
            </UCard>

            <UCard variant="outline">
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-lg bg-success/10">
                  <UIcon name="i-lucide-file-check" class="size-6 text-success" />
                </div>
                <div>
                  <p class="text-sm text-muted">
                    初回ダウンロード
                  </p>
                  <p class="text-2xl font-bold text-highlighted">
                    {{ initialDownloads }}
                  </p>
                </div>
              </div>
            </UCard>

            <UCard variant="outline">
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-lg bg-info/10">
                  <UIcon name="i-lucide-refresh-cw" class="size-6 text-info" />
                </div>
                <div>
                  <p class="text-sm text-muted">
                    再ダウンロード
                  </p>
                  <p class="text-2xl font-bold text-highlighted">
                    {{ redownloadCount }}
                  </p>
                </div>
              </div>
            </UCard>

            <!-- <UCard variant="outline">
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-lg bg-warning/10">
                  <UIcon name="i-lucide-users" class="size-6 text-warning" />
                </div>
                <div>
                  <p class="text-sm text-muted">
                    総ユーザー数
                  </p>
                  <p class="text-2xl font-bold text-highlighted">
                    {{ totalUsers.toLocaleString() }}
                  </p>
                </div>
              </div>
            </UCard> -->
          </div>

          <!-- フィルター -->
          <UCard variant="outline" class="mb-6">
            <template #header>
              <div class="flex items-center justify-between">
                <h2 class="text-xl font-semibold text-highlighted">
                  フィルター
                </h2>
                <UButton
                  v-if="hasActiveFilters"
                  label="リセット"
                  icon="i-lucide-x"
                  color="neutral"
                  variant="ghost"
                  size="xs"
                  @click="resetFilters"
                />
              </div>
            </template>

            <UFormField
              label="実行条件"
              class="mb-4"
            >
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <UPopover>
                  <UInput
                    icon="i-lucide-calendar"
                    placeholder="ダウンロード日時"
                    :model-value="formattedDateRange"
                    :ui="{ base: 'text-left' }"
                    readonly
                  />
                  <template #content>
                    <UCalendar v-model="dateRange" :number-of-months="2" class="p-2" range />
                  </template>
                </UPopover>
                <USelectMenu
                  placeholder="実行ユーザー"
                  icon="i-lucide-user" :items="userNames" multiple
                />
              </div>
            </UFormField>

            <UFormField label="ダウンロード対象">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <USelectMenu
                  placeholder="リポジトリ"
                  icon="i-lucide-folder" :items="repositoryNames" multiple
                />
                <USelectMenu
                  placeholder="グループ"
                  icon="i-lucide-users" :items="userGroupNames" multiple
                />
                <USelectMenu
                  placeholder="ユーザー"
                  icon="i-lucide-user" :items="userNames" multiple
                />
              </div>
            </UFormField>
          </UCard>

          <!-- テーブル -->
          <UCard variant="outline">
            <template #header>
              <div class="flex items-center justify-between">
                <h2 class="text-xl font-semibold text-highlighted">
                  履歴一覧
                </h2>
                <div class="flex items-center gap-3">
                  <!-- <div class="flex items-center gap-2">
                    <UBadge
                      v-if="hasActiveFilters && matchedCount > 0"
                      :label="`${matchedCount}件ヒット`"
                      color="success"
                      variant="soft"
                    />
                  </div> -->
                  <div class="flex items-center gap-2">
                    <span class="text-md text-muted">表示件数:</span>
                    <USelectMenu
                      v-model="itemsPerPage"
                      :items="itemsPerPageOptions"
                      value-key="value"
                      size="md"
                      class="w-24"
                      :search-input="false"
                    />
                  </div>
                </div>
              </div>
            </template>

            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-default">
                <!-- ヘッダー行 -->
                <thead>
                  <tr>
                    <th class="w-12 px-4 py-3.5" />
                    <th class="px-4 py-3.5 text-left">
                      <UButton
                        color="neutral"
                        variant="ghost"
                        class="font-semibold -mx-2"
                        :icon="getSortIcon('downloadedAt')"
                        @click="toggleSort('downloadedAt')"
                      >
                        ダウンロード日時
                      </UButton>
                    </th>
                    <th class="px-4 py-3.5 text-left text-sm">
                      <!-- <UButton
                    color="neutral"
                    variant="ghost"
                    class="font-semibold -mx-2"
                    :icon="getSortIcon('downloaderName')"
                    @click="toggleSort('downloaderName')"
                  >
                    ダウンロード者
                  </UButton> -->
                      ダウンロード者
                    </th>
                    <th class="px-4 py-3.5 text-left text-sm">
                      <!-- <UButton
                    color="neutral"
                    variant="ghost"
                    class="font-semibold -mx-2"
                    :icon="getSortIcon('userCount')"
                    @click="toggleSort('userCount')"
                  >
                    ユーザー数
                  </UButton> -->
                      ユーザー数
                    </th>
                    <th class="px-4 py-3.5 text-left text-sm">
                      <!-- <UButton
                    color="neutral"
                    variant="ghost"
                    class="font-semibold -mx-2"
                    :icon="getSortIcon('groupCount')"
                    @click="toggleSort('groupCount')"
                  >
                    グループ数
                  </UButton> -->
                      グループ数
                    </th>
                    <!-- <th class="px-4 py-3.5 text-left text-sm">
                      <UButton
                    color="neutral"
                    variant="ghost"
                    class="font-semibold -mx-2"
                    :icon="getSortIcon('status')"
                    @click="toggleSort('status')"
                  >
                    ステータス
                  </UButton>
                      ステータス
                    </th> -->
                    <th class="px-4 py-3.5 text-left text-sm">
                      操作
                    </th>
                    <th />
                  </tr>
                </thead>
                <!-- データ行 -->
                <tbody class="divide-y divide-default">
                  <template v-for="parent in paginatedData" :key="parent.id">
                    <!-- 親行 -->
                    <tr
                      class="hover:bg-elevated/50 transition-colors"
                      :class="{
                        // 'bg-elevated/25': expandedRows.has(parent.id),
                        // 'ring-2 ring-inset ring-success/30 bg-success/5': parent._matchedFields && parent._matchedFields.length > 0,
                        'bg-success/5': parent._matchedFields && parent._matchedFields.length > 0,
                      }"
                    >
                      <!--  -->
                      <td class="px-4 py-3">
                        <div class="flex items-center gap-1">
                          <UIcon
                            v-if="parent._matchedFields && parent._matchedFields.length > 0"
                            name="i-lucide-search-check"
                            class="size-4 text-success shrink-0"
                          />
                          <UButton
                            v-if="parent.children && parent.children.length > 0"
                            :icon="expandedRows.has(parent.id) ? 'i-lucide-chevron-down' : 'i-lucide-chevron-right'"
                            color="neutral"
                            variant="ghost"
                            size="xs"
                            square
                            @click="toggleExpand(parent.id)"
                          />
                        </div>
                      </td>
                      <!-- ダウンロード日時 -->
                      <td class="px-4 py-3 text-sm">
                        <span :class="{ 'font-semibold text-success': parent._matchedFields?.includes('date') }">
                          {{ new Date(parent.downloadedAt).toLocaleString('ja-JP', {
                            year: 'numeric',
                            month: '2-digit',
                            day: '2-digit',
                            hour: '2-digit',
                            minute: '2-digit',
                          }) }}
                        </span>
                      </td>
                      <!-- ダウンロード者 -->
                      <td class="px-4 py-3 text-sm">
                        <div class="flex items-center gap-2">
                          <span :class="{ 'font-semibold text-success': parent._matchedFields?.includes('name') }">
                            {{ parent.downloaderName }}
                          </span>
                          <UBadge
                            v-if="parent.children && parent.children.length > 0"
                            :label="`+${parent.children.length}`"
                            color="neutral"
                            size="xs"
                            variant="subtle"
                          />
                        </div>
                      </td>
                      <!-- ユーザー数 -->
                      <td class="px-4 py-3 text-sm">
                        <UPopover :content="{ align: 'start' }">
                          <UButton
                            color="neutral"
                            variant="ghost"
                            size="xs"
                            :label="`${parent.userCount}人`"
                            trailing-icon="i-lucide-chevron-down"
                            class="font-normal"
                          />

                          <template #content>
                            <div class="w-72 max-h-80">
                              <!-- リスト -->
                              <div class="max-h-60 overflow-y-auto">
                                <div
                                  v-for="(user, index) in users.slice(0, parent.userCount)"
                                  :key="user.id"
                                  class="px-4 py-2.5 hover:bg-elevated/50 transition-colors"
                                  :class="{ 'border-b border-default': index < parent.userCount - 1 }"
                                >
                                  <div class="flex items-center gap-2">
                                    <!-- <UIcon name="i-lucide-user" class="size-4 text-muted shrink-0" /> -->
                                    <span class="text-sm text-default truncate">{{ user.displayName }}</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </template>
                        </UPopover>
                      </td>
                      <!-- グループ数 -->
                      <td class="px-4 py-3 text-sm">
                        <UPopover :content="{ align: 'start' }">
                          <UButton
                            color="neutral"
                            variant="ghost"
                            size="xs"
                            :label="`${parent.groupCount}グループ`"
                            trailing-icon="i-lucide-chevron-down"
                            class="font-normal"
                          />

                          <template #content>
                            <div class="w-72 max-h-80">
                              <!-- リスト -->
                              <div class="max-h-60 overflow-y-auto">
                                <div
                                  v-for="(group, index) in groups.slice(0, parent.groupCount)"
                                  :key="group.id"
                                  class="px-4 py-2.5 hover:bg-elevated/50 transition-colors"
                                  :class="{ 'border-b border-default': index < parent.groupCount - 1 }"
                                >
                                  <div class="flex items-center gap-2">
                                    <!-- <UIcon name="i-lucide-users" class="size-4 text-muted shrink-0" /> -->
                                    <span class="text-sm text-default truncate">{{ group.displayName }}</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </template>
                        </UPopover>
                      </td>
                      <!-- ステータス -->
                      <!-- <td class="px-4 py-3 text-sm">
                        <UBadge
                          :label="statusConfig[parent.status]?.label"
                          :color="statusConfig[parent.status]?.color"
                          variant="subtle"
                        />
                      </td> -->
                      <!-- 操作 -->
                      <td class="px-4 py-3 flex items-center gap-2">
                        <UButton
                          v-if="!parent.isDisabled"
                          label="再ダウンロード"
                          icon="i-lucide-download"
                          color="primary"
                          variant="outline"
                          size="sm"
                          @click="handleRedownload(parent)"
                        />
                        <UButton
                          v-else
                          label="期限切れ"
                          icon="i-lucide-clock-alert"
                          color="neutral"
                          variant="outline"
                          size="sm"
                          disabled
                          @click="handleRedownload(parent)"
                        />
                      </td>
                      <!-- action -->
                      <td>
                        <UDropdownMenu :items="getDropdownActions(parent)">
                          <UButton
                            icon="i-lucide-ellipsis-vertical"
                            color="neutral"
                            variant="ghost"
                            aria-label="Actions"
                          />
                          <template #checksum="{ item }">
                            <UTooltip :text="generateRandomChecksum()" placement="left">
                              <span class="flex items-center gap-2 cursor-help text-gray-700">
                                <UIcon name="i-lucide-hash" class="w-4 h-4 text-gray-500" />
                                チェックサムを確認
                              </span>
                            </UTooltip>
                          </template>
                        </UDropdownMenu>
                      </td>
                    </tr>

                    <!-- 子行（展開時） -->
                    <template v-if="expandedRows.has(parent.id) && parent.children">
                      <tr
                        v-for="child in parent.children"
                        :key="child.id"
                        class="hover:bg-elevated/50 transition-colors"
                        :class="{
                          'bg-elevated/10': !(child._matchedFields && child._matchedFields.length > 0),
                          // 'bg-elevated/25': !(child._matchedFields && child._matchedFields.length > 0),
                          // 'ring-2 ring-inset ring-success/30 bg-success/5': child._matchedFields && child._matchedFields.length > 0,
                          'bg-success/5': child._matchedFields && child._matchedFields.length > 0,
                        }"
                      >
                        <!--  -->
                        <td class="px-4 py-3">
                          <UIcon
                            v-if="child._matchedFields && child._matchedFields.length > 0"
                            name="i-lucide-search-check"
                            class="size-4 text-success"
                          />
                        </td>
                        <!-- ダウンロード日時 -->
                        <td class="px-4 py-3 text-sm">
                          <div class="flex items-center gap-2">
                            <UIcon name="i-lucide-corner-down-right" class="size-4 text-muted" />
                            <!-- <span :class="{ 'font-semibold text-success': child._matchedFields?.includes('date') }"> -->
                            <span>
                              {{ new Date(child.downloadedAt).toLocaleString('ja-JP', {
                                year: 'numeric',
                                month: '2-digit',
                                day: '2-digit',
                                hour: '2-digit',
                                minute: '2-digit',
                              }) }}
                            </span>
                          </div>
                        </td>
                        <!-- ダウンロード者 -->
                        <td class="px-4 py-3 text-sm">
                          <div class="flex items-center gap-2">
                            <UBadge
                              :label="`再DL ${child.redownloadCount}回目`"
                              color="info"
                              size="xs"
                            />
                            <span :class="{ 'font-semibold text-success': child._matchedFields?.includes('name') }">
                              {{ child.downloaderName }}
                            </span>
                          </div>
                        </td>
                        <!-- ユーザー数 -->
                        <td class="px-4 py-3 text-sm">
                          <!-- <UPopover :content="{ align: 'start' }">
                            <UButton
                              color="neutral"
                              variant="ghost"
                              size="xs"
                              :label="`${child.userCount}人`"
                              trailing-icon="i-lucide-chevron-down"
                              class="font-normal"
                            />

                            <template #content>
                              <div class="w-72 max-h-80">
                                <div class="max-h-60 overflow-y-auto">
                                  <div
                                    v-for="(user, index) in users.slice(0, child.userCount)"
                                    :key="user.id"
                                    class="px-4 py-2.5 hover:bg-elevated/50 transition-colors"
                                    :class="{ 'border-b border-default': index < child.userCount - 1 }"
                                  >
                                    <div class="flex items-center gap-2">
                                      <span class="text-sm text-default truncate">{{ user.displayName }}</span>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </template>
                          </UPopover> -->
                        </td>
                        <!-- グループ数 -->
                        <td class="px-4 py-3 text-sm">
                          <!-- <UPopover :content="{ align: 'start' }">
                            <UButton
                              color="neutral"
                              variant="ghost"
                              size="xs"
                              :label="`${child.groupCount}グループ`"
                              trailing-icon="i-lucide-chevron-down"
                              class="font-normal"
                            />

                            <template #content>
                              <div class="w-72 max-h-80">

                                <div class="max-h-60 overflow-y-auto">
                                  <div
                                    v-for="(group, index) in groups.slice(0, child.groupCount)"
                                    :key="group.id"
                                    class="px-4 py-2.5 hover:bg-elevated/50 transition-colors"
                                    :class="{ 'border-b border-default': index < child.groupCount - 1 }"
                                  >
                                    <div class="flex items-center gap-2">
                                      <span class="text-sm text-default truncate">{{ group.displayName }}</span>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </template>
                          </UPopover> -->
                        </td>
                        <!-- ステータス -->
                        <!-- <td class="px-4 py-3 text-sm">
                          <UBadge
                            :label="statusConfig[child.status]?.label"
                            :color="statusConfig[child.status]?.color"
                            variant="subtle"
                          />
                        </td> -->
                        <!-- 操作 -->
                        <td class="px-4 py-3">
                          <!-- <UButton
                            label="再ダウンロード"
                            icon="i-lucide-download"
                            color="neutral"
                            variant="ghost"
                            size="sm"
                            @click="handleRedownload(child)"
                          /> -->
                        </td>
                        <!-- action -->
                        <td>
                          <UDropdownMenu :items="getDropdownActions(child)">
                            <UButton
                              icon="i-lucide-ellipsis-vertical"
                              color="neutral"
                              variant="ghost"
                              aria-label="Actions"
                            />
                          </UDropdownMenu>
                        </td>
                      </tr>
                    </template>
                  </template>
                </tbody>
              </table>

              <!-- データがない場合 -->
              <div v-if="paginatedData.length === 0" class="text-center py-12 text-muted">
                <UIcon name="i-lucide-search-x" class="size-12 mx-auto mb-3 opacity-50" />
                <p>検索条件に一致するデータが見つかりませんでした</p>
              </div>
            </div>

            <!-- ページネーション -->
            <template #footer>
              <div class="flex items-center">
                <div class="flex-1 text-sm text-muted">
                  {{ ((currentPage - 1) * itemsPerPage) + 1 }}〜{{ Math.min(currentPage * itemsPerPage, totalItems) }} / {{ totalItems }}件
                </div>
                <UPagination
                  v-model:page="currentPage"
                  :total="totalItems"
                  :items-per-page="itemsPerPage"
                  :sibling-count="1"
                  show-edges
                  class="flex-2 flex justify-center"
                />
                <div class="flex-1" />
              </div>
            </template>
          </UCard>
        </div>
      </template>

      <!-- アップロードタブ -->
      <template #upload>
        <div class="container mx-auto px-6 py-6">
          <!-- 統計カード -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <UCard variant="outline">
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-lg bg-primary/10">
                  <UIcon name="i-lucide-upload" class="size-6 text-primary" />
                </div>
                <div>
                  <p class="text-sm text-muted">
                    総アップロード数
                  </p>
                  <p class="text-2xl font-bold text-highlighted">
                    {{ totalUploads }}
                  </p>
                </div>
              </div>
            </UCard>

            <UCard variant="outline">
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-lg bg-success/10">
                  <UIcon name="i-lucide-check-circle" class="size-6 text-success" />
                </div>
                <div>
                  <p class="text-sm text-muted">
                    成功件数
                  </p>
                  <p class="text-2xl font-bold text-highlighted">
                    {{ successCount }}
                  </p>
                </div>
              </div>
            </UCard>

            <UCard variant="outline">
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-lg bg-error/10">
                  <UIcon name="i-lucide-x-circle" class="size-6 text-error" />
                </div>
                <div>
                  <p class="text-sm text-muted">
                    失敗件数
                  </p>
                  <p class="text-2xl font-bold text-highlighted">
                    {{ failureCount }}
                  </p>
                </div>
              </div>
            </UCard>

            <!-- <UCard variant="outline">
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-lg bg-info/10">
                  <UIcon name="i-lucide-clock" class="size-6 text-info" />
                </div>
                <div>
                  <p class="text-sm text-muted">
                    最新アップロード日時
                  </p>
                  <p class="text-lg font-bold text-highlighted">
                    {{ latestUploadDate }}
                  </p>
                </div>
              </div>
            </UCard> -->
          </div>

          <!-- フィルター -->
          <UCard variant="outline" class="mb-6">
            <template #header>
              <div class="flex items-center justify-between">
                <h2 class="text-xl font-semibold text-highlighted">
                  フィルター
                </h2>
                <UButton
                  v-if="hasActiveFilters"
                  label="リセット"
                  icon="i-lucide-x"
                  color="neutral"
                  variant="ghost"
                  size="xs"
                  @click="resetFilters"
                />
              </div>
            </template>

            <UFormField
              label="実行条件"
              class="mb-4"
            >
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <UPopover>
                  <UInput
                    icon="i-lucide-calendar"
                    placeholder="アップロード日時"
                    :model-value="formattedDateRange"
                    :ui="{ base: 'text-left' }"
                    readonly
                  />
                  <template #content>
                    <UCalendar v-model="dateRange" :number-of-months="2" class="p-2" range />
                  </template>
                </UPopover>
                <USelectMenu
                  placeholder="実行ユーザー"
                  icon="i-lucide-user" :items="userNames" multiple
                />
              </div>
            </UFormField>

            <UFormField label="アップロード対象">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <USelectMenu
                  placeholder="リポジトリ"
                  icon="i-lucide-folder" :items="repositoryNames" multiple
                />
                <USelectMenu
                  placeholder="グループ"
                  icon="i-lucide-users" :items="userGroupNames" multiple
                />
                <USelectMenu
                  placeholder="ユーザー"
                  icon="i-lucide-user" :items="userNames" multiple
                />
              </div>
            </UFormField>
          </UCard>

          <!-- テーブル -->
          <UCard variant="outline">
            <template #header>
              <div class="flex items-center justify-between">
                <h2 class="text-xl font-semibold text-highlighted">
                  履歴一覧
                </h2>
                <div class="flex items-center gap-3">
                  <!-- <div class="flex items-center gap-2">
                    <UBadge
                      v-if="hasActiveFilters && matchedCount > 0"
                      :label="`${matchedCount}件ヒット`"
                      color="success"
                      variant="soft"
                    />
                  </div> -->
                  <div class="flex items-center gap-2">
                    <span class="text-md text-muted">表示件数:</span>
                    <USelectMenu
                      v-model="itemsPerPage"
                      :items="itemsPerPageOptions"
                      value-key="value"

                      class="w-24"
                    />
                  </div>
                </div>
              </div>
            </template>

            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-default">
                <!-- ヘッダー行 -->
                <thead>
                  <tr>
                    <th class="w-12 px-4 py-3.5" />
                    <th class="px-4 py-3.5 text-left">
                      <UButton
                        color="neutral"
                        variant="ghost"
                        class="font-semibold -mx-2"
                        :icon="getSortIcon('downloadedAt')"
                        @click="toggleSort('downloadedAt')"
                      >
                        アップロード日時
                      </UButton>
                    </th>
                    <th class="px-4 py-3.5 text-left text-sm">
                      <!-- <UButton
                    color="neutral"
                    variant="ghost"
                    class="font-semibold -mx-2"
                    :icon="getSortIcon('downloaderName')"
                    @click="toggleSort('downloaderName')"
                  >
                    ダウンロード者
                  </UButton> -->
                      アップロード者
                    </th>
                    <th class="px-4 py-3.5 text-left text-sm">
                      <!-- <UButton
                    color="neutral"
                    variant="ghost"
                    class="font-semibold -mx-2"
                    :icon="getSortIcon('userCount')"
                    @click="toggleSort('userCount')"
                  >
                    ユーザー数
                  </UButton> -->
                      ユーザー数
                    </th>
                    <th class="px-4 py-3.5 text-left text-sm">
                      <!-- <UButton
                    color="neutral"
                    variant="ghost"
                    class="font-semibold -mx-2"
                    :icon="getSortIcon('groupCount')"
                    @click="toggleSort('groupCount')"
                  >
                    グループ数
                  </UButton> -->
                      グループ数
                    </th>
                    <th class="px-4 py-3.5 text-left text-sm">
                      <!-- <UButton
                    color="neutral"
                    variant="ghost"
                    class="font-semibold -mx-2"
                    :icon="getSortIcon('status')"
                    @click="toggleSort('status')"
                  >
                    ステータス
                  </UButton> -->
                      ステータス
                    </th>
                    <!-- <th class="px-4 py-3.5 text-left text-sm">
                      操作
                    </th> -->
                    <th />
                  </tr>
                </thead>
                <!-- データ行 -->
                <tbody class="divide-y divide-default">
                  <template v-for="parent in paginatedData" :key="parent.id">
                    <!-- 親行 -->
                    <tr
                      class="hover:bg-elevated/50 transition-colors"
                      :class="{
                        // 'bg-elevated/25': expandedRows.has(parent.id),
                        // 'ring-2 ring-inset ring-success/30 bg-success/5': parent._matchedFields && parent._matchedFields.length > 0,
                        'bg-success/5': parent._matchedFields && parent._matchedFields.length > 0,
                      }"
                    >
                      <!--  -->
                      <td class="px-4 py-3">
                        <div class="flex items-center gap-1">
                          <UIcon
                            v-if="parent._matchedFields && parent._matchedFields.length > 0"
                            name="i-lucide-search-check"
                            class="size-4 text-success shrink-0"
                          />
                          <!-- <UButton
                            v-if="parent.children && parent.children.length > 0"
                            :icon="expandedRows.has(parent.id) ? 'i-lucide-chevron-down' : 'i-lucide-chevron-right'"
                            color="neutral"
                            variant="ghost"
                            size="xs"
                            square
                            @click="toggleExpand(parent.id)"
                          /> -->
                        </div>
                      </td>
                      <!-- アップロード日時 -->
                      <td class="px-4 py-3 text-sm">
                        <!-- <span :class="{ 'font-semibold text-success': parent._matchedFields?.includes('date') }">
                          {{ new Date(parent.downloadedAt).toLocaleString('ja-JP', {
                            year: 'numeric',
                            month: '2-digit',
                            day: '2-digit',
                            hour: '2-digit',
                            minute: '2-digit',
                          }) }}
                        </span> -->
                        <ULink :to="`/upload/1`" class="hover:underline" raw>
                          {{ new Date(parent.downloadedAt).toLocaleString('ja-JP', {
                            year: 'numeric',
                            month: '2-digit',
                            day: '2-digit',
                            hour: '2-digit',
                            minute: '2-digit',
                          }) }}
                        </ULink>
                      </td>
                      <!-- アップロード者 -->
                      <td class="px-4 py-3 text-sm">
                        <div class="flex items-center gap-2">
                          <span :class="{ 'font-semibold text-success': parent._matchedFields?.includes('name') }">
                            {{ parent.downloaderName }}
                          </span>
                          <!-- <UBadge
                            v-if="parent.children && parent.children.length > 0"
                            :label="`+${parent.children.length}`"
                            color="neutral"
                            size="xs"
                            variant="subtle"
                          /> -->
                        </div>
                      </td>
                      <!-- ユーザー数 -->
                      <td class="px-4 py-3 text-sm">
                        <UPopover :content="{ align: 'start' }">
                          <UButton
                            color="neutral"
                            variant="ghost"
                            size="xs"
                            :label="`${parent.userCount}人`"
                            trailing-icon="i-lucide-chevron-down"
                            class="font-normal"
                          />

                          <template #content>
                            <div class="w-72 max-h-80">
                              <!-- リスト -->
                              <div class="max-h-60 overflow-y-auto">
                                <div
                                  v-for="(user, index) in users.slice(0, parent.userCount)"
                                  :key="user.id"
                                  class="px-4 py-2.5 hover:bg-elevated/50 transition-colors"
                                  :class="{ 'border-b border-default': index < parent.userCount - 1 }"
                                >
                                  <div class="flex items-center gap-2">
                                    <!-- <UIcon name="i-lucide-user" class="size-4 text-muted shrink-0" /> -->
                                    <span class="text-sm text-default truncate">{{ user.displayName }}</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </template>
                        </UPopover>
                      </td>
                      <!-- グループ数 -->
                      <td class="px-4 py-3 text-sm">
                        <UPopover :content="{ align: 'start' }">
                          <UButton
                            color="neutral"
                            variant="ghost"
                            size="xs"
                            :label="`${parent.groupCount}グループ`"
                            trailing-icon="i-lucide-chevron-down"
                            class="font-normal"
                          />

                          <template #content>
                            <div class="w-72 max-h-80">
                              <!-- リスト -->
                              <div class="max-h-60 overflow-y-auto">
                                <div
                                  v-for="(group, index) in groups.slice(0, parent.groupCount)"
                                  :key="group.id"
                                  class="px-4 py-2.5 hover:bg-elevated/50 transition-colors"
                                  :class="{ 'border-b border-default': index < parent.groupCount - 1 }"
                                >
                                  <div class="flex items-center gap-2">
                                    <!-- <UIcon name="i-lucide-users" class="size-4 text-muted shrink-0" /> -->
                                    <span class="text-sm text-default truncate">{{ group.displayName }}</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </template>
                        </UPopover>
                      </td>
                      <!-- ステータス -->
                      <td class="px-4 py-3 text-sm">
                        <UBadge
                          :label="statusConfig[parent.status]?.label"
                          :color="statusConfig[parent.status]?.color"
                          variant="subtle"
                        />
                      </td>
                      <!-- 操作 -->
                      <!-- <td class="px-4 py-3 flex items-center gap-2">
                        <UButton
                          label="詳細"
                          icon="i-lucide-info"
                          color="primary"
                          variant="outline"
                          size="sm"
                        />
                      </td> -->
                      <!-- action -->
                      <td>
                        <UDropdownMenu :items="getDropdownActions(parent, 'upload')">
                          <UButton
                            icon="i-lucide-ellipsis-vertical"
                            color="neutral"
                            variant="ghost"
                            aria-label="Actions"
                          />
                        </UDropdownMenu>
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>

              <!-- データがない場合 -->
              <div v-if="paginatedData.length === 0" class="text-center py-12 text-muted">
                <UIcon name="i-lucide-search-x" class="size-12 mx-auto mb-3 opacity-50" />
                <p>検索条件に一致するデータが見つかりませんでした</p>
              </div>
            </div>

            <!-- ページネーション -->
            <template #footer>
              <div class="flex items-center">
                <div class="flex-1 text-sm text-muted">
                  {{ ((currentPage - 1) * itemsPerPage) + 1 }}〜{{ Math.min(currentPage * itemsPerPage, totalItems) }} / {{ totalItems }}件
                </div>
                <UPagination
                  v-model:page="currentPage"
                  :total="totalItems"
                  :items-per-page="itemsPerPage"
                  :sibling-count="1"
                  show-edges
                  class="flex-2 flex justify-center"
                />
                <div class="flex-1" />
              </div>
            </template>
          </UCard>
        </div>
      </template>
    </UTabs>
  </div>
</template>
