<script lang="ts" setup>
import { useToast } from 'vue-toastification'
import type { PropType } from 'vue-demi'
import { getDetails } from '../../../api/client'
import type { Definition, History } from '~/types'

const props = defineProps({
  analysis: { type: Object as PropType<History> },
  modalVisible: Boolean,
})
const emit = defineEmits(['modal:close'])

function closeModal() {
  emit('modal:close')
}

const details = ref<Definition | undefined>()
const toast = useToast()
const definitionLoader = ref<boolean>(true)

const getDefinition = (kind: string) => {
  getDetails(kind).then((resp: Definition) => {
    details.value = resp
    setTimeout(() => {
      definitionLoader.value = false
    }, 1500)
  }).catch(() => {
    toast.error('Something went wrong..')
  })
}

watch(() => props.analysis, (val) => {
  if (val)
    getDefinition(val.Kind)
})
</script>

<template>
  <el-dialog v-model="props.modalVisible" :show-close="false" width="80%" @close="closeModal">
    <template #header="{ close, titleId }">
      <div class="flex flex-row justify-between">
        <h2 :id="titleId" class="text-xl text-base font-bold">
          Quick view of the analysis:
          {{ props.analysis.FileName }}
        </h2>
        <carbon:close class=" cursor-pointer text-2xl" @click="close" />
      </div>
    </template>
    <div class="grid grid-cols-2 gap-4">
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
        <div
          v-for="(predict, i) in props.analysis.Prediction" v-else :key="i"
          class="flex flex-col space-y-2 mt-2"
        >
          <div class="flex flex-row justify-between font-bold">
            <span class="inline-block py-1 px-2 bg-blue-700 text-white text-xs">{{ predict.label }}</span>
            <div>{{ Math.round(predict.probability) }}%</div>
          </div>
          <div class="relative w-full h-1 mb-2 rounded bg-blue-400 p-1">
            <div
              class="absolute top-0 left-0 w-4/6 h-full bg-blue-700 rounded"
              :style="{ width: `${predict.probability}%` }"
            />
          </div>
        </div>
      </div>
      <div class="h-full w-full flex justify-center items-center">
        <img
          class="h-80 object-cover rounded"
          :src="`data:image/jpeg;charset=utf-8;base64,${props.analysis.Image}`" alt=""
        >
      </div>
    </div>
    <div class="p-4 border rounded border-gray-100 mt-2">
      <div class="p-6 rounded bg-white">
        <div class="flex mb-2">
          <span class="inline-block mr-2">
            <carbon-data-enrichment class="text-blue-700" />
          </span>
          <h3 class="text-sm text-blue-600">
            Details
          </h3>
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
              <div
                v-for="(tag, i) in details?.tags" :key="i"
                class="text text-xs text-blue-500 py-1 px-3 rounded-md bg-blue-100"
              >
                {{ tag.name }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>
