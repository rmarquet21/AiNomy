<script lang="ts" setup>
import { ref } from 'vue'
import { useToast } from 'vue-toastification'
import { getAnalyse } from '../../../api/client'

defineProps<{
  isVisible: boolean
}>()

const emit = defineEmits(['close'])
const kind = ref('pneumonia')
const file = ref()
const router = useRouter()
const toast = useToast()

const sendAnalyseQuery = async () => {
  if (!file.value) {
    toast.info('Aucun fichier sélectionné')
    return
  }

  const formData = new FormData()
  formData.append('image', file.value.raw)

  getAnalyse(formData, kind.value)
    .then((data: any) => {
      toast.success('File analysed successfully')

      router.push({
        name: 'analysis-prediction',
        query: {
          data: JSON.stringify(data),
          kind: kind.value,
        },
      })
    }).catch((err: any) => {
      toast.error(err)
    })
}

const beforeUpload = (uploadedFile: any) => {
  const allowedType = ['image/jpeg', 'image/png']
  if (allowedType.includes(uploadedFile.type)) {
    toast.info('Le fichier doit être de type JPEG')
    return false
  }
  if (uploadedFile.size > 1024 * 1024) {
    toast.info('La taille du fichier doit être inférieure à 1MB')
    return false
  }
  file.value = uploadedFile
  return true
}
</script>

<template>
  <el-drawer
    :model-value="isVisible"
    title="Import your analyse"
    @close="emit('close')"
  >
    <div>
      <el-radio-group v-model="kind" class="mb-4">
        <el-radio label="pneumonia" size="large" border>
          pneumonia
        </el-radio>
        <el-radio label="alzheimer" size="large" border>
          alzheimer
        </el-radio>
      </el-radio-group>
    </div>
    <el-form @submit.prevent="sendAnalyseQuery">
      <el-upload
        class="upload-demo w-full"
        drag
        action=""
        accept="*"
        :multiple="false"
        :limit="1"
        :auto-upload="false"
        @change="beforeUpload"
      >
        <el-icon class="el-icon--upload">
          <carbon:cloud-upload />
        </el-icon>
        <div class="el-upload__text">
          click to upload
        <!-- Drop CSV file here or <em>click to upload</em> -->
        </div>
        <template #tip>
          <div class="el-upload__tip">
            jpg file with a size less than 1mb
          </div>
        </template>
      </el-upload>
      <el-button type="primary" class="w-full" native-type="submit">
        submit
      </el-button>
    </el-form>
  </el-drawer>
</template>
