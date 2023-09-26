<script lang="ts" setup>
import { Buffer } from 'buffer'
import { useToast } from 'vue-toastification'
import { getAnalyse, getDetails, getHistory } from '../../../../api/client'
import type { Definition, History, Prediction } from '~/types'
import QuickView from '~/analysis/components/quickView.vue'

const route = useRoute()
const router = useRouter()
// const prediction = JSON.parse(router.query.data)
let prediction: Prediction[] | undefined

if (typeof route.query.data === 'string')
  prediction = JSON.parse(route.query.data)

let kind: string = route.query.kind as string

const definitionLoader = ref<boolean>(true)
const historyLoader = ref<boolean>(true)

const details = ref<Definition | undefined>()
const historyList = ref<History[] | undefined>()
const toast = useToast()

const analysisQuickView = ref<History | undefined>()

const isDrawerVisible = ref(false)

const closeDrawer = () => {
  isDrawerVisible.value = false
}
const openDrawer = () => {
  isDrawerVisible.value = true
}

const getDefinition = () => {
  getDetails(kind).then((resp: Definition) => {
    details.value = resp
    setTimeout(() => {
      definitionLoader.value = false
    }, 1500)
  }).catch(() => {
    toast.error('Something went wrong..')
  })
}

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

const handleClickDetails = (row: History) => {
  analysisQuickView.value = row
  modalVisible.value = true
}

const getUserHistory = () => {
  getHistory().then((data: History[]) => {
    historyList.value = data
    setTimeout(() => {
      historyLoader.value = false
    }, 1500)
  }).catch(() => {
    toast.error('Something went wrong..')
  })
}

const getFileFromBase64 = (string64: string, fileName: string) => {
  const trimmedString = string64.replace('dataimage/jpegbase64', '')
  const buffer = Buffer.from(trimmedString, 'base64')
  const type = 'image/jpeg'
  const blob = new Blob([buffer], { type })
  return new File([blob], fileName, { lastModified: new Date().getTime(), type })
}

const sendAnalyseQuery = async (file: any, kind: string, filename: string) => {
  if (!file) {
    toast.info('Aucun fichier sélectionné')
    return
  }

  file = getFileFromBase64(file, filename)

  const formData = new FormData()
  formData.append('image', file)

  getAnalyse(formData, kind)
    .then((data: any) => {
      toast.success('File analysed successfully')

      router.push({
        name: 'analysis-prediction',
        query: {
          data: JSON.stringify(data),
          kind,
        },
      })
    }).catch((err: any) => {
      toast.error(err)
    })
}

const scrollToTop = () => {
  window.scrollTo(0, 0)
}

watch(() => route.query, () => {
  isDrawerVisible.value = false
  definitionLoader.value = true
  historyLoader.value = true
  kind = route.query.kind as string
  if (typeof route.query.data === 'string')
    prediction = JSON.parse(route.query.data)
  getDefinition()
  getUserHistory()
  scrollToTop()
}, { deep: true })

onMounted(() => {
  getDefinition()
  getUserHistory()
})
</script>

