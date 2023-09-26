<!-- eslint-disable no-console -->
<script lang="ts" setup>
import type { History } from '~/types'
import QuickView from '~/analysis/components/quickView.vue'

const props = defineProps({
  historyList: Array<History>,
  isLoading: Boolean,
  filter: {
    type: String,
    default: '',
  },
})

const pageSize = ref(10)
const page = ref(1)
const analysisQuickView = ref<History | undefined>()

const filteredHistory = computed(() => {
  if (props.filter === '') {
    return props.historyList
  }
  else {
    return props.historyList.filter((history) => {
      return history.FileName.toLowerCase().includes(props.filter.toLowerCase())
    })
  }
})

const setPage = (newPage: number) => {
  page.value = newPage
}

const pagedTableData = computed(() => {
  return filteredHistory?.value?.slice(pageSize.value * page.value - pageSize.value, pageSize.value * page.value) ?? []
})

const useModal = () => {
  const modalVisible = ref<boolean>(false)
  const handleClose = () => {
    modalVisible.value = false
  }

  return {
    handleClose,
    modalVisible,
  }
}

const { modalVisible, handleClose } = useModal()
const handleView = ($index: number, row: any) => {
  console.log('Handle view', $index, row)
  analysisQuickView.value = row
  modalVisible.value = true
}
const handleDelete = ($index: number, row: any) => {
  console.log('Handle edit', $index, row)
}
</script>

<template>
  <quick-view :modal-visible="modalVisible" :analysis="analysisQuickView" @modal:close="handleClose" />
  <el-table v-loading="props.isLoading" :data="pagedTableData" border style="width: 100%" height="80vh">
    <el-table-column prop="ID" label="ID" />
    <el-table-column prop="FileName" label="Name" />
    <el-table-column prop="Kind" label="Kind" />
    <el-table-column label="Operations" align="right">
      <template #default="scope">
        <el-button size="small" @click="handleView(scope.$index, scope.row)">
          view
        </el-button>
        <el-button
          size="small"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)"
        >
          delete
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <div v-if="filteredHistory" class="flex items-center justify-center mt-2">
    <el-pagination layout="prev, pager, next" :total="filteredHistory.length" background @current-change="setPage" />
  </div>
</template>
