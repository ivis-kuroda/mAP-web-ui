<script setup lang="ts">
import { upperFirst } from 'scule'

import type { DropdownMenuItem, TableColumn, TableRow } from '@nuxt/ui'

import { UButton, UCheckbox, UDropdownMenu, ULink } from '#components'

const { repositories, groups } = useDataStore()
const localePath = useLocalePath()
const data = ref<Group[]>(groups)
const toast = useToast()
const { copy } = useClipboard()

const columnNameMap = {
  displayName: $t('group.name-column'),
  publicStatus: $t('group.public-status'),
  joinCondition: $t('group.join-condition'),
  memberVisibility: $t('group.member-visibility'),
} as const

type GroupTableColumn = TableColumn<Group>
const columns = computed<GroupTableColumn[]>(() => [
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
      const name = row.original.displayName
      return h(ULink,
        {
          to: localePath(`/groups/${row.original.id}`),
          class: 'font-bold hover:underline inline-flex items-center',
        },
        [
          h('span', name),
        ])
    },
    enableHiding: false,
  },
  {
    accessorKey: 'publicStatus',
    header: ({ column }) => sortableHeader(column, columnNameMap.publicStatus),
    cell: ({ row }) => {
      return row.original.isPublic
        ? $t('group.public-badge')
        : $t('group.private-badge')
    },
    sortingFn: (rowA, rowB) => {
      return Number(rowA.original.isPublic) - Number(rowB.original.isPublic)
    },
  },
  {
    accessorKey: 'memberVisibility',
    header: ({ column }) => sortableHeader(column, columnNameMap.memberVisibility),
    cell: ({ row }) => {
      const visibility = row.original.memberVisibility
      const labelMap = {
        public: $t('group.members-public'),
        private: $t('group.members-private'),
        hidden: $t('group.members-hidden'),
      } as const

      return labelMap[visibility]
    },
    sortingFn: (rowA, rowB) => {
      const orderMap = {
        public: 2,
        private: 0,
        hidden: 1,
      } as const

      const a = orderMap[rowA.original.memberVisibility]
      const b = orderMap[rowB.original.memberVisibility]
      return a - b
    },
  },
  {
    accessorKey: 'members',
    header: ({ column }) => sortableHeader(column, $t('group.member-count')),
    cell: ({ row }) => {
      const count = row.original.members?.length || 0
      return h('span', $t('group.members-count', { count }))
    },
  },
  {
    id: 'actions',
    enableHiding: false,
    cell: ({ row }) => {
      return h(
        h(
          // @ts-expect-error: props type mismatch
          UDropdownMenu,
          {
            'content': {
              align: 'end',
            },
            'items': getRowItems(row),
            'aria-label': 'Actions dropdown',
          },
          () =>
            h(UButton, {
              'icon': 'i-lucide-ellipsis-vertical',
              'color': 'neutral',
              'variant': 'ghost',
              'size': 'sm',
              'class': 'ml-auto',
              'aria-label': 'Actions dropdown',
            }),
        ),
      )
    },
  },
])

function getRowItems(row: TableRow<Group>): DropdownMenuItem[] {
  return [
    {
      type: 'label',
      label: $t('table.actions-label'),
    },
    {
      label: $t('group.copy-group-id'),
      icon: 'i-lucide-clipboard-copy',
      onSelect() {
        copy(row.original.id)

        toast.add({
          title: $t('group.copy-group-id-clipboard'),
          color: 'success',
          icon: 'i-lucide-circle-check',
        })
      },
    },
    {
      label: $t('group.edit'),
      icon: 'i-lucide-square-pen',
    },
    {
      label: $t('group.show-details'),
      icon: 'i-lucide-eye',
    },
    {
      label: $t('group.view-in-cloud-gateway'),
      icon: 'i-lucide-external-link',
    },
    {
      type: 'separator',
    },
    {
      label: $t('group.delete'),
      icon: 'i-lucide-trash',
      color: 'error',
    },
  ]
}

const table = useTemplateRef('table')

const columnVisibility = ref({ id: false })

type Column = Parameters<
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  Extract<GroupTableColumn['header'], (...arguments_: any) => any>
>[0]['column']

