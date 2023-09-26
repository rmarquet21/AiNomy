<script lang="ts" setup>
import { useToast } from 'vue-toastification'
import { getHistory } from '../../../../api/client'

const historyList = ref()
const historyLoader = ref<boolean>(true)
const toast = useToast()
const filter = ref('')

const isDrawerVisible = ref(false)
const getUserHistory = () => {
  getHistory().then((data: any) => {
    historyList.value = data
    setTimeout(() => {
      historyLoader.value = false
    }, 1500)
  }).catch(() => {
    toast.error('Something went wrong..')
  })
}

onMounted(() => {
  getUserHistory()
})

const closeDrawer = () => {
  isDrawerVisible.value = false
}
const openDrawer = () => {
  isDrawerVisible.value = true
}
</script>

<template>
  <div class="flex flex-end w-100 p-2 justify-between">
    <span v-if="!historyLoader && historyList" class="font-medium">
      You have <b>{{ historyList.length }} analyse{{ historyList.length === 1 ? '' : 's' }}</b>
    </span>
    <span v-else-if="!historyLoader && !historyList" class="font-medium">
      You have <b>0 analyses</b>
    </span>
    <span v-else>
      Fetching your analyses...
    </span>
    <div class="h-full space-x-4 flex">
      <el-input
        v-model="filter"
        placeholder="Search files"
      />
      <el-button type="primary" @click="openDrawer">
        Importer une analyse
      </el-button>
    </div>
  </div>
  <import-drawer :is-visible="isDrawerVisible" @close="closeDrawer" />
  <analysis-table :history-list="historyList" :is-loading="historyLoader" :filter="filter" />
</template>

<route lang="yaml">
meta:
  layout: dashboard-history
  requiresAuth: true
</route>
