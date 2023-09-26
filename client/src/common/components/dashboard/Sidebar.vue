<script lang="ts" setup>
import { isDark, toggleDark } from '~/common/composables'
</script>

<template>
  <el-menu
    class="h-full flex flex-col w-52"
    default-active="1"
    collapse
  >
    <el-menu-item index="1">
      <el-icon>
        <carbon:ica-2d />
      </el-icon>
      <template #title>
        Analyses
      </template>
    </el-menu-item>
    <el-menu-item index="2">
      <el-icon>
        <carbon:settings />
      </el-icon>
      <template #title>
        Paramètres ( comming soon )
      </template>
    </el-menu-item>
    <el-menu-item index="3" @click="toggleDark()">
      <el-icon>
        <carbon-moon v-if="isDark" />
        <carbon-sun v-else />
      </el-icon>
      <template #title>
        Dark mode
      </template>
    </el-menu-item>
  </el-menu>
</template>