function sortableHeader(column: Column, label: string) {
  const sortDirection = column.getIsSorted()
  const iconSet = {
    asc: 'i-lucide-arrow-down-a-z',
    desc: 'i-lucide-arrow-up-a-z',
    none: 'i-lucide-arrow-up-down',
  } as const

  return h(UButton, {
    color: sortDirection ? 'primary' : 'neutral',
    variant: 'ghost',
    size: 'xs',
    label,
    icon: sortDirection ? iconSet[sortDirection] : iconSet.none,
    class: 'font-medium cursor-pointer',
    onClick() {
      if (sortDirection === 'asc') column.toggleSorting(true) // to desc
      else if (sortDirection === 'desc') column.clearSorting() // to default
      else column.toggleSorting(false) // to asc
    },
  })
}

const sorting = ref([{ id: 'id', desc: false }])

const page = ref(1)
const pageSize = ref(20)
const pageOptions = ref([20, 50, 100])

const globalFilter = ref('')
const filteredData = computed(() => {
  let result = data.value

  // グローバルフィルター
  if (globalFilter.value) {
    const f = globalFilter.value.toLowerCase()
    result = result.filter(item => item.displayName.toLowerCase().includes(f))
  }

  // リポジトリフィルター
  if (filterStatus.repositoryFilter && selectedRepositories.value.length > 0) {
    result = result.filter((item) => {
      return selectedRepositories.value.includes(item.displayName)
    })
  }

  // 公開状態フィルター
  if (filterStatus.publicStatusFilter && selectedPublicStatus.value.length > 0) {
    result = result.filter((item) => {
      const statusLabel = item.isPublic ? $t('group.public-badge') : $t('group.private-badge')
      return selectedPublicStatus.value.includes(statusLabel)
    })
  }

  // メンバー公開フィルター
  if (filterStatus.memberVisibilityFilter && selectedMemberVisibilities.value.length > 0) {
    result = result.filter((item) => {
      const labelMap = {
        public: $t('group.members-public'),
        private: $t('group.members-private'),
        hidden: $t('group.members-hidden'),
      } as const
      const visibilityLabel = labelMap[item.memberVisibility]
      return selectedMemberVisibilities.value.includes(visibilityLabel)
    })
  }

  return result
})

const pagedData = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

const displayInfo = computed(() => {
  const total = filteredData.value.length
  const start = (page.value - 1) * pageSize.value + 1
  const end = Math.min(page.value * pageSize.value, total)

  return $t('table.display-info-text', { start, end, total })
})

const isZero = ref(false) // data.value.length > 0
const isCreatable = true

const filterStatus = reactive({
  repositoryFilter: false,
  publicStatusFilter: false,
  memberVisibilityFilter: false,
})

const filterItems = computed<DropdownMenuItem[]>(() => [
  {
    label: $t('group.repository-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.repositoryFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.repositoryFilter = checked
    },
  },
  {
    label: $t('group.public-status'),
    type: 'checkbox' as const,
    checked: filterStatus.publicStatusFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.publicStatusFilter = checked
    },
  },
  {
    label: $t('group.member-visibility-filter'),
    type: 'checkbox' as const,
    checked: filterStatus.memberVisibilityFilter,
    onUpdateChecked(checked: boolean) {
      filterStatus.memberVisibilityFilter = checked
    },
  },
])

const selectedRepositories = ref<string[]>([])
const selectedPublicStatus = ref<string[]>([])
const selectedMemberVisibilities = ref<string[]>([])

watch([selectedRepositories, selectedPublicStatus, selectedMemberVisibilities, globalFilter],
  () => {
    page.value = 1 // フィルター変更時は1ページ目に戻る
  })

const repositoryNames = ref(repositories.map(repo => repo.displayName))
const publicStatus = ref([$t('group.public-badge'), $t('group.private-badge')])
const memberVisibilities = ref([
  $t('group.members-public'), $t('group.members-private'), $t('group.members-hidden'),
])

const rowSelection = ref<Record<string, boolean>>({})
const selectedGroups = computed(() => {
  const selectedIds = new Set(Object.entries(rowSelection.value)
    .filter(([, isSelected]) => isSelected)
    .map(([id]) => id))

  return data.value.filter((group, index) => selectedIds.has(index.toString()))
})

function onSelect(first: Event | TableRow<Group>, second: Event | TableRow<Group>) {
  const row = 'original' in first ? first : second as TableRow<Group>
  row.toggleSelected(!row.getIsSelected())
}
</script>