<template>
  <div>
    <quick-view :modal-visible="modalVisible" :analysis="analysisQuickView" @modal:close="handleClose" />
    <section class="py-8">
      <div class="container px-4 mx-auto">
        <div class="py-12 bg-blue-700 rounded overflow-hidden">
          <div class="flex flex-wrap">
            <div class="w-full md:w-1/2 px-6 md:pl-12 lg:pr-0 mb-10 md:mb-0">
              <h3 class="mb-2 text-6xl font-medium text-white">
                <span class="text-green-300">Analyse </span>
                <span>another file ?</span>
              </h3>
              <p class="text-xl font-medium text-blue-100">
                Go ahead, streamline your workflow
              </p>
            </div>
            <div class="w-full md:w-1/2 px-12 flex justify-end">
              <el-button @click="openDrawer">
                upload another file
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </section>
    <hr class="w-3/4 mx-auto opacity-75">
    <section class="py-8">
      <div class="container px-4 mx-auto">
        <h2 class="mb-2 text-2xl font-bold text-blue-700 mb-6 border-l border-l-4 border-blue-700 pl-2">
          Analysis : jean marc 2018 hopital grand lyon
        </h2>
        <div class="flex flex-wrap lg:space-x-4">
          <div class="w-full lg:flex-1 px-6 py-10 bg-white border rounded border-gray-100 flex flex-col gap-y-3">
            <div class="flex mb-3 items-center justify-between">
              <h3 class="text-gray-500 flex flex-row">
                <carbon:order-details class="text-blue-700 text-lg text mr-2" />
                <h3 class="text-sm text-blue-600">
                  Accuracy
                </h3>
              </h3>
            </div>
            <div v-if="definitionLoader">
              <el-skeleton :rows="3" />
            </div>
            <div v-for="(predict, i) in prediction" v-else :key="i" class="flex flex-col space-y-2 mt-2">
              <div class="flex flex-row justify-between font-bold">
                <span class="inline-block py-1 px-2 bg-blue-700 text-white text-xs">{{ predict.label }}</span>
                <div>{{ Math.round(predict.probability) }}%</div>
              </div>
              <div class="relative w-full h-1 mb-2 rounded bg-blue-400 p-1">
                <div class="absolute top-0 left-0 w-4/6 h-full bg-blue-700 rounded" :style="{ width: `${predict.probability}%` }" />
              </div>
            </div>
          </div>
          <div class="w-2/3 p-4 border rounded border-gray-100">
            <div class="p-6 rounded bg-white">
              <div class="flex mb-2">
                <span class="inline-block mr-2">
                  <carbon-data-enrichment class="text-blue-700" />
                </span>
                <h3 class="text-sm text-blue-600">
                  Details
                </h3>
                <span class="inline-block ml-auto px-2 py-1 text-xs text-gray-500 bg-gray-50 rounded-full">30 Days</span>
              </div>
              <div v-if="definitionLoader">
                <el-skeleton :rows="5" />
              </div>
              <div v-else>
                <h2 class="text text-base text-blue-700 font-semibold mb-2">
                  What is a {{ details?.category }} ?
                </h2>
                <p class="text text-base text-gray-400">
                  {{ details?.description }}
                </p>
                <div class="mt-2 text-base text-gray-600">
                  <h2 class="text text-base text-blue-700 font-semibold mb-2">
                    Key factors :
                  </h2>
                  <div v-for="(key, i) in details?.key_factors" :key="i">
                    <p class="text text-gray-400">
                      - {{ key.name }}
                    </p>
                  </div>
                </div>
                <div class="mt-2 text-base text-gray-600">
                  <h2 class="text text-base text-blue-700 font-semibold mb-2">
                    Tags
                  </h2>
                  <div class="flex flex-row gap-5">
                    <!-- <div v-for="(tag, i) in details?.tags" :key="i" class="text text-xs text-black py-1 px-3 rounded-md" :style="{ backgroundColor: tag.color }"> -->
                    <div v-for="(tag, i) in details?.tags" :key="i" class="text text-xs text-blue-500 py-1 px-3 rounded-md bg-blue-100">
                      {{ tag.name }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-8">
      <div class="container px-4 mx-auto overflow-x-scroll">
        <h2 class="text-2xl font-bold text-blue-700 mb-6 border-l-4 border-blue-700 pl-2">
          Your last analysis
        </h2>
        <div class="flex flex-nowrap lg:space-x-4 py-4">
          <div v-if="historyLoader" class="flex gap-4">
            <div v-for="i in 10" :key="i">
              <el-skeleton style="width: 300px">
                <template #template>
                  <el-skeleton-item variant="image" style="width: 300px; height: 300px" />
                  <div style="padding: 14px">
                    <el-skeleton-item variant="p" style="width: 50%" />
                    <div
                      style=" display: flex; align-items: center; justify-items: space-between;"
                    >
                      <el-skeleton-item variant="text" style="margin-right: 16px" />
                      <el-skeleton-item variant="text" style="width: 30%" />
                      <el-skeleton-item variant="text" style="margin-right: 16px" />
                      <el-skeleton-item variant="text" style="width: 30%" />
                      <el-skeleton-item variant="text" style="margin-right: 16px" />
                    </div>
                  </div>
                </template>
              </el-skeleton>
            </div>
          </div>

          <div v-for="(history, i) in historyList" :key="i" class="inline-block p-4 border rounded border-gray-100">
            <div class="w-96">
              <div class="p-4 bg-white rounded">
                <div class="relative h-40 w-full mb-4">
                  <img class="w-full h-full object-cover rounded" :src="`data:image/jpeg;charset=utf-8;base64,${history.Image}`" alt="">
                  <span class="absolute top-0 right-0 py-1 px-2 mt-2 mr-2 bg-blue-700 rounded text-xs text-white">{{ history.Kind }}</span>
                </div>
                <div class="flex mb-6 justify-between items-center">
                  <div>
                    <h3 class="text-sm font-medium">
                      {{ history.FileName }}
                    </h3>
                    <span class="text-xs text-gray-500">{{ history.ID }}</span>
                  </div>
                  <button class="ml-auto p-2 bg-blue-200 rounded" @click="sendAnalyseQuery(history.Image, history.Kind, history.FileName)">
                    <carbon-reset class="text-blue-700" />
                  </button>
                </div>
                <div class="flex mb-2 justify-between items-center">
                  <h4 class="text-xs font-medium">
                    Analyse date
                  </h4>
                  <span class="inline-block py-1 px-2 rounded-full bg-green-50 text-xs text-green-500">08 March 2021</span>
                </div>
                <div class="flex mb-5 justify-between items-center">
                  <h4 class="text-xs font-medium">
                    Last Update
                  </h4>
                  <span class="text-xs text-blue-500 font-medium">6 days ago</span>
                </div>
                <div class="flex justify-end border-t border-gray-50 pt-4">
                  <a class="py-2 px-3 bg-blue-700 hover:bg-blue-600 rounded text-xs text-white transition duration-200" href="#" @click="handleClickDetails(history)">See Details</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
  <import-drawer :is-visible="isDrawerVisible" @close="closeDrawer" />
</template>

<style scoped>

</style>

<route lang="yaml">
meta:
  layout: dashboard
  requiresAuth: true
</route>