<template>
  <div class="flex justify-center p-6">
    <UCard class="w-full max-w-6xl">
      <h2 class="text-2xl font-semibold">
        {{ $t('group.list-title') }}
      </h2>
      <div v-if="!isZero">
        <div class="flex justify-between items-center mt-4">
          <UButton
            v-if="isCreatable"
            color="primary" :label="$t('group.create-button')"
            variant="solid" icon="i-lucide-plus" :to="localePath('/groups/new')" class="mb-4"
          />

          <UModal
            v-if="selectedGroups.length > 0"
            :title="$t('group.delete-confirmation-title', { count: selectedGroups.length })"
            :description="$t('group.delete-confirmation-description')"
            :ui="{ footer: 'justify-end' }" :close="false"
          >
            <UButton
              color="error" variant="outline" class="mb-4 ml-auto"
              :label="$t('group.delete-selected-groups-button')"
            />
            <template #body>
              <div class="flex flex-col justify-between items-center mt-4">
                <div class="gap-4 text-center">
                  <div v-for="group in selectedGroups" :key="group.id" class="mb-2">
                    <p>
                      {{ group.displayName }}
                      ({{ $t('group.members-count', { count: group.members?.length || 0 }) }})
                    </p>
                  </div>
                </div>
              </div>
            </template>
            <template #footer="{ close }">
              <div class="flex gap-2">
                <UButton
                  color="neutral" :label="$t('modal.cancel-button')"
                  variant="subtle" @click="close"
                />
                <UButton color="error" :label="$t('modal.delete-button')" @click="close" />
              </div>
            </template>
          </UModal>
        </div>

        <div class="flex justify-between mb-4">
          <div>
            <div>
              <UInput
                v-model="globalFilter" :placeholder="$t('search-placeholder')"
                icon="i-lucide-search" class="max-w-sm pr-4"
              />
              <UDropdownMenu :items="filterItems">
                <UButton
                  :label="$t('table.add-filter-button')" color="neutral"
                  trailing-icon="i-lucide-chevron-down" variant="outline"
                />
              </UDropdownMenu>
            </div>
            <div class="flex flex-col">
              <USelectMenu
                v-if="filterStatus.repositoryFilter"
                v-model="selectedRepositories"
                :placeholder="$t('group.repository-filter')"
                icon="i-lucide-folder"
                :items="repositoryNames"
                class="mt-2"
                multiple
              />
              <USelectMenu
                v-if="filterStatus.publicStatusFilter"
                v-model="selectedPublicStatus"
                :placeholder="$t('group.public-status')"
                :items="publicStatus"
                :search-input="false"
                class="mt-2"
                multiple
              />
              <USelectMenu
                v-if="filterStatus.memberVisibilityFilter"
                v-model="selectedMemberVisibilities"
                :placeholder="$t('group.member-visibility-filter')"
                :items="memberVisibilities" :search-input="false" class="mt-2" multiple
              />
            </div>
          </div>

          <div class="flex justify-end items-center space-x-2 mb-2">
            <UDropdownMenu
              :items="
                table?.tableApi
                  ?.getAllColumns()
                  .filter((column) => column.getCanHide())
                  .map((column) => ({
                    label: upperFirst(column.id),
                    type: 'checkbox' as const,
                    checked: column.getIsVisible(),
                    onUpdateChecked(checked: boolean) {
                      table?.tableApi?.getColumn(column.id)?.toggleVisibility(!!checked)
                    },
                    onSelect(e: Event) {
                      e.preventDefault()
                    },
                  }))
              "
              :content="{ align: 'end' }"
            >
              <UButton
                color="neutral" variant="outline"
                trailing-icon="i-lucide-chevron-down" :label="$t('table.display-item-label')"
              />
            </UDropdownMenu>

            <div class="flex items-center space-x-2">
              <span class="text-sm text-gray-600">{{ $t('table.display-count-label') }}</span>
              <USelect v-model="pageSize" :items="pageOptions" class="w-24" />
            </div>
          </div>
        </div>

        <div>
          <UTable
            ref="table"
            v-model:column-visibility="columnVisibility"
            v-model:sorting="sorting"
            v-model:row-selection="rowSelection"
            :data="pagedData" :columns="columns" @select="onSelect"
          />

          <div class="flex justify-center mt-4">
            <div class="flex-1 text-gray-500 text-sm">
              {{ displayInfo }}
            </div>
            <div class="flex-2 flex justify-center">
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
      <div v-if="isZero">
        <UEmpty
          :title="$t('group.no-users-title')"
          :actions="[{
            icon: 'i-lucide-plus',
            label: $t('group.create-button'),
            to: 'groups/new',
          }, {
            icon: 'i-lucide-refresh-cw',
            label: $t('reload-button'),
            color: 'neutral',
            variant: 'subtle',
          }]"
        />
      </div>
    </UCard>
  </div>
  <USwitch v-model="isZero" label="test用" />
</template>
